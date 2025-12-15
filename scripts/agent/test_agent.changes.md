# Changelog

- Initial version of test_agent.py
- 2025-12-15: Reworked legacy `agent.py` tests to use pytest fixtures and `monkeypatch` (no global `sys.path` edits).
- 2025-12-15: Added coverage for `agents_only`, `max_files`, ignore matching, and subprocess invocation wiring.
