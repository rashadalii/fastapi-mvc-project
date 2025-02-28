from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application configuration settings.
    
    Attributes:
        DATABASE_URL: MySQL database connection string
        SECRET_KEY: Secret key for JWT token generation and validation
        ALGORITHM: Algorithm used for JWT token encoding/decoding
        ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes
        CACHE_EXPIRY_SECONDS: Expiration time for cached data in seconds
    """
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/fastapi_db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CACHE_EXPIRY_SECONDS: int = 300  # 5 minutes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching for better performance.
    
    Returns:
        Settings: Application configuration settings
    """
    return Settings()