"""Sales Forecaster — live daily forecast from the saved Ridge model."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils import analysis as an  # noqa: E402
from utils import charts, data_loader, theme  # noqa: E402

import datetime as dt  # noqa: E402

import pandas as pd  # noqa: E402

model, features = data_loader.load_model()
daily = data_loader.load_daily()
recon = data_loader.load_reconstruction()

LAST_DATE = daily["date"].max().date()
FIRST_DATE = (daily["date"].min() + pd.Timedelta(days=30)).date()
FIELDS = ["lag_1", "lag_7", "lag_30", "rolling_7", "rolling_30"]

theme.header(
    "Forecast <em>tomorrow's</em> takings.",
    "Pick a date and enter recent sales. The Ridge model saved by the notebook turns them into a "
    "daily gross-sales forecast and shows which inputs drove it.",
    eyebrow="SAVED MODEL · cannabis_ridge_model.joblib",
    meta="RIDGE α=1.0 · 14 FEATURES · MAE $4,444",
    pills=["<b>Pick</b> a date", "<b>Load</b> recent sales or type your own", "<b>Forecast</b> the day"],
    icon="forecast",
)


def load_history(date: dt.date) -> None:
    values = an.recent_inputs(daily, date)
    for k in FIELDS:
        st.session_state[k] = round(values[k], 2)


if "lag_1" not in st.session_state:
    st.session_state["date"] = LAST_DATE + dt.timedelta(days=1)
    load_history(st.session_state["date"])

form_col, result_col = st.columns([0.9, 1.1], gap="large")
with form_col:
    with st.container(border=True):
        st.html('<div class="cs-kicker">Forecast inputs</div>')
        date = st.date_input("Date to forecast", key="date", min_value=FIRST_DATE,
                             max_value=dt.date(2026, 12, 31), format="YYYY-MM-DD")
        if st.button("Load recent sales from the data", icon=":material/history:", use_container_width=True):
            load_history(date)
            st.rerun()
        a, b = st.columns(2)
        a.number_input("Yesterday's sales", key="lag_1", min_value=0.0, step=1000.0, format="%.2f")
        b.number_input("Sales 7 days ago", key="lag_7", min_value=0.0, step=1000.0, format="%.2f")
        a.number_input("Sales 30 days ago", key="lag_30", min_value=0.0, step=1000.0, format="%.2f")
        b.number_input("7-day average", key="rolling_7", min_value=0.0, step=1000.0, format="%.2f")
        st.number_input("30-day average", key="rolling_30", min_value=0.0, step=1000.0, format="%.2f")
        st.caption("Averages cover the days before the forecast date, as in the notebook (shift 1, then rolling).")

row = an.feature_row(date, *(st.session_state[k] for k in FIELDS))
value = an.predict(model, features, row)
low = max(0.0, value + recon["residual_p10"])
high = value + recon["residual_p90"]

with result_col:
    theme.forecast_card(
        value, low, high, date.strftime("%a %d %b %Y"),
        value / an.TYPICAL_DAY - 1,
        value / st.session_state["lag_1"] - 1 if st.session_state["lag_1"] else 0.0,
        an.season(date.month),
        "Weekend" if date.weekday() >= 5 else "Weekday",
    )
    if date > LAST_DATE + dt.timedelta(days=1):
        st.warning("This date is past the end of the data (31 Dec 2024). Enter the recent sales yourself; "
                   "loaded values stop at the last day of data.", icon=":material/info:")

left, right = st.columns(2, gap="medium")
with left:
    contrib = an.contributions(model, features, row)
    theme.chart(charts.contribution_bars(contrib, float(model.intercept_), value, height=430))
with right:
    hist = daily[daily["date"] < pd.Timestamp(date)].tail(30)
    if hist.empty:
        hist = daily.head(30)
    theme.chart(charts.forecast_context(hist, date, value, low, high, height=430))

actual = daily.loc[daily["date"] == pd.Timestamp(date), "gross_sales"]
if not actual.empty:
    err = actual.iloc[0] - value
    st.info(f"Reconstructed actual for {date:%d %b %Y}: {an.money(actual.iloc[0])} · forecast miss {an.money(err)}.",
            icon=":material/fact_check:")

theme.footer()
