# Improvements: `agent-coder.py`

## Fixed
- Add logging for all major actions.
- Add type hints for all methods.
- Use `pathlib` consistently.

## Suggested improvements
- Add more sophisticated static analysis (e.g., pylint, mypy).
- Implement a retry mechanism if syntax validation fails (ask AI to fix syntax).
- Validate generated code against security best practices (e.g., no hardcoded secrets).
- Support diff-based application of changes instead of full file rewrite.
- Add `black` or `autopep8` formatting step after generation.
- Add docstrings for all methods.
- Add unit tests for edge cases.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-coder.py`