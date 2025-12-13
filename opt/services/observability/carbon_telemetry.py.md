# Code Issues Report: opt\services\observability\carbon_telemetry.py
Generated: 2025-12-13T15:16:19.231503
Source: opt\services\observability\carbon_telemetry.py

## Issues Summary
Total: 4 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 448 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 449 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 449 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 504 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |

## Implementation Status
Items marked below as fixed:
