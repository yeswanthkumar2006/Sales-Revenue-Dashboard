"""Chart Components Module - Enhanced with Light Theme & Better Representations."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, List


# Modern Color Palette for Light Theme
COLOR_PALETTE = {
    'primary': '#1e6dd5',
    'secondary': '#2e88e5',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'neutral': '#6b7280',
    'light': '#f3f4f6',
}

CHART_COLORS = ['#1e6dd5', '#2e88e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6']


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    subtitle: str = "",
    height: int = 400,
    show_grid: bool = True
) -> None:
    """Create enhanced interactive line chart with better labels and formatting."""
    fig = px.line(
        df, 
        x=x_col, 
        y=y_col, 
        title=title, 
        markers=True,
        template='plotly_white'
    )
    
    fig.update_traces(
        line=dict(color=COLOR_PALETTE['primary'], width=3),
        marker=dict(size=8, color=COLOR_PALETTE['primary'])
    )
    
    fig.update_layout(
        height=height,
        hovermode='x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        showlegend=False,
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    subtitle: str = "",
    height: int = 400,
    orientation: str = 'v',
    show_values: bool = True
) -> None:
    """Create enhanced bar chart with value labels for better readability."""
    if orientation == 'h':
        fig = px.bar(
            df, 
            x=y_col,
            y=x_col, 
            orientation='h',
            title=title,
            template='plotly_white'
        )
    else:
        fig = px.bar(
            df, 
            x=x_col, 
            y=y_col, 
            title=title,
            template='plotly_white'
        )
    
    fig.update_traces(
        marker=dict(
            color=COLOR_PALETTE['primary'],
            line=dict(color=COLOR_PALETTE['secondary'], width=1)
        ),
        text=df[y_col].apply(lambda x: f'${x:,.0f}' if x > 1000 else f'{x:,.0f}') if show_values else None,
        textposition='outside' if orientation == 'h' else 'outside'
    )
    
    fig.update_layout(
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=x_col.replace('_', ' ').title() if orientation == 'v' else y_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title() if orientation == 'v' else x_col.replace('_', ' ').title(),
        showlegend=False,
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
        hovermode='closest'
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_pie_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str = "",
    subtitle: str = "",
    height: int = 400,
    show_percentages: bool = True
) -> None:
    """Create enhanced pie chart with better labels and percentages."""
    fig = px.pie(
        df, 
        names=names_col, 
        values=values_col, 
        title=title,
        color_discrete_sequence=CHART_COLORS,
        template='plotly_white'
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent' if show_percentages else 'label',
        hovertemplate='<b>%{label}</b><br>Value: %{value:,}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=height,
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=50, r=150, t=80 if subtitle else 50, b=50),
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: str = "",
    subtitle: str = "",
    height: int = 400
) -> None:
    """Create scatter plot with optional size and color dimensions."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=title,
        hover_data=df.columns.tolist(),
        template='plotly_white',
        color_discrete_sequence=CHART_COLORS
    )
    
    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(color='white', width=1),
            opacity=0.7
        )
    )
    
    fig.update_layout(
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        hovermode='closest',
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_heatmap(
    df: pd.DataFrame,
    title: str = "",
    subtitle: str = "",
    height: int = 400
) -> None:
    """Create correlation heatmap with improved colors."""
    numeric_df = df.select_dtypes(include=["number"])
    corr_matrix = numeric_df.corr()
    
    fig = px.imshow(
        corr_matrix, 
        text_auto='.2f', 
        title=title, 
        color_continuous_scale='RdBu_r',
        template='plotly_white',
        aspect='auto'
    )
    
    fig.update_layout(
        height=height,
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        margin=dict(l=100, r=100, t=80 if subtitle else 50, b=50),
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_histogram(
    df: pd.DataFrame,
    col: str,
    title: str = "",
    subtitle: str = "",
    nbins: int = 30,
    height: int = 400
) -> None:
    """Create histogram with better distribution visualization."""
    fig = px.histogram(
        df, 
        x=col, 
        nbins=nbins, 
        title=title,
        template='plotly_white'
    )
    
    fig.update_traces(
        marker=dict(
            color=COLOR_PALETTE['primary'],
            line=dict(color=COLOR_PALETTE['secondary'], width=1)
        )
    )
    
    fig.update_layout(
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=col.replace('_', ' ').title(),
        yaxis_title='Frequency (Count)',
        showlegend=False,
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
        hovermode='x unified'
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_box_plot(
    df: pd.DataFrame,
    x_col: Optional[str],
    y_col: str,
    title: str = "",
    subtitle: str = "",
    height: int = 400
) -> None:
    """Create box plot showing distribution and outliers."""
    fig = px.box(
        df, 
        x=x_col, 
        y=y_col, 
        title=title,
        template='plotly_white',
        color_discrete_sequence=CHART_COLORS
    )
    
    fig.update_traces(
        marker=dict(opacity=0.6),
        line=dict(width=2)
    )
    
    fig.update_layout(
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=x_col.replace('_', ' ').title() if x_col else None,
        yaxis_title=y_col.replace('_', ' ').title(),
        showlegend=False,
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
        hovermode='closest'
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def create_multi_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = "",
    subtitle: str = "",
    height: int = 400
) -> None:
    """Create multi-series bar chart for comparing multiple metrics."""
    fig = go.Figure()
    
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            name=y_col.replace('_', ' ').title(),
            marker=dict(color=CHART_COLORS[i % len(CHART_COLORS)])
        ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial, sans-serif", size=11, color=COLOR_PALETTE['neutral']),
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title='Value',
        barmode='group',
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80 if subtitle else 50, b=50),
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            showarrow=False,
            font=dict(size=12, color=COLOR_PALETTE['neutral']),
            xanchor='left'
        )
    
    st.plotly_chart(fig, use_container_width=True)
