"""Cached loaders for the notebook figures, daily series and saved Ridge model."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MODEL_PATH = ROOT / "models" / "cannabis_ridge_model.joblib"


@st.cache_data(show_spinner=False)
def load_figures() -> dict:
    return json.loads((DATA / "notebook_figures.json").read_text())


@st.cache_data(show_spinner=False)
def load_reconstruction() -> dict:
    return json.loads((DATA / "reconstruction.json").read_text())


@st.cache_data(show_spinner=False)
def load_daily() -> pd.DataFrame:
    df = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
    df["dow"] = df["date"].dt.dayofweek
    df["day_name"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["year"] = df["date"].dt.year
    return df


@st.cache_data(show_spinner=False)
def load_holdout() -> pd.DataFrame:
    return pd.read_csv(DATA / "holdout.csv", parse_dates=["date"])


@st.cache_data(show_spinner=False)
def load_coefficients() -> pd.DataFrame:
    return pd.read_csv(DATA / "ridge_coefficients.csv")


@st.cache_data(show_spinner=False)
def monthly() -> pd.DataFrame:
    fig = load_figures()
    df = pd.DataFrame(
        {"month": pd.to_datetime(list(fig["monthly_sales"])), "sales": list(fig["monthly_sales"].values())}
    )
    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month
    return df


@st.cache_data(show_spinner=False)
def quarterly() -> pd.DataFrame:
    fig = load_figures()
    return pd.DataFrame({"quarter": list(fig["quarterly_sales"]), "sales": list(fig["quarterly_sales"].values())})


@st.cache_data(show_spinner=False)
def yearly() -> pd.DataFrame:
    fig = load_figures()
    df = pd.DataFrame({"year": [int(y) for y in fig["yearly_sales"]], "sales": list(fig["yearly_sales"].values())})
    df["growth"] = df["sales"].pct_change()
    return df


@st.cache_data(show_spinner=False)
def categories() -> pd.DataFrame:
    fig = load_figures()
    rows = [{"category": k, **v} for k, v in fig["categories"].items()]
    df = pd.DataFrame(rows).sort_values("sum", ascending=False).reset_index(drop=True)
    df["days"] = (df["sum"] / df["mean"]).round().astype(int)
    df["share"] = df["sum"] / df["sum"].sum()
    return df


@st.cache_data(show_spinner=False)
def models() -> pd.DataFrame:
    return pd.DataFrame(load_figures()["models"])


@st.cache_resource(show_spinner=False)
def load_model():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        artifacts = joblib.load(MODEL_PATH)
    return artifacts["model"], list(artifacts["features"])
