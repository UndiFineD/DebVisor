"""
Comprehensive tests for Agent implementation - Phases 1-5.

This file consolidates all agent feature tests:
- Phase 4a: Core features (dry-run, selective agents, timeouts, metrics)
- Phase 4b: Advanced features (snapshots, cascading ignores, rollback)
- Phase 4c: Parallel execution (async, multiprocessing, webhooks, callbacks)
- Phase 5: Reporting & monitoring (circuit breaker, reports, benchmarking, cost analysis, cleanup)
"""
from __future__ import annotations
import logging
import sys
import time
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent", AGENT_DIR / "agent.py")


# ============================================================================
# PHASE 4A: CORE FEATURES (DRY-RUN, SELECTIVE AGENTS, TIMEOUTS, METRICS)
# ============================================================================

class TestDryRunMode:
    """Test dry-run mode functionality."""

    def test_dry_run_flag_set_on_init(self, tmp_path: Path, agent_module):
        """Verify dry_run flag is set correctly on Agent initialization."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        assert agent.dry_run is True

    def test_dry_run_false_by_default(self, tmp_path: Path, agent_module):
        """Verify dry_run is False by default."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.dry_run is False

    def test_dry_run_mode_logged(self, tmp_path: Path, agent_module, caplog):
        """Verify dry-run mode is logged when enabled."""
        (tmp_path / ".git").mkdir()
        with caplog.at_level(logging.INFO):
            agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        assert "DRY RUN MODE" in caplog.text


class TestSelectiveAgentExecution:
    """Test selective agent execution (--only-agents)."""

    def test_selective_agents_stored_as_set(self, tmp_path: Path, agent_module):
        """Verify selective agents are stored as a set."""
        (tmp_path / ".git").mkdir()
        agents = ['coder', 'tests']
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=agents
        )
        assert isinstance(agent.selective_agents, set)
        assert agent.selective_agents == {'coder', 'tests'}

    def test_selective_agents_none_by_default(self, tmp_path: Path, agent_module):
        """Verify selective_agents is empty set by default."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.selective_agents == set()

    def test_should_execute_agent_returns_true_when_no_filter(self, tmp_path: Path, agent_module):
        """Verify all agents execute when no selective filter applied."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        assert agent.should_execute_agent('coder') is True
        assert agent.should_execute_agent('tests') is True
        assert agent.should_execute_agent('documentation') is True

    def test_should_execute_agent_respects_filter(self, tmp_path: Path, agent_module):
        """Verify selective filter is respected."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=['coder', 'tests']
        )
        
        assert agent.should_execute_agent('coder') is True
        assert agent.should_execute_agent('tests') is True
        assert agent.should_execute_agent('documentation') is False

    def test_should_execute_agent_case_insensitive(self, tmp_path: Path, agent_module):
        """Verify agent name matching is case-insensitive."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=['coder']
        )
        
        assert agent.should_execute_agent('CODER') is True
        assert agent.should_execute_agent('Coder') is True
        assert agent.should_execute_agent('coder') is True


class TestConfigurableTimeouts:
    """Test per-agent timeout configuration."""

    def test_timeout_per_agent_stored(self, tmp_path: Path, agent_module):
        """Verify timeout_per_agent dict is stored correctly."""
        (tmp_path / ".git").mkdir()
        timeouts = {'coder': 60, 'tests': 300}
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent=timeouts
        )
        assert agent.timeout_per_agent == timeouts

    def test_timeout_per_agent_defaults_to_empty_dict(self, tmp_path: Path, agent_module):
        """Verify timeout_per_agent defaults to empty dict."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.timeout_per_agent == {}

    def test_get_timeout_for_agent_returns_configured_value(self, tmp_path: Path, agent_module):
        """Verify configured timeout is returned."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent={'coder': 60}
        )
        assert agent.get_timeout_for_agent('coder') == 60

    def test_get_timeout_for_agent_returns_default(self, tmp_path: Path, agent_module):
        """Verify default timeout returned for unconfigured agent."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent={'coder': 60}
        )
        assert agent.get_timeout_for_agent('tests', default=120) == 120


class TestMetricsTracking:
    """Test metrics collection and reporting."""

    def test_metrics_initialized(self, tmp_path: Path, agent_module):
        """Verify metrics dict is initialized."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        assert 'files_processed' in agent.metrics
        assert 'files_modified' in agent.metrics
        assert 'agents_applied' in agent.metrics
        assert 'start_time' in agent.metrics

    def test_metrics_counters_start_at_zero(self, tmp_path: Path, agent_module):
        """Verify metrics counters initialized to zero."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        assert agent.metrics['files_processed'] == 0
        assert agent.metrics['files_modified'] == 0
        assert agent.metrics['agents_applied'] == {}

    def test_print_metrics_summary_sets_end_time(self, tmp_path: Path, agent_module, capsys):
        """Verify print_metrics_summary sets end_time."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.print_metrics_summary()
        assert agent.metrics['end_time'] is not None


# ============================================================================
# PHASE 4B: ADVANCED FEATURES (SNAPSHOTS, CASCADING IGNORES, ROLLBACK)
# ============================================================================

class TestFileSnapshots:
    """Test file snapshot creation and restoration."""

    def test_create_file_snapshot_returns_snapshot_id(self, tmp_path: Path, agent_module):
        """Verify snapshot creation returns a snapshot ID."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("original content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        assert snapshot_id is not None
        assert isinstance(snapshot_id, str)

    def test_create_file_snapshot_creates_snapshot_directory(self, tmp_path: Path, agent_module):
        """Verify .agent_snapshots directory is created."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path  # Override to use temp path
        snapshot_dir = tmp_path / ".agent_snapshots"
        
        agent.create_file_snapshot(file_path)
        assert snapshot_dir.exists()

    def test_restore_from_snapshot_returns_false_for_invalid_snapshot(self, tmp_path: Path, agent_module):
        """Verify False returned for invalid snapshot IDs."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        result = agent.restore_from_snapshot(file_path, "invalid_snapshot_id")
        
        assert result is False


class TestCascadingCodeignore:
    """Test cascading .codeignore pattern loading."""

    def test_load_cascading_codeignore_loads_root_patterns(self, tmp_path: Path, agent_module):
        """Verify root .codeignore patterns are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n__pycache__/\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore()
        
        assert "*.log" in patterns
        assert "__pycache__/" in patterns

    def test_load_cascading_codeignore_loads_subdirectory_patterns(self, tmp_path: Path, agent_module):
        """Verify patterns from subdirectory .codeignore are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / ".codeignore").write_text("*.tmp\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(src_dir)
        
        # Should include patterns from both root and subdirectory
        assert "*.log" in patterns
        assert "*.tmp" in patterns


# ============================================================================
# PHASE 4C: PARALLEL EXECUTION (ASYNC, MULTIPROCESSING, WEBHOOKS, CALLBACKS)
# ============================================================================

class TestAsyncFileProcessing:
    """Test async file processing."""

    def test_enable_async_flag(self, tmp_path: Path, agent_module):
        """Verify enable_async flag can be set."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), enable_async=True)
        assert agent.enable_async is True


class TestMultiprocessingExecution:
    """Test multiprocessing file processing."""

    def test_process_files_multiprocessing_exists(self, tmp_path: Path, agent_module):
        """Verify process_files_multiprocessing method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'process_files_multiprocessing')
        assert callable(agent.process_files_multiprocessing)

    def test_multiprocessing_flag(self, tmp_path: Path, agent_module):
        """Verify multiprocessing flag can be set."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), enable_multiprocessing=True)
        assert agent.enable_multiprocessing is True


class TestWebhookSupport:
    """Test webhook functionality."""

    def test_register_webhook(self, tmp_path: Path, agent_module):
        """Verify webhook registration works."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.register_webhook("https://example.com/webhook")
        assert "https://example.com/webhook" in agent.webhooks

    def test_send_webhook_notification_exists(self, tmp_path: Path, agent_module):
        """Verify send_webhook_notification method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'send_webhook_notification')


class TestCallbackSupport:
    """Test callback functionality."""

    def test_register_callback(self, tmp_path: Path, agent_module):
        """Verify callback registration works."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        def my_callback(event):
            pass
        
        agent.register_callback(my_callback)
        assert len(agent.callbacks) > 0

    def test_execute_callbacks_exists(self, tmp_path: Path, agent_module):
        """Verify execute_callbacks method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'execute_callbacks')


# ============================================================================
# PHASE 5: REPORTING & MONITORING
# ============================================================================

class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_circuit_breaker_initialization(self, agent_module):
        """Test circuit breaker initialization with defaults."""
        cb = agent_module.CircuitBreaker("test_backend")
        
        assert cb.name == "test_backend"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_custom_parameters(self, agent_module):
        """Test circuit breaker with custom parameters."""
        cb = agent_module.CircuitBreaker(
            "service",
            failure_threshold=3,
            recovery_timeout=30,
            backoff_multiplier=1.5
        )
        
        assert cb.failure_threshold == 3
        assert cb.recovery_timeout == 30
        assert cb.backoff_multiplier == 1.5

    def test_circuit_breaker_success_call(self, agent_module):
        """Test successful call through circuit breaker."""
        cb = agent_module.CircuitBreaker("test")
        
        def successful_func():
            return "success"
        
        result = cb.call(successful_func)
        
        assert result == "success"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_failure_call(self, agent_module):
        """Test failed call through circuit breaker."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=3)
        
        def failing_func():
            raise Exception("Service down")
        
        with pytest.raises(Exception):
            cb.call(failing_func)
        
        assert cb.failure_count == 1
        assert cb.state == "CLOSED"

    def test_circuit_breaker_opens_after_threshold(self, agent_module):
        """Test circuit opens after failure threshold exceeded."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=2)
        
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

    def test_circuit_breaker_fast_fail_when_open(self, agent_module):
        """Test circuit fails immediately when open."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=1)
        
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

    def test_circuit_breaker_recovery(self, agent_module):
        """Test circuit breaker recovery from OPEN to CLOSED."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)
        
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


class TestReportGeneration:
    """Tests for improvement report generation."""

    def test_generate_improvement_report(self, tmp_path: Path, agent_module):
        """Test basic improvement report generation."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
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

    def test_generate_improvement_report_includes_mode_info(self, tmp_path: Path, agent_module):
        """Test report includes execution mode information."""
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True, enable_async=True)
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


class TestBenchmarking:
    """Tests for execution benchmarking."""

    def test_benchmark_execution(self, tmp_path: Path, agent_module):
        """Test execution benchmarking."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
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


class TestCostAnalysis:
    """Tests for cost analysis."""

    def test_cost_analysis_basic(self, tmp_path: Path, agent_module):
        """Test basic cost analysis."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
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

    def test_cost_analysis_different_backend(self, tmp_path: Path, agent_module):
        """Test cost analysis with different backend pricing."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 5,
            'agents_applied': {'coder': 3},
            'start_time': 0.0,
            'end_time': 5.0,
        }
        
        analysis = agent.cost_analysis(backend='openai', cost_per_request=0.001)
        
        assert analysis['backend'] == 'openai'
        assert analysis['cost_per_request'] == 0.001


class TestSnapshotCleanup:
    """Tests for snapshot cleanup functionality."""

    def test_cleanup_old_snapshots_no_directory(self, tmp_path: Path, agent_module):
        """Test cleanup handles missing snapshot directory gracefully."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        # No snapshot directory exists
        cleaned = agent.cleanup_old_snapshots()
        
        assert cleaned == 0

    def test_cleanup_old_snapshots_empty_directory(self, tmp_path: Path, agent_module):
        """Test cleanup with empty snapshot directory."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path
        
        snapshot_dir = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()
        
        cleaned = agent.cleanup_old_snapshots()
        
        assert cleaned == 0

    def test_cleanup_old_snapshots_removes_old_files(self, tmp_path: Path, agent_module):
        """Test cleanup removes snapshots older than threshold."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path
        
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


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPhase5Integration:
    """Integration tests for Phase 5 features."""

    def test_circuit_breaker_with_agent_execution(self, tmp_path: Path, agent_module):
        """Test circuit breaker integration with agent."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        cb = agent_module.CircuitBreaker("test_backend")
        
        def run_agent():
            return agent.generate_improvement_report()
        
        report = cb.call(run_agent)
        
        assert 'summary' in report
        assert cb.state == "CLOSED"

    def test_full_phase5_workflow(self, tmp_path: Path, agent_module):
        """Test complete Phase 5 workflow."""
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=False)
        
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


# ============================================================================
# EDGE CASES & ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling across all phases."""

    def test_circuit_breaker_call_with_arguments(self, agent_module):
        """Test circuit breaker with function arguments."""
        cb = agent_module.CircuitBreaker("test")
        
        def func_with_args(a, b, c=None):
            return f"{a}+{b}+{c}"
        
        result = cb.call(func_with_args, 1, 2, c=3)
        
        assert result == "1+2+3"

    def test_cost_analysis_with_zero_files(self, tmp_path: Path, agent_module):
        """Test cost analysis with no files processed."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 0,
            'agents_applied': {},
            'start_time': 0.0,
            'end_time': 1.0,
        }
        
        cost = agent.cost_analysis()
        
        # Should not divide by zero
        assert cost['cost_per_file'] == 0

    def test_circuit_breaker_multiple_state_transitions(self, agent_module):
        """Test multiple state transitions."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)
        
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


# ============================================================================
# PHASE 6: PLUGIN SYSTEM, RATE LIMITING, CONFIG FILES, ADVANCED FEATURES
# ============================================================================


class TestAgentExecutionStateEnum:
    """Test AgentExecutionState enum."""
    
    def test_enum_values_exist(self, agent_module):
        """Verify all execution state values exist."""
        states = agent_module.AgentExecutionState
        assert states.PENDING is not None
        assert states.RUNNING is not None
        assert states.COMPLETED is not None
        assert states.FAILED is not None
        assert states.CANCELLED is not None
        assert states.PAUSED is not None
    
    def test_enum_values_are_unique(self, agent_module):
        """Verify enum values are unique."""
        states = agent_module.AgentExecutionState
        values = [s.value for s in states]
        assert len(values) == len(set(values))


class TestRateLimitStrategyEnum:
    """Test RateLimitStrategy enum."""
    
    def test_all_strategies_exist(self, agent_module):
        """Verify all rate limit strategies exist."""
        strategies = agent_module.RateLimitStrategy
        assert strategies.FIXED_WINDOW is not None
        assert strategies.SLIDING_WINDOW is not None
        assert strategies.TOKEN_BUCKET is not None
        assert strategies.LEAKY_BUCKET is not None


class TestConfigFormatEnum:
    """Test ConfigFormat enum."""
    
    def test_all_formats_exist(self, agent_module):
        """Verify all config formats exist."""
        formats = agent_module.ConfigFormat
        assert formats.YAML is not None
        assert formats.TOML is not None
        assert formats.JSON is not None
        assert formats.INI is not None


class TestLockTypeEnum:
    """Test LockType enum."""
    
    def test_all_lock_types_exist(self, agent_module):
        """Verify all lock types exist."""
        locks = agent_module.LockType
        assert locks.SHARED is not None
        assert locks.EXCLUSIVE is not None
        assert locks.ADVISORY is not None


class TestDiffOutputFormatEnum:
    """Test DiffOutputFormat enum."""
    
    def test_all_formats_exist(self, agent_module):
        """Verify all diff output formats exist."""
        formats = agent_module.DiffOutputFormat
        assert formats.UNIFIED is not None
        assert formats.CONTEXT is not None
        assert formats.SIDE_BY_SIDE is not None
        assert formats.HTML is not None


class TestAgentPriorityEnum:
    """Test AgentPriority enum."""
    
    def test_all_priorities_exist(self, agent_module):
        """Verify all priority levels exist."""
        priorities = agent_module.AgentPriority
        assert priorities.CRITICAL is not None
        assert priorities.HIGH is not None
        assert priorities.NORMAL is not None
        assert priorities.LOW is not None
        assert priorities.BACKGROUND is not None
    
    def test_priority_ordering(self, agent_module):
        """Verify priority ordering is correct."""
        priorities = agent_module.AgentPriority
        assert priorities.CRITICAL.value < priorities.HIGH.value
        assert priorities.HIGH.value < priorities.NORMAL.value
        assert priorities.NORMAL.value < priorities.LOW.value
        assert priorities.LOW.value < priorities.BACKGROUND.value


class TestHealthStatusEnum:
    """Test HealthStatus enum."""
    
    def test_all_statuses_exist(self, agent_module):
        """Verify all health statuses exist."""
        statuses = agent_module.HealthStatus
        assert statuses.HEALTHY is not None
        assert statuses.DEGRADED is not None
        assert statuses.UNHEALTHY is not None
        assert statuses.UNKNOWN is not None


class TestRateLimitConfigDataclass:
    """Test RateLimitConfig dataclass."""
    
    def test_default_values(self, agent_module):
        """Verify default values are set correctly."""
        config = agent_module.RateLimitConfig()
        assert config.requests_per_second == 10.0
        assert config.requests_per_minute == 60
        assert config.burst_size == 10
        assert config.cooldown_seconds == 1.0
    
    def test_custom_values(self, agent_module):
        """Verify custom values can be set."""
        config = agent_module.RateLimitConfig(
            requests_per_second=5.0,
            requests_per_minute=30,
            burst_size=5,
            cooldown_seconds=0.5
        )
        assert config.requests_per_second == 5.0
        assert config.requests_per_minute == 30
        assert config.burst_size == 5
        assert config.cooldown_seconds == 0.5


class TestAgentPluginConfigDataclass:
    """Test AgentPluginConfig dataclass."""
    
    def test_required_fields(self, agent_module):
        """Verify required fields are enforced."""
        config = agent_module.AgentPluginConfig(
            name="test_plugin",
            module_path="/path/to/plugin.py"
        )
        assert config.name == "test_plugin"
        assert config.module_path == "/path/to/plugin.py"
        assert config.entry_point == "run"
        assert config.enabled is True
    
    def test_custom_priority(self, agent_module):
        """Verify custom priority can be set."""
        config = agent_module.AgentPluginConfig(
            name="critical_plugin",
            module_path="/path/to/plugin.py",
            priority=agent_module.AgentPriority.CRITICAL
        )
        assert config.priority == agent_module.AgentPriority.CRITICAL


class TestFileLockDataclass:
    """Test FileLock dataclass."""
    
    def test_file_lock_creation(self, tmp_path: Path, agent_module):
        """Verify FileLock can be created."""
        lock = agent_module.FileLock(
            file_path=tmp_path / "test.py",
            lock_type=agent_module.LockType.EXCLUSIVE,
            owner="test_owner",
            acquired_at=time.time()
        )
        assert lock.file_path == tmp_path / "test.py"
        assert lock.lock_type == agent_module.LockType.EXCLUSIVE
        assert lock.owner == "test_owner"
        assert lock.expires_at is None


class TestDiffResultDataclass:
    """Test DiffResult dataclass."""
    
    def test_diff_result_creation(self, tmp_path: Path, agent_module):
        """Verify DiffResult can be created."""
        result = agent_module.DiffResult(
            file_path=tmp_path / "test.py",
            original_content="old content",
            modified_content="new content"
        )
        assert result.file_path == tmp_path / "test.py"
        assert result.original_content == "old content"
        assert result.modified_content == "new content"
        assert result.additions == 0
        assert result.deletions == 0


class TestIncrementalStateDataclass:
    """Test IncrementalState dataclass."""
    
    def test_default_values(self, agent_module):
        """Verify default values are set correctly."""
        state = agent_module.IncrementalState()
        assert state.last_run_timestamp == 0.0
        assert state.processed_files == {}
        assert state.file_hashes == {}
        assert state.pending_files == []


class TestAgentHealthCheckDataclass:
    """Test AgentHealthCheck dataclass."""
    
    def test_health_check_creation(self, agent_module):
        """Verify AgentHealthCheck can be created."""
        check = agent_module.AgentHealthCheck(
            agent_name="coder",
            status=agent_module.HealthStatus.HEALTHY,
            response_time_ms=50.0
        )
        assert check.agent_name == "coder"
        assert check.status == agent_module.HealthStatus.HEALTHY
        assert check.response_time_ms == 50.0
        assert check.error_message is None


class TestShutdownStateDataclass:
    """Test ShutdownState dataclass."""
    
    def test_default_values(self, agent_module):
        """Verify default values are set correctly."""
        state = agent_module.ShutdownState()
        assert state.shutdown_requested is False
        assert state.current_file is None
        assert state.completed_files == []
        assert state.pending_files == []


class TestRateLimiter:
    """Test RateLimiter class."""
    
    def test_rate_limiter_creation(self, agent_module):
        """Verify RateLimiter can be created."""
        limiter = agent_module.RateLimiter()
        assert limiter.config is not None
        assert limiter.tokens > 0
    
    def test_acquire_token(self, agent_module):
        """Verify token can be acquired."""
        limiter = agent_module.RateLimiter()
        result = limiter.acquire(timeout=1.0)
        assert result is True
    
    def test_get_stats(self, agent_module):
        """Verify stats can be retrieved."""
        limiter = agent_module.RateLimiter()
        stats = limiter.get_stats()
        assert 'tokens_available' in stats
        assert 'requests_last_minute' in stats
        assert 'requests_per_second' in stats
        assert 'burst_size' in stats
    
    def test_custom_config(self, agent_module):
        """Verify custom config is applied."""
        config = agent_module.RateLimitConfig(
            requests_per_second=1.0,
            burst_size=2
        )
        limiter = agent_module.RateLimiter(config)
        assert limiter.config.requests_per_second == 1.0
        assert limiter.config.burst_size == 2


class TestFileLockManager:
    """Test FileLockManager class."""
    
    def test_lock_manager_creation(self, agent_module):
        """Verify FileLockManager can be created."""
        manager = agent_module.FileLockManager()
        assert manager.lock_timeout == 300.0
        assert manager.locks == {}
    
    def test_acquire_and_release_lock(self, tmp_path: Path, agent_module):
        """Verify lock can be acquired and released."""
        manager = agent_module.FileLockManager()
        test_file = tmp_path / "test.py"
        test_file.write_text("test")
        
        lock = manager.acquire_lock(test_file)
        assert lock is not None
        assert lock.lock_type == agent_module.LockType.EXCLUSIVE
        
        result = manager.release_lock(test_file)
        assert result is True
    
    def test_shared_lock_allows_multiple(self, tmp_path: Path, agent_module):
        """Verify shared locks can coexist."""
        manager = agent_module.FileLockManager()
        test_file = tmp_path / "test.py"
        test_file.write_text("test")
        
        lock1 = manager.acquire_lock(test_file, lock_type=agent_module.LockType.SHARED)
        assert lock1 is not None
        
        lock2 = manager.acquire_lock(test_file, lock_type=agent_module.LockType.SHARED)
        assert lock2 is not None


class TestDiffGenerator:
    """Test DiffGenerator class."""
    
    def test_diff_generator_creation(self, agent_module):
        """Verify DiffGenerator can be created."""
        generator = agent_module.DiffGenerator()
        assert generator.output_format == agent_module.DiffOutputFormat.UNIFIED
        assert generator.context_lines == 3
    
    def test_generate_diff(self, tmp_path: Path, agent_module):
        """Verify diff can be generated."""
        generator = agent_module.DiffGenerator()
        test_file = tmp_path / "test.py"
        
        result = generator.generate_diff(
            test_file,
            "line1\nline2\nline3",
            "line1\nmodified\nline3"
        )
        
        assert result.file_path == test_file
        assert result.additions > 0 or result.deletions > 0
        assert len(result.diff_lines) > 0
    
    def test_format_diff_unified(self, tmp_path: Path, agent_module):
        """Verify unified diff format works."""
        generator = agent_module.DiffGenerator()
        test_file = tmp_path / "test.py"
        
        diff_result = generator.generate_diff(
            test_file,
            "old",
            "new"
        )
        
        formatted = generator.format_diff(diff_result)
        assert isinstance(formatted, str)
    
    def test_format_diff_html(self, tmp_path: Path, agent_module):
        """Verify HTML diff format works."""
        generator = agent_module.DiffGenerator()
        test_file = tmp_path / "test.py"
        
        diff_result = generator.generate_diff(
            test_file,
            "old",
            "new"
        )
        
        formatted = generator.format_diff(
            diff_result, 
            agent_module.DiffOutputFormat.HTML
        )
        assert '<html>' in formatted.lower() or '<table' in formatted.lower()


class TestIncrementalProcessor:
    """Test IncrementalProcessor class."""
    
    def test_processor_creation(self, tmp_path: Path, agent_module):
        """Verify IncrementalProcessor can be created."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        assert processor.repo_root == tmp_path
        assert processor.state is not None
    
    def test_get_changed_files_all_new(self, tmp_path: Path, agent_module):
        """Verify all files are returned when none processed."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        
        file1 = tmp_path / "test1.py"
        file2 = tmp_path / "test2.py"
        file1.write_text("test1")
        file2.write_text("test2")
        
        changed = processor.get_changed_files([file1, file2])
        assert len(changed) == 2
    
    def test_mark_processed(self, tmp_path: Path, agent_module):
        """Verify file can be marked as processed."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("test")
        
        processor.mark_processed(test_file)
        
        assert str(test_file) in processor.state.processed_files
        assert str(test_file) in processor.state.file_hashes
    
    def test_reset_state(self, tmp_path: Path, agent_module):
        """Verify state can be reset."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("test")
        
        processor.mark_processed(test_file)
        processor.reset_state()
        
        assert processor.state.processed_files == {}
        assert processor.state.file_hashes == {}


class TestGracefulShutdown:
    """Test GracefulShutdown class."""
    
    def test_shutdown_creation(self, tmp_path: Path, agent_module):
        """Verify GracefulShutdown can be created."""
        handler = agent_module.GracefulShutdown(tmp_path)
        assert handler.repo_root == tmp_path
        assert handler.state.shutdown_requested is False
    
    def test_should_continue_initially(self, tmp_path: Path, agent_module):
        """Verify should_continue returns True initially."""
        handler = agent_module.GracefulShutdown(tmp_path)
        assert handler.should_continue() is True
    
    def test_set_current_file(self, tmp_path: Path, agent_module):
        """Verify current file can be set."""
        handler = agent_module.GracefulShutdown(tmp_path)
        test_file = tmp_path / "test.py"
        
        handler.set_current_file(test_file)
        assert handler.state.current_file == str(test_file)
        
        handler.set_current_file(None)
        assert handler.state.current_file is None
    
    def test_mark_completed(self, tmp_path: Path, agent_module):
        """Verify file can be marked as completed."""
        handler = agent_module.GracefulShutdown(tmp_path)
        test_file = tmp_path / "test.py"
        
        handler.mark_completed(test_file)
        assert str(test_file) in handler.state.completed_files
    
    def test_set_pending_files(self, tmp_path: Path, agent_module):
        """Verify pending files can be set."""
        handler = agent_module.GracefulShutdown(tmp_path)
        files = [tmp_path / "test1.py", tmp_path / "test2.py"]
        
        handler.set_pending_files(files)
        assert len(handler.state.pending_files) == 2


class TestConfigLoader:
    """Test ConfigLoader class."""
    
    def test_loader_creation_without_path(self, agent_module):
        """Verify ConfigLoader can be created without path."""
        loader = agent_module.ConfigLoader()
        assert loader.config_path is None
    
    def test_loader_creation_with_json_path(self, tmp_path: Path, agent_module):
        """Verify ConfigLoader detects JSON format."""
        config_path = tmp_path / "config.json"
        loader = agent_module.ConfigLoader(config_path)
        assert loader.format == agent_module.ConfigFormat.JSON
    
    def test_loader_creation_with_yaml_path(self, tmp_path: Path, agent_module):
        """Verify ConfigLoader detects YAML format."""
        config_path = tmp_path / "config.yaml"
        loader = agent_module.ConfigLoader(config_path)
        assert loader.format == agent_module.ConfigFormat.YAML
    
    def test_load_json_config(self, tmp_path: Path, agent_module):
        """Verify JSON config can be loaded."""
        config_path = tmp_path / "config.json"
        config_path.write_text('{"repo_root": ".", "dry_run": true, "loop": 3}')
        
        loader = agent_module.ConfigLoader(config_path)
        config = loader.load()
        
        assert config.dry_run is True
        assert config.loop == 3
    
    def test_find_config_file(self, tmp_path: Path, agent_module):
        """Verify config file can be found."""
        config_path = tmp_path / "agent.json"
        config_path.write_text('{}')
        
        found = agent_module.ConfigLoader.find_config_file(tmp_path)
        assert found == config_path
    
    def test_find_config_file_not_found(self, tmp_path: Path, agent_module):
        """Verify None returned when no config found."""
        found = agent_module.ConfigLoader.find_config_file(tmp_path)
        assert found is None


class TestHealthChecker:
    """Test HealthChecker class."""
    
    def test_checker_creation(self, tmp_path: Path, agent_module):
        """Verify HealthChecker can be created."""
        checker = agent_module.HealthChecker(tmp_path)
        assert checker.repo_root == tmp_path
        assert checker.results == {}
    
    def test_check_python(self, tmp_path: Path, agent_module):
        """Verify Python check returns healthy."""
        checker = agent_module.HealthChecker(tmp_path)
        result = checker.check_python()
        
        assert result.agent_name == 'python'
        assert result.status == agent_module.HealthStatus.HEALTHY
        assert 'version' in result.details
    
    def test_check_git(self, tmp_path: Path, agent_module):
        """Verify git check runs."""
        checker = agent_module.HealthChecker(tmp_path)
        result = checker.check_git()
        
        assert result.agent_name == 'git'
        # May be healthy or unhealthy depending on git availability
        assert result.status in [
            agent_module.HealthStatus.HEALTHY,
            agent_module.HealthStatus.UNHEALTHY
        ]
    
    def test_run_all_checks(self, tmp_path: Path, agent_module):
        """Verify all checks can be run."""
        checker = agent_module.HealthChecker(tmp_path)
        results = checker.run_all_checks()
        
        assert 'python' in results
        assert 'git' in results
        # Agent scripts will be unhealthy in test environment
        assert 'coder' in results


class TestAgentPluginSystem:
    """Test Agent plugin system methods."""
    
    def test_register_plugin(self, tmp_path: Path, agent_module):
        """Verify plugin can be registered."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        # Create a mock plugin
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context):
                return True
        
        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)
        
        assert "test_plugin" in agent.plugins
    
    def test_unregister_plugin(self, tmp_path: Path, agent_module):
        """Verify plugin can be unregistered."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context):
                return True
        
        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)
        
        result = agent.unregister_plugin("test_plugin")
        assert result is True
        assert "test_plugin" not in agent.plugins
    
    def test_get_plugin(self, tmp_path: Path, agent_module):
        """Verify plugin can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context):
                return True
        
        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)
        
        retrieved = agent.get_plugin("test_plugin")
        assert retrieved is plugin


class TestAgentRateLimiting:
    """Test Agent rate limiting methods."""
    
    def test_enable_rate_limiting(self, tmp_path: Path, agent_module):
        """Verify rate limiting can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_rate_limiting()
        
        assert hasattr(agent, 'rate_limiter')
        assert agent.rate_limiter is not None
    
    def test_enable_rate_limiting_with_config(self, tmp_path: Path, agent_module):
        """Verify rate limiting can be enabled with custom config."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        config = agent_module.RateLimitConfig(requests_per_second=5.0)
        agent.enable_rate_limiting(config)
        
        assert agent.rate_limiter.config.requests_per_second == 5.0
    
    def test_get_rate_limit_stats(self, tmp_path: Path, agent_module):
        """Verify rate limit stats can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_rate_limiting()
        stats = agent.get_rate_limit_stats()
        
        assert 'tokens_available' in stats


class TestAgentFileLocking:
    """Test Agent file locking methods."""
    
    def test_enable_file_locking(self, tmp_path: Path, agent_module):
        """Verify file locking can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_file_locking()
        
        assert hasattr(agent, 'lock_manager')
        assert agent.lock_manager is not None
    
    def test_enable_file_locking_with_timeout(self, tmp_path: Path, agent_module):
        """Verify file locking can be enabled with custom timeout."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_file_locking(lock_timeout=600.0)
        
        assert agent.lock_manager.lock_timeout == 600.0


class TestAgentDiffPreview:
    """Test Agent diff preview methods."""
    
    def test_enable_diff_preview(self, tmp_path: Path, agent_module):
        """Verify diff preview can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_diff_preview()
        
        assert hasattr(agent, 'diff_generator')
        assert agent.diff_generator is not None
    
    def test_preview_changes(self, tmp_path: Path, agent_module):
        """Verify changes can be previewed."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        test_file = tmp_path / "test.py"
        test_file.write_text("old content")
        
        diff = agent.preview_changes(test_file, "new content")
        
        assert diff.original_content == "old content"
        assert diff.modified_content == "new content"


class TestAgentIncrementalProcessing:
    """Test Agent incremental processing methods."""
    
    def test_enable_incremental_processing(self, tmp_path: Path, agent_module):
        """Verify incremental processing can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_incremental_processing()
        
        assert hasattr(agent, 'incremental_processor')
        assert agent.incremental_processor is not None
    
    def test_get_changed_files(self, tmp_path: Path, agent_module):
        """Verify changed files can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_incremental_processing()
        
        file1 = tmp_path / "test1.py"
        file1.write_text("test")
        
        changed = agent.get_changed_files([file1])
        assert len(changed) == 1
    
    def test_reset_incremental_state(self, tmp_path: Path, agent_module):
        """Verify incremental state can be reset."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_incremental_processing()
        
        # Process a file
        file1 = tmp_path / "test1.py"
        file1.write_text("test")
        agent.incremental_processor.mark_processed(file1)
        
        # Reset
        agent.reset_incremental_state()
        
        assert agent.incremental_processor.state.processed_files == {}


class TestAgentGracefulShutdown:
    """Test Agent graceful shutdown methods."""
    
    def test_enable_graceful_shutdown(self, tmp_path: Path, agent_module):
        """Verify graceful shutdown can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        agent.enable_graceful_shutdown()
        
        assert hasattr(agent, 'shutdown_handler')
        assert agent.shutdown_handler is not None
    
    def test_resume_from_shutdown_no_state(self, tmp_path: Path, agent_module):
        """Verify None returned when no resume state."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        result = agent.resume_from_shutdown()
        assert result is None


class TestAgentHealthChecks:
    """Test Agent health check methods."""
    
    def test_run_health_checks(self, tmp_path: Path, agent_module):
        """Verify health checks can be run."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        results = agent.run_health_checks()
        
        assert 'python' in results
        assert 'git' in results
    
    def test_is_healthy(self, tmp_path: Path, agent_module):
        """Verify is_healthy returns boolean."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        result = agent.is_healthy()
        
        assert isinstance(result, bool)


class TestAgentConfigFile:
    """Test Agent configuration file methods."""
    
    def test_from_config_file(self, tmp_path: Path, agent_module):
        """Verify Agent can be created from config file."""
        config_path = tmp_path / "agent.json"
        config_path.write_text('{"repo_root": "' + str(tmp_path).replace('\\', '\\\\') + '", "dry_run": true}')
        (tmp_path / ".git").mkdir()
        
        agent = agent_module.Agent.from_config_file(config_path)
        
        assert agent.dry_run is True
    
    def test_auto_configure_no_config(self, tmp_path: Path, agent_module):
        """Verify auto_configure works without config file."""
        (tmp_path / ".git").mkdir()
        
        agent = agent_module.Agent.auto_configure(str(tmp_path))
        
        assert agent is not None
        assert agent.repo_root == tmp_path
    
    def test_auto_configure_with_config(self, tmp_path: Path, agent_module):
        """Verify auto_configure uses config file if found."""
        config_path = tmp_path / "agent.json"
        config_path.write_text('{"loop": 5}')
        (tmp_path / ".git").mkdir()
        
        agent = agent_module.Agent.auto_configure(str(tmp_path))
        
        assert agent.loop == 5


# ============================================================================
# PHASE 6 INTEGRATION TESTS
# ============================================================================


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""
    
    def test_full_phase6_workflow(self, tmp_path: Path, agent_module):
        """Test complete Phase 6 workflow."""
        (tmp_path / ".git").mkdir()
        
        # Create agent with all Phase 6 features
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        agent.enable_rate_limiting()
        agent.enable_file_locking()
        agent.enable_diff_preview()
        agent.enable_incremental_processing()
        agent.enable_graceful_shutdown()
        
        # Verify all features are enabled
        assert hasattr(agent, 'rate_limiter')
        assert hasattr(agent, 'lock_manager')
        assert hasattr(agent, 'diff_generator')
        assert hasattr(agent, 'incremental_processor')
        assert hasattr(agent, 'shutdown_handler')
    
    def test_config_with_rate_limiting(self, tmp_path: Path, agent_module):
        """Test config file with rate limiting."""
        config_path = tmp_path / "agent.json"
        config_content = '''
        {
            "repo_root": ".",
            "rate_limit": {
                "requests_per_second": 2.0,
                "burst_size": 5
            }
        }
        '''
        config_path.write_text(config_content)
        (tmp_path / ".git").mkdir()
        
        agent = agent_module.Agent.from_config_file(config_path)
        
        # Rate limiting should be enabled from config
        assert hasattr(agent, 'rate_limiter')
        assert agent.rate_limiter.config.requests_per_second == 2.0
    
    def test_plugin_execution_with_rate_limiting(self, tmp_path: Path, agent_module):
        """Test plugins execute with rate limiting."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_rate_limiting()
        
        # Create and register a mock plugin
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context):
                return True
        
        plugin = MockPlugin("test")
        agent.register_plugin(plugin)
        
        # Run plugins on a test file
        test_file = tmp_path / "test.py"
        test_file.write_text("# test")
        
        results = agent.run_plugins(test_file)
        
        assert 'test' in results
        assert results['test'] is True
    
    def test_health_check_before_run(self, tmp_path: Path, agent_module):
        """Test health check before agent run."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        # Run health checks
        results = agent.run_health_checks()
        
        # Check Python is healthy
        assert results['python'].status == agent_module.HealthStatus.HEALTHY
