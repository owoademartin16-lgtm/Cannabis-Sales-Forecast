"""Insights — what the notebook found, in plain language."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils import analysis as an  # noqa: E402
from utils import charts, data_loader, theme  # noqa: E402

fig = data_loader.load_figures()
yearly = data_loader.yearly()
cats = data_loader.categories()
corr = fig["correlations"]

theme.header(
    "What the numbers <em>say</em>.",
    "Seven takeaways from the notebook, each tied to a figure it printed.",
    icon="insights",
)

theme.briefing(
    [
        {"tag": "Growth", "stat": "$45.7M → $100.5M",
         "title": "Sales more than doubled in four years",
         "copy": "Yearly gross sales rose 39.9%, 28.3% and 22.5%. Growth is slowing in percentage terms but still adds "
                 "about $18M a year.", "accent": theme.ORANGE},
        {"tag": "Seasonality", "stat": "Feb 2021 · $2.58M",
         "title": "A seasonal wave on top of the trend",
         "copy": "Monthly totals rise and dip in a regular rhythm. The lowest month is February 2021 and the highest is "
                 "November 2024 at $9.16M.", "accent": theme.YELLOW},
        {"tag": "Calendar", "stat": f"r = {corr['IsWeekend']:.4f}",
         "title": "Weekends and month edges don't matter",
         "copy": "Day of week, weekend, month-start and month-end flags all correlate with sales at under 0.02. "
                 "Staffing doesn't need a weekend bump.", "accent": theme.TEAL},
        {"tag": "Products", "stat": f"Flower {cats.iloc[0]['share']:.1%}",
         "title": "Flower leads, but only just",
         "copy": "Flower brought in $103.1M, Concentrates $95.0M and Edibles $94.0M. Average days differ by under 3%, "
                 "so Flower leads mostly because it had more days.", "accent": theme.ORANGE},
        {"tag": "Signal", "stat": f"lag_1 r = {corr['lag_1']:.3f}",
         "title": "Recent sales are the best predictor",
         "copy": "Yesterday's sales (0.992) and the 7-day average (0.991) dominate. The saved model leans on "
                 "the 7-day average more than anything else.", "accent": theme.YELLOW},
        {"tag": "Models", "stat": "R² 0.900 vs −0.050",
         "title": "Linear models win; tree models fail",
         "copy": "Ridge and Linear Regression miss by about $4,444 a day. Tree models can't extrapolate past "
                 "training highs, so they under-forecast 2024.", "accent": theme.ORANGE},
        {"tag": "Caveat", "stat": "HTTP 404",
         "title": "The data is simulated",
         "copy": "The notebook's Massachusetts CCC download failed, so it used its built-in simulated series. "
                 "Re-run with real data before acting on these numbers.", "accent": theme.ASPHALT},
    ]
)

theme.section("Next steps", "", kicker="Recommendations")
st.markdown(
    "- **Swap in real data.** Point the notebook at a working Cannabis Control Commission export and retrain.\n"
    "- **Forecast more than one day.** Feed each forecast back in as the next day's lag to plan a week ahead.\n"
    "- **Fix the chart cell.** Replace the hard-coded R² list with the printed scores.\n"
    "- **Track model drift.** Re-score Ridge monthly; retrain if MAE rises well above $4,444."
)
theme.footer()
