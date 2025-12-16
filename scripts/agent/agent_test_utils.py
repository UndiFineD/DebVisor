#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test utilities for agent scripts.

Provides helpers to load agent modules dynamically and manage sys.path for testing.
"""

from __future__ import annotations
import hashlib
import importlib.util
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar


# ============================================================================
# Type-Safe Enums for Test Utilities
# ============================================================================


class TestStatus(Enum):
    """Status of a test execution."""
    
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    PENDING = "pending"


class MockResponseType(Enum):
    """Types of mock AI backend responses."""
    
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    EMPTY = "empty"


class IsolationLevel(Enum):
    """File system isolation levels."""
    
    NONE = "none"
    TEMP_DIR = "temp_dir"
    COPY_ON_WRITE = "copy_on_write"
    SANDBOX = "sandbox"


class TestDataType(Enum):
    """Types of test data."""
    
    PYTHON_CODE = "python_code"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    TEXT = "text"


class PerformanceMetricType(Enum):
    """Types of performance metrics."""
    
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    FILE_IO = "file_io"
    CPU_TIME = "cpu_time"


class CleanupStrategy(Enum):
    """Cleanup strategies for test resources."""
    
    IMMEDIATE = "immediate"
    DEFERRED = "deferred"
    ON_SUCCESS = "on_success"
    NEVER = "never"


# ============================================================================
# Dataclasses for Structured Test Data
# ============================================================================


@dataclass
class TestFixture:
    """A test fixture with setup and teardown.
    
    Attributes:
        name: Fixture name.
        setup_fn: Setup function.
        teardown_fn: Teardown function.
        scope: Fixture scope (function, class, module, session).
        data: Fixture data.
    """
    
    name: str
    setup_fn: Optional[Callable[[], Any]] = None
    teardown_fn: Optional[Callable[[Any], None]] = None
    scope: str = "function"
    data: Any = None


@dataclass
class MockResponse:
    """Mock AI backend response.
    
    Attributes:
        content: Response content.
        response_type: Type of response.
        latency_ms: Simulated latency.
        tokens_used: Simulated token count.
        error_message: Error message if applicable.
    """
    
    content: str = ""
    response_type: MockResponseType = MockResponseType.SUCCESS
    latency_ms: int = 100
    tokens_used: int = 0
    error_message: Optional[str] = None


@dataclass
class TestDataFactory:
    """Factory for generating test data.
    
    Attributes:
        data_type: Type of data to generate.
        template: Template for generation.
        variations: Number of variations to create.
        seed: Random seed for reproducibility.
    """
    
    data_type: TestDataType
    template: str = ""
    variations: int = 1
    seed: Optional[int] = None


@dataclass
class TestResult:
    """Result of a test execution.
    
    Attributes:
        test_name: Name of the test.
        status: Test status.
        duration_ms: Test duration.
        error_message: Error message if failed.
        assertions_count: Number of assertions.
        timestamp: When test was run.
    """
    
    test_name: str
    status: TestStatus
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    assertions_count: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class PerformanceMetric:
    """Performance metric from test execution.
    
    Attributes:
        metric_type: Type of metric.
        value: Metric value.
        unit: Unit of measurement.
        test_name: Associated test.
        timestamp: When captured.
    """
    
    metric_type: PerformanceMetricType
    value: float
    unit: str
    test_name: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class TestEnvironment:
    """Test environment configuration.
    
    Attributes:
        name: Environment name.
        env_vars: Environment variables.
        temp_dir: Temporary directory.
        isolation_level: File system isolation.
        cleanup: Cleanup strategy.
    """
    
    name: str
    env_vars: Dict[str, str] = field(default_factory=dict)
    temp_dir: Optional[Path] = None
    isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR
    cleanup: CleanupStrategy = CleanupStrategy.IMMEDIATE


@dataclass
class TestSnapshot:
    """Snapshot for snapshot testing.
    
    Attributes:
        name: Snapshot name.
        content: Snapshot content.
        content_hash: Hash of content.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """
    
    name: str
    content: str
    content_hash: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    
    def __post_init__(self) -> None:
        """Compute content hash if not provided."""
        if not self.content_hash:
            self.content_hash = hashlib.sha256(
                self.content.encode("utf-8")
            ).hexdigest()


@dataclass  
class TestAssertion:
    """Custom assertion for agent testing.
    
    Attributes:
        name: Assertion name.
        expected: Expected value.
        actual: Actual value.
        passed: Whether assertion passed.
        message: Assertion message.
    """
    
    name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""


AGENT_DIR = Path(__file__).resolve().parent


# ============================================================================
# Mock AI Backend
# ============================================================================


class MockAIBackend:
    """Mock AI backend for testing.
    
    Provides configurable mock responses for AI backend calls
    without making real API requests.
    
    Example:
        mock = MockAIBackend()
        mock.add_response("prompt1", MockResponse(content="response"))
        result = mock.call("prompt1")
    """
    
    def __init__(self) -> None:
        """Initialize mock backend."""
        self._responses: Dict[str, MockResponse] = {}
        self._default_response = MockResponse(content="Mock response")
        self._call_history: List[Tuple[str, float]] = []
    
    def add_response(
        self,
        prompt_pattern: str,
        response: MockResponse,
    ) -> None:
        """Add mock response for a prompt pattern.
        
        Args:
            prompt_pattern: Prompt pattern (can be exact or regex).
            response: Mock response to return.
        """
        self._responses[prompt_pattern] = response
        logging.debug(f"Added mock response for pattern: {prompt_pattern}")
    
    def set_default_response(self, response: MockResponse) -> None:
        """Set default response for unmatched prompts.
        
        Args:
            response: Default mock response.
        """
        self._default_response = response
    
    def call(self, prompt: str) -> str:
        """Call mock backend with prompt.
        
        Args:
            prompt: Prompt to send.
            
        Returns:
            str: Mock response content.
            
        Raises:
            TimeoutError: If response type is TIMEOUT.
            RuntimeError: If response type is ERROR.
        """
        self._call_history.append((prompt, time.time()))
        
        # Find matching response
        response = self._default_response
        for pattern, resp in self._responses.items():
            if pattern in prompt or re.search(pattern, prompt):
                response = resp
                break
        
        # Simulate latency
        if response.latency_ms > 0:
            time.sleep(response.latency_ms / 1000)
        
        # Handle response types
        if response.response_type == MockResponseType.TIMEOUT:
            raise TimeoutError("Mock timeout")
        if response.response_type == MockResponseType.ERROR:
            raise RuntimeError(response.error_message or "Mock error")
        if response.response_type == MockResponseType.RATE_LIMITED:
            raise RuntimeError("Rate limited")
        if response.response_type == MockResponseType.EMPTY:
            return ""
        
        return response.content
    
    def get_call_history(self) -> List[Tuple[str, float]]:
        """Get history of calls made."""
        return list(self._call_history)
    
    def clear(self) -> None:
        """Clear all mock responses and history."""
        self._responses.clear()
        self._call_history.clear()


# ============================================================================
# Test Fixture Generator
# ============================================================================


class FixtureGenerator:
    """Generates test fixtures for common agent scenarios.
    
    Example:
        gen = FixtureGenerator()
        fixture = gen.create_python_file_fixture("test.py", "print('hello')")
    """
    
    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize fixture generator.
        
        Args:
            base_dir: Base directory for fixtures.
        """
        self.base_dir = base_dir or Path(tempfile.mkdtemp())
        self._fixtures: Dict[str, TestFixture] = {}
    
    def create_python_file_fixture(
        self,
        filename: str,
        content: str,
    ) -> TestFixture:
        """Create a Python file fixture.
        
        Args:
            filename: File name.
            content: File content.
            
        Returns:
            TestFixture: Created fixture.
        """
        file_path = self.base_dir / filename
        
        def setup() -> Path:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return file_path
        
        def teardown(path: Path) -> None:
            if path.exists():
                path.unlink()
        
        fixture = TestFixture(
            name=filename,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[filename] = fixture
        return fixture
    
    def create_directory_fixture(
        self,
        dirname: str,
        files: Dict[str, str],
    ) -> TestFixture:
        """Create a directory fixture with files.
        
        Args:
            dirname: Directory name.
            files: Dict of filename to content.
            
        Returns:
            TestFixture: Created fixture.
        """
        dir_path = self.base_dir / dirname
        
        def setup() -> Path:
            dir_path.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                (dir_path / name).write_text(content, encoding="utf-8")
            return dir_path
        
        def teardown(path: Path) -> None:
            if path.exists():
                shutil.rmtree(path)
        
        fixture = TestFixture(
            name=dirname,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[dirname] = fixture
        return fixture
    
    def cleanup_all(self) -> None:
        """Clean up all created fixtures."""
        for fixture in self._fixtures.values():
            if fixture.teardown_fn and fixture.data:
                try:
                    fixture.teardown_fn(fixture.data)
                except Exception as e:
                    logging.warning(f"Failed to cleanup fixture {fixture.name}: {e}")
        self._fixtures.clear()


# ============================================================================
# Test Data Factory
# ============================================================================


class TestDataGenerator:
    """Generates realistic test data for agent testing.
    
    Example:
        gen = TestDataGenerator()
        code = gen.generate_python_code(with_errors=False)
    """
    
    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize data generator.
        
        Args:
            seed: Random seed for reproducibility.
        """
        self.seed = seed
        if seed:
            import random
            random.seed(seed)
    
    def generate_python_code(
        self,
        with_errors: bool = False,
        with_docstrings: bool = True,
        num_functions: int = 3,
    ) -> str:
        """Generate sample Python code.
        
        Args:
            with_errors: Include syntax errors.
            with_docstrings: Include docstrings.
            num_functions: Number of functions to generate.
            
        Returns:
            str: Generated Python code.
        """
        lines = ['"""Generated test module."""', "", "import os", ""]
        
        for i in range(num_functions):
            lines.append(f"def function_{i}(arg1, arg2):")
            if with_docstrings:
                lines.append(f'    """Function {i} docstring."""')
            if with_errors and i == 0:
                lines.append("    return arg1 +")  # Syntax error
            else:
                lines.append(f"    return arg1 + arg2 + {i}")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_markdown(
        self,
        with_headers: bool = True,
        with_code_blocks: bool = True,
        num_sections: int = 3,
    ) -> str:
        """Generate sample markdown content.
        
        Args:
            with_headers: Include headers.
            with_code_blocks: Include code blocks.
            num_sections: Number of sections.
            
        Returns:
            str: Generated markdown.
        """
        lines = []
        
        if with_headers:
            lines.append("# Test Document")
            lines.append("")
        
        for i in range(num_sections):
            if with_headers:
                lines.append(f"## Section {i}")
            lines.append("")
            lines.append(f"This is section {i} content.")
            lines.append("")
            
            if with_code_blocks:
                lines.append("```python")
                lines.append(f"print('Section {i}')")
                lines.append("```")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_json(
        self,
        num_items: int = 5,
        nested: bool = True,
    ) -> str:
        """Generate sample JSON content.
        
        Args:
            num_items: Number of items.
            nested: Include nested structures.
            
        Returns:
            str: Generated JSON.
        """
        data = {
            "items": [
                {
                    "id": i,
                    "name": f"item_{i}",
                    "value": i * 10,
                }
                for i in range(num_items)
            ],
        }
        
        if nested:
            data["metadata"] = {
                "generated": datetime.now().isoformat(),
                "count": num_items,
            }
        
        return json.dumps(data, indent=2)


# ============================================================================
# File System Isolation
# ============================================================================


class FileSystemIsolator:
    """Isolates file system operations for testing.
    
    Example:
        with FileSystemIsolator() as fs:
            fs.write_file("test.txt", "content")
            content = fs.read_file("test.txt")
    """
    
    def __init__(
        self,
        isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR,
    ) -> None:
        """Initialize file system isolator.
        
        Args:
            isolation_level: Level of isolation.
        """
        self.isolation_level = isolation_level
        self._temp_dir: Optional[Path] = None
        self._original_cwd: Optional[str] = None
        self._created_files: List[Path] = []
    
    def __enter__(self) -> "FileSystemIsolator":
        """Enter context and set up isolation."""
        if self.isolation_level == IsolationLevel.TEMP_DIR:
            self._temp_dir = Path(tempfile.mkdtemp())
            self._original_cwd = os.getcwd()
            os.chdir(self._temp_dir)
        return self
    
    def __exit__(self, *args: Any) -> None:
        """Exit context and clean up."""
        if self._original_cwd:
            os.chdir(self._original_cwd)
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir)
        self._created_files.clear()
    
    def write_file(self, path: str, content: str) -> Path:
        """Write a file in isolated environment.
        
        Args:
            path: File path.
            content: File content.
            
        Returns:
            Path: Path to created file.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self._created_files.append(file_path)
        return file_path
    
    def read_file(self, path: str) -> str:
        """Read a file from isolated environment.
        
        Args:
            path: File path.
            
        Returns:
            str: File content.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path
        return file_path.read_text(encoding="utf-8")
    
    def get_temp_dir(self) -> Optional[Path]:
        """Get the temporary directory."""
        return self._temp_dir


# ============================================================================
# Performance Tracker
# ============================================================================


class PerformanceTracker:
    """Tracks test execution performance.
    
    Example:
        tracker = PerformanceTracker()
        with tracker.track("test_function"):
            run_test()
        metrics = tracker.get_metrics()
    """
    
    def __init__(self) -> None:
        """Initialize performance tracker."""
        self._metrics: List[PerformanceMetric] = []
        self._start_times: Dict[str, float] = {}
    
    @contextmanager
    def track(self, test_name: str) -> Iterator[None]:
        """Track execution time for a test.
        
        Args:
            test_name: Name of the test.
        """
        start = time.time()
        self._start_times[test_name] = start
        try:
            yield
        finally:
            duration = (time.time() - start) * 1000  # ms
            metric = PerformanceMetric(
                metric_type=PerformanceMetricType.EXECUTION_TIME,
                value=duration,
                unit="ms",
                test_name=test_name,
            )
            self._metrics.append(metric)
            del self._start_times[test_name]
    
    def record_metric(
        self,
        test_name: str,
        metric_type: PerformanceMetricType,
        value: float,
        unit: str,
    ) -> None:
        """Record a performance metric.
        
        Args:
            test_name: Test name.
            metric_type: Type of metric.
            value: Metric value.
            unit: Unit of measurement.
        """
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            unit=unit,
            test_name=test_name,
        )
        self._metrics.append(metric)
    
    def get_metrics(self) -> List[PerformanceMetric]:
        """Get all recorded metrics."""
        return list(self._metrics)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of performance metrics."""
        if not self._metrics:
            return {}
        
        execution_times = [
            m.value for m in self._metrics
            if m.metric_type == PerformanceMetricType.EXECUTION_TIME
        ]
        
        return {
            "total_metrics": len(self._metrics),
            "avg_execution_time_ms": (
                sum(execution_times) / len(execution_times)
                if execution_times else 0
            ),
            "max_execution_time_ms": max(execution_times) if execution_times else 0,
            "min_execution_time_ms": min(execution_times) if execution_times else 0,
        }
    
    def clear(self) -> None:
        """Clear all recorded metrics."""
        self._metrics.clear()
        self._start_times.clear()


# ============================================================================
# Snapshot Testing
# ============================================================================


class SnapshotManager:
    """Manages snapshots for snapshot testing.
    
    Example:
        mgr = SnapshotManager(Path("snapshots"))
        mgr.assert_match("test1", actual_output)
    """
    
    def __init__(self, snapshot_dir: Path) -> None:
        """Initialize snapshot manager.
        
        Args:
            snapshot_dir: Directory to store snapshots.
        """
        self.snapshot_dir = snapshot_dir
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self._snapshots: Dict[str, TestSnapshot] = {}
    
    def _get_snapshot_path(self, name: str) -> Path:
        """Get path for a snapshot."""
        return self.snapshot_dir / f"{name}.snap"
    
    def save_snapshot(self, name: str, content: str) -> TestSnapshot:
        """Save a new snapshot.
        
        Args:
            name: Snapshot name.
            content: Snapshot content.
            
        Returns:
            TestSnapshot: Created snapshot.
        """
        snapshot = TestSnapshot(name=name, content=content)
        path = self._get_snapshot_path(name)
        path.write_text(content, encoding="utf-8")
        self._snapshots[name] = snapshot
        return snapshot
    
    def load_snapshot(self, name: str) -> Optional[TestSnapshot]:
        """Load an existing snapshot.
        
        Args:
            name: Snapshot name.
            
        Returns:
            Optional[TestSnapshot]: Loaded snapshot or None.
        """
        path = self._get_snapshot_path(name)
        if not path.exists():
            return None
        
        content = path.read_text(encoding="utf-8")
        snapshot = TestSnapshot(name=name, content=content)
        self._snapshots[name] = snapshot
        return snapshot
    
    def assert_match(
        self,
        name: str,
        actual: str,
        update: bool = False,
    ) -> bool:
        """Assert that actual matches snapshot.
        
        Args:
            name: Snapshot name.
            actual: Actual content.
            update: Update snapshot if mismatch.
            
        Returns:
            bool: True if match, False otherwise.
        """
        expected = self.load_snapshot(name)
        
        if expected is None:
            # No snapshot exists, create it
            self.save_snapshot(name, actual)
            return True
        
        if expected.content == actual:
            return True
        
        if update:
            self.save_snapshot(name, actual)
            return True
        
        return False
    
    def get_diff(self, name: str, actual: str) -> List[str]:
        """Get diff between snapshot and actual.
        
        Args:
            name: Snapshot name.
            actual: Actual content.
            
        Returns:
            List[str]: Diff lines.
        """
        import difflib
        
        expected = self.load_snapshot(name)
        if expected is None:
            return ["No snapshot exists"]
        
        return list(difflib.unified_diff(
            expected.content.splitlines(),
            actual.splitlines(),
            fromfile=f"snapshot/{name}",
            tofile="actual",
            lineterm="",
        ))


# ============================================================================
# Test Result Aggregator
# ============================================================================


class TestResultAggregator:
    """Aggregates test results for reporting.
    
    Example:
        agg = TestResultAggregator()
        agg.add_result(TestResult(name="test1", status=TestStatus.PASSED))
        report = agg.get_report()
    """
    
    def __init__(self) -> None:
        """Initialize result aggregator."""
        self._results: List[TestResult] = []
    
    def add_result(self, result: TestResult) -> None:
        """Add a test result.
        
        Args:
            result: Test result to add.
        """
        self._results.append(result)
    
    def get_results(self) -> List[TestResult]:
        """Get all results."""
        return list(self._results)
    
    def get_report(self) -> Dict[str, Any]:
        """Get aggregated report.
        
        Returns:
            Dict containing test statistics.
        """
        total = len(self._results)
        passed = sum(1 for r in self._results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self._results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self._results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in self._results if r.status == TestStatus.ERROR)
        
        durations = [r.duration_ms for r in self._results]
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "pass_rate": passed / total if total > 0 else 0.0,
            "total_duration_ms": sum(durations),
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
        }
    
    def get_failures(self) -> List[TestResult]:
        """Get failed tests."""
        return [r for r in self._results if r.status == TestStatus.FAILED]
    
    def clear(self) -> None:
        """Clear all results."""
        self._results.clear()


# ============================================================================
# Test Assertion Helpers
# ============================================================================


class AgentAssertions:
    """Custom assertion helpers for agent testing.
    
    Example:
        assertions = AgentAssertions()
        assertions.assert_valid_python("print('hello')")
        assertions.assert_markdown_structure(content, headers=True)
    """
    
    def __init__(self) -> None:
        """Initialize assertion helpers."""
        self._assertions: List[TestAssertion] = []
    
    def assert_valid_python(self, code: str) -> bool:
        """Assert code is valid Python.
        
        Args:
            code: Python code to validate.
            
        Returns:
            bool: True if valid.
            
        Raises:
            AssertionError: If invalid Python.
        """
        try:
            compile(code, "<string>", "exec")
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except SyntaxError as e:
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid Python: {e}")
    
    def assert_contains_docstring(self, code: str) -> bool:
        """Assert code contains docstrings.
        
        Args:
            code: Python code to check.
            
        Returns:
            bool: True if contains docstrings.
        """
        has_docstring = '"""' in code or "'''" in code
        assertion = TestAssertion(
            name="contains_docstring",
            expected=True,
            actual=has_docstring,
            passed=has_docstring,
        )
        self._assertions.append(assertion)
        
        if not has_docstring:
            raise AssertionError("Code does not contain docstrings")
        return True
    
    def assert_markdown_structure(
        self,
        content: str,
        headers: bool = True,
        code_blocks: bool = False,
    ) -> bool:
        """Assert markdown has expected structure.
        
        Args:
            content: Markdown content.
            headers: Expect headers.
            code_blocks: Expect code blocks.
            
        Returns:
            bool: True if structure matches.
        """
        issues = []
        
        if headers and not re.search(r"^#+\s", content, re.MULTILINE):
            issues.append("missing headers")
        
        if code_blocks and "```" not in content:
            issues.append("missing code blocks")
        
        passed = len(issues) == 0
        assertion = TestAssertion(
            name="markdown_structure",
            expected="valid structure",
            actual=", ".join(issues) if issues else "valid",
            passed=passed,
        )
        self._assertions.append(assertion)
        
        if not passed:
            raise AssertionError(f"Markdown structure issues: {', '.join(issues)}")
        return True
    
    def assert_json_valid(self, content: str) -> bool:
        """Assert content is valid JSON.
        
        Args:
            content: JSON content.
            
        Returns:
            bool: True if valid JSON.
        """
        try:
            json.loads(content)
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except json.JSONDecodeError as e:
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid JSON: {e}")
    
    def get_assertions(self) -> List[TestAssertion]:
        """Get all recorded assertions."""
        return list(self._assertions)


# ============================================================================
# Legacy Functions (Preserved)
# ============================================================================


@contextmanager
def agent_dir_on_path() -> Iterator[None]:
    """Temporarily add the agent directory to sys.path.

    Note: This is a legacy helper to support tests that rely on implicit imports
    from the scripts/agent directory. For new code, prefer using load_agent_module
    or proper package imports.
    """
    old_sys_path = list(sys.path)
    sys.path.insert(0, str(AGENT_DIR))
    try:
        yield
    finally:
        sys.path[:] = old_sys_path


def get_base_agent_module() -> ModuleType:
    """Load base_agent module without modifying sys.path."""
    return load_agent_module("base_agent.py", "base_agent")


def load_module_from_path(name: str, path: Path) -> ModuleType:
    """Load a module from a specific path."""
    logging.debug(f"Loading module {name} from {path}")
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        logging.error(f"Could not load module {name} from {path}")
        raise ImportError(f"Could not load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@contextmanager
def agent_sys_path() -> Iterator[None]:
    """Add scripts/agent to sys.path temporarily."""
    path = str(AGENT_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)
        try:
            yield
        finally:
            sys.path.remove(path)
    else:
        yield


def load_agent_module(filename: str, module_name: str | None = None) -> ModuleType:
    """Load an agent module from scripts/agent by filename.

    Supports files that are not valid Python identifiers (e.g. `agent-changes.py`).
    """
    path = AGENT_DIR / filename
    if not path.exists():
        raise FileNotFoundError(path)
    if module_name is None:
        safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
        if not safe or safe[0].isdigit():
            safe = f"m_{safe}"
        module_name = f"_dv_legacy_{safe}"
    # Use the helper for consistency
    try:
        return load_module_from_path(module_name, path)
    except Exception:
        # Clean up if execution fails
        sys.modules.pop(module_name, None)
        raise
