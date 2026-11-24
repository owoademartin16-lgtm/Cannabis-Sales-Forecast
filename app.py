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
    fig = data_loader.load_figures()
    monthly = data_loader.monthly()
    yearly = data_loader.yearly()
    cats = data_loader.categories()
    models = data_loader.models()
    total = yearly["sales"].sum()
    growth = yearly["sales"].iloc[-1] / yearly["sales"].iloc[0] - 1
    peak = monthly.loc[monthly["sales"].idxmax()]
    desc = fig["describe_gross_sales"]

    theme.cover(
        "Four years of <em>retail cannabis</em>, day by day.",
        "Daily gross sales from January 2021 to December 2024: how fast the business grew, "
        "which products carried it, and how well a simple Ridge model forecasts tomorrow.",
        stats=[
            (an.money(total, compact=True, digits=1), "gross sales"),
            (f"{growth:+.0%}", "2024 vs 2021"),
            (an.money(desc["mean"]), "average model day"),
            ("0.900", "Ridge R² · unseen 2024"),
        ],
        trend=[(str(int(y)), float(v)) for y, v in zip(yearly["year"], yearly["sales"])],
    )

    theme.kpis(
        [
            {"label": "Gross sales", "value": an.money(total, compact=True, digits=1),
             "sub": f"{fig['raw_rows']:,} days · 2021–2024", "accent": theme.ORANGE},
            {"label": "2024 sales", "value": an.money(yearly['sales'].iloc[-1], compact=True, digits=1),
             "sub": f"{yearly['growth'].iloc[-1]:+.1%} vs 2023", "accent": theme.YELLOW},
            {"label": "Average day", "value": an.money(desc["mean"]),
             "sub": f"median {an.money(desc['p50'])} · {fig['model_rows']:,} model days", "accent": theme.ORANGE},
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

    theme.note(
        "<b>Data source.</b> Every total on this page is copied from the printed outputs of "
        "<i>Cannabis Sales.ipynb</i>. The notebook's Massachusetts CCC download returned HTTP 404, "
        "so its figures come from the notebook's built-in simulated sales series."
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
navigation.run()

with st.sidebar:
    st.divider()
    theme.side_snapshot(data_loader.load_figures())
