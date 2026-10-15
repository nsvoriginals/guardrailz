from pathlib import Path

import streamlit as st

from railz import viz
from railz.catalog import RAIL_CATALOG
from railz.state import init_state
from theme import footer, page_title

init_state()
viz.inject_styles()

CONFIG_DIR = Path(__file__).resolve().parent.parent / "railz" / "config"

page_title("Rails", "policy")

for rail in RAIL_CATALOG:
    color = "#7FE3D6" if rail["stage"] == "input" else "#5CA8FF"
    st.markdown(
        '<div class="rz-panel">'
        '<div class="rz-head">'
        f'<div class="rz-title" style="display:flex;align-items:center;gap:.55rem">'
        f'<span class="msym" style="font-size:1.1rem;color:{color}">{rail["icon"]}</span>{rail["name"]}</div>'
        f'<span class="rz-pill info"><span class="rz-pdot"></span>{rail["stage"]} rail</span>'
        '</div>'
        f'<div class="rz-cbody">{rail["job"]}</div>'
        f'<div class="rz-sub" style="margin-top:.55rem">action {rail["action"]} · flow {rail["flow"]}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.write("")
tabs = st.tabs(["config.yml", "rails.co", "prompts.yml", "actions.py"])
files = ["config.yml", "rails.co", "prompts.yml", "actions.py"]
for tab, name in zip(tabs, files):
    with tab:
        path = CONFIG_DIR / name
        lang = "python" if name.endswith(".py") else ("yaml" if name.endswith(".yml") else "text")
        st.code(path.read_text(), language=lang)

footer()
