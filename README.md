# Cannabis Gross Sales Forecast

Daily gross sales forecasting from four years of sales records, presented as a multi-page Streamlit dashboard.

## Dashboard

| Page | What it shows |
| --- | --- |
| Overview | Headline KPIs, monthly trend, category mix, yearly growth, model scoreboard |
| Sales Trends | All 48 monthly totals, year-by-month view, quarterly bars, year × month heatmap, daily series |
| Calendar & Seasonality | Day of week, calendar month, Q4, month start/end, product-category ranges |
| Model Lab | Six-model comparison, holdout actual vs forecast, residuals, cross-validation, correlations |
| Sales Forecaster | Live forecast from the saved Ridge model, with a feature-by-feature breakdown |
| Insights | Seven takeaways and next steps |

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## Where the numbers come from

- **Monthly, quarterly, yearly and category totals, summary statistics, model scores, cross-validation scores, correlations and the first 10 test predictions** are copied exactly from the printed outputs of `Cannabis Sales.ipynb` into `data/notebook_figures.json`.
- The notebook's Massachusetts Cannabis Control Commission download returned **HTTP 404**, so the notebook ran on its built-in simulated series. That series used no random seed, so its daily rows can't be regenerated.
- `build_assets.py` rebuilds a daily series with the same recipe and a fixed seed, then rescales it so all 48 monthly totals, the printed daily rows, and each category's total, mean, min and max match the notebook exactly. Daily-level charts (day of week, holdout forecasts, residuals) use this reconstruction. On it, the saved Ridge model scores MAE $4,442, RMSE $5,579 and R² 0.901, against the notebook's $4,444, $5,615 and 0.900.
- The notebook's model-comparison chart cell uses a hard-coded R² list (0.914, 0.914, 0.146, −0.529, −0.781, −0.921) that doesn't match its printed scores. The Model Lab shows both.

## Model

- Calendar features plus lag (1, 7, 30 days) and rolling-average (7, 30 days) features
- Chronological split: 1,144 training rows, 287 test rows (20 Mar – 31 Dec 2024)
- Compared Linear, Ridge, Random Forest, CatBoost, XGBoost and Gradient Boosting
- Ridge won: test R² 0.900, average miss $4,444 a day

## Files

```
app.py                      Streamlit entry point and Overview page
pages/                      Sales Trends, Calendar, Model Lab, Forecaster, Insights
utils/                      theme, Plotly charts, data loading, feature helpers
data/notebook_figures.json  exact figures from the notebook outputs
data/*.csv                  reconstructed daily series, holdout forecasts, coefficients
build_assets.py             regenerates data/*.csv
models/cannabis_ridge_model.joblib   saved Ridge model and feature order
Cannabis Sales.ipynb        original analysis
```
