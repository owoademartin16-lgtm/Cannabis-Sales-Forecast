"""Calendar & Seasonality — day of week, month, Q4 and month-edge effects."""

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
daily = data_loader.filtered_daily(years, sel_cats)
cats = data_loader.filtered_categories(years, sel_cats)
corr = fig["correlations"]

model_days = daily[daily["date"] >= "2021-01-31"]
weekend = model_days[model_days["dow"] >= 5]["gross_sales"].mean()
weekday = model_days[model_days["dow"] < 5]["gross_sales"].mean()
q4 = model_days[model_days["month"] >= 10]["gross_sales"].mean()
rest = model_days[model_days["month"] < 10]["gross_sales"].mean()
start = model_days[model_days["day"] <= 3]["gross_sales"].mean()
end = model_days[model_days["day"] >= 28]["gross_sales"].mean()
mid = model_days[(model_days["day"] > 3) & (model_days["day"] < 28)]["gross_sales"].mean()

theme.header(
    "The calendar <em>barely</em> moves the needle.",
    "Weekends, month starts and month ends look almost the same as any other day. "
    "What matters is the long upward trend and the months-long seasonal wave.",
    pills=[
        f"<b>r = {corr['DayOfWeek']:.4f}</b> day of week",
        f"<b>r = {corr['IsWeekend']:.4f}</b> weekend flag",
        f"<b>r = {corr['is_q4']:.3f}</b> Q4 flag",
        f"<b>r = {corr['Month']:.3f}</b> month",
    ],
    icon="calendar",
)

theme.kpis(
    [
        {"label": "Weekend vs weekday", "value": an.pct(weekend / weekday - 1, signed=True),
         "sub": f"{an.money(weekend)} vs {an.money(weekday)}", "accent": theme.TEAL},
        {"label": "Q4 vs Jan–Sep", "value": an.pct(q4 / rest - 1, signed=True),
         "sub": f"{an.money(q4)} vs {an.money(rest)}", "accent": theme.YELLOW},
        {"label": "Month start (days 1–3)", "value": an.money(start), "sub": f"{start / mid - 1:+.1%} vs mid-month", "accent": theme.ORANGE},
        {"label": "Month end (day 28+)", "value": an.money(end), "sub": f"{end / mid - 1:+.1%} vs mid-month", "accent": theme.ORANGE},
        {"label": "Weekend correlation", "value": f"{corr['IsWeekend']:.4f}", "sub": "notebook correlation", "accent": theme.ASPHALT},
    ],
    columns=5,
)

left, right = st.columns(2, gap="medium")
with left:
    theme.chart(charts.dow_bars(model_days, height=330))
with right:
    theme.chart(charts.month_of_year(monthly, height=330))

theme.note(
    "Q4 is higher partly because it falls late in each year, so the growth trend lifts it. "
    "Sales grew all year round, so later months always sit higher than earlier ones."
)

left, mid_col, right = st.columns(3, gap="medium")
with left:
    theme.chart(charts.segment_bars(["Weekday", "Weekend"], [weekday, weekend], [theme.ORANGE, theme.TEAL],
                                    "Weekday vs weekend", height=300))
with mid_col:
    theme.chart(charts.segment_bars(["Jan–Sep", "Q4"], [rest, q4], [theme.ORANGE, theme.YELLOW],
                                    "Q4 vs the rest of the year", height=300))
with right:
    theme.chart(charts.segment_bars(["Days 1–3", "Days 4–27", "Day 28+"], [start, mid, end],
                                    [theme.ORANGE_BRIGHT, theme.ORANGE, theme.ORANGE_BRIGHT],
                                    "Month start · middle · end", height=300))

theme.section(
    "Product categories",
    "Category totals, averages and ranges as printed by the notebook. Each day was tagged with one random category.",
    kicker="Notebook output",
)
left, right = st.columns([0.85, 1.15], gap="medium")
with left:
    theme.chart(charts.category_range(cats, height=300))
with right:
    with st.container(border=True, height=348):
        theme.table(
        cats.rename(columns={"category": "Category", "sum": "Total", "mean": "Mean", "min": "Min",
                                 "max": "Max", "days": "Days", "share": "Share"})
            [["Category", "Total", "Share", "Days", "Mean", "Min", "Max"]],
        {"Total": "${:,.0f}", "Share": "{:.1%}", "Mean": "${:,.2f}", "Min": "${:,.2f}", "Max": "${:,.2f}"},
        )
        if filtered:
            st.caption(f"Slice: {data_loader.slice_label(years, sel_cats)}.")
        else:
            st.caption("Flower leads by about $8M, but its average day is only 2.6% above Concentrates.")

st.caption("Day-of-week, Q4 and month-edge averages use the reconstructed daily series (model rows, 31 Jan 2021 onward).")
theme.footer()
