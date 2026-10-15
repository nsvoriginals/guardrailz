import streamlit as st

FONTS = """
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700,900&f[]=clash-display@400,500,600,700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0">
<style>
@font-face {
    font-family: 'Nothing Font';
    src: url('app/static/nothing-font.otf') format('opentype');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}
</style>
"""

CSS = """
<style>
/* =========================================================
   NOIR — design system
   display: Nothing Font · body: Satoshi · mono: JetBrains Mono
   ========================================================= */

:root {
    --bg: #050507;
    --bg-soft: #0A0A11;
    --surface: rgba(255,255,255,0.028);
    --surface-2: rgba(255,255,255,0.055);
    --surface-solid: #0F0F16;
    --line: rgba(255,255,255,0.075);
    --line-strong: rgba(255,255,255,0.15);

    --text: #F2F2F7;
    --text-dim: #9C9CB4;
    --text-mute: #6A6A84;

    --violet: #7C5CFF;
    --indigo: #5B8CFF;
    --mint: #4FD1C5;
    --rose: #FF5C7C;
    --amber: #FFB86B;
    --green: #5BE49B;

    --brand: linear-gradient(120deg, #8B6DFF 0%, #6B5CFF 45%, #4FD1C5 120%);

    --font-display: 'Nothing Font', 'Clash Display', 'Satoshi', 'Inter', ui-sans-serif, system-ui, sans-serif;
    --font-label: 'Nothing Font', 'JetBrains Mono', ui-monospace, monospace;
    --font-body: 'Satoshi', 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;

    --ease: cubic-bezier(.22, 1, .36, 1);
    --ease-io: cubic-bezier(.65, 0, .35, 1);

    --r-xs: 9px;
    --r-sm: 13px;
    --r: 18px;
    --r-lg: 26px;
    --r-xl: 34px;

    --header-h: 76px;
}

/* ---------- base ---------- */
html, body, [data-testid="stApp"] {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    font-weight: 400;
    font-synthesis: none;
    font-synthesis-weight: none;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* single-weight display font (Nothing Font) — never faux-bold it */
[class*="rz-"], .hero-title, .eyebrow, .chip, .page-title,
.section-head, .sh-title, .sh-eyebrow, .card-title, .card-tag, .hero-meta span {
    font-synthesis-weight: none;
}

[data-testid="stApp"] {
    min-height: 100vh;
    isolation: isolate;
}

#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

/* aurora — slow drifting light */
[data-testid="stApp"]::before {
    content: "";
    position: fixed;
    inset: -20vh -10vw auto -10vw;
    height: 130vh;
    z-index: -2;
    pointer-events: none;
    background:
        radial-gradient(46vw 40vh at 12% 8%,  rgba(124,92,255,.30),  transparent 62%),
        radial-gradient(40vw 34vh at 84% 4%,  rgba(79,209,197,.20),  transparent 60%),
        radial-gradient(52vw 44vh at 68% 78%, rgba(91,140,255,.16),  transparent 65%),
        radial-gradient(34vw 30vh at 24% 62%, rgba(255,92,124,.10),  transparent 62%);
    filter: blur(14px) saturate(135%);
    animation: auroraDrift 26s ease-in-out infinite alternate;
    opacity: .85;
}

/* fine engineering grid + vignette */
[data-testid="stApp"]::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-image:
        linear-gradient(to right, rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,.035) 1px, transparent 1px),
        radial-gradient(ellipse at 50% 0%, transparent 45%, rgba(5,5,7,.72) 100%);
    background-size: 78px 78px, 78px 78px, 100% 100%;
    mask-image: radial-gradient(ellipse 110% 80% at 50% 0%, #000 25%, transparent 78%);
    -webkit-mask-image: radial-gradient(ellipse 110% 80% at 50% 0%, #000 25%, transparent 78%);
    opacity: .5;
}

@keyframes auroraDrift {
    0%   { transform: translate3d(0,0,0)      scale(1);    }
    50%  { transform: translate3d(-2.5%, 2%,0) scale(1.06);}
    100% { transform: translate3d(2.5%, -1.5%,0) scale(1.02);}
}

@keyframes rise {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes riseSm {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes floatY {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-7px); }
}
@keyframes pulseSoft {
    0%, 100% { opacity: 1;   transform: scale(1);   }
    50%      { opacity: .55; transform: scale(.86); }
}
@keyframes beat {
    0%, 100% { transform: scale(1); }
    30%      { transform: scale(1.18); }
    60%      { transform: scale(1); }
}
@keyframes spinSlow { to { transform: rotate(360deg); } }
@keyframes iconPop {
    0%   { transform: translateY(0) scale(1) rotate(0); }
    35%  { transform: translateY(-5px) scale(1.22) rotate(-12deg); }
    70%  { transform: translateY(0) scale(1) rotate(0); }
    100% { transform: translateY(0) scale(1) rotate(0); }
}
@keyframes navIconIn {
    0%   { opacity: 0; transform: translateY(-14px) rotate(-25deg) scale(.5); }
    60%  { opacity: 1; transform: translateY(2px)  rotate(4deg)   scale(1.08); }
    100% { opacity: 1; transform: translateY(0)  rotate(0)     scale(1); }
}
@keyframes sheen {
    0%   { transform: translateX(-130%) skewX(-18deg); }
    100% { transform: translateX(320%)  skewX(-18deg); }
}
@keyframes shimmer {
    from { background-position: -220% 0; }
    to   { background-position:  220% 0; }
}
@keyframes gradientMove {
    from { background-position: 0% center; }
    to   { background-position: 200% center; }
}
@keyframes borderDance {
    from { --spin: 0deg; }
    to   { --spin: 360deg; }
}
@keyframes tick {
    0%, 100% { opacity: .35; }
    50%      { opacity: 1; }
}
@keyframes enterUp {
    from { opacity: 0; transform: translateY(60px) scale(.985); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}
@keyframes dropLine {
    from { transform: scaleY(0); opacity: 0; }
    to   { transform: scaleY(1); opacity: 1; }
}

/* =========================================================
   HEADER + TOP NAVIGATION
   ========================================================= */
[data-testid="stHeader"] {
    position: fixed !important;
    top: 0; left: 0; right: 0;
    height: var(--header-h);
    z-index: 100000;
    background: linear-gradient(180deg, rgba(7,7,12,.92) 0%, rgba(7,7,12,.78) 65%, rgba(7,7,12,0) 100%);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    border-bottom: 1px solid transparent;
    box-shadow: 0 1px 0 rgba(255,255,255,.05);
    transition: height .4s var(--ease), background .4s ease;
    animation: fadeIn .6s ease both;
}
[data-testid="stToolbar"] {
    height: var(--header-h) !important;
    padding: 0 1.6rem !important;
    align-items: center;
}

/* sidebar toggle — we don't have a sidebar */
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* brand mark + wordmark */
[data-testid="stHeader"] div:has(> [data-testid="stLogo"]),
[data-testid="stHeader"] [data-testid="stLogoLink"] {
    display: inline-flex;
    align-items: center;
    gap: .7rem;
    text-decoration: none;
}
[data-testid="stLogo"],
[data-testid="stLogoLink"] img,
[data-testid="stLogoLink"] svg {
    width: 32px !important;
    height: 32px !important;
    max-height: 32px !important;
    transition: transform .55s var(--ease), filter .45s ease;
    filter: drop-shadow(0 6px 16px rgba(124,92,255,.45));
}
[data-testid="stHeader"] div:has(> [data-testid="stLogo"])::after,
[data-testid="stHeader"] [data-testid="stLogoLink"]::after {
    content: "Noir";
    font-family: var(--font-display);
    font-weight: 400;
    font-size: 1.55rem;
    letter-spacing: 0.02em;
    line-height: 1;
    background: linear-gradient(96deg, #FFFFFF 10%, #C8C2FF 55%, #8FF0E4 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    transform: translateY(-2px);
}
[data-testid="stHeader"]:hover div:has(> [data-testid="stLogo"]) img,
[data-testid="stHeader"]:hover [data-testid="stLogo"] {
    transform: rotate(-8deg) scale(1.07);
    filter: drop-shadow(0 10px 24px rgba(79,209,197,.55));
}

/* the pill nav — absolutely centered in the header */
[data-testid="stTopNav"] {
    position: absolute !important;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 5px;
    border-radius: 999px;
    background: rgba(255,255,255,.045);
    border: 1px solid var(--line);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.07),
        0 18px 44px -26px rgba(0,0,0,.95);
}
[data-testid="stTopNav"] > * { animation: riseSm .6s var(--ease) both; }
[data-testid="stTopNav"] > *:nth-child(1) { animation-delay: .10s; }
[data-testid="stTopNav"] > *:nth-child(2) { animation-delay: .18s; }
[data-testid="stTopNav"] > *:nth-child(3) { animation-delay: .26s; }
[data-testid="stTopNav"] > *:nth-child(4) { animation-delay: .34s; }
[data-testid="stTopNav"] > *:nth-child(5) { animation-delay: .42s; }

[data-testid="stTopNavLink"] {
    position: relative;
    display: inline-flex !important;
    align-items: center;
    gap: .5rem;
    padding: .58rem 1.12rem !important;
    border-radius: 999px;
    font-family: var(--font-body);
    font-size: .93rem;
    font-weight: 500;
    letter-spacing: -0.005em;
    color: var(--text-dim) !important;    border: 1px solid transparent !important;
    overflow: hidden;
    transition:
        color .28s ease,
        background .32s ease,
        border-color .32s ease,
        transform .45s var(--ease),
        box-shadow .45s ease;
}
[data-testid="stTopNavLink"] * { color: inherit !important; }
[data-testid="stTopNavLink"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, transparent 20%, rgba(255,255,255,.16) 50%, transparent 80%);
    transform: translateX(-130%);
    pointer-events: none;
}
[data-testid="stTopNavLink"]:hover::before { animation: sheen .9s var(--ease); }

[data-testid="stTopNavLink"] [data-testid="stIconMaterial"],
[data-testid="stTopNavLink"] svg {
    font-size: 1.18rem;
    transition: transform .5s var(--ease), filter .4s ease;
    transform-origin: 50% 65%;
    animation: navIconIn .7s var(--ease) both;
    animation-delay: .25s;
}
[data-testid="stTopNavLink"]:hover {
    color: #FFFFFF !important;
    background: rgba(255,255,255,.07);
    border-color: rgba(255,255,255,.10) !important;
    transform: translateY(-2px);
}
[data-testid="stTopNavLink"]:hover [data-testid="stIconMaterial"] {
    transform: translateY(-3px) scale(1.16) rotate(-9deg);
    filter: drop-shadow(0 6px 14px rgba(124,92,255,.75));
}
[data-testid="stTopNavLink"]:active { transform: translateY(0) scale(.97); }

[data-testid="stTopNavLink"][aria-current="page"] {
    color: #fff !important;
    background:
        linear-gradient(140deg, rgba(124,92,255,.42), rgba(91,140,255,.24) 55%, rgba(79,209,197,.20)),
        rgba(255,255,255,.04);
    border-color: rgba(255,255,255,.18) !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.22),
        0 10px 26px -14px rgba(124,92,255,.9);
    font-weight: 600;
}
[data-testid="stTopNavLink"][aria-current="page"] [data-testid="stIconMaterial"],
[data-testid="stTopNavLink"][aria-current="page"] svg {
    animation: iconPop .8s var(--ease) both;
}
[data-testid="stTopNavLink"][aria-current="page"]::after {
    content: "";
    position: absolute;
    left: 26%;
    right: 26%;
    bottom: 5px;
    height: 2px;
    border-radius: 2px;
    background: linear-gradient(90deg, transparent, #8FF0E4, transparent);
    animation: dropLine .6s var(--ease) both;
    animation-delay: .2s;
    opacity: .9;
}

/* right hand header actions */
[data-testid="stHeaderActionElements"] {
    opacity: .55;
    transition: opacity .3s ease;
}
[data-testid="stHeaderActionElements"]:hover { opacity: 1; }

/* =========================================================
   LAYOUT
   ========================================================= */
.block-container {
    max-width: 1240px;
    margin: 0 auto;
    padding: calc(var(--header-h) + 3.4rem) 2.4rem 7rem !important;
}
[data-testid="stAppViewContainer"] { padding-top: 0; }

/* =========================================================
   TYPOGRAPHY — display face is the dot-matrix Nothing Font,
   so tracking must stay positive to avoid glyph overlap.
   ========================================================= */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display) !important;
    color: var(--text) !important;
    letter-spacing: 0.012em !important;
    word-spacing: 0.06em !important;
    font-weight: 400 !important;
    line-height: 1.16 !important;
    animation: rise .7s var(--ease) both;
}
p, div, span, label, li, td, th {
    color: var(--text);
    font-family: var(--font-body);
}
[data-testid="stMarkdownContainer"] p { line-height: 1.68; color: var(--text-dim); }
a { color: var(--mint); text-decoration: none; transition: opacity .25s ease; }
a:hover { opacity: .8; }

.page-title {
    font-family: var(--font-display) !important;
    font-size: clamp(2rem, 3.4vw, 2.75rem) !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
    word-spacing: .08em !important;
    line-height: 1 !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: .85rem;
    text-transform: uppercase;
}
.page-title .msym { font-size: 1.7rem; color: var(--violet); }

/* =========================================================
   HERO
   ========================================================= */
div[data-testid="stVerticalBlock"][class*="st-key-hero"] {
    position: relative;
    overflow: hidden;
    padding: 4.6rem 3.4rem 3rem !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--r-xl) !important;
    background:
        radial-gradient(120% 140% at 8% -20%, rgba(124,92,255,.28), transparent 55%),
        radial-gradient(90% 120% at 96% 8%, rgba(79,209,197,.16), transparent 55%),
        linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.012) 55%, transparent),
        rgba(10,10,17,.72);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.07),
        0 40px 90px -50px rgba(0,0,0,1);
    animation: enterUp .95s var(--ease) both;
}
div[data-testid="stVerticalBlock"][class*="st-key-hero"]::before {
    content: "";
    position: absolute;
    top: -40%;
    left: -10%;
    width: 60%;
    height: 180%;
    background: conic-gradient(from 180deg, transparent, rgba(139,109,255,.16), transparent 42%);
    animation: spinSlow 24s linear infinite;
    pointer-events: none;
    filter: blur(28px);
}
div[data-testid="stVerticalBlock"][class*="st-key-hero"]::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(115deg, rgba(139,109,255,.75), transparent 38%, transparent 62%, rgba(79,209,197,.55));
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
            mask-composite: exclude;
    pointer-events: none;
}
div[data-testid="stVerticalBlock"][class*="st-key-hero"] > * { position: relative; z-index: 1; }

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .6rem;
    padding: .5rem 1rem .5rem .85rem;
    font-family: var(--font-label);
    font-size: .76rem;
    font-weight: 400;
    letter-spacing: .16em;
    text-transform: uppercase;
    color: #D9D5F5;
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 999px;
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(8px);
    margin-bottom: 1.7rem;
    animation: riseSm .7s var(--ease) both;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.09);
}
.eyebrow-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--mint);
    box-shadow: 0 0 0 0 rgba(79,209,197,.7);
    animation: pulseSoft 2.1s ease-in-out infinite;
}

.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(3rem, 6.4vw, 5.75rem) !important;
    font-weight: 400 !important;
    text-transform: uppercase !important;
    line-height: 1.04 !important;
    letter-spacing: 0.018em !important;
    word-spacing: 0.06em !important;
    padding: 0 !important;
    overflow-wrap: break-word;
    margin: 0 0 1.6rem !important;
    background: linear-gradient(96deg, #FFFFFF 6%, #D6D0FF 32%, #FFFFFF 52%, #A9F2EA 78%, #FFFFFF 96%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: rise .95s var(--ease) both, gradientMove 11s linear infinite;
}
.hero-sub {
    font-size: 1.14rem;
    line-height: 1.75;
    font-weight: 300;
    color: var(--text-dim);
    max-width: 640px;
    margin: 0 0 2.3rem;
    animation: rise .95s var(--ease) both .12s;
}
.hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem 1.6rem;
    margin-top: 2rem;
    padding-top: 1.6rem;
    border-top: 1px solid var(--line);
    animation: rise .9s var(--ease) both .3s;
}
.hero-meta span {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    font-family: var(--font-label);
    font-size: .8rem;
    letter-spacing: .07em;
    text-transform: uppercase;
    color: var(--text-dim);
    font-weight: 400;
}
.hero-meta .msym { color: var(--mint); }

/* =========================================================
   SECTION HEADS · CHIPS · ICONS
   ========================================================= */
.section-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 2rem;
    margin: 3.6rem 0 1.6rem;
    animation: rise .7s var(--ease) both;
}
.section-head .sh-eyebrow {
    display: flex;
    align-items: center;
    gap: .55rem;
    font-family: var(--font-label);
    font-size: .72rem;
    font-weight: 400;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--violet);
    margin-bottom: .7rem;
}
.section-head .sh-title {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 2.6vw, 2.15rem);
    font-weight: 400;
    letter-spacing: 0.014em;
    word-spacing: .05em;
    text-transform: uppercase;
    color: var(--text);
    margin: 0;
    line-height: 1.14;
}
.section-head .sh-sub {
    margin: .7rem 0 0;
    color: var(--text-dim);
    font-size: .97rem;
    font-weight: 300;
    line-height: 1.65;
    max-width: 560px;
}
.section-head .sh-rule {
    flex: 1;
    height: 1px;
    margin-bottom: .8rem;
    background: linear-gradient(90deg, var(--line-strong), transparent);
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .4rem .85rem;
    border-radius: 999px;
    font-size: .8rem;
    font-weight: 500;
    border: 1px solid var(--line);
    background: rgba(255,255,255,.04);
    color: var(--text-dim);
    transition: transform .4s var(--ease), border-color .3s ease, background .3s ease;
}
.chip:hover {
    transform: translateY(-2px);
    border-color: rgba(124,92,255,.55);
    background: rgba(124,92,255,.10);
}
.chip .msym { color: var(--violet); }

.msym {
    font-family: 'Material Symbols Rounded';
    font-weight: normal;
    font-style: normal;
    font-size: 1.25em;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    vertical-align: -0.16em;
    transition: transform .5s var(--ease), color .3s ease, filter .4s ease;
}
.msym-float  { animation: floatY 3.6s ease-in-out infinite; }
.msym-pulse  { animation: pulseSoft 2.4s ease-in-out infinite; }
.msym-beat   { animation: beat 2.2s ease-in-out infinite; }
.msym-spin   { animation: spinSlow 6s linear infinite; }
.msym-tick   { animation: tick 1.4s ease-in-out infinite; }

/* =========================================================
   CARDS
   ========================================================= */
div[data-testid="stVerticalBlock"][class*="st-key-"] {
    background:
        linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.008) 45%, transparent),
        rgba(11,11,18,.66);
    border: 1px solid var(--line) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.75rem;
    backdrop-filter: blur(10px);
    transition:
        transform .5s var(--ease),
        border-color .35s ease,
        box-shadow .5s ease,
        background .35s ease;
    animation: riseSm .7s var(--ease) both;
    position: relative;
    overflow: hidden;
}
div[data-testid="stVerticalBlock"][class*="st-key-"]::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.22), transparent);
    opacity: .5;
}
div[data-testid="stVerticalBlock"][class*="st-key-"]:hover {
    transform: translateY(-6px);
    border-color: rgba(124,92,255,.42) !important;
    box-shadow:
        0 30px 60px -32px rgba(124,92,255,.75),
        inset 0 1px 0 rgba(255,255,255,.06);
}
div[data-testid="stVerticalBlock"][class*="st-key-"]:hover::after {
    background: linear-gradient(90deg, transparent, rgba(139,109,255,.9), rgba(79,209,197,.6), transparent);
    opacity: 1;
}

.icon-chip {
    width: 50px;
    height: 50px;
    display: grid;
    place-items: center;
    border-radius: 15px;
    margin-bottom: 1.1rem;
    background: linear-gradient(145deg, rgba(124,92,255,.26), rgba(91,140,255,.10));
    border: 1px solid rgba(139,109,255,.42);
    color: #C7BBFF;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 10px 26px -16px rgba(124,92,255,.9);
    transition: transform .5s var(--ease), box-shadow .45s ease, border-color .35s ease;
    position: relative;
    overflow: hidden;
}
.icon-chip::before {
    content: "";
    position: absolute;
    inset: -40%;
    background: conic-gradient(from 0deg, transparent, rgba(143,240,228,.5), transparent 45%);
    animation: spinSlow 7s linear infinite;
    opacity: 0;
    transition: opacity .4s ease;
}
.icon-chip > * { position: relative; z-index: 1; }
.icon-chip .msym { font-size: 1.5rem; }
[class*="st-key-card"]:hover .icon-chip,
div[data-testid="stVerticalBlock"][class*="st-key-"]:hover .icon-chip {
    transform: translateY(-4px) rotate(-7deg) scale(1.06);
    border-color: rgba(143,240,228,.55);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.2), 0 18px 36px -18px rgba(79,209,197,.85);
}
[class*="st-key-card"]:hover .icon-chip::before,
div[data-testid="stVerticalBlock"][class*="st-key-"]:hover .icon-chip::before { opacity: 1; }

.card-title {
    font-family: var(--font-display);
    font-weight: 400;
    font-size: 1.2rem;
    letter-spacing: 0.014em;
    word-spacing: .05em;
    text-transform: uppercase;
    color: var(--text) !important;
    margin: 0 0 .55rem !important;
    display: flex;
    align-items: center;
    gap: .6rem;
    flex-wrap: wrap;
    line-height: 1.25;
}
.card-text {
    color: var(--text-dim) !important;
    font-size: .94rem;
    line-height: 1.68;
    font-weight: 300;
    margin: 0 !important;
}
.card-tag {
    display: inline-block;
    margin-bottom: 1rem;
    font-family: var(--font-label);
    font-size: .7rem;
    font-weight: 400;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--violet);
}

/* danger zone */
div[data-testid="stVerticalBlock"][class*="st-key-danger"] {
    border-color: rgba(255,92,124,.32) !important;
    background:
        radial-gradient(120% 130% at 100% 0%, rgba(255,92,124,.14), transparent 55%),
        rgba(11,11,18,.7) !important;
}
div[data-testid="stVerticalBlock"][class*="st-key-danger"] .icon-chip {
    background: linear-gradient(145deg, rgba(255,92,124,.26), rgba(255,92,124,.08));
    border-color: rgba(255,92,124,.45);
    color: #FFB3C2;
}
div[data-testid="stVerticalBlock"][class*="st-key-danger"]:hover {
    border-color: rgba(255,92,124,.6) !important;
    box-shadow: 0 30px 60px -34px rgba(255,92,124,.8);
}
div[data-testid="stVerticalBlock"][class*="st-key-danger"] .card-title { color: #FFD7DF; }
div[data-testid="stVerticalBlock"][class*="st-key-danger"] .stButton button {
    border-color: rgba(255,92,124,.4);
    color: #FFC6D1;
}
div[data-testid="stVerticalBlock"][class*="st-key-danger"] .stButton button:hover {
    border-color: rgba(255,92,124,.85);
    background: rgba(255,92,124,.14);
    color: #fff;
    box-shadow: 0 16px 38px -18px rgba(255,92,124,.95);
}

/* =========================================================
   BUTTONS
   ========================================================= */
.stButton button,
.stDownloadButton button,
.stFormSubmitButton button,
.stLinkButton button {
    font-family: var(--font-body);
    font-weight: 600;
    font-size: .94rem;
    letter-spacing: -0.006em;
    border-radius: 999px;
    padding: .72rem 1.4rem;
    min-height: 44px;
    border: 1px solid var(--line-strong);
    background: rgba(255,255,255,.045);
    color: var(--text);
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: .55rem;
    transition:
        transform .4s var(--ease),
        border-color .3s ease,
        background .3s ease,
        box-shadow .4s ease,
        color .3s ease;
}
.stButton button:hover,
.stDownloadButton button:hover,
.stFormSubmitButton button:hover,
.stLinkButton button:hover {
    transform: translateY(-3px);
    border-color: rgba(139,109,255,.65);
    background: rgba(124,92,255,.10);
    color: #fff;
    box-shadow: 0 16px 38px -18px rgba(124,92,255,.9);
}
.stButton button:active { transform: translateY(-1px) scale(.98); }

.stButton button::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(110deg, transparent 30%, rgba(255,255,255,.28) 50%, transparent 70%);
    transform: translateX(-120%);
    transition: transform .8s var(--ease);
    pointer-events: none;
}
.stButton button:hover::before { transform: translateX(120%); }

.stButton button svg,
.stButton button [data-testid="stIconMaterial"],
.stDownloadButton button [data-testid="stIconMaterial"],
.stFormSubmitButton button [data-testid="stIconMaterial"] {
    transition: transform .5s var(--ease);
}
.stButton button:hover [data-testid="stIconMaterial"] { transform: translateX(3px); }
.stButton button:hover svg { transform: scale(1.12); }

.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"],
.stButton button[data-testid="stBaseButton-primary"],
.stFormSubmitButton button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: var(--brand);
    background-size: 180% auto;
    border-color: rgba(255,255,255,.16);
    color: #fff;
    font-weight: 600;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.3),
        0 14px 34px -16px rgba(124,92,255,.95);
}
.stButton button[kind="primary"]:hover,
.stFormSubmitButton button[kind="primary"]:hover {
    background: var(--brand);
    background-size: 220% auto;
    animation: gradientMove 3.5s linear infinite;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.4),
        0 22px 46px -18px rgba(124,92,255,1);
}
.stButton button[kind="primary"]:hover [data-testid="stIconMaterial"] {
    transform: translateX(5px);
}
.stButton button:focus-visible {
    outline: 2px solid var(--mint);
    outline-offset: 3px;
}
.stButton button:disabled {
    opacity: .45;
    transform: none !important;
    box-shadow: none !important;
}

/* =========================================================
   METRICS
   ========================================================= */
[data-testid="stMetric"] {
    background:
        linear-gradient(180deg, rgba(255,255,255,.04), transparent 60%),
        rgba(11,11,18,.6);
    border: 1px solid var(--line);
    border-radius: var(--r) !important;
    padding: 1.25rem 1.35rem;
    transition: transform .45s var(--ease), border-color .35s ease, box-shadow .45s ease;
    animation: riseSm .7s var(--ease) both;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: rgba(139,109,255,.5);
    box-shadow: 0 26px 54px -30px rgba(124,92,255,.8);
}
[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    left: 0;
    top: 14%;
    bottom: 14%;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background: linear-gradient(180deg, var(--violet), var(--mint));
    transform: scaleY(.35);
    transform-origin: top;
    transition: transform .5s var(--ease);
}
[data-testid="stMetric"]:hover::before { transform: scaleY(1); }

[data-testid="stMetricLabel"] p {
    color: var(--text-mute) !important;
    font-family: var(--font-label) !important;
    font-size: .7rem !important;
    font-weight: 400 !important;
    text-transform: uppercase;
    letter-spacing: .18em !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-weight: 400 !important;
    color: var(--text);
    font-size: clamp(1.7rem, 2.3vw, 2.3rem) !important;
    letter-spacing: 0.03em !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricValue"] svg,
[data-testid="stMetricValue"] [data-testid="stIconMaterial"] { color: var(--violet); }
[data-testid="stMetricDelta"] {
    font-family: var(--font-label);
    font-size: .78rem;
    font-weight: 400;
    letter-spacing: .05em;
    border-radius: 999px;
    padding: .2rem .55rem;
    background: rgba(255,255,255,.05);
}
[data-testid="stMetricDelta"]:has(div[data-testid="stIconMaterial"]) { display: flex; align-items: center; gap: .3rem; }
[data-testid="stMetricDelta"] div { font-size: .82rem; }

/* =========================================================
   TABS
   ========================================================= */
[data-testid="stTabs"] {
    gap: .5rem;
    border-bottom: 1px solid var(--line);
    padding-bottom: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font-body);
    font-weight: 500;
    font-size: .95rem;
    color: var(--text-dim) !important;
    padding: .85rem 1.1rem !important;
    border-radius: var(--r-sm) var(--r-sm) 0 0;
    transition: color .3s ease, background .3s ease;
    position: relative;
}
[data-testid="stTabs"] [role="tab"]::after {
    content: "";
    position: absolute;
    left: 18%;
    right: 18%;
    bottom: -1px;
    height: 2px;
    background: linear-gradient(90deg, var(--violet), var(--mint));
    transform: scaleX(0);
    transform-origin: center;
    transition: transform .45s var(--ease);
}
[data-testid="stTabs"] [role="tab"]:hover { color: var(--text) !important; background: rgba(255,255,255,.035); }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #fff !important;
    font-weight: 600;
    background: rgba(124,92,255,.10);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]::after { transform: scaleX(1); }
[data-testid="stTabPanel"] { animation: riseSm .55s var(--ease) both; }

/* =========================================================
   FORMS
   ========================================================= */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    font-weight: 500 !important;
    font-size: .88rem;
    letter-spacing: -0.004em;
    color: var(--text-dim) !important;
}
input[type="text"], input[type="number"], input[type="password"],
input[type="search"], input[type="email"], input[type="url"],
textarea, [data-baseweb="input"] > div,
[data-baseweb="select"] > div {
    background: rgba(255,255,255,.045) !important;
    border: 1px solid var(--line-strong) !important;
    color: var(--text) !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--font-body) !important;
    font-size: .95rem !important;
    min-height: 46px;
    backdrop-filter: blur(8px);
    transition: border-color .3s ease, box-shadow .35s ease, background .3s ease;
}
input:hover, textarea:hover,
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover {
    border-color: rgba(139,109,255,.5) !important;
}
input:focus, textarea:focus,
[data-baseweb="input"]:focus-within > div, [data-baseweb="select"]:focus-within > div {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 4px rgba(124,92,255,.16) !important;
    background: rgba(255,255,255,.06) !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder { color: var(--text-mute); }

/* select / dropdown chevrons */
[data-baseweb="select"] svg { color: var(--violet) !important; }
[data-baseweb="menu"] {
    background: #10101A !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: var(--r-sm) !important;
    box-shadow: 0 30px 60px -30px #000 !important;
    backdrop-filter: blur(18px);
}
[data-baseweb="menu"] li { font-size: .93rem; }
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[data-iso-focused="true"] { background: rgba(124,92,255,.22) !important; }

/* radio + segmented */
[data-testid="stRadio"] > div {
    gap: .55rem;
}
[data-testid="stRadio"] [role="radiogroup"] { gap: .5rem; }
[data-testid="stRadio"] [role="radio"],
.stButtonGroup button {
    border: 1px solid var(--line) !important;
    background: rgba(255,255,255,.035) !important;
    border-radius: 999px !important;
    color: var(--text-dim) !important;
    padding: .5rem 1.05rem !important;
    font-size: .88rem;
    font-weight: 500;
    transition: all .35s var(--ease);
}
[data-testid="stRadio"] [role="radio"]:hover,
.stButtonGroup button:hover {
    border-color: rgba(139,109,255,.5) !important;
    color: var(--text) !important;
    transform: translateY(-2px);
}
[data-testid="stRadio"] [role="radio"][aria-checked="true"],
.stButtonGroup button[kind="primary"],
.stButtonGroup button[data-testid="stButtonSecondary"][aria-checked="true"] {
    background: linear-gradient(140deg, rgba(124,92,255,.4), rgba(91,140,255,.22)) !important;
    border-color: rgba(255,255,255,.22) !important;
    color: #fff !important;
    font-weight: 600;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.2), 0 10px 26px -16px rgba(124,92,255,.9);
}

/* checkbox */
[data-testid="stCheckbox"] {
    transition: transform .3s var(--ease);
}
[data-testid="stCheckbox"]:hover { transform: translateX(3px); }
[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: var(--violet);
    width: 18px;
    height: 18px;
    cursor: pointer;
}

/* toggle */
[data-testid="stWidget"] [role="switch"],
.st-bhz9p5, .st-emotion-cache-1m8l8sl {
    transition: background .4s ease, border-color .3s ease !important;
}
[data-testid="stWidget"] [role="switch"][aria-checked="true"] {
    background: var(--brand) !important;
    border-color: rgba(255,255,255,.2) !important;
}
[data-testid="stWidget"] [role="switch"]:hover {
    box-shadow: 0 0 0 5px rgba(124,92,255,.15);
}

/* slider */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    background: var(--violet);
}
[data-testid="stSlider"] div[role="slider"] {
    border: 2px solid #fff;
    box-shadow: 0 6px 18px -6px rgba(124,92,255,1);
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div,
[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--violet), var(--mint));
}

/* =========================================================
   DATA / TABLES / CHARTS
   ========================================================= */
[data-testid="stDataFrame"] {
    border-radius: var(--r) !important;
    overflow: hidden;
    border: 1px solid var(--line);
    background: rgba(11,11,18,.6);
    --gdg-font-family: 'JetBrains Mono', monospace;
    --gdg-text-color: #E9E9F4;
    --gdg-text-dark-color: #16161F;
    --gdg-bg-cell: #0D0D15;
    --gdg-bg-header: #131320;
    --gdg-bg-header-hover: #191927;
    --gdg-bg-bubble: rgba(124,92,255,.28);
    --gdg-accent-color: #7C5CFF;
    --gdg-border-color: rgba(255,255,255,.07);
    --gdg-header-font-family: 'Inter', sans-serif;
}
[data-testid="stArrowDataFrame"] {
    border-radius: var(--r) !important;
    border: 1px solid var(--line);
    overflow: hidden;
}
[data-testid="stTable"] {
    background: rgba(11,11,18,.6);
    border: 1px solid var(--line);
    border-radius: var(--r);
}
[data-testid="stTable"] thead th {
    font-family: var(--font-mono);
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--text-mute);
    background: rgba(255,255,255,.03);
}

.vega-embed {
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
}
.vega-embed .vega-actions { display: none !important; }
[data-testid="stVegaLiteChart"] .chart-container,
[data-testid="stVegaLiteChart"] figure { margin: 0 !important; }

/* =========================================================
   MISC COMPONENTS
   ========================================================= */
hr, [data-testid="stHeadingDivider"] {
    border: none !important;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--line-strong) 20%, var(--line-strong) 80%, transparent) !important;
    margin: 2.4rem 0 !important;
    opacity: .8;
}

[data-testid="stExpander"] {
    background: rgba(11,11,18,.6) !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--r) !important;
    transition: border-color .35s ease, box-shadow .45s ease, transform .4s var(--ease);
}
[data-testid="stExpander"]:hover {
    border-color: rgba(139,109,255,.45) !important;
    box-shadow: 0 24px 50px -34px rgba(124,92,255,.9);
    transform: translateY(-3px);
}
[data-testid="stExpander"] summary {
    font-weight: 400 !important;
    font-family: var(--font-display);
    letter-spacing: 0.014em;
    text-transform: uppercase;
}

[data-testid="stAlert"],
[data-testid="stNotification"] {
    background: rgba(11,11,18,.75) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: var(--r) !important;
    backdrop-filter: blur(10px);
    animation: riseSm .5s var(--ease) both;
}
[data-testid="stAlert"] > div > div > div,
[data-testid="stAlert"] p { font-size: .93rem; }

[data-testid="stProgress"] [data-testid="stProgressBarTrack"] {
    height: 8px;
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    overflow: hidden;
}
[data-testid="stProgress"] [role="progressbar"] {
    background: var(--brand) !important;
    border-radius: 999px;
    background-size: 200% 100% !important;
    animation: shimmer 3s linear infinite, riseSm .6s var(--ease) both;
    position: relative;
}
[data-testid="stProgress"] [role="progressbar"]::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.55), transparent);
    transform: translateX(-100%);
    animation: sheen 2.6s var(--ease-io) infinite;
}

.stDivider, div[data-testid="stDivider"] { border-color: var(--line); }

[data-testid="stSpinner"] {
    border-radius: var(--r);
    background: rgba(11,11,18,.75);
    border: 1px solid var(--line);
    padding: 1rem;
}
[data-testid="stCodeBlock"] {
    background: #0C0C14 !important;
    border: 1px solid var(--line);
    border-radius: var(--r);
}
code, pre {
    font-family: var(--font-mono) !important;
    font-size: .88rem;
    background: rgba(255,255,255,.05) !important;
    border-radius: 7px;
}
pre { border: 1px solid var(--line); padding: 1.1rem 1.2rem; }

[data-testid="stToast"] {
    background: rgba(14,14,22,.94) !important;
    border: 1px solid rgba(139,109,255,.45) !important;
    border-radius: 999px !important;
    backdrop-filter: blur(16px);
    box-shadow: 0 26px 50px -26px #000;
    font-weight: 500;
}

[data-testid="stPageLink"] button {
    border-radius: 999px;
    border: 1px solid var(--line-strong);
    background: rgba(255,255,255,.04);
}

/* =========================================================
   FOOTER
   ========================================================= */
.noir-footer {
    margin-top: 4.5rem;
    padding-top: 2.2rem;
    border-top: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1.2rem;
    animation: rise .8s var(--ease) both;
}
.noir-footer .nf-brand {
    display: flex;
    align-items: center;
    gap: .6rem;
    font-family: var(--font-display);
    font-weight: 400;
    font-size: 1.25rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text);
}
.noir-footer .nf-brand .msym {
    color: var(--violet);
    animation: spinSlow 14s linear infinite;
}
.noir-footer .nf-links { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.noir-footer .nf-links span {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    font-family: var(--font-label);
    font-size: .78rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--text-mute);
    transition: color .3s ease, transform .35s var(--ease);
    cursor: default;
}
.noir-footer .nf-links span:hover { color: var(--text); transform: translateY(-2px); }
.noir-footer .nf-copy {
    font-family: var(--font-label);
    font-size: .78rem;
    letter-spacing: .1em;
    color: var(--text-mute);
}

/* =========================================================
   SCROLLBAR · MOTION · RESPONSIVE
   ========================================================= */
::-webkit-scrollbar { width: 11px; height: 11px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(124,92,255,.7), rgba(79,209,197,.5));
    border-radius: 999px;
    border: 3px solid var(--bg);
}
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #9B80FF, #6FE3D6); }
* { scrollbar-width: thin; scrollbar-color: rgba(124,92,255,.6) transparent; }

::selection { background: rgba(124,92,255,.45); color: #fff; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .001ms !important;
    }
}

@media (max-width: 900px) {
    .block-container { padding: calc(var(--header-h) + 1.6rem) 1.15rem 4rem !important; }
    [data-testid="stHeader"] { backdrop-filter: blur(18px); }
    [data-testid="stTopNav"] {
        position: static;
        transform: none;
        flex-wrap: wrap;
        justify-content: center;
        border-radius: 20px;
        margin: 0 auto;
        max-width: 100%;
    }
    [data-testid="stToolbar"] { flex-wrap: wrap; height: auto !important; padding: .7rem 1rem !important; }
    :root { --header-h: 128px; }
    div[data-testid="stVerticalBlock"][class*="st-key-hero"] { padding: 2.6rem 1.5rem 2.2rem !important; }
    .hero-title { font-size: clamp(2.1rem, 9vw, 3rem); }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    .section-head { flex-direction: column; align-items: flex-start; gap: .8rem; }
}
</style>
"""


def inject_theme() -> None:
    st.markdown(FONTS + CSS, unsafe_allow_html=True)


def icon(name: str, size: str = "1.25rem", cls: str = "") -> str:
    """Inline Material Symbols ligature icon."""
    extra = f" {cls}" if cls else ""
    return f'<span class="msym{extra}" style="font-size:{size}">{name}</span>'


def eyebrow(text: str, dot: bool = True) -> str:
    lead = '<span class="eyebrow-dot"></span>' if dot else ""
    return f'<div class="eyebrow">{lead}<span>{text}</span></div>'


def chip(text: str, ic: str | None = None) -> str:
    lead = icon(ic, "1rem") if ic else ""
    return f'<span class="chip">{lead}{text}</span>'


def hero(eyebrow_text: str, title: str, subtitle: str, meta: list[tuple[str, str]] | None = None) -> str:
    """Rendered inside a bordered container keyed `hero`."""
    st.markdown(eyebrow(eyebrow_text), unsafe_allow_html=True)
    st.markdown(f'<h1 class="hero-title">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-sub">{subtitle}</p>', unsafe_allow_html=True)
    if meta:
        items = "".join(
            f"<span>{icon(ic, '1.05rem')}{text}</span>" for text, ic in meta
        )
        st.markdown(f'<div class="hero-meta">{items}</div>', unsafe_allow_html=True)


def section_head(title: str, sub: str = "", eyebrow_text: str = "", rule: bool = True) -> None:
    eb = (
        f'<div class="sh-eyebrow">{icon("auto_awesome", "0.95rem")}{eyebrow_text}</div>'
        if eyebrow_text
        else ""
    )
    r = '<div class="sh-rule"></div>' if rule else ""
    s = f'<p class="sh-sub">{sub}</p>' if sub else ""
    st.markdown(
        f'<div class="section-head"><div>{eb}<p class="sh-title">{title}</p>{s}</div>{r}</div>',
        unsafe_allow_html=True,
    )


def card_icon(name: str, size: str = "1.5rem") -> str:
    return f'<div class="icon-chip">{icon(name, size)}</div>'


def page_title(title: str, ic: str) -> None:
    st.markdown(
        f'<div class="page-title">{icon(ic, "1.9rem", "msym-float")}{title}</div>',
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        f"""
<div class="noir-footer">
    <div class="nf-brand">{icon("blur_on", "1.35rem")} Noir</div>
    <div class="nf-links">
        <span>{icon("description", "1rem")} Docs</span>
        <span>{icon("code", "1rem")} API</span>
        <span>{icon("shield_lock", "1rem")} Security</span>
        <span>{icon("public", "1rem")} Status</span>
    </div>
    <div class="nf-copy">© 2026 Noir Labs</div>
</div>
""",
        unsafe_allow_html=True,
    )
