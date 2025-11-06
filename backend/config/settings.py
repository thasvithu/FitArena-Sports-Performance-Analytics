"""
Configuration settings for FitArena platform
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "FitArena"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_FILE_EXTENSIONS: str = ".csv,.xlsx,.xls"
    UPLOAD_DIRECTORY: str = "./data/uploads"
    
    # ML Models
    MODEL_PATH: str = "./models/saved_models"
    MODEL_RETRAIN_INTERVAL_DAYS: int = 7
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/fitarena.log"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Data Processing
    BATCH_SIZE: int = 1000
    MAX_WORKERS: int = 4
    
    @field_validator('ALLOWED_ORIGINS')
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @field_validator('ALLOWED_FILE_EXTENSIONS')
    def parse_file_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()
