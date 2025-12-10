#!/usr/bin/env python3
"""
Unit tests for Licensing Server.

Tests for:
- License tiers and feature flags
- License bundle serialization
- Hardware fingerprinting
- Signature verification
- License validation logic
"""

import unittest
    # from datetime import datetime, timedelta, timezone
    # from unittest.mock import MagicMock, patch, mock_open

from opt.services.licensing.licensing_server import (
    LicenseTier,
    FeatureFlag,
    LicenseFeatures,
    LicenseBundle,
    ECDSAVerifier,
    HardwareFingerprint,
)


class TestLicenseFeatures(unittest.TestCase):
    """Tests for LicenseFeatures logic."""

    def test_grace_period_calculation(self) -> None:
        """Test grace period calculation."""
        expires_at = datetime.now(timezone.utc)
        features = LicenseFeatures(
            tier=LicenseTier.STANDARD, expires_at=expires_at, grace_period_days=7
        )

        expected_grace = expires_at + timedelta(days=7)
        self.assertEqual(features.grace_until, expected_grace)

    def test_no_expiration_grace_period(self) -> None:
        """Test grace period when no expiration set."""
        features = LicenseFeatures(tier=LicenseTier.ENTERPRISE, expires_at=None)
        self.assertIsNone(features.grace_until)

    def test_enabled_features_standard(self) -> None:
        """Test enabled features for Standard tier."""
        features = LicenseFeatures(tier=LicenseTier.STANDARD, expires_at=None)

        enabled = features.enabled_features
        self.assertIn(FeatureFlag.BASIC_VM, enabled)
        self.assertIn(FeatureFlag.HA_CLUSTERING, enabled)
        self.assertNotIn(FeatureFlag.MULTI_REGION, enabled)

    def test_custom_features_override(self) -> None:
        """Test custom features overriding tier defaults."""
        features = LicenseFeatures(
            tier=LicenseTier.STANDARD,
            expires_at=None,
            custom_features={"multi_region": True, "ha_clustering": False},
        )

        enabled = features.enabled_features
        self.assertIn(FeatureFlag.MULTI_REGION, enabled)
        self.assertNotIn(FeatureFlag.HA_CLUSTERING, enabled)


class TestLicenseBundle(unittest.TestCase):
    """Tests for LicenseBundle serialization."""

    def setUp(self) -> None:
        self.features = LicenseFeatures(
            tier=LicenseTier.PROFESSIONAL,
            expires_at=datetime.now(timezone.utc),
            max_nodes=10,
        )
        self.bundle = LicenseBundle(
            id="lic-123",
            version=1,
            issued_at=datetime.now(timezone.utc),
            customer_id="cust-456",
            customer_name="Acme Corp",
            features=self.features,
            hardware_fingerprint="uuid:1234",
            signature=b"signature_bytes",
            public_key_id="key-1",
        )

    def test_serialization_roundtrip(self) -> None:
        """Test to_dict and from_dict roundtrip."""
        data = self.bundle.to_dict()
        restored = LicenseBundle.from_dict(data)

        self.assertEqual(self.bundle.id, restored.id)
        self.assertEqual(self.bundle.customer_id, restored.customer_id)
        self.assertEqual(self.bundle.features.tier, restored.features.tier)
        self.assertEqual(self.bundle.signature, restored.signature)


class TestHardwareFingerprint(unittest.TestCase):
    """Tests for hardware fingerprint generation."""

    @patch("platform.system")
    def test_linux_fingerprint(self, mock_system):
        """Test fingerprint generation on Linux."""
        mock_system.return_value = "Linux"

        with patch("builtins.open", mock_open(read_data="uuid-1234\n")):
            fingerprint = HardwareFingerprint.generate()
            # Result is a hash, so we check length and type
            self.assertIsInstance(fingerprint, str)
            self.assertEqual(len(fingerprint), 32)

    @patch("platform.system")
    @patch("subprocess.run")
    def test_windows_fingerprint(self, mock_run, mock_system):
        """Test fingerprint generation on Windows."""
        mock_system.return_value = "Windows"
        mock_run.return_value = MagicMock(
            stdout="UUID\nWindows-UUID-1234\n", returncode=0
        )

        fingerprint = HardwareFingerprint.generate()
        self.assertIsInstance(fingerprint, str)
        self.assertEqual(len(fingerprint), 32)


class TestECDSAVerifier(unittest.TestCase):
    """Tests for signature verification."""

    def setUp(self) -> None:
        self.verifier = ECDSAVerifier()

    @patch("opt.services.licensing.licensing_server.HAS_CRYPTO", False)
    def test_fallback_verification(self) -> None:
        """Test fallback verification when crypto missing."""
        data = b"test data"
        # Fallback uses sha256 digest as signature
        import hashlib

        signature = hashlib.sha256(data).digest()

        result = self.verifier.verify(data, signature, "key-1")
        self.assertTrue(result)

    @patch("opt.services.licensing.licensing_server.HAS_CRYPTO", False)
    def test_fallback_verification_fail(self) -> None:
        """Test fallback verification failure."""
        data = b"test data"
        signature = b"wrong signature"

        result = self.verifier.verify(data, signature, "key-1")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
