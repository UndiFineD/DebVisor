"""
Centralized Configuration Management for DebVisor.

Uses Pydantic Settings to load configuration from environment variables,
.env files, and secrets. Provides validation and type safety.
"""

import os
from typing import List, Optional, Union, Dict, Any
from pydantic import Field, PostgresDsn, RedisDsn, AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings."""

    # General
    ENVIRONMENT: str = Field("production", env="FLASK_ENV")
    DEBUG: bool = Field(False, env="FLASK_DEBUG")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    SERVICE_NAME: str = Field("debvisor", env="DEBVISOR_SERVICE_NAME")

    # Database
    DATABASE_URL: str = Field("sqlite:///debvisor.db", env="DATABASE_URL")
    DB_POOL_SIZE: int = Field(20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(10, env="DB_MAX_OVERFLOW")
    DB_POOL_TIMEOUT: int = Field(30, env="DB_POOL_TIMEOUT")
    DB_POOL_RECYCLE: int = Field(3600, env="DB_POOL_RECYCLE")

    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field("json", env="LOG_FORMAT")

    # Security
    CORS_ORIGINS: List[str] = Field(["*"], env="CORS_ORIGINS")
    JWT_SECRET_KEY: Optional[str] = Field(None, env="JWT_SECRET_KEY")
    
    # Services
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    KAFKA_BOOTSTRAP_SERVERS: Optional[str] = Field(None, env="KAFKA_BOOTSTRAP_SERVERS")
    
    # OpenTelemetry
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = Field(None, env="OTEL_EXPORTER_OTLP_ENDPOINT")

    # RPC Service
    RPC_HOST: str = Field("127.0.0.1", env="RPC_HOST")
    RPC_PORT: int = Field(7443, env="RPC_PORT")
    RPC_CERT_FILE: str = Field("/etc/debvisor/certs/rpc.crt", env="RPC_CERT_FILE")
    RPC_KEY_FILE: str = Field("/etc/debvisor/certs/rpc.key", env="RPC_KEY_FILE")
    RPC_CA_FILE: str = Field("/etc/debvisor/certs/ca.crt", env="RPC_CA_FILE")

    # Scheduler
    SCHEDULER_CONFIG_DIR: str = Field("/etc/debvisor/scheduler", env="SCHEDULER_CONFIG_DIR")
    SCHEDULER_MAX_WORKERS: int = Field(10, env="SCHEDULER_MAX_WORKERS")

    # Anomaly Detection
    ANOMALY_CONFIG_DIR: str = Field("/etc/debvisor/anomaly", env="ANOMALY_CONFIG_DIR")
    ANOMALY_BASELINE_WINDOW: int = Field(604800, env="ANOMALY_BASELINE_WINDOW")
    ANOMALY_Z_SCORE_THRESHOLD: float = Field(3.0, env="ANOMALY_Z_SCORE_THRESHOLD")
    ANOMALY_CONFIDENCE_THRESHOLD: float = Field(0.65, env="ANOMALY_CONFIDENCE_THRESHOLD")
    ANOMALY_MAX_HISTORY: int = Field(10000, env="ANOMALY_MAX_HISTORY")

    # Multi-Region
    MULTIREGION_CONFIG_DIR: str = Field("/etc/debvisor/regions", env="MULTIREGION_CONFIG_DIR")

    # Licensing
    LICENSE_CACHE_PATH: str = Field("/var/lib/debvisor/license.cache", env="LICENSE_CACHE_PATH")
    LICENSE_PORTAL_URL: str = Field("https://licensing.debvisor.io/api/v1", env="LICENSE_PORTAL_URL")
    LICENSE_API_KEY: Optional[str] = Field(None, env="LICENSE_API_KEY")
    LICENSE_HEARTBEAT_INTERVAL: int = Field(300, env="LICENSE_HEARTBEAT_INTERVAL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @validator("SECRET_KEY", pre=True, always=True)
    def validate_secret_key(cls, v, values):
        if not v and values.get("ENVIRONMENT") == "production":
            raise ValueError("SECRET_KEY must be set in production environment")
        if not v:
            import secrets
            return secrets.token_hex(32)
        return v

# Global settings instance
try:
    settings = Settings()
except Exception as e:
    # In case of validation error (e.g. missing SECRET_KEY in prod), print and re-raise
    print(f"Configuration Error: {e}")
    # For development convenience, we might want to allow partial loading or defaults,
    # but for now, let's be strict about validity.
    if os.getenv("FLASK_ENV") != "production":
        # Fallback for dev/test if .env is missing
        print("Warning: Failed to load settings, using defaults/mock for development.")
        class DevSettings(Settings):
            SECRET_KEY: str = "dev-secret-key"
        settings = DevSettings()
    else:
        raise
