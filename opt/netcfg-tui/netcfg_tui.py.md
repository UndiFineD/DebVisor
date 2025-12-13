# Code Issues Report: opt\netcfg-tui\netcfg_tui.py
Generated: 2025-12-13T15:13:04.619701
Source: opt\netcfg-tui\netcfg_tui.py

## Issues Summary
Total: 3 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 107 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 1120 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 1125 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status
Items marked below as fixed:
