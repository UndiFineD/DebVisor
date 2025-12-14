# Improvements

- Add an explicit `--dry-run` option (print diff only, do not write).
- Prefer `gh copilot suggest` (or another generation command) for content generation instead of `explain`.
- Add structured prompts per file type (description/changelog/errors/improvements) to produce consistent output.
- Add a small "dedupe"/normalization step for agent-generated markdown sections to guarantee idempotent reruns.
