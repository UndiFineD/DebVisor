# Code Issues Report: etc\debvisor\test_validate_blocklists.py

Generated: 2025-12-13T17:07:06.819455
Source: etc\debvisor\test_validate_blocklists.py

## Issues Summary

Total: 46 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 27 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 48 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 63 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 75 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 87 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 126 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 149 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 173 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 197 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 212 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 221 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 222 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 232 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 242 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 252 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 264 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 265 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 266 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 280 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 295 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 305 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 315 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 328 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 329 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 338 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 347 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 361 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 390 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 416 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 444 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 445 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 458 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 472 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 479 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 486 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 493 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 502 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 503 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 512 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 513 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 526 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 526 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 537 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 553 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 553 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 565 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 46 issues to fix

### Issue at Line 27

**Tool:**bandit |**Code:**`B404` |**Severity:** LOW

**Message:** Consider possible security implications associated with the
subprocess module.

### Context

```python

import pytest
import tempfile
import subprocess
import os

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 48

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (1)

```python
        # Should not raise exception via ipaddress module
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_ipv6_cidr(self) -> None:
        """Valid IPv6 CIDR blocks should pass"""
```python

### Proposal (1)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 63

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (2)

```python
        for cidr in valid_cidrs:
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_single_ipv4(self) -> None:
        """Single IPv4 addresses should be treated as /32"""
```python

### Proposal (2)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 75

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (3)

```python
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_valid_single_ipv6(self) -> None:
        """Single IPv6 addresses should be treated as /128"""
```python

### Proposal (3)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 87

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (4)

```python
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_invalid_ipv4_cidr(self) -> None:
        """Invalid IPv4 CIDR should raise ValueError"""
```python

### Proposal (4)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 126

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (5)

```python
            ip_network("256.0.0.0/8")

        # Error message should contain useful info
        assert "256" in str(exc_info.value) or "octet" in str(exc_info.value).lower()

class TestCommentHandling:
```python

### Proposal (5)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 149

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (6)

```python
                for line in f:
                    _line=line.split[0]("    #").strip()
                    if line:
                        assert ip_network(line, strict=False)
        finally:
            os.unlink(temp_file)

```python

### Proposal (6)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 173

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (7)

```python
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal (7)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 197

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (8)

```python
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal (8)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 212

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (9)

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2

    def test_subnet_overlap_detected(self) -> None:
        """Subnet should be detected as overlap with supernet"""
```python

### Proposal (9)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 221

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (10)

```python
        _supernet=ip_network("10.0.0.0/8")
        _subnet=ip_network("10.0.0.0/24")

        assert subnet.subnet_of(supernet)  # type: ignore[arg-type]
        assert supernet.supernet_of(subnet)  # type: ignore[arg-type]

    def test_partial_overlap_in_same_family(self) -> None:
```python

### Proposal (10)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 222

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (11)

```python
        _subnet=ip_network("10.0.0.0/24")

        assert subnet.subnet_of(supernet)  # type: ignore[arg-type]
        assert supernet.supernet_of(subnet)  # type: ignore[arg-type]

    def test_partial_overlap_in_same_family(self) -> None:
        """Partial overlaps in same address family should be detected"""
```python

### Proposal (11)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 232

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (12)

```python
        _net2=ip_network("10.0.128.0/17")

        # These overlap
        assert net2.subnet_of(net1)  # type: ignore[arg-type]

    def test_no_overlap_different_ranges(self) -> None:
        """Non-overlapping ranges should not overlap"""
```python

### Proposal (12)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 242

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (13)

```python
        _net2=ip_network("10.0.1.0/24")

        # Should not overlap (different subnets)
        assert not net1.overlaps(net2)

    def test_ipv4_ipv6_separate_families(self) -> None:
        """IPv4 and IPv6 should not overlap (different address families)"""
```python

### Proposal (13)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 252

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (14)

```python
        _ipv6_net=ip_network("2001:db8::/32")

        # Different families - should not compare for overlap
        assert ipv4_net.version != ipv6_net.version

    def test_overlap_warning_format(self) -> None:
        """Overlap warnings should have clear, actionable format"""
```python

### Proposal (14)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 264

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (15)

```python
        # Format: "[WARN] Overlap detected: 10.0.0.0/24 is subset of 10.0.0.0/8"
        warning=f"[WARN] Overlap detected: {subnet} is subset of {supernet}"

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

```python

### Proposal (15)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 265

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (16)

```python
        warning=f"[WARN] Overlap detected: {subnet} is subset of {supernet}"

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

```python

### Proposal (16)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 266

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (17)

```python

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

class TestWhitelistOverride:
```python

### Proposal (17)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 280

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (18)

```python
        _whitelist=ip_network("10.0.0.0/24")

        # Whitelist entry is subset of blocklist
        assert whitelist.subnet_of(blocklist)  # type: ignore[arg-type]

    def test_whitelist_supernet_allows_all_subnets(self) -> None:
        """Whitelist supernet should allow all subnets"""
```python

### Proposal (18)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 295

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (19)

```python

        # All blocked entries are within whitelist supernet
        for blocked in blocklist:
            assert blocked.subnet_of(whitelist)  # type: ignore[arg-type]

    def test_whitelist_does_not_override_outside_range(self) -> None:
        """Whitelist should not override entries outside its range"""
```python

### Proposal (19)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 305

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (20)

```python
        _whitelist=ip_network("192.168.0.0/16")

        # Different ranges - no override
        assert not blocklist.overlaps(whitelist)

    def test_single_ip_whitelist_override(self) -> None:
        """Single IP whitelist should override CIDR blocklist"""
```python

### Proposal (20)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 315

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (21)

```python
        _whitelist_ip=ip_address("10.0.0.1")

        # Single IP is within the blocklist range
        assert whitelist_ip in blocklist

class TestDuplicateDetection:
```python

### Proposal (21)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 328

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (22)

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2
        assert hash(net1) == hash(net2)

    def test_different_prefix_formats_same_network(self) -> None:
```python

### Proposal (22)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 329

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (23)

```python
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2
        assert hash(net1) == hash(net2)

    def test_different_prefix_formats_same_network(self) -> None:
        """Same network with different formats should be detected"""
```python

### Proposal (23)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 338

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (24)

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.1/8", strict=False)    # Different host, same network

        assert net1 == net2    # Should be normalized

    def test_duplicate_single_ips(self) -> None:
        """Duplicate single IP entries should be detected"""
```python

### Proposal (24)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 347

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (25)

```python
        _ip1=ip_network("10.0.0.1/32")
        _ip2=ip_network("10.0.0.1/32")

        assert ip1 == ip2

    def test_duplicate_detection_ignores_order(self) -> None:
        """Duplicates should be detected regardless of order"""
```python

### Proposal (25)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 361

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (26)

```python

        # Create set to detect duplicates
        _unique=set(entries)
        assert len(unique) == 2

class TestBlocklistFileFormat:
```python

### Proposal (26)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 390

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (27)

```python
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 4
        finally:
            os.unlink(temp_file)

```python

### Proposal (27)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 416

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (28)

```python
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 3
        finally:
            os.unlink(temp_file)

```python

### Proposal (28)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 444

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (29)

```python
                            ipv4_count += 1
                        else:
                            ipv6_count += 1
            assert ipv4_count == 2
            assert ipv6_count == 2
        finally:
            os.unlink(temp_file)
```python

### Proposal (29)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 445

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (30)

```python
                        else:
                            ipv6_count += 1
            assert ipv4_count == 2
            assert ipv6_count == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal (30)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 458

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (31)

```python
        from ipaddress import ip_network

        _doc_range=ip_network("2001:db8::/32")
        assert doc_range.is_documentation  # type: ignore[union-attr]

    def test_private_ranges_ipv4(self) -> None:
        """Private IPv4 ranges should be recognized"""
```python

### Proposal (31)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 472

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (32)

```python

        for cidr in private_ranges:
            _net=ip_network(cidr)
            assert net.is_private

    def test_private_ranges_ipv6(self) -> None:
        """Private IPv6 ranges (ULA) should be recognized"""
```python

### Proposal (32)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 479

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (33)

```python
        from ipaddress import ip_network

        _ula_range=ip_network("fc00::/7")
        assert ula_range.is_private

    def test_link_local_ipv6(self) -> None:
        """Link-local IPv6 range handling"""
```python

### Proposal (33)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 486

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (34)

```python
        from ipaddress import ip_network

        _link_local=ip_network("fe80::/10")
        assert link_local.is_link_local

    def test_multicast_ipv6(self) -> None:
        """Multicast IPv6 range handling"""
```python

### Proposal (34)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 493

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (35)

```python
        from ipaddress import ip_network

        _multicast=ip_network("ff00::/8")
        assert multicast.is_multicast

    def test_loopback_ranges(self) -> None:
        """Loopback ranges should be recognized"""
```python

### Proposal (35)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 502

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (36)

```python
        _ipv4_loopback=ip_address("127.0.0.1")
        _ipv6_loopback=ip_address("::1")

        assert ipv4_loopback.is_loopback
        assert ipv6_loopback.is_loopback

```python

### Proposal (36)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 503

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (37)

```python
        _ipv6_loopback=ip_address("::1")

        assert ipv4_loopback.is_loopback
        assert ipv6_loopback.is_loopback

class TestValidationScriptIntegration:
```python

### Proposal (37)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 512

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (38)

```python
    def test_validation_script_exists(self) -> None:
        """Validation script should exist and be executable"""
        script_path="etc/debvisor/validate-blocklists.sh"
        assert os.path.exists(script_path), f"Script not found: {script_path}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    def test_validation_script_with_valid_blocklist(self) -> None:
```python

### Proposal (38)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 513

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (39)

```python
        """Validation script should exist and be executable"""
        script_path="etc/debvisor/validate-blocklists.sh"
        assert os.path.exists(script_path), f"Script not found: {script_path}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    def test_validation_script_with_valid_blocklist(self) -> None:
        """Script should validate correct blocklist files"""
```python

### Proposal (39)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 526

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context (40)

```python

        try:
        # Script should accept valid file (exit code 0)
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal (40)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 526 (1)

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context (41)

```python

        try:
        # Script should accept valid file (exit code 0)
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal (41)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 537

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (42)

```python
                _text=True,
            )
            # May not be 0 if script requires other args, but should parse entries
            assert (
                "10.0.0.0/8" or "Valid" in result.stdout or result.returncode in [0, 2]
            )
        finally:
```python

### Proposal (42)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 553

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context (43)

```python
            temp_file=f.name

        try:
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal (43)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 553 (1)

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context (44)

```python
            temp_file=f.name

        try:
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal (44)

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 565

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when
compiling to optimised byte code.

### Context (45)

```python
                _text=True,
            )
            # Should report error or return non-zero
            assert (
                result.returncode != 0
                or "error" in result.stderr.lower()
                or "invalid" in result.stdout.lower()
```python

### Proposal (45)

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
