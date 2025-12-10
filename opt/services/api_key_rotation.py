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
API Key Rotation Mechanism for DebVisor.

Implements automatic API key rotation with:
- Scheduled rotation based on policy
- Grace period for old key validity
- Notification system for rotation events
- Audit logging
- Integration with Vault secrets management

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import hashlib
import hmac
import logging
import secrets
import string
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================


class KeyStatus(Enum):
    """API key status."""

    ACTIVE = "active"
    ROTATING = "rotating"
    GRACE_PERIOD = "grace_period"
    REVOKED = "revoked"
    EXPIRED = "expired"


class RotationTrigger(Enum):
    """What triggered key rotation."""

    SCHEDULED = "scheduled"
    MANUAL = "manual"
    SECURITY_INCIDENT = "security_incident"
    POLICY_CHANGE = "policy_change"
    KEY_COMPROMISE = "key_compromise"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class RotationPolicy:
    """API key rotation policy."""

    # Timing
    rotation_interval_days: int = 90
    grace_period_hours: int = 24
    warning_days_before: int = 7

    # Security
    min_key_length: int = 32
    key_complexity_required: bool = True
    require_approval: bool = False

    # Notifications
    notify_on_rotation: bool = True
    notify_on_expiry_warning: bool = True
    notification_channels: List[str] = field(
        default_factory=lambda: ["email", "webhook"]
    )


@dataclass
class APIKey:
    """Represents an API key."""

    key_id: str
    key_hash: str    # Never store plaintext key
    service_name: str
    description: str = ""

    # Status and lifecycle
    status: KeyStatus = KeyStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    last_rotated_at: Optional[datetime] = None

    # Rotation tracking
    rotation_count: int = 0
    previous_key_hash: Optional[str] = None
    grace_period_ends_at: Optional[datetime] = None

    # Metadata
    scopes: Set[str] = field(default_factory=set)
    rate_limit: Optional[int] = None    # Requests per minute
    allowed_ips: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """Check if key is expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_in_grace_period(self) -> bool:
        """Check if key is in grace period."""
        if self.grace_period_ends_at is None:
            return False
        return datetime.now(timezone.utc) < self.grace_period_ends_at

    @property
    def days_until_expiry(self) -> Optional[int]:
        """Get days until expiry."""
        if self.expires_at is None:
            return None
        delta = self.expires_at - datetime.now(timezone.utc)
        return max(0, delta.days)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding sensitive data)."""
        return {
            "key_id": self.key_id,
            "service_name": self.service_name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used_at": (
                self.last_used_at.isoformat() if self.last_used_at else None
            ),
            "last_rotated_at": (
                self.last_rotated_at.isoformat() if self.last_rotated_at else None
            ),
            "rotation_count": self.rotation_count,
            "scopes": list(self.scopes),
            "rate_limit": self.rate_limit,
            "days_until_expiry": self.days_until_expiry,
        }


@dataclass
class RotationEvent:
    """Records a key rotation event."""

    event_id: str
    key_id: str
    service_name: str
    trigger: RotationTrigger
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    old_key_hash: Optional[str] = None
    new_key_hash: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    initiated_by: str = "system"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "event_id": self.event_id,
            "key_id": self.key_id,
            "service_name": self.service_name,
            "trigger": self.trigger.value,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "error_message": self.error_message,
            "initiated_by": self.initiated_by,
        }


# =============================================================================
# Key Generator
# =============================================================================


class APIKeyGenerator:
    """Generates secure API keys."""

    DEFAULT_KEY_LENGTH = 32
    KEY_PREFIX = "dv_"    # DebVisor prefix

    @classmethod
    def generate(
        cls,
        length: int = DEFAULT_KEY_LENGTH,
        prefix: str = KEY_PREFIX,
        include_checksum: bool = True,
    ) -> str:
        """
        Generate a secure API key.

        Args:
            length: Key length (excluding prefix and checksum)
            prefix: Key prefix for identification
            include_checksum: Include checksum suffix

        Returns:
            Generated API key
        """
        # Use cryptographically secure random
        alphabet = string.ascii_letters + string.digits
        key_body = "".join(secrets.choice(alphabet) for _ in range(length))

        key = f"{prefix}{key_body}"

        if include_checksum:
            # Add 4-character checksum
            checksum = cls._calculate_checksum(key)[:4]
            key = f"{key}_{checksum}"

        return key

    @classmethod
    def hash_key(cls, key: str) -> str:
        """
        Hash an API key for storage.

        Uses PBKDF2-HMAC-SHA256 with a static salt.

        Args:
            key: Plaintext API key

        Returns:
            Hashed key
        """
        # Use a static salt for deterministic hashing (required for O(1) lookup)
        # In production, this salt should be loaded from a secure environment variable
        salt = os.getenv("API_KEY_SALT", "debvisor_static_salt_v1").encode()
        # 600,000 iterations recommended by OWASP for PBKDF2-HMAC-SHA256
        return hashlib.pbkdf2_hmac("sha256", key.encode(), salt, 600000).hex()

    @classmethod
    def _calculate_checksum(cls, data: str) -> str:
        """Calculate checksum for key validation."""
        # Use HMAC-SHA256 for checksum calculation
        # This avoids "weak cryptographic hash" warnings while providing integrity
        # Note: This is an integrity check, not a password hash.
        checksum_key = os.getenv("API_KEY_CHECKSUM_KEY", "debvisor_checksum_key").encode()
        return hmac.new(
            checksum_key, data.encode(), hashlib.sha256
        ).hexdigest()

    @classmethod
    def validate_format(cls, key: str) -> bool:
        """
        Validate API key format.

        Args:
            key: API key to validate

        Returns:
            True if format is valid
        """
        if not key.startswith(cls.KEY_PREFIX):
            return False

        parts = key.split("_")
        if len(parts) < 2:
            return False

        # Check minimum length
        body = parts[1] if len(parts) == 2 else "_".join(parts[1:-1])
        if len(body) < 16:
            return False

        # Validate checksum if present
        if len(parts) >= 3:
            checksum = parts[-1]
            key_without_checksum = "_".join(parts[:-1])
            expected = cls._calculate_checksum(key_without_checksum)[:4]
            return checksum == expected

        return True


# =============================================================================
# Key Rotation Manager
# =============================================================================


class APIKeyRotationManager:
    """
    Manages API key lifecycle and rotation.

    Features:
    - Automatic scheduled rotation
    - Grace period for old keys
    - Notification system
    - Audit logging
    - Vault integration (optional)
    """

    def __init__(
        self,
        default_policy: Optional[RotationPolicy] = None,
        vault_manager: Any = None,    # Optional VaultSecretsManager
    ) -> None:
        """
        Initialize rotation manager.

        Args:
            default_policy: Default rotation policy
            vault_manager: Optional Vault integration
        """
        self.default_policy = default_policy or RotationPolicy()
        self.vault_manager = vault_manager

        # Storage (in production, use database/Vault)
        self._keys: Dict[str, APIKey] = {}
        self._policies: Dict[str, RotationPolicy] = {}
        self._events: List[RotationEvent] = []

        # Callbacks
        self._notification_callbacks: List[Callable[..., Any]] = []

        # Background task
        self._rotation_task: Optional[asyncio.Task[None]] = None

        logger.info("API Key Rotation Manager initialized")

    # =========================================================================
    # Key Management
    # =========================================================================

    async def create_key(
        self,
        service_name: str,
        description: str = "",
        scopes: Optional[Set[str]] = None,
        policy: Optional[RotationPolicy] = None,
        expires_in_days: Optional[int] = None,
    ) -> tuple[str, APIKey]:
        """
        Create a new API key.

        Args:
            service_name: Service the key belongs to
            description: Key description
            scopes: Permission scopes
            policy: Rotation policy (uses default if not provided)
            expires_in_days: Override expiry days

        Returns:
            Tuple of (plaintext_key, APIKey object)
        """
        import uuid

        # Generate key
        plaintext_key = APIKeyGenerator.generate()
        key_hash = APIKeyGenerator.hash_key(plaintext_key)
        key_id = str(uuid.uuid4())[:8]

        # Calculate expiry
        policy = policy or self.default_policy
        if expires_in_days is None:
            expires_in_days = policy.rotation_interval_days

        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        # Create key object
        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            service_name=service_name,
            description=description,
            scopes=scopes or set(),
            expires_at=expires_at,
        )

        # Store
        self._keys[key_id] = api_key
        self._policies[key_id] = policy

        # Store in Vault if available
        if self.vault_manager:
            try:
                await self._store_in_vault(api_key, plaintext_key)
            except Exception as e:
                logger.error(f"Failed to store key in Vault: {e}")

        logger.info(f"Created API key {key_id} for service {service_name}")

        return plaintext_key, api_key

    async def rotate_key(
        self,
        key_id: str,
        trigger: RotationTrigger = RotationTrigger.MANUAL,
        initiated_by: str = "system",
    ) -> tuple[str, APIKey]:
        """
        Rotate an API key.

        Args:
            key_id: Key ID to rotate
            trigger: What triggered the rotation
            initiated_by: User/system that initiated rotation

        Returns:
            Tuple of (new_plaintext_key, updated APIKey)
        """
        import uuid

        api_key = self._keys.get(key_id)
        if not api_key:
            raise KeyError(f"API key {key_id} not found")

        policy = self._policies.get(key_id, self.default_policy)

        # Store old key for grace period
        old_key_hash = api_key.key_hash

        # Generate new key
        new_plaintext_key = APIKeyGenerator.generate()
        new_key_hash = APIKeyGenerator.hash_key(new_plaintext_key)

        # Update key object
        api_key.previous_key_hash = old_key_hash
        api_key.key_hash = new_key_hash
        api_key.status = KeyStatus.ROTATING
        api_key.last_rotated_at = datetime.now(timezone.utc)
        api_key.rotation_count += 1

        # Set grace period
        api_key.grace_period_ends_at = datetime.now(timezone.utc) + timedelta(
            hours=policy.grace_period_hours
        )

        # Update expiry
        api_key.expires_at = datetime.now(timezone.utc) + timedelta(
            days=policy.rotation_interval_days
        )

        # Record event
        event = RotationEvent(
            event_id=str(uuid.uuid4())[:8],
            key_id=key_id,
            service_name=api_key.service_name,
            trigger=trigger,
            old_key_hash=old_key_hash[:8] + "...",    # Truncated for safety
            new_key_hash=new_key_hash[:8] + "...",
            initiated_by=initiated_by,
        )
        self._events.append(event)

        # Store in Vault if available
        if self.vault_manager:
            try:
                await self._store_in_vault(api_key, new_plaintext_key)
            except Exception as e:
                logger.error(f"Failed to store rotated key in Vault: {e}")

        # Send notifications
        if policy.notify_on_rotation:
            await self._send_notification(
                "key_rotated",
                api_key,
                {"trigger": trigger.value, "initiated_by": initiated_by},
            )

        logger.info(
            f"Rotated API key {key_id} for service {api_key.service_name} "
            f"(trigger: {trigger.value})"
        )

        return new_plaintext_key, api_key

    async def revoke_key(
        self,
        key_id: str,
        reason: str = "Manual revocation",
        initiated_by: str = "system",
    ) -> bool:
        """
        Revoke an API key immediately.

        Args:
            key_id: Key ID to revoke
            reason: Revocation reason
            initiated_by: User/system that initiated revocation

        Returns:
            True if revoked
        """
        api_key = self._keys.get(key_id)
        if not api_key:
            return False

        api_key.status = KeyStatus.REVOKED
        api_key.previous_key_hash = None    # Invalidate grace period
        api_key.grace_period_ends_at = None

        # Record event
        import uuid

        event = RotationEvent(
            event_id=str(uuid.uuid4())[:8],
            key_id=key_id,
            service_name=api_key.service_name,
            trigger=RotationTrigger.MANUAL,
            initiated_by=initiated_by,
        )
        self._events.append(event)

        logger.warning(
            f"Revoked API key {key_id} for service {api_key.service_name}: {reason}"
        )

        return True

    # =========================================================================
    # Key Validation
    # =========================================================================

    def validate_key(self, plaintext_key: str) -> Optional[APIKey]:
        """
        Validate an API key.

        Checks both current and grace-period keys.

        Args:
            plaintext_key: Plaintext API key

        Returns:
            APIKey if valid, None otherwise
        """
        # Validate format first
        if not APIKeyGenerator.validate_format(plaintext_key):
            return None

        key_hash = APIKeyGenerator.hash_key(plaintext_key)

        for api_key in self._keys.values():
            # Skip revoked/expired keys
            if api_key.status == KeyStatus.REVOKED:
                continue
            if api_key.is_expired:
                api_key.status = KeyStatus.EXPIRED
                continue

            # Check current key
            if api_key.key_hash == key_hash:
                api_key.last_used_at = datetime.now(timezone.utc)
                return api_key

            # Check grace period key
            if api_key.previous_key_hash == key_hash:
                if api_key.is_in_grace_period:
                    api_key.last_used_at = datetime.now(timezone.utc)
                    return api_key

        return None

    # =========================================================================
    # Scheduled Rotation
    # =========================================================================

    async def start_rotation_scheduler(self) -> None:
        """Start the background rotation scheduler."""
        if self._rotation_task:
            return

        self._rotation_task = asyncio.create_task(self._rotation_loop())
        logger.info("API key rotation scheduler started")

    async def stop_rotation_scheduler(self) -> None:
        """Stop the background rotation scheduler."""
        if self._rotation_task:
            self._rotation_task.cancel()
            try:
                await self._rotation_task
            except asyncio.CancelledError:
                pass
            self._rotation_task = None
        logger.info("API key rotation scheduler stopped")

    async def _rotation_loop(self) -> None:
        """Background rotation check loop."""
        while True:
            try:
                await asyncio.sleep(3600)    # Check every hour
                await self._check_scheduled_rotations()
                await self._cleanup_grace_periods()
                await self._send_expiry_warnings()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Rotation scheduler error: {e}")

    async def _check_scheduled_rotations(self) -> None:
        """Check for keys needing rotation."""
        for key_id, api_key in self._keys.items():
            if api_key.status not in (KeyStatus.ACTIVE, KeyStatus.GRACE_PERIOD):
                continue

            policy = self._policies.get(key_id, self.default_policy)

            # Check if rotation is due
            if api_key.last_rotated_at:
                days_since_rotation = (
                    datetime.now(timezone.utc) - api_key.last_rotated_at
                ).days
            else:
                days_since_rotation = (
                    datetime.now(timezone.utc) - api_key.created_at
                ).days

            if days_since_rotation >= policy.rotation_interval_days:
                try:
                    await self.rotate_key(key_id, trigger=RotationTrigger.SCHEDULED)
                except Exception as e:
                    logger.error(f"Scheduled rotation failed for {key_id}: {e}")

    async def _cleanup_grace_periods(self) -> None:
        """Clean up expired grace periods."""
        for api_key in self._keys.values():
            if api_key.grace_period_ends_at:
                if datetime.now(timezone.utc) > api_key.grace_period_ends_at:
                    api_key.previous_key_hash = None
                    api_key.grace_period_ends_at = None
                    api_key.status = KeyStatus.ACTIVE
                    logger.debug(f"Grace period ended for key {api_key.key_id}")

    async def _send_expiry_warnings(self) -> None:
        """Send warnings for keys expiring soon."""
        for key_id, api_key in self._keys.items():
            if api_key.status != KeyStatus.ACTIVE:
                continue

            policy = self._policies.get(key_id, self.default_policy)

            if api_key.days_until_expiry is not None:
                if api_key.days_until_expiry <= policy.warning_days_before:
                    if policy.notify_on_expiry_warning:
                        await self._send_notification(
                            "key_expiry_warning",
                            api_key,
                            {"days_remaining": api_key.days_until_expiry},
                        )

    # =========================================================================
    # Notifications
    # =========================================================================

    def register_notification_callback(
        self, callback: Callable[[str, APIKey, Dict[str, Any]], None]
    ) -> None:
        """Register a notification callback."""
        self._notification_callbacks.append(callback)

    async def _send_notification(
        self, event_type: str, api_key: APIKey, details: Dict[str, Any]
    ) -> None:
        """Send notifications to registered callbacks."""
        for callback in self._notification_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event_type, api_key, details)
                else:
                    callback(event_type, api_key, details)
            except Exception as e:
                logger.error(f"Notification callback error: {e}")

    # =========================================================================
    # Vault Integration
    # =========================================================================

    async def _store_in_vault(self, api_key: APIKey, plaintext_key: str) -> None:
        """Store key in Vault."""
        if not self.vault_manager:
            return

        secret_path = f"api-keys/{api_key.service_name}/{api_key.key_id}"
        secret_data = {
            "key": plaintext_key,
            "key_id": api_key.key_id,
            "service_name": api_key.service_name,
            "created_at": api_key.created_at.isoformat(),
            "expires_at": (
                api_key.expires_at.isoformat() if api_key.expires_at else None
            ),
        }

        self.vault_manager.store_secret(secret_path, secret_data, overwrite=True)

    # =========================================================================
    # Reporting
    # =========================================================================

    def get_all_keys(self) -> List[Dict[str, Any]]:
        """Get all keys (without sensitive data)."""
        return [key.to_dict() for key in self._keys.values()]

    def get_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific key."""
        api_key = self._keys.get(key_id)
        return api_key.to_dict() if api_key else None

    def get_rotation_history(
        self, key_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get rotation event history."""
        events = self._events

        if key_id:
            events = [e for e in events if e.key_id == key_id]

        return [e.to_dict() for e in events[-limit:]]

    def get_expiring_keys(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get keys expiring within specified days."""
        expiring = []

        for api_key in self._keys.values():
            if api_key.days_until_expiry is not None:
                if api_key.days_until_expiry <= days:
                    expiring.append(api_key.to_dict())

        return sorted(expiring, key=lambda x: x.get("days_until_expiry", 999))


# =============================================================================
# Global Instance
# =============================================================================

_rotation_manager: Optional[APIKeyRotationManager] = None


def get_rotation_manager() -> APIKeyRotationManager:
    """Get global rotation manager instance."""
    global _rotation_manager
    if _rotation_manager is None:
        _rotation_manager = APIKeyRotationManager()
    return _rotation_manager


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    async def main() -> None:
        manager = get_rotation_manager()

        # Create a key
        key, api_key = await manager.create_key(
            service_name="test-service",
            description="Test API key",
            scopes={"read", "write"},
        )

        print("Created key: <REDACTED>")
        print(f"Key details: {api_key.to_dict()}")

        # Validate key
        validated = manager.validate_key(key)
        print(f"Validated: {validated is not None}")

        # Rotate key
        new_key, updated = await manager.rotate_key(
            api_key.key_id, trigger=RotationTrigger.MANUAL
        )

        print("New key: <REDACTED>")
        print(
            f"Old key still valid (grace period): {manager.validate_key(key) is not None}"
        )
        print(f"New key valid: {manager.validate_key(new_key) is not None}")

        # Get history
        history = manager.get_rotation_history()
        print(f"Rotation history: {history}")

    asyncio.run(main())
