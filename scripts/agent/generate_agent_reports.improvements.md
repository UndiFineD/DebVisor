# Improvements: `generate_agent_reports.py`

## Suggested improvements
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting).
- Add `--help` examples and validate CLI args (paths, required files).

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/generate_agent_reports.py`
