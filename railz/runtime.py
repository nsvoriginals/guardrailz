from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

import streamlit as st

from railz.catalog import DEFAULT_MODEL
from railz.engine import NemoEngine, has_api_key
from railz.mock import mock_trace
from railz.trace import Trace


@lru_cache(maxsize=1)
def _engine() -> NemoEngine:
    return NemoEngine()


def run_turn(
    messages: List[dict],
    model: str = DEFAULT_MODEL,
    rails_on: bool = True,
    force_mock: bool = False,
) -> Trace:
    if force_mock or not has_api_key():
        preset = "on_topic"
        user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        lowered = user.lower()
        if any(k in lowered for k in ["ignore all previous", "system prompt", "you are now dan", "bypass your safety", "no rules"]):
            preset = "multiturn" if "bypass" in lowered else "jailbreak"
        elif "@" in user or "4111" in user or "ssn" in lowered:
            preset = "pii"
        elif any(k in lowered for k in ["poem", "haiku", "joke", "song", "story about"]):
            preset = "off_topic"
        elif any(k in lowered for k in ["worthless", "stupid", "idiot", "hurt"]):
            preset = "toxic"
        trace = mock_trace(preset, model)
        trace.user_input = user
        return trace

    return _engine().run(messages, model=model, rails_on=rails_on)


def run_preset(preset_id: str, model: str = DEFAULT_MODEL) -> Trace:
    return mock_trace(preset_id, model)


def engine_badge(force_mock: bool = False) -> tuple[str, str]:
    if force_mock or not has_api_key():
        return "mock", "Demo · scripted"
    return "live", "Live · Groq"
