"""Data Processing Pipeline Module."""

import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data cleaning, transformation, and aggregation."""
    
    def __init__(self):
        """Initialize data processor."""
        self.original_df = None
        self.processed_df = None
    
    def load_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Load and validate data."""
        self.original_df = df.copy()
        return self.original_df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data by removing nulls and duplicates."""
        try:
            logger.info("Starting data cleaning...")
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Handle missing values
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            
            # Remove rows with critical missing values
            critical_cols = ["customer_id", "revenue", "date"]
            df = df.dropna(subset=[col for col in critical_cols if col in df.columns])
            
            logger.info(f"Data cleaned: {len(df)} rows remaining")
            return df
        except Exception as e:
            logger.error(f"Data cleaning error: {str(e)}")
            raise
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform data for analysis."""
        try:
            df = df.copy()
            
            # Convert date columns
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            
            # Ensure numeric columns
            numeric_cols = ["revenue", "quantity", "price"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Create additional features
            if "revenue" in df.columns and "quantity" in df.columns:
                df["avg_price"] = df["revenue"] / df["quantity"].replace(0, 1)
            
            self.processed_df = df
            return df
        except Exception as e:
            logger.error(f"Data transformation error: {str(e)}")
            raise
    
    def aggregate_by_period(
        self, df: pd.DataFrame, period: str = "D"
    ) -> pd.DataFrame:
        """Aggregate data by time period."""
        if "date" not in df.columns:
            return df
        
        df = df.set_index("date")
        agg_dict = {col: "sum" for col in df.select_dtypes(include=[np.number]).columns}
        return df.resample(period).agg(agg_dict).reset_index()
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics."""
        stats = {
            "total_rows": len(df),
            "total_revenue": df["revenue"].sum() if "revenue" in df.columns else 0,
            "avg_revenue": df["revenue"].mean() if "revenue" in df.columns else 0,
            "date_range": {
                "start": str(df["date"].min()) if "date" in df.columns else None,
                "end": str(df["date"].max()) if "date" in df.columns else None,
            },
        }
        return stats
