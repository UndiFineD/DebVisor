# Errors: `base_agent.py`

## Scan scope
- Static scan (AST parse) + lightweight compile/syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile
- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards
- Invokes external tools (`copilot` CLI and/or `gh copilot`) via `subprocess`.
- In `auto` mode, if no backend is available/configured, the agent returns the original content (or a fallback message) to avoid overwriting files with placeholders.
- For `DV_AGENT_BACKEND=github-models`, GitHub Models must be configured (`GITHUB_MODELS_BASE_URL`, `GITHUB_TOKEN`, and `DV_AGENT_MODEL`/`GITHUB_MODELS_MODEL`) and `requests` must be installed.
- For explicit backends (`copilot`, `gh`, `github-models`) that are unavailable/misconfigured, `run_subagent` may raise a `RuntimeError`.
