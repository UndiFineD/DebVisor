# Code Issues Report: scripts\fix_all_errors.py

Generated: 2025-12-13T15:21:05.503636
Source: scripts\fix_all_errors.py

## Issues Summary

Total: 18 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 52 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 750 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 750 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 771 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 771 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 779 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 779 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 831 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 1149 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1187 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1228 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1313 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1376 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1405 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1800 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 1800 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 1845 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 1845 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:
