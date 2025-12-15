# Errors: `generate_agent_reports.py`

## Scan scope
- Static scan (AST parse) + lightweight compile/syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile
- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards
- Runs `git` via `subprocess`; will fail if git is not installed or repo has no remote.
- May invoke AI tooling via `BaseAgent` (local `copilot` CLI, GitHub Models, or `gh copilot` depending on configuration).
- If no AI backend is available/configured, behavior should fall back safely without overwriting content with placeholders.
