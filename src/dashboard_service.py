"""Shared services for the Streamlit sales intelligence app."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

from data.sample_data import generate_sample_data
from src.analytics_engine import AnalyticsEngine
from src.data_processor import DataProcessor


APP_TITLE = "Revenue Intelligence Suite"
APP_SUBTITLE = "A focused operating view for sales growth, product mix, and executive reporting."
ROOT_DIR = Path(__file__).resolve().parent.parent
STYLE_PATH = ROOT_DIR / "assets" / "style.css"

THEMES = {
    "Light": {
        "page": "#f8fafc",
        "surface": "#ffffff",
        "ink": "#111827",
        "muted": "#64748b",
        "line": "#e5e7eb",
        "hero": "linear-gradient(135deg, #ffffff 0%, #eff6ff 58%, #ecfdf5 100%)",
        "primary": "#2457c5",
        "accent": "#10b981",
        "plot_template": "plotly_white",
        "scale": ["#dbeafe", "#2457c5"],
    },
    "Dark": {
        "page": "#08111f",
        "surface": "#0f1b2d",
        "ink": "#e5eefc",
        "muted": "#9fb2cc",
        "line": "#22314a",
        "hero": "linear-gradient(135deg, #0f1b2d 0%, #102a4c 58%, #092f2c 100%)",
        "primary": "#60a5fa",
        "accent": "#34d399",
        "plot_template": "plotly_dark",
        "scale": ["#172554", "#60a5fa"],
    },
}


@dataclass(frozen=True)
class RevenueMetrics:
    """Top-level metrics used across dashboard pages."""

    revenue: float
    orders: int
    customers: int
    units: int
    avg_order_value: float
    avg_unit_price: float
    revenue_per_customer: float
    growth_rate: float


def configure_page(page_title: str) -> None:
    """Apply a consistent Streamlit page configuration."""
    st.set_page_config(
        page_title=f"{page_title} | {APP_TITLE}",
        page_icon="assets/logo.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_global_styles() -> None:
    """Load project CSS when available."""
    if STYLE_PATH.exists():
        st.markdown(f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_sidebar_chrome(section_title: str) -> dict[str, str]:
    """Render shared sidebar controls and return the selected theme."""
    with st.sidebar:
        st.markdown(f"### {section_title}")
        st.caption("Tune the workspace appearance and move between focused analysis modes.")
        theme_name = st.radio(
            "Appearance",
            options=["Light", "Dark"],
            horizontal=True,
            key=f"{section_title.lower().replace(' ', '_')}_theme",
        )
        st.markdown(
            f"""
            <div class="sidebar-status">
                <span>Mode</span>
                <strong>{theme_name}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    theme = THEMES[theme_name]
    apply_theme_styles(theme)
    return theme


def apply_theme_styles(theme: dict[str, str]) -> None:
    """Inject theme variables for Streamlit chrome."""
    st.markdown(
        f"""
        <style>
            :root {{
                --page: {theme["page"]};
                --surface: {theme["surface"]};
                --ink: {theme["ink"]};
                --muted: {theme["muted"]};
                --line: {theme["line"]};
                --primary: {theme["primary"]};
                --primary-soft: {theme["scale"][0]};
                --hero-bg: {theme["hero"]};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_header(title: str, description: str) -> None:
    """Render the shared page header."""
    st.markdown(
        f"""
        <div class="app-hero">
            <div>
                <p class="eyebrow">{APP_TITLE}</p>
                <h1>{title}</h1>
                <p>{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=900, show_spinner=False)
def load_sales_data(rows: int = 12000) -> pd.DataFrame:
    """Load sales data from the configured database, falling back to generated data."""
    processor = DataProcessor()

    try:
        from src.config import AppConfig
        from src.database import DatabaseManager

        config = AppConfig()
        db = DatabaseManager(config)
        df = db.get_sales_data(limit=config.max_data_points)
        db.close()
        if df is None or df.empty:
            df = generate_sample_data(rows=rows)
    except Exception:
        df = generate_sample_data(rows=rows)

    df = processor.load_data(df)
    df = processor.clean_data(df)
    df = processor.transform_data(df)
    return df.sort_values("date").reset_index(drop=True)


def apply_sidebar_filters(df: pd.DataFrame, key_prefix: str) -> pd.DataFrame:
    """Apply consistent sidebar filters with stable Streamlit keys."""
    filtered = df.copy()
    st.sidebar.markdown("### Analysis Scope")

    if "date" in filtered.columns:
        filtered["date"] = pd.to_datetime(filtered["date"])
        min_date = filtered["date"].min().date()
        max_date = filtered["date"].max().date()
        date_range = st.sidebar.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=f"{key_prefix}_date_range",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered = filtered[
                (filtered["date"].dt.date >= start_date)
                & (filtered["date"].dt.date <= end_date)
            ]

    for column, label in (
        ("region", "Regions"),
        ("category", "Categories"),
        ("product_name", "Products"),
    ):
        if column in filtered.columns:
            options = sorted(filtered[column].dropna().unique().tolist())
            default = options if column != "product_name" else []
            selected = st.sidebar.multiselect(
                label,
                options=options,
                default=default,
                key=f"{key_prefix}_{column}",
            )
            if selected:
                filtered = filtered[filtered[column].isin(selected)]

    if "revenue" in filtered.columns and not filtered.empty:
        minimum = float(filtered["revenue"].min())
        maximum = float(filtered["revenue"].max())
        if minimum < maximum:
            selected_range = st.sidebar.slider(
                "Order revenue",
                min_value=minimum,
                max_value=maximum,
                value=(minimum, maximum),
                key=f"{key_prefix}_revenue",
            )
            filtered = filtered[
                (filtered["revenue"] >= selected_range[0])
                & (filtered["revenue"] <= selected_range[1])
            ]

    st.sidebar.caption(f"{len(filtered):,} records selected")
    return filtered


def calculate_metrics(df: pd.DataFrame) -> RevenueMetrics:
    """Calculate executive metrics for a filtered data frame."""
    if df.empty:
        return RevenueMetrics(0, 0, 0, 0, 0, 0, 0, 0)

    revenue = float(df["revenue"].sum())
    orders = int(len(df))
    customers = int(df["customer_id"].nunique()) if "customer_id" in df.columns else 0
    units = int(df["quantity"].sum()) if "quantity" in df.columns else 0
    avg_order_value = revenue / orders if orders else 0
    avg_unit_price = revenue / units if units else 0
    revenue_per_customer = revenue / customers if customers else 0

    daily = revenue_by_day(df)
    growth_rate = 0.0
    if len(daily) >= 14:
        recent = daily.tail(7)["revenue"].sum()
        previous = daily.iloc[-14:-7]["revenue"].sum()
        growth_rate = ((recent - previous) / abs(previous)) * 100 if previous else 0.0

    return RevenueMetrics(
        revenue=revenue,
        orders=orders,
        customers=customers,
        units=units,
        avg_order_value=avg_order_value,
        avg_unit_price=avg_unit_price,
        revenue_per_customer=revenue_per_customer,
        growth_rate=growth_rate,
    )


def revenue_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and quantity by day."""
    if df.empty:
        return pd.DataFrame(columns=["date", "revenue", "quantity", "orders"])

    daily = (
        df.assign(date=pd.to_datetime(df["date"]).dt.date)
        .groupby("date", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"), orders=("revenue", "size"))
    )
    daily["date"] = pd.to_datetime(daily["date"])
    return daily


def grouped_revenue(df: pd.DataFrame, group_col: str, limit: int | None = None) -> pd.DataFrame:
    """Aggregate sales metrics by a categorical column."""
    if df.empty or group_col not in df.columns:
        return pd.DataFrame(columns=[group_col, "revenue", "quantity", "orders", "customers"])

    grouped = (
        df.groupby(group_col, as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("revenue", "size"),
            customers=("customer_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )
    grouped["avg_order_value"] = grouped["revenue"] / grouped["orders"].replace(0, 1)
    grouped["share"] = grouped["revenue"] / grouped["revenue"].sum()
    return grouped.head(limit) if limit else grouped


def generate_business_insights(df: pd.DataFrame) -> list[str]:
    """Create compact business insights for the current selection."""
    if df.empty:
        return ["No records match the current filters."]

    engine = AnalyticsEngine()
    insights = engine.generate_insights(df)

    product_rank = grouped_revenue(df, "product_name", limit=1)
    category_rank = grouped_revenue(df, "category", limit=1)
    region_rank = grouped_revenue(df, "region", limit=1)

    if not product_rank.empty:
        row = product_rank.iloc[0]
        insights.append(f"Leading product: {row['product_name']} contributes {row['share']:.1%} of selected revenue.")
    if not category_rank.empty:
        row = category_rank.iloc[0]
        insights.append(f"Top category: {row['category']} at ${row['revenue']:,.0f} revenue.")
    if not region_rank.empty:
        row = region_rank.iloc[0]
        insights.append(f"Strongest region: {row['region']} with {row['orders']:,} orders.")

    return insights


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Return CSV bytes for Streamlit downloads."""
    return df.to_csv(index=False).encode("utf-8")


def display_metric_row(metrics: RevenueMetrics) -> None:
    """Render the standard executive metric row."""
    columns = st.columns(4)
    columns[0].metric("Net revenue", f"${metrics.revenue:,.0f}", f"{metrics.growth_rate:+.1f}% last 7d")
    columns[1].metric("Orders", f"{metrics.orders:,}", f"{metrics.units:,} units")
    columns[2].metric("Customers", f"{metrics.customers:,}", f"${metrics.revenue_per_customer:,.0f} per customer")
    columns[3].metric("Avg order value", f"${metrics.avg_order_value:,.2f}", f"${metrics.avg_unit_price:,.2f} per unit")


def format_columns(df: pd.DataFrame, money_columns: Iterable[str] = ()) -> pd.DataFrame:
    """Return a display-friendly copy with rounded values."""
    formatted = df.copy()
    for column in money_columns:
        if column in formatted.columns:
            formatted[column] = formatted[column].map(lambda value: f"${value:,.2f}")
    if "share" in formatted.columns:
        formatted["share"] = formatted["share"].map(lambda value: f"{value:.1%}")
    return formatted
