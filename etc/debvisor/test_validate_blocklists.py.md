# Code Issues Report: etc\debvisor\test_validate_blocklists.py

Generated: 2025-12-13T15:10:53.534083
Source: etc\debvisor\test_validate_blocklists.py

## Issues Summary

Total: 46 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 77 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 98 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 113 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 125 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 137 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 176 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 199 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 223 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 247 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 262 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 271 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 272 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 282 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 292 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 302 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 314 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 315 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 316 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 330 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 345 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 355 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 365 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 378 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 379 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 388 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 397 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 411 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 440 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 466 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 494 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 495 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 508 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 522 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 529 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 536 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 543 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 552 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 553 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 562 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 563 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 576 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 576 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 587 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 603 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 603 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 615 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 46 issues to fix

### Issue at Line 77

**Tool:**bandit |**Code:**`B404` |**Severity:** LOW

**Message:** Consider possible security implications associated with the subprocess module.

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

### Issue at Line 98

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # Should not raise exception via ipaddress module
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_ipv6_cidr(self) -> None:
        """Valid IPv6 CIDR blocks should pass"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 113

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        for cidr in valid_cidrs:
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_single_ipv4(self) -> None:
        """Single IPv4 addresses should be treated as /32"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 125

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_valid_single_ipv6(self) -> None:
        """Single IPv6 addresses should be treated as /128"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 137

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_invalid_ipv4_cidr(self) -> None:
        """Invalid IPv4 CIDR should raise ValueError"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 176

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            ip_network("256.0.0.0/8")

        # Error message should contain useful info
        assert "256" in str(exc_info.value) or "octet" in str(exc_info.value).lower()

class TestCommentHandling:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 199

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                for line in f:
                    _line=line.split[0]("    #").strip()
                    if line:
                        assert ip_network(line, strict=False)
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 223

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 247

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 262

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2

    def test_subnet_overlap_detected(self) -> None:
        """Subnet should be detected as overlap with supernet"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 271

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _supernet=ip_network("10.0.0.0/8")
        _subnet=ip_network("10.0.0.0/24")

        assert subnet.subnet_of(supernet)  # type: ignore[arg-type]
        assert supernet.supernet_of(subnet)  # type: ignore[arg-type]

    def test_partial_overlap_in_same_family(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 272

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _subnet=ip_network("10.0.0.0/24")

        assert subnet.subnet_of(supernet)  # type: ignore[arg-type]
        assert supernet.supernet_of(subnet)  # type: ignore[arg-type]

    def test_partial_overlap_in_same_family(self) -> None:
        """Partial overlaps in same address family should be detected"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 282

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net2=ip_network("10.0.128.0/17")

        # These overlap
        assert net2.subnet_of(net1)  # type: ignore[arg-type]

    def test_no_overlap_different_ranges(self) -> None:
        """Non-overlapping ranges should not overlap"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 292

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net2=ip_network("10.0.1.0/24")

        # Should not overlap (different subnets)
        assert not net1.overlaps(net2)

    def test_ipv4_ipv6_separate_families(self) -> None:
        """IPv4 and IPv6 should not overlap (different address families)"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 302

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _ipv6_net=ip_network("2001:db8::/32")

        # Different families - should not compare for overlap
        assert ipv4_net.version != ipv6_net.version

    def test_overlap_warning_format(self) -> None:
        """Overlap warnings should have clear, actionable format"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 314

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # Format: "[WARN] Overlap detected: 10.0.0.0/24 is subset of 10.0.0.0/8"
        warning=f"[WARN] Overlap detected: {subnet} is subset of {supernet}"

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 315

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        warning=f"[WARN] Overlap detected: {subnet} is subset of {supernet}"

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 316

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning

class TestWhitelistOverride:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 330

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _whitelist=ip_network("10.0.0.0/24")

        # Whitelist entry is subset of blocklist
        assert whitelist.subnet_of(blocklist)  # type: ignore[arg-type]

    def test_whitelist_supernet_allows_all_subnets(self) -> None:
        """Whitelist supernet should allow all subnets"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 345

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # All blocked entries are within whitelist supernet
        for blocked in blocklist:
            assert blocked.subnet_of(whitelist)  # type: ignore[arg-type]

    def test_whitelist_does_not_override_outside_range(self) -> None:
        """Whitelist should not override entries outside its range"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 355

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _whitelist=ip_network("192.168.0.0/16")

        # Different ranges - no override
        assert not blocklist.overlaps(whitelist)

    def test_single_ip_whitelist_override(self) -> None:
        """Single IP whitelist should override CIDR blocklist"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 365

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _whitelist_ip=ip_address("10.0.0.1")

        # Single IP is within the blocklist range
        assert whitelist_ip in blocklist

class TestDuplicateDetection:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 378

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2
        assert hash(net1) == hash(net2)

    def test_different_prefix_formats_same_network(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 379

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net2=ip_network("10.0.0.0/8")

        assert net1 == net2
        assert hash(net1) == hash(net2)

    def test_different_prefix_formats_same_network(self) -> None:
        """Same network with different formats should be detected"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 388

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _net1=ip_network("10.0.0.0/8")
        _net2=ip_network("10.0.0.1/8", strict=False)    # Different host, same network

        assert net1 == net2    # Should be normalized

    def test_duplicate_single_ips(self) -> None:
        """Duplicate single IP entries should be detected"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 397

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _ip1=ip_network("10.0.0.1/32")
        _ip2=ip_network("10.0.0.1/32")

        assert ip1 == ip2

    def test_duplicate_detection_ignores_order(self) -> None:
        """Duplicates should be detected regardless of order"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 411

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # Create set to detect duplicates
        _unique=set(entries)
        assert len(unique) == 2

class TestBlocklistFileFormat:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 440

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 4
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 466

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 3
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 494

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                            ipv4_count += 1
                        else:
                            ipv6_count += 1
            assert ipv4_count == 2
            assert ipv6_count == 2
        finally:
            os.unlink(temp_file)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 495

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                        else:
                            ipv6_count += 1
            assert ipv4_count == 2
            assert ipv6_count == 2
        finally:
            os.unlink(temp_file)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 508

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        from ipaddress import ip_network

        _doc_range=ip_network("2001:db8::/32")
        assert doc_range.is_documentation  # type: ignore[union-attr]

    def test_private_ranges_ipv4(self) -> None:
        """Private IPv4 ranges should be recognized"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 522

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        for cidr in private_ranges:
            _net=ip_network(cidr)
            assert net.is_private

    def test_private_ranges_ipv6(self) -> None:
        """Private IPv6 ranges (ULA) should be recognized"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 529

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        from ipaddress import ip_network

        _ula_range=ip_network("fc00::/7")
        assert ula_range.is_private

    def test_link_local_ipv6(self) -> None:
        """Link-local IPv6 range handling"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 536

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        from ipaddress import ip_network

        _link_local=ip_network("fe80::/10")
        assert link_local.is_link_local

    def test_multicast_ipv6(self) -> None:
        """Multicast IPv6 range handling"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 543

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        from ipaddress import ip_network

        _multicast=ip_network("ff00::/8")
        assert multicast.is_multicast

    def test_loopback_ranges(self) -> None:
        """Loopback ranges should be recognized"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 552

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _ipv4_loopback=ip_address("127.0.0.1")
        _ipv6_loopback=ip_address("::1")

        assert ipv4_loopback.is_loopback
        assert ipv6_loopback.is_loopback

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 553

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _ipv6_loopback=ip_address("::1")

        assert ipv4_loopback.is_loopback
        assert ipv6_loopback.is_loopback

class TestValidationScriptIntegration:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 562

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
    def test_validation_script_exists(self) -> None:
        """Validation script should exist and be executable"""
        script_path="etc/debvisor/validate-blocklists.sh"
        assert os.path.exists(script_path), f"Script not found: {script_path}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    def test_validation_script_with_valid_blocklist(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 563

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        """Validation script should exist and be executable"""
        script_path="etc/debvisor/validate-blocklists.sh"
        assert os.path.exists(script_path), f"Script not found: {script_path}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    def test_validation_script_with_valid_blocklist(self) -> None:
        """Script should validate correct blocklist files"""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 576

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python

        try:
        # Script should accept valid file (exit code 0)
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 576

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python

        try:
        # Script should accept valid file (exit code 0)
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 587

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                _text=True,
            )
            # May not be 0 if script requires other args, but should parse entries
            assert (
                "10.0.0.0/8" or "Valid" in result.stdout or result.returncode in [0, 2]
            )
        finally:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 603

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python
            temp_file=f.name

        try:
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 603

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python
            temp_file=f.name

        try:
            _result=subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 615

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                _text=True,
            )
            # Should report error or return non-zero
            assert (
                result.returncode != 0
                or "error" in result.stderr.lower()
                or "invalid" in result.stdout.lower()
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
