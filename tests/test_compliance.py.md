# Code Issues Report: tests\test_compliance.py

Generated: 2025-12-13T15:23:30.602451
Source: tests\test_compliance.py

## Issues Summary

Total: 9 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 17 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 18 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 30 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 35 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 36 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 38 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 44 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 45 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 64 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 9 issues to fix

### Issue at Line 17

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

def test_default_policies(engine):
    assert len(engine.policies) >= 3
    assert "SEC-001" in engine.policies

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 18

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

def test_default_policies(engine):
    assert len(engine.policies) >= 3
    assert "SEC-001" in engine.policies

def test_policy_registration(engine):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 30

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        _check_function = "check_test",
    )
    engine.register_policy(p)
    assert "TEST-001" in engine.policies

def test_compliance_scan(engine, sample_resources):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 35

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

def test_compliance_scan(engine, sample_resources):
    report = engine.run_compliance_scan(sample_resources)
    assert report.total_resources == 2
    assert report.violations_count > 0
    # res-noncompliant should trigger violations in mock check
    assert any(v.resource_id == "res-noncompliant" for v in report.violations)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 36

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
def test_compliance_scan(engine, sample_resources):
    report = engine.run_compliance_scan(sample_resources)
    assert report.total_resources == 2
    assert report.violations_count > 0
    # res-noncompliant should trigger violations in mock check
    assert any(v.resource_id == "res-noncompliant" for v in report.violations)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 38

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    assert report.total_resources == 2
    assert report.violations_count > 0
    # res-noncompliant should trigger violations in mock check
    assert any(v.resource_id == "res-noncompliant" for v in report.violations)

def test_audit_logging(engine, sample_resources):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 44

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
def test_audit_logging(engine, sample_resources):
    engine.run_compliance_scan(sample_resources)
    logs = engine.get_audit_log()
    assert len(logs) > 0
    assert any("Violation detected" in line_item["message"] for line_item in logs)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 45

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    engine.run_compliance_scan(sample_resources)
    logs = engine.get_audit_log()
    assert len(logs) > 0
    assert any("Violation detected" in line_item["message"] for line_item in logs)

def test_remediation_trigger(engine):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 64

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    engine.run_compliance_scan(resources)

    logs = engine.get_audit_log()
    assert any("Remediation started" in line_item["message"] for line_item in logs)
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
