"""Cannabis sales intelligence — Streamlit dashboard.

Run with:

    python3 -m streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Cannabis Sales · Forecast Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils import analysis as an  # noqa: E402
from utils import charts, data_loader, theme  # noqa: E402

theme.inject()

try:
    st.logo(str(data_loader.ROOT / "assets" / "logo.svg"), size="large")
except Exception:
    pass


def overview() -> None:
    years, sel_cats = data_loader.selection()
    filtered = data_loader.is_filtered(years, sel_cats)
    fig = data_loader.load_figures()
    monthly = data_loader.filtered_monthly(years, sel_cats)
    yearly = data_loader.filtered_yearly(years, sel_cats)
    cats = data_loader.filtered_categories(years, sel_cats)
    daily = data_loader.filtered_daily(years, sel_cats)
    models = data_loader.models()
    total = monthly["sales"].sum()
    peak = monthly.loc[monthly["sales"].idxmax()]
    desc = fig["describe_gross_sales"]
    last = yearly.iloc[-1]
    if filtered:
        avg_value, avg_sub = an.money(daily["gross_sales"].mean()), (
            f"median {an.money(daily['gross_sales'].median())} · reconstructed days")
    else:
        avg_value, avg_sub = an.money(desc["mean"]), (
            f"median {an.money(desc['p50'])} · {fig['model_rows']:,} model days")

    theme.cover(
        "Four years of <em>retail cannabis</em>.",
        "Daily gross sales, 2021–2024, with a Ridge forecast.",
    )

    theme.kpis(
        [
            {"label": "Gross sales", "value": an.money(total, compact=True, digits=1),
             "sub": (f"{len(daily):,} days · {data_loader.slice_label(years, sel_cats)}" if filtered
                     else f"{fig['raw_rows']:,} days · 2021–2024"), "accent": theme.ORANGE},
            {"label": f"{int(last['year'])} sales", "value": an.money(last['sales'], compact=True, digits=1),
             "sub": ("no prior year in slice" if last["growth"] != last["growth"]
                     else f"{last['growth']:+.1%} vs {int(last['year']) - 1}"), "accent": theme.YELLOW},
            {"label": "Average day", "value": avg_value, "sub": avg_sub, "accent": theme.ORANGE},
            {"label": "Best month", "value": f"{peak['month']:%b %Y}",
             "sub": an.money(peak["sales"]), "accent": theme.YELLOW},
            {"label": "Top category", "value": cats.iloc[0]["category"],
             "sub": f"{an.money(cats.iloc[0]['sum'], compact=True, digits=1)} · {cats.iloc[0]['share']:.1%}",
             "accent": theme.TEAL},
            {"label": "Ridge MAE", "value": an.money(models.iloc[0]["mae"]),
             "sub": f"RMSE {an.money(models.iloc[0]['rmse'])} · R² {models.iloc[0]['r2']:.3f}",
             "accent": theme.ASPHALT},
        ],
        columns=6,
    )

    left, right = st.columns([1.35, 0.65], gap="medium")
    with left:
        theme.chart(charts.monthly_trend(monthly, height=340))
    with right:
        theme.chart(charts.category_donut(cats, height=340))

    left, right = st.columns(2, gap="medium")
    with left:
        theme.chart(charts.yearly_bars(yearly, height=330))
    with right:
        theme.chart(charts.model_metric(models, "r2", height=330))

    if filtered:
        st.caption(
            f"Slice: {data_loader.slice_label(years, sel_cats)}. Year-only slices use the notebook's exact "
            "monthly totals; category slices use the reconstructed daily rows, which add up to the notebook's totals."
        )
    theme.footer()


pages = [
    st.Page(overview, title="Overview", icon=":material/dashboard:", default=True),
    st.Page("pages/1_Sales_Trends.py", title="Sales Trends", icon=":material/trending_up:"),
    st.Page("pages/2_Calendar_and_Seasonality.py", title="Calendar & Seasonality", icon=":material/calendar_month:"),
    st.Page("pages/3_Model_Lab.py", title="Model Lab", icon=":material/model_training:"),
    st.Page("pages/4_Sales_Forecaster.py", title="Sales Forecaster", icon=":material/query_stats:"),
    st.Page("pages/5_Insights.py", title="Insights", icon=":material/lightbulb:"),
]

navigation = st.navigation(pages, position="sidebar")
if navigation.title in {"Overview", "Sales Trends", "Calendar & Seasonality"}:
    data_loader.slicers()
navigation.run()

with st.sidebar:
    st.divider()
    theme.side_snapshot(data_loader.load_figures())
