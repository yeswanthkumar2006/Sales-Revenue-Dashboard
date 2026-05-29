"""Interactive revenue exploration page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.dashboard_service import (
    apply_sidebar_filters,
    calculate_metrics,
    display_metric_row,
    format_columns,
    grouped_revenue,
    load_global_styles,
    load_sales_data,
    render_app_header,
    render_sidebar_chrome,
    revenue_by_day,
    to_csv_bytes,
)


load_global_styles()


df = load_sales_data()
theme = render_sidebar_chrome("Revenue Explorer")
filtered = apply_sidebar_filters(df, "explorer")

render_app_header(
    "Revenue Explorer",
    "Slice the transaction base by date, region, category, product, and order value.",
)

if filtered.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

display_metric_row(calculate_metrics(filtered))

tab_overview, tab_table, tab_quality = st.tabs(["Trend analysis", "Transaction table", "Data profile"])

with tab_overview:
    daily = revenue_by_day(filtered)
    group_by = st.selectbox("Compare revenue by", ["region", "category", "product_name"], index=0)
    grouped = grouped_revenue(filtered, group_by, limit=12)

    left, right = st.columns([1.45, 1])
    with left:
        trend = px.line(
            daily,
            x="date",
            y=["revenue", "quantity"],
            title="Revenue and unit volume over time",
            template=theme["plot_template"],
        )
        trend.update_layout(height=430, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="", yaxis_title="Value")
        st.plotly_chart(trend, use_container_width=True)

    with right:
        bar = px.bar(
            grouped.sort_values("revenue"),
            x="revenue",
            y=group_by,
            orientation="h",
            title=f"Revenue by {group_by.replace('_', ' ')}",
            template=theme["plot_template"],
            color="share",
            color_continuous_scale=theme["scale"],
        )
        bar.update_layout(height=430, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(bar, use_container_width=True)

with tab_table:
    st.markdown("### Filtered Transactions")
    visible_columns = st.multiselect(
        "Columns",
        options=filtered.columns.tolist(),
        default=["date", "region", "category", "product_name", "quantity", "price", "revenue"],
    )
    table = filtered[visible_columns].sort_values("date", ascending=False)
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button(
        "Export filtered transactions",
        data=to_csv_bytes(table),
        file_name="revenue_explorer_transactions.csv",
        mime="text/csv",
    )

with tab_quality:
    st.markdown("### Data Profile")
    profile_cols = st.columns(4)
    profile_cols[0].metric("Rows", f"{len(filtered):,}")
    profile_cols[1].metric("Columns", f"{len(filtered.columns):,}")
    profile_cols[2].metric("Missing values", f"{int(filtered.isna().sum().sum()):,}")
    profile_cols[3].metric("Duplicate rows", f"{int(filtered.duplicated().sum()):,}")

    st.markdown("### Segment Summary")
    summary = grouped_revenue(filtered, "category")
    st.dataframe(
        format_columns(summary, money_columns=["revenue", "avg_order_value"]),
        use_container_width=True,
        hide_index=True,
    )
