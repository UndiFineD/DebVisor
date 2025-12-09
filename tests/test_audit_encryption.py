#!/usr/bin/env python3
"""
Unit tests for Audit Log Encryption.

Tests for:
  - Field-level encryption/decryption
  - Key rotation
  - Encrypted field serialization
  - Searchable encryption hashing
"""

import unittest
import secrets
from unittest.mock import MagicMock, patch

from opt.services.audit_encryption import (
    FieldEncryptor,
    KeyStatus,
    EncryptedField,
)


class TestEncryptedField(unittest.TestCase):
    """Tests for EncryptedField serialization."""

    def test_serialization_roundtrip(self) -> None:
        """Test to_dict and from_dict roundtrip."""
        field = EncryptedField(
            ciphertext=b"cipher",
            nonce=b"nonce",
            tag=b"tag",
            key_id="key-1",
            algorithm="AES-256-GCM",
            version=1,
        )

        data = field.to_dict()
        restored = EncryptedField.from_dict(data)

        self.assertEqual(field.ciphertext, restored.ciphertext)
        self.assertEqual(field.nonce, restored.nonce)
        self.assertEqual(field.tag, restored.tag)
        self.assertEqual(field.key_id, restored.key_id)


class TestFieldEncryptor(unittest.TestCase):
    """Tests for FieldEncryptor logic."""

    def setUp(self) -> None:
        self.master_key = secrets.token_bytes(32)
        self.encryptor = FieldEncryptor(master_key=self.master_key)

    def test_initialization(self) -> None:
        """Test encryptor initialization."""
        self.assertIsNotNone(self.encryptor._active_key_id)
        self.assertEqual(len(self.encryptor._keys), 1)

        active_key = self.encryptor._keys[self.encryptor._active_key_id]
        self.assertEqual(active_key.key_material, self.master_key)
        self.assertEqual(active_key.status, KeyStatus.ACTIVE)

    def test_key_rotation(self) -> None:
        """Test key rotation."""
        old_key_id = self.encryptor._active_key_id
        new_key_id = self.encryptor.rotate_key()

        self.assertNotEqual(old_key_id, new_key_id)
        self.assertEqual(self.encryptor._active_key_id, new_key_id)

        old_key = self.encryptor._keys[old_key_id]
        self.assertEqual(old_key.status, KeyStatus.ROTATED)
        self.assertIsNotNone(old_key.rotated_at)

    @patch("cryptography.hazmat.primitives.ciphers.aead.AESGCM")
    def test_encrypt_decrypt(self, mock_aesgcm_cls):
        """Test encryption and decryption flow."""
        # Mock AESGCM
        mock_aesgcm = MagicMock()
        mock_aesgcm.encrypt.return_value = (
            b"encrypted_data" + b"tag_bytes_______"
        )  # 16 bytes tag
        mock_aesgcm.decrypt.return_value = b"secret message"
        mock_aesgcm_cls.return_value = mock_aesgcm

        # Encrypt
        plaintext = "secret message"
        encrypted = self.encryptor.encrypt(plaintext)

        self.assertIsInstance(encrypted, EncryptedField)
        self.assertEqual(encrypted.key_id, self.encryptor._active_key_id)

        # Decrypt
        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(decrypted, b"secret message")

    def test_decrypt_unknown_key(self) -> None:
        """Test decryption with unknown key."""
        encrypted = EncryptedField(
            ciphertext=b"cipher",
            nonce=b"nonce",
            tag=b"tag",
            key_id="unknown-key",
            algorithm="AES-256-GCM",
        )

        with self.assertRaises(ValueError):
            self.encryptor.decrypt(encrypted)

    def test_encrypt_no_active_key(self) -> None:
        """Test encryption when no active key exists."""
        # Manually clear keys
        self.encryptor._keys = {}
        self.encryptor._active_key_id = None

        with self.assertRaises(ValueError):
            self.encryptor.encrypt("test")


if __name__ == "__main__":
    unittest.main()
