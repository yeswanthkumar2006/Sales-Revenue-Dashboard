"""Utility Functions Module."""

import logging
import hashlib
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from functools import wraps
import time

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def measure_execution_time(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper


def format_currency(value: float, decimal_places: int = 2) -> str:
    """Format value as currency."""
    return f"${value:,.{decimal_places}f}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """Format value as percentage."""
    return f"{value:.{decimal_places}f}%"


def format_large_number(value: int) -> str:
    """Format large numbers with K, M, B suffixes."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def validate_date_range(
    start_date: datetime, end_date: datetime, max_days: int = 365
) -> bool:
    """Validate date range."""
    delta = (end_date - start_date).days
    return 0 <= delta <= max_days


def get_date_range(days_back: int = 30) -> tuple:
    """Get date range for last N days."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """Safe division with default value."""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default


def batch_process(items: List[Any], batch_size: int = 100):
    """Generator to process items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def get_top_items(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Get top N items by column value."""
    return df.nlargest(n, column)


def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculate percentile value."""
    return np.percentile(data, percentile)


def generate_csv_filename(prefix: str = "export") -> str:
    """Generate unique CSV filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"


def serialize_to_json(obj: Any) -> str:
    """Serialize object to JSON."""
    return json.dumps(obj, default=str, indent=2)


def hash_value(value: str) -> str:
    """Generate hash of value."""
    return hashlib.sha256(value.encode()).hexdigest()
