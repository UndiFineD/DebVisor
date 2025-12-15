# Description: `base_agent.py`

## Module purpose
Base Agent: Common functionality for all AI-powered agents.

Provides shared functionality for agents that improve code files using AI assistance.

## Location
- Path: `scripts/agent/base_agent.py`

## Public surface
- Classes: BaseAgent
- Functions: create_main_function

## Behavior summary
- Uses `argparse` for CLI parsing (via `create_main_function`).
- Invokes external commands via `subprocess` to access Copilot backends.
- Selects an AI backend via environment variables (or CLI `--backend`).
- Mutates `sys.path` to import optional markdown fixing utilities.

## AI backends
`BaseAgent.run_subagent(...)` supports multiple backends.

### Backend selection
- Env: `DV_AGENT_BACKEND`
	- `auto` (default): try local `copilot` CLI, then GitHub Models (if configured), then `gh copilot` for command-like prompts
	- `copilot`: force local `copilot` CLI
	- `gh`: force `gh copilot` (GitHub CLI extension; best suited for terminal commands)
	- `github-models`: force GitHub Models OpenAI-compatible API

### Configuration
- `DV_AGENT_MAX_CONTEXT_CHARS` (default `12000`): maximum number of characters of existing file content added to the prompt.
- `DV_AGENT_REPO_ROOT` (optional): overrides repo root used as `cwd` for subprocess invocations.
- `DV_AGENT_SYSTEM_PROMPT` (default: a generic helpful assistant prompt): system prompt for the GitHub Models route.

GitHub Models route:
- `GITHUB_MODELS_BASE_URL`: base URL for the OpenAI-compatible endpoint (used with `/v1/chat/completions`).
- `DV_AGENT_MODEL` (preferred) or `GITHUB_MODELS_MODEL`: model name.
- `GITHUB_TOKEN`: token for the API (never printed; diagnostics only report set/unset).

### Diagnostics
- CLI: `--describe-backends` prints a safe snapshot of what is available/configured (never prints token contents).
- API: `BaseAgent.get_backend_status()` and `BaseAgent.describe_backends()`.

## Key dependencies
- Top imports: `subprocess`, `pathlib`, `argparse`, `difflib`, `sys`
- Optional: `requests` (GitHub Models backend)
- Optional: `fix_markdown_lint` (markdown normalization for `.md` / `.plan.md` only)

## File fingerprint
- SHA256(source): (not tracked here; regenerate via tooling if needed)
