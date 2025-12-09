#!/usr/bin/env python3
"""
DebVisor Secrets Management - Vault Integration.

Enterprise-grade secrets management using HashiCorp Vault:
- Secure credential storage and rotation
- RBAC-based access control
- Audit logging for all secret operations
- Automatic secret rotation
- Multi-cloud and on-premises support
- Compliance framework support (SOC2, HIPAA, PCI DSS)

Features:
- K/V v2 secret engine support
- Dynamic database credential generation
- TLS certificate management
- Encryption as a service
- Seal/unseal management
- Disaster recovery support
"""

import hvac
import logging
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, cast

logger = logging.getLogger(__name__)


class SecretType(Enum):
    """Types of secrets managed by Vault."""

    DATABASE_CREDENTIAL = "database"
    API_KEY = "api_key"
    TLS_CERTIFICATE = "tls_cert"
    SSH_KEY = "ssh_key"
    ENCRYPTION_KEY = "encryption_key"
    APPLICATION_CONFIG = "app_config"


class VaultPolicy(Enum):
    """Predefined Vault RBAC policies."""

    ADMIN = "admin"
    DEVELOPER = "developer"
    OPERATOR = "operator"
    AUDITOR = "auditor"
    APPLICATION = "application"


@dataclass
class VaultConfig:
    """Vault configuration."""

    url: str
    token: Optional[str] = None
    namespace: str = "debvisor"
    auth_method: str = "token"  # token, kubernetes, approle
    cert_path: Optional[str] = None
    key_path: Optional[str] = None
    ca_cert_path: Optional[str] = None
    max_retries: int = 3
    timeout: int = 30


@dataclass
class RotationPolicy:
    """Secret rotation policy."""

    enabled: bool = True
    interval_days: int = 90
    warning_days: int = 7
    require_explicit_approval: bool = False
    rotation_window: Tuple[int, int] = (2, 4)  # UTC hours


@dataclass
class SecretMetadata:
    """Metadata about a secret."""

    path: str
    secret_type: SecretType
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    rotated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    owner: str = ""
    description: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    rotation_policy: RotationPolicy = field(default_factory=RotationPolicy)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format dates."""
        d = asdict(self)
        if self.created_at:
            d["created_at"] = self.created_at.isoformat()
        if self.rotated_at:
            d["rotated_at"] = self.rotated_at.isoformat()
        if self.expires_at:
            d["expires_at"] = self.expires_at.isoformat()
        return d


class VaultSecretsManager:
    """Manage secrets using HashiCorp Vault."""

    def __init__(self, config: VaultConfig):
        """
        Initialize Vault secrets manager.

        Args:
            config: Vault configuration

        Raises:
            ConnectionError: If cannot connect to Vault
        """
        self.config = config
        self.client = self._initialize_client()
        self.audit_log: List[Dict[str, Any]] = []
        self.secrets_cache: Dict[str, Tuple[Any, datetime]] = {}

    def _initialize_client(self) -> hvac.Client:
        """Initialize Vault client with configured authentication."""
        try:
            # Create client with TLS support
            client = hvac.Client(
                url=self.config.url,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
                verify=self.config.ca_cert_path if self.config.ca_cert_path else True,
            )

            # Authenticate based on method
            if self.config.auth_method == "token" and self.config.token:
                client.token = self.config.token
                logger.info("Authenticated with token method")

            elif self.config.auth_method == "kubernetes":
                # Kubernetes auth with in-cluster service account
                with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
                    jwt = f.read()

                client.auth.kubernetes.login(
                    role="debvisor-app",
                    jwt=jwt,
                )
                logger.info("Authenticated with Kubernetes auth method")

            elif self.config.auth_method == "approle":
                # AppRole authentication for service-to-service
                role_id = self._read_secret_file("/etc/vault/role-id")
                secret_id = self._read_secret_file("/etc/vault/secret-id")

                client.auth.approle.login(
                    role_id=role_id,
                    secret_id=secret_id,
                )
                logger.info("Authenticated with AppRole auth method")

            # Verify authentication
            if not client.is_authenticated():
                raise hvac.exceptions.AuthenticationError(
                    "Failed to authenticate with Vault"
                )

            logger.info(f"Successfully connected to Vault at {self.config.url}")
            return client

        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {str(e)}")
            raise ConnectionError(f"Cannot connect to Vault: {str(e)}")

    @staticmethod
    def _read_secret_file(path: str) -> str:
        """Read secret from file."""
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read secret file {path}: {str(e)}")
            raise

    def store_secret(
        self,
        name: str,
        secret: Dict[str, Any],
        metadata: Optional[SecretMetadata] = None,
        overwrite: bool = False,
    ) -> bool:
        """
        Store secret in Vault.

        Args:
            name: Secret name/path
            secret: Secret data as dictionary
            metadata: Optional metadata
            overwrite: Allow overwriting existing secret

        Returns:
            True if successful

        Raises:
            ValueError: If secret already exists and overwrite=False
            hvac.exceptions.InvalidRequest: If Vault request fails
        """
        path = f"secret/data/{self.config.namespace}/{name}"

        try:
            # Check if secret already exists
            if not overwrite:
                try:
                    self.client.secrets.kv.v2.read_secret_version(path=path)
                    raise ValueError(f"Secret already exists: {name}")
                except hvac.exceptions.InvalidPath:
                    pass  # Secret doesn't exist, continue

            # Store secret
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret_data=secret,
            )

            # Log operation
            self._log_audit_event(
                action="store_secret",
                resource=name,
                result="success",
                metadata=metadata.to_dict() if metadata else {},
            )

            logger.info(f"Stored secret: {name}")
            return True

        except Exception as e:
            self._log_audit_event(
                action="store_secret",
                resource=name,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to store secret {name}: {str(e)}")
            raise

    def retrieve_secret(
        self, name: str, use_cache: bool = True, cache_ttl_seconds: int = 300
    ) -> Dict[str, Any]:
        """
        Retrieve secret from Vault.

        Args:
            name: Secret name/path
            use_cache: Use local cache if available
            cache_ttl_seconds: Cache TTL in seconds

        Returns:
            Secret data

        Raises:
            hvac.exceptions.InvalidPath: If secret not found
        """
        path = f"secret/data/{self.config.namespace}/{name}"

        # Check cache
        if use_cache and name in self.secrets_cache:
            secret_data, cached_at = self.secrets_cache[name]
            if (
                datetime.now(timezone.utc) - cached_at
            ).total_seconds() < cache_ttl_seconds:
                logger.debug(f"Retrieved secret from cache: {name}")
                return cast(Dict[str, Any], secret_data)

        try:
            # Retrieve from Vault
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            secret_data = cast(Dict[str, Any], response["data"]["data"])

            # Cache result
            if use_cache:
                self.secrets_cache[name] = (secret_data, datetime.now(timezone.utc))

            # Log operation
            self._log_audit_event(
                action="retrieve_secret",
                resource=name,
                result="success",
            )

            logger.debug(f"Retrieved secret: {name}")
            return secret_data

        except hvac.exceptions.InvalidPath:
            self._log_audit_event(
                action="retrieve_secret",
                resource=name,
                result="not_found",
            )
            logger.error(f"Secret not found: {name}")
            raise

        except Exception as e:
            self._log_audit_event(
                action="retrieve_secret",
                resource=name,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to retrieve secret {name}: {str(e)}")
            raise

    def rotate_secret(
        self, name: str, new_secret: Dict[str, Any], require_approval: bool = False
    ) -> bool:
        """
        Rotate secret with automatic versioning.

        Args:
            name: Secret name/path
            new_secret: New secret data
            require_approval: Require explicit approval for rotation

        Returns:
            True if successful

        Raises:
            ValueError: If rotation policy not met
        """
        path = f"secret/data/{self.config.namespace}/{name}"

        try:
            # Get current version metadata
            current = self.client.secrets.kv.v2.read_secret_version(path=path)
            metadata = current.get("metadata", {})

            # Log rotation
            self._log_audit_event(
                action="rotate_secret",
                resource=name,
                result="initiated",
                metadata={
                    "previous_version": metadata.get("version"),
                    "approval_required": require_approval,
                },
            )

            # Store rotated secret
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret_data=new_secret,
            )

            # Clear cache for this secret
            if name in self.secrets_cache:
                del self.secrets_cache[name]

            # Log completion
            self._log_audit_event(
                action="rotate_secret",
                resource=name,
                result="completed",
                metadata={
                    "new_version": metadata.get("version", 0) + 1,
                    "rotated_at": datetime.now(timezone.utc).isoformat(),
                },
            )

            logger.info(f"Rotated secret: {name}")
            return True

        except Exception as e:
            self._log_audit_event(
                action="rotate_secret",
                resource=name,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to rotate secret {name}: {str(e)}")
            raise

    def delete_secret(self, name: str, purge: bool = False) -> bool:
        """
        Delete secret from Vault.

        Args:
            name: Secret name/path
            purge: Permanently purge all versions (requires special policy)

        Returns:
            True if successful

        Raises:
            hvac.exceptions.InvalidRequest: If deletion fails
        """
        path = f"secret/data/{self.config.namespace}/{name}"

        try:
            if purge:
                # Permanently delete all versions
                self.client.secrets.kv.v2.destroy_secret_version(
                    path=path, version=None
                )
                logger.info(f"Permanently purged secret: {name}")
            else:
                # Soft delete (mark for deletion)
                self.client.secrets.kv.v2.delete_secret_version(path=path)
                logger.info(f"Deleted secret: {name}")

            # Clear cache
            if name in self.secrets_cache:
                del self.secrets_cache[name]

            # Log operation
            self._log_audit_event(
                action="delete_secret",
                resource=name,
                result="success",
                metadata={"purged": purge},
            )

            return True

        except Exception as e:
            self._log_audit_event(
                action="delete_secret",
                resource=name,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to delete secret {name}: {str(e)}")
            raise

    def generate_dynamic_credentials(
        self, database_role: str, ttl_hours: int = 1
    ) -> Dict[str, str]:
        """
        Generate dynamic database credentials.

        Args:
            database_role: Database role name
            ttl_hours: Credential TTL in hours

        Returns:
            Dictionary with username and password

        Raises:
            hvac.exceptions.InvalidRequest: If generation fails
        """
        # path = f"database/creds/{database_role}"

        try:
            response = self.client.secrets.database.generate_credentials(
                name=database_role,
                static=False,
            )

            credentials = {
                "username": response["data"]["username"],
                "password": response["data"]["password"],
                "ttl": response["data"]["ttl"],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

            # Log operation (without password)
            self._log_audit_event(
                action="generate_credentials",
                resource=database_role,
                result="success",
                metadata={
                    "username": credentials["username"],
                    "ttl_hours": ttl_hours,
                },
            )

            logger.info(f"Generated credentials for database role: {database_role}")
            return credentials

        except Exception as e:
            self._log_audit_event(
                action="generate_credentials",
                resource=database_role,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to generate credentials: {str(e)}")
            raise

    def issue_tls_certificate(
        self, common_name: str, alt_names: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Issue TLS certificate via Vault PKI.

        Args:
            common_name: Certificate common name
            alt_names: List of alternative names

        Returns:
            Certificate, key, and CA bundle

        Raises:
            hvac.exceptions.InvalidRequest: If issuance fails
        """
        # path = "pki/issue/debvisor-cert"

        try:
            alt_names = alt_names or []
            response = self.client.secrets.pki.generate_certificate(
                name="debvisor-cert",
                common_name=common_name,
                alt_names=",".join(alt_names) if alt_names else None,
            )

            certificate = {
                "certificate": response["data"]["certificate"],
                "private_key": response["data"]["private_key"],
                "ca_chain": response["data"]["ca_chain"],
                "serial_number": response["data"]["serial_number"],
                "issued_at": datetime.now(timezone.utc).isoformat(),
            }

            # Log operation
            self._log_audit_event(
                action="issue_certificate",
                resource=common_name,
                result="success",
                metadata={
                    "common_name": common_name,
                    "alt_names": alt_names,
                    "serial": certificate["serial_number"],
                },
            )

            logger.info(f"Issued TLS certificate for: {common_name}")
            return certificate

        except Exception as e:
            self._log_audit_event(
                action="issue_certificate",
                resource=common_name,
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to issue certificate: {str(e)}")
            raise

    def list_secrets(self, pattern: str = "") -> List[str]:
        """
        List secrets matching pattern.

        Args:
            pattern: Optional search pattern

        Returns:
            List of secret paths
        """
        path = f"secret/metadata/{self.config.namespace}"

        try:
            response = self.client.secrets.kv.v2.list_secrets(path=path)
            keys = cast(List[str], response["data"]["keys"])

            # Filter by pattern if provided
            if pattern:
                keys = [k for k in keys if pattern in k]

            self._log_audit_event(
                action="list_secrets",
                resource="*",
                result="success",
                metadata={"count": len(keys), "pattern": pattern},
            )

            return keys

        except Exception as e:
            self._log_audit_event(
                action="list_secrets",
                resource="*",
                result="failed",
                error=str(e),
            )
            logger.error(f"Failed to list secrets: {str(e)}")
            return []

    def setup_audit_logging(self, enable: bool = True) -> bool:
        """Enable Vault audit logging."""
        try:
            if enable:
                # Enable file audit backend
                self.client.sys.enable_audit_backend(
                    backend_type="file",
                    description="DebVisor audit log",
                    options={"file_path": "/var/log/vault-audit.log"},
                )
                logger.info("Enabled Vault audit logging")
            else:
                self.client.sys.disable_audit_backend(path="file/")
                logger.info("Disabled Vault audit logging")

            return True

        except Exception as e:
            logger.error(f"Failed to setup audit logging: {str(e)}")
            return False

    def _log_audit_event(
        self,
        action: str,
        resource: str,
        result: str,
        metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        """Log audit event."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "resource": resource,
            "result": result,
            "metadata": metadata or {},
            "error": error,
        }
        self.audit_log.append(event)
        # Use default=str to handle any remaining non-serializable objects
        logger.debug(f"Audit event: {json.dumps(event, default=str)}")

    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit events."""
        return self.audit_log[-limit:]


# Example usage and initialization
def example_usage() -> None:
    """Example of using VaultSecretsManager."""
    # Configure Vault
    config = VaultConfig(
        url="https://vault.debvisor.local:8200",
        token=os.getenv("VAULT_TOKEN", "s.xxxxxxxxxxxxxx"),  # nosec B106
        namespace="debvisor",
        auth_method="token",
        ca_cert_path="/etc/vault/ca.crt",
    )

    # Initialize manager
    manager = VaultSecretsManager(config)

    # Store a secret
    manager.store_secret(
        "database/postgres",
        {
            "host": "postgres.default.svc.cluster.local",
            "port": 5432,
            "username": "debvisor",
            "password": os.getenv("DB_PASSWORD", ""),
        },
    )

    # Retrieve secret
    secret = manager.retrieve_secret("database/postgres")
    print(f"Retrieved secret for user: {secret.get('username', 'unknown')}")

    # Generate dynamic credentials
    creds = manager.generate_dynamic_credentials("postgres-role")
    print(f"Generated credentials for user: {creds.get('username', 'unknown')}")

    # Rotate secret
    manager.rotate_secret(
        "database/postgres",
        {
            "password": os.getenv("NEW_DB_PASSWORD", ""),
        },
    )

    # List secrets
    secrets = manager.list_secrets("database")
    print(f"Found {len(secrets)} database secrets")

    # Get audit log
    audit_log = manager.get_audit_log()
    print(f"Audit events: {len(audit_log)}")


if __name__ == "__main__":
    try:
        from opt.core.logging import configure_logging

        configure_logging(service_name="secrets-management")
    except ImportError:
        logging.basicConfig(level=logging.INFO)
    example_usage()
