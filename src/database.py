"""Database Connection and Management Module."""

import logging
from typing import Optional, List, Any
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import pandas as pd
from src.config import AppConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, config: AppConfig):
        """Initialize database manager."""
        self.config = config
        self.engine = None
        self.SessionLocal = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize database engine."""
        try:
            self.engine = create_engine(
                self.config.database_url,
                poolclass=QueuePool,
                pool_size=self.config.db_pool_size,
                max_overflow=20,
                pool_recycle=self.config.db_pool_recycle,
                echo=self.config.debug,
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session context manager."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: dict = None) -> List[Any]:
        """Execute raw SQL query."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            raise
    
    def get_sales_data(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Get sales data as pandas DataFrame."""
        try:
            query = "SELECT * FROM sales"
            if limit:
                query += f" LIMIT {limit}"
            
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            logger.warning(f"Failed to get sales data: {str(e)}")
            return None
    
    def get_table_schema(self, table_name: str) -> dict:
        """Get table schema information."""
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            return {col["name"]: str(col["type"]) for col in columns}
        except Exception as e:
            logger.error(f"Failed to get schema: {str(e)}")
            return {}
    
    def health_check(self) -> bool:
        """Check database connection health."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
    
    def close(self):
        """Close database engine."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database engine closed")
