"""Formatting helpers and the forecast feature builder."""

from __future__ import annotations

import datetime as dt

import pandas as pd

SERIES_START = dt.date(2021, 1, 1)
TYPICAL_DAY = 201_702.570124
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def money(value: float, compact: bool = False, digits: int = 0) -> str:
    if compact:
        for size, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
            if abs(value) >= size:
                return f"${value / size:,.{max(digits, 1)}f}{suffix}"
    return f"${value:,.{digits}f}"


def pct(value: float, digits: int = 1, signed: bool = False) -> str:
    return f"{value:+.{digits}%}" if signed else f"{value:.{digits}%}"


def feature_row(date: dt.date, lag_1: float, lag_7: float, lag_30: float,
                rolling_7: float, rolling_30: float) -> dict:
    """Same calendar flags as the notebook. time_step counts days from 2021-01-01."""
    weekday = date.weekday()
    return {
        "Month": date.month,
        "Day": date.day,
        "Year": date.year,
        "is_q4": int(date.month in (10, 11, 12)),
        "is_month_start": int(date.day <= 3),
        "is_month_end": int(date.day >= 28),
        "DayOfWeek": weekday,
        "IsWeekend": int(weekday >= 5),
        "time_step": max(0, (date - SERIES_START).days),
        "lag_1": float(lag_1),
        "lag_7": float(lag_7),
        "lag_30": float(lag_30),
        "rolling_mean_7": float(rolling_7),
        "rolling_mean_30": float(rolling_30),
    }


def predict(model, features: list[str], row: dict) -> float:
    frame = pd.DataFrame([[row[f] for f in features]], columns=features)
    return max(0.0, float(model.predict(frame)[0]))


def contributions(model, features: list[str], row: dict) -> pd.DataFrame:
    df = pd.DataFrame({"feature": features, "value": [row[f] for f in features], "coef": model.coef_})
    df["contribution"] = df["value"] * df["coef"]
    return df


def recent_inputs(daily: pd.DataFrame, date: dt.date) -> dict:
    """Lag and rolling inputs taken from the daily series ending the day before `date`."""
    series = daily.set_index("date")["gross_sales"]
    history = series[series.index < pd.Timestamp(date)]
    if len(history) < 30:
        history = series.iloc[:30]
    return {
        "lag_1": float(history.iloc[-1]),
        "lag_7": float(history.iloc[-7]),
        "lag_30": float(history.iloc[-30]),
        "rolling_7": float(history.iloc[-7:].mean()),
        "rolling_30": float(history.iloc[-30:].mean()),
    }


def season(month: int) -> str:
    return {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
            6: "Summer", 7: "Summer", 8: "Summer"}.get(month, "Autumn") + (" · Q4" if month >= 10 else "")
