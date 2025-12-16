# Changelog

- Initial version of agent-stats.py
- 2025-12-15: No functional changes in this iteration; documentation and test coverage refreshed.

## [2025-12-16]
- Add support for exporting stats to CSV. (Fixed)
- Add logging for all major actions. (Fixed)
- Add type hints for all methods. (Fixed)

## [2025-12-15]
- Added support for exporting stats to CSV format (`--format csv`).
- Added detailed logging for stats reporting.
- Added explicit type hints to `__init__` and `report_stats`.
- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `fmt` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `report_stats` is missing type annotations. (Fixed)
