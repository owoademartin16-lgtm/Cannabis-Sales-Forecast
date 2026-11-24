"""Visual system for the cannabis sales intelligence dashboard.

Forest green, harvest gold and a soft sage paper, with the same chart and
spacing discipline as the NYC taxi dashboard.
"""

from __future__ import annotations

import base64
import html

import streamlit as st

# ------------------------------------------------------------------ palette ---
BG = "#F1F0E6"
SURFACE = "#FCFCF6"
SURFACE_ALT = "#E3E7D6"
BORDER = "#C9D0B8"
BORDER_SOFT = "#DFE4D3"

INK = "#10241B"
ASPHALT = "#10241B"
ASPHALT_2 = "#1B3A2C"
TITLE = "#10241B"
SUBTITLE = "#34403A"
MUTED = "#5F6B63"
FAINT = "#929C93"

YELLOW = "#D9A93A"
YELLOW_BRIGHT = "#F0C75E"
YELLOW_SOFT = "#F3E3B5"
ORANGE = "#2F8F5B"
ORANGE_BRIGHT = "#3DB374"
ORANGE_SOFT = "#D3ECDD"
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

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "displaylogo": False,
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#F1F0E6; --surface:#FCFCF6; --surface-alt:#E3E7D6;
  --border:#C9D0B8; --border-soft:#DFE4D3;
  --field:#EEF1E4; --field-hover:#E6EBDA;
  --ink:#10241B; --title:#10241B; --subtitle:#34403A;
  --muted:#5F6B63; --faint:#929C93;
  --asphalt:#10241B; --asphalt-2:#1B3A2C;
  --yellow:#D9A93A; --yellow-bright:#F0C75E; --yellow-soft:#F3E3B5;
  --orange:#2F8F5B; --orange-bright:#3DB374; --orange-soft:#D3ECDD;
  --teal:#6E4F8F; --teal-bright:#8C6BB0; --teal-soft:#E6DDF0;
  --blue:#416B8A; --blue-soft:#DCE7EF;
  --display:'Bebas Neue',Impact,sans-serif;
  --sans:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'IBM Plex Mono','SFMono-Regular',Menlo,monospace;
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
</style>
"""


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
