"""Data Seeding Script."""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig
from src.database import DatabaseManager
from data.sample_data import generate_sample_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database(rows: int = 10000):
    """Seed database with sample data."""
    try:
        config = AppConfig()
        db = DatabaseManager(config)
        
        logger.info(f"Seeding database with {rows} sample records...")
        
        # Generate sample data
        df = generate_sample_data(rows=rows)
        
        # Insert data
        df.to_sql("sales", db.engine, if_exists="append", index=False)
        
        logger.info(f"✓ Database seeded with {len(df)} records!")
        
    except Exception as e:
        logger.error(f"✗ Data seeding failed: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed sales database")
    parser.add_argument("--rows", type=int, default=10000, help="Number of rows to seed")
    args = parser.parse_args()
    
    seed_database(rows=args.rows)
