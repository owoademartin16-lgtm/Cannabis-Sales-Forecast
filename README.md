# Cannabis Gross Sales Forecast

Daily gross sales forecasting from four years of sales records, plus a live prediction app.

## What it does

- Engineers calendar features plus lag (1, 7, 30 days) and rolling-average features
- Splits chronologically: 1,144 training rows, 287 test rows on unseen 2024 data
- Compares Linear, Ridge, Random Forest, CatBoost, XGBoost, and Gradient Boosting
- Ships the winner (Ridge, test R² 0.900, average miss $4,444/day) as a Streamlit app

## Files

- `Cannabis Sales.ipynb` — analysis, feature engineering, and model comparison
- `cannabis_sales_app.py` — Streamlit sales forecasting app
- `cannabis_ridge_model.joblib` — trained Ridge model and feature order

## How to run

```bash
pip install -r requirements.txt
streamlit run cannabis_sales_app.py
```
