# Code Issues Report: opt\netcfg-tui\tests\test_netcfg.py
Generated: 2025-12-13T14:31:26.633778
Source: opt\netcfg-tui\tests\test_netcfg.py

## Issues Summary
Total: 2 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 70 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 83 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |

## Implementation Status
Items marked below as fixed:


## Fix Proposals

**2 issues to fix:**


### Issue at Line 70

**Tool:** bandit | **Code:** `B108` | **Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

**Context:**
```
        cfg.method = "static"
        cfg.address = "10.0.0.1"

        write_networkd([cfg], "/tmp/out")

        # Check if files were written
        # We expect 10-eth0.network
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 83

**Tool:** bandit | **Code:** `B108` | **Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

**Context:**
```

    def test_write_netplan(self, mock_makedirs, mock_file):
        cfg = InterfaceConfig("eth0", "wired")
        write_netplan([cfg], "/tmp/out")

        mock_file.assert_called()
        handle = mock_file()
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
