"""Main Streamlit entry point for the Revenue Intelligence Suite."""

from __future__ import annotations

import plotly.express as px
import pandas as pd
import streamlit as st

from src.dashboard_service import (
    APP_SUBTITLE,
    APP_TITLE,
    calculate_metrics,
    configure_page,
    display_metric_row,
    generate_business_insights,
    grouped_revenue,
    load_global_styles,
    load_sales_data,
    render_sidebar_chrome,
    render_app_header,
    revenue_by_day,
    to_csv_bytes,
)


configure_page("Growth Command Center")
load_global_styles()


def render_growth_command_center() -> None:
    """Render the executive overview."""
    df = load_sales_data()
    filtered = df.copy()
    theme = render_sidebar_chrome("Growth Command Center")

    with st.sidebar:
        view_mode = st.radio(
            "Dashboard mode",
            options=["Executive", "Operations"],
            index=0,
            horizontal=True,
            key="main_view_mode",
        )
        period = st.select_slider(
            "Time window",
            options=["30 days", "90 days", "180 days", "All data"],
            value="All data",
            key="main_period",
        )
        region_options = sorted(df["region"].dropna().unique().tolist())
        selected_regions = st.multiselect(
            "Regional focus",
            options=region_options,
            default=region_options,
            key="main_regions",
        )
        category_options = sorted(df["category"].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Category focus",
            options=category_options,
            default=category_options,
            key="main_categories",
        )

    if period != "All data":
        days = int(period.split()[0])
        cutoff = filtered["date"].max() - pd.Timedelta(days=days)
        filtered = filtered[filtered["date"] >= cutoff]
    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]
    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]

    render_app_header(
        "Growth Command Center",
        APP_SUBTITLE,
    )

    if filtered.empty:
        st.warning("No records match the current dashboard controls.")
        st.stop()

    metrics = calculate_metrics(filtered)
    display_metric_row(metrics)

    st.markdown("### Revenue Pulse")
    daily = revenue_by_day(filtered)
    category_mix = grouped_revenue(filtered, "category")
    region_mix = grouped_revenue(filtered, "region")

    left, right = st.columns([2, 1])
    with left:
        trend = px.area(
            daily,
            x="date",
            y="revenue",
            title="Daily revenue trajectory",
            template=theme["plot_template"],
            color_discrete_sequence=[theme["primary"]],
        )
        trend.update_traces(line=dict(width=2.5), hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.0f}<extra></extra>")
        trend.update_layout(height=410, margin=dict(l=20, r=20, t=55, b=20), yaxis_title="Revenue", xaxis_title="")
        st.plotly_chart(trend, use_container_width=True)

    with right:
        mix = px.pie(
            category_mix,
            names="category",
            values="revenue",
            title="Category contribution",
            hole=0.58,
            template=theme["plot_template"],
            color_discrete_sequence=["#2457c5", "#10b981", "#f59e0b", "#ef4444", "#64748b"],
        )
        mix.update_layout(height=410, margin=dict(l=10, r=10, t=55, b=10), legend_title_text="")
        st.plotly_chart(mix, use_container_width=True)

    st.markdown("### Performance Leaders")
    col1, col2 = st.columns(2)
    with col1:
        top_products = grouped_revenue(filtered, "product_name", limit=8)
        product_fig = px.bar(
            top_products.sort_values("revenue"),
            x="revenue",
            y="product_name",
            orientation="h",
            title="Top products by revenue",
            template=theme["plot_template"],
            color="revenue",
            color_continuous_scale=theme["scale"],
        )
        product_fig.update_layout(height=390, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(product_fig, use_container_width=True)

    with col2:
        region_fig = px.bar(
            region_mix,
            x="region",
            y="revenue",
            title="Regional revenue position",
            template=theme["plot_template"],
            color="revenue",
            color_continuous_scale=theme["scale"],
        )
        region_fig.update_layout(height=390, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="", yaxis_title="Revenue", showlegend=False)
        st.plotly_chart(region_fig, use_container_width=True)

    st.markdown("### Decision Notes")
    insights = generate_business_insights(filtered)
    insight_cols = st.columns(3)
    for index, insight in enumerate(insights[:6]):
        with insight_cols[index % 3]:
            st.info(insight)

    if view_mode == "Operations":
        st.markdown("### Data Quality Snapshot")
        quality_cols = st.columns(4)
        quality_cols[0].metric("Records", f"{len(filtered):,}")
        quality_cols[1].metric("Date span", f"{daily['date'].dt.date.nunique():,} days")
        quality_cols[2].metric("Products", f"{filtered['product_name'].nunique():,}")
        quality_cols[3].metric("Categories", f"{filtered['category'].nunique():,}")
        st.download_button(
            "Download current dataset",
            data=to_csv_bytes(filtered),
            file_name="revenue_command_center_data.csv",
            mime="text/csv",
        )


def run_app_navigation() -> None:
    """Register polished app navigation labels."""
    pages = {
        APP_TITLE: [
            st.Page(
                render_growth_command_center,
                title="HOME Page",
                icon=":material/home:",
                url_path="home",
                default=True,
            ),
            st.Page(
                "pages/1_Revenue_Explorer.py",
                title="Revenue Explorer",
                icon=":material/query_stats:",
                url_path="revenue-explorer",
            ),
            st.Page(
                "pages/2_Product_Portfolio.py",
                title="Product Portfolio",
                icon=":material/category:",
                url_path="product-portfolio",
            ),
            st.Page(
                "pages/3_Executive_Report_Studio.py",
                title="Executive Report Studio",
                icon=":material/contract:",
                url_path="executive-report-studio",
            ),
        ]
    }
    selected_page = st.navigation(pages, position="sidebar", expanded=True)
    selected_page.run()


if __name__ == "__main__":
    run_app_navigation()
