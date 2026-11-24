"""Model Lab — six models, holdout errors, cross-validation and feature signal."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils import analysis as an  # noqa: E402
from utils import charts, data_loader, theme  # noqa: E402

import pandas as pd  # noqa: E402

fig = data_loader.load_figures()
models = data_loader.models()
holdout = data_loader.load_holdout()
recon = data_loader.load_reconstruction()
coefs = data_loader.load_coefficients()
ridge = models.iloc[0]
split = fig["split"]

CHART_MODELS = ["Linear Regression", "Ridge Regression", "Random Forest", "Gradient Boosting", "CatBoost", "XGBoost"]
CHART_R2 = [0.914, 0.914, 0.146, -0.529, -0.781, -0.921]

theme.header(
    "Simple beats <em>clever</em>.",
    "Six models were trained on Jan 2021 – Mar 2024 and tested on the next 287 days. "
    "The two linear models track sales within about $4,400 a day; every tree model did worse than guessing the average.",
    pills=[
        f"<b>{split['train']:,}</b> train days → <b>{split['test']}</b> test days",
        f"Test window <b>{split['test_start']}</b> to <b>{split['test_end']}</b>",
        "<b>14</b> calendar, lag and rolling features",
    ],
    icon="model",
)

theme.kpis(
    [
        {"label": "Ridge MAE", "value": an.money(ridge["mae"]), "sub": "average daily miss", "accent": theme.ORANGE},
        {"label": "Ridge RMSE", "value": an.money(ridge["rmse"]), "sub": "penalises big misses", "accent": theme.ORANGE},
        {"label": "Ridge R²", "value": f"{ridge['r2']:.3f}", "sub": "on unseen 2024 days", "accent": theme.YELLOW},
        {"label": "CV mean R²", "value": f"{fig['cv']['ridge_mean']:.3f}", "sub": "Ridge · 5-fold TimeSeriesSplit", "accent": theme.TEAL},
        {"label": "Best tree model", "value": "−0.050", "sub": "Gradient Boosting R²", "accent": theme.ASPHALT},
    ],
    columns=5,
)

left, right = st.columns([0.95, 1.05], gap="medium")
with left:
    metric = st.segmented_control("Metric", ["R²", "MAE", "RMSE"], default="R²", label_visibility="collapsed")
    key = {"R²": "r2", "MAE": "mae", "RMSE": "rmse"}[metric or "R²"]
    theme.chart(charts.model_metric(models, key, height=330))
with right:
    with st.container(border=True, height=418):
        st.html('<div class="cs-kicker">Notebook scoreboard</div>')
        theme.table(
        models.rename(columns={"model": "Model", "mae": "MAE", "rmse": "RMSE", "r2": "R²", "status": "Status"}),
        {"MAE": "${:,.0f}", "RMSE": "${:,.0f}", "R²": "{:.3f}"},
        )
        st.caption(
            "Tree models can't predict above the highest sales they saw in training. Sales kept growing in 2024, "
            "so their forecasts stayed too low."
        )

theme.section(
    "Two sets of R² in the notebook",
    "The evaluation cells print the scores above. A later chart cell plots a hard-coded list "
    "(0.914, 0.914, 0.146, −0.529, −0.781, −0.921) that doesn't match them. Both are shown here.",
    kicker="Notebook check",
)
theme.chart(charts.notebook_r2_chart(models, CHART_R2, CHART_MODELS, height=320))

theme.section(
    "Holdout forecasts",
    "Saved Ridge model scored on the reconstructed 2024 test window: "
    f"MAE {an.money(recon['saved_model_holdout']['mae'])}, RMSE {an.money(recon['saved_model_holdout']['rmse'])}, "
    f"R² {recon['saved_model_holdout']['r2']:.3f}, close to the notebook's printed $4,444 / $5,615 / 0.900.",
    kicker="Actual vs predicted",
)
theme.chart(charts.actual_vs_predicted(holdout, height=360))

left, right = st.columns(2, gap="medium")
with left:
    theme.chart(charts.first_ten(fig["first_test_predictions"], height=320))
with right:
    theme.chart(charts.residual_hist(holdout, height=320))

first = pd.DataFrame(fig["first_test_predictions"])
first["error"] = first["actual"] - first["predicted"]
with st.expander("First 10 test days · exact notebook values"):
    theme.table(
        first.rename(columns={"date": "Date", "actual": "Actual", "predicted": "Predicted", "error": "Error"}),
        {"Actual": "${:,.2f}", "Predicted": "${:,.2f}", "Error": "${:,.2f}"},
    )

theme.section("What the model listens to", "Correlations are the notebook's printed values; coefficients come from the saved model file.", kicker="Features")
left, right = st.columns(2, gap="medium")
with left:
    theme.chart(charts.correlations(fig["correlations"], height=420))
with right:
    theme.chart(charts.cv_folds(fig["cv"], height=420))

with st.expander("Saved Ridge coefficients"):
    theme.table(
        coefs,
        {"coefficient": "{:,.6f}"})
    st.caption("Intercept 118,286.90 · alpha 1.0. rolling_mean_7 (0.962) carries most of the forecast.")

theme.footer()
