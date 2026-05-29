"""Tests for Data Processor Module."""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processor import DataProcessor


@pytest.fixture
def sample_df():
    """Create sample dataframe for testing."""
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=10),
        "revenue": [100, 200, 150, 300, 250, 400, 350, 500, 450, 600],
        "quantity": [1, 2, 1, 3, 2, 4, 3, 5, 4, 6],
        "customer_id": np.random.randint(1000, 2000, 10)
    })


def test_data_processor_initialization():
    """Test DataProcessor initialization."""
    processor = DataProcessor()
    assert processor is not None


def test_clean_data(sample_df):
    """Test data cleaning."""
    processor = DataProcessor()
    processor.load_data(sample_df)
    cleaned = processor.clean_data(sample_df)
    assert len(cleaned) > 0
    assert cleaned.isnull().sum().sum() == 0


def test_transform_data(sample_df):
    """Test data transformation."""
    processor = DataProcessor()
    processor.load_data(sample_df)
    transformed = processor.transform_data(sample_df)
    assert "avg_price" in transformed.columns


def test_aggregate_by_period(sample_df):
    """Test data aggregation."""
    processor = DataProcessor()
    aggregated = processor.aggregate_by_period(sample_df, period="D")
    assert len(aggregated) > 0


def test_get_summary_stats(sample_df):
    """Test summary statistics."""
    processor = DataProcessor()
    stats = processor.get_summary_stats(sample_df)
    assert "total_rows" in stats
    assert "total_revenue" in stats
