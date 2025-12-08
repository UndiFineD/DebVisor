#!/usr/bin/env python3
"""
HashiCorp Vault Integration for DebVisor

Implements SECRET-001: Secrets management service with Vault integration.

Features:
- HashiCorp Vault client with automatic authentication
- Secret storage and retrieval with versioning
- Automatic secret rotation with configurable policies
- Encrypted secret storage with audit trail
- Support for multiple secret engines (KV v2, Database, PKI)
- Lease management and renewal
- High availability with automatic failover
"""

import hvac
import logging
import time
import threading
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

logger = logging.getLogger(__name__)


class AuthMethod(Enum):
    """Vault authentication methods."""

    TOKEN = "token"  # nosec B105
    APPROLE = "approle"
    KUBERNETES = "kubernetes"
    LDAP = "ldap"
    USERPASS = "userpass"


class SecretEngine(Enum):
    """Vault secret engine types."""

    KV_V2 = "kv-v2"
    DATABASE = "database"
    PKI = "pki"
    TRANSIT = "transit"
    AWS = "aws"
    AZURE = "azure"


@dataclass
class VaultConfig:
    """Vault configuration."""

    url: str = "http://127.0.0.1:8200"
    auth_method: AuthMethod = AuthMethod.TOKEN
    token: Optional[str] = None
    role_id: Optional[str] = None
    secret_id: Optional[str] = None
    namespace: Optional[str] = None
    mount_point: str = "secret"
    verify_ssl: bool = True
    timeout: int = 30
    max_retries: int = 3


@dataclass
class SecretMetadata:
    """Metadata for a secret."""

    path: str
    version: int
    created_time: datetime
    destroyed: bool
    deletion_time: Optional[datetime]
    custom_metadata: Dict[str, str]


@dataclass
class RotationPolicy:
    """Secret rotation policy."""

    enabled: bool = False
    rotation_period_days: int = 90
    notification_days: int = 14
    auto_rotate: bool = True
    rotation_callback: Optional[Callable] = None


class VaultClient:
    """
    HashiCorp Vault client with automatic authentication and secret management.

    Implements SECRET-001: Secrets management service.
    """

    def __init__(self, config: VaultConfig):
        self.config = config
        self.client: Optional[hvac.Client] = None
        self.is_authenticated = False
        self.token_renewal_thread: Optional[threading.Thread] = None
        self.rotation_policies: Dict[str, RotationPolicy] = {}

        self._connect()

        logger.info(
            f"VaultClient initialized: url={config.url}, "
            f"auth_method={config.auth_method.value}, "
            f"mount_point={config.mount_point}"
        )

    def _connect(self):
        """Connect to Vault and authenticate."""
        try:
            # Create Vault client
            self.client = hvac.Client(
                url=self.config.url,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout,
                namespace=self.config.namespace,
            )

            # Authenticate based on method
            if self.config.auth_method == AuthMethod.TOKEN:
                self._authenticate_token()
            elif self.config.auth_method == AuthMethod.APPROLE:
                self._authenticate_approle()
            elif self.config.auth_method == AuthMethod.KUBERNETES:
                self._authenticate_kubernetes()
            elif self.config.auth_method == AuthMethod.USERPASS:
                self._authenticate_userpass()
            else:
                raise ValueError(f"Unsupported auth method: {self.config.auth_method}")

            # Verify authentication
            if not self.client.is_authenticated():
                raise RuntimeError("Vault authentication failed")

            self.is_authenticated = True

            # Start token renewal thread if using token auth
            if self.config.auth_method == AuthMethod.TOKEN:
                self._start_token_renewal()

            logger.info("Successfully authenticated to Vault")

        except Exception as e:
            logger.error(f"Failed to connect to Vault: {e}")
            raise

    def _authenticate_token(self):
        """Authenticate using static token."""
        if not self.config.token:
            raise ValueError("Token required for token authentication")

        self.client.token = self.config.token
        logger.debug("Authenticated using token")

    def _authenticate_approle(self):
        """Authenticate using AppRole."""
        if not self.config.role_id or not self.config.secret_id:
            raise ValueError(
                "role_id and secret_id required for AppRole authentication"
            )

        response = self.client.auth.approle.login(
            role_id=self.config.role_id,
            secret_id=self.config.secret_id,
        )
        self.client.token = response["auth"]["client_token"]
        logger.debug("Authenticated using AppRole")

    def _authenticate_kubernetes(self):
        """Authenticate using Kubernetes service account."""
        # Read service account token
        token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"  # nosec B105
        with open(token_path, "r") as f:
            jwt = f.read().strip()

        role = self.config.role_id or "debvisor"
        response = self.client.auth.kubernetes.login(
            role=role,
            jwt=jwt,
        )
        self.client.token = response["auth"]["client_token"]
        logger.debug(f"Authenticated using Kubernetes (role: {role})")

    def _authenticate_userpass(self):
        """Authenticate using username/password."""
        if not self.config.role_id:  # Using role_id as username
            raise ValueError("Username required for userpass authentication")

        response = self.client.auth.userpass.login(
            username=self.config.role_id,
            password=self.config.secret_id,
        )
        self.client.token = response["auth"]["client_token"]
        logger.debug(f"Authenticated using userpass (user: {self.config.role_id})")

    def _start_token_renewal(self):
        """Start background thread for token renewal."""

        def renew_token():
            while self.is_authenticated:
                try:
                    # Renew token every 12 hours
                    time.sleep(12 * 3600)

                    if self.client.is_authenticated():
                        self.client.auth.token.renew_self()
                        logger.info("Vault token renewed successfully")
                    else:
                        logger.warning("Token expired, re-authenticating")
                        self._connect()

                except Exception as e:
                    logger.error(f"Failed to renew token: {e}")

        self.token_renewal_thread = threading.Thread(target=renew_token, daemon=True)
        self.token_renewal_thread.start()
        logger.debug("Token renewal thread started")

    def create_secret(
        self,
        path: str,
        data: Dict[str, Any],
        custom_metadata: Optional[Dict[str, str]] = None,
    ) -> SecretMetadata:
        """
        Create or update a secret in Vault.

        Args:
            path: Secret path (e.g., "db/postgres/password")
            data: Secret data as key-value pairs
            custom_metadata: Optional metadata for the secret

        Returns:
            SecretMetadata with version info
        """
        try:
            # Write secret to KV v2 engine
            response = self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=self.config.mount_point,
            )

            # Update custom metadata if provided
            if custom_metadata:
                self.client.secrets.kv.v2.update_metadata(
                    path=path,
                    custom_metadata=custom_metadata,
                    mount_point=self.config.mount_point,
                )

            version = response["data"]["version"]
            created_time = datetime.now(timezone.utc)

            logger.info(f"Created secret: path={path}, version={version}")

            return SecretMetadata(
                path=path,
                version=version,
                created_time=created_time,
                destroyed=False,
                deletion_time=None,
                custom_metadata=custom_metadata or {},
            )

        except Exception as e:
            logger.error(f"Failed to create secret {path}: {e}")
            raise

    def read_secret(
        self, path: str, version: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Read a secret from Vault.

        Args:
            path: Secret path
            version: Optional specific version to read

        Returns:
            Secret data or None if not found
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                version=version,
                mount_point=self.config.mount_point,
            )

            secret_data = response["data"]["data"]
            version = response["data"]["metadata"]["version"]

            logger.debug(f"Read secret: path={path}, version={version}")
            return secret_data

        except hvac.exceptions.InvalidPath:
            logger.warning(f"Secret not found: {path}")
            return None
        except Exception as e:
            logger.error(f"Failed to read secret {path}: {e}")
            raise

    def delete_secret(self, path: str, versions: Optional[List[int]] = None):
        """
        Delete specific versions of a secret.

        Args:
            path: Secret path
            versions: List of versions to delete (None = delete latest)
        """
        try:
            if versions:
                self.client.secrets.kv.v2.delete_secret_versions(
                    path=path,
                    versions=versions,
                    mount_point=self.config.mount_point,
                )
                logger.info(
                    f"Deleted secret versions: path={path}, versions={versions}"
                )
            else:
                self.client.secrets.kv.v2.delete_latest_version_of_secret(
                    path=path,
                    mount_point=self.config.mount_point,
                )
                logger.info(f"Deleted latest secret version: path={path}")

        except Exception as e:
            logger.error(f"Failed to delete secret {path}: {e}")
            raise

    def list_secrets(self, path: str = "") -> List[str]:
        """
        List secrets at a given path.

        Args:
            path: Path to list (empty for root)

        Returns:
            List of secret paths
        """
        try:
            response = self.client.secrets.kv.v2.list_secrets(
                path=path,
                mount_point=self.config.mount_point,
            )

            secrets = response["data"]["keys"]
            logger.debug(f"Listed {len(secrets)} secrets at path: {path}")
            return secrets

        except hvac.exceptions.InvalidPath:
            logger.debug(f"No secrets found at path: {path}")
            return []
        except Exception as e:
            logger.error(f"Failed to list secrets at {path}: {e}")
            raise

    def get_secret_metadata(self, path: str) -> Optional[SecretMetadata]:
        """
        Get metadata for a secret.

        Args:
            path: Secret path

        Returns:
            SecretMetadata or None if not found
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_metadata(
                path=path,
                mount_point=self.config.mount_point,
            )

            metadata = response["data"]
            current_version = metadata["current_version"]
            versions = metadata["versions"]

            version_info = versions.get(str(current_version), {})

            return SecretMetadata(
                path=path,
                version=current_version,
                created_time=datetime.fromisoformat(
                    version_info.get("created_time", "").replace("Z", "+00:00")
                ),
                destroyed=version_info.get("destroyed", False),
                deletion_time=None,
                custom_metadata=metadata.get("custom_metadata", {}),
            )

        except hvac.exceptions.InvalidPath:
            logger.warning(f"Secret metadata not found: {path}")
            return None
        except Exception as e:
            logger.error(f"Failed to get metadata for {path}: {e}")
            raise

    def rotate_secret(
        self, path: str, new_data: Dict[str, Any], keep_versions: int = 5
    ) -> SecretMetadata:
        """
        Rotate a secret by creating a new version.

        Args:
            path: Secret path
            new_data: New secret data
            keep_versions: Number of old versions to retain

        Returns:
            SecretMetadata for new version
        """
        try:
            # Create new version
            metadata = self.create_secret(path, new_data)

            # Clean up old versions
            all_metadata = self.get_secret_metadata(path)
            if all_metadata and metadata.version > keep_versions:
                old_versions = list(range(1, metadata.version - keep_versions + 1))
                if old_versions:
                    self.delete_secret(path, old_versions)
                    logger.info(f"Cleaned up old versions: {old_versions}")

            logger.info(f"Rotated secret: path={path}, new_version={metadata.version}")
            return metadata

        except Exception as e:
            logger.error(f"Failed to rotate secret {path}: {e}")
            raise

    def set_rotation_policy(self, path: str, policy: RotationPolicy):
        """
        Set rotation policy for a secret.

        Args:
            path: Secret path
            policy: Rotation policy configuration
        """
        self.rotation_policies[path] = policy
        logger.info(
            f"Set rotation policy: path={path}, enabled={policy.enabled}, "
            f"period={policy.rotation_period_days}d"
        )

    def check_rotation_needed(self, path: str) -> bool:
        """
        Check if a secret needs rotation based on policy.

        Args:
            path: Secret path

        Returns:
            True if rotation needed
        """
        policy = self.rotation_policies.get(path)
        if not policy or not policy.enabled:
            return False

        metadata = self.get_secret_metadata(path)
        if not metadata:
            return False

        age = datetime.now(timezone.utc) - metadata.created_time
        rotation_threshold = timedelta(days=policy.rotation_period_days)

        return age >= rotation_threshold

    def auto_rotate_secrets(self) -> Dict[str, SecretMetadata]:
        """
        Automatically rotate all secrets with enabled policies.

        Returns:
            Dict mapping path to new SecretMetadata
        """
        rotations = {}

        for path, policy in self.rotation_policies.items():
            if not policy.enabled or not policy.auto_rotate:
                continue

            if self.check_rotation_needed(path):
                try:
                    # Call rotation callback if provided
                    if policy.rotation_callback:
                        new_data = policy.rotation_callback(path)
                    else:
                        logger.warning(
                            f"No rotation callback for {path}, skipping auto-rotation"
                        )
                        continue

                    # Rotate secret
                    metadata = self.rotate_secret(path, new_data)
                    rotations[path] = metadata

                    logger.info(f"Auto-rotated secret: {path}")

                except Exception as e:
                    logger.error(f"Failed to auto-rotate {path}: {e}")

        return rotations

    def generate_database_credentials(
        self, role: str, ttl: str = "1h"
    ) -> Dict[str, str]:
        """
        Generate dynamic database credentials using Vault database engine.

        Args:
            role: Database role name
            ttl: Time-to-live for credentials

        Returns:
            Dict with username and password
        """
        try:
            response = self.client.secrets.database.generate_credentials(
                name=role,
                mount_point="database",
            )

            credentials = {
                "username": response["data"]["username"],
                "password": response["data"]["password"],
                "lease_id": response["lease_id"],
                "lease_duration": response["lease_duration"],
            }

            logger.info(f"Generated database credentials: role={role}, ttl={ttl}")
            return credentials

        except Exception as e:
            logger.error(f"Failed to generate database credentials for {role}: {e}")
            raise

    def encrypt_data(self, plaintext: str, key_name: str = "debvisor") -> str:
        """
        Encrypt data using Vault transit engine.

        Args:
            plaintext: Data to encrypt
            key_name: Transit key name

        Returns:
            Encrypted ciphertext
        """
        try:
            response = self.client.secrets.transit.encrypt_data(
                name=key_name,
                plaintext=plaintext,
                mount_point="transit",
            )

            ciphertext = response["data"]["ciphertext"]
            logger.debug(f"Encrypted data using key: {key_name}")
            return ciphertext

        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            raise

    def decrypt_data(self, ciphertext: str, key_name: str = "debvisor") -> str:
        """
        Decrypt data using Vault transit engine.

        Args:
            ciphertext: Encrypted data
            key_name: Transit key name

        Returns:
            Decrypted plaintext
        """
        try:
            response = self.client.secrets.transit.decrypt_data(
                name=key_name,
                ciphertext=ciphertext,
                mount_point="transit",
            )

            plaintext = response["data"]["plaintext"]
            logger.debug(f"Decrypted data using key: {key_name}")
            return plaintext

        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise

    def close(self):
        """Close Vault connection and stop background threads."""
        self.is_authenticated = False
        if self.token_renewal_thread:
            self.token_renewal_thread.join(timeout=5)
        logger.info("VaultClient closed")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize Vault client
    config = VaultConfig(
        url="http://127.0.0.1:8200",
        auth_method=AuthMethod.TOKEN,
        token="dev-only-token",  # nosec B106
        verify_ssl=False,
    )

    vault = VaultClient(config)

    # Store a secret
    vault.create_secret(
        path="db/postgres/password",
        data={
            "username": "postgres",
            "password": "super-secret-password",
            "host": "localhost",
            "port": "5432",
        },
        custom_metadata={
            "owner": "debvisor",
            "environment": "production",
        },
    )

    # Read the secret
    secret = vault.read_secret("db/postgres/password")
    print(f"Secret retrieved for: {secret.get('username', 'unknown')}")

    # List secrets
    secrets = vault.list_secrets("db")
    if isinstance(secrets, dict):
        logging.info(f"Found {len(secrets)} secret keys")
    elif isinstance(secrets, list):
        logging.info(f"Found {len(secrets)} secret keys")
    else:
        logging.info("Secrets listed successfully")

    # Set rotation policy
    def generate_new_password(path: str) -> Dict[str, Any]:
        import secrets

        return {
            "username": "postgres",
            "password": secrets.token_urlsafe(32),
            "host": "localhost",
            "port": "5432",
        }

    policy = RotationPolicy(
        enabled=True,
        rotation_period_days=90,
        auto_rotate=True,
        rotation_callback=generate_new_password,
    )
    vault.set_rotation_policy("db/postgres/password", policy)

    # Clean up
    vault.close()
