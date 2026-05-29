"""Executive report builder page."""

from __future__ import annotations

from datetime import datetime

import plotly.express as px
import streamlit as st

from src.dashboard_service import (
    apply_sidebar_filters,
    calculate_metrics,
    format_columns,
    generate_business_insights,
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
theme = render_sidebar_chrome("Report Studio")
filtered = apply_sidebar_filters(df, "reports")

render_app_header(
    "Executive Report Studio",
    "Build a clean leadership-ready sales brief from the same governed data model.",
)

if filtered.empty:
    st.warning("No report can be generated because the current filters returned no records.")
    st.stop()

with st.sidebar:
    st.markdown("### Report Options")
    report_title = st.text_input("Report title", value="Sales Performance Brief")
    include_raw_data = st.checkbox("Include transaction export", value=False)
    ranking_limit = st.slider("Ranking rows", min_value=5, max_value=20, value=10)

metrics = calculate_metrics(filtered)
daily = revenue_by_day(filtered)
top_products = grouped_revenue(filtered, "product_name", limit=ranking_limit)
top_regions = grouped_revenue(filtered, "region", limit=ranking_limit)
top_categories = grouped_revenue(filtered, "category", limit=ranking_limit)
insights = generate_business_insights(filtered)

st.markdown(f"## {report_title}")
st.caption(f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

summary_cols = st.columns(4)
summary_cols[0].metric("Revenue", f"${metrics.revenue:,.0f}", f"{metrics.growth_rate:+.1f}%")
summary_cols[1].metric("Orders", f"{metrics.orders:,}")
summary_cols[2].metric("Customers", f"{metrics.customers:,}")
summary_cols[3].metric("Avg order value", f"${metrics.avg_order_value:,.2f}")

st.markdown("### Executive Summary")
for insight in insights[:5]:
    st.markdown(f"- {insight}")

trend = px.area(
    daily,
    x="date",
    y="revenue",
    title="Revenue trend for report period",
    template=theme["plot_template"],
    color_discrete_sequence=[theme["primary"]],
)
trend.update_layout(height=360, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="", yaxis_title="Revenue")
st.plotly_chart(trend, use_container_width=True)

rank_col1, rank_col2 = st.columns(2)
with rank_col1:
    st.markdown("### Product Ranking")
    st.dataframe(
        format_columns(top_products, money_columns=["revenue", "avg_order_value"]),
        use_container_width=True,
        hide_index=True,
    )

with rank_col2:
    st.markdown("### Regional Ranking")
    st.dataframe(
        format_columns(top_regions, money_columns=["revenue", "avg_order_value"]),
        use_container_width=True,
        hide_index=True,
    )

st.markdown("### Category Mix")
st.dataframe(
    format_columns(top_categories, money_columns=["revenue", "avg_order_value"]),
    use_container_width=True,
    hide_index=True,
)

report_lines = [
    report_title,
    f"Generated: {datetime.now().isoformat(timespec='seconds')}",
    "",
    "Executive Summary",
    *[f"- {insight}" for insight in insights[:8]],
    "",
    "Key Metrics",
    f"- Revenue: ${metrics.revenue:,.2f}",
    f"- Orders: {metrics.orders:,}",
    f"- Customers: {metrics.customers:,}",
    f"- Average order value: ${metrics.avg_order_value:,.2f}",
    f"- Revenue per customer: ${metrics.revenue_per_customer:,.2f}",
]

downloads = st.columns(2)
downloads[0].download_button(
    "Download executive brief",
    data="\n".join(report_lines).encode("utf-8"),
    file_name="executive_sales_brief.md",
    mime="text/markdown",
)

export_df = filtered if include_raw_data else top_products
downloads[1].download_button(
    "Download supporting data",
    data=to_csv_bytes(export_df),
    file_name="sales_report_supporting_data.csv",
    mime="text/csv",
)
