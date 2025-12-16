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

"""Legacy tests for scripts/agent/agent.py.

These tests live next to the agent scripts so they can be run directly via:

    pytest scripts/agent/test_agent.py
"""

from __future__ import annotations
import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List
import pytest
from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def agent_module() -> ModuleType:
    with agent_dir_on_path():
        import agent
        return importlib.reload(agent)


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "README.md").write_text("# Test Repository", encoding="utf-8")
    return root


def test_agent_initialization_defaults(agent_module: ModuleType, repo_root: Path) -> None:
    a = agent_module.Agent(repo_root=str(repo_root))
    assert a.repo_root == repo_root
    assert a.agents_only is False
    assert a.max_files is None


def test_load_codeignore_ignores_comments(agent_module: ModuleType, repo_root: Path) -> None:
    (repo_root / ".codeignore").write_text("# Comment\n__pycache__\n*.tmp\n", encoding="utf-8")
    patterns = agent_module.load_codeignore(repo_root)
    assert "__pycache__" in patterns
    assert "*.tmp" in patterns
    assert "# Comment" not in patterns


def test_find_code_files_filters_extensions(agent_module: ModuleType, repo_root: Path) -> None:
    a = agent_module.Agent(repo_root=str(repo_root))
    (repo_root / "script.py").write_text("# Python script", encoding="utf-8")
    (repo_root / "module.js").write_text("// JavaScript module", encoding="utf-8")
    (repo_root / "readme.txt").write_text("Documentation", encoding="utf-8")
    files = a.find_code_files()
    names = {p.name for p in files}
    assert "script.py" in names
    assert "module.js" in names
    assert "readme.txt" not in names


def test_agents_only_filters_to_scripts_agent(agent_module: ModuleType, repo_root: Path) -> None:
    # Create a structure that looks like a repo.
    scripts_agent = repo_root / "scripts" / "agent"
    scripts_agent.mkdir(parents=True)
    (repo_root / "top.py").write_text("print('x')\n", encoding="utf-8")
    (scripts_agent / "inner.py").write_text("print('y')\n", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(repo_root), agents_only=True)
    files = a.find_code_files()
    assert all(p.is_relative_to(scripts_agent) for p in files)


def test_max_files_limits_results(agent_module: ModuleType, repo_root: Path) -> None:
    (repo_root / "a.py").write_text("print('a')\n", encoding="utf-8")
    (repo_root / "b.py").write_text("print('b')\n", encoding="utf-8")
    (repo_root / "c.py").write_text("print('c')\n", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(repo_root), max_files=2)
    assert len(a.find_code_files()) == 2


def test_is_ignored_matches_globs(agent_module: ModuleType, repo_root: Path) -> None:
    a = agent_module.Agent(repo_root=str(repo_root))
    a.ignored_patterns = {"__pycache__", "*.tmp"}
    cache_file = repo_root / "__pycache__" / "module.pyc"
    cache_file.parent.mkdir()
    cache_file.write_text("bytecode", encoding="utf-8")
    temp_file = repo_root / "temp.tmp"
    temp_file.write_text("temporary", encoding="utf-8")
    normal_file = repo_root / "normal.py"
    normal_file.write_text("normal", encoding="utf-8")
    assert a._is_ignored(cache_file)
    assert a._is_ignored(temp_file)
    assert not a._is_ignored(normal_file)


def test_run_stats_update_invokes_subprocess(agent_module: ModuleType, repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    called: Dict[str, Any] = {}

    def fake_run(cmd: List[str], **kwargs: Any) -> Any:
        called["cmd"] = cmd
        called["kwargs"] = kwargs

        class R:
            returncode = 0
        return R()

    monkeypatch.setattr(agent_module.subprocess, "run", fake_run, raising=True)
    sample_file = repo_root / "sample.py"
    sample_file.write_text("print('x')\n", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(repo_root))
    a.run_stats_update([sample_file])
    assert "agent-stats.py" in str(called["cmd"][1])
    assert called["kwargs"].get("cwd") == repo_root


def test_run_tests_no_test_file_does_not_invoke_subprocess(agent_module: ModuleType, repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("subprocess.run should not be called")

    monkeypatch.setattr(agent_module.subprocess, "run", boom, raising=True)
    sample_file = repo_root / "sample.py"
    sample_file.write_text("print('x')\n", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(repo_root))
    a.run_tests(sample_file)


def test_run_tests_with_test_file_invokes_pytest(agent_module: ModuleType, repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    called: Dict[str, Any] = {}

    def fake_run(cmd: List[str], **kwargs: Any) -> Any:
        called["cmd"] = cmd
        called["kwargs"] = kwargs

        class R:
            returncode = 0
            stdout = ""
            stderr = ""

        return R()

    monkeypatch.setattr(agent_module.subprocess, "run", fake_run, raising=True)
    sample_file = repo_root / "sample.py"
    sample_file.write_text("print('x')\n", encoding="utf-8")
    test_file = repo_root / "test_sample.py"
    test_file.write_text("def test_sample():\n    assert True\n", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(repo_root))
    a.run_tests(sample_file)
    cmd = called["cmd"]
    assert cmd[1:3] == ["-m", "pytest"]
    assert str(test_file) in cmd
    assert called["kwargs"].get("cwd") == repo_root


# ============================================================================
# PHASE 4A: CORE FEATURES (DRY-RUN, SELECTIVE AGENTS, TIMEOUTS, METRICS)
# ============================================================================

class TestDryRunMode:
    """Test dry-run mode functionality."""

    def test_dry_run_flag_set_on_init(self, tmp_path: Path):
        """Verify dry_run flag is set correctly on Agent initialization."""
        (tmp_path / ".git").mkdir()
        sys.path.insert(0, str(tmp_path.parent.parent / "scripts" / "agent"))
        try:
            import agent as agent_module
            agent_obj = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
            assert agent_obj.dry_run is True
        finally:
            sys.path.pop(0)

    def test_dry_run_false_by_default(self, tmp_path: Path):
        """Verify dry_run is False by default."""
        (tmp_path / ".git").mkdir()
        sys.path.insert(0, str(tmp_path.parent.parent / "scripts" / "agent"))
        try:
            import agent as agent_module
            agent_obj = agent_module.Agent(repo_root=str(tmp_path))
            assert agent_obj.dry_run is False
        finally:
            sys.path.pop(0)


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_circuit_breaker_initialization(self):
        """Test circuit breaker initialization with defaults."""
        # Import from agent module
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            import agent
            cb = agent.CircuitBreaker("test_backend")
            
            assert cb.name == "test_backend"
            assert cb.state == "CLOSED"
            assert cb.failure_count == 0
        finally:
            sys.path.pop(0)

    def test_circuit_breaker_success_call(self):
        """Test successful call through circuit breaker."""
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            import agent
            cb = agent.CircuitBreaker("test")
            
            def successful_func():
                return "success"
            
            result = cb.call(successful_func)
            
            assert result == "success"
            assert cb.state == "CLOSED"
            assert cb.failure_count == 0
        finally:
            sys.path.pop(0)


class TestReportGeneration:
    """Tests for improvement report generation."""

    def test_generate_improvement_report(self, tmp_path: Path):
        """Test basic improvement report generation."""
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            import agent
            agent_obj = agent.Agent(repo_root=str(tmp_path))
            agent_obj.metrics = {
                'files_processed': 10,
                'files_modified': 5,
                'agents_applied': {'coder': 4, 'tests': 3},
                'start_time': 0.0,
                'end_time': 10.0,
            }
            
            report = agent_obj.generate_improvement_report()
            
            assert report['summary']['files_processed'] == 10
            assert report['summary']['files_modified'] == 5
        finally:
            sys.path.pop(0)


class TestCostAnalysis:
    """Tests for cost analysis."""

    def test_cost_analysis_basic(self, tmp_path: Path):
        """Test basic cost analysis."""
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            import agent
            agent_obj = agent.Agent(repo_root=str(tmp_path))
            agent_obj.metrics = {
                'files_processed': 10,
                'agents_applied': {'coder': 8, 'tests': 7},
                'start_time': 0.0,
                'end_time': 10.0,
            }
            
            analysis = agent_obj.cost_analysis(backend='github-models', cost_per_request=0.0001)
            
            assert analysis['backend'] == 'github-models'
            assert analysis['files_processed'] == 10
        finally:
            sys.path.pop(0)

