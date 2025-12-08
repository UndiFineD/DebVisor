import pytest
import os
import json
import tempfile
import asyncio
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Import the class to test
# We need to patch the module level logger and HAS_CRYPTO if needed, 
# but since we are in a test environment with requirements installed, 
# we assume cryptography is available.
from opt.services.backup_manager import BackupEncryption

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp

@pytest.fixture
def backup_encryption(temp_dir):
    key_path = os.path.join(temp_dir, "backup.key")
    return BackupEncryption(key_path=key_path)

def test_key_generation(backup_encryption):
    """Test that a key is generated if it doesn't exist."""
    assert os.path.exists(backup_encryption.key_path)
    with open(backup_encryption.key_path, "rb") as f:
        key = f.read()
    assert len(key) == 32  # 256 bits
    assert backup_encryption._key == key

def test_key_loading(temp_dir):
    """Test that an existing key is loaded."""
    key_path = os.path.join(temp_dir, "existing.key")
    existing_key = AESGCM.generate_key(bit_length=256)
    with open(key_path, "wb") as f:
        f.write(existing_key)
    
    be = BackupEncryption(key_path=key_path)
    assert be._key == existing_key

@pytest.mark.asyncio
async def test_encrypt_decrypt_roundtrip(backup_encryption, temp_dir):
    """Test full encryption and decryption cycle."""
    input_data = b"Hello, World! " * 1000  # Enough to be interesting, but small enough for speed
    input_path = os.path.join(temp_dir, "input.dat")
    encrypted_path = os.path.join(temp_dir, "output.enc")
    decrypted_path = os.path.join(temp_dir, "restored.dat")

    with open(input_path, "wb") as f:
        f.write(input_data)

    # Encrypt
    await backup_encryption.encrypt_file(input_path, encrypted_path)
    assert os.path.exists(encrypted_path)
    
    # Verify header structure
    with open(encrypted_path, "rb") as f:
        header_line = f.readline()
        header = json.loads(header_line)
        assert header["algo"] == "AES-256-GCM"
        assert header["chunked"] is True
        assert "dek_nonce" in header
        assert "encrypted_dek" in header

    # Decrypt
    await backup_encryption.decrypt_file(encrypted_path, decrypted_path)
    assert os.path.exists(decrypted_path)

    # Verify content
    with open(decrypted_path, "rb") as f:
        restored_data = f.read()
    
    assert restored_data == input_data

@pytest.mark.asyncio
async def test_large_file_chunking(backup_encryption, temp_dir):
    """Test that chunking works correctly (mocking a small chunk size)."""
    # Mock CHUNK_SIZE to be small to force multiple chunks
    backup_encryption.CHUNK_SIZE = 1024  # 1KB chunks
    
    data_size = 5 * 1024  # 5KB total
    input_data = os.urandom(data_size)
    input_path = os.path.join(temp_dir, "large_input.dat")
    encrypted_path = os.path.join(temp_dir, "large_output.enc")
    decrypted_path = os.path.join(temp_dir, "large_restored.dat")

    with open(input_path, "wb") as f:
        f.write(input_data)

    await backup_encryption.encrypt_file(input_path, encrypted_path)
    await backup_encryption.decrypt_file(encrypted_path, decrypted_path)

    with open(decrypted_path, "rb") as f:
        restored_data = f.read()
    
    assert restored_data == input_data
