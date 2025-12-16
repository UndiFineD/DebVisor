"""
Tests for Phase 5: Reporting & Monitoring

Phase 5 implements:
1. Detailed improvement reports with statistics
2. Performance benchmarking and metrics
3. Cost analysis for API backends
4. Circuit breaker pattern for failing backends
5. Automated snapshot cleanup with retention policies

Test coverage includes:
- Report generation with comprehensive statistics
- Benchmark timing analysis per file and agent
- Cost estimation for different backends
- Circuit breaker state transitions and recovery
- Snapshot cleanup with retention policies
- Integration with existing Phase 4a/4b/4c features
- Edge cases (empty data, missing directories, invalid parameters)
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import time
import sys

# Add scripts/agent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts' / 'agent'))

from agent import Agent, CircuitBreaker


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_circuit_breaker_initialization(self):
        """Test circuit breaker initialization with defaults."""
        cb = CircuitBreaker("test_backend")
        
        assert cb.name == "test_backend"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_custom_parameters(self):
        """Test circuit breaker with custom parameters."""
        cb = CircuitBreaker(
            "service",
            failure_threshold=3,
            recovery_timeout=30,
            backoff_multiplier=1.5
        )
        
        assert cb.failure_threshold == 3
        assert cb.recovery_timeout == 30
        assert cb.backoff_multiplier == 1.5

    def test_circuit_breaker_success_call(self):
        """Test successful call through circuit breaker."""
        cb = CircuitBreaker("test")
        
        def successful_func():
            return "success"
        
        result = cb.call(successful_func)
        
        assert result == "success"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_failure_call(self):
        """Test failed call through circuit breaker."""
        cb = CircuitBreaker("test", failure_threshold=3)
        
        def failing_func():
            raise Exception("Service down")
        
        with pytest.raises(Exception):
            cb.call(failing_func)
        
        assert cb.failure_count == 1
        assert cb.state == "CLOSED"

    def test_circuit_breaker_opens_after_threshold(self):
        """Test circuit opens after failure threshold exceeded."""
        cb = CircuitBreaker("test", failure_threshold=2)
        
        def failing_func():
            raise Exception("Service down")
        
        # First failure
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "CLOSED"
        
        # Second failure opens circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"

    def test_circuit_breaker_fast_fail_when_open(self):
        """Test circuit fails immediately when open."""
        cb = CircuitBreaker("test", failure_threshold=1)
        
        def failing_func():
            raise Exception("Service down")
        
        # Open the circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"
        
        # Next call should fail immediately without calling function
        call_count = 0
        def count_calls():
            nonlocal call_count
            call_count += 1
            raise Exception("Should not be called")
        
        with pytest.raises(Exception, match="Circuit breaker.*OPEN"):
            cb.call(count_calls)
        
        assert call_count == 0  # Function never called

    def test_circuit_breaker_recovery(self):
        """Test circuit breaker recovery from OPEN to CLOSED."""
        cb = CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)
        
        def failing_func():
            raise Exception("Service down")
        
        def succeeding_func():
            return "ok"
        
        # Open the circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Should enter HALF_OPEN state
        result = cb.call(succeeding_func)
        assert result == "ok"
        assert cb.state == "HALF_OPEN"
        
        # Another success should close it
        result = cb.call(succeeding_func)
        assert cb.state == "CLOSED"

    def test_circuit_breaker_half_open_failure_reopens(self):
        """Test circuit reopens if it fails during HALF_OPEN."""
        cb = CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)
        
        def failing_func():
            raise Exception("Still down")
        
        # Open the circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Fail in HALF_OPEN state
        with pytest.raises(Exception):
            cb.call(failing_func)
        
        assert cb.state == "OPEN"


class TestReportGeneration:
    """Tests for improvement report generation."""

    def test_generate_improvement_report(self, tmp_path):
        """Test basic improvement report generation."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 10,
            'files_modified': 5,
            'agents_applied': {'coder': 4, 'tests': 3},
            'start_time': 0.0,
            'end_time': 10.0,
        }
        
        report = agent.generate_improvement_report()
        
        assert report['summary']['files_processed'] == 10
        assert report['summary']['files_modified'] == 5
        assert 'coder' in report['agents']
        assert report['summary']['modification_rate'] == 50.0

    def test_generate_improvement_report_includes_mode_info(self, tmp_path):
        """Test report includes execution mode information."""
        agent = Agent(repo_root=str(tmp_path), dry_run=True, enable_async=True)
        agent.metrics = {
            'files_processed': 5,
            'files_modified': 2,
            'agents_applied': {},
            'start_time': 0.0,
            'end_time': 5.0,
        }
        
        report = agent.generate_improvement_report()
        
        assert report['mode']['dry_run'] is True
        assert report['mode']['async_enabled'] is True

    def test_generate_improvement_report_with_empty_metrics(self, tmp_path):
        """Test report generation with no files processed."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 0,
            'files_modified': 0,
            'agents_applied': {},
            'start_time': time.time(),
            'end_time': None,
        }
        
        report = agent.generate_improvement_report()
        
        assert report['summary']['files_processed'] == 0
        assert report['summary']['modification_rate'] == 0


class TestBenchmarking:
    """Tests for execution benchmarking."""

    def test_benchmark_execution(self, tmp_path):
        """Test execution benchmarking."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'start_time': time.time() - 10,
            'end_time': time.time(),
            'files_processed': 5,
            'agents_applied': {'coder': 3, 'tests': 2},
        }
        
        files = [tmp_path / f'test{i}.py' for i in range(5)]
        for f in files:
            f.write_text('# test')
        
        benchmark = agent.benchmark_execution(files)
        
        assert benchmark['file_count'] == 5
        assert 'average_per_file' in benchmark
        assert 'per_file' in benchmark
        assert len(benchmark['per_file']) == 5

    def test_benchmark_execution_with_single_file(self, tmp_path):
        """Test benchmarking with single file."""
        agent = Agent(repo_root=str(tmp_path))
        start = time.time()
        agent.metrics = {
            'start_time': start,
            'end_time': start + 2.5,
            'files_processed': 1,
            'agents_applied': {},
        }
        
        files = [tmp_path / 'test.py']
        files[0].write_text('# test')
        
        benchmark = agent.benchmark_execution(files)
        
        assert benchmark['file_count'] == 1
        assert abs(benchmark['average_per_file'] - 2.5) < 0.1

    def test_benchmark_execution_with_no_files(self, tmp_path):
        """Test benchmarking with empty file list."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'start_time': time.time() - 5,
            'end_time': time.time(),
            'files_processed': 0,
            'agents_applied': {},
        }
        
        benchmark = agent.benchmark_execution([])
        
        assert benchmark['file_count'] == 0


class TestCostAnalysis:
    """Tests for cost analysis."""

    def test_cost_analysis_basic(self, tmp_path):
        """Test basic cost analysis."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 10,
            'agents_applied': {'coder': 8, 'tests': 7},
            'start_time': 0.0,
            'end_time': 10.0,
        }
        
        analysis = agent.cost_analysis(backend='github-models', cost_per_request=0.0001)
        
        assert analysis['backend'] == 'github-models'
        assert analysis['files_processed'] == 10
        assert analysis['total_agent_runs'] == 15
        assert abs(analysis['total_estimated_cost'] - 0.0015) < 0.0001

    def test_cost_analysis_different_backend(self, tmp_path):
        """Test cost analysis with different backend pricing."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 5,
            'agents_applied': {'coder': 3},
            'start_time': 0.0,
            'end_time': 5.0,
        }
        
        analysis = agent.cost_analysis(backend='openai', cost_per_request=0.001)
        
        assert analysis['backend'] == 'openai'
        assert analysis['cost_per_request'] == 0.001
        assert analysis['total_estimated_cost'] == 0.003

    def test_cost_analysis_cost_per_file(self, tmp_path):
        """Test cost per file calculation."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 10,
            'agents_applied': {'coder': 5},
            'start_time': 0.0,
            'end_time': 10.0,
        }
        
        analysis = agent.cost_analysis(cost_per_request=0.0001)
        
        expected_cost_per_file = 0.0005 / 10  # 5 requests * 0.0001 / 10 files
        assert abs(analysis['cost_per_file'] - expected_cost_per_file) < 0.0001


class TestSnapshotCleanup:
    """Tests for snapshot cleanup functionality."""

    def test_cleanup_old_snapshots_removes_old_files(self, tmp_path):
        """Test cleanup removes snapshots older than threshold."""
        agent = Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path  # Override repo root to use temp path
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        # Create old snapshot (11 days old)
        old_snapshot = snapshot_dir / '1000000_abc123_main.py'
        old_snapshot.write_text('old content')
        old_mtime = time.time() - (11 * 24 * 60 * 60)
        import os
        os.utime(old_snapshot, (old_mtime, old_mtime))
        
        # Create recent snapshot (2 days old)
        recent_snapshot = snapshot_dir / '2000000_def456_main.py'
        recent_snapshot.write_text('recent content')
        
        cleaned = agent.cleanup_old_snapshots(max_age_days=7)
        
        assert cleaned == 1
        assert not old_snapshot.exists()
        assert recent_snapshot.exists()

    def test_cleanup_old_snapshots_respects_count_limit(self, tmp_path):
        """Test cleanup respects max snapshots per file."""
        agent = Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path  # Override repo root to use temp path
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        # Create 5 snapshots for same file
        for i in range(5):
            snapshot = snapshot_dir / f'{i}_hash{i}_test.py'
            snapshot.write_text(f'content {i}')
        
        cleaned = agent.cleanup_old_snapshots(max_age_days=30, max_snapshots_per_file=2)
        
        # Should delete 3 oldest snapshots
        assert cleaned == 3

    def test_cleanup_old_snapshots_no_directory(self, tmp_path):
        """Test cleanup handles missing snapshot directory gracefully."""
        agent = Agent(repo_root=str(tmp_path))
        
        # No snapshot directory exists
        cleaned = agent.cleanup_old_snapshots()
        
        assert cleaned == 0

    def test_cleanup_old_snapshots_empty_directory(self, tmp_path):
        """Test cleanup with empty snapshot directory."""
        agent = Agent(repo_root=str(tmp_path))
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        cleaned = agent.cleanup_old_snapshots()
        
        assert cleaned == 0

    def test_cleanup_old_snapshots_mixed_files(self, tmp_path):
        """Test cleanup with snapshots of different files."""
        agent = Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path  # Override repo root to use temp path
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        # Create 3 snapshots for file1
        for i in range(3):
            snapshot = snapshot_dir / f'{i}_hash{i}_file1.py'
            snapshot.write_text(f'content {i}')
        
        # Create 2 snapshots for file2
        for i in range(3, 5):
            snapshot = snapshot_dir / f'{i}_hash{i}_file2.py'
            snapshot.write_text(f'content {i}')
        
        cleaned = agent.cleanup_old_snapshots(max_snapshots_per_file=1)
        
        # Should keep 1 per file, delete 3
        assert cleaned == 3


class TestPhase5Integration:
    """Integration tests for Phase 5 features."""

    def test_circuit_breaker_with_agent_execution(self, tmp_path):
        """Test circuit breaker integration with agent."""
        agent = Agent(repo_root=str(tmp_path))
        
        cb = CircuitBreaker("test_backend")
        
        def run_agent():
            return agent.generate_improvement_report()
        
        report = cb.call(run_agent)
        
        assert 'summary' in report
        assert cb.state == "CLOSED"

    def test_report_with_parallel_execution(self, tmp_path):
        """Test report generation after parallel execution."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        agent.metrics = {
            'files_processed': 8,
            'files_modified': 6,
            'agents_applied': {'coder': 5, 'tests': 4},
            'start_time': 0.0,
            'end_time': 8.0,
        }
        
        report = agent.generate_improvement_report()
        
        assert report['mode']['async_enabled'] is True
        assert report['summary']['files_processed'] == 8

    def test_cost_analysis_with_metrics_tracking(self, tmp_path):
        """Test cost analysis with comprehensive metrics."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 20,
            'files_modified': 15,
            'agents_applied': {
                'coder': 18,
                'tests': 15,
                'documentation': 12
            },
            'start_time': 0.0,
            'end_time': 60.0,
        }
        
        cost = agent.cost_analysis(cost_per_request=0.0001)
        
        # 18 + 15 + 12 = 45 requests
        assert cost['total_agent_runs'] == 45
        assert abs(cost['total_estimated_cost'] - 0.0045) < 0.0001

    def test_full_phase5_workflow(self, tmp_path):
        """Test complete Phase 5 workflow."""
        agent = Agent(repo_root=str(tmp_path), dry_run=False, enable_async=False)
        
        # Simulate execution metrics
        agent.metrics = {
            'files_processed': 10,
            'files_modified': 7,
            'agents_applied': {'coder': 8, 'tests': 6},
            'start_time': time.time() - 15,
            'end_time': time.time(),
        }
        
        # Generate report
        report = agent.generate_improvement_report()
        assert 'summary' in report
        
        # Benchmark
        files = [tmp_path / f'test{i}.py' for i in range(10)]
        for f in files:
            f.write_text('# test')
        benchmark = agent.benchmark_execution(files)
        assert 'average_per_file' in benchmark
        
        # Cost analysis
        cost = agent.cost_analysis(cost_per_request=0.0001)
        assert 'total_estimated_cost' in cost
        
        # Cleanup
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        cleaned = agent.cleanup_old_snapshots()
        assert cleaned == 0


class TestPhase5EdgeCases:
    """Edge case tests for Phase 5 features."""

    def test_circuit_breaker_call_with_arguments(self):
        """Test circuit breaker with function arguments."""
        cb = CircuitBreaker("test")
        
        def func_with_args(a, b, c=None):
            return f"{a}+{b}+{c}"
        
        result = cb.call(func_with_args, 1, 2, c=3)
        
        assert result == "1+2+3"

    def test_cost_analysis_with_zero_files(self, tmp_path):
        """Test cost analysis with no files processed."""
        agent = Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 0,
            'agents_applied': {},
            'start_time': 0.0,
            'end_time': 1.0,
        }
        
        cost = agent.cost_analysis()
        
        # Should not divide by zero
        assert cost['cost_per_file'] == 0

    def test_circuit_breaker_multiple_state_transitions(self):
        """Test multiple state transitions."""
        cb = CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)
        
        def fail():
            raise Exception("fail")
        
        def succeed():
            return "ok"
        
        # CLOSED -> OPEN
        with pytest.raises(Exception):
            cb.call(fail)
        assert cb.state == "OPEN"
        
        # OPEN (fast fail)
        with pytest.raises(Exception, match="OPEN"):
            cb.call(fail)
        
        # Wait for recovery
        time.sleep(1.1)
        
        # OPEN -> HALF_OPEN -> CLOSED
        cb.call(succeed)
        cb.call(succeed)
        assert cb.state == "CLOSED"

    def test_cleanup_snapshots_with_invalid_names(self, tmp_path):
        """Test cleanup handles malformed snapshot names."""
        agent = Agent(repo_root=str(tmp_path))
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        # Create snapshot with valid name
        valid = snapshot_dir / '1000_abc_test.py'
        valid.write_text('content')
        
        # Create snapshot with invalid name
        invalid = snapshot_dir / 'invalid_format'
        invalid.write_text('content')
        
        cleaned = agent.cleanup_old_snapshots()
        
        # Should handle gracefully, invalid file stays
        assert valid.exists()
        assert invalid.exists()

    def test_benchmark_with_zero_time_elapsed(self, tmp_path):
        """Test benchmarking when no time has elapsed."""
        agent = Agent(repo_root=str(tmp_path))
        now = time.time()
        agent.metrics = {
            'start_time': now,
            'end_time': now,  # Same time
            'files_processed': 5,
            'agents_applied': {},
        }
        
        files = [tmp_path / f'test{i}.py' for i in range(5)]
        for f in files:
            f.write_text('# test')
        
        benchmark = agent.benchmark_execution(files)
        
        assert benchmark['total_time'] == 0
        assert benchmark['average_per_file'] == 0
