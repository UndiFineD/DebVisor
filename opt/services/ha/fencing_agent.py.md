# Code Issues Report: opt\services\ha\fencing_agent.py
Generated: 2025-12-13T15:15:30.215273
Source: opt\services\ha\fencing_agent.py

## Issues Summary
Total: 3 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 117 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 324 | 0 | bandit | `B113` | MEDIUM | Call to requests without timeout |
| 373 | 0 | bandit | `B113` | MEDIUM | Call to requests without timeout |

## Implementation Status
Items marked below as fixed:
