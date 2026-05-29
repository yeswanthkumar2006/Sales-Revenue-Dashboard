"""KPI Card Components Module."""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any


def create_kpi_card(
    title: str,
    value: Any,
    metric_unit: str = "",
    delta: Optional[str] = None,
    delta_color: str = "normal",
    icon: str = "📊"
) -> None:
    """Create a KPI card component."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(
            label=title,
            value=f"{icon} {value}{metric_unit}",
            delta=delta,
            delta_color=delta_color
        )
    
    with col2:
        st.write("")


def create_kpi_grid(kpis: Dict[str, Dict[str, Any]], columns: int = 4) -> None:
    """Create a grid of KPI cards."""
    cols = st.columns(columns)
    
    for idx, (title, kpi_data) in enumerate(kpis.items()):
        with cols[idx % columns]:
            value = kpi_data.get("value", 0)
            unit = kpi_data.get("unit", "")
            delta = kpi_data.get("delta", None)
            icon = kpi_data.get("icon", "📊")
            
            st.metric(
                label=title,
                value=f"{value}{unit}",
                delta=delta
            )


def create_comparison_cards(
    current: float, previous: float, title: str = "Comparison"
) -> None:
    """Create comparison cards."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current", f"${current:,.2f}")
    
    with col2:
        st.metric("Previous", f"${previous:,.2f}")
    
    with col3:
        change = ((current - previous) / abs(previous)) * 100 if previous != 0 else 0
        st.metric("Change", f"{change:+.2f}%")
