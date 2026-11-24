"""Plotly chart builders with a single visual language."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import analysis as an
from . import theme as t

FONT = "Nunito, -apple-system, BlinkMacSystemFont, sans-serif"
DISPLAY = "Righteous, Trebuchet MS, sans-serif"
MONO = "JetBrains Mono, Menlo, monospace"


# ------------------------------------------------------------------- layout ---
def base(fig: go.Figure, height: int = 320, legend: bool = False) -> go.Figure:
    entries = sum(
        1
        for trace in fig.data
        if getattr(trace, "showlegend", None) is not False and getattr(trace, "name", None)
    )
    top_margin = max(58, 18 + 21 * entries) if legend else 28
    fig.update_layout(
        height=height,
        margin=dict(l=6, r=8, t=top_margin, b=6),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=11, color=t.SUBTITLE),
        hoverlabel=dict(
            bgcolor=t.ASPHALT,
            bordercolor=t.ASPHALT,
            font=dict(family=FONT, size=11, color="#F7F5EA"),
        ),
        showlegend=legend,
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=1.0,
            font=dict(size=10, color=t.MUTED),
            bgcolor="rgba(252,252,246,0.94)",
            bordercolor="rgba(201,208,184,0.9)",
            borderwidth=1,
            itemsizing="constant",
            tracegroupgap=2,
        ),
        bargap=0.38,
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=t.BORDER,
        ticks="outside",
        tickcolor=t.BORDER,
        ticklen=3,
        tickfont=dict(size=10, color=t.MUTED),
        title_font=dict(size=10, color=t.MUTED),
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=10, color=t.MUTED),
        title_font=dict(size=10, color=t.MUTED),
    )
    return fig


def _title(fig: go.Figure, text: str) -> None:
    fig.update_layout(
        title=dict(
            text=text,
            font=dict(family=DISPLAY, size=16, color=t.ASPHALT),
            x=0,
            xanchor="left",
            y=0.98,
            pad=dict(b=5),
        )
    )


def _empty(height: int = 300, text: str = "No data for this view") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=text,
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(family=FONT, size=13, color=t.MUTED),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return base(fig, height=height)


def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


YEAR_COLORS = {2021: "#B8C6AE", 2022: t.TEAL_BRIGHT, 2023: t.ORANGE, 2024: t.YELLOW}
CAT_COLORS = {"Flower": t.ORANGE, "Concentrates": t.YELLOW, "Edibles": t.TEAL}
MODEL_COLORS = {
    "Ridge Regression": t.ORANGE,
    "Linear Regression": t.ORANGE_BRIGHT,
    "Gradient Boosting": t.YELLOW,
    "Random Forest": "#B8C6AE",
    "CatBoost": t.TEAL_BRIGHT,
    "XGBoost": t.TEAL,
}


def _badge(fig: go.Figure, x, y, text: str, yshift: int = 18) -> None:
    fig.add_annotation(
        x=x, y=y, text=text, showarrow=False, yshift=yshift,
        font=dict(size=10, color=t.ASPHALT, family=MONO),
        bgcolor="rgba(252,252,246,.92)", bordercolor=t.BORDER, borderwidth=1,
    )


# ------------------------------------------------------------------ trends ---
def monthly_trend(monthly: pd.DataFrame, height: int = 330) -> go.Figure:
    peak = monthly.loc[monthly["sales"].idxmax()]
    low = monthly.loc[monthly["sales"].idxmin()]
    fig = go.Figure(
        go.Scatter(
            x=monthly["month"], y=monthly["sales"], mode="lines",
            line=dict(color=t.ORANGE, width=2.6, shape="spline", smoothing=0.6),
            fill="tozeroy", fillcolor=_rgba(t.ORANGE, 0.13),
            hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>", showlegend=False,
        )
    )
    for row, color in ((peak, t.YELLOW), (low, t.TEAL)):
        fig.add_trace(go.Scatter(
            x=[row["month"]], y=[row["sales"]], mode="markers", showlegend=False, hoverinfo="skip",
            marker=dict(color=t.ASPHALT, size=9, line=dict(color=color, width=2)),
        ))
    _badge(fig, peak["month"], peak["sales"], f"<b>{peak['month']:%b %Y}</b> · {an.money(peak['sales'], compact=True, digits=2)}")
    _badge(fig, low["month"], low["sales"], f"<b>{low['month']:%b %Y}</b> · {an.money(low['sales'], compact=True, digits=2)}", yshift=-18)
    fig.update_xaxes(tickformat="%b %Y", nticks=9)
    fig.update_yaxes(title_text="Monthly gross sales", tickprefix="$", tickformat="~s", rangemode="tozero")
    _title(fig, f"Monthly gross sales · {len(monthly)} months")
    return base(fig, height=height)


def yearly_bars(yearly: pd.DataFrame, height: int = 330) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=yearly["year"].astype(str), y=yearly["sales"],
        marker=dict(color=[YEAR_COLORS[y] for y in yearly["year"]], line=dict(width=0)),
        text=[an.money(v, compact=True, digits=1) for v in yearly["sales"]], textposition="outside",
        textfont=dict(family=MONO, size=11, color=t.ASPHALT), cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    for _, row in yearly.dropna().iterrows():
        fig.add_annotation(x=str(int(row["year"])), y=row["sales"] / 2, text=f"<b>{row['growth']:+.1%}</b>",
                           showarrow=False, font=dict(family=MONO, size=10, color=t.ASPHALT))
    fig.update_yaxes(visible=False, range=[0, yearly["sales"].max() * 1.18])
    _title(fig, "Yearly gross sales · growth vs prior year")
    return base(fig, height=height)


def category_donut(cats: pd.DataFrame, height: int = 330) -> go.Figure:
    top = cats.iloc[0]
    fig = go.Figure(go.Pie(
        labels=cats["category"], values=cats["sum"], hole=0.68, sort=False,
        marker=dict(colors=[CAT_COLORS[c] for c in cats["category"]], line=dict(color=t.SURFACE, width=2)),
        textinfo="none",
        customdata=cats["days"],
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{customdata} days · %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text=(f"<span style='font-family:{DISPLAY};font-size:30px;color:{t.ASPHALT};'>{top['share'] * 100:.1f}%</span>"
              f"<br><span style='font-family:{MONO};font-size:9px;color:{t.MUTED};letter-spacing:.12em;'>"
              f"{top['category'].upper()}</span>"),
        showarrow=False, x=0.5, y=0.5,
    )
    fig.update_layout(margin=dict(l=4, r=4, t=28, b=4), legend=dict(orientation="h", y=-0.02, x=0.5, xanchor="center", yanchor="top"))
    _title(fig, "Gross sales by product category")
    fig = base(fig, height=height, legend=True)
    fig.update_layout(margin=dict(t=34, b=30), legend=dict(orientation="h", y=-0.02, x=0.5, xanchor="center", yanchor="top", bgcolor="rgba(0,0,0,0)", borderwidth=0))
    return fig


def daily_line(daily: pd.DataFrame, height: int = 360) -> go.Figure:
    series = daily.set_index("date")["gross_sales"]
    roll = series.rolling("30D").mean().where(series.index >= series.index[0] + pd.Timedelta(days=29)).values
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["gross_sales"], mode="lines", name="Daily gross sales",
        line=dict(color=_rgba(t.ORANGE, 0.45), width=1),
        hovertemplate="<b>%{x|%a %d %b %Y}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=daily["date"], y=roll, mode="lines", name="30-day average",
        line=dict(color=t.ASPHALT, width=2.4),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>30-day avg $%{y:,.0f}<extra></extra>",
    ))
    fig.update_yaxes(title_text="Daily gross sales", tickprefix="$", tickformat="~s")
    _title(fig, f"Daily gross sales · {len(daily):,} days")
    return base(fig, height=height, legend=True)


def monthly_by_year(monthly: pd.DataFrame, height: int = 340) -> go.Figure:
    fig = go.Figure()
    for year, group in monthly.groupby("year"):
        fig.add_trace(go.Scatter(
            x=[an.MONTH_ABBR[m - 1] for m in group["month_num"]], y=group["sales"], name=str(year),
            mode="lines+markers", line=dict(color=YEAR_COLORS[year], width=2.4),
            marker=dict(size=6), hovertemplate=f"<b>%{{x}} {year}</b><br>$%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_yaxes(title_text="Monthly gross sales", tickprefix="$", tickformat="~s")
    _title(fig, "Each year, month by month")
    return base(fig, height=height, legend=True)


def quarterly_bars(quarterly: pd.DataFrame, height: int = 340) -> go.Figure:
    colors = [t.YELLOW if q.endswith("Q4") else _rgba(t.ORANGE, 0.75) for q in quarterly["quarter"]]
    fig = go.Figure(go.Bar(
        x=quarterly["quarter"], y=quarterly["sales"], marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    fig.update_yaxes(title_text="Quarterly gross sales", tickprefix="$", tickformat="~s")
    _title(fig, "Quarterly gross sales · Q4 in gold")
    return base(fig, height=height)


def month_year_heatmap(monthly: pd.DataFrame, height: int = 300) -> go.Figure:
    pivot = monthly.pivot(index="year", columns="month_num", values="sales")
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=an.MONTH_ABBR, y=[str(y) for y in pivot.index],
        colorscale=t.GOLD_SCALE, xgap=3, ygap=3,
        text=[[an.money(v, compact=True, digits=2) for v in row] for row in pivot.values],
        texttemplate="%{text}", textfont=dict(family=MONO, size=10),
        hovertemplate="<b>%{x} %{y}</b><br>$%{z:,.0f}<extra></extra>",
        colorbar=dict(thickness=10, tickprefix="$", tickformat="~s", outlinewidth=0),
    ))
    fig.update_yaxes(autorange="reversed")
    _title(fig, "Monthly gross sales · year × month")
    return base(fig, height=height)


# ---------------------------------------------------------------- calendar ---
def dow_bars(daily: pd.DataFrame, height: int = 330) -> go.Figure:
    dow = daily.groupby("dow")["gross_sales"].mean().reindex(range(7))
    colors = [t.TEAL if d >= 5 else t.ORANGE for d in range(7)]
    fig = go.Figure(go.Bar(
        x=[d[:3] for d in an.DAY_NAMES], y=dow.values, marker=dict(color=colors, line=dict(width=0)),
        text=[an.money(v, compact=True, digits=1) for v in dow.values], textposition="outside",
        textfont=dict(family=MONO, size=10, color=t.ASPHALT), cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>avg $%{y:,.0f}<extra></extra>",
    ))
    lo, hi = dow.min(), dow.max()
    fig.update_yaxes(range=[lo * 0.97, hi * 1.02], tickprefix="$", tickformat="~s", title_text="Average daily sales")
    _title(fig, "Average sales by day of week · weekend in purple")
    return base(fig, height=height)


def month_of_year(monthly: pd.DataFrame, height: int = 330) -> go.Figure:
    df = monthly.copy()
    if "days" not in df:
        df["days"] = df["month"].dt.days_in_month
    totals = df.groupby("month_num")[["sales", "days"]].sum()
    g = totals["sales"] / totals["days"]
    colors = [t.YELLOW if m >= 10 else _rgba(t.ORANGE, 0.75) for m in g.index]
    fig = go.Figure(go.Bar(
        x=an.MONTH_ABBR, y=g.values, marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>avg $%{y:,.0f} per day<extra></extra>",
    ))
    fig.update_yaxes(range=[g.min() * 0.9, g.max() * 1.04], tickprefix="$", tickformat="~s", title_text="Average sales per day")
    _title(fig, "Average sales per day by calendar month")
    return base(fig, height=height)


def segment_bars(labels: list[str], values: list[float], colors: list[str], title: str, height: int = 300) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker=dict(color=colors, line=dict(width=0)),
        text=[an.money(v, compact=True, digits=1) for v in values], textposition="outside",
        textfont=dict(family=MONO, size=10, color=t.ASPHALT), cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>avg $%{y:,.0f}<extra></extra>",
    ))
    fig.update_yaxes(range=[min(values) * 0.95, max(values) * 1.04], tickprefix="$", tickformat="~s")
    _title(fig, title)
    return base(fig, height=height)


def category_range(cats: pd.DataFrame, height: int = 300) -> go.Figure:
    fig = go.Figure()
    for _, row in cats.iterrows():
        c = CAT_COLORS[row["category"]]
        fig.add_trace(go.Scatter(
            x=[row["min"], row["max"]], y=[row["category"]] * 2, mode="lines",
            line=dict(color=_rgba(c, 0.45), width=10), showlegend=False, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[row["min"], row["mean"], row["max"]], y=[row["category"]] * 3, mode="markers",
            marker=dict(color=[c, t.ASPHALT, c], size=[9, 12, 9], line=dict(color=t.SURFACE, width=1.5)),
            customdata=["Min", "Mean", "Max"], showlegend=False,
            hovertemplate="<b>%{y}</b> · %{customdata}<br>$%{x:,.0f}<extra></extra>",
        ))
    fig.update_xaxes(tickprefix="$", tickformat="~s", title_text="Daily gross sales (min · mean · max)")
    _title(fig, "Daily sales range by category")
    return base(fig, height=height)


# --------------------------------------------------------------- model lab ---
def model_metric(models: pd.DataFrame, metric: str = "r2", height: int = 340) -> go.Figure:
    label = {"r2": "R²", "mae": "MAE", "rmse": "RMSE"}[metric]
    df = models.sort_values(metric, ascending=metric != "r2")
    text = [f"{v:.3f}" if metric == "r2" else an.money(v) for v in df[metric]]
    fig = go.Figure(go.Bar(
        y=df["model"], x=df[metric], orientation="h",
        marker=dict(color=[MODEL_COLORS[m] for m in df["model"]], line=dict(width=0)),
        text=text, textposition="outside", textfont=dict(family=MONO, size=10, color=t.ASPHALT), cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>" + label + " %{text}<extra></extra>",
    ))
    if metric == "r2":
        fig.add_vline(x=0, line=dict(color=t.MUTED, width=1, dash="dot"))
        fig.update_xaxes(range=[-1.25, 1.25])
    else:
        fig.update_xaxes(tickprefix="$", tickformat="~s", range=[0, df[metric].max() * 1.22])
    fig.update_yaxes(autorange="reversed")
    _title(fig, f"Holdout {label} · six models")
    fig = base(fig, height=height)
    fig.update_layout(margin=dict(l=6, r=40, t=34, b=6))
    return fig


def notebook_r2_chart(models: pd.DataFrame, chart_r2: list[float], names: list[str], height: int = 320) -> go.Figure:
    printed = models.set_index("model")["r2"].reindex(names)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=printed.values, name="Printed evaluation", marker_color=t.ORANGE,
                         hovertemplate="<b>%{x}</b><br>printed R² %{y:.3f}<extra></extra>"))
    fig.add_trace(go.Bar(x=names, y=chart_r2, name="Hard-coded chart list", marker_color=t.YELLOW,
                         hovertemplate="<b>%{x}</b><br>chart R² %{y:.3f}<extra></extra>"))
    fig.add_hline(y=0, line=dict(color=t.MUTED, width=1, dash="dot"))
    fig.update_layout(barmode="group", bargap=0.3)
    fig.update_xaxes(tickfont=dict(size=9))
    _title(fig, "R² · printed scores vs the notebook's chart cell")
    return base(fig, height=height, legend=True)


def actual_vs_predicted(holdout: pd.DataFrame, height: int = 360) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=holdout["date"], y=holdout["actual"], name="Actual", mode="lines",
        line=dict(color=t.ASPHALT, width=1.6),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>actual $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=holdout["date"], y=holdout["predicted"], name="Ridge forecast", mode="lines",
        line=dict(color=t.ORANGE_BRIGHT, width=2),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>forecast $%{y:,.0f}<extra></extra>",
    ))
    fig.update_yaxes(tickprefix="$", tickformat="~s", title_text="Daily gross sales")
    _title(fig, "Holdout · actual vs Ridge forecast · 287 days")
    return base(fig, height=height, legend=True)


def residual_hist(holdout: pd.DataFrame, height: int = 320) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=holdout["residual"], nbinsx=36, marker=dict(color=_rgba(t.ORANGE, 0.8), line=dict(color=t.SURFACE, width=1)),
        hovertemplate="$%{x:,.0f}<br>%{y} days<extra></extra>",
    ))
    fig.add_vline(x=0, line=dict(color=t.ASPHALT, width=1.4, dash="dot"))
    fig.update_xaxes(tickprefix="$", tickformat="~s", title_text="Actual − forecast")
    fig.update_yaxes(title_text="Days")
    fig.update_layout(bargap=0.05)
    _title(fig, "Holdout residuals")
    return base(fig, height=height)


def first_ten(rows: list[dict], height: int = 320) -> go.Figure:
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["actual"], name="Actual", mode="lines+markers",
                             line=dict(color=t.ASPHALT, width=2), marker=dict(size=7),
                             hovertemplate="<b>%{x|%d %b}</b><br>actual $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["predicted"], name="Predicted", mode="lines+markers",
                             line=dict(color=t.ORANGE_BRIGHT, width=2, dash="dot"), marker=dict(size=7),
                             hovertemplate="<b>%{x|%d %b}</b><br>predicted $%{y:,.0f}<extra></extra>"))
    fig.update_xaxes(tickformat="%d %b")
    fig.update_yaxes(tickprefix="$", tickformat="~s")
    _title(fig, "First 10 test days · Linear Regression (notebook output)")
    return base(fig, height=height, legend=True)


def cv_folds(cv: dict, height: int = 320) -> go.Figure:
    folds = [f"Fold {i}" for i in range(1, 6)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=folds, y=cv["linear"], name=f"Linear · mean {cv['linear_mean']:.3f}", marker_color=t.ORANGE_BRIGHT,
                         hovertemplate="<b>%{x}</b><br>Linear R² %{y:.4f}<extra></extra>"))
    fig.add_trace(go.Bar(x=folds, y=cv["ridge"], name=f"Ridge · mean {cv['ridge_mean']:.3f}", marker_color=t.ORANGE,
                         hovertemplate="<b>%{x}</b><br>Ridge R² %{y:.4f}<extra></extra>"))
    fig.update_layout(barmode="group", bargap=0.3)
    fig.update_yaxes(range=[0, 1], title_text="R²")
    _title(fig, "TimeSeriesSplit · 5-fold R²")
    return base(fig, height=height, legend=True)


def correlations(corr: dict, height: int = 400) -> go.Figure:
    s = pd.Series(corr).sort_values()
    colors = [t.ORANGE if v >= 0.5 else (t.YELLOW if v >= 0.1 else "#B8C6AE") for v in s.values]
    fig = go.Figure(go.Bar(
        y=s.index, x=s.values, orientation="h", marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.3f}" for v in s.values], textposition="outside", cliponaxis=False,
        textfont=dict(family=MONO, size=10, color=t.ASPHALT),
        hovertemplate="<b>%{y}</b><br>r = %{x:.6f}<extra></extra>",
    ))
    fig.update_xaxes(range=[-0.1, 1.15], title_text="Correlation with Gross Sales")
    _title(fig, "Feature correlation with gross sales")
    fig = base(fig, height=height)
    fig.update_layout(margin=dict(l=6, r=40, t=34, b=6))
    return fig


def contribution_bars(contrib: pd.DataFrame, intercept: float, total: float, height: int = 420) -> go.Figure:
    df = contrib.reindex(contrib["contribution"].abs().sort_values(ascending=False).index)
    labels = ["Intercept"] + df["feature"].tolist()
    values = [intercept] + df["contribution"].tolist()
    floor = total - sum(values)
    if floor > 0.5:
        labels.append("Floor at $0")
        values.append(floor)
    fig = go.Figure(go.Waterfall(
        orientation="h",
        y=labels + ["Forecast"],
        x=values + [total],
        measure=["absolute"] + ["relative"] * (len(values) - 1) + ["total"],
        increasing=dict(marker=dict(color=t.ORANGE)), decreasing=dict(marker=dict(color=t.TEAL_BRIGHT)),
        totals=dict(marker=dict(color=t.YELLOW)), connector=dict(line=dict(color=t.BORDER, width=1)),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    fig.update_xaxes(tickprefix="$", tickformat="~s")
    _title(fig, "How the Ridge model builds this forecast")
    return base(fig, height=height)


def forecast_context(history: pd.DataFrame, date, value: float, low: float, high: float, height: int = 330) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history["date"], y=history["gross_sales"], mode="lines+markers", name="Last 30 days",
        line=dict(color=t.ASPHALT, width=1.8), marker=dict(size=4),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    ts = pd.Timestamp(date)
    fig.add_trace(go.Scatter(
        x=[ts, ts], y=[low, high], mode="lines", name="Typical range",
        line=dict(color=_rgba(t.YELLOW, 0.8), width=10), hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=[ts], y=[value], mode="markers", name="Forecast",
        marker=dict(color=t.ORANGE, size=13, line=dict(color=t.SURFACE, width=2)),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>forecast $%{y:,.0f}<extra></extra>",
    ))
    fig.update_yaxes(tickprefix="$", tickformat="~s")
    fig.update_xaxes(tickformat="%d %b")
    _title(fig, "Forecast in context")
    return base(fig, height=height, legend=True)
