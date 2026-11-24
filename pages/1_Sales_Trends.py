"""Sales Trends — daily, monthly, quarterly and yearly gross sales."""

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
years, sel_cats = data_loader.selection()
filtered = data_loader.is_filtered(years, sel_cats)
monthly = data_loader.filtered_monthly(years, sel_cats)
quarterly = data_loader.filtered_quarterly(years, sel_cats)
yearly = data_loader.filtered_yearly(years, sel_cats)
daily = data_loader.filtered_daily(years, sel_cats)

q4_share = quarterly[quarterly["quarter"].str.endswith("Q4")]["sales"].sum() / quarterly["sales"].sum()
span = int(yearly["year"].iloc[-1] - yearly["year"].iloc[0])
cagr = (yearly["sales"].iloc[-1] / yearly["sales"].iloc[0]) ** (1 / span) - 1 if span else None
best_q = quarterly.loc[quarterly["sales"].idxmax()]
low = monthly.loc[monthly["sales"].idxmin()]

theme.header(
    "A business that <em>doubled</em> in four years.",
    "Gross sales climbed every year, from $45.7M in 2021 to $100.5M in 2024, with a steady "
    "seasonal wave on top of the growth line.",
    pills=[
        f"<b>{'—' if cagr is None else f'{cagr:.1%}'}</b> compound annual growth",
        f"<b>{best_q['quarter']}</b> best quarter",
        f"<b>{q4_share:.1%}</b> of sales in Q4s",
    ],
    icon="trends",
)

theme.kpis(
    [
        {"label": f"{int(r.year)} sales", "value": an.money(r.sales, compact=True, digits=1),
         "sub": "no prior year in slice" if r.growth != r.growth else f"{r.growth:+.1%} year on year",
         "accent": charts.YEAR_COLORS[int(r.year)]}
        for r in yearly.itertuples()
    ]
    + [
        {"label": "Best quarter", "value": best_q["quarter"], "sub": an.money(best_q["sales"]), "accent": theme.YELLOW},
        {"label": "Lowest month", "value": f"{low['month']:%b %Y}", "sub": an.money(low["sales"], digits=2), "accent": theme.TEAL},
    ],
    columns=6,
)

theme.section(
    "Monthly totals",
    (f"{len(monthly)} monthly totals exactly as printed by the notebook's <code>monthly_sales</code> cell."
     if data_loader.all_cats(sel_cats) else
     f"{len(monthly)} monthly totals for {', '.join(sel_cats)}, summed from the reconstructed daily rows."),
    kicker=("Slice · " + data_loader.slice_label(years, sel_cats)) if filtered else "Notebook output",
)
theme.chart(charts.monthly_trend(monthly, height=340))

left, right = st.columns(2, gap="medium")
with left:
    theme.chart(charts.monthly_by_year(monthly, height=340))
with right:
    theme.chart(charts.quarterly_bars(quarterly, height=340))

theme.chart(charts.month_year_heatmap(monthly, height=300))

theme.section(
    "Daily detail",
    "Daily view with a 30-day average. The notebook printed only a few daily rows, so the other "
    "days come from its simulation recipe, rescaled so every monthly total and category figure above matches exactly.",
    kicker="Reconstructed daily series",
)
theme.chart(charts.daily_line(daily, height=360))

with st.expander("Monthly, quarterly and yearly tables"):
    c1, c2, c3 = st.columns([1.2, 1, 0.8])
    theme.table(
        monthly.assign(Month=monthly["month"].dt.strftime("%Y-%m"))[["Month", "sales"]]
        .rename(columns={"sales": "Gross sales"}),
        {"Gross sales": "${:,.2f}"}, where=c1, height=360,
    )
    theme.table(
        quarterly.rename(columns={"quarter": "Quarter", "sales": "Gross sales"}),
        {"Gross sales": "${:,.0f}"}, where=c2, height=360)
    theme.table(
        yearly.rename(columns={"year": "Year", "sales": "Gross sales", "growth": "Growth"}),
        {"Gross sales": "${:,.0f}", "Growth": "{:+.1%}"}, where=c3)

theme.footer()
