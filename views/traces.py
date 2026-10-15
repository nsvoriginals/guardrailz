import streamlit as st

from railz import viz
from railz.catalog import PRESET_PROMPTS
from railz.runtime import run_preset
from railz.state import add_trace, init_state
from theme import footer, page_title

init_state()
viz.inject_styles()


def _summ(trace):
    status = "blocked" if trace.blocked else "passed"
    text = trace.user_input[:54] + ("…" if len(trace.user_input) > 54 else "")
    return f"{status.upper()} · {trace.created_at} · {text}"


page_title("Trace Explorer", "account_tree")

traces = st.session_state.traces

top_l, top_r = st.columns([2.2, 1.6], vertical_alignment="bottom")
with top_l:
    if traces:
        options = [t.id for t in traces]
        default_id = st.session_state.selected_trace_id if st.session_state.selected_trace_id in options else options[0]
        selected = st.selectbox(
            "Conversation turns",
            options=options,
            index=options.index(default_id),
            format_func=lambda tid: _summ(next(t for t in traces if t.id == tid)),
        )
    else:
        selected = None
with top_r:
    st.markdown('<div class="sh-eyebrow" style="margin-bottom:.4rem">Demo traces</div>', unsafe_allow_html=True)
    pcols = st.columns(3)
    for i, preset in enumerate(PRESET_PROMPTS):
        with pcols[i % 3]:
            if st.button(preset["label"], key=f"load_{preset['id']}", use_container_width=True):
                trace = run_preset(preset["id"], model=st.session_state.model)
                add_trace(trace)
                st.session_state.selected_trace_id = trace.id
                st.rerun()

if not traces:
    st.markdown(
        '<div class="rz-panel"><div class="rz-empty">No traces yet. Send a message in Chat, '
        'or load a demo trace above.</div></div>',
        unsafe_allow_html=True,
    )
    footer()
    st.stop()

trace = next(t for t in traces if t.id == selected)
st.session_state.selected_trace_id = trace.id

c1, c2 = st.columns([3, 1], vertical_alignment="center")
with c1:
    st.markdown(
        f'<div style="font-family:var(--font-mono,monospace);font-size:.8rem;color:rgba(242,242,247,.8)">'
        f'“{trace.user_input}”</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(viz.status_pill(trace), unsafe_allow_html=True)

st.markdown(viz.metrics_html(trace), unsafe_allow_html=True)

if trace.error:
    st.error(f"Engine error: {trace.error}")

if trace.blocked:
    st.markdown(viz.blocked_card_html(trace), unsafe_allow_html=True)

tab_overview, tab_waterfall, tab_tree, tab_rails = st.tabs(["Pipeline", "Waterfall", "Span tree", "Rails"])

with tab_overview:
    st.markdown(viz.pipeline_html(trace), unsafe_allow_html=True)
    if trace.output:
        st.markdown(
            '<div class="rz-panel"><div class="rz-head"><div class="rz-title">Model answer</div></div>'
            f'<div class="rz-cbody" style="font-size:.9rem;line-height:1.6;color:rgba(242,242,247,.9)">{trace.output}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    elif trace.blocked:
        st.markdown(
            '<div class="rz-panel"><div class="rz-head"><div class="rz-title">Model answer</div></div>'
            '<div class="rz-empty">No model call — the request was stopped by an input rail.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

with tab_waterfall:
    st.markdown(viz.waterfall_html(trace), unsafe_allow_html=True)

with tab_tree:
    st.markdown(viz.span_tree_html(trace), unsafe_allow_html=True)

with tab_rails:
    st.markdown(viz.rail_cards_html(trace), unsafe_allow_html=True)

footer()
