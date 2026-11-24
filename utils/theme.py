"""Visual system for the cannabis sales intelligence dashboard.

Forest green, harvest gold and a soft sage paper, with the same chart and
spacing discipline as the NYC taxi dashboard.
"""

from __future__ import annotations

import base64
import html

import streamlit as st

# ------------------------------------------------------------------ palette ---
BG = "#E2ECD6"
SURFACE = "#FAFCF5"
SURFACE_ALT = "#E3E7D6"
BORDER = "#BCCDAE"
BORDER_SOFT = "#DFE4D3"

INK = "#10241B"
ASPHALT = "#10241B"
ASPHALT_2 = "#1B3A2C"
TITLE = "#10241B"
SUBTITLE = "#34403A"
MUTED = "#5F6B63"
FAINT = "#929C93"

YELLOW = "#E0B23C"
YELLOW_BRIGHT = "#F0C75E"
YELLOW_SOFT = "#F3E3B5"
ORANGE = "#1F7A3F"
ORANGE_BRIGHT = "#3FAE5A"
ORANGE_SOFT = "#CFE8D2"
TEAL = "#6E4F8F"
TEAL_BRIGHT = "#8C6BB0"
TEAL_SOFT = "#E6DDF0"
BLUE = "#416B8A"
BLUE_SOFT = "#DCE7EF"
CREAM = "#F8F8EF"

ACCENT = YELLOW
SECONDARY = ORANGE
TERTIARY = TEAL

GOLD_SCALE = [
    [0.0, "#F7F1DC"],
    [0.25, "#EBD48F"],
    [0.50, "#D9A93A"],
    [0.75, "#8FA14A"],
    [1.00, "#2F6B45"],
]
FOREST_SCALE = [
    [0.0, "#EEF1E4"],
    [0.35, "#B8C6AE"],
    [0.70, "#5F6B63"],
    [1.00, "#10241B"],
]
TEAL_SCALE = [
    [0.0, "#F3EFF8"],
    [0.45, "#D3C6E6"],
    [0.75, "#8C6BB0"],
    [1.00, "#4A3266"],
]


def _leaf(fill: str, stem: str | None = None) -> str:
    """Seven-leaflet cannabis leaf as SVG markup (100×100 box, base at 50,82)."""
    blades = [(0, 40), (-28, 34), (28, 34), (-58, 27), (58, 27), (-86, 17), (86, 17)]
    paths = "".join(
        f'<path transform="translate(50 82) rotate({a})" '
        f'd="M0 0 C4.6 -{n * .3:.0f} 4.2 -{n * .72:.0f} 0 -{n} C-4.2 -{n * .72:.0f} -4.6 -{n * .3:.0f} 0 0Z"/>'
        for a, n in blades
    )
    stem_line = f'<path d="M50 82 L50 96" stroke="{stem or fill}" stroke-width="2.4" stroke-linecap="round"/>'
    return f'<g fill="{fill}">{paths}</g>{stem_line}'


def _uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


LEAF_PATTERN = _uri(
    '<svg xmlns="http://www.w3.org/2000/svg" width="260" height="260" viewBox="0 0 260 260">'
    f'<g transform="translate(18 10) rotate(-18 50 50) scale(.95)">{_leaf("rgba(31,122,63,.075)")}</g>'
    f'<g transform="translate(150 140) rotate(24 50 50) scale(.72)">{_leaf("rgba(31,122,63,.06)")}</g>'
    f'<g transform="translate(160 6) rotate(40 50 50) scale(.38)">{_leaf("rgba(224,178,60,.10)")}</g>'
    f'<g transform="translate(30 176) rotate(-40 50 50) scale(.42)">{_leaf("rgba(224,178,60,.09)")}</g>'
    "</svg>"
)
LEAF_GOLD = _uri(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{_leaf("#E0B23C")}</svg>')
LEAF_MINT = _uri(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{_leaf("#9FD8A8")}</svg>')

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "displaylogo": False,
}

CSS_TEMPLATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Righteous&family=JetBrains+Mono:wght@400;500;600&family=Nunito:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#E2ECD6; --surface:#FAFCF5; --surface-alt:#E3E7D6;
  --border:#BCCDAE; --border-soft:#DFE4D3;
  --field:#EEF1E4; --field-hover:#E6EBDA;
  --ink:#10241B; --title:#10241B; --subtitle:#34403A;
  --muted:#5F6B63; --faint:#929C93;
  --asphalt:#10241B; --asphalt-2:#1B3A2C;
  --yellow:#E0B23C; --yellow-bright:#F0C75E; --yellow-soft:#F3E3B5;
  --orange:#1F7A3F; --orange-bright:#3FAE5A; --orange-soft:#CFE8D2;
  --teal:#6E4F8F; --teal-bright:#8C6BB0; --teal-soft:#E6DDF0;
  --blue:#416B8A; --blue-soft:#DCE7EF;
  --display:'Righteous','Trebuchet MS',sans-serif;
  --sans:'Nunito',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'JetBrains Mono','SFMono-Regular',Menlo,monospace;
}

html, body, .stApp, [data-testid="stAppViewContainer"]{
  background-color:var(--bg) !important; color:var(--ink);
}
.stApp{
  background-image:
    radial-gradient(880px 430px at 0% -10%, rgba(217,169,58,.16), transparent 62%),
    radial-gradient(760px 430px at 100% -8%, rgba(47,143,91,.08), transparent 60%),
    repeating-linear-gradient(0deg, rgba(16,36,27,.018) 0 1px, transparent 1px 5px);
  background-attachment:fixed;
}
[data-testid="stHeader"]{ background:transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{
  visibility:hidden !important; height:0 !important;
}
.block-container{ padding-top:1.55rem; padding-bottom:3.6rem; max-width:1380px; }
[data-testid="stSidebar"]{ width:306px !important; }

h1,h2,h3,h4{ font-family:var(--display) !important; color:var(--title); letter-spacing:.01em; }
p,li,label,span,div,input,button,textarea,td,th{ font-family:var(--sans); }
a{ color:var(--teal); }

/* ---------------------------------------------------------------- sidebar --- */
[data-testid="stSidebar"]{
  background:#F6F7EF !important;
  border-right:1px solid var(--border);
}
[data-testid="stSidebar"] .block-container{ padding-top:.8rem; }
[data-testid="stSidebar"] hr{ border-color:var(--border-soft); margin:.85rem 0; }
[data-testid="stSidebarNav"] a{
  border-radius:8px !important; padding:7px 10px !important;
  transition:background .15s ease;
}
[data-testid="stSidebarNav"] a:hover{ background:var(--surface-alt) !important; }
[data-testid="stSidebarNav"] a[aria-current="page"]{
  background:linear-gradient(90deg, rgba(217,169,58,.28), rgba(217,169,58,.04)) !important;
  box-shadow:inset 3px 0 0 var(--asphalt);
}
[data-testid="stSidebarNav"] a[aria-current="page"] span{
  color:var(--asphalt) !important; font-weight:800 !important;
}
[data-testid="stSidebarNav"] span{ font-size:12.5px !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label{
  font-size:12px !important; color:var(--subtitle) !important;
}

.cs-side-label{
  font-family:var(--mono); font-size:9.5px; letter-spacing:.17em;
  text-transform:uppercase; color:var(--muted); font-weight:600;
  margin:2px 0 7px 2px;
}
.cs-side-note{ font-size:11.5px; color:#56625A; line-height:1.55; }
.cs-side-stat{
  display:flex; justify-content:space-between; gap:10px; font-size:11.5px;
  color:var(--subtitle); padding:5px 0; border-bottom:1px dashed var(--border);
}
.cs-side-stat b{ font-family:var(--mono); color:var(--asphalt); font-weight:600; }
.cs-side-plate{
  border:1px solid var(--border); background:var(--surface); border-radius:10px;
  padding:8px 10px; margin-top:8px;
  font-family:var(--mono); font-size:9px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--muted); line-height:1.55;
}
.cs-side-plate b{ color:var(--asphalt); }

/* ------------------------------------------------------------------- hero --- */
.cs-hero{
  position:relative; overflow:hidden; border-radius:20px;
  background:
    radial-gradient(520px 260px at 92% -20%, rgba(217,169,58,.18), transparent 68%),
    linear-gradient(118deg,#0B2018 0%,#12301F 54%,#1A3D2A 100%);
  color:#F7F5EA; padding:1.5rem 1.8rem 1.7rem;
  box-shadow:0 18px 38px -28px rgba(16,36,27,.72);
  margin-bottom:1.1rem;
}
.cs-hero::before{
  content:""; position:absolute; right:-50px; bottom:-120px; width:370px; height:370px;
  border-radius:50%; border:1px solid rgba(217,169,58,.14);
  box-shadow:0 0 0 28px rgba(217,169,58,.035), 0 0 0 56px rgba(217,169,58,.02);
  pointer-events:none;
}
.cs-hero::after{
  content:""; position:absolute; left:0; right:0; bottom:0; height:9px;
  background:conic-gradient(var(--yellow) 25%, #0B2018 0 50%, var(--yellow) 0 75%, #0B2018 0);
  background-size:18px 18px; opacity:.95;
}
.cs-hero-top{
  display:flex; justify-content:space-between; align-items:center;
  gap:12px; margin-bottom:13px; position:relative; z-index:1;
}
.cs-eyebrow{
  display:inline-flex; align-items:center; gap:8px;
  font-family:var(--mono); font-size:9.5px; letter-spacing:.17em;
  text-transform:uppercase; color:#F3E3B5;
  background:rgba(217,169,58,.12); border:1px solid rgba(217,169,58,.32);
  padding:5px 11px; border-radius:999px;
}
.cs-eyebrow .dot{ width:6px; height:6px; border-radius:50%; background:var(--yellow); }
.cs-hero-meta{
  font-family:var(--mono); font-size:9.5px; letter-spacing:.1em;
  color:#A9BBAF; text-transform:uppercase; white-space:nowrap;
}
.cs-hero-main{ display:flex; align-items:center; gap:18px; position:relative; z-index:1; }
.cs-hero-mark{
  flex:0 0 auto; width:64px; height:64px; border-radius:15px;
  display:grid; place-items:center;
  background:var(--yellow); border:1px solid rgba(255,255,255,.25);
  box-shadow:0 10px 24px -14px rgba(0,0,0,.8);
}
.cs-hero-mark svg, .cs-hero-mark img{ width:43px; height:43px; display:block; }
.cs-title{
  font-family:var(--display) !important; font-weight:400;
  font-size:clamp(2.35rem,4.6vw,4rem); line-height:.94;
  letter-spacing:.012em; text-transform:uppercase; margin:0 0 7px; color:#F7F5EA;
}
.cs-title em{ font-style:normal; color:var(--yellow); }
.cs-lede{
  margin:0; max-width:920px; color:#CFDCD3; font-size:13.5px; line-height:1.65;
}
.cs-hero-pills{ display:flex; flex-wrap:wrap; gap:7px; margin-top:14px; position:relative; z-index:1; }
.cs-hero-pill{
  font-family:var(--mono); font-size:10px; letter-spacing:.04em;
  color:#E6EEE8; background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.14); border-radius:999px; padding:4px 10px;
}
.cs-hero-pill b{ color:var(--yellow); font-weight:600; }

/* ------------------------------------------------------------------ cover --- */
.cs-cover{
  position:relative; display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);
  background:var(--surface); border:1px solid var(--border); border-radius:18px;
  overflow:hidden; margin-bottom:1.1rem; box-shadow:0 14px 30px -26px rgba(16,36,27,.55);
}
.cs-cover::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:6px;
  background:linear-gradient(180deg,var(--orange) 0%,var(--orange) 55%,var(--yellow) 55%,var(--yellow) 100%);
}
.cs-cover-text{ padding:1.6rem 1.8rem 1.5rem 2.2rem; }
.cs-cover.slim{ grid-template-columns:1fr; }
.cs-cover.slim .cs-cover-text{ padding:1.1rem 1.6rem 1.1rem 2rem; }
.cs-cover.slim .cs-cover-eyebrow{ margin-bottom:8px; }
.cs-cover.slim .cs-cover-title{ font-size:clamp(2rem,3.4vw,2.9rem); margin-bottom:6px; }
.cs-cover-eyebrow{
  display:flex; align-items:center; gap:10px; margin-bottom:14px;
  font-family:var(--mono); font-size:9.5px; letter-spacing:.2em; text-transform:uppercase; color:var(--muted);
}
.cs-cover-eyebrow::after{ content:""; flex:1; height:1px; background:var(--border); }
.cs-cover-title{
  font-family:var(--display) !important; font-weight:400; text-transform:uppercase;
  font-size:clamp(2.3rem,4.2vw,3.7rem); line-height:.95; letter-spacing:.01em;
  color:var(--asphalt); margin:0 0 12px;
}
.cs-cover-title em{
  font-style:normal; color:var(--orange);
  background:linear-gradient(transparent 68%, rgba(217,169,58,.45) 68%);
}
.cs-cover-lede{ margin:0; max-width:620px; color:var(--subtitle); font-size:13.5px; line-height:1.7; }
.cs-cover-stats{
  background:#12301F; color:#F7F5EA; padding:1.25rem 1.4rem 1rem;
  display:flex; flex-direction:column; justify-content:space-between; gap:12px;
}
.cs-cover-grid{ display:grid; grid-template-columns:1fr 1fr; }
.cs-cover-stat{ padding:10px 12px; border-bottom:1px solid rgba(255,255,255,.12); }
.cs-cover-stat:nth-child(odd){ border-right:1px solid rgba(255,255,255,.12); }
.cs-cover-stat:nth-last-child(-n+2){ border-bottom:none; }
.cs-cover-stat b{
  display:block; font-family:var(--display); font-weight:400; font-size:2.05rem; line-height:1;
  color:var(--yellow); letter-spacing:.01em;
}
.cs-cover-stat span{
  display:block; margin-top:5px; font-family:var(--mono); font-size:9.5px;
  letter-spacing:.12em; text-transform:uppercase; color:#B9C9BE;
}
.cs-cover-spark{ border-top:1px dashed rgba(255,255,255,.18); padding-top:8px; }
.cs-cover-spark-label{
  font-family:var(--mono); font-size:9px; letter-spacing:.16em; text-transform:uppercase; color:#B9C9BE;
}
.cs-cover-spark img{ width:100%; height:auto; max-height:96px; display:block; margin-top:4px; }
@media (max-width:900px){
  .cs-cover{ grid-template-columns:1fr; }
}

/* ------------------------------------------------------------------- kpis --- */
.cs-kpis{
  display:grid; grid-template-columns:repeat(var(--cols,6),minmax(0,1fr));
  gap:10px; margin:16px 0 2px;
}
@media (max-width:1220px){ .cs-kpis{ grid-template-columns:repeat(3,minmax(0,1fr)) !important; } }
@media (max-width:700px){ .cs-kpis{ grid-template-columns:repeat(2,minmax(0,1fr)) !important; } }
.cs-kpi{
  background:var(--surface); border:1px solid var(--border);
  border-radius:13px; padding:12px 14px 11px; position:relative; overflow:hidden;
  box-shadow:0 1px 2px rgba(16,36,27,.03), 0 14px 26px -28px rgba(16,36,27,.65);
}
.cs-kpi::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:4px;
  background:var(--accent,var(--yellow));
}
.cs-kpi::after{
  content:""; position:absolute; right:10px; top:9px; width:18px; height:5px;
  background:repeating-linear-gradient(135deg, var(--accent,var(--yellow)) 0 6px, transparent 6px 12px);
  background-size:6px 5px; opacity:.5;
}
.cs-kpi-label{
  font-family:var(--mono); font-size:8.8px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--muted); font-weight:500; margin-bottom:5px;
  padding-right:18px;
}
.cs-kpi-value{
  font-family:var(--display); font-size:clamp(28px,2.8vw,40px);
  font-weight:400; color:var(--asphalt); line-height:.96; letter-spacing:.015em;
}
.cs-kpi-value small{ font-family:var(--sans); font-size:11px; color:var(--muted); font-weight:600; margin-left:3px; }
.cs-kpi-sub{ font-size:10.5px; color:var(--muted); margin-top:6px; line-height:1.45; }

/* ---------------------------------------------------------------- section --- */
.cs-section{ margin:26px 0 8px; }
.cs-kicker{
  font-family:var(--mono); font-size:9.5px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--orange); font-weight:600; margin-bottom:3px;
}
.cs-section h3{
  font-family:var(--display) !important; font-size:30px; font-weight:400;
  margin:0 0 3px; color:var(--title); letter-spacing:.025em; text-transform:uppercase;
}
.cs-section p{ font-size:13px; color:var(--subtitle); margin:0; max-width:950px; line-height:1.6; }

/* --------------------------------------------------------------- briefing --- */
.cs-brief{ margin:6px 0 2px; }
.cs-brief-item{
  display:grid; grid-template-columns:52px minmax(0,1fr); gap:16px;
  padding:17px 0 18px; border-bottom:1px dashed var(--border); position:relative;
}
.cs-brief-item:first-child{ border-top:1px dashed var(--border); }
.cs-brief-item::before{
  content:""; position:absolute; left:0; top:18px; bottom:18px; width:3px;
  background:var(--accent,var(--yellow)); border-radius:2px;
}
.cs-brief-index{
  font-family:var(--display); font-size:30px; line-height:1; color:var(--faint);
  padding-left:11px; letter-spacing:.02em;
}
.cs-brief-body{ min-width:0; }
.cs-brief-meta{ display:flex; flex-wrap:wrap; align-items:center; gap:9px; margin-bottom:3px; }
.cs-brief-tag{
  font-family:var(--mono); font-size:8.8px; letter-spacing:.15em; text-transform:uppercase;
  color:var(--orange); font-weight:600;
}
.cs-brief-stat{
  font-family:var(--display); font-size:31px; font-weight:400; color:var(--asphalt);
  line-height:1; letter-spacing:.015em;
}
.cs-brief-stat small{ font-family:var(--sans); font-size:11px; color:var(--muted); font-weight:600; margin-left:2px; }
.cs-brief-title{
  font-size:13px; color:var(--asphalt); font-weight:800; margin:3px 0 3px; line-height:1.4;
}
.cs-brief-copy{ font-size:12px; color:var(--subtitle); margin:0; line-height:1.62; max-width:980px; }
@media (max-width:700px){
  .cs-brief-item{ grid-template-columns:38px minmax(0,1fr); gap:10px; }
  .cs-brief-index{ font-size:24px; padding-left:8px; }
}

/* ------------------------------------------------------------------ cards --- */
.cs-card{
  background:var(--surface); border:1px solid var(--border); border-radius:14px;
  padding:15px 17px; box-shadow:0 1px 2px rgba(16,36,27,.03);
}
.cs-card h4{
  font-family:var(--display) !important; font-size:23px; font-weight:400;
  margin:0 0 2px; color:var(--asphalt); letter-spacing:.03em; text-transform:uppercase;
}
.cs-card p{ font-size:12px; color:var(--muted); margin:0; line-height:1.55; }

/* ------------------------------------------------------------------ table --- */
.cs-table{ width:100%; border-collapse:collapse; font-size:12.5px; }
.cs-table thead th{
  font-family:var(--mono); font-size:8.8px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--muted); text-align:left; font-weight:600; padding:7px 9px;
  border-bottom:1px solid var(--border);
}
.cs-table tbody td{
  padding:9px 9px; border-bottom:1px dashed var(--border-soft); color:var(--subtitle);
  vertical-align:middle;
}
.cs-table tbody tr:last-child td{ border-bottom:none; }
.cs-table tbody tr:hover{ background:#F4F6EC; }
.cs-table .num{ text-align:right; font-family:var(--mono); color:var(--asphalt); }
.cs-table .name{ font-weight:700; color:var(--asphalt); }
.cs-table .subtle{ font-size:11px; color:var(--muted); }

.cs-chip{
  display:inline-block; font-family:var(--mono); font-size:8.8px; letter-spacing:.08em;
  text-transform:uppercase; padding:3px 8px; border-radius:999px; font-weight:600;
  white-space:nowrap;
}
.cs-chip.yellow{ background:var(--yellow-soft); color:#6B5113; }
.cs-chip.orange{ background:var(--orange-soft); color:#1E5C3A; }
.cs-chip.teal{ background:var(--teal-soft); color:#4A3266; }
.cs-chip.dark{ background:var(--asphalt); color:#F7F5EA; }
.cs-chip.info{ background:var(--blue-soft); color:#274A6B; }

/* ------------------------------------------------------------------ meter --- */
.cs-meter{
  position:relative; overflow:hidden; border-radius:18px;
  background:
    radial-gradient(420px 220px at 100% 0%, rgba(217,169,58,.18), transparent 65%),
    linear-gradient(118deg,#0B2018,#143524 60%,#1D4630);
  color:#F7F5EA; padding:1.45rem 1.55rem 1.6rem;
  box-shadow:0 18px 34px -24px rgba(16,36,27,.72);
}
.cs-meter::after{
  content:""; position:absolute; left:0; right:0; bottom:0; height:8px;
  background:conic-gradient(var(--yellow) 25%, #0B2018 0 50%, var(--yellow) 0 75%, #0B2018 0);
  background-size:16px 16px;
}
.cs-meter .plate{
  display:inline-block; font-family:var(--mono); font-size:8.5px; letter-spacing:.15em;
  text-transform:uppercase; color:#F3E3B5; border:1px solid rgba(217,169,58,.35);
  background:rgba(217,169,58,.10); border-radius:4px; padding:3px 7px;
}
.cs-meter .kicker{
  font-family:var(--mono); font-size:9px; letter-spacing:.16em; text-transform:uppercase;
  color:#A9BBAF; margin-top:12px;
}
.cs-meter .fare{
  font-family:var(--display); font-size:clamp(56px,7vw,82px); line-height:.88;
  letter-spacing:.02em; color:var(--yellow); margin:2px 0 4px;
}
.cs-meter .range{ font-size:12.5px; color:#D5E2D9; }
.cs-meter .range b{ color:#F7F5EA; }
.cs-meter .route{
  margin:14px 0 10px; height:10px; border-radius:999px;
  background:linear-gradient(90deg,var(--yellow),var(--orange));
  position:relative;
}
.cs-meter .route::before, .cs-meter .route::after{
  content:""; position:absolute; top:50%; width:12px; height:12px; border-radius:50%;
  background:#F7F5EA; border:3px solid #10241B; transform:translateY(-50%);
}
.cs-meter .route::before{ left:-2px; }
.cs-meter .route::after{ right:-2px; }
.cs-meter .meta{
  display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px;
  margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,.16);
}
.cs-meter .meta div span{
  display:block; font-family:var(--mono); font-size:8.5px; letter-spacing:.1em;
  text-transform:uppercase; color:#A3B8AA; margin-bottom:3px;
}
.cs-meter .meta div b{ font-size:13px; color:#F7F5EA; font-weight:700; }
.cs-meter .fine{ font-size:10.5px; color:#A3B8AA; line-height:1.5; margin-top:10px; }

/* ------------------------------------------------------------------ note --- */
.cs-mono{ font-family:var(--mono); font-size:11px; color:var(--muted); }
.cs-empty{
  border:1px dashed var(--border); border-radius:16px; padding:2.2rem 1.5rem;
  text-align:center; background:rgba(252,252,246,.55);
}
.cs-empty .mark{ font-family:var(--display); font-size:40px; color:var(--yellow); line-height:1; }
.cs-empty h4{ margin:.3rem 0 .2rem; font-size:25px; font-weight:400; }
.cs-empty p{ margin:0 auto; max-width:360px; font-size:12px; color:var(--muted); line-height:1.55; }

/* --------------------------------------------------------------- streamlit --- */
div[data-testid="stVerticalBlockBorderWrapper"]{
  background:var(--surface); border-radius:14px;
}
[data-testid="stMetric"]{
  background:var(--surface); border:1px solid var(--border); border-radius:12px;
  padding:10px 12px;
}
[data-testid="stMetricLabel"] p{ font-size:11px !important; color:var(--muted) !important; }
[data-testid="stMetricValue"]{ font-family:var(--display) !important; color:var(--asphalt) !important; }

.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button{
  border-radius:8px !important; font-weight:700 !important;
  border:1px solid var(--border) !important;
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"]{
  background:var(--asphalt) !important;
  border:1px solid var(--asphalt) !important; color:var(--yellow) !important;
  box-shadow:0 8px 18px -12px rgba(16,36,27,.7);
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover{
  background:var(--yellow) !important; color:var(--asphalt) !important;
  border-color:var(--yellow) !important;
}
[data-baseweb="tab-list"]{
  gap:4px; background:var(--surface-alt); padding:4px; border-radius:9px;
  border:1px solid var(--border);
}
[data-baseweb="tab"]{
  border-radius:6px !important; padding:7px 14px !important;
  font-size:12px !important; color:var(--muted) !important;
}
[data-baseweb="tab"][aria-selected="true"]{
  background:var(--surface) !important; color:var(--asphalt) !important;
  box-shadow:0 1px 3px rgba(16,36,27,.10);
}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"]{ display:none; }

[data-testid="stExpander"]{
  background:var(--surface); border:1px solid var(--border) !important;
  border-radius:11px !important;
}
[data-testid="stDataFrame"]{
  border:1px solid var(--border); border-radius:10px; overflow:hidden;
}
[data-testid="stAlert"]{ border-radius:10px; }
[data-testid="stForm"]{
  background:var(--surface); border:1px solid var(--border); border-radius:14px;
}
/* Dropdown fields sit on a warmer shade so they read as editable controls. */
[data-testid="stForm"] [data-testid="stSelectbox"] [role="group"],
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div{
  background:var(--field) !important;
  border-color:var(--border) !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.55);
  transition:background .12s ease, border-color .12s ease;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [role="group"]:hover,
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover{
  background:var(--field-hover) !important;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [role="group"]:focus-within,
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within{
  background:var(--field-hover) !important;
  border-color:var(--asphalt) !important;
}

.cs-footer{
  margin-top:34px; padding-top:13px; border-top:1px solid var(--border);
  display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;
  font-family:var(--mono); font-size:9px; letter-spacing:.08em;
  text-transform:uppercase; color:var(--faint);
}

/* ------------------------------------------------------------- plotly maps --- */
[data-testid="stPlotlyChart"] .maplibregl-control-container{
  position:absolute !important;
  inset:0 !important;
  width:100% !important;
  height:100% !important;
  pointer-events:none;
}
[data-testid="stPlotlyChart"] .maplibregl-ctrl-bottom-right{
  position:absolute !important;
  right:6px !important;
  bottom:6px !important;
}
[data-testid="stPlotlyChart"] .maplibregl-ctrl{
  pointer-events:auto;
}
[data-testid="stPlotlyChart"] .maplibregl-ctrl-attrib{
  background:rgba(252,252,246,.92) !important;
  border-radius:4px;
}
[data-testid="stPlotlyChart"] .maplibregl-ctrl-attrib summary{
  display:none !important;
}
[data-testid="stPlotlyChart"] .maplibregl-ctrl-attrib a{
  font-family:var(--mono) !important;
  font-size:9px !important;
  color:var(--muted) !important;
}

/* -------------------------------------------------------------- responsive --- */
@media (max-width:1100px){
  [data-testid="stHorizontalBlock"]{ flex-wrap:wrap !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]{
    flex:1 1 100% !important; width:100% !important; min-width:100% !important;
  }
}
@media (max-width:640px){
  .cs-hero{ padding:1.2rem 1.2rem 1.45rem; }
  .cs-hero-main{ gap:12px; align-items:flex-start; }
  .cs-hero-mark{ width:48px; height:48px; }
  .cs-hero-mark svg, .cs-hero-mark img{ width:32px; height:32px; }
  .cs-hero-meta{ display:none; }
  .cs-title{ font-size:2.1rem; }
}

/* ------------------------------------------------------------ weed skin --- */
.stApp{
  background-image:
    radial-gradient(900px 460px at 0% -10%, rgba(224,178,60,.16), transparent 62%),
    radial-gradient(800px 460px at 100% -8%, rgba(31,122,63,.14), transparent 60%),
    url("__LEAF_PATTERN__") !important;
  background-size:auto, auto, 260px 260px !important;
  background-attachment:fixed !important;
}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0E2A19 0%,#123722 60%,#0E2A19 100%) !important;
  border-right:1px solid #0A1F12 !important;
}
[data-testid="stSidebar"]::before{
  content:""; position:absolute; inset:0; pointer-events:none; opacity:.55;
  background:url("__LEAF_PATTERN__"); background-size:200px 200px;
  filter:brightness(2.2) saturate(.6);
}
[data-testid="stSidebarNav"] span, [data-testid="stSidebarNav"] a{ color:#D6E9D2 !important; }
[data-testid="stSidebarNav"] a:hover{ background:rgba(255,255,255,.07) !important; }
[data-testid="stSidebarNav"] a[aria-current="page"]{
  background:linear-gradient(90deg, rgba(224,178,60,.32), rgba(224,178,60,.06)) !important;
  box-shadow:inset 3px 0 0 var(--yellow) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span{ color:#FFF3CF !important; }
[data-testid="stSidebar"] hr{ border-color:rgba(255,255,255,.14) !important; }
[data-testid="stSidebar"] .cs-side-label{ color:#9FD8A8; }
[data-testid="stSidebar"] .cs-side-stat{ color:#C9DEC6; border-bottom-color:rgba(255,255,255,.14); }
[data-testid="stSidebar"] .cs-side-stat b{ color:#F3D98A; }
[data-testid="stSidebar"] .cs-side-plate{
  background:rgba(255,255,255,.06); border-color:rgba(255,255,255,.16); color:#A9C4A8;
}
[data-testid="stSidebar"] .cs-side-plate b{ color:#F3D98A; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{
  color:#D6E9D2 !important; font-weight:700 !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{ color:#A9C4A8 !important; }

[data-testid="stSidebar"] button[data-variant="pills"]{
  background:rgba(255,255,255,.04) !important; border:1px solid rgba(214,233,210,.28) !important;
  color:#A9C4A8 !important;
}
[data-testid="stSidebar"] button[data-variant="pills"] p{ color:#A9C4A8 !important; }
[data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="true"]{
  background:var(--yellow) !important; border:1px solid var(--yellow) !important; color:#0E2A19 !important;
}
[data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="true"] p{ color:#0E2A19 !important; font-weight:800 !important; }

/* KPI tiles: dark leaf cards */
.cs-kpis{ gap:12px; }
.cs-kpi{
  background:
    radial-gradient(160px 90px at 100% 0%, rgba(224,178,60,.18), transparent 70%),
    linear-gradient(150deg,#123B24 0%,#0D2B1A 100%);
  border:1px solid rgba(159,216,168,.22); border-radius:20px;
  padding:14px 16px 13px; color:#EAF5E4;
  box-shadow:0 18px 30px -24px rgba(9,30,17,.9);
}
.cs-kpi::before{
  left:16px; right:16px; top:0; bottom:auto; width:auto; height:3px;
  border-radius:0 0 4px 4px; background:var(--accent,var(--yellow));
}
.cs-kpi::after{
  right:-14px; top:auto; bottom:-16px; width:78px; height:78px;
  background:url("__LEAF_GOLD__") no-repeat center/contain; opacity:.13;
  transform:rotate(-22deg);
}
.cs-kpi-label{ color:#9FD8A8; font-weight:600; padding-right:0; }
.cs-kpi-label::before{
  content:""; display:inline-block; width:11px; height:11px; margin-right:6px; vertical-align:-1px;
  background:url("__LEAF_MINT__") no-repeat center/contain;
}
.cs-kpi-value{ color:#FFF3CF; font-size:clamp(21px,2vw,29px); line-height:1.05; letter-spacing:0; }
.cs-kpi-sub{ color:#B5CDB1; position:relative; z-index:1; }

/* type scale for Righteous */
.cs-title{ font-size:clamp(1.9rem,3.6vw,3.1rem) !important; letter-spacing:0 !important; line-height:1.02 !important; }
.cs-cover-title{ letter-spacing:0 !important; line-height:1.05 !important; }
.cs-cover.slim .cs-cover-title{ font-size:clamp(1.7rem,2.9vw,2.5rem) !important; }
.cs-section h3{ font-size:23px !important; letter-spacing:.01em !important; }
.cs-cover::after{
  content:""; position:absolute; right:22px; top:50%; width:96px; height:96px; transform:translateY(-50%) rotate(14deg);
  background:url("__LEAF_GOLD__") no-repeat center/contain; opacity:.22; pointer-events:none;
}
.cs-cover{ background:rgba(250,252,245,.92); }
</style>
"""


CSS = (CSS_TEMPLATE.replace("__LEAF_PATTERN__", LEAF_PATTERN)
       .replace("__LEAF_GOLD__", LEAF_GOLD).replace("__LEAF_MINT__", LEAF_MINT))


def inject() -> None:
    st.html(CSS)


_SVG_OPEN = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" '
    'stroke="#10241B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
)
_ICON_SVGS = {
    "dashboard": _SVG_OPEN
    + '<path d="M32 54V30"/>'
    '<path d="M32 30c-3-9-3-16 0-22 3 6 3 13 0 22z"/>'
    '<path d="M32 34c-7-6-13-8-20-8 3 7 10 10 20 8z"/>'
    '<path d="M32 34c7-6 13-8 20-8-3 7-10 10-20 8z"/>'
    '<path d="M32 42c-6-1-11 1-15 5 6 2 11 0 15-5zM32 42c6-1 11 1 15 5-6 2-11 0-15-5z"/>'
    "</svg>",
    "trends": _SVG_OPEN
    + '<path d="M10 52h44"/><path d="M14 44l11-12 9 7 16-20"/><path d="M42 19h8v8"/></svg>',
    "calendar": _SVG_OPEN
    + '<rect x="10" y="14" width="44" height="38" rx="4"/><path d="M10 25h44M22 9v9M42 9v9"/>'
    '<path d="M19 34h6M29 34h6M39 34h6M19 43h6M29 43h6"/></svg>',
    "model": _SVG_OPEN
    + '<rect x="17" y="17" width="30" height="30" rx="3"/>'
    '<path d="M25 9v8M39 9v8M25 47v8M39 47v8M9 25h8M9 39h8M47 25h8M47 39h8"/>'
    '<path d="M27 27h10v10H27z"/></svg>',
    "forecast": _SVG_OPEN
    + '<path d="M10 50h44"/><path d="M14 42l10-9 8 5 8-10"/>'
    '<path d="M40 28l12-8" stroke-dasharray="3 5"/><circle cx="52" cy="20" r="3"/></svg>',
    "insights": _SVG_OPEN
    + '<path d="M24 43h16"/>'
    '<path d="M26 37c-4-3.4-6-8-6-12.5A12 12 0 0 1 44 24.5c0 4.5-2 9.1-6 12.5"/>'
    '<path d="M27 43v5h10v-5M29 54h6"/></svg>',
}


def header(
    title: str,
    lede: str,
    *,
    eyebrow: str = "CANNABIS RETAIL · DAILY GROSS SALES · 2021–2024",
    meta: str = "1,461 DAYS · 3 CATEGORIES · RIDGE FORECAST",
    pills: list[str] | None = None,
    icon: str = "dashboard",
) -> None:
    inject()
    pill_html = "".join(f'<span class="cs-hero-pill">{p}</span>' for p in (pills or []))
    icon_svg = _ICON_SVGS.get(icon, _ICON_SVGS["dashboard"])
    icon_uri = "data:image/svg+xml;base64," + base64.b64encode(
        icon_svg.encode("utf-8")
    ).decode("ascii")
    st.html(
        f"""
        <div class="cs-hero">
          <div class="cs-hero-top">
            <span class="cs-eyebrow"><span class="dot"></span>{html.escape(eyebrow)}</span>
            <span class="cs-hero-meta">{html.escape(meta)}</span>
          </div>
          <div class="cs-hero-main">
            <div class="cs-hero-mark">
              <img src="{icon_uri}" alt="" aria-hidden="true" />
            </div>
            <div>
              <h1 class="cs-title">{title}</h1>
              <p class="cs-lede">{lede}</p>
            </div>
          </div>
          <div class="cs-hero-pills">{pill_html}</div>
        </div>
        """
    )


def cover(title: str, lede: str, stats: list[tuple[str, str]] | None = None,
          trend: list[tuple[str, float]] | None = None,
          *, eyebrow: str = "CANNABIS RETAIL · DAILY GROSS SALES · 2021–2024",
          trend_label: str = "Gross sales by year") -> None:
    """Overview banner: headline, with an optional stat ledger and yearly trend line on the right."""
    inject()
    if not stats:
        st.html(
            f"""
            <div class="cs-cover slim">
              <div class="cs-cover-text">
                <div class="cs-cover-eyebrow">{html.escape(eyebrow)}</div>
                <h1 class="cs-cover-title">{title}</h1>
                <p class="cs-cover-lede">{lede}</p>
              </div>
            </div>
            """
        )
        return
    cells = "".join(f'<div class="cs-cover-stat"><b>{v}</b><span>{html.escape(k)}</span></div>' for v, k in stats)
    w, h, pad = 300, 74, 18
    vals = [v for _, v in trend]
    lo, hi = min(vals), max(vals)
    pts = [(pad + i * (w - 2 * pad) / max(len(vals) - 1, 1),
            12 + (h - 30) * (1 - (v - lo) / ((hi - lo) or 1))) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{pts[0][0]:.1f},{h - 16} " + line + f" {pts[-1][0]:.1f},{h - 16}"
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{YELLOW}"/>'
        f'<text x="{x:.1f}" y="{h - 3}" text-anchor="middle" font-size="9" fill="#B9C9BE" '
        f'font-family="IBM Plex Mono, monospace">{html.escape(lbl)}</text>'
        for (x, y), (lbl, _) in zip(pts, trend)
    )
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<polygon points="{area}" fill="rgba(217,169,58,.14)"/>'
           f'<polyline points="{line}" fill="none" stroke="{YELLOW}" stroke-width="2"/>{dots}</svg>')
    svg = ('<img alt="" aria-hidden="true" src="data:image/svg+xml;base64,'
           + base64.b64encode(svg.encode("utf-8")).decode("ascii") + '" />')
    st.html(
        f"""
        <div class="cs-cover">
          <div class="cs-cover-text">
            <div class="cs-cover-eyebrow">{html.escape(eyebrow)}</div>
            <h1 class="cs-cover-title">{title}</h1>
            <p class="cs-cover-lede">{lede}</p>
          </div>
          <div class="cs-cover-stats">
            <div class="cs-cover-grid">{cells}</div>
            <div class="cs-cover-spark">
              <div class="cs-cover-spark-label">{html.escape(trend_label)}</div>
              {svg}
            </div>
          </div>
        </div>
        """
    )


def section(title: str, description: str = "", kicker: str = "") -> None:
    st.html(
        f"""
        <div class="cs-section">
          <div class="cs-kicker">{html.escape(kicker)}</div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
        """
    )


def kpis(items: list[dict], columns: int | None = None) -> None:
    cols = columns or len(items)
    cards = []
    for item in items:
        accent = item.get("accent", YELLOW)
        cards.append(
            f"""
            <div class="cs-kpi" style="--accent:{accent}">
              <div class="cs-kpi-label">{html.escape(str(item['label']))}</div>
              <div class="cs-kpi-value">{item['value']}</div>
              <div class="cs-kpi-sub">{item.get('sub', '')}</div>
            </div>
            """
        )
    st.html(f'<div class="cs-kpis" style="--cols:{cols}">' + "".join(cards) + "</div>")


def chips(items: list[tuple[str, str]]) -> str:
    return "".join(
        f'<span class="cs-chip {tone}">{html.escape(text)}</span>' for text, tone in items
    )


def briefing(items: list[dict]) -> None:
    rows = []
    for index, item in enumerate(items, start=1):
        accent = item.get("accent", YELLOW)
        rows.append(
            f"""
            <div class="cs-brief-item" style="--accent:{accent}">
              <div class="cs-brief-index">{index:02d}</div>
              <div class="cs-brief-body">
                <div class="cs-brief-meta">
                  <span class="cs-brief-tag">{html.escape(item['tag'])}</span>
                  <span class="cs-brief-stat">{item['stat']}</span>
                </div>
                <div class="cs-brief-title">{item['title']}</div>
                <p class="cs-brief-copy">{item['copy']}</p>
              </div>
            </div>
            """
        )
    st.html('<div class="cs-brief">' + "".join(rows) + "</div>")


def footer(text: str = "Cannabis Sales Forecast · daily gross sales · 2021–2024") -> None:
    st.html(
        f"""
        <div class="cs-footer">
          <span>{html.escape(text)}</span>
          <span>Ridge Regression · 14 features · holdout R² 0.900</span>
        </div>
        """
    )


def forecast_card(
    value: float,
    low: float,
    high: float,
    date_label: str,
    vs_typical: float,
    vs_yesterday: float | None,
    season: str,
    day_type: str,
) -> None:
    st.html(
        f"""
        <div class="cs-meter">
          <span class="plate">FORECAST · DAILY GROSS SALES</span>
          <div class="kicker">Ridge model forecast</div>
          <div class="fare">${value:,.0f}</div>
          <div class="range">Typical range <b>${low:,.0f}–${high:,.0f}</b> · model error ±$4,444 MAE</div>
          <div class="route"></div>
          <div class="meta">
            <div><span>Date</span><b>{html.escape(date_label)}</b></div>
            <div><span>vs typical day</span><b>{vs_typical:+.1%}</b></div>
            <div><span>vs yesterday</span><b>{'—' if vs_yesterday is None else f'{vs_yesterday:+.1%}'}</b></div>
          </div>
          <div class="meta" style="margin-top:10px;padding-top:10px;">
            <div><span>Season</span><b>{html.escape(season)}</b></div>
            <div><span>Day type</span><b>{html.escape(day_type)}</b></div>
            <div><span>Model</span><b>Ridge α=1.0</b></div>
          </div>
          <div class="fine">Typical day = notebook mean of $201,703. The range is the 10th–90th percentile of holdout residuals. This is a model estimate, not a guarantee.</div>
        </div>
        """
    )


def empty_state() -> None:
    st.html(
        """
        <div class="cs-empty">
          <div class="mark">$ ---,---</div>
          <h4>Your forecast is waiting</h4>
          <p>Pick a date and enter recent sales. The saved Ridge model from the notebook will forecast that day's gross sales.</p>
        </div>
        """
    )


def side_snapshot(fig: dict) -> None:
    """Sidebar dataset card shared by every page."""
    total = sum(fig["yearly_sales"].values())
    ridge = next(m for m in fig["models"] if m["model"] == "Ridge Regression")
    with st.sidebar:
        st.html('<div class="cs-side-label">Snapshot</div>')
        st.html(
            f"""
        <div class="cs-side-stat"><span>Days of sales</span><b>{fig['raw_rows']:,}</b></div>
        <div class="cs-side-stat"><span>Gross sales</span><b>${total / 1e6:.1f}M</b></div>
        <div class="cs-side-stat"><span>Avg day</span><b>${fig['describe_gross_sales']['mean']:,.0f}</b></div>
        <div class="cs-side-stat"><span>Ridge R²</span><b>{ridge['r2']:.3f}</b></div>
        <div class="cs-side-stat"><span>Holdout days</span><b>{fig['split']['test']:,}</b></div>
        <div class="cs-side-plate">
          <b>Cannabis Sales.ipynb</b> · 2021–2024<br>
          Figures as printed in the notebook
        </div>
        """
        )


def chart(fig, box_height: int | None = None) -> None:
    """Plotly chart inside a bordered card, sized like the taxi dashboard."""
    height = box_height or int(fig.layout.height or 330) + 48
    with st.container(border=True, height=height):
        st.plotly_chart(fig, config=PLOTLY_CONFIG, use_container_width=True)


def note(text: str) -> None:
    st.html(f'<div class="cs-side-plate" style="margin:4px 0 10px">{text}</div>')


def table(df, formats: dict, where=None, **kwargs) -> None:
    """Dataframe with simple string formats, without needing jinja2."""
    import pandas as pd

    out = df.copy()
    for col, fmt in formats.items():
        out[col] = out[col].map(lambda v, f=fmt: "—" if pd.isna(v) else f.format(v))
    (where or st).dataframe(out, hide_index=True, use_container_width=True, **kwargs)
