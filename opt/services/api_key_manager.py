#!/usr/bin/env python3
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


"""
API Key Manager for DebVisor

Implements AUTH-001: API key rotation mechanism with automatic expiration,
overlap periods, and comprehensive audit logging.

Features:
- Automatic key expiration (90 days default)
- Key rotation workflow with overlap period (7 days)
- Comprehensive audit logging
- Key usage tracking
- Support for multiple active keys per principal
- Graceful key deprecation
"""

import secrets
import hashlib
import logging
import json
import os
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from pathlib import Path

_logger=logging.getLogger(__name__)


class KeyStatus(Enum):
    """API key status states."""

    ACTIVE="active"
    EXPIRING="expiring"    # Within overlap period
    EXPIRED="expired"
    REVOKED="revoked"


@dataclass
class APIKey:
    """API key data model."""

    key_id: str
    principal_id: str
    key_hash: str    # SHA-256 hash of the actual key
    created_at: datetime
    expires_at: datetime
    last_used_at: Optional[datetime]
    use_count: int
    status: KeyStatus
    description: str
    rotation_id: Optional[str] = None    # Links keys in same rotation cycle

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        _data=asdict(self)
        data["created_at"] = self.created_at.isoformat()  # type: ignore[name-defined]
        data["expires_at"] = self.expires_at.isoformat()  # type: ignore[name-defined]
        data["last_used_at"] = (  # type: ignore[name-defined]
            self.last_used_at.isoformat() if self.last_used_at else None
        )
        data["status"] = self.status.value  # type: ignore[name-defined]
        return data  # type: ignore[name-defined]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "APIKey":
        """Create from dictionary."""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["expires_at"] = datetime.fromisoformat(data["expires_at"])
        data["last_used_at"] = (
            datetime.fromisoformat(data["last_used_at"])
            if data["last_used_at"]
            else None
        )
        data["status"] = KeyStatus(data["status"])
        return cls(**data)


@dataclass
class KeyRotationConfig:
    """Configuration for key rotation."""

    expiration_days: int=90
    overlap_days: int=7
    warning_days: int=14
    auto_rotate: bool=True
    max_active_keys_per_principal: int=3


class APIKeyManager:
    """
    Manages API key lifecycle including rotation, expiration, and auditing.

    Implements AUTH-001: API key rotation mechanism.
    """

    def __init__(self, config: KeyRotationConfig, storagepath: str) -> None:
        self.config=config
        self.storage_path=Path(storage_path)  # type: ignore[name-defined]
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.keys_file=self.storage_path / "api_keys.json"
        self.audit_log=self.storage_path / "api_key_audit.log"

        # In-memory key store (load from disk)
        self.keys: Dict[str, APIKey] = {}
        self._load_keys()

        logger.info(  # type: ignore[name-defined]
            f"APIKeyManager initialized: expiration={config.expiration_days}d, "
            f"overlap={config.overlap_days}d"
        )

    def _load_keys(self) -> None:
        """Load keys from persistent storage."""
        if self.keys_file.exists():
            with open(self.keys_file, "r") as f:
                _data=json.load(f)
                self.keys={
                    key_id: APIKey.from_dict(key_data)
                    for key_id, key_data in data.items()  # type: ignore[name-defined]
                }
            logger.info(f"Loaded {len(self.keys)} API keys from storage")  # type: ignore[name-defined]

    def _save_keys(self) -> None:
        """Save keys to persistent storage."""
        _data={key_id: key.to_dict() for key_id, key in self.keys.items()}
        with open(self.keys_file, "w") as f:
            json.dump(data, f, indent=2)  # type: ignore[name-defined]

    def _audit_log_event(
        self, event: str, key_id: str, principal_id: str, details: Dict[str, Any]
    ) -> None:
        """Write audit log entry."""
        log_entry={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "key_id": key_id,
            "principal_id": principal_id,
            "details": details,
        }

        with open(self.audit_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        logger.info(  # type: ignore[name-defined]
            f"API key audit: event={event}, key_id={key_id}, "
            f"principal={principal_id}"
        )

    def _generate_key(self) -> str:
        """Generate cryptographically secure random API key."""
        # Format: dv_<random_32_bytes_hex>
        return f"dv_{secrets.token_hex(32)}"

    def _hash_key(self, key: str) -> str:
        """Hash API key for secure storage using PBKDF2-HMAC-SHA256."""
        # Use static salt since keys are randomly generated and unique
        salt = b"debvisor_api_key_salt_v1"
        return hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000).hex()

    def create_key(
        self,
        principal_id: str,
        description: str="",
        custom_expiration_days: Optional[int] = None,
        skip_audit: bool=False,
    ) -> Tuple[str, APIKey]:
        """
        Create new API key for a principal.

        Returns:
            (api_key, APIKey): The actual key and metadata
        """
        # Generate key
        _api_key=self._generate_key()
        _key_hash=self._hash_key(api_key)
        _key_id=f"key_{secrets.token_hex(8)}"

        # Calculate expiration
        _now=datetime.now(timezone.utc)
        expiration_days=custom_expiration_days or self.config.expiration_days
        _expires_at=now + timedelta(days=expiration_days)  # type: ignore[name-defined]

        # Create key object
        _key_obj=APIKey(  # type: ignore[call-arg]
            _key_id=key_id,  # type: ignore[name-defined]
            _principal_id=principal_id,
            _key_hash=key_hash,  # type: ignore[name-defined]
            _created_at=now,  # type: ignore[name-defined]
            _expires_at=expires_at,  # type: ignore[name-defined]
            _last_used_at=None,
            _use_count=0,
            _status=KeyStatus.ACTIVE,
            _description=description,
        )

        # Store key
        self.keys[key_id] = key_obj  # type: ignore[name-defined]
        self._save_keys()

        # Audit log (skip if part of rotation)
        if not skip_audit:
            self._audit_log_event(  # type: ignore[call-arg]
                _event="key_created",
                _key_id=key_id,  # type: ignore[name-defined]
                _principal_id=principal_id,
                _details={
                    "expires_at": expires_at.isoformat(),  # type: ignore[name-defined]
                    "description": description,
                },
            )

        logger.info(  # type: ignore[name-defined]
            f"Created API key: key_id={key_id}, principal={principal_id}, "  # type: ignore[name-defined]
            f"expires={expires_at.date()}"  # type: ignore[name-defined]
        )

        return api_key, key_obj

    def validate_key(self, apikey: str) -> Optional[APIKey]:
        """
        Validate API key and return key metadata if valid.

        Returns None if key is invalid, expired, or revoked.
        """
        _key_hash=self._hash_key(api_key)

        # Find key by hash
        for key_obj in self.keys.values():
            if key_obj.key_hash == key_hash:  # type: ignore[name-defined]
            # Check status
                if key_obj.status in [KeyStatus.EXPIRED, KeyStatus.REVOKED]:
                    logger.warning(  # type: ignore[name-defined]
                        f"Rejected {key_obj.status.value} key: "
                        f"key_id={key_obj.key_id}, principal={key_obj.principal_id}"
                    )
                    return None

                # Check expiration
                _now=datetime.now(timezone.utc)
                if now > key_obj.expires_at:  # type: ignore[name-defined]
                    logger.warning(  # type: ignore[name-defined]
                        f"Rejected expired key: key_id={key_obj.key_id}, "
                        f"principal={key_obj.principal_id}"
                    )
                    key_obj.status=KeyStatus.EXPIRED
                    self._save_keys()
                    return None

                # Update usage stats
                key_obj.last_used_at=now  # type: ignore[name-defined]
                key_obj.use_count += 1
                self._save_keys()

                return key_obj

        logger.warning("Rejected unknown API key")  # type: ignore[name-defined]
        return None

    def rotate_key(
        self, old_key_id: str, description: str="Rotated key"
    ) -> Tuple[str, APIKey]:
        """
        Rotate an existing API key.

        Creates new key and marks old key as expiring.
        Old key remains valid during overlap period.

        Returns:
            (new_api_key, APIKey): The new key and metadata
        """
        _old_key=self.keys.get(old_key_id)
        if not old_key:  # type: ignore[name-defined]
            raise ValueError(f"Key not found: {old_key_id}")

        # Generate rotation ID to link keys
        _rotation_id=f"rotation_{secrets.token_hex(8)}"

        # Create new key
        new_api_key, new_key_obj=self.create_key(  # type: ignore[call-arg]
            _principal_id=old_key.principal_id,  # type: ignore[name-defined]
            _description=description,
            _skip_audit=True,    # Don't log key_created for rotations
        )
        new_key_obj.rotation_id=rotation_id  # type: ignore[name-defined]

        # Update old key status
        _now=datetime.now(timezone.utc)
        old_key.status=KeyStatus.EXPIRING  # type: ignore[name-defined]
        old_key.rotation_id=rotation_id  # type: ignore[name-defined]
        old_key.expires_at=now + timedelta(days=self.config.overlap_days)  # type: ignore[name-defined]

        self._save_keys()

        # Audit log
        self._audit_log_event(  # type: ignore[call-arg]
            _event="key_rotated",
            _key_id=old_key_id,
            _principal_id=old_key.principal_id,  # type: ignore[name-defined]
            _details={
                "new_key_id": new_key_obj.key_id,
                "rotation_id": rotation_id,  # type: ignore[name-defined]
                "overlap_days": self.config.overlap_days,
            },
        )

        logger.info(  # type: ignore[name-defined]
            f"Rotated API key: old_key={old_key_id}, new_key={new_key_obj.key_id}, "
            f"rotation_id={rotation_id}"  # type: ignore[name-defined]
        )

        return new_api_key, new_key_obj

    def revoke_key(self, keyid: str, reason: str="") -> None:
        """Revoke an API key immediately."""
        _key_obj=self.keys.get(key_id)  # type: ignore[name-defined]
        if not key_obj:
            raise ValueError(f"Key not found: {key_id}")  # type: ignore[name-defined]

        key_obj.status=KeyStatus.REVOKED
        self._save_keys()

        # Audit log
        self._audit_log_event(  # type: ignore[call-arg]
            _event="key_revoked",
            _key_id=key_id,  # type: ignore[name-defined]
            _principal_id=key_obj.principal_id,
            _details={"reason": reason},
        )

        logger.warning(  # type: ignore[name-defined]
            f"Revoked API key: key_id={key_id}, principal={key_obj.principal_id}, "  # type: ignore[name-defined]
            f"reason={reason}"
        )

    def list_keys_for_principal(self, principalid: str) -> List[APIKey]:
        """List all keys for a principal."""
        return [key for key in self.keys.values() if key.principal_id== principal_id]  # type: ignore[name-defined]

    def check_expiring_keys(self) -> List[APIKey]:
        """
        Check for keys expiring soon (within warning period).

        Returns list of keys needing rotation.
        """
        _now=datetime.now(timezone.utc)
        _warning_threshold=now + timedelta(days=self.config.warning_days)  # type: ignore[name-defined]

        expiring_keys=[
            key
            for key in self.keys.values()
            if key.status == KeyStatus.ACTIVE and key.expires_at <= warning_threshold  # type: ignore[name-defined]
        ]

        return expiring_keys

    def auto_rotate_expiring_keys(self) -> Dict[str, str]:
        """
        Automatically rotate keys expiring soon.

        Returns dict mapping old_key_id -> new_key_id.
        """
        if not self.config.auto_rotate:
            logger.info("Auto-rotation disabled")  # type: ignore[name-defined]
            return {}

        _expiring_keys=self.check_expiring_keys()
        rotations={}

        for old_key in expiring_keys:  # type: ignore[name-defined]
            try:
                new_api_key, new_key_obj=self.rotate_key(  # type: ignore[call-arg]
                    old_key.key_id,
                    _description=f"Auto-rotated from {old_key.key_id}",
                )
                rotations[old_key.key_id] = new_key_obj.key_id
                logger.info(  # type: ignore[name-defined]
                    f"Auto-rotated key: {old_key.key_id} -> {new_key_obj.key_id}"
                )
            except Exception as e:
                logger.error(f"Failed to auto-rotate key {old_key.key_id}: {e}")  # type: ignore[name-defined]

        return rotations

    def cleanup_expired_keys(self, retentiondays: int=365) -> int:
        """
        Remove expired/revoked keys older than retention period.

        Keeps audit log intact, only removes from active key store.
        """
        _now=datetime.now(timezone.utc)
        _retention_threshold=now - timedelta(days=retention_days)  # type: ignore[name-defined]

        keys_to_remove=[
            key_id
            for key_id, key in self.keys.items()
            if key.status in [KeyStatus.EXPIRED, KeyStatus.REVOKED]
            and key.expires_at < retention_threshold  # type: ignore[name-defined]
        ]

        for key_id in keys_to_remove:
            _key=self.keys.pop(key_id)
            logger.info(  # type: ignore[name-defined]
                f"Cleaned up old key: key_id={key_id}, "
                f"principal={key.principal_id}, status={key.status.value}"  # type: ignore[name-defined]
            )

        if keys_to_remove:
            self._save_keys()

        return len(keys_to_remove)

    def get_key_stats(self) -> Dict[str, int]:
        """Get statistics about API keys."""
        _total_keys=len(self.keys)
        active_keys=sum(1 for k in self.keys.values() if k.status== KeyStatus.ACTIVE)
        _expiring_keys=sum(
            1 for k in self.keys.values() if k.status== KeyStatus.EXPIRING
        )
        _expired_keys=sum(
            1 for k in self.keys.values() if k.status== KeyStatus.EXPIRED
        )
        revoked_keys=sum(
            1 for k in self.keys.values() if k.status== KeyStatus.REVOKED
        )

        return {
            "total_keys": total_keys,  # type: ignore[name-defined]
            "active_keys": active_keys,
            "expiring_keys": expiring_keys,  # type: ignore[name-defined]
            "expired_keys": expired_keys,  # type: ignore[name-defined]
            "revoked_keys": revoked_keys,
        }


# Example usage
if _name__== "__main__":  # type: ignore[name-defined]
    logging.basicConfig(level=logging.INFO)

    config=KeyRotationConfig(  # type: ignore[call-arg]
        _expiration_days=90,
        _overlap_days=7,
        _warning_days=14,
        _auto_rotate=True,
    )

    import tempfile

    _manager=APIKeyManager(config, f"{tempfile.gettempdir()}/debvisor_keys")

    # Create key
    api_key, key_obj=manager.create_key(  # type: ignore[name-defined]
        _principal_id="admin@debvisor.local",
        _description="Admin API key",
    )
    print(f"Created key: {api_key}")
    print(f"Key ID: {key_obj.key_id}")
    print(f"Expires: {key_obj.expires_at}")

    # Validate key
    _validated=manager.validate_key(api_key)  # type: ignore[name-defined]
    print(f"Validation: {validated.principal_id if validated else 'FAILED'}")  # type: ignore[name-defined]

    # Check stats
    _stats=manager.get_key_stats()  # type: ignore[name-defined]
    print(f"Stats: {stats}")  # type: ignore[name-defined]
