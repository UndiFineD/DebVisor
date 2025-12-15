# Improvements: `base_agent.py`

## Suggested improvements
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.
- Consider standardizing subprocess error handling (consistent `check=True` usage and clearer stderr capture/reporting).
- Consider using `logging` instead of `print` for controllable verbosity.
- Consider making the `gh copilot` route use full prompt context (it currently only uses a short prompt slice).
- Consider caching `_command_available()` results per process to avoid repeated `--version` probes.
- Consider adding unit tests for `auto` backend ordering and the command-like prompt detection heuristic.
- Use `shutil.which` for a faster initial check of command existence in `_command_available`.
- Add type hints to `_resolve_repo_root` and other internal helpers.
- Implement `__repr__` for `BaseAgent` to aid in debugging.
- Lazy import `requests` to reduce startup time if it's not always needed.
- Refactor `fix_markdown_content` import to be less fragile, possibly by moving the fix module to a shared library location.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/base_agent.py`
