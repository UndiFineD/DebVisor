# Security Scan Report

<https://github.com/UndiFineD/DebVisor/security/code-scanning>
is reporting many erros

please append the errors to this file security-scan.md

## Code Scanning Alerts

| Number | Tool | Rule | Description | State | URL |
|---|---|---|---|---|---|
| 5113 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5113](https://github.com/UndiFineD/DebVisor/security/code-scanning/5113) |
| 5112 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5112](https://github.com/UndiFineD/DebVisor/security/code-scanning/5112) |
| 5111 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5111](https://github.com/UndiFineD/DebVisor/security/code-scanning/5111) |
| 5110 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5110](https://github.com/UndiFineD/DebVisor/security/code-scanning/5110) |
| 5109 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5109](https://github.com/UndiFineD/DebVisor/security/code-scanning/5109) |
| 5108 | flake8 | E305 | Expected 2 blank lines after class/function | closed | [View Alert 5108](https://github.com/UndiFineD/DebVisor/security/code-scanning/5108) |
| 5107 | flake8 | E501 | Line too long | closed | [View Alert 5107](https://github.com/UndiFineD/DebVisor/security/code-scanning/5107) |
| 5106 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5106](https://github.com/UndiFineD/DebVisor/security/code-scanning/5106) |
| 5105 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5105](https://github.com/UndiFineD/DebVisor/security/code-scanning/5105) |
| 5104 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5104](https://github.com/UndiFineD/DebVisor/security/code-scanning/5104) |
| 5103 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5103](https://github.com/UndiFineD/DebVisor/security/code-scanning/5103) |
| 5102 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5102](https://github.com/UndiFineD/DebVisor/security/code-scanning/5102) |
| 5101 | flake8 | E306 | Expected 1 blank line before nested def | closed | [View Alert 5101](https://github.com/UndiFineD/DebVisor/security/code-scanning/5101) |
| 5100 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5100](https://github.com/UndiFineD/DebVisor/security/code-scanning/5100) |
| 5099 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5099](https://github.com/UndiFineD/DebVisor/security/code-scanning/5099) |
| 5098 | flake8 | E117 | Over-indented | closed | [View Alert 5098](https://github.com/UndiFineD/DebVisor/security/code-scanning/5098) |
| 5097 | flake8 | E111 | Indentation is not a multiple of 4 | closed | [View Alert 5097](https://github.com/UndiFineD/DebVisor/security/code-scanning/5097) |
| 5096 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5096](https://github.com/UndiFineD/DebVisor/security/code-scanning/5096) |
| 5095 | flake8 | E302 | Expected 2 blank lines | closed | [View Alert 5095](https://github.com/UndiFineD/DebVisor/security/code-scanning/5095) |
| 5094 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5094](https://github.com/UndiFineD/DebVisor/security/code-scanning/5094) |
| 5093 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5093](https://github.com/UndiFineD/DebVisor/security/code-scanning/5093) |
| 5092 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5092](https://github.com/UndiFineD/DebVisor/security/code-scanning/5092) |
| 5091 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5091](https://github.com/UndiFineD/DebVisor/security/code-scanning/5091) |
| 5090 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5090](https://github.com/UndiFineD/DebVisor/security/code-scanning/5090) |
| 5089 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5089](https://github.com/UndiFineD/DebVisor/security/code-scanning/5089) |
| 5088 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5088](https://github.com/UndiFineD/DebVisor/security/code-scanning/5088) |
| 5087 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5087](https://github.com/UndiFineD/DebVisor/security/code-scanning/5087) |
| 5086 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5086](https://github.com/UndiFineD/DebVisor/security/code-scanning/5086) |
| 5085 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5085](https://github.com/UndiFineD/DebVisor/security/code-scanning/5085) |
| 5084 | flake8 | W293 | Blank line contains whitespace | closed | [View Alert 5084](https://github.com/UndiFineD/DebVisor/security/code-scanning/5084) |

## Resolution Status

All identified flake8 errors in `opt/services/migration/import_wizard.py` and `scripts/fix_markdown_lint_comprehensive.py` have been resolved.

- **W293**: Blank line contains whitespace - Fixed by `autopep8`.
- **E302**: Expected 2 blank lines - Fixed by `autopep8`.
- **E501**: Line too long - Fixed by manual refactoring and line wrapping.
- **F401**: Module imported but unused - Fixed by removing unused imports.
- **F841**: Local variable assigned but never used - Fixed by removing unused variables.
- **E305**: Expected 2 blank lines after class or function definition - Fixed by `autopep8`.
- **E306**: Expected 1 blank line before a nested definition - Fixed by `autopep8`.
- **E117**: Over-indented - Fixed by `autopep8`.
- **E111**: Indentation is not a multiple of 4 - Fixed by `autopep8`.

The files are now compliant with PEP 8 standards.

## Bandit Security Scan Alerts

| Tool | Rule | Description | State | Resolution |
|---|---|---|---|---|
| bandit | B602/B605/B607 | Subprocess with shell=True or partial paths | closed | Fixed in `debvisor_menu.py` and `first_boot_keygen.py` by using `shell=False` and full paths. |
| bandit | B105/B107 | Hardcoded password/secret | closed | Fixed in `app.py`, `security.py`, `socketio_server.py` by using `secrets.token_hex()` or env vars. |
| bandit | B110/B112 | Try, Except, Pass/Continue | closed | Fixed in `app.py`, `auth_2fa.py`, `routes/auth.py` by adding logging or explicit handling. |
| bandit | B104 | Bind to all interfaces | closed | Fixed in `app.py` by making host configurable via `FLASK_HOST`. |
| bandit | B101 | Assert used in production | closed | Fixed in `config.py` by replacing assert with runtime check. |
