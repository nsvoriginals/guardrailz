import streamlit as st

from theme import card_icon, footer, page_title

page_title("Settings", "tune")
st.caption("Manage your workspace, appearance and notifications.")

st.write("")
left, right = st.columns([1.25, 1], gap="large")

with left:
    with st.container(border=True, key="card-workspace"):
        st.markdown(card_icon("apartment"), unsafe_allow_html=True)
        st.markdown('<p class="card-title">Workspace</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-text">Identity used across deploys, docs and embeds.</p>',
                    unsafe_allow_html=True)
        st.write("")
        st.text_input("Display name", value="Noir Labs")
        st.text_input("Slug", value="noir-labs", help="Used in your Noir URLs.")
        st.toggle("Public directory listing", value=False)

    with st.container(border=True, key="card-appearance"):
        st.markdown(card_icon("palette"), unsafe_allow_html=True)
        st.markdown('<p class="card-title">Appearance</p>', unsafe_allow_html=True)
        st.write("")
        st.radio("Density", ["Comfortable", "Compact"], horizontal=True)
        st.select_slider("Corner radius", options=[6, 10, 14, 18, 22], value=14)
        st.color_picker("Accent color", value="#7C5CFF")

with right:
    with st.container(border=True, key="card-notify"):
        st.markdown(card_icon("notifications"), unsafe_allow_html=True)
        st.markdown('<p class="card-title">Notifications</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-text">Choose what lands in your inbox.</p>',
                    unsafe_allow_html=True)
        st.write("")
        st.checkbox("Deploy succeeded", value=True)
        st.checkbox("Deploy failed", value=True)
        st.checkbox("Weekly digest", value=False)
        st.checkbox("Product updates", value=False)

    with st.container(border=True, key="danger"):
        st.markdown(card_icon("warning"), unsafe_allow_html=True)
        st.markdown('<p class="card-title">Danger zone</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-text">Deleting the workspace removes all data permanently. '
                    'This action cannot be undone.</p>', unsafe_allow_html=True)
        st.write("")
        if st.button("Delete workspace", icon=":material/delete_forever:", use_container_width=True):
            st.error("Disabled in the demo.")

st.write("")
s1, s2, _ = st.columns([1, 1, 3])
with s1:
    if st.button("Save changes", type="primary", icon=":material/check:", use_container_width=True):
        st.toast("Workspace settings saved.")
with s2:
    if st.button("Reset", icon=":material/restart_alt:", use_container_width=True):
        st.toast("Reverted to last saved state.")

footer()
