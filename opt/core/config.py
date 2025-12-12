# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Centralized Configuration Management for DebVisor.

Uses Pydantic Settings to load configuration from environment variables,
.env files, and secrets. Provides validation and type safety.
"""

import os
from typing import List, Optional, Tuple, Dict, Any
from pydantic import Field, validator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource

try:
    import hvac
    HAS_VAULT = True
except ImportError:
    HAS_VAULT = False


class VaultSettingsSource(PydanticBaseSettingsSource):
    """
    Custom Pydantic settings source to load configuration from HashiCorp Vault.

    Requires VAULT_ADDR and VAULT_TOKEN environment variables.
    Defaults to reading from 'secret/data/debvisor/config'.
    """
    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
    # Not used in __call__ based implementation but required by abstract base class in some versions
        return None, field_name, False

    def __call__(self) -> Dict[str, Any]:
        if not HAS_VAULT:
            return {}

        vault_addr = os.getenv("VAULT_ADDR")
        vault_token = os.getenv("VAULT_TOKEN")
        vault_path = os.getenv("VAULT_PATH", "debvisor/config")
        vault_mount = os.getenv("VAULT_MOUNT", "secret")

        if not vault_addr or not vault_token:
            return {}

        try:
            client = hvac.Client(url=vault_addr, token=vault_token)
            if not client.is_authenticated():
                return {}

            # Read from KV v2
            response = client.secrets.kv.v2.read_secret_version(
                path=vault_path, mount_point=vault_mount
            )

            if response and 'data' in response and 'data' in response['data']:
                return dict(response['data']['data'])

        except Exception as e:
        # Log to stderr but don't crash application startup
            print(f"Warning: Failed to load secrets from Vault: {e}")

        return {}


class Settings(BaseSettings):
    """Global application settings."""

    # General
    ENVIRONMENT: str = Field("production", validation_alias="FLASK_ENV")
    DEBUG: bool = Field(False, validation_alias="FLASK_DEBUG")
    SECRET_KEY: Optional[str] = Field(None, validation_alias="SECRET_KEY")
    SERVICE_NAME: str = Field("debvisor", validation_alias="DEBVISOR_SERVICE_NAME")

    # Database
    DATABASE_URL: str = Field("sqlite:///debvisor.db", validation_alias="DATABASE_URL")
    DB_POOL_SIZE: int = Field(20, validation_alias="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(10, validation_alias="DB_MAX_OVERFLOW")
    DB_POOL_TIMEOUT: int = Field(30, validation_alias="DB_POOL_TIMEOUT")
    DB_POOL_RECYCLE: int = Field(3600, validation_alias="DB_POOL_RECYCLE")

    # Logging
    LOG_LEVEL: str = Field("INFO", validation_alias="LOG_LEVEL")
    LOG_FORMAT: str = Field("json", validation_alias="LOG_FORMAT")

    # Security
    CORS_ORIGINS: List[str] = Field(["*"], validation_alias="CORS_ORIGINS")
    JWT_SECRET_KEY: Optional[str] = Field(None, validation_alias="JWT_SECRET_KEY")

    # Services
    REDIS_URL: str = Field("redis://localhost:6379/0", validation_alias="REDIS_URL")
    KAFKA_BOOTSTRAP_SERVERS: Optional[str] = Field(None, validation_alias="KAFKA_BOOTSTRAP_SERVERS")

    # OpenTelemetry
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = Field(
        None, validation_alias="OTEL_EXPORTER_OTLP_ENDPOINT"
    )

    # RPC Service
    RPC_HOST: str = Field("127.0.0.1", validation_alias="RPC_HOST")
    RPC_PORT: int = Field(7443, validation_alias="RPC_PORT")
    RPC_CERT_FILE: str = Field("/etc/debvisor/certs/rpc.crt", validation_alias="RPC_CERT_FILE")
    RPC_KEY_FILE: str = Field("/etc/debvisor/certs/rpc.key", validation_alias="RPC_KEY_FILE")
    RPC_CA_FILE: str = Field("/etc/debvisor/certs/ca.crt", validation_alias="RPC_CA_FILE")

    # Scheduler
    SCHEDULER_CONFIG_DIR: str = Field(
        "/etc/debvisor/scheduler", validation_alias="SCHEDULER_CONFIG_DIR"
    )
    SCHEDULER_MAX_WORKERS: int = Field(10, validation_alias="SCHEDULER_MAX_WORKERS")

    # Anomaly Detection
    ANOMALY_CONFIG_DIR: str = Field("/etc/debvisor/anomaly", validation_alias="ANOMALY_CONFIG_DIR")
    ANOMALY_BASELINE_WINDOW: int = Field(604800, validation_alias="ANOMALY_BASELINE_WINDOW")
    ANOMALY_Z_SCORE_THRESHOLD: float = Field(3.0, validation_alias="ANOMALY_Z_SCORE_THRESHOLD")
    ANOMALY_CONFIDENCE_THRESHOLD: float = Field(
        0.65, validation_alias="ANOMALY_CONFIDENCE_THRESHOLD"
    )
    ANOMALY_MAX_HISTORY: int = Field(10000, validation_alias="ANOMALY_MAX_HISTORY")

    # Multi-Region
    MULTIREGION_CONFIG_DIR: str = Field(
        "/etc/debvisor/regions", validation_alias="MULTIREGION_CONFIG_DIR"
    )

    # Licensing
    LICENSE_CACHE_PATH: str = Field(
        "/var/lib/debvisor/license.cache", validation_alias="LICENSE_CACHE_PATH"
    )
    LICENSE_PORTAL_URL: str = Field(
        "https://licensing.debvisor.io/api/v1", validation_alias="LICENSE_PORTAL_URL"
    )
    LICENSE_API_KEY: Optional[str] = Field(None, validation_alias="LICENSE_API_KEY")
    LICENSE_HEARTBEAT_INTERVAL: int = Field(300, validation_alias="LICENSE_HEARTBEAT_INTERVAL")

    # Rate Limiting
    RATELIMIT_STORAGE_URI: str = Field("memory://", validation_alias="RATELIMIT_STORAGE_URI")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @classmethod
    def load_validated_config(cls) -> "Settings":
        """
        Load and validate configuration.
        Exits the application if validation fails.
        """
        try:
            return cls()
        except Exception as e:
            import sys
            print(f"Configuration Error: {e}", file=sys.stderr)
            sys.exit(1)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            VaultSettingsSource(settings_cls),
            file_secret_settings,
        )

    @validator("SECRET_KEY", pre=True, always=True)
    def validate_secret_key(cls, v: Optional[str], values: Dict[str, Any]) -> str:
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
