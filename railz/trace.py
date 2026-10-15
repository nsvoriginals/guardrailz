from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMCall(BaseModel):
    task: str = "unknown"
    model: str = "unknown"
    provider: str = "unknown"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration: float = 0.0
    prompt: str = ""
    completion: str = ""
    from_cache: bool = False


class ActionRun(BaseModel):
    name: str
    label: str = ""
    duration: float = 0.0
    params: Dict[str, Any] = Field(default_factory=dict)
    blocked: bool = False
    reason: str = ""
    score: float = 0.0
    matches: List[Dict[str, Any]] = Field(default_factory=list)
    detail: Dict[str, Any] = Field(default_factory=dict)
    llm_calls: List[LLMCall] = Field(default_factory=list)


class RailRun(BaseModel):
    type: str = "input"
    name: str = ""
    status: str = "passed"
    decisions: List[str] = Field(default_factory=list)
    duration: float = 0.0
    reason: str = ""
    label: str = ""
    actions: List[ActionRun] = Field(default_factory=list)


class SpanNode(BaseModel):
    id: str
    parent_id: Optional[str] = None
    kind: str = "internal"
    name: str = "span"
    detail: str = ""
    start: float = 0.0
    duration: float = 0.0
    status: str = "info"
    meta: Dict[str, Any] = Field(default_factory=dict)
    depth: int = 0
    children: List[str] = Field(default_factory=list)


class Trace(BaseModel):
    id: str = Field(default_factory=lambda: f"tr_{int(time.time() * 1000) % 10_000_000}")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    engine: str = "mock"
    model: str = "openai/gpt-oss-20b"
    user_input: str = ""
    output: str = ""
    blocked: bool = False
    blocked_by: str = ""
    block_reason: str = ""
    total_duration: float = 0.0
    input_rails_duration: float = 0.0
    output_rails_duration: float = 0.0
    generation_duration: float = 0.0
    llm_calls_count: int = 0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    rails: List[RailRun] = Field(default_factory=list)
    spans: List[SpanNode] = Field(default_factory=list)
    events: List[str] = Field(default_factory=list)
    baseline_output: Optional[str] = None
    baseline_duration: float = 0.0
    error: Optional[str] = None

    def span_map(self) -> Dict[str, SpanNode]:
        return {s.id: s for s in self.spans}

    def root_spans(self) -> List[SpanNode]:
        ids = {s.id for s in self.spans}
        return [s for s in self.spans if not s.parent_id or s.parent_id not in ids]

    def waterfall_span(self) -> float:
        return max((s.start + s.duration for s in self.spans), default=0.0) or self.total_duration or 0.001


RAIL_DISPLAY = {
    "check jailbreak": ("Input rail", "shield", "Jailbreak / prompt injection"),
    "check sensitive data": ("Input rail", "key_off", "Sensitive data / PII"),
    "check on topic": ("Input rail", "topic", "Topical guardrail"),
    "self check output": ("Output rail", "fact_check", "Self-check output"),
    "check toxicity": ("Output rail", "gavel", "Moderation / toxicity"),
}

ACTION_DISPLAY = {
    "railz_check_jailbreak": "Jailbreak detector",
    "railz_check_sensitive_data": "PII scanner",
    "railz_check_topic": "Topic router",
    "railz_self_check_output": "Output self-check",
    "railz_check_toxicity": "Toxicity classifier",
}


def _llm_call_from_info(info: Any) -> LLMCall:
    return LLMCall(
        task=info.task or "unknown",
        model=info.llm_model_name or "unknown",
        provider=info.llm_provider_name or "unknown",
        prompt_tokens=info.prompt_tokens or 0,
        completion_tokens=info.completion_tokens or 0,
        total_tokens=info.total_tokens or 0,
        duration=info.duration or 0.0,
        prompt=info.prompt or "",
        completion=info.completion or "",
        from_cache=bool(getattr(info, "from_cache", False)),
    )


def _action_from_executed(executed: Any) -> ActionRun:
    verdict = executed.return_value
    blocked = False
    reason = ""
    score = 0.0
    matches: List[Dict[str, Any]] = []
    detail: Dict[str, Any] = {}
    if isinstance(verdict, BaseModel):
        data = verdict.model_dump()
    elif isinstance(verdict, dict):
        data = verdict
    else:
        data = {}
    if data:
        blocked = bool(data.get("blocked", False))
        reason = str(data.get("reason", "") or "")
        score = float(data.get("score", 0.0) or 0.0)
        matches = list(data.get("matches", []) or [])
        detail = dict(data.get("detail", {}) or {})

    return ActionRun(
        name=executed.action_name,
        label=ACTION_DISPLAY.get(executed.action_name, executed.action_name),
        duration=executed.duration or 0.0,
        params={k: v for k, v in (executed.action_params or {}).items() if isinstance(v, (str, int, float, bool))},
        blocked=blocked,
        reason=reason,
        score=round(score, 2),
        matches=matches,
        detail=detail,
        llm_calls=[_llm_call_from_info(c) for c in (executed.llm_calls or [])],
    )


def _rail_from_activated(activated: Any) -> RailRun:
    actions = [_action_from_executed(a) for a in (activated.executed_actions or [])]
    stopped = bool(activated.stop) or any("stop" in str(d).lower() for d in (activated.decisions or []))
    blocked = any(a.blocked for a in actions) or stopped
    reason = next((a.reason for a in actions if a.reason), "")
    label = next((a.label for a in actions if a.matches or a.detail), "")
    return RailRun(
        type=activated.type or "input",
        name=activated.name,
        status="blocked" if blocked else "passed",
        decisions=list(activated.decisions or []),
        duration=activated.duration or 0.0,
        reason=reason,
        label=label,
        actions=actions,
    )


def build_spans(interaction_log: Any) -> List[SpanNode]:
    spans: List[SpanNode] = []
    by_id: Dict[str, SpanNode] = {}

    for span in interaction_log.trace:
        cls = type(span).__name__
        meta: Dict[str, Any] = {}
        detail = ""
        status = "info"

        if cls == "InteractionSpan":
            kind = "interaction"
            name = "Guardrails request"
            detail = "Top-level span for the whole turn"
        elif cls == "RailSpan":
            kind = "rail"
            rail_name = getattr(span, "rail_name", "rail")
            name = rail_name
            decisions = getattr(span, "rail_decisions", None) or []
            stopped = bool(getattr(span, "rail_stop", False)) or any("stop" in str(d).lower() for d in decisions)
            status = "blocked" if stopped else "passed"
            detail = ", ".join(str(d) for d in decisions) or "evaluated"
            meta = {"rail_type": getattr(span, "rail_type", "")}
        elif cls == "ActionSpan":
            kind = "action"
            action_name = getattr(span, "action_name", "action")
            name = ACTION_DISPLAY.get(action_name, action_name)
            count = getattr(span, "llm_calls_count", 0)
            detail = f"{count} LLM call(s)" if count else "local check"
            meta = {"action_name": action_name}
        elif cls == "LLMSpan":
            kind = "llm"
            operation = getattr(span, "operation_name", "chat")
            model = getattr(span, "request_model", "")
            name = model or operation
            detail = operation
            tokens = getattr(span, "usage_total_tokens", None)
            status = "error" if getattr(span, "error", False) else "info"
            meta = {
                "provider": getattr(span, "provider_name", ""),
                "prompt_tokens": getattr(span, "usage_input_tokens", None) or 0,
                "completion_tokens": getattr(span, "usage_output_tokens", None) or 0,
                "total_tokens": tokens or 0,
                "task": operation,
            }
        else:
            kind = "internal"
            name = getattr(span, "name", cls)
            detail = cls

        node = SpanNode(
            id=span.span_id,
            parent_id=span.parent_id,
            kind=kind,
            name=name,
            detail=detail,
            start=round(span.start_time or 0.0, 4),
            duration=round(span.duration or 0.0, 4),
            status=status,
            meta=meta,
        )
        spans.append(node)
        by_id[node.id] = node

    for node in spans:
        if node.parent_id and node.parent_id in by_id:
            by_id[node.parent_id].children.append(node.id)

    def assign_depth(node: SpanNode, depth: int) -> None:
        node.depth = depth
        for child_id in node.children:
            assign_depth(by_id[child_id], depth + 1)

    for node in spans:
        if not node.parent_id or node.parent_id not in by_id:
            assign_depth(node, 0)

    return spans


def build_trace(
    interaction_log: Any,
    stats: Any,
    user_input: str,
    output: str,
    model: str,
    engine: str = "nemo",
    baseline_output: Optional[str] = None,
    baseline_duration: float = 0.0,
    colang_history: Optional[str] = None,
) -> Trace:
    rails = [_rail_from_activated(a) for a in (interaction_log.activated_rails or [])]
    spans = build_spans(interaction_log)

    blocked_rail = next((r for r in rails if r.status == "blocked"), None)
    blocked = blocked_rail is not None

    events: List[str] = []
    for event in (interaction_log.events or [])[:200]:
        if not isinstance(event, dict):
            continue
        etype = event.get("type") or event.get("event", {}).get("type", "")
        if etype in ("StartInputRail", "StartOutputRail") or (
            isinstance(etype, str) and etype.startswith(("Start", "Bot", "Utterance", "User"))
        ):
            events.append(etype)

    return Trace(
        engine=engine,
        model=model,
        user_input=user_input,
        output=output,
        blocked=blocked,
        blocked_by=blocked_rail.name if blocked_rail else "",
        block_reason=blocked_rail.reason if blocked_rail else "",
        total_duration=getattr(stats, "total_duration", 0.0) or 0.0,
        input_rails_duration=getattr(stats, "input_rails_duration", 0.0) or 0.0,
        output_rails_duration=getattr(stats, "output_rails_duration", 0.0) or 0.0,
        generation_duration=getattr(stats, "generation_rails_duration", 0.0) or 0.0,
        llm_calls_count=getattr(stats, "llm_calls_count", 0) or 0,
        total_tokens=getattr(stats, "llm_calls_total_tokens", 0) or 0,
        prompt_tokens=getattr(stats, "llm_calls_total_prompt_tokens", 0) or 0,
        completion_tokens=getattr(stats, "llm_calls_total_completion_tokens", 0) or 0,
        rails=rails,
        spans=spans,
        events=events,
        baseline_output=baseline_output,
        baseline_duration=baseline_duration,
    )
