import os

import streamlit as st

st.set_page_config(
    page_title="Railz — NeMo Guardrails studio",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from railz.state import init_state
from theme import inject_theme

inject_theme()
init_state()

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "assets", "logo-mark.svg")

st.logo(LOGO, icon_image=LOGO, size="medium")

pages = [
    st.Page("views/chat.py", title="Chat", icon=":material/forum:", default=True),
    st.Page("views/traces.py", title="Traces", icon=":material/account_tree:"),
    st.Page("views/rails.py", title="Rails", icon=":material/policy:"),
    st.Page("views/settings.py", title="Settings", icon=":material/tune:"),
]

st.navigation(pages, position="top").run()
