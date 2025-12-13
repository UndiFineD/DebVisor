# Code Issues Report: opt\k8sctl_enhanced.py
Generated: 2025-12-13T15:12:27.317173
Source: opt\k8sctl_enhanced.py

## Issues Summary
Total: 2 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 30 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 408 | 0 | bandit | `B608` | MEDIUM | Possible SQL injection vector through string-based query construction. |

## Implementation Status
Items marked below as fixed:
