● I'll analyze the current code of `agent-stats.py` and update its description file.

● I don't have permission to create files. Here's the updated description content for
   `agent-stats.py.description.md` based on the current code:

   ---

   **agent-stats.py.description.md**

   ```markdown
   # agent-stats.py

   ## Module Purpose

   Stats Agent: Reports statistics on file metadata and supporting artifacts.

   Analyzes multiple files to track which have associated `.description.md`, `.changes.md`,
   `.errors.md`, `.improvements.md` files, and corresponding test files.

   ## Description

   This module provides a Stats Agent that scans a list of files and generates statistics on their
   associated metadata files. It checks for the presence of description files, changelog files,
   error reports, improvement suggestions, and test files. The agent supports both text and JSON
   output formats for easy integration with other tools.

   ## Behavior Summary

   - Has a CLI entrypoint (`__main__`)
   - Uses `argparse` for CLI parsing with `--files` (required) and `--format` (optional) arguments
   - Scans each file's parent directory for associated metadata files (`.description.md`,
   `.changes.md`, `.errors.md`, `.improvements.md`)
   - Checks for corresponding test files using the `test_{filename}.py` naming convention
   - Outputs statistics in either human-readable text format or JSON format
   - Reports total file count and counts for each metadata artifact type

   ## Key Dependencies

   - Top imports: `argparse`, `json`, `pathlib`, `typing`
   - Standard library only - no external dependencies

   ## Usage

   ```bash
   # Text output (default)
   python agent-stats.py --files file1.py file2.py file3.py

   # JSON output
   python agent-stats.py --files file1.py file2.py --format json
   ```

   ## Output Statistics

   - `total_files`: Total number of files analyzed
   - `files_with_context`: Files with `.description.md`
   - `files_with_changes`: Files with `.changes.md`
   - `files_with_errors`: Files with `.errors.md`
   - `files_with_improvements`: Files with `.improvements.md`
   - `files_with_tests`: Files with corresponding `test_{filename}.py`
   ```

   You'll need to create this file manually at `scripts\agent\agent-stats.py.description.md`.
