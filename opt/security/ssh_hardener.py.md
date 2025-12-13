# Code Issues Report: opt\security\ssh_hardener.py

Generated: 2025-12-13T15:13:29.041103
Source: opt\security\ssh_hardener.py

## Issues Summary

Total: 5 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 113 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 191 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 191 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 199 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 199 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:
