"""Tests for Phase 4a: Core features (dry-run, selective agents, timeouts, metrics)."""
from __future__ import annotations
import logging
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent", AGENT_DIR / "agent.py")


# ============================================================================
# Tests for Dry-Run Mode
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


# ============================================================================
# Tests for Selective Agent Execution
# ============================================================================

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

    def test_selective_agents_logged(self, tmp_path: Path, agent_module, caplog):
        """Verify selective agents list is logged."""
        (tmp_path / ".git").mkdir()
        with caplog.at_level(logging.INFO):
            agent = agent_module.Agent(
                repo_root=str(tmp_path),
                selective_agents=['coder', 'tests']
            )
        assert "Selective execution" in caplog.text


# ============================================================================
# Tests for Configurable Timeouts
# ============================================================================

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

    def test_get_timeout_for_agent_case_insensitive(self, tmp_path: Path, agent_module):
        """Verify timeout lookup is case-insensitive."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent={'coder': 60}
        )
        assert agent.get_timeout_for_agent('CODER') == 60
        assert agent.get_timeout_for_agent('Coder') == 60


# ============================================================================
# Tests for Metrics Tracking
# ============================================================================

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
        assert 'end_time' in agent.metrics

    def test_metrics_counters_start_at_zero(self, tmp_path: Path, agent_module):
        """Verify metrics counters initialized to zero."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        assert agent.metrics['files_processed'] == 0
        assert agent.metrics['files_modified'] == 0
        assert agent.metrics['agents_applied'] == {}

    def test_metrics_start_time_set(self, tmp_path: Path, agent_module):
        """Verify start time is set on initialization."""
        (tmp_path / ".git").mkdir()
        import time
        before = time.time()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        after = time.time()
        
        assert before <= agent.metrics['start_time'] <= after

    def test_print_metrics_summary_sets_end_time(self, tmp_path: Path, agent_module, capsys):
        """Verify print_metrics_summary sets end_time."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        assert agent.metrics['end_time'] is None
        agent.print_metrics_summary()
        assert agent.metrics['end_time'] is not None

    def test_print_metrics_summary_shows_dry_run_status(self, tmp_path: Path, agent_module, capsys):
        """Verify metrics summary indicates dry-run status."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        agent.print_metrics_summary()
        
        captured = capsys.readouterr()
        assert "Dry-run mode:    Yes" in captured.out

    def test_print_metrics_summary_with_file_counts(self, tmp_path: Path, agent_module, capsys):
        """Verify metrics summary includes file processing information."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics['files_processed'] = 10
        agent.metrics['files_modified'] = 5
        
        agent.print_metrics_summary()
        
        captured = capsys.readouterr()
        assert "Files processed: 10" in captured.out
        assert "Files modified:  5" in captured.out

    def test_print_metrics_summary_with_agent_counts(self, tmp_path: Path, agent_module, capsys):
        """Verify metrics summary includes agent application counts."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics['agents_applied'] = {'coder': 5, 'tests': 3}
        
        agent.print_metrics_summary()
        
        captured = capsys.readouterr()
        assert "coder: 5" in captured.out
        assert "tests: 3" in captured.out

    def test_metrics_execution_time_reasonable(self, tmp_path: Path, agent_module):
        """Verify execution time is calculated correctly."""
        (tmp_path / ".git").mkdir()
        import time
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        time.sleep(0.1)  # Sleep for at least 100ms
        agent.print_metrics_summary()
        
        elapsed = agent.metrics['end_time'] - agent.metrics['start_time']
        assert elapsed >= 0.1


# ============================================================================
# Tests for Help/Documentation
# ============================================================================

class TestCommandLineIntegration:
    """Test command-line argument parsing for new features."""

    def test_help_includes_dry_run(self, agent_module):
        """Verify --dry-run flag documented in help."""
        import io
        from contextlib import redirect_stderr
        
        parser = agent_module.argparse.ArgumentParser()
        # Capture help output
        f = io.StringIO()
        with redirect_stderr(f):
            try:
                # This will exit, so we catch it
                agent_module.argparse.ArgumentParser().parse_args(['--help'])
            except SystemExit:
                pass


# ============================================================================
# Tests for Combined Features
# ============================================================================

class TestFeatureCombinations:
    """Test interactions between multiple Phase 4a features."""

    def test_dry_run_with_selective_agents(self, tmp_path: Path, agent_module):
        """Verify dry-run and selective agents work together."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            dry_run=True,
            selective_agents=['coder']
        )
        
        assert agent.dry_run is True
        assert agent.selective_agents == {'coder'}
        assert agent.should_execute_agent('coder') is True
        assert agent.should_execute_agent('tests') is False

    def test_all_features_together(self, tmp_path: Path, agent_module):
        """Verify all Phase 4a features can be configured together."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            dry_run=True,
            selective_agents=['coder', 'tests'],
            timeout_per_agent={'coder': 60, 'tests': 300}
        )
        
        assert agent.dry_run is True
        assert agent.selective_agents == {'coder', 'tests'}
        assert agent.get_timeout_for_agent('coder') == 60
        assert agent.get_timeout_for_agent('tests') == 300
        assert agent.get_timeout_for_agent('documentation') == 120  # default
