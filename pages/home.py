import streamlit as st

from theme import card_icon, footer, hero, icon, section_head

with st.container(border=True, key="hero"):
    hero(
        eyebrow_text="Now in private beta",
        title="The data workspace<br>for serious teams.",
        subtitle="Ship internal tools, dashboards and automations in hours — not weeks. "
                 "Built on a typed runtime, native state and zero-config deploys.",
    )

    b1, b2, b3, _ = st.columns([1.25, 1.15, 1.15, 2.2], vertical_alignment="center")
    with b1:
        if st.button("Start building", type="primary", icon=":material/rocket_launch:",
                     use_container_width=True):
            st.switch_page("pages/dashboard.py")
    with b2:
        if st.button("Book a demo", icon=":material/videocam:", use_container_width=True):
            st.toast("A demo link is on the way.")
    with b3:
        if st.button("Star on GitHub", icon=":material/star:", use_container_width=True):
            st.toast("Thanks for the star!")

    st.markdown(
        '<div class="hero-meta">'
        f'<span>{icon("bolt", "1.05rem")} Deploy in 40 seconds</span>'
        f'<span>{icon("verified_user", "1.05rem")} SOC 2 Type II</span>'
        f'<span>{icon("payments", "1.05rem")} No credit card required</span>'
        f'<span>{icon("public", "1.05rem")} 6 global regions</span>'
        '</div>',
        unsafe_allow_html=True,
    )

section_head(
    "Everything you need to ship",
    "One workspace for data, product and infrastructure teams — with the primitives you already trust.",
    eyebrow_text="Platform",
)

features = [
    ("bolt", "Instant deploys",
     "Push to main. We build, sign and roll out in under 40 seconds — with instant rollback on every release."),
    ("shield_lock", "Typed runtime",
     "Catch schema drift and bad migrations before they reach production. Types are enforced end to end."),
    ("insights", "Live telemetry",
     "Trace every query and render. Diagnose slow pages in a single, unified view of your stack."),
]
cols = st.columns(3, gap="medium")
for i, (col, (ic, title, body)) in enumerate(zip(cols, features)):
    with col:
        with st.container(border=True, key=f"card{i}"):
            st.markdown(card_icon(ic), unsafe_allow_html=True)
            st.markdown(f'<p class="card-title">{title}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="card-text">{body}</p>', unsafe_allow_html=True)

section_head(
    "Built for the whole loop",
    "Model it, query it, ship it. Noir gives every team the same source of truth.",
    eyebrow_text="Workflow",
)

left, right = st.columns([1.05, 1], gap="large")
with left:
    with st.container(border=True, key="steps"):
        st.markdown(card_icon("route"), unsafe_allow_html=True)
        st.markdown('<p class="card-title">From idea to production</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-text">A single pipeline that stays fast as your team grows.</p>',
                    unsafe_allow_html=True)
        st.write("")
        st.code(
            "noir deploy --prod\n"
            "  ✓ type-check    18ms\n"
            "  ✓ migrations     2/2\n"
            "  ✓ edge bundle   142kb\n"
            "  → live in 38.4s",
            language="bash",
        )
with right:
    steps = [
        ("add_circle", "Connect", "Point Noir at your data — Postgres, BigQuery, S3 or the API."),
        ("stacks", "Model", "Define entities once. Types, migrations and docs stay in sync."),
        ("rocket_launch", "Ship", "Promote to edge with a keystroke. Rollback is instant."),
    ]
    for ic, title, body in steps:
        with st.container(border=True, key=f"step-{title.lower()}"):
            st.markdown(
                f'<p class="card-title">{icon(ic, "1.25rem")}{title}</p>'
                f'<p class="card-text">{body}</p>',
                unsafe_allow_html=True,
            )

section_head(
    "The numbers speak first",
    "Real traffic from workspaces already running on Noir.",
    eyebrow_text="Scale",
)

m1, m2, m3, m4 = st.columns(4, gap="small")
m1.metric("Active users", "48,231", "+8.4%", icon=":material/group:")
m2.metric("P95 latency", "112 ms", "-24 ms", icon=":material/speed:")
m3.metric("Deploys / day", "1,204", "+12%", icon=":material/rocket_launch:")
m4.metric("Uptime", "99.99%", "30d", icon=":material/health_and_safety:")

st.write("")
with st.container(border=True, key="logos"):
    st.markdown(
        '<p class="card-tag">Trusted by teams at</p>',
        unsafe_allow_html=True,
    )
    lg = st.columns(5, gap="medium")
    for col, name in zip(lg, ["Northwind", "Sable", "Aperture", "Lumen", "Vanta"]):
        with col:
            st.markdown(
                f'<div style="font-family:var(--font-display);font-size:1.18rem;font-weight:600;'
                f'letter-spacing:-0.02em;opacity:.55;transition:opacity .3s ease">{name}</div>',
                unsafe_allow_html=True,
            )

footer()
