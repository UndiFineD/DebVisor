# Changelog

- 2025-12-15: Added utilities for legacy agent tests (safe path-loading of agent modules, including hyphenated filenames).

## Session 6 [2025-01-13]

### Added - Type-Safe Enums
- `TestStatus` enum: PASSED, FAILED, SKIPPED, ERROR, PENDING
- `MockResponseType` enum: SUCCESS, ERROR, TIMEOUT, RATE_LIMITED, EMPTY
- `IsolationLevel` enum: NONE, TEMP_DIR, COPY_ON_WRITE, SANDBOX
- `TestDataType` enum: PYTHON_CODE, MARKDOWN, JSON, YAML, TEXT
- `PerformanceMetricType` enum: EXECUTION_TIME, MEMORY_USAGE, FILE_IO, CPU_TIME
- `CleanupStrategy` enum: IMMEDIATE, DEFERRED, ON_SUCCESS, NEVER

### Added - Dataclasses for Structured Data
- `TestFixture` dataclass: name, setup_fn, teardown_fn, scope, data
- `MockResponse` dataclass: content, response_type, latency_ms, tokens_used, error_message
- `TestDataFactory` dataclass: data_type, template, variations, seed
- `TestResult` dataclass: test_name, status, duration_ms, error_message, assertions_count
- `PerformanceMetric` dataclass: metric_type, value, unit, test_name, timestamp
- `TestEnvironment` dataclass: name, env_vars, temp_dir, isolation_level, cleanup
- `TestSnapshot` dataclass: name, content, content_hash, created_at, updated_at
- `TestAssertion` dataclass: name, expected, actual, passed, message

### Added - MockAIBackend Class
- `add_response()`: Add mock response for prompt pattern
- `set_default_response()`: Set default response
- `call()`: Call mock backend with simulated latency
- `get_call_history()`: Get history of calls
- `clear()`: Clear responses and history

### Added - FixtureGenerator Class
- `create_python_file_fixture()`: Create Python file fixture
- `create_directory_fixture()`: Create directory with files
- `cleanup_all()`: Clean up all created fixtures

### Added - TestDataGenerator Class
- `generate_python_code()`: Generate sample Python code
- `generate_markdown()`: Generate sample markdown content
- `generate_json()`: Generate sample JSON content

### Added - FileSystemIsolator Class
- Context manager for file system isolation
- `write_file()`: Write file in isolated environment
- `read_file()`: Read file from isolated environment
- `get_temp_dir()`: Get temporary directory

### Added - PerformanceTracker Class
- `track()`: Context manager to track execution time
- `record_metric()`: Record performance metric
- `get_metrics()`: Get all recorded metrics
- `get_summary()`: Get performance summary

### Added - SnapshotManager Class
- `save_snapshot()`: Save new snapshot
- `load_snapshot()`: Load existing snapshot
- `assert_match()`: Assert actual matches snapshot
- `get_diff()`: Get diff between snapshot and actual

### Added - TestResultAggregator Class
- `add_result()`: Add test result
- `get_results()`: Get all results
- `get_report()`: Get aggregated report with statistics
- `get_failures()`: Get failed tests

### Added - AgentAssertions Class
- `assert_valid_python()`: Assert code is valid Python
- `assert_contains_docstring()`: Assert code has docstrings
- `assert_markdown_structure()`: Assert markdown structure
- `assert_json_valid()`: Assert valid JSON

## [2025-12-16]
- Add type hints for all methods. (Fixed)
- Add docstrings for all methods. (Fixed)

## [2025-12-15]
- Added detailed logging for module loading.
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
