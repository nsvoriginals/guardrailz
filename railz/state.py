from __future__ import annotations

from typing import List

import streamlit as st

from railz.catalog import DEFAULT_MODEL, STARTER_MESSAGES
from railz.engine import has_api_key
from railz.trace import Trace


def init_state() -> None:
    st.session_state.setdefault("messages", [dict(m) for m in STARTER_MESSAGES])
    st.session_state.setdefault("traces", [])
    st.session_state.setdefault("model", DEFAULT_MODEL)
    st.session_state.setdefault("rails_on", True)
    st.session_state.setdefault("force_mock", not has_api_key())
    st.session_state.setdefault("pending", None)
    st.session_state.setdefault("selected_trace_id", None)


def add_trace(trace: Trace) -> None:
    traces: List[Trace] = st.session_state.traces
    traces.insert(0, trace)
    del traces[12:]


def latest_trace() -> Trace | None:
    traces = st.session_state.traces
    return traces[0] if traces else None
