● I'll analyze the current code and update the description file to match the actual
   implementation.

● Now I'll update the description file with accurate information based on the actual code:

● I don't have write permissions. Here's the complete updated description content:

   ```markdown
   # agent-changes.description.md

   ## Module Purpose
   `agent-changes.py` implements a Changes Agent that improves and updates changelog files (e.g.,
   `file.changes.md`). It extends `BaseAgent` to provide AI-assisted changelog enhancement with
   structured improvement suggestions and optional AI content generation.

   ## Description
   This module reads existing changelog files, provides 10 structured improvement suggestions for
   better change documentation, and optionally enhances content using AI assistance (GitHub Copilot
    CLI). When GitHub CLI is unavailable, it gracefully falls back to providing suggestion
   guidelines while preserving original content.

   The agent ensures changelog files follow best practices: version tracking, change
   categorization, semantic versioning, breaking change documentation, and migration guides.

   ## Public Surface

   ### Class: `ChangesAgent`
   Extends `BaseAgent` with changelog-specific functionality.

   **Methods:**
   - `_get_default_content() -> str`: Returns default content for new changelog files
   - `_get_fallback_response() -> str`: Returns fallback message when GitHub CLI is unavailable
   - `improve_content(prompt: str) -> str`: Provides 10-point improvement suggestions or AI
   enhancement

   ### Function: `main()`
   CLI entry point created via `create_main_function()` that accepts:
   - `file_path`: Path to the changes file (e.g., file.changes.md)
   - Optional `--prompt`: Custom improvement instructions

   ## Behavior
   Provides 10 structured changelog improvement suggestions:
   1. Include version numbers and dates
   2. Categorize changes (features, bug fixes, breaking changes)
   3. Use consistent formatting and terminology
   4. Include links to related issues or pull requests
   5. Document breaking changes clearly
   6. Add migration guides for major changes
   7. Include contributor acknowledgments
   8. Follow semantic versioning principles
   9. Add deprecation notices for removed features
   10. Include performance impact assessments

   Original changelog content is always preserved. AI enhancement is attempted when GitHub CLI is
   available; otherwise, structured suggestions are provided as comments.

   ## Key Dependencies
   - `base_agent`: Imports `BaseAgent` and `create_main_function`
   - GitHub CLI (`gh`): Optional runtime dependency for AI enhancement
   - Python 3.x standard library (argparse, pathlib, subprocess)
   ```

   This accurately reflects the current implementation based on the code analysis.
