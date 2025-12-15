# Changelog

- Initial version of base_agent.py
- 2025-12-15: Force UTF-8 decoding for `subprocess` output to avoid Windows `cp1252` decode failures.
- 2025-12-15: Add multi-backend AI routing (`DV_AGENT_BACKEND`) supporting local `copilot` CLI, `gh copilot`, and GitHub Models.
- 2025-12-15: Add backend diagnostics (`--describe-backends`, `describe_backends`, `get_backend_status`) without leaking secrets.
- 2025-12-15: Move token access out of import-time code paths; treat missing/invalid configuration as a recoverable condition in `auto` mode.

## [2025-12-15]
- Added robust file reading with error handling in `read_previous_content`.
- Added explicit type hints to `__init__`.
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting). (Fixed)
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `create_main_function` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `update_file` is missing type annotations. (Fixed)
