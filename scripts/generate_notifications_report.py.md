# Code Issues Report: scripts\generate_notifications_report.py

Generated: 2025-12-13T15:22:15.069303
Source: scripts\generate_notifications_report.py

## Issues Summary

Total: 2 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 26 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 60 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:
