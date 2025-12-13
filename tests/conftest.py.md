# Code Issues Report: tests\conftest.py

Generated: 2025-12-13T17:18:20.720331
Source: tests\conftest.py

## Issues Summary

Total: 9 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 245 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 332 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 343 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 368 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 369 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 385 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 390 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 391 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 392 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 9 issues to fix

### Issue at Line 245

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        """Generate random integer"""
        import random

        return random.randint(min_val, max_val)

@pytest.fixture
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 332

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    start = time.time()
    yield
    elapsed = time.time() - start
    assert (
        elapsed  None:
        """Assert dict contains expected keys and values"""
        for key, value in expected.items():
            assert key in actual, f"Key '{key}' not found in actual dict"
            assert (
                actual[key] == value
            ), f"Value mismatch for key '{key}': {actual[key]} != {value}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 369

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Assert dict contains expected keys and values"""
        for key, value in expected.items():
            assert key in actual, f"Key '{key}' not found in actual dict"
            assert (
                actual[key] == value
            ), f"Value mismatch for key '{key}': {actual[key]} != {value}"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 385

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def assert_list_contains_all(actual: List[Any], *items: Any) -> None:
        """Assert list contains all items"""
        for item in items:
            assert item in actual, f"List does not contain: {item}"

    @staticmethod
    def assert_response_valid(response: Dict[str, Any]) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 390

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    @staticmethod
    def assert_response_valid(response: Dict[str, Any]) -> None:
        """Assert response has valid structure"""
        assert "status" in response, "Response missing 'status' field"
        assert "success" in response, "Response missing 'success' field"
        assert isinstance(response["success"], bool), "'success' must be bool"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 391

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def assert_response_valid(response: Dict[str, Any]) -> None:
        """Assert response has valid structure"""
        assert "status" in response, "Response missing 'status' field"
        assert "success" in response, "Response missing 'success' field"
        assert isinstance(response["success"], bool), "'success' must be bool"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 392

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Assert response has valid structure"""
        assert "status" in response, "Response missing 'status' field"
        assert "success" in response, "Response missing 'success' field"
        assert isinstance(response["success"], bool), "'success' must be bool"

@pytest.fixture
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
