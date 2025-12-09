#!/usr/bin/env python3
"""
Flask Application Configuration

Three configuration profiles:
- development: Debug enabled, easier error messages
- testing: In-memory database, CSRF disabled
- production: Secure defaults, HTTPS enforced

Includes CORS (Cross-Origin Resource Sharing) whitelist configuration
with flexible origin matching and credential support.
"""

import os
from datetime import datetime
from datetime import timedelta
from typing import List

# Import centralized settings
try:
    from opt.core.config import settings
    HAS_CENTRAL_CONFIG = True
except ImportError:
    HAS_CENTRAL_CONFIG = False


class CORSConfig:
    """CORS configuration and whitelist management."""

    # Default allowed origins by environment
    ALLOWED_ORIGINS = {
        "development": [
            "http://localhost:3000",
            "http://localhost:5000",
            "http://localhost:8000",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5000",
        ],
        "testing": [
            "http://localhost:3000",
            "http://localhost:5000",
        ],
        "production": [
            # MUST be configured via environment variables in production
        ],
    }

    # Allowed HTTP methods
    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

    # Allowed headers
    ALLOWED_HEADERS = [
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-Token",
    ]

    # Exposed headers
    EXPOSED_HEADERS = [
        "X-Total-Count",
        "X-Page-Count",
        "Content-Disposition",
    ]

    # Allow credentials (cookies, auth headers)
    ALLOW_CREDENTIALS = True

    # Max age of preflight cache (seconds)
    MAX_AGE = 3600

    @classmethod
    def get_allowed_origins(cls, env: str = "production") -> List[str]:
        """
        Get allowed origins for environment.

        Merges defaults with environment variable overrides.

        Args:
            env: Environment name ('development', 'testing', 'production')

        Returns:
            List of allowed origins
        """
        # Use centralized settings if available
        if HAS_CENTRAL_CONFIG and settings.CORS_ORIGINS:
            return settings.CORS_ORIGINS

        default_origins = cls.ALLOWED_ORIGINS.get(env, [])

Get additional origins from environment variable
        env_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
        additional = [o.strip() for o in env_origins.split(", ") if o.strip()]

        return default_origins + additional

    @classmethod
    def validate_origin(cls, origin: str, allowed_origins: List[str]) -> bool:
        """
        Validate if origin is in whitelist.

        Supports exact matching and wildcard patterns (*).

        Args:
            origin: Origin header value
            allowed_origins: List of allowed origins

        Returns:
            True if origin is allowed, False otherwise
        """
        if not origin:
            return False

        for allowed in allowed_origins:
            # Exact match
            if origin == allowed:
                return True

            # Wildcard matching for subdomains (e.g., *.example.com)
            if "*" in allowed:
                pattern = allowed.replace(".", r"\.").replace("*", ".+")
                import re

                if re.match(f"^{pattern}$", origin):
                    return True

        return False


class Config:
    """Base configuration shared by all profiles"""

    # Flask settings
    # Note: In production, SECRET_KEY is enforced by opt.core.config.Settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY and os.getenv("FLASK_ENV") != "production":
        SECRET_KEY = "dev-key-change-in-production"

    DEBUG = False
    TESTING = False

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_REFRESH_EACH_REQUEST = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:////var/lib/debvisor/panel/panel.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # RPC Service configuration
    RPC_HOST = os.getenv("RPC_HOST", "localhost")
    RPC_PORT = int(os.getenv("RPC_PORT", "7443"))
    RPC_CA_CERT = os.getenv("RPC_CA_CERT", "/etc/debvisor/panel/tls/ca.crt")
    RPC_CLIENT_CERT = os.getenv("RPC_CLIENT_CERT", "/etc/debvisor/panel/tls/client.crt")
    RPC_CLIENT_KEY = os.getenv("RPC_CLIENT_KEY", "/etc/debvisor/panel/tls/client.key")
    RPC_TIMEOUT = int(os.getenv("RPC_TIMEOUT", "30"))

    # TLS/HTTPS
    TLS_CERT = os.getenv("TLS_CERT", "/etc/debvisor/panel/tls/server.crt")
    TLS_KEY = os.getenv("TLS_KEY", "/etc/debvisor/panel/tls/server.key")

    # Logging
    LOG_DIR = os.getenv("LOG_DIR", "/var/log/debvisor")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RATELIMIT_DEFAULT = "100/hour"

    # CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

    # CORS configuration
    CORS_ALLOWED_ORIGINS = CORSConfig.get_allowed_origins()
    CORS_ALLOWED_METHODS = CORSConfig.ALLOWED_METHODS
    CORS_ALLOWED_HEADERS = CORSConfig.ALLOWED_HEADERS
    CORS_EXPOSED_HEADERS = CORSConfig.EXPOSED_HEADERS
    CORS_ALLOW_CREDENTIALS = CORSConfig.ALLOW_CREDENTIALS
    CORS_MAX_AGE = CORSConfig.MAX_AGE


class DevelopmentConfig(Config):
    """Development configuration with debug enabled"""

    DEBUG = False  # Disabled by default, enable via FLASK_DEBUG=1
    TESTING = False
    SQLALCHEMY_ECHO = True
    WTF_CSRF_SSL_STRICT = False  # Allow self-signed certs in dev
    CORS_ALLOWED_ORIGINS = CORSConfig.get_allowed_origins("development")


class TestingConfig(Config):
    """Testing configuration with in-memory database"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    CORS_ALLOWED_ORIGINS = CORSConfig.get_allowed_origins("testing")


class ProductionConfig(Config):
    """Production configuration with strict security"""

    DEBUG = False
    TESTING = False
    # In production, SECRET_KEY must be set via environment
    if not os.getenv("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set in production")
    CORS_ALLOWED_ORIGINS = CORSConfig.get_allowed_origins("production")


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": ProductionConfig,
}
