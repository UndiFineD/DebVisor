#!/usr/bin/env python3
"""
Audit Log Encryption for DebVisor.

Provides field-level encryption for sensitive audit log data:
- AES-256-GCM encryption for audit records
- Key rotation support
- Searchable encrypted fields
- Compliance with data protection regulations

Author: DebVisor Team
Date: November 28, 2025
"""

import base64
import hashlib
import json
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================


class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms."""

    AES_256_GCM = "AES-256-GCM"
    AES_256_CBC = "AES-256-CBC"
    CHACHA20_POLY1305 = "ChaCha20-Poly1305"


class KeyStatus(Enum):
    """Encryption key status."""

    ACTIVE = "active"
    ROTATED = "rotated"
    DISABLED = "disabled"
    DESTROYED = "destroyed"


class SensitivityLevel(Enum):
    """Data sensitivity levels."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PII = "pii"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class EncryptionKey:
    """Encryption key metadata."""

    key_id: str
    algorithm: EncryptionAlgorithm
    status: KeyStatus
    created_at: datetime
    rotated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    version: int = 1

    # Key material (should be stored securely in production)
    key_material: bytes = field(
        default_factory=lambda: secrets.token_bytes(32), repr=False
    )

    @property
    def is_active(self) -> bool:
        """Check if key is active."""
        if self.status != KeyStatus.ACTIVE:
            return False
        if self.expires_at and datetime.now(timezone.utc) > self.expires_at:
            return False
        return True


@dataclass
class EncryptedField:
    """Encrypted field container."""

    ciphertext: bytes
    nonce: bytes
    tag: bytes
    key_id: str
    algorithm: str
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "ct": base64.b64encode(self.ciphertext).decode(),
            "nonce": base64.b64encode(self.nonce).decode(),
            "tag": base64.b64encode(self.tag).decode(),
            "kid": self.key_id,
            "alg": self.algorithm,
            "v": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptedField":
        """Create from dictionary."""
        return cls(
            ciphertext=base64.b64decode(data["ct"]),
            nonce=base64.b64decode(data["nonce"]),
            tag=base64.b64decode(data["tag"]),
            key_id=data["kid"],
            algorithm=data["alg"],
            version=data.get("v", 1),
        )


@dataclass
class AuditLogEntry:
    """Audit log entry with encryption support."""

    id: str
    timestamp: datetime
    action: str
    actor_id: str
    resource_type: str
    resource_id: str

    # Potentially sensitive fields
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    # Metadata
    sensitivity: SensitivityLevel = SensitivityLevel.INTERNAL
    encrypted_fields: Set[str] = field(default_factory=set)

    # Searchable hashes for encrypted fields
    search_hashes: Dict[str, str] = field(default_factory=dict)


# =============================================================================
# Field Encryption
# =============================================================================


class FieldEncryptor:
    """
    Field-level encryption for audit logs.

    Uses AES-256-GCM for authenticated encryption with
    support for key rotation and searchable encryption.
    """

    # Fields that should always be encrypted
    SENSITIVE_FIELDS = {
        "ip_address",
        "user_agent",
        "email",
        "phone",
        "ssn",
        "account_number",
        "credit_card",
        "address",
        "name",
        "date_of_birth",
        "password_hash",
        "api_key",
    }

    def __init__(
        self,
        master_key: Optional[bytes] = None,
        algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM,
    ):
        """
        Initialize encryptor.

        Args:
            master_key: Master encryption key (32 bytes for AES-256)
            algorithm: Encryption algorithm to use
        """
        self.algorithm = algorithm
        self._keys: Dict[str, EncryptionKey] = {}
        self._active_key_id: Optional[str] = None

        # Initialize with master key
        if master_key:
            self._initialize_key(master_key)
        else:
            self._initialize_key(secrets.token_bytes(32))

        logger.info(f"Field encryptor initialized with {algorithm.value}")

    def _initialize_key(self, key_material: bytes) -> str:
        """Initialize a new encryption key."""
        key_id = secrets.token_hex(8)
        key = EncryptionKey(
            key_id=key_id,
            algorithm=self.algorithm,
            status=KeyStatus.ACTIVE,
            created_at=datetime.now(timezone.utc),
            key_material=key_material,
        )
        self._keys[key_id] = key
        self._active_key_id = key_id
        return key_id

    def rotate_key(self) -> str:
        """
        Rotate to a new encryption key.

        Returns:
            New key ID
        """
        # Mark current key as rotated
        if self._active_key_id:
            old_key = self._keys[self._active_key_id]
            old_key.status = KeyStatus.ROTATED
            old_key.rotated_at = datetime.now(timezone.utc)

        # Create new key
        new_key_material = secrets.token_bytes(32)
        new_key_id = self._initialize_key(new_key_material)

        logger.info(f"Key rotated: {self._active_key_id} -> {new_key_id}")
        return new_key_id

    def encrypt(
        self, plaintext: Union[str, bytes], key_id: Optional[str] = None
    ) -> EncryptedField:
        """
        Encrypt a field value.

        Args:
            plaintext: Value to encrypt
            key_id: Optional specific key to use

        Returns:
            EncryptedField container
        """
        key_id = key_id or self._active_key_id
        if not key_id or key_id not in self._keys:
            raise ValueError("No active encryption key")

        key = self._keys[key_id]

        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")

        if self.algorithm == EncryptionAlgorithm.AES_256_GCM:
            return self._encrypt_aes_gcm(plaintext, key)
        else:
            raise NotImplementedError(f"Algorithm {self.algorithm} not implemented")

    def decrypt(self, encrypted: EncryptedField) -> bytes:
        """
        Decrypt a field value.

        Args:
            encrypted: EncryptedField container

        Returns:
            Decrypted bytes
        """
        key = self._keys.get(encrypted.key_id)
        if not key:
            raise ValueError(f"Key {encrypted.key_id} not found")

        if key.status == KeyStatus.DESTROYED:
            raise ValueError(f"Key {encrypted.key_id} has been destroyed")

        if encrypted.algorithm == EncryptionAlgorithm.AES_256_GCM.value:
            return self._decrypt_aes_gcm(encrypted, key)
        else:
            raise NotImplementedError(
                f"Algorithm {encrypted.algorithm} not implemented"
            )

    def _encrypt_aes_gcm(self, plaintext: bytes, key: EncryptionKey) -> EncryptedField:
        """Encrypt using AES-256-GCM."""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM

        nonce = secrets.token_bytes(12)  # 96-bit nonce for GCM
        aesgcm = AESGCM(key.key_material)

        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        # GCM appends tag to ciphertext
        actual_ciphertext = ciphertext[:-16]
        tag = ciphertext[-16:]

        return EncryptedField(
            ciphertext=actual_ciphertext,
            nonce=nonce,
            tag=tag,
            key_id=key.key_id,
            algorithm=EncryptionAlgorithm.AES_256_GCM.value,
            version=key.version,
        )

    def _decrypt_aes_gcm(self, encrypted: EncryptedField, key: EncryptionKey) -> bytes:
        """Decrypt using AES-256-GCM."""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM

        aesgcm = AESGCM(key.key_material)

        # Reconstruct ciphertext with tag
        ciphertext_with_tag = encrypted.ciphertext + encrypted.tag

        return aesgcm.decrypt(encrypted.nonce, ciphertext_with_tag, None)

    def create_search_hash(self, value: str, salt: Optional[bytes] = None) -> str:
        """
        Create a searchable hash for encrypted data.

        Uses HMAC-SHA256 for deterministic hashing that allows
        searching without decryption.

        Args:
            value: Value to hash
            salt: Optional salt (should be consistent for searchability)

        Returns:
            Base64-encoded hash
        """
        import hmac

        if salt is None:
            # Use key material as salt for deterministic hashing
            key = self._keys.get(self._active_key_id) if self._active_key_id else None
            salt = key.key_material if key else b""

        # Normalize value
        normalized = value.lower().strip()

        # Create HMAC
        h = hmac.new(salt, normalized.encode("utf-8"), hashlib.sha256)
        return base64.b64encode(h.digest()).decode()

    def is_sensitive_field(self, field_name: str) -> bool:
        """Check if a field should be encrypted."""
        return field_name.lower() in self.SENSITIVE_FIELDS


# =============================================================================
# Encrypted Audit Logger
# =============================================================================


class EncryptedAuditLogger:
    """
    Audit logger with field-level encryption.

    Features:
    - Automatic encryption of sensitive fields
    - Searchable encryption for queries
    - Key rotation support
    - Compliance-ready audit trails
    """

    def __init__(
        self,
        encryptor: Optional[FieldEncryptor] = None,
        storage_backend: Optional[Any] = None,
    ):
        """
        Initialize encrypted audit logger.

        Args:
            encryptor: Field encryptor instance
            storage_backend: Optional storage backend
        """
        self.encryptor = encryptor or FieldEncryptor()
        self.storage = storage_backend
        self._log_buffer: List[AuditLogEntry] = []

        logger.info("Encrypted audit logger initialized")

    def log(
        self,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        sensitivity: SensitivityLevel = SensitivityLevel.INTERNAL,
        encrypt_fields: Optional[List[str]] = None,
    ) -> AuditLogEntry:
        """
        Log an audit event with encryption.

        Args:
            action: Action performed (e.g., "create", "update", "delete")
            actor_id: ID of the actor performing the action
            resource_type: Type of resource affected
            resource_id: ID of the affected resource
            details: Additional details (sensitive fields will be encrypted)
            ip_address: Client IP address
            user_agent: Client user agent
            sensitivity: Data sensitivity level
            encrypt_fields: Additional fields to encrypt

        Returns:
            AuditLogEntry with encrypted fields
        """
        entry_id = secrets.token_hex(16)
        timestamp = datetime.now(timezone.utc)

        # Determine fields to encrypt
        fields_to_encrypt = set(encrypt_fields or [])

        # Auto-detect sensitive fields in details
        encrypted_details = {}
        search_hashes = {}
        encrypted_field_names: Set[str] = set()

        if details:
            for key, value in details.items():
                if self.encryptor.is_sensitive_field(key) or key in fields_to_encrypt:
                    if value is not None:
                        str_value = str(value) if not isinstance(value, str) else value
                        encrypted = self.encryptor.encrypt(str_value)
                        encrypted_details[key] = encrypted.to_dict()
                        encrypted_field_names.add(key)

                        # Create searchable hash
                        search_hashes[key] = self.encryptor.create_search_hash(
                            str_value
                        )
                else:
                    encrypted_details[key] = value

        # Encrypt IP address if present
        encrypted_ip = None
        if ip_address:
            if sensitivity in (
                SensitivityLevel.CONFIDENTIAL,
                SensitivityLevel.RESTRICTED,
                SensitivityLevel.PII,
            ):
                encrypted = self.encryptor.encrypt(ip_address)
                encrypted_ip = json.dumps(encrypted.to_dict())
                encrypted_field_names.add("ip_address")
                search_hashes["ip_address"] = self.encryptor.create_search_hash(
                    ip_address
                )
            else:
                encrypted_ip = ip_address

        # Encrypt user agent if present
        encrypted_ua = None
        if user_agent:
            if sensitivity in (SensitivityLevel.RESTRICTED, SensitivityLevel.PII):
                encrypted = self.encryptor.encrypt(user_agent)
                encrypted_ua = json.dumps(encrypted.to_dict())
                encrypted_field_names.add("user_agent")
            else:
                encrypted_ua = user_agent

        entry = AuditLogEntry(
            id=entry_id,
            timestamp=timestamp,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=encrypted_details if encrypted_details else None,
            ip_address=encrypted_ip,
            user_agent=encrypted_ua,
            sensitivity=sensitivity,
            encrypted_fields=encrypted_field_names,
            search_hashes=search_hashes,
        )

        # Store entry
        self._store_entry(entry)

        logger.debug(
            f"Audit log entry created: {entry_id} (encrypted: {encrypted_field_names})"
        )

        return entry

    def _store_entry(self, entry: AuditLogEntry) -> None:
        """Store audit log entry."""
        self._log_buffer.append(entry)

        if self.storage:
            try:
                self.storage.store(self._entry_to_dict(entry))
            except Exception as e:
                logger.error(f"Failed to store audit entry: {e}")

    def _entry_to_dict(self, entry: AuditLogEntry) -> Dict[str, Any]:
        """Convert entry to dictionary for storage."""
        return {
            "id": entry.id,
            "timestamp": entry.timestamp.isoformat(),
            "action": entry.action,
            "actor_id": entry.actor_id,
            "resource_type": entry.resource_type,
            "resource_id": entry.resource_id,
            "details": entry.details,
            "ip_address": entry.ip_address,
            "user_agent": entry.user_agent,
            "sensitivity": entry.sensitivity.value,
            "encrypted_fields": list(entry.encrypted_fields),
            "search_hashes": entry.search_hashes,
        }

    def search_by_hash(
        self, field_name: str, value: str, limit: int = 100
    ) -> List[AuditLogEntry]:
        """
        Search audit logs by encrypted field value.

        Args:
            field_name: Name of the field to search
            value: Value to search for
            limit: Maximum results

        Returns:
            Matching audit log entries
        """
        search_hash = self.encryptor.create_search_hash(value)

        results = []
        for entry in self._log_buffer:
            if entry.search_hashes.get(field_name) == search_hash:
                results.append(entry)
                if len(results) >= limit:
                    break

        return results

    def decrypt_entry(self, entry: AuditLogEntry) -> Dict[str, Any]:
        """
        Decrypt all encrypted fields in an entry.

        Args:
            entry: Audit log entry to decrypt

        Returns:
            Decrypted entry as dictionary
        """
        result = self._entry_to_dict(entry)

        # Decrypt details
        if entry.details:
            decrypted_details = {}
            for key, value in entry.details.items():
                if (
                    key in entry.encrypted_fields
                    and isinstance(value, dict)
                    and "ct" in value
                ):
                    encrypted = EncryptedField.from_dict(value)
                    decrypted_details[key] = self.encryptor.decrypt(encrypted).decode(
                        "utf-8"
                    )
                else:
                    decrypted_details[key] = value
            result["details"] = decrypted_details

        # Decrypt IP address
        if entry.ip_address and "ip_address" in entry.encrypted_fields:
            try:
                encrypted_data = json.loads(entry.ip_address)
                encrypted = EncryptedField.from_dict(encrypted_data)
                result["ip_address"] = self.encryptor.decrypt(encrypted).decode("utf-8")
            except (json.JSONDecodeError, KeyError):
                pass

        # Decrypt user agent
        if entry.user_agent and "user_agent" in entry.encrypted_fields:
            try:
                encrypted_data = json.loads(entry.user_agent)
                encrypted = EncryptedField.from_dict(encrypted_data)
                result["user_agent"] = self.encryptor.decrypt(encrypted).decode("utf-8")
            except (json.JSONDecodeError, KeyError):
                pass

        return result

    def rotate_keys(self) -> str:
        """
        Rotate encryption keys.

        Note: Existing encrypted data remains readable with old keys.
        New entries will use the new key.

        Returns:
            New key ID
        """
        new_key_id = self.encryptor.rotate_key()
        logger.info(f"Audit log encryption keys rotated to: {new_key_id}")
        return new_key_id

    def get_recent_logs(
        self,
        limit: int = 100,
        action: Optional[str] = None,
        actor_id: Optional[str] = None,
        resource_type: Optional[str] = None,
    ) -> List[AuditLogEntry]:
        """
        Get recent audit logs with optional filtering.

        Args:
            limit: Maximum number of entries
            action: Filter by action
            actor_id: Filter by actor
            resource_type: Filter by resource type

        Returns:
            List of audit log entries
        """
        results = []

        for entry in reversed(self._log_buffer):
            if action and entry.action != action:
                continue
            if actor_id and entry.actor_id != actor_id:
                continue
            if resource_type and entry.resource_type != resource_type:
                continue

            results.append(entry)
            if len(results) >= limit:
                break

        return results

    def export_for_compliance(
        self, start_date: datetime, end_date: datetime, decrypt: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Export audit logs for compliance reporting.

        Args:
            start_date: Start of date range
            end_date: End of date range
            decrypt: Whether to decrypt sensitive fields

        Returns:
            List of audit log entries
        """
        results = []

        for entry in self._log_buffer:
            if start_date <= entry.timestamp <= end_date:
                if decrypt:
                    results.append(self.decrypt_entry(entry))
                else:
                    results.append(self._entry_to_dict(entry))

        return results


# =============================================================================
# Global Instance
# =============================================================================

_audit_logger: Optional[EncryptedAuditLogger] = None


def get_audit_logger() -> EncryptedAuditLogger:
    """Get global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = EncryptedAuditLogger()
    return _audit_logger


def configure_audit_logger(
    master_key: Optional[bytes] = None, storage_backend: Optional[Any] = None
) -> EncryptedAuditLogger:
    """
    Configure global audit logger.

    Args:
        master_key: Master encryption key
        storage_backend: Storage backend for persistence

    Returns:
        Configured EncryptedAuditLogger
    """
    global _audit_logger

    encryptor = FieldEncryptor(master_key=master_key)
    _audit_logger = EncryptedAuditLogger(
        encryptor=encryptor, storage_backend=storage_backend
    )

    return _audit_logger


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Initialize logger
    audit = configure_audit_logger()

    # Log some test events
    print("Creating audit log entries...")

    # Standard log
    entry1 = audit.log(
        action="login",
        actor_id="user-123",
        resource_type="session",
        resource_id="sess-456",
        details={"method": "password", "success": True},
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0...",
        sensitivity=SensitivityLevel.INTERNAL,
    )

    # PII log (auto-encrypts sensitive fields)
    entry2 = audit.log(
        action="update",
        actor_id="admin-001",
        resource_type="customer",
        resource_id="cust-789",
        details={
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "name": "John Doe",
            "account_number": "1234567890",
            "update_reason": "Customer request",
        },
        ip_address="10.0.0.50",
        sensitivity=SensitivityLevel.PII,
    )

    # Payment log
    entry3 = audit.log(
        action="payment",
        actor_id="user-456",
        resource_type="transaction",
        resource_id="txn-001",
        details={
            "amount": 1500.00,
            "credit_card": "4111111111111111",
            "method": "card",
        },
        ip_address="172.16.0.25",
        sensitivity=SensitivityLevel.RESTRICTED,
    )

    print(f"\nCreated {len(audit._log_buffer)} audit entries")
    print(f"Entry 1 encrypted fields: {entry1.encrypted_fields}")
    print(f"Entry 2 encrypted fields: {entry2.encrypted_fields}")
    print(f"Entry 3 encrypted fields: {entry3.encrypted_fields}")

    # Test search by hash
    print("\n" + "=" * 60)
    print("SEARCH BY ENCRYPTED FIELD:")
    print("=" * 60)

    results = audit.search_by_hash("email", "john.doe@example.com")
    print(f"Found {len(results)} entries with matching email")

    # Test decryption
    print("\n" + "=" * 60)
    print("DECRYPTED ENTRY:")
    print("=" * 60)

    decrypted = audit.decrypt_entry(entry2)
    print(json.dumps(decrypted, indent=2, default=str))

    # Test key rotation
    print("\n" + "=" * 60)
    print("KEY ROTATION:")
    print("=" * 60)

    new_key = audit.rotate_keys()
    print(f"New key ID: {new_key}")

    # Log new entry with rotated key
    entry4 = audit.log(
        action="view",
        actor_id="user-789",
        resource_type="report",
        resource_id="rpt-001",
        details={"report_type": "financial"},
        sensitivity=SensitivityLevel.CONFIDENTIAL,
    )

    # Both old and new entries should be decryptable
    print("\nDecrypting entry with old key:")
    print(json.dumps(audit.decrypt_entry(entry2), indent=2, default=str)[:200] + "...")

    print("\nDecrypting entry with new key:")
    print(json.dumps(audit.decrypt_entry(entry4), indent=2, default=str))
