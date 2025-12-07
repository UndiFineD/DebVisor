# Security Scan Report

<https://github.com/UndiFineD/DebVisor/security/code-scanning>
is reporting many erros

please append the errors to this file security-scan.md

## Code Scanning Alerts

| Number | Tool | Rule | Description | State | URL |
|---|---|---|---|---|---|
| - | flake8 | W504 | Line break after binary operator | closed | Fixed by autopep8 and manual formatting |
| - | flake8 | E704 | Multiple statements on one line (def) | closed | Fixed by manual formatting in opt/core/unified_backend.py |

## Bandit Security Scan Alerts

| Tool | Rule | Description | State | Resolution |
|---|---|---|---|---|
| bandit | B101 | Use of assert detected | closed | Configured .bandit to exclude tests |
| bandit | B404 | Import subprocess | closed | Reviewed and marked as safe (nosec) where necessary |
| bandit | B603 | Subprocess call - check for execution of untrusted input | closed | Added check=False/True and nosec comments |
| bandit | B104 | Possible binding to all interfaces | closed | Marked as intended for containerized deployment |
| bandit | B105 | Possible hardcoded password | closed | Verified as false positives (headers/event IDs) and marked nosec |
| bandit | B112 | Try, Except, Continue detected | closed | Added comment explaining safety |
| bandit | B405 | Import xml.etree.ElementTree | closed | Replaced with defusedxml |
| bandit | B314 | Using xml.etree.ElementTree.parse | closed | Replaced with defusedxml |
