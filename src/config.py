"""Configuration Management Module."""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path

# Load environment variables
load_dotenv()


class AppConfig(BaseSettings):
    """Application configuration management."""
    
    # Application Settings
    app_name: str = Field(default="Sales Analytics Dashboard", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database Settings
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="sales_analytics", env="DB_NAME")
    db_user: str = Field(default="user", env="DB_USER")
    db_password: str = Field(default="password", env="DB_PASSWORD")
    db_pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    db_pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")
    
    # Redis Settings
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # Cache Settings
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # API Settings
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    # Security
    secret_key: str = Field(default="change-me-in-production", env="SECRET_KEY")
    jwt_secret: str = Field(default="change-me-in-production", env="JWT_SECRET")
    
    # Performance
    max_data_points: int = Field(default=100000, env="MAX_DATA_POINTS")
    
    class Settings:
        """Pydantic settings config."""
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() == "development"
