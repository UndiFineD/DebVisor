# Code Issues Report: opt\dvctl.py

Generated: 2025-12-13T15:11:59.808074
Source: opt\dvctl.py

## Issues Summary

Total: 7 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 60 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 200 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 200 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 245 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 258 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 268 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 280 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:
