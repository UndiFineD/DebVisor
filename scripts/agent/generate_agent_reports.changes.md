# Changelog

- 2025-12-15: Added report generation for each `scripts/agent/*.py` into `*.description.md`, `*.errors.md`, and `*.improvements.md`.

## [2025-12-15]
- Added detailed logging for report generation process.
- Added explicit type hints to `main`.
- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Fixed exception handling in `generate_agent_reports.py` (robust file reading).
