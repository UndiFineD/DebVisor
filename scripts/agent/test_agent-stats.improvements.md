# Improvements: `test_agent-stats.py`

## Suggested improvements
- Keep explicit invocation of this test file (it is not pytest-discoverable due to the `-` in the name).
- Consider using `logging` instead of `print` for controllable verbosity.
- Consider adding a test ensuring output formatting is stable for CI diffs.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_agent-stats.py`
