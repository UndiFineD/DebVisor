# Code Issues Report: tests\test_backup_manager_encryption.py

Generated: 2025-12-13T15:08:05.192097
Source: tests\test_backup_manager_encryption.py

## Issues Summary

Total: 12 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 28 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 31 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 32 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 43 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 61 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 67 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 68 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 69 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 70 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 74 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 80 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 104 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 12 issues to fix

### Issue at Line 28

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

def test_key_generation(backup_encryption):
    """Test that a key is generated if it doesn't exist."""
    assert os.path.exists(backup_encryption.key_path)
    with open(backup_encryption.key_path, "rb") as f:
        key = f.read()
    assert len(key) == 32    # 256 bits
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 31

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    assert os.path.exists(backup_encryption.key_path)
    with open(backup_encryption.key_path, "rb") as f:
        key = f.read()
    assert len(key) == 32    # 256 bits
    assert backup_encryption._key == key

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 32

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    with open(backup_encryption.key_path, "rb") as f:
        key = f.read()
    assert len(key) == 32    # 256 bits
    assert backup_encryption._key == key

def test_key_loading(temp_dir):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 43

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        f.write(existing_key)

    be = BackupEncryption(key_path=key_path)
    assert be._key == existing_key

@pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 61

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

    # Encrypt
    await backup_encryption.encrypt_file(input_path, encrypted_path)
    assert os.path.exists(encrypted_path)

    # Verify header structure
    with open(encrypted_path, "rb") as f:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 67

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    with open(encrypted_path, "rb") as f:
        header_line = f.readline()
        header = json.loads(header_line)
        assert header["algo"] == "AES-256-GCM"
        assert header["chunked"] is True
        assert "dek_nonce" in header
        assert "encrypted_dek" in header
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 68

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        header_line = f.readline()
        header = json.loads(header_line)
        assert header["algo"] == "AES-256-GCM"
        assert header["chunked"] is True
        assert "dek_nonce" in header
        assert "encrypted_dek" in header

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 69

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        header = json.loads(header_line)
        assert header["algo"] == "AES-256-GCM"
        assert header["chunked"] is True
        assert "dek_nonce" in header
        assert "encrypted_dek" in header

    # Decrypt
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 70

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        assert header["algo"] == "AES-256-GCM"
        assert header["chunked"] is True
        assert "dek_nonce" in header
        assert "encrypted_dek" in header

    # Decrypt
    await backup_encryption.decrypt_file(encrypted_path, decrypted_path)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 74

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

    # Decrypt
    await backup_encryption.decrypt_file(encrypted_path, decrypted_path)
    assert os.path.exists(decrypted_path)

    # Verify content
    with open(decrypted_path, "rb") as f:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 80

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    with open(decrypted_path, "rb") as f:
        restored_data = f.read()

    assert restored_data == input_data

@pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 104

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    with open(decrypted_path, "rb") as f:
        restored_data = f.read()

    assert restored_data == input_data
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
