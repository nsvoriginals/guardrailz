import streamlit as st

from railz import viz
from railz.catalog import MODELS, PRESET_PROMPTS, block_message_for, model_by_id
from railz.runtime import engine_badge, run_turn
from railz.state import add_trace, init_state
from theme import footer, page_title

init_state()
viz.inject_styles()

head_l, head_r = st.columns([2.1, 1.4], vertical_alignment="center")
with head_l:
    page_title("Guardrail Studio", "shield")
    mode, mode_label = engine_badge(st.session_state.force_mock)
    badge_cls = "passed" if mode == "live" else "info"
    st.markdown(f'<span class="rz-pill {badge_cls}"><span class="rz-pdot"></span>{mode_label}</span>',
                unsafe_allow_html=True)
with head_r:
    c1, c2 = st.columns([1.3, 1], vertical_alignment="center")
    with c1:
        st.selectbox(
            "Model",
            options=[m["id"] for m in MODELS],
            format_func=lambda mid: model_by_id(mid)["label"],
            key="model",
            label_visibility="collapsed",
        )
    with c2:
        st.toggle("Rails", key="rails_on", help="Turn the guardrails on or off for this session.")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Clear chat", icon=":material/restart_alt:", use_container_width=True):
            st.session_state.messages = st.session_state.messages[:1]
            st.session_state.traces = []
            st.rerun()
    with b2:
        if st.button("Open traces", icon=":material/account_tree:", use_container_width=True):
            st.switch_page("views/traces.py")

st.markdown('<div class="sh-eyebrow" style="margin:.4rem 0 .5rem">Scenarios</div>', unsafe_allow_html=True)
pcols = st.columns(len(PRESET_PROMPTS))
for col, preset in zip(pcols, PRESET_PROMPTS):
    with col:
        if st.button(preset["label"], key=f"preset_{preset['id']}", use_container_width=True):
            st.session_state.pending = preset["prompt"]
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=":material/person:" if message["role"] == "user" else ":material/shield:"):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about Aperture…")
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/shield:"):
        with st.spinner("Running guardrails…"):
            trace = run_turn(
                st.session_state.messages,
                model=st.session_state.model,
                rails_on=st.session_state.rails_on,
                force_mock=st.session_state.force_mock,
            )
        add_trace(trace)

        if trace.error:
            st.error(f"Engine error: {trace.error}")
        content = trace.output
        if trace.blocked:
            content = f"**Blocked by the `{trace.blocked_by}` rail.** {block_message_for(trace.blocked_by)}"
        if not content:
            content = "_No response generated._"
        st.markdown(content)

        st.markdown(viz.status_pill(trace), unsafe_allow_html=True)
        st.markdown(viz.pipeline_html(trace), unsafe_allow_html=True)
        if trace.blocked:
            st.markdown(viz.blocked_card_html(trace), unsafe_allow_html=True)
        st.markdown(viz.metrics_html(trace), unsafe_allow_html=True)
        if st.button("Inspect full trace", icon=":material/account_tree:", key=f"insp_{trace.id}"):
            st.session_state.selected_trace_id = trace.id
            st.switch_page("views/traces.py")

    st.session_state.messages.append({"role": "assistant", "content": content})

footer()
