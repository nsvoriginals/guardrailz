import numpy as np
import pandas as pd
import streamlit as st

from theme import footer, icon, page_title, section_head

page_title("Dashboard", "insights")
st.caption("Live view of workspace activity over the last 30 days.")

st.write("")
f1, f2, f3, _ = st.columns([1.2, 1.5, 1.1, 2.6], vertical_alignment="bottom")
with f1:
    st.selectbox("Range", ["Last 7 days", "Last 30 days", "Last 90 days"], index=1)
with f2:
    st.radio("Surface", ["All", "Web", "Mobile", "API"], horizontal=True)
with f3:
    st.write("")
    if st.button("Refresh", icon=":material/refresh:", use_container_width=True):
        st.toast("Metrics refreshed just now.")

st.write("")

k1, k2, k3, k4 = st.columns(4, gap="small")
k1.metric("Requests", "1.42M", "+6.1%", icon=":material/bolt:")
k2.metric("Error rate", "0.03%", "-0.01%", icon=":material/bug_report:")
k3.metric("Avg. cost", "$0.0021", "-3%", icon=":material/payments:")
k4.metric("P95 latency", "112 ms", "-24 ms", icon=":material/speed:")

rng = np.random.default_rng(7)
series = pd.DataFrame(
    np.cumsum(rng.standard_normal((120, 3)) * 4, axis=0),
    columns=["web", "mobile", "api"],
)

tab_traffic, tab_regions, tab_events = st.tabs(
    [":material/show_chart:  Traffic", ":material/public:  Regions", ":material/table_view:  Events"]
)

with tab_traffic:
    with st.container(border=True, key="chart-traffic"):
        st.markdown(
            f'<p class="card-title">{icon("show_chart", "1.2rem")}Requests by surface</p>'
            f'<p class="card-text">Cumulative requests, sampled every 15 minutes.</p>',
            unsafe_allow_html=True,
        )
        st.line_chart(series, height=300, color=["#7C5CFF", "#4FD1C5", "#FF5C7C"])

    c1, c2 = st.columns([1.4, 1], gap="medium")
    with c1:
        with st.container(border=True, key="chart-mix"):
            st.markdown(f'<p class="card-title">{icon("bar_chart", "1.2rem")}Traffic mix</p>',
                        unsafe_allow_html=True)
            mix = pd.DataFrame(
                {"surface": ["Web", "Mobile", "API", "Edge"], "requests": [482, 366, 298, 154]}
            )
            st.bar_chart(mix, x="surface", y="requests", color="#7C5CFF", height=260)
    with c2:
        with st.container(border=True, key="chart-health"):
            st.markdown(f'<p class="card-title">{icon("monitor_heart", "1.2rem")}Health</p>',
                        unsafe_allow_html=True)
            st.progress(0.97, text="Availability 97%")
            st.progress(0.82, text="Cache hit rate 82%")
            st.progress(0.64, text="Queue depth 64%")

with tab_regions:
    regions = pd.DataFrame(
        {
            "region": ["iad1", "fra1", "sin1", "cdg1", "sfo1"],
            "latency": [42, 61, 88, 74, 51],
            "share": [38, 24, 17, 12, 9],
        }
    )
    with st.container(border=True, key="chart-regions"):
        st.markdown(
            f'<p class="card-title">{icon("public", "1.2rem")}Regional latency</p>'
            f'<p class="card-text">P95 latency in milliseconds across the edge network.</p>',
            unsafe_allow_html=True,
        )
        st.bar_chart(regions, x="region", y="latency", color="#4FD1C5", height=300)

with tab_events:
    with st.container(border=True, key="chart-events"):
        st.markdown(
            f'<p class="card-title">{icon("table_view", "1.2rem")}Recent events</p>'
            f'<p class="card-text">Streaming from the last hour across all regions.</p>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            pd.DataFrame(
                {
                    "id": [f"evt_{i:04d}" for i in range(8)],
                    "type": ["deploy", "query", "auth", "deploy", "error", "query", "cache", "deploy"],
                    "region": ["iad1", "fra1", "sin1", "iad1", "fra1", "iad1", "cdg1", "sin1"],
                    "ms": [42, 118, 9, 51, 3, 87, 12, 96],
                }
            ),
            width="stretch",
            hide_index=True,
            height=320,
        )

footer()
