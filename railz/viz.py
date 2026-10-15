from __future__ import annotations

from typing import Dict, List, Optional

import streamlit as st

from railz.trace import RAIL_DISPLAY, Trace

KIND_COLOR = {
    "interaction": "#7C5CFF",
    "rail": "#7FE3D6",
    "action": "#FFC24B",
    "llm": "#5CA8FF",
    "internal": "#8A8A9A",
}

RAIL_ICON = {
    "check jailbreak": "shield",
    "check sensitive data": "key_off",
    "check on topic": "topic",
    "self check output": "fact_check",
    "check toxicity": "gavel",
}

PIPELINE_ORDER = [
    "check jailbreak",
    "check sensitive data",
    "check on topic",
    "GENERATE",
    "self check output",
    "check toxicity",
]


COMPONENT_CSS = """
<style>
:root {
  --rz-violet:#7C5CFF; --rz-teal:#7FE3D6; --rz-amber:#FFC24B;
  --rz-blue:#5CA8FF; --rz-red:#FF5C7C; --rz-green:#4BE39A; --rz-grey:#8A8A9A;
  --rz-line:rgba(255,255,255,.09); --rz-panel:rgba(255,255,255,.028);
}
@keyframes rz-grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes rz-fade { from { opacity:0; transform:translateY(6px);} to {opacity:1; transform:none;} }
@keyframes rz-pulse { 0%,100% { box-shadow:0 0 0 0 rgba(255,92,124,.5);} 50% { box-shadow:0 0 0 10px rgba(255,92,124,0);} }
@keyframes rz-glow { 0%,100% { opacity:.55;} 50% { opacity:1;} }
@keyframes rz-sweep { from { left:-30%; } to { left:130%; } }

.rz-panel {
  background:var(--rz-panel); border:1px solid var(--rz-line); border-radius:18px;
  padding:1.1rem 1.2rem; margin:.35rem 0; position:relative; overflow:hidden;
  animation:rz-fade .4s ease both;
}
.rz-head { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.9rem; }
.rz-head .rz-title {
  font-family:var(--font-display,'Nothing Font',sans-serif); text-transform:uppercase;
  letter-spacing:.14em; font-size:.72rem; color:rgba(242,242,247,.62);
}
.rz-head .rz-sub { font-family:var(--font-mono,'JetBrains Mono',monospace); font-size:.68rem; color:rgba(242,242,247,.4); }

/* ---------- waterfall ---------- */
.rz-wf { display:flex; flex-direction:column; gap:.28rem; }
.rz-row { display:grid; grid-template-columns:minmax(120px,220px) 1fr; align-items:center; gap:.8rem; }
.rz-row .rz-name {
  font-family:var(--font-label,'JetBrains Mono',monospace); font-size:.72rem;
  color:rgba(242,242,247,.82); display:flex; align-items:center; gap:.45rem;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.rz-row .rz-name .rz-d { color:rgba(242,242,247,.3); font-size:.6rem; }
.rz-track {
  position:relative; height:20px; border-radius:7px;
  background:linear-gradient(90deg, rgba(255,255,255,.03), rgba(255,255,255,.05));
  border:1px solid rgba(255,255,255,.05);
}
.rz-bar {
  position:absolute; top:2px; height:14px; border-radius:6px; min-width:3px;
  transform-origin:left center; animation:rz-grow .55s cubic-bezier(.2,.8,.2,1) both;
}
.rz-bar .rz-barlabel {
  position:absolute; right:6px; top:50%; transform:translateY(-50%);
  font-family:var(--font-mono,monospace); font-size:.56rem; color:rgba(5,5,7,.72);
  white-space:nowrap;
}
.rz-gridline { position:absolute; top:0; bottom:0; width:1px; background:rgba(255,255,255,.06); }

/* ---------- tree ---------- */
.rz-tree { font-family:var(--font-label,'JetBrains Mono',monospace); }
.rz-node {
  display:flex; align-items:center; gap:.6rem; padding:.34rem .5rem;
  border-left:2px solid var(--rz-line); margin-left:calc(var(--d)*18px);
  border-radius:0 8px 8px 0; animation:rz-fade .35s ease both;
}
.rz-node:hover { background:rgba(255,255,255,.035); }
.rz-dot { width:8px; height:8px; border-radius:50%; flex:none; }
.rz-node .rz-nlabel { font-size:.74rem; color:rgba(242,242,247,.9); }
.rz-node .rz-ndetail { font-size:.62rem; color:rgba(242,242,247,.4); }
.rz-node .rz-ndur { margin-left:auto; font-size:.64rem; color:rgba(242,242,247,.55); }
.rz-node.blocked { background:rgba(255,92,124,.08); border-left-color:var(--rz-red); }

/* ---------- pipeline ---------- */
.rz-pipe { display:flex; align-items:stretch; gap:0; flex-wrap:wrap; }
.rz-pstep { display:flex; align-items:center; }
.rz-node-card {
  width:118px; border:1px solid var(--rz-line); border-radius:14px; padding:.7rem .6rem;
  background:rgba(255,255,255,.02); text-align:center; position:relative;
  opacity:.35; animation:rz-fade .4s ease both;
}
.rz-node-card.on { opacity:1; }
.rz-node-card .rz-ico {
  display:inline-flex; width:30px; height:30px; align-items:center; justify-content:center;
  border-radius:9px; margin-bottom:.4rem; font-size:.95rem;
}
.rz-node-card .rz-nname { font-family:var(--font-mono,monospace); font-size:.6rem; color:rgba(242,242,247,.85); line-height:1.2; }
.rz-node-card .rz-nstat { font-family:var(--font-display,sans-serif); text-transform:uppercase; letter-spacing:.1em; font-size:.52rem; margin-top:.3rem; }
.rz-node-card.passed { border-color:rgba(75,227,154,.4); box-shadow:0 0 0 1px rgba(75,227,154,.12); }
.rz-node-card.blocked { border-color:rgba(255,92,124,.55); animation:rz-pulse 1.4s ease-in-out infinite; }
.rz-node-card.skipped { opacity:.18; }
.rz-node-card.gen { border-color:rgba(92,168,255,.45); }
.rz-link { width:26px; height:2px; background:var(--rz-line); position:relative; }
.rz-link.on { background:linear-gradient(90deg,var(--rz-teal),var(--rz-violet)); }
.rz-link.blocked { background:var(--rz-red); }

/* ---------- verdict pill / badge ---------- */
.rz-pill {
  display:inline-flex; align-items:center; gap:.4rem; padding:.28rem .6rem; border-radius:999px;
  font-family:var(--font-mono,monospace); font-size:.64rem; border:1px solid var(--rz-line);
}
.rz-pill.passed { color:#4BE39A; border-color:rgba(75,227,154,.35); background:rgba(75,227,154,.08); }
.rz-pill.blocked { color:#FF7C97; border-color:rgba(255,92,124,.4); background:rgba(255,92,124,.09); }
.rz-pill.info { color:rgba(242,242,247,.65); }
.rz-pill .rz-pdot { width:7px; height:7px; border-radius:50%; background:currentColor; }

.rz-metrics { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.2rem; }
.rz-metric {
  flex:1 1 110px; border:1px solid var(--rz-line); border-radius:14px; padding:.6rem .7rem;
  background:rgba(255,255,255,.02);
}
.rz-metric .rz-mv { font-family:var(--font-display,sans-serif); font-size:1.15rem; color:#fff; }
.rz-metric .rz-ml { font-family:var(--font-mono,monospace); font-size:.56rem; text-transform:uppercase; letter-spacing:.12em; color:rgba(242,242,247,.42); }

/* ---------- blocked card ---------- */
.rz-block {
  border:1px solid rgba(255,92,124,.35); border-radius:18px; overflow:hidden;
  background:linear-gradient(180deg, rgba(255,92,124,.10), rgba(255,92,124,.02));
  animation:rz-fade .4s ease both;
}
.rz-block .rz-btop { display:flex; align-items:center; gap:.7rem; padding:.9rem 1.1rem; border-bottom:1px solid rgba(255,92,124,.18); }
.rz-block .rz-bicon {
  width:34px; height:34px; border-radius:11px; display:flex; align-items:center; justify-content:center;
  background:rgba(255,92,124,.16); color:#FF7C97; font-size:1rem;
}
.rz-block .rz-bname { font-family:var(--font-display,sans-serif); text-transform:uppercase; letter-spacing:.1em; font-size:.8rem; color:#fff; }
.rz-block .rz-bflow { font-family:var(--font-mono,monospace); font-size:.62rem; color:rgba(255,124,151,.85); }
.rz-block .rz-bbody { padding:1rem 1.1rem; }
.rz-block .rz-breason { color:rgba(242,242,247,.85); font-size:.85rem; margin-bottom:.7rem; }
.rz-why { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:.4rem; }
.rz-why li { font-family:var(--font-mono,monospace); font-size:.68rem; color:rgba(242,242,247,.6); padding-left:1rem; position:relative; }
.rz-why li:before { content:"›"; position:absolute; left:0; color:var(--rz-red); }
.rz-match {
  font-family:var(--font-mono,monospace); font-size:.66rem; background:rgba(0,0,0,.35);
  border:1px solid var(--rz-line); border-radius:8px; padding:.3rem .5rem; margin:.2rem 0;
  color:rgba(242,242,247,.72);
}
.rz-compare { display:grid; grid-template-columns:1fr 1fr; gap:.7rem; margin-top:.9rem; }
.rz-ccol { border:1px solid var(--rz-line); border-radius:14px; padding:.8rem; background:rgba(255,255,255,.02); }
.rz-ccol h5 { font-family:var(--font-display,sans-serif); text-transform:uppercase; letter-spacing:.12em; font-size:.6rem; margin:0 0 .5rem; color:rgba(242,242,247,.5); }
.rz-ccol .rz-cbody { font-size:.82rem; color:rgba(242,242,247,.85); line-height:1.5; }
.rz-ccol.no { border-color:rgba(255,92,124,.3); }
.rz-ccol.yes { border-color:rgba(75,227,154,.3); }
@media (max-width:720px){ .rz-compare{grid-template-columns:1fr;} }

.rz-legend { display:flex; gap:.9rem; flex-wrap:wrap; margin-top:.7rem; }
.rz-legend span { font-family:var(--font-mono,monospace); font-size:.62rem; color:rgba(242,242,247,.5); display:flex; align-items:center; gap:.35rem; }
.rz-legend i { width:9px; height:9px; border-radius:3px; display:inline-block; }
.rz-empty { color:rgba(242,242,247,.45); font-family:var(--font-mono,monospace); font-size:.75rem; padding:.6rem 0; }
</style>
"""


def inject_styles() -> None:
    st.markdown(COMPONENT_CSS, unsafe_allow_html=True)


def _fmt_dur(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} s"


def _status_text(trace: Trace) -> str:
    return "blocked" if trace.blocked else "passed"


def status_pill(trace: Trace) -> str:
    cls = "blocked" if trace.blocked else "passed"
    text = f"blocked · {trace.blocked_by}" if trace.blocked else "passed all rails"
    return f'<span class="rz-pill {cls}"><span class="rz-pdot"></span>{text}</span>'


def metrics_html(trace: Trace) -> str:
    cells = [
        ("total", _fmt_dur(trace.total_duration)),
        ("input rails", _fmt_dur(trace.input_rails_duration)),
        ("generation", _fmt_dur(trace.generation_duration)),
        ("output rails", _fmt_dur(trace.output_rails_duration)),
        ("llm calls", str(trace.llm_calls_count)),
        ("tokens", f"{trace.total_tokens:,}"),
    ]
    inner = "".join(
        f'<div class="rz-metric"><div class="rz-mv">{v}</div><div class="rz-ml">{k}</div></div>'
        for k, v in cells
    )
    return f'<div class="rz-metrics">{inner}</div>'


def waterfall_html(trace: Trace) -> str:
    if not trace.spans:
        return '<div class="rz-empty">No spans captured for this turn.</div>'
    total = trace.waterfall_span()
    rows: List[str] = []
    for span in trace.spans:
        color = KIND_COLOR.get(span.kind, KIND_COLOR["internal"])
        if span.status == "blocked":
            color = "#FF5C7C"
        left = max(0.0, span.start / total * 100)
        width = max(1.2, span.duration / total * 100)
        delay = min(0.8, span.start / total * 0.8)
        indent = f'<span class="rz-d">{"└ " * 1 if span.depth else ""}</span>'
        label = f"{_fmt_dur(span.duration)}"
        dur_tag = "" if span.kind == "interaction" else f'<span style="color:rgba(242,242,247,.4);font-size:.6rem">{label}</span>'
        rows.append(
            f'<div class="rz-row">'
            f'  <div class="rz-name" style="padding-left:{span.depth * 14}px">{indent}{span.name} {dur_tag}</div>'
            f'  <div class="rz-track">'
            f'    <div class="rz-bar" style="left:{left:.3f}%;width:{width:.3f}%;background:{color};'
            f'animation-delay:{delay:.3f}s">'
            f'<span class="rz-barlabel">{_fmt_dur(span.duration)}</span></div>'
            f'  </div>'
            f'</div>'
        )
    legend = (
        '<div class="rz-legend">'
        '<span><i style="background:#7C5CFF"></i>turn</span>'
        '<span><i style="background:#7FE3D6"></i>rail</span>'
        '<span><i style="background:#FFC24B"></i>action</span>'
        '<span><i style="background:#5CA8FF"></i>llm call</span>'
        '<span><i style="background:#FF5C7C"></i>blocked</span>'
        '</div>'
    )
    return (
        '<div class="rz-panel">'
        '<div class="rz-head"><div class="rz-title">Span waterfall</div>'
        f'<div class="rz-sub">0 – {_fmt_dur(total)}</div></div>'
        f'<div class="rz-wf">{"".join(rows)}</div>{legend}</div>'
    )


def span_tree_html(trace: Trace) -> str:
    if not trace.spans:
        return ""
    by_id = trace.span_map()

    def render(node_id: str) -> str:
        node = by_id[node_id]
        color = KIND_COLOR.get(node.kind, KIND_COLOR["internal"])
        if node.status == "blocked":
            color = "#FF5C7C"
        extra = ""
        tokens = node.meta.get("total_tokens")
        if tokens:
            extra = f' · {tokens:,} tok'
        cls = "rz-node blocked" if node.status == "blocked" else "rz-node"
        html = (
            f'<div class="{cls}" style="--d:{node.depth}">'
            f'<span class="rz-dot" style="background:{color}"></span>'
            f'<span class="rz-nlabel">{node.name}</span>'
            f'<span class="rz-ndetail">{node.detail}{extra}</span>'
            f'<span class="rz-ndur">{_fmt_dur(node.duration)}</span>'
            f'</div>'
        )
        for child in node.children:
            html += render(child)
        return html

    inner = "".join(render(root.id) for root in trace.root_spans())
    return (
        '<div class="rz-panel"><div class="rz-head">'
        '<div class="rz-title">Span tree</div>'
        f'<div class="rz-sub">{len(trace.spans)} spans</div></div>'
        f'<div class="rz-tree">{inner}</div></div>'
    )


def pipeline_html(trace: Trace) -> str:
    ran = {rail.name: rail for rail in trace.rails}
    cards: List[str] = []
    lit = True
    for name in PIPELINE_ORDER:
        is_gen = name == "GENERATE"
        if is_gen:
            status = "passed"
            if trace.blocked and not any(r.type == "output" for r in trace.rails):
                status = "skipped"
                lit = False
            on = lit and not trace.blocked
            icon = "auto_awesome"
            label = "Generate answer"
            cls = f"rz-node-card gen {'on' if on else ''}"
            ico_color = "#5CA8FF"
        else:
            rail = ran.get(name)
            if rail is not None and rail.status == "blocked":
                status = "blocked"
                on = True
                lit = False
            elif rail is not None:
                status = "passed"
                on = lit
            else:
                status = "skipped"
                on = False
                lit = False
            icon = RAIL_ICON.get(name, "tune")
            label = RAIL_DISPLAY.get(name, (name, "", name))[2]
            cls = f"rz-node-card {'on' if on else ''} {status}"

        color = {"passed": "#4BE39A", "blocked": "#FF5C7C", "skipped": "#8A8A9A"}[status]
        if is_gen and status != "skipped":
            color = "#5CA8FF"
        cards.append(
            f'<div class="rz-pstep">'
            f'<div class="{cls}">'
            f'<span class="rz-ico" style="background:{color}22;color:{color}">'
            f'<span class="msym">{icon}</span></span>'
            f'<div class="rz-nname">{label}</div>'
            f'<div class="rz-nstat" style="color:{color}">{status}</div>'
            f'</div></div>'
        )
        if name != PIPELINE_ORDER[-1]:
            nxt = PIPELINE_ORDER[PIPELINE_ORDER.index(name) + 1]
            link_cls = "rz-link"
            if status == "blocked":
                link_cls += " blocked"
            elif status == "passed":
                link_cls += " on"
            cards.append(f'<div class="rz-pstep"><div class="{link_cls}"></div></div>')

    return (
        '<div class="rz-panel"><div class="rz-head">'
        '<div class="rz-title">Rail pipeline</div>'
        f'<div class="rz-sub">{len(trace.rails)} rails executed</div></div>'
        f'<div class="rz-pipe">{"".join(cards)}</div></div>'
    )


def blocked_card_html(trace: Trace) -> str:
    if not trace.blocked:
        return ""
    rail = next((r for r in trace.rails if r.status == "blocked"), None)
    action = rail.actions[0] if rail and rail.actions else None
    display = RAIL_DISPLAY.get(trace.blocked_by, ("Rail", "shield", trace.blocked_by))
    icon = RAIL_ICON.get(trace.blocked_by, "block")

    why: List[str] = []
    if action:
        for key, value in list(action.detail.items())[:3]:
            why.append(f"<li>{key}: {value}</li>")
    matches = ""
    if action:
        for match in action.matches[:4]:
            matches += f'<div class="rz-match">{match}</div>'

    baseline = trace.baseline_output or "—"
    blocked_col = (
        '<div class="rz-ccol no"><h5>With guardrails</h5>'
        f'<div class="rz-cbody">Blocked at <b>{trace.blocked_by}</b> in {_fmt_dur(trace.total_duration)} — '
        'the model never saw the request.</div></div>'
    )
    base_col = (
        '<div class="rz-ccol yes"><h5>Without guardrails</h5>'
        f'<div class="rz-cbody">{baseline}</div></div>'
    )

    return (
        '<div class="rz-block">'
        '<div class="rz-btop">'
        f'<div class="rz-bicon"><span class="msym">{icon}</span></div>'
        f'<div><div class="rz-bname">Blocked · {display[2]}</div>'
        f'<div class="rz-bflow">flow · {display[2].lower().replace(" ", "-")} · {action.name if action else ""}</div></div>'
        '</div>'
        '<div class="rz-bbody">'
        f'<div class="rz-breason">{trace.block_reason or "This request was blocked by a guardrail."}</div>'
        f'<ul class="rz-why">{"".join(why)}</ul>'
        f'{matches}'
        f'<div class="rz-compare">{blocked_col}{base_col}</div>'
        '</div></div>'
    )


def rail_cards_html(trace: Trace) -> str:
    if not trace.rails:
        return '<div class="rz-empty">No rails executed.</div>'
    cards = []
    for rail in trace.rails:
        display = RAIL_DISPLAY.get(rail.name, (rail.type.title() + " rail", "tune", rail.name))
        icon = RAIL_ICON.get(rail.name, "tune")
        status = rail.status
        color = "#FF5C7C" if status == "blocked" else "#4BE39A"
        action = rail.actions[0] if rail.actions else None
        reason = f'<div class="rz-breason" style="color:#FF7C97">{rail.reason}</div>' if rail.reason else ""
        cards.append(
            '<div class="rz-panel" style="margin:.3rem 0">'
            '<div class="rz-head" style="margin-bottom:.5rem">'
            f'<div class="rz-title" style="display:flex;align-items:center;gap:.5rem">'
            f'<span class="msym" style="font-size:1rem;color:{color}">{icon}</span>'
            f'{display[2]}</div>'
            f'<span class="rz-pill {status}"><span class="rz-pdot"></span>{status}</span></div>'
            f'{reason}'
            f'<div class="rz-sub">{_fmt_dur(rail.duration)} · {action.label if action else ""}</div>'
            '</div>'
        )
    return "".join(cards)
