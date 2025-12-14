# Description

`base_agent.py` provides the shared implementation for the agent scripts under `scripts/agent/`.

It handles:

- Reading the target file (or initializing a default stub for new files)
- Calling GitHub Copilot CLI (via `gh copilot …`) to generate an improved version
- Writing the updated content back to disk and printing a unified diff

Notes:

- Markdown normalization is applied only to markdown files (`.md`, `.markdown`, `.plan.md`).
- If `gh` / Copilot CLI is not available, agents keep the existing file content unchanged.
