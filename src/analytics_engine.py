"""AI and Analytics Engine Module."""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Provides analytics and predictive capabilities."""
    
    def __init__(self):
        """Initialize analytics engine."""
        self.models = {}
        self.scaler = StandardScaler()
    
    def calculate_growth_rate(
        self, values: List[float], periods: int = 1
    ) -> float:
        """Calculate growth rate."""
        if len(values) <= periods or periods < 1:
            return 0.0
        
        try:
            baseline = values[0] if periods == 1 else values[-(periods + 1)]
            pct_change = ((values[-1] - baseline) / abs(baseline)) * 100 if baseline != 0 else 0
            return round(pct_change, 2)
        except:
            return 0.0
    
    def forecast_revenue(
        self, historical_data: pd.DataFrame, periods: int = 30
    ) -> pd.DataFrame:
        """Forecast future revenue using linear regression."""
        try:
            if "date" not in historical_data.columns or "revenue" not in historical_data.columns:
                return None
            
            # Prepare data
            df = historical_data.sort_values("date").copy()
            df["days"] = (df["date"] - df["date"].min()).dt.days
            
            X = df[["days"]].values
            y = df["revenue"].values
            
            # Train model
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate forecast
            last_day = df["days"].max()
            future_days = np.array([[last_day + i] for i in range(1, periods + 1)])
            predictions = model.predict(future_days)
            
            # Create forecast dataframe
            last_date = df["date"].max()
            forecast_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
            
            forecast_df = pd.DataFrame({
                "date": forecast_dates,
                "forecast_revenue": predictions
            })
            
            return forecast_df
        except Exception as e:
            logger.error(f"Revenue forecast error: {str(e)}")
            return None
    
    def identify_anomalies(
        self, values: List[float], threshold: float = 2.0
    ) -> List[int]:
        """Identify anomalies using z-score."""
        try:
            if len(values) < 3:
                return []
            
            mean = np.mean(values)
            std = np.std(values)
            
            if std == 0:
                return []
            
            z_scores = np.abs((np.array(values) - mean) / std)
            anomaly_indices = np.where(z_scores > threshold)[0].tolist()
            
            return anomaly_indices
        except Exception as e:
            logger.error(f"Anomaly detection error: {str(e)}")
            return []
    
    def get_correlations(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """Calculate correlation matrix."""
        try:
            numeric_df = df.select_dtypes(include=[np.number])
            if columns:
                numeric_df = numeric_df[[col for col in columns if col in numeric_df.columns]]
            
            return numeric_df.corr()
        except Exception as e:
            logger.error(f"Correlation calculation error: {str(e)}")
            return None
    
    def generate_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate business insights from data."""
        insights = []
        
        try:
            if "revenue" in df.columns:
                total_revenue = df["revenue"].sum()
                insights.append(f"Total Revenue: ${total_revenue:,.2f}")
                
                # Growth insight
                if len(df) > 1:
                    recent_revenue = df["revenue"].tail(7).sum()
                    older_revenue = df["revenue"].iloc[-14:-7].sum() if len(df) >= 14 else recent_revenue
                    growth = ((recent_revenue - older_revenue) / abs(older_revenue)) * 100 if older_revenue != 0 else 0
                    insights.append(f"7-Day Growth: {growth:+.2f}%")
            
            if "customer_id" in df.columns:
                unique_customers = df["customer_id"].nunique()
                insights.append(f"Unique Customers: {unique_customers:,}")
            
            if "date" in df.columns:
                date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"
                insights.append(f"Date Range: {date_range}")
        
        except Exception as e:
            logger.error(f"Insight generation error: {str(e)}")
        
        return insights
