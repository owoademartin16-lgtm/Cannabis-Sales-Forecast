"""Cannabis Sales Forecaster — daily gross sales prediction.

Loads the pre-trained artifacts retrained exactly from "Cannabis Sales.ipynb":
  - cannabis_ridge_model.joblib  ({'model': Ridge(alpha=1.0), 'features': [...]})
    Features: Month, Day, Year, is_q4, is_month_start, is_month_end,
    DayOfWeek, IsWeekend, time_step, lag_1, lag_7, lag_30,
    rolling_mean_7, rolling_mean_30 (chronological 80/20 split:
    1,144 train rows, 287 test rows).

Pipeline (exactly as trained — never retrained here):
  Date + Recent Sales -> Calendar Features -> DataFrame in exact
  feature order -> Saved Ridge Model -> Predicted Gross Sales

Run with:
    streamlit run cannabis_sales_app.py
"""

import datetime

import joblib
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
MODEL_PATH = "cannabis_ridge_model.joblib"

# First date of the training series; time_step counts days since it.
SERIES_START_DATE = datetime.date(2021, 1, 1)

# Typical daily gross sales from training data (context only).
TYPICAL_DAY = 201700.0


@st.cache_resource
def load_assets():
    """Load model + feature list once; raises FileNotFoundError."""
    artifacts = joblib.load(MODEL_PATH)
    return artifacts["model"], list(artifacts["features"])


def build_input_df(selected_date, lag_1, lag_7, lag_30,
                    rolling_mean_7, rolling_mean_30, features):
    """One row in exact training column order; calendar parts are automatic."""
    weekday = selected_date.weekday()  # Monday=0
    row = {
        "Month": selected_date.month,
        "Day": selected_date.day,
        "Year": selected_date.year,
        "is_q4": 1 if selected_date.month in (10, 11, 12) else 0,
        "is_month_start": 1 if selected_date.day <= 3 else 0,
        "is_month_end": 1 if selected_date.day >= 28 else 0,
        "DayOfWeek": weekday,
        "IsWeekend": 1 if weekday >= 5 else 0,
        "time_step": max(0, (selected_date - SERIES_START_DATE).days),
        "lag_1": float(lag_1),
        "lag_7": float(lag_7),
        "lag_30": float(lag_30),
        "rolling_mean_7": float(rolling_mean_7),
        "rolling_mean_30": float(rolling_mean_30),
    }
    return pd.DataFrame([[row[f] for f in features]], columns=features)


def predict_sales(model, input_df):
    """Predict and floor at zero (sales can't be negative)."""
    return max(0.0, float(model.predict(input_df)[0]))


# Cannabis theme: deep-green hero, gold accents, soft result card.
THEME_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
.hero {
    background: linear-gradient(120deg, #052E16 0%, #166534 60%, #3DDC97 100%);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    color: #FFFFFF;
    box-shadow: 0 12px 32px rgba(5, 46, 22, 0.35);
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #FFFFFF !important;
    margin: 0 0 0.3rem !important;
    font-size: 2.4rem !important;
}
.hero p { color: #D9F2E6 !important; margin: 0; font-size: 1.05rem; }
.hero .gold-rule {
    width: 72px; height: 4px; border-radius: 4px;
    background: linear-gradient(90deg, #D4AF37, #F6E27A);
    margin-bottom: 0.9rem;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #166534, #3DDC97);
    border: none; color: #FFFFFF !important;
    font-weight: 800; font-size: 1.05rem;
    border-radius: 12px; padding: 0.7rem 1.4rem; width: 100%;
    box-shadow: 0 6px 18px rgba(22, 101, 52, 0.4);
}
div.stButton > button[kind="primary"]:hover {
    filter: brightness(1.08);
}
.sales-card {
    background: linear-gradient(120deg, #052E16, #15803D);
    border-radius: 16px; padding: 1.6rem 1.8rem; color: #FFFFFF;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.25);
    text-align: center; margin-bottom: 1rem;
}
.sales-card .label {
    font-size: 0.8rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: rgba(255, 255, 255, 0.85);
}
.sales-card .value { font-size: 2.6rem; font-weight: 800; margin: 0.1rem 0; }
.sales-card .context { color: #D9F2E6; }
</style>
"""

WEEKDAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]


# ------------------------------------------------------------------
# App
# ------------------------------------------------------------------
def main():
    try:
        model, features = load_assets()
    except FileNotFoundError as err:
        st.error(
            "Model file not found. Make sure 'cannabis_ridge_model.joblib' "
            f"is in the same folder as this script. (Details: {err})"
        )
        st.stop()
    except Exception:
        st.error("Could not load the model file. Check it is valid and try again.")
        st.stop()

    st.set_page_config(
        page_title="Cannabis Sales Forecaster",
        page_icon="🌿",
        layout="wide",
    )

    # ---- Header ----
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="hero"><div class="gold-rule"></div>'
        '<div style="display:flex;align-items:center;gap:0.9rem;">'
        '<svg width="52" height="52" viewBox="0 0 64 64" fill="none">'
        "<defs><linearGradient id='gold' x1='0' y1='0' x2='1' y2='1'>"
        "<stop offset='0' stop-color='#F6E27A'/>"
        "<stop offset='1' stop-color='#D4AF37'/></linearGradient></defs>"
        "<rect x='10' y='44' width='44' height='6' rx='3' fill='url(#gold)'/>"
        "<rect x='14' y='30' width='8' height='14' rx='2' fill='url(#gold)'/>"
        "<rect x='28' y='22' width='8' height='22' rx='2' fill='url(#gold)'/>"
        "<rect x='42' y='12' width='8' height='32' rx='2' fill='url(#gold)'/>"
        "</svg>"
        "<div><h1 style='margin:0 !important;'>Cannabis Sales Forecaster</h1>"
        "<p>AI-powered daily gross sales forecast</p></div>"
        "</div></div>",
        unsafe_allow_html=True,
    )

    # ---- Input sections ----
    with st.container(border=True):
        st.subheader("Forecast Date")
        c1, c2, c3 = st.columns(3)
        with c1:
            year = st.number_input("Year", 2021, 2026, 2024, 1)
        with c2:
            month = st.number_input("Month", 1, 12, 12, 1)
        with c3:
            day = st.number_input("Day", 1, 31, 15, 1)

    with st.container(border=True):
        st.subheader("Recent Daily Gross Sales ($)")
        st.caption("Actual sales on those past days, used for lag features. "
                   "Averages feed the rolling means.")
        r1, r2, r3 = st.columns(3)
        with r1:
            lag_1 = st.number_input("Sales yesterday", 0.0, value=200000.0,
                                    step=1000.0)
        with r2:
            lag_7 = st.number_input("Sales 7 days ago", 0.0, value=195000.0,
                                    step=1000.0)
        with r3:
            lag_30 = st.number_input("Sales 30 days ago", 0.0, value=190000.0,
                                     step=1000.0)
        r4, r5 = st.columns(2)
        with r4:
            rolling_mean_7 = st.number_input("Average of last 7 days", 0.0,
                                             value=198000.0, step=1000.0)
        with r5:
            rolling_mean_30 = st.number_input("Average of last 30 days", 0.0,
                                              value=196000.0, step=1000.0)

    predict = st.button("Predict Sales", type="primary")

    # ---- Prediction section ----
    if predict:
        try:
            selected_date = datetime.date(int(year), int(month), int(day))
        except ValueError:
            st.error("Invalid date for that month (e.g. Feb 30 does not exist).")
            st.stop()

        try:
            input_df = build_input_df(
                selected_date, lag_1, lag_7, lag_30,
                rolling_mean_7, rolling_mean_30, features,
            )
            prediction = predict_sales(model, input_df)
        except Exception:
            st.error("Could not compute the forecast. "
                     "Check the inputs and try again.")
        else:
            st.divider()
            weekday = selected_date.weekday()
            kind = "Weekend" if weekday >= 5 else "Weekday"
            vs_typical = prediction / TYPICAL_DAY
            st.markdown(
                '<div class="sales-card">'
                '<div class="label">Predicted Daily Gross Sales</div>'
                f'<div class="value">${prediction:,.2f}</div>'
                f'<div>{selected_date.strftime("%A, %B %d, %Y")}</div>'
                f'<div class="context">Typical day ≈ ${TYPICAL_DAY:,.0f} · '
                f"this forecast is {vs_typical:.1f}x typical</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            date_line = (
                f"**{WEEKDAY_NAMES[weekday]}** · "
                f"{MONTH_NAMES[selected_date.month - 1]} · {kind}"
            )
            if selected_date.month in (10, 11, 12):
                date_line += " · Q4"
            st.markdown(date_line)

    # ---- Model section ----
    st.divider()
    with st.expander("About this forecast"):
        st.markdown(
            "**Model**\n\nRidge Regression (R² 0.900 on unseen 2024 data)\n\n"
            "**Purpose**\n\nPredict next-day total gross sales revenue"
        )


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
# pip install streamlit pandas numpy joblib scikit-learn
# streamlit run cannabis_sales_app.py
