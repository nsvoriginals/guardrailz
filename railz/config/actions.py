from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

from pydantic import BaseModel, Field

from nemoguardrails.actions import action
from nemoguardrails.context import llm_call_info_var
from nemoguardrails.llm.call import llm_call
from nemoguardrails.logging.explain import LLMCallInfo


class RailzVerdict(BaseModel):
    blocked: bool = False
    allowed: bool = True
    reason: str = ""
    label: str = ""
    score: float = 0.0
    matches: List[Dict[str, Any]] = Field(default_factory=list)
    detail: Dict[str, Any] = Field(default_factory=dict)


RAIL_SETTINGS: Dict[str, Any] = {
    "jailbreak": {
        "use_llm_judge": True,
        "block_threshold": 0.5,
        "label": "Jailbreak / prompt injection",
    },
    "sensitive_data": {
        "block_on": True,
        "entities": ["EMAIL", "PHONE", "SSN", "CREDIT_CARD", "API_KEY", "PRIVATE_KEY", "IPV4"],
        "label": "Sensitive data / PII",
    },
    "topic": {
        "allowed": [
            "aperture",
            "dashboard",
            "metric",
            "alert",
            "report",
            "integration",
            "billing",
            "account",
            "api",
            "export",
            "chart",
            "workspace",
            "user",
            "team",
            "query",
            "data",
        ],
        "min_off_topic_length": 4,
        "label": "Topical guardrail",
    },
    "toxicity": {
        "use_llm_judge": True,
        "threshold": 0.6,
        "label": "Moderation / toxicity",
    },
}


JAILBREAK_PATTERNS: List[Tuple[str, str, float]] = [
    (r"ignore\s+(all\s+)?(the\s+)?(previous|prior|above)\s+instructions", "ignore-instructions", 0.9),
    (r"disregard\s+(all\s+)?(the\s+)?(previous|prior|system)\s+(instructions|prompt|rules)", "disregard-rules", 0.9),
    (r"(reveal|show|print|repeat|expose)\s+(me\s+)?(your\s+)?(system\s+)?(prompt|instructions|rules)", "prompt-leak", 0.85),
    (r"you\s+are\s+now\s+(dan|do\s+anything\s+now)", "dan-mode", 0.95),
    (r"do\s+anything\s+now", "dan-mode", 0.95),
    (r"(enable|activate|enter)\s+(developer|debug|god|unrestricted)\s+mode", "dev-mode", 0.9),
    (r"pretend\s+(you\s+are|to\s+be)", "pretend", 0.6),
    (r"(act|behave)\s+as\s+(if\s+you\s+(are|were)|an?\s+)", "roleplay", 0.45),
    (r"roleplay\s+as", "roleplay", 0.5),
    (r"(bypass|disable|turn\s+off|ignore)\s+(your\s+)?(safety|guardrails|filters|guidelines|restrictions|rules)", "bypass-safety", 0.9),
    (r"without\s+any\s+(rules|restrictions|filters|limitations)", "no-rules", 0.7),
    (r"jailbreak", "jailbreak-keyword", 0.8),
    (r"no\s+longer\s+bound\s+by", "no-bounds", 0.8),
    (r"\]\s*\]\s*\}\s*\}|<\|[a-z_]+\|>", "token-injection", 0.7),
]

BASE64_BLOB = re.compile(r"[A-Za-z0-9+/]{60,}={0,2}")


PII_PATTERNS: Dict[str, re.Pattern[str]] = {
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"),
    "PHONE": re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s.\-]?)?(?:\(?\d{3}\)?[\s.\-]?)\d{3}[\s.\-]?\d{4}(?!\d)"),
    "SSN": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    "CREDIT_CARD": re.compile(r"(?<!\d)(?:\d[ \-]?){13,16}(?!\d)"),
    "API_KEY": re.compile(r"(?:sk|pk|gsk|rk|api|token)[-_][A-Za-z0-9_\-]{16,}"),
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "IPV4": re.compile(r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)"),
}

SECRET_HINTS = re.compile(r"(password|passwd|secret|api[_\s]?key|token|credential)s?\b", re.IGNORECASE)


TOXIC_TERMS: List[Tuple[str, float]] = [
    (r"\b(idiot|moron|stupid|dumbass|imbecile)\b", 0.6),
    (r"\b(shut\s+up|screw\s+you|fuck\s+you|go\s+to\s+hell)\b", 0.9),
    (r"\b(hate|despise)\s+(you|them|those|these)\b", 0.7),
    (r"\b(kill|murder|hurt|attack)\s+(you|him|her|them|people)\b", 0.95),
    (r"\b(slur|retard|faggot|nigg)\w*", 0.98),
    (r"\b(worthless|pathetic|useless)\b", 0.5),
]


def _luhn(number: str) -> bool:
    digits = [int(d) for d in re.sub(r"\D", "", number)]
    if len(digits) < 13:
        return False
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _snippet(text: str, start: int, end: int, pad: int = 24) -> str:
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    prefix = "…" if lo > 0 else ""
    suffix = "…" if hi < len(text) else ""
    return f"{prefix}{text[lo:hi]}{suffix}"


def _scan_pii(text: str, entities: Sequence[str]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for entity in entities:
        pattern = PII_PATTERNS.get(entity)
        if pattern is None:
            continue
        for match in pattern.finditer(text):
            value = match.group(0)
            if entity == "CREDIT_CARD" and not _luhn(value):
                continue
            if entity == "IPV4" and value.startswith(("0.", "127.", "255.")):
                continue
            found.append(
                {
                    "entity": entity,
                    "value": value,
                    "start": match.start(),
                    "end": match.end(),
                    "context": _snippet(text, match.start(), match.end()),
                }
            )
    return found


async def _llm_judge(task: str, context: Dict[str, Any], llm: Any, llm_task_manager: Any) -> Optional[bool]:
    if llm is None or llm_task_manager is None:
        return None
    try:
        prompt = llm_task_manager.render_task_prompt(task=task, context=context)
        stop = llm_task_manager.get_stop_tokens(task=task)
        llm_call_info_var.set(LLMCallInfo(task=task))
        response = await llm_call(
            llm,
            prompt,
            stop=stop,
            llm_params={"temperature": 0.0, "max_tokens": 8},
        )
        parsed: Sequence[Any] = llm_task_manager.parse_task_output(task=task, output=response.content)
        return bool(parsed[0]) if parsed else None
    except Exception:
        return None


@action(is_system_action=True)
async def railz_check_jailbreak(
    text: str,
    llm: Any = None,
    llm_task_manager: Any = None,
    config: Any = None,
    **kwargs: Any,
) -> RailzVerdict:
    """Heuristic + LLM-judge jailbreak / prompt-injection detection."""
    settings = RAIL_SETTINGS["jailbreak"]
    lowered = text or ""
    matches: List[Dict[str, Any]] = []
    score = 0.0

    for pattern, label, weight in JAILBREAK_PATTERNS:
        if re.search(pattern, lowered, re.IGNORECASE):
            matches.append({"pattern": label, "weight": weight})
            score = max(score, weight)

    if BASE64_BLOB.search(lowered):
        matches.append({"pattern": "base64-blob", "weight": 0.6})
        score = max(score, 0.6)

    judge_safe: Optional[bool] = None
    if settings["use_llm_judge"]:
        judge_safe = await _llm_judge(
            "railz_jailbreak_judge",
            {"user_input": lowered},
            llm,
            llm_task_manager,
        )

    judge_blocked = judge_safe is False
    heuristic_blocked = score >= settings["block_threshold"]
    blocked = judge_blocked or heuristic_blocked

    reason = ""
    if judge_blocked:
        reason = "The LLM judge classified this message as a jailbreak attempt."
    elif heuristic_blocked:
        reason = "Matched known jailbreak / prompt-injection patterns."

    label = matches[0]["pattern"] if matches else ("llm-judge" if judge_blocked else "")

    return RailzVerdict(
        blocked=blocked,
        allowed=not blocked,
        reason=reason,
        label=label,
        score=round(max(score, 1.0 if judge_blocked else 0.0), 2),
        matches=matches,
        detail={
            "heuristic_score": round(score, 2),
            "judge": "unsafe" if judge_safe is False else ("safe" if judge_safe is True else "skipped"),
            "threshold": settings["block_threshold"],
        },
    )


@action(is_system_action=True)
async def railz_check_sensitive_data(
    text: str,
    config: Any = None,
    **kwargs: Any,
) -> RailzVerdict:
    """Regex-based PII / secret detection (no Presidio required)."""
    settings = RAIL_SETTINGS["sensitive_data"]
    found = _scan_pii(text or "", settings["entities"])

    secret_hint = bool(SECRET_HINTS.search(text or ""))
    blocked = settings["block_on"] and len(found) > 0

    entities = sorted({m["entity"] for m in found})
    if blocked:
        reason = f"Found {len(found)} sensitive item(s): {', '.join(entities)}."
    else:
        reason = ""

    return RailzVerdict(
        blocked=blocked,
        allowed=not blocked,
        reason=reason,
        label=", ".join(entities),
        score=1.0 if blocked else 0.0,
        matches=found,
        detail={
            "entities_detected": entities,
            "secret_keyword_present": secret_hint,
            "entity_count": len(found),
        },
    )


@action(is_system_action=True)
async def railz_check_topic(
    text: str,
    llm: Any = None,
    llm_task_manager: Any = None,
    config: Any = None,
    **kwargs: Any,
) -> RailzVerdict:
    """Keyword grounding plus an optional LLM topical judge."""
    settings = RAIL_SETTINGS["topic"]
    lowered = (text or "").lower()

    hits = [topic for topic in settings["allowed"] if topic in lowered]
    keyword_on_topic = len(hits) > 0

    judge_safe: Optional[bool] = None
    if not keyword_on_topic and len(lowered.strip()) >= settings["min_off_topic_length"]:
        judge_safe = await _llm_judge(
            "railz_topic_judge",
            {"user_input": text},
            llm,
            llm_task_manager,
        )

    if keyword_on_topic:
        allowed = True
    elif judge_safe is not None:
        allowed = judge_safe
    else:
        allowed = False

    reason = "" if allowed else "The message is not about the Aperture platform."
    return RailzVerdict(
        blocked=not allowed,
        allowed=allowed,
        reason=reason,
        label="on-topic" if allowed else "off-topic",
        score=0.0 if allowed else 1.0,
        matches=[{"topic": h} for h in hits],
        detail={
            "keyword_hits": hits,
            "judge": "safe" if judge_safe is True else ("unsafe" if judge_safe is False else "skipped"),
        },
    )


@action(is_system_action=True)
async def railz_self_check_output(
    bot_message: str,
    llm: Any = None,
    llm_task_manager: Any = None,
    config: Any = None,
    **kwargs: Any,
) -> RailzVerdict:
    """LLM self-check of the generated answer (NeMo self_check_output prompt task)."""
    if llm is None or llm_task_manager is None:
        return RailzVerdict(
            blocked=False,
            allowed=True,
            reason="",
            label="skipped",
            detail={"judge": "skipped (no LLM)"},
        )

    judge_safe = await _llm_judge(
        "self_check_output",
        {"bot_response": bot_message},
        llm,
        llm_task_manager,
    )

    blocked = judge_safe is False
    return RailzVerdict(
        blocked=blocked,
        allowed=not blocked,
        reason="The answer failed the output self-check." if blocked else "",
        label="unsafe" if blocked else "safe",
        score=1.0 if blocked else 0.0,
        detail={"judge": "unsafe" if blocked else "safe"},
    )


@action(is_system_action=True)
async def railz_check_toxicity(
    text: str,
    llm: Any = None,
    llm_task_manager: Any = None,
    config: Any = None,
    **kwargs: Any,
) -> RailzVerdict:
    """Lexicon-based toxicity scoring plus an optional LLM judge."""
    settings = RAIL_SETTINGS["toxicity"]
    lowered = text or ""
    matches: List[Dict[str, Any]] = []
    score = 0.0

    for pattern, weight in TOXIC_TERMS:
        if re.search(pattern, lowered, re.IGNORECASE):
            matches.append({"pattern": pattern, "weight": weight})
            score = max(score, weight)

    judge_safe: Optional[bool] = None
    if settings["use_llm_judge"]:
        judge_safe = await _llm_judge(
            "railz_toxicity_judge",
            {"bot_response": lowered},
            llm,
            llm_task_manager,
        )

    judge_blocked = judge_safe is False
    lexicon_blocked = score >= settings["threshold"]
    blocked = judge_blocked or lexicon_blocked

    reason = ""
    if judge_blocked:
        reason = "The LLM judge flagged this content as toxic."
    elif lexicon_blocked:
        reason = "Matched known toxic terms."

    return RailzVerdict(
        blocked=blocked,
        allowed=not blocked,
        reason=reason,
        label="toxic" if blocked else "clean",
        score=round(max(score, 1.0 if judge_blocked else 0.0), 2),
        matches=matches,
        detail={
            "lexicon_score": round(score, 2),
            "judge": "unsafe" if judge_safe is False else ("safe" if judge_safe is True else "skipped"),
            "threshold": settings["threshold"],
        },
    )
