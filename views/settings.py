import streamlit as st

from railz import viz
from railz.catalog import MODELS, RAIL_CATALOG, model_by_id
from railz.engine import has_api_key
from railz.state import init_state
from theme import footer, page_title

init_state()
viz.inject_styles()

page_title("Settings", "tune")

c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    info = model_by_id(st.session_state.model)
    st.markdown(
        '<div class="rz-panel"><div class="rz-head"><div class="rz-title">Engine</div></div>'
        f'<div class="rz-cbody">{info["label"]} · {info["note"]}</div></div>',
        unsafe_allow_html=True,
    )
    st.selectbox(
        "Model",
        options=[m["id"] for m in MODELS],
        format_func=lambda mid: f"{model_by_id(mid)['label']}  ·  {mid}",
        key="model",
    )
    st.toggle("Guardrails on", key="rails_on")
    st.toggle("Demo mode (scripted traces)", key="force_mock",
              help="Forces canned traces. Auto-enabled when GROQ_API_KEY is missing.")

    st.write("")
    st.markdown(
        '<div class="rz-panel"><div class="rz-head"><div class="rz-title">Credentials</div></div>'
        f'<div class="rz-cbody">GROQ_API_KEY: '
        f'{"set" if has_api_key() else "missing — add it to .env"}</div></div>',
        unsafe_allow_html=True,
    )

with c2:
    for rail in RAIL_CATALOG:
        color = "#7FE3D6" if rail["stage"] == "input" else "#5CA8FF"
        st.markdown(
            '<div class="rz-panel" style="margin:.3rem 0;padding:.7rem .9rem">'
            f'<div class="rz-title" style="display:flex;align-items:center;gap:.5rem">'
            f'<span class="msym" style="font-size:.95rem;color:{color}">{rail["icon"]}</span>{rail["name"]}'
            f'<span class="rz-sub" style="margin-left:auto">{rail["stage"]}</span></div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.caption("Config lives in `railz/config/` — edit `rails.co`, `prompts.yml` and `actions.py` there.")

footer()
