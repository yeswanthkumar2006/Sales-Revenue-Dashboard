"""Filter Components Module."""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def create_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Create comprehensive filters for data."""
    st.sidebar.subheader("📋 Filters")
    
    filtered_df = df.copy()
    
    # Date range filter
    if "date" in filtered_df.columns:
        filtered_df["date"] = pd.to_datetime(filtered_df["date"])
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=filtered_df["date"].min().date()
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=filtered_df["date"].max().date()
            )
        
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date) &
            (filtered_df["date"].dt.date <= end_date)
        ]
    
    # Region filter
    if "region" in filtered_df.columns:
        regions = st.sidebar.multiselect(
            "Regions",
            options=filtered_df["region"].unique(),
            default=filtered_df["region"].unique()
        )
        if regions:
            filtered_df = filtered_df[filtered_df["region"].isin(regions)]
    
    # Category filter
    if "category" in filtered_df.columns:
        categories = st.sidebar.multiselect(
            "Categories",
            options=filtered_df["category"].unique(),
            default=filtered_df["category"].unique()
        )
        if categories:
            filtered_df = filtered_df[filtered_df["category"].isin(categories)]
    
    # Product filter
    if "product_name" in filtered_df.columns:
        products = st.sidebar.multiselect(
            "Products",
            options=filtered_df["product_name"].unique()
        )
        if products:
            filtered_df = filtered_df[filtered_df["product_name"].isin(products)]
    
    # Revenue range filter
    if "revenue" in filtered_df.columns:
        min_revenue, max_revenue = st.sidebar.slider(
            "Revenue Range",
            min_value=float(filtered_df["revenue"].min()),
            max_value=float(filtered_df["revenue"].max()),
            value=(float(filtered_df["revenue"].min()), float(filtered_df["revenue"].max()))
        )
        filtered_df = filtered_df[
            (filtered_df["revenue"] >= min_revenue) &
            (filtered_df["revenue"] <= max_revenue)
        ]
    
    # Clear filters button
    if st.sidebar.button("🔄 Clear All Filters"):
        st.rerun()
    
    return filtered_df
