"""Database Initialization Script."""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig
from src.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQL for creating tables
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    customer_id INTEGER NOT NULL,
    region VARCHAR(50),
    category VARCHAR(50),
    product_name VARCHAR(100),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region);
"""


def init_database():
    """Initialize database schema."""
    try:
        config = AppConfig()
        db = DatabaseManager(config)
        
        logger.info("Initializing database...")
        
        # Execute table creation
        with db.engine.connect() as conn:
            conn.execute(CREATE_TABLES_SQL)
            conn.commit()
        
        logger.info("✓ Database initialized successfully!")
        
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()
