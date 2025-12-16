# Changelog

## [1.0.2] - 2025-12-16

### Fixed

- Improved exception handling in `_run_command` to be more specific (`OSError`) and robust (`errors='replace'`). (Fixed)
- Added type hint and docstring to `_load_fix_markdown_content`. (Fixed)
- Added type hints for all methods. (Fixed)
- Add logging for all major actions. (Fixed)

## [1.0.1] - 2025-12-15

### Changed

- Improved Windows robustness for subprocess output decoding in `BaseAgent`.
- Expanded agent test coverage (unit tests under `tests/` plus legacy `scripts/agent/test_*.py`).
- Added VS Code tasks to run both agent test suites.
- Improved exception handling in `_run_command` to be more specific (`OSError`) and robust (`errors='replace'`).
- Added type hints to all methods in `agent.py`.

## [1.0.0] - 2025-12-14

### Added

- Initial implementation of the Agent orchestrator
- Support for multiple specialized sub-agents
- Iterative improvement loop with change detection
- Git integration for automatic commits and pushes
- Configurable file processing limits
- Comprehensive progress reporting

### Features

- Recursive code file discovery
- Automatic creation of supporting documentation files
- Error handling and recovery
- Stats reporting for processed files
- Command-line interface with multiple options

## [0.1.0] - 2025-12-13

### Initial

- Basic agent framework
- Sub-agent coordination system
- File processing pipeline
- Initial git operations support

## [2025-12-15]
- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting). (Fixed)
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `_commit_and_push` is missing type annotations. (Fixed)
- Function `_log_changes` is missing type annotations. (Fixed)
- Function `_mark_improvements_fixed` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `process_file` is missing type annotations. (Fixed)
- Function `run_stats_update` is missing type annotations. (Fixed)
- Function `run_tests` is missing type annotations. (Fixed)
- Function `run` is missing type annotations. (Fixed)
- Function `setup_logging` is missing type annotations. (Fixed)
