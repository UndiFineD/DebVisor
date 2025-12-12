# !/usr/bin/env python3
"""
Tests for API Key Manager (AUTH-001)

Tests key rotation, expiration, validation, and audit logging.
"""

import pytest
import tempfile
import shutil
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from opt.services.api_key_manager import (
    APIKeyManager,
    KeyRotationConfig,
    KeyStatus,
)
from typing import Generator


@pytest.fixture


def temp_storage() -> Generator[str, None, None]:
    """Create temporary storage directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture


def key_manager(temp_storage):
    """Create APIKeyManager instance for testing."""
    config = KeyRotationConfig(
        _expiration_days = 90,
        _overlap_days = 7,
        _warning_days = 14,
        _auto_rotate = True,
    )
    return APIKeyManager(config, temp_storage)


class TestAPIKeyCreation:
    """Test API key creation and validation."""

    def test_create_key(self, key_manager):
        """Test creating a new API key."""
        api_key, key_obj = key_manager.create_key(
            principal_id="user@test.com",
            _description = "Test key",
        )

        # Verify key format
        assert api_key.startswith("dv_")
        assert len(api_key) == 67    # "dv_" + 64 hex chars

        # Verify key object
        assert key_obj.principal_id == "user@test.com"
        assert key_obj.status == KeyStatus.ACTIVE
        assert key_obj.use_count == 0
        assert key_obj.description == "Test key"

    def test_validate_key(self, key_manager):
        """Test API key validation."""
        api_key, key_obj = key_manager.create_key(
            principal_id="user@test.com",
            _description = "Test key",
        )

        # Validate key
        validated = key_manager.validate_key(api_key)
        assert validated is not None
        assert validated.key_id == key_obj.key_id
        assert validated.principal_id == "user@test.com"
        assert validated.use_count == 1    # Incremented on validation

    def test_validate_invalid_key(self, key_manager):
        """Test validation of invalid key."""
        invalid_key = "dv_" + "0" * 64
        validated = key_manager.validate_key(invalid_key)
        assert validated is None

    def test_key_usage_tracking(self, key_manager):
        """Test that key usage is tracked."""
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )

        # Use key multiple times
        for i in range(5):
            validated = key_manager.validate_key(api_key)
            assert validated.use_count == i + 1


class TestKeyRotation:
    """Test API key rotation functionality."""

    def test_rotate_key(self, key_manager):
        """Test key rotation."""
        # Create original key
        old_api_key, old_key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            description="Original key",
        )

        # Rotate key
        new_api_key, new_key_obj = key_manager.rotate_key(
            old_key_obj.key_id,
            _description = "Rotated key",
        )

        # Verify new key
        assert new_api_key != old_api_key
        assert new_key_obj.key_id != old_key_obj.key_id
        assert new_key_obj.principal_id == old_key_obj.principal_id
        assert new_key_obj.status == KeyStatus.ACTIVE

        # Verify old key marked as expiring
        old_key_refreshed = key_manager.keys[old_key_obj.key_id]
        assert old_key_refreshed.status == KeyStatus.EXPIRING

        # Verify rotation linkage
        assert old_key_refreshed.rotation_id == new_key_obj.rotation_id

    def test_rotated_key_overlap(self, key_manager):
        """Test that old key works during overlap period."""
        # Create and rotate key
        old_api_key, old_key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Original key",
        )
        new_api_key, new_key_obj = key_manager.rotate_key(old_key_obj.key_id)

        # Both keys should work
        old_validated = key_manager.validate_key(old_api_key)
        new_validated = key_manager.validate_key(new_api_key)

        assert old_validated is not None
        assert new_validated is not None
        assert old_validated.status == KeyStatus.EXPIRING
        assert new_validated.status == KeyStatus.ACTIVE

    def test_auto_rotate_expiring_keys(self, key_manager):
        """Test automatic rotation of expiring keys."""
        # Create key expiring soon (mock by setting warning threshold high)
        key_manager.config.warning_days = 100    # Everything is "expiring soon"

        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )

        # Auto-rotate
        rotations = key_manager.auto_rotate_expiring_keys()

        # Verify rotation occurred
        assert len(rotations) == 1
        assert key_obj.key_id in rotations

        # Verify old key is expiring
        old_key = key_manager.keys[key_obj.key_id]
        assert old_key.status == KeyStatus.EXPIRING


class TestKeyRevocation:
    """Test key revocation functionality."""

    def test_revoke_key(self, key_manager):
        """Test revoking an API key."""
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )

        # Revoke key
        key_manager.revoke_key(key_obj.key_id, reason="Security incident")

        # Verify key is revoked
        key_refreshed = key_manager.keys[key_obj.key_id]
        assert key_refreshed.status == KeyStatus.REVOKED

        # Verify revoked key doesn't validate
        validated = key_manager.validate_key(api_key)
        assert validated is None

    def test_revoke_nonexistent_key(self, key_manager):
        """Test revoking nonexistent key raises error."""
        with pytest.raises(ValueError, match="Key not found"):
            key_manager.revoke_key("nonexistent_key_id")


class TestKeyExpiration:
    """Test key expiration functionality."""

    def test_expired_key_validation(self, key_manager):
        """Test that expired keys are rejected."""
        # Create key with short expiration
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Short-lived key",
            _custom_expiration_days = 0,    # Expires immediately
        )

        # Force expiration by setting expires_at to past
        key_obj.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        key_manager._save_keys()

        # Verify expired key is rejected
        validated = key_manager.validate_key(api_key)
        assert validated is None

        # Verify key status updated to expired
        key_refreshed = key_manager.keys[key_obj.key_id]
        assert key_refreshed.status == KeyStatus.EXPIRED

    def test_check_expiring_keys(self, key_manager):
        """Test identifying keys expiring soon."""
        # Create keys with different expirations
        key_manager.create_key(
            principal_id="user1@test.com",
            custom_expiration_days=100,    # Not expiring soon
        )
        key_manager.create_key(
            principal_id="user2@test.com",
            _custom_expiration_days = 5,    # Expiring soon
        )

        # Check expiring keys (warning threshold is 14 days)
        expiring = key_manager.check_expiring_keys()

        # Only second key should be expiring
        assert len(expiring) == 1
        assert expiring[0].principal_id == "user2@test.com"


class TestKeyCleanup:
    """Test key cleanup functionality."""

    def test_cleanup_expired_keys(self, key_manager):
        """Test cleanup of old expired keys."""
        # Create expired key
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Old key",
        )

        # Mark as expired and old
        key_obj.status = KeyStatus.EXPIRED
        key_obj.expires_at = datetime.now(timezone.utc) - timedelta(days=400)
        key_manager._save_keys()

        # Cleanup with 365 day retention
        removed = key_manager.cleanup_expired_keys(retention_days=365)

        # Verify key removed
        assert removed == 1
        assert key_obj.key_id not in key_manager.keys

    def test_cleanup_preserves_recent_expired(self, key_manager):
        """Test that recent expired keys are preserved."""
        # Create recently expired key
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Recent key",
        )
        key_obj.status = KeyStatus.EXPIRED
        key_obj.expires_at = datetime.now(timezone.utc) - timedelta(days=30)
        key_manager._save_keys()

        # Cleanup with 365 day retention
        removed = key_manager.cleanup_expired_keys(retention_days=365)

        # Key should be preserved
        assert removed == 0
        assert key_obj.key_id in key_manager.keys


class TestKeyPersistence:
    """Test key persistence and loading."""

    def test_keys_persisted(self, temp_storage):
        """Test that keys are saved to disk."""
        config = KeyRotationConfig()
        manager = APIKeyManager(config, temp_storage)

        # Create key
        api_key, key_obj = manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )

        # Verify file created
        keys_file = Path(temp_storage) / "api_keys.json"
        assert keys_file.exists()

        # Verify content
        with open(keys_file, "r") as f:
            data = json.load(f)
            assert key_obj.key_id in data

    def test_keys_loaded_on_init(self, temp_storage):
        """Test that keys are loaded from disk on initialization."""
        config = KeyRotationConfig()

        # Create manager and key
        manager1 = APIKeyManager(config, temp_storage)
        api_key, key_obj = manager1.create_key(
            principal_id="user@test.com",
            _description = "Test key",
        )

        # Create new manager instance (should load from disk)
        manager2 = APIKeyManager(config, temp_storage)

        # Verify key loaded
        assert key_obj.key_id in manager2.keys
        assert manager2.keys[key_obj.key_id].principal_id == "user@test.com"

        # Verify validation works
        validated = manager2.validate_key(api_key)
        assert validated is not None


class TestAuditLogging:
    """Test audit logging functionality."""

    def test_audit_log_created(self, key_manager, temp_storage):
        """Test that audit log file is created."""
        # Create key (triggers audit log)
        key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )

        # Verify audit log exists
        audit_log = Path(temp_storage) / "api_key_audit.log"
        assert audit_log.exists()

    def test_audit_log_entries(self, key_manager, temp_storage):
        """Test audit log entries are written."""
        # Perform various operations
        api_key, key_obj = key_manager.create_key(
            _principal_id = "user@test.com",
            _description = "Test key",
        )
        key_manager.rotate_key(key_obj.key_id)

        # Read audit log
        audit_log = Path(temp_storage) / "api_key_audit.log"
        with open(audit_log, "r") as f:
            lines = f.readlines()

        # Verify entries
        assert len(lines) >= 2    # create + rotate

        # Parse entries
        entries = [json.loads(line) for line in lines]
        assert entries[0]["event"] == "key_created"
        assert entries[1]["event"] == "key_rotated"


class TestStatistics:
    """Test key statistics functionality."""

    def test_get_key_stats(self, key_manager):
        """Test getting key statistics."""
        # Create keys with different statuses
        api_key1, key_obj1 = key_manager.create_key(
            principal_id="user1@test.com",
            description="Active key",
        )
        api_key2, key_obj2 = key_manager.create_key(
            _principal_id = "user2@test.com",
            _description = "Will be revoked",
        )
        key_manager.revoke_key(key_obj2.key_id)

        # Get stats
        stats = key_manager.get_key_stats()

        # Verify stats
        assert stats["total_keys"] == 2
        assert stats["active_keys"] == 1
        assert stats["revoked_keys"] == 1
        assert stats["expired_keys"] == 0
        assert stats["expiring_keys"] == 0

    def test_list_keys_for_principal(self, key_manager):
        """Test listing keys for a specific principal."""
        # Create keys for different principals
        key_manager.create_key(principal_id="user1@test.com")
        key_manager.create_key(principal_id="user1@test.com")
        key_manager.create_key(principal_id="user2@test.com")

        # List keys for user1
        user1_keys = key_manager.list_keys_for_principal("user1@test.com")

        # Verify results
        assert len(user1_keys) == 2
        assert all(k.principal_id == "user1@test.com" for k in user1_keys)
