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


# ---------------------------------------------------------------- slicers ---
YEARS = [2021, 2022, 2023, 2024]
CATEGORIES = ["Flower", "Edibles", "Concentrates"]


def _keep(widget_key: str, store_key: str) -> None:
    st.session_state[store_key] = st.session_state[widget_key]


def slicers() -> None:
    """Sidebar year / category slicers; the choice persists across pages."""
    years = st.session_state.get("f_years", YEARS)
    cats = st.session_state.get("f_cats", CATEGORIES)
    with st.sidebar:
        st.html('<div class="cs-side-label">Slicers</div>')
        st.pills("Year", YEARS, selection_mode="multi", default=years, key="_w_years",
                 on_change=_keep, args=("_w_years", "f_years"))
        st.pills("Product category", CATEGORIES, selection_mode="multi", default=cats, key="_w_cats",
                 on_change=_keep, args=("_w_cats", "f_cats"))
        if set(years) != set(YEARS) or set(cats) != set(CATEGORIES):
            if st.button("Reset slicers", icon=":material/restart_alt:", use_container_width=True):
                for key in ("f_years", "f_cats", "_w_years", "_w_cats"):
                    st.session_state.pop(key, None)
                st.rerun()


def selection() -> tuple[list[int], list[str]]:
    """Current slicer choice; stops the page with a hint when a slicer is empty."""
    years = sorted(st.session_state.get("f_years", YEARS))
    cats = [c for c in CATEGORIES if c in st.session_state.get("f_cats", CATEGORIES)]
    if not years or not cats:
        st.warning("Pick at least one year and one product category in the sidebar slicers.")
        st.stop()
    return years, cats


def all_cats(cats: list[str]) -> bool:
    return set(cats) == set(CATEGORIES)


def is_filtered(years: list[int], cats: list[str]) -> bool:
    return set(years) != set(YEARS) or not all_cats(cats)


def filtered_daily(years: list[int], cats: list[str]) -> pd.DataFrame:
    d = load_daily()
    return d[d["year"].isin(years) & d["category"].isin(cats)].reset_index(drop=True)


def filtered_monthly(years: list[int], cats: list[str]) -> pd.DataFrame:
    """Exact notebook monthly totals unless categories are sliced (then reconstructed rows)."""
    if all_cats(cats):
        m = monthly()
        return m[m["year"].isin(years)].reset_index(drop=True)
    d = filtered_daily(years, cats)
    m = d.groupby(d["date"].dt.to_period("M").dt.to_timestamp())["gross_sales"].sum().reset_index()
    m.columns = ["month", "sales"]
    m["year"] = m["month"].dt.year
    m["month_num"] = m["month"].dt.month
    return m


def filtered_quarterly(years: list[int], cats: list[str]) -> pd.DataFrame:
    if all_cats(cats):
        q = quarterly()
        return q[q["quarter"].str[:4].astype(int).isin(years)].reset_index(drop=True)
    m = filtered_monthly(years, cats)
    q = m.groupby(m["month"].dt.to_period("Q").astype(str))["sales"].sum().reset_index()
    q.columns = ["quarter", "sales"]
    return q


def filtered_yearly(years: list[int], cats: list[str]) -> pd.DataFrame:
    if all_cats(cats):
        y = yearly()
        y = y[y["year"].isin(years)].reset_index(drop=True)
    else:
        m = filtered_monthly(years, cats)
        y = m.groupby("year")["sales"].sum().reset_index()
    prev = y["year"].shift(1)
    y["growth"] = (y["sales"] / y["sales"].shift(1) - 1).where(prev == y["year"] - 1)
    return y


def filtered_categories(years: list[int], cats: list[str]) -> pd.DataFrame:
    """Exact notebook category figures unless years are sliced (then reconstructed rows)."""
    if set(years) == set(YEARS):
        c = categories()
        c = c[c["category"].isin(cats)].reset_index(drop=True)
    else:
        d = filtered_daily(years, cats)
        c = (d.groupby("category")["gross_sales"].agg(["sum", "mean", "min", "max", "count"])
             .rename(columns={"count": "days"}).reset_index()
             .sort_values("sum", ascending=False).reset_index(drop=True))
    c["share"] = c["sum"] / c["sum"].sum()
    return c


def slice_label(years: list[int], cats: list[str]) -> str:
    y = "All years" if set(years) == set(YEARS) else ", ".join(map(str, years))
    k = "all categories" if all_cats(cats) else ", ".join(cats)
    return f"{y} · {k}"
