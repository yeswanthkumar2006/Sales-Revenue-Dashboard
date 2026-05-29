"""Sample Data Generator Module."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional


def generate_sample_data(rows: int = 10000, days_back: int = 365) -> pd.DataFrame:
    """Generate sample sales data for testing and development."""
    np.random.seed(42)
    
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
    products = {
        "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
        "Home": ["Lamp", "Chair", "Table", "Rug"],
        "Sports": ["Running Shoes", "Yoga Mat", "Dumbbells", "Bicycle"],
        "Books": ["Fiction Novel", "Self-Help", "Technical Guide", "Biography"]
    }
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    dates = [start_date + timedelta(days=int(x)) for x in np.random.randint(0, days_back, rows)]
    
    # Generate data
    data = {
        "date": dates,
        "customer_id": np.random.randint(1000, 5000, rows),
        "region": np.random.choice(regions, rows),
        "category": np.random.choice(categories, rows),
        "quantity": np.random.randint(1, 20, rows).astype(int),
        "price": np.random.uniform(10, 500, rows),
    }
    
    df = pd.DataFrame(data)
    
    # Add product based on category
    df["product_name"] = df["category"].apply(
        lambda x: np.random.choice(products.get(x, []))
    )
    
    # Calculate revenue
    df["revenue"] = df["quantity"] * df["price"]
    
    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)
    
    return df
