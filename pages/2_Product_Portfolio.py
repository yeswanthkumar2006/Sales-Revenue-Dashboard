"""Product portfolio intelligence page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.dashboard_service import (
    apply_sidebar_filters,
    format_columns,
    generate_business_insights,
    grouped_revenue,
    load_global_styles,
    load_sales_data,
    render_app_header,
    render_sidebar_chrome,
)


load_global_styles()


df = load_sales_data()
theme = render_sidebar_chrome("Product Portfolio")
filtered = apply_sidebar_filters(df, "portfolio")

render_app_header(
    "Product Portfolio",
    "Find the products, categories, and regions that deserve more focus or corrective action.",
)

if filtered.empty:
    st.warning("No products match the current filter selection.")
    st.stop()

product_summary = grouped_revenue(filtered, "product_name")
category_summary = grouped_revenue(filtered, "category")

leader = product_summary.iloc[0]
focus_cols = st.columns(4)
focus_cols[0].metric("Portfolio revenue", f"${product_summary['revenue'].sum():,.0f}")
focus_cols[1].metric("Active products", f"{len(product_summary):,}")
focus_cols[2].metric("Top product", leader["product_name"], f"${leader['revenue']:,.0f}")
focus_cols[3].metric("Top product share", f"{leader['share']:.1%}", f"{int(leader['orders']):,} orders")

left, right = st.columns([1.25, 1])
with left:
    pareto = product_summary.copy()
    pareto["cumulative_share"] = pareto["revenue"].cumsum() / pareto["revenue"].sum()
    fig = px.bar(
        pareto.head(15),
        x="product_name",
        y="revenue",
        title="Top product revenue concentration",
        template=theme["plot_template"],
        color="share",
        color_continuous_scale=theme["scale"],
    )
    fig.add_scatter(
        x=pareto.head(15)["product_name"],
        y=pareto.head(15)["cumulative_share"] * pareto.head(15)["revenue"].max(),
        mode="lines+markers",
        name="Cumulative share",
        line=dict(color="#111827", width=2),
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=55, b=80), xaxis_title="", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)

with right:
    category = px.treemap(
        filtered,
        path=["category", "product_name"],
        values="revenue",
        title="Category and product mix",
        template=theme["plot_template"],
        color="revenue",
        color_continuous_scale=theme["scale"],
    )
    category.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(category, use_container_width=True)

st.markdown("### Portfolio Matrix")
matrix = product_summary.copy()
matrix["revenue_per_order"] = matrix["revenue"] / matrix["orders"].replace(0, 1)
matrix["unit_velocity"] = matrix["quantity"] / matrix["orders"].replace(0, 1)
scatter = px.scatter(
    matrix,
    x="orders",
    y="revenue_per_order",
    size="revenue",
    color="share",
    hover_name="product_name",
    title="Volume versus value",
    template=theme["plot_template"],
    color_continuous_scale=theme["scale"],
)
scatter.update_layout(height=450, margin=dict(l=20, r=20, t=55, b=20), xaxis_title="Order volume", yaxis_title="Revenue per order")
st.plotly_chart(scatter, use_container_width=True)

st.markdown("### Recommended Focus")
insight_cols = st.columns(3)
for index, insight in enumerate(generate_business_insights(filtered)[:6]):
    with insight_cols[index % 3]:
        st.success(insight)

st.markdown("### Product Ranking")
st.dataframe(
    format_columns(product_summary, money_columns=["revenue", "avg_order_value"]),
    use_container_width=True,
    hide_index=True,
)
