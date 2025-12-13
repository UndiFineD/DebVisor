# Code Issues Report: opt\services\virtualization\xen_manager.py

Generated: 2025-12-13T15:18:26.764587
Source: opt\services\virtualization\xen_manager.py

## Issues Summary

Total: 14 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 127 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 241 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 241 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 266 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 266 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 360 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 360 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 489 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 489 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 519 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 605 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 605 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 627 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 657 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:
