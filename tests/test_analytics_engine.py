"""Tests for Analytics Engine Module."""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics_engine import AnalyticsEngine


@pytest.fixture
def sample_df():
    """Create sample dataframe for testing."""
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=10),
        "revenue": [100, 200, 150, 300, 250, 400, 350, 500, 450, 600],
        "quantity": [1, 2, 1, 3, 2, 4, 3, 5, 4, 6],
    })


def test_analytics_engine_initialization():
    """Test AnalyticsEngine initialization."""
    engine = AnalyticsEngine()
    assert engine is not None


def test_calculate_growth_rate():
    """Test growth rate calculation."""
    engine = AnalyticsEngine()
    values = [100, 150, 200]
    growth = engine.calculate_growth_rate(values)
    assert growth == 100.0


def test_identify_anomalies():
    """Test anomaly detection."""
    engine = AnalyticsEngine()
    values = [1, 2, 3, 4, 5, 100]  # 100 is anomaly
    anomalies = engine.identify_anomalies(values, threshold=2.0)
    assert len(anomalies) > 0


def test_get_correlations(sample_df):
    """Test correlation calculation."""
    engine = AnalyticsEngine()
    corr = engine.get_correlations(sample_df)
    assert corr is not None


def test_generate_insights(sample_df):
    """Test insight generation."""
    engine = AnalyticsEngine()
    insights = engine.generate_insights(sample_df)
    assert len(insights) > 0
