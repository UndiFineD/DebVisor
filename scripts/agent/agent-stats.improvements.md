● I'll analyze the `agent-stats.py` file to provide more comprehensive and actionable
   improvements.

● Now let me check similar agent files to understand the patterns and best practices used in this
   codebase:

● Let me view the file to provide the improved suggestions as output instead:

● Based on my analysis of `agent-stats.py` and the codebase patterns, here are **comprehensive
   improvements** organized by priority:

   ## **High Priority Improvements**

   ### **Input Validation & Error Handling**
   - Validate file paths exist before processing with clear error messages
   - Handle empty file lists (currently silently succeeds with zeros)
   - Add graceful I/O error handling for permissions/encoding issues
   - Verify parent directories exist before reading companion files

   ### **Logging & Observability**
   - Replace `print` with `logging` module (aligns with `base_agent.py` standard)
   - Support `--verbose`/`-v` flag and `DV_AGENT_VERBOSITY` environment variable
   - Add debug-level logging showing file processing details
   - Report which companion files are missing per file

   ### **CLI Enhancements**
   - Add usage examples to `--help` (e.g., `--files scripts/agent/*.py`)
   - Support glob patterns: `--files 'scripts/**/*.py'`
   - Add `--directory` option to process all Python files automatically
   - Show percentage completion metrics (e.g., "60% have tests")

   ## **Medium Priority**

   ### **Enhanced Statistics**
   - Calculate completion percentages and coverage ratios
   - Add `--details` flag listing which files lack each companion type
   - Group stats by subdirectory for large codebases
   - Support `--baseline` to compare against previous runs

   ### **Output Formats**
   - **Note**: JSON mode already exists (line 101) but needs documentation
   - Add CSV output: `--format csv` for spreadsheet import
   - Add markdown tables: `--format markdown` for reports
   - Return non-zero exit codes based on coverage thresholds

   ### **CI/CD Integration**
   - Add `--min-coverage` to fail builds below targets
   - Add `--output FILE` to export results
   - Generate badge JSON for README shields
   - Support `--watch` mode for continuous monitoring

   ## **Low Priority**

   ### **Code Quality**
   - Expand type hints for better IDE support
   - Extract magic strings (file suffixes) to module constants
   - Split calculation from reporting logic for testability
   - Add comprehensive docstrings with examples

   ### **Testing**
   - Add edge case tests (non-existent files, empty lists, permissions)
   - Verify JSON structure and text formatting in tests
   - Integration tests with actual agent-generated files
   - Performance tests for hundreds of files

   ### **Advanced Features**
   - Historical tracking in database/file for trend analysis
   - Git integration to show stats only for changed files
   - Color terminal output (red=0%, green=100%)
   - Interactive TUI for exploring stats
   - Config file support (`.agent-stats.yaml`)

   ## **Implementation Priority Order**
   1. Input validation (prevent silent failures)
   2. Logging replacement (codebase consistency)
   3. Help examples (immediate usability)
   4. Percentage statistics (more useful output)
   5. CI/CD thresholds (enable quality gates)
