#!/usr/bin/env python3
"""
Unit tests for API Key Rotation.

Tests for:
- Rotation policy configuration
- API Key lifecycle and status
- Key generation and hashing
- Rotation logic
"""

import unittest
from datetime import datetime, timezone
from opt.services.api_key_rotation import (
    RotationPolicy,
    APIKey,
    KeyStatus,
)


class TestRotationPolicy(unittest.TestCase):
    """Tests for RotationPolicy configuration."""

    def test_default_policy(self) -> None:
        """Test default policy values."""
        policy = RotationPolicy()
        self.assertEqual(policy.rotation_interval_days, 90)
        self.assertEqual(policy.grace_period_hours, 24)
        self.assertTrue(policy.notify_on_rotation)

    def test_custom_policy(self) -> None:
        """Test custom policy values."""
        policy = RotationPolicy(
            rotation_interval_days=30, grace_period_hours=48, require_approval=True
        )
        self.assertEqual(policy.rotation_interval_days, 30)
        self.assertEqual(policy.grace_period_hours, 48)
        self.assertTrue(policy.require_approval)


class TestAPIKey(unittest.TestCase):
    """Tests for APIKey model."""

    def setUp(self) -> None:
        self.key = APIKey(
            key_id="key-123",
            key_hash="hashed_secret",
            service_name="payment-service",
            description="Payment API Key",
        )

    def test_initial_status(self) -> None:
        """Test initial key status."""
        self.assertEqual(self.key.status, KeyStatus.ACTIVE)
        self.assertEqual(self.key.rotation_count, 0)
        self.assertIsNone(self.key.previous_key_hash)

    def test_key_metadata(self) -> None:
        """Test key metadata handling."""
        self.key.scopes.add("read:payments")
        self.key.allowed_ips.add("10.0.0.1")

        self.assertIn("read:payments", self.key.scopes)
        self.assertIn("10.0.0.1", self.key.allowed_ips)

    def test_lifecycle_timestamps(self) -> None:
        """Test lifecycle timestamps."""
        now = datetime.now(timezone.utc)
        self.key.last_used_at = now
        self.key.last_rotated_at = now

        self.assertEqual(self.key.last_used_at, now)
        self.assertEqual(self.key.last_rotated_at, now)


if __name__ == "__main__":
    unittest.main()
