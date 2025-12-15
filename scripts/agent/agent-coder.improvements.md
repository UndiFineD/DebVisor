# Improvements: `agent-coder.py`

## Fixed
- Removed blocking fallback for "improve" prompts to enable AI backend usage.
- Enabled proper delegation to `BaseAgent` for code generation.

## Suggested improvements
- Add more sophisticated static analysis (e.g., pylint, mypy).
- Implement a retry mechanism if syntax validation fails (ask AI to fix syntax).

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-coder.py`