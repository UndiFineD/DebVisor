# Code Issues Report: tests\benchmarks\test_performance.py

Generated: 2025-12-13T17:18:18.444076
Source: tests\benchmarks\test_performance.py

## Issues Summary

Total: 17 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 287 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 291 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 292 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 293 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 294 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 297 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 297 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 297 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 299 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 302 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 318 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 319 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 320 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 321 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 324 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 325 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 326 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 17 issues to fix

### Issue at Line 287

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
## =============================================================================
def create_mock_vm(vm_id: str = None) -> Dict[str, Any]:
    """Create a mock VM object for testing."""
    vm_id = vm_id or f"vm-{random.randint(1000, 9999)}"
    return {
        "id": vm_id,
        "name": f"test-vm-{vm_id}",
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 291

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
    return {
        "id": vm_id,
        "name": f"test-vm-{vm_id}",
        "status": random.choice(["running", "stopped", "paused"]),
        "vcpus": random.randint(1, 16),
        "memory_mb": random.randint(512, 32768),
        "disk_gb": random.randint(10, 500),
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 292

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "id": vm_id,
        "name": f"test-vm-{vm_id}",
        "status": random.choice(["running", "stopped", "paused"]),
        "vcpus": random.randint(1, 16),
        "memory_mb": random.randint(512, 32768),
        "disk_gb": random.randint(10, 500),
        "network_interfaces": [
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 293

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "name": f"test-vm-{vm_id}",
        "status": random.choice(["running", "stopped", "paused"]),
        "vcpus": random.randint(1, 16),
        "memory_mb": random.randint(512, 32768),
        "disk_gb": random.randint(10, 500),
        "network_interfaces": [
            {
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 294

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "status": random.choice(["running", "stopped", "paused"]),
        "vcpus": random.randint(1, 16),
        "memory_mb": random.randint(512, 32768),
        "disk_gb": random.randint(10, 500),
        "network_interfaces": [
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 297

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "disk_gb": random.randint(10, 500),
        "network*interfaces": [
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
            }
            for * in range(random.randint(1, 4))
        ],
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 297

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "disk_gb": random.randint(10, 500),
        "network*interfaces": [
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
            }
            for * in range(random.randint(1, 4))
        ],
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 297

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "disk*gb": random.randint(10, 500),
        "network*interfaces": [
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
            }
            for * in range(random.randint(1, 4))
        ],
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 299

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
            }
            for * in range(random.randint(1, 4))
        ],
        "created*at": datetime.now(timezone.utc).isoformat(),
        "hypervisor": random.choice(["kvm", "xen"]),
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 302

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            for * in range(random.randint(1, 4))
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hypervisor": random.choice(["kvm", "xen"]),
        "tags": ["test", "benchmark"],
    }

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 318

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "kvm": {"status": "ok", "latency_ms": random.uniform(1, 10)},
            "ceph": {"status": "ok", "latency_ms": random.uniform(5, 20)},
            "kubernetes": {"status": "ok", "latency_ms": random.uniform(2, 15)},
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 319

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "kvm": {"status": "ok", "latency_ms": random.uniform(1, 10)},
            "ceph": {"status": "ok", "latency_ms": random.uniform(5, 20)},
            "kubernetes": {"status": "ok", "latency_ms": random.uniform(2, 15)},
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
        },
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 320

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "services": {
            "kvm": {"status": "ok", "latency_ms": random.uniform(1, 10)},
            "ceph": {"status": "ok", "latency_ms": random.uniform(5, 20)},
            "kubernetes": {"status": "ok", "latency_ms": random.uniform(2, 15)},
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
        },
        "metrics": {
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 321

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            "kvm": {"status": "ok", "latency_ms": random.uniform(1, 10)},
            "ceph": {"status": "ok", "latency_ms": random.uniform(5, 20)},
            "kubernetes": {"status": "ok", "latency_ms": random.uniform(2, 15)},
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
        },
        "metrics": {
            "cpu_percent": random.uniform(10, 80),
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 324

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
        },
        "metrics": {
            "cpu_percent": random.uniform(10, 80),
            "memory_percent": random.uniform(20, 70),
            "disk_percent": random.uniform(30, 60),
        },
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 325

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        },
        "metrics": {
            "cpu_percent": random.uniform(10, 80),
            "memory_percent": random.uniform(20, 70),
            "disk_percent": random.uniform(30, 60),
        },
    }
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 326

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        "metrics": {
            "cpu_percent": random.uniform(10, 80),
            "memory_percent": random.uniform(20, 70),
            "disk_percent": random.uniform(30, 60),
        },
    }

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
