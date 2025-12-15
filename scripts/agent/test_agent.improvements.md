# Improvements: `test_agent.py`

## Suggested improvements
- [x] *Note*: All `print` usages are inside strings written to test files.
- [x] Security: Use `check=True` or `check=False` explicitly in `subprocess.run`. (Verified in `agent.py` which is the code under test)

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_agent.py`
