# Code Issues Report: tests\test_acme_certificates.py
Generated: 2025-12-13T15:07:40.437327
Source: tests\test_acme_certificates.py

## Issues Summary
Total: 14 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 13 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 14 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 15 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 25 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 26 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 27 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 28 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 36 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 37 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 53 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 57 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 58 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 59 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 60 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status
Items marked below as fixed:


## Fix Proposals

**14 issues to fix:**


### Issue at Line 13

**Tool:** bandit | **Code:** `B108` | **Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

**Context:**
```
def acme_manager() -> None:
    config = ACMEConfig(
        _email = "test@example.com",
        _cert_dir = "/tmp/certs",
        _account_dir = "/tmp/account",
        _webroot = "/tmp/webroot"
    )
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 14

**Tool:** bandit | **Code:** `B108` | **Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

**Context:**
```
    config = ACMEConfig(
        _email = "test@example.com",
        _cert_dir = "/tmp/certs",
        _account_dir = "/tmp/account",
        _webroot = "/tmp/webroot"
    )
    return ACMECertificateManager(config)  # type: ignore[return-value]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 15

**Tool:** bandit | **Code:** `B108` | **Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

**Context:**
```
        _email = "test@example.com",
        _cert_dir = "/tmp/certs",
        _account_dir = "/tmp/account",
        _webroot = "/tmp/webroot"
    )
    return ACMECertificateManager(config)  # type: ignore[return-value]

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 25

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    with patch.object(acme_manager, '_issue_certificate', return_value=True) as mock_issue:
        success, cert = await acme_manager.request_certificate(["example.com"])

        assert success is True
        assert cert.common_name == "example.com"
        assert cert.status == CertificateStatus.VALID
        assert cert.issued_at is not None
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 26

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        success, cert = await acme_manager.request_certificate(["example.com"])

        assert success is True
        assert cert.common_name == "example.com"
        assert cert.status == CertificateStatus.VALID
        assert cert.issued_at is not None

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 27

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        assert success is True
        assert cert.common_name == "example.com"
        assert cert.status == CertificateStatus.VALID
        assert cert.issued_at is not None


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 28

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        assert success is True
        assert cert.common_name == "example.com"
        assert cert.status == CertificateStatus.VALID
        assert cert.issued_at is not None


@pytest.mark.asyncio
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 36

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    with patch.object(acme_manager, '_issue_certificate', return_value=False) as mock_issue:
        success, cert = await acme_manager.request_certificate(["example.com"])

        assert success is False
        assert cert.status == CertificateStatus.ERROR


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 37

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        success, cert = await acme_manager.request_certificate(["example.com"])

        assert success is False
        assert cert.status == CertificateStatus.ERROR


@pytest.mark.asyncio
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 53

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        with patch.object(acme_manager, '_parse_certificate_info'):
            result = await acme_manager._issue_certificate(cert)

            assert result is True
            # Verify certbot was called
            args, _ = mock_run.call_args
            cmd = args[0]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 57

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            # Verify certbot was called
            args, _ = mock_run.call_args
            cmd = args[0]
            assert "certbot" in cmd
            assert "certonly" in cmd
            assert "-d" in cmd
            assert "example.com" in cmd
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 58

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            args, _ = mock_run.call_args
            cmd = args[0]
            assert "certbot" in cmd
            assert "certonly" in cmd
            assert "-d" in cmd
            assert "example.com" in cmd
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 59

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            cmd = args[0]
            assert "certbot" in cmd
            assert "certonly" in cmd
            assert "-d" in cmd
            assert "example.com" in cmd
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 60

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            assert "certbot" in cmd
            assert "certonly" in cmd
            assert "-d" in cmd
            assert "example.com" in cmd
```

**Proposal:**
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
