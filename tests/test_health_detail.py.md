# Code Issues Report: tests\test_health_detail.py
Generated: 2025-12-13T14:42:51.468551
Source: tests\test_health_detail.py

## Issues Summary
Total: 11 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 65 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 67 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 68 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 69 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 70 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 71 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 72 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 82 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 84 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 85 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 86 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status
Items marked below as fixed:


## Fix Proposals

**11 issues to fix:**


### Issue at Line 65

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    resp = app_client.get("/health/detail", base_url="https://localhost")
    if resp.status_code == 301:
        print(f"Redirecting to: {resp.headers.get('Location')}")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "build" in data
    assert "checks" in data
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 67

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        print(f"Redirecting to: {resp.headers.get('Location')}")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "build" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 68

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "build" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 69

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    data = resp.get_json()
    assert "build" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
    assert data["status"] in ("ok", "degraded")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 70

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    assert "build" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
    assert data["status"] in ("ok", "degraded")

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 71

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
    assert data["status"] in ("ok", "degraded")


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 72

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
    assert data["status"] in ("ok", "degraded")


def test_health_detail_with_envs(app_client, monkeypatch):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 82

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    monkeypatch.setenv("SMTP_STARTTLS", "true")

    resp = app_client.get("/health/detail", base_url="https://localhost")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "checks" in data
    assert "redis" in data["checks"]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 84

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    resp = app_client.get("/health/detail", base_url="https://localhost")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "checks" in data
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 85

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "checks" in data
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 86

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
    data = resp.get_json()
    assert "checks" in data
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
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
