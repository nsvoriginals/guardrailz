import os

import streamlit as st

st.set_page_config(
    page_title="Noir — the data workspace",
    page_icon=":material/blur_on:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from theme import inject_theme

inject_theme()

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "assets", "logo-mark.svg")

st.logo(LOGO, icon_image=LOGO, size="medium")

pages = [
    st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/insights:"),
    st.Page("pages/settings.py", title="Settings", icon=":material/tune:"),
]

st.navigation(pages, position="top").run()
