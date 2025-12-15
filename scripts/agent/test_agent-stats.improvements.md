# Improvements: `test_agent-stats.py`

## Suggested improvements
- [Fixed] Consider using `logging` instead of `print` for controllable verbosity. (False positive: "print" in string literal)
- [Fixed] Function `test_stats_agent_counts_files` is missing type annotations.
- Rename the file to be pytest-importable (avoid '-' and extra '.'), then update references.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_agent-stats.py`
