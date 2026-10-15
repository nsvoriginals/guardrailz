from __future__ import annotations

import asyncio
import os
import time
from typing import Any, Dict, List, Optional

from railz.catalog import DEFAULT_MODEL
from railz.trace import Trace, build_trace


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass


def has_api_key() -> bool:
    _load_env()
    return bool(os.environ.get("GROQ_API_KEY"))


def _run(coro: Any) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class NemoEngine:
    """Real NeMo Guardrails runtime with tracing enabled."""

    def __init__(self, config_path: str = "railz/config") -> None:
        self.config_path = config_path
        self._rails: Dict[str, Any] = {}

    def _get_rails(self, model: str) -> Any:
        if model in self._rails:
            return self._rails[model]
        from nemoguardrails import LLMRails, RailsConfig

        config = RailsConfig.from_path(self.config_path)
        if config.models:
            config.models[0].model = model
        rails = LLMRails(config, verbose=False)
        self._rails[model] = rails
        return rails

    def _options(self) -> Any:
        from nemoguardrails.rails.llm.options import (
            GenerationLogOptions,
            GenerationOptions,
        )

        return GenerationOptions(
            log=GenerationLogOptions(
                activated_rails=True,
                llm_calls=True,
                internal_events=True,
                colang_history=True,
            ),
        )

    def run(self, messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, rails_on: bool = True) -> Trace:
        user_input = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        started = time.perf_counter()
        try:
            if not rails_on:
                return self._run_bypass(messages, model, user_input, started)

            res = _run(self._generate(messages, model))
            duration = time.perf_counter() - started
            log = getattr(res, "log", None)
            response = res.response if isinstance(res.response, dict) else {"content": str(res.response)}
            output = response.get("content", "")

            baseline_output = None
            baseline_duration = 0.0
            blocked = self._is_blocked(log)

            if blocked:
                baseline_output, baseline_duration = self._baseline(messages, model, started)

            trace = build_trace(
                interaction_log=log,
                stats=getattr(log, "stats", None),
                user_input=user_input,
                output=output,
                model=model,
                engine="nemo",
                baseline_output=baseline_output,
                baseline_duration=baseline_duration,
            )
            if not trace.total_duration:
                trace.total_duration = round(duration, 3)
            return trace
        except Exception as exc:  # pragma: no cover - surfaced in the UI
            return self._error_trace(model, user_input, exc, time.perf_counter() - started)

    async def _generate(self, messages: List[Dict[str, str]], model: str) -> Any:
        rails = self._get_rails(model)
        from nemoguardrails.tracing.interaction_types import (
            InteractionOutput,
            extract_interaction_log,
        )

        res = await rails.generate_async(messages=messages, options=self._options())
        self._last_extract = extract_interaction_log

        log = getattr(res, "log", None)
        if log is not None and getattr(log, "trace", None):
            pass
        elif log is not None:
            entry = InteractionOutput(
                id=getattr(log, "id", "turn"),
                input=messages[-1]["content"] if messages else "",
                output=res.response.get("content", "") if isinstance(res.response, dict) else str(res.response),
            )
            extracted = extract_interaction_log(
                entry, log, span_format="opentelemetry", enable_content_capture=True
            )
            log.trace = extracted.trace
            if not getattr(log, "events", None):
                log.events = extracted.events
        return res

    def _run_bypass(self, messages: List[Dict[str, str]], model: str, user_input: str, started: float) -> Trace:
        rails = self._get_rails(model)
        res = _run(rails.generate_async(messages=messages, options=None))
        duration = time.perf_counter() - started
        output = res.get("content", "") if isinstance(res, dict) else str(res)
        return Trace(
            engine="nemo",
            model=model,
            user_input=user_input,
            output=output,
            blocked=False,
            total_duration=round(duration, 3),
            generation_duration=round(duration, 3),
        )

    def _baseline(self, messages: List[Dict[str, str]], model: str, started: float) -> tuple[Optional[str], float]:
        try:
            rails = self._get_rails(model)

            async def _plain() -> str:
                res = await rails.llm.generate_async(messages)
                return getattr(res, "content", "") or ""

            t0 = time.perf_counter()
            text = _run(_plain())
            return text, round(time.perf_counter() - t0, 3)
        except Exception:
            return None, 0.0

    @staticmethod
    def _is_blocked(log: Any) -> bool:
        for rail in getattr(log, "activated_rails", []) or []:
            if getattr(rail, "stop", False):
                return True
            for action in getattr(rail, "executed_actions", []) or []:
                verdict = action.return_value
                if isinstance(verdict, dict) and verdict.get("blocked"):
                    return True
                if hasattr(verdict, "blocked") and getattr(verdict, "blocked"):
                    return True
        return False

    @staticmethod
    def _error_trace(model: str, user_input: str, exc: Exception, duration: float) -> Trace:
        return Trace(
            engine="nemo",
            model=model,
            user_input=user_input,
            output="",
            blocked=False,
            total_duration=round(duration, 3),
            error=f"{type(exc).__name__}: {exc}",
        )
