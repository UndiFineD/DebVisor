# Improvements: `agent.py`

## Fixed
- Improved exception handling in `_run_command` to be more specific (`OSError`) and robust (`errors='replace'`). (Fixed)
- Added type hint and docstring to `_load_fix_markdown_content`. (Fixed)
- Added type hints for all methods. (Fixed)
- Add logging for all major actions. (Fixed)
- Add comprehensive docstrings for all methods following Google style format. (Fixed)
- Implement error recovery: retry failed file processing with exponential backoff. (Fixed)
- Add cache for `.codeignore` patterns to avoid re-parsing on each run. (Fixed)
- Add unit tests for edge cases (missing files, empty repos, malformed codeignore). (Fixed) [2025-12-16]
  * TestCodeignoreCache: 4 tests for caching, invalidation, missing files, comments
  * TestAgentContextManager: 2 tests for context manager support and error logging
  * TestCommandRetry: 3 tests for retry logic, exponential backoff, timeout handling
  * TestIgnorePatternMatching: 3 tests for pattern matching logic and edge cases
- Implement dry-run mode: show what would be done without actually modifying files. (Fixed) [2025-12-16]
  * TestDryRunMode: 3 tests for dry-run flag, default, and logging
- Add `--summary` flag to print statistics: files processed, fixes applied, time elapsed. (Fixed) [2025-12-16]
  * TestMetricsTracking: 8 tests for metrics tracking and summary reporting
  * Implemented as print_metrics_summary() method called at end of run()
- Add configurable timeout values per agent type. (Fixed) [2025-12-16]
  * TestConfigurableTimeouts: 5 tests for timeout configuration and retrieval
  * New --timeout CLI argument, timeout_per_agent dict parameter
- Implement selective agent execution: `--only-coder`, `--skip-tests`, etc. (Fixed) [2025-12-16]
  * TestSelectiveAgentExecution: 6 tests for agent filtering and execution control
  * New --only-agents CLI argument, selective_agents parameter, should_execute_agent() method

## Suggested improvements
- [ ] Implement async file processing using `asyncio` for better performance.
- [ ] Add progress bar using `tqdm` for visual feedback on large repos.
- [ ] Support `.agentignore` files in subdirectories (cascading ignore patterns).
- [ ] Add `--summary` flag to print statistics: files processed, fixes applied, time elapsed.
- [ ] Implement dry-run mode: show what would be done without actually modifying files.
- [ ] Add parallel processing using `multiprocessing.Pool` for independent files.
- [ ] Create metrics collection: track improvements per file, per agent, over time.
- [ ] Add webhook/callback support for integration with CI/CD pipelines.
- [ ] Implement selective agent execution: `--only-coder`, `--skip-tests`, etc.
- [ ] Add rollback functionality: save pre-agent versions for recovery.
- [ ] Refactor: File is large (900+ lines), consider splitting into: `agent_orchestrator.py`, `agent_processor.py`, `agent_reporter.py`.
- [ ] Add configurable timeout values per agent type (some may need longer timeouts).
- [ ] Implement progress tracking with timestamps for performance monitoring.
- [ ] Add integration tests with real repositories for end-to-end validation.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent.py`
