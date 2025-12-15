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
from pathlib import Path

import pytest

from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def agent_module():
    with agent_dir_on_path():
        import agent

        return importlib.reload(agent)


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "README.md").write_text("# Test Repository", encoding="utf-8")
    return root


def test_agent_initialization_defaults(agent_module, repo_root: Path):
    a = agent_module.Agent(repo_root=str(repo_root))
    assert a.repo_root == repo_root
    assert a.agents_only is False
    assert a.max_files is None


def test_load_codeignore_ignores_comments(agent_module, repo_root: Path):
    (repo_root / ".codeignore").write_text("# Comment\n__pycache__\n*.tmp\n", encoding="utf-8")
    patterns = agent_module.load_codeignore(repo_root)
    assert "__pycache__" in patterns
    assert "*.tmp" in patterns
    assert "# Comment" not in patterns


def test_find_code_files_filters_extensions(agent_module, repo_root: Path):
    a = agent_module.Agent(repo_root=str(repo_root))

    (repo_root / "script.py").write_text("# Python script", encoding="utf-8")
    (repo_root / "module.js").write_text("// JavaScript module", encoding="utf-8")
    (repo_root / "readme.txt").write_text("Documentation", encoding="utf-8")

    files = a.find_code_files()
    names = {p.name for p in files}

    assert "script.py" in names
    assert "module.js" in names
    assert "readme.txt" not in names


def test_agents_only_filters_to_scripts_agent(agent_module, repo_root: Path):
    # Create a structure that looks like a repo.
    scripts_agent = repo_root / "scripts" / "agent"
    scripts_agent.mkdir(parents=True)

    (repo_root / "top.py").write_text("print('x')\n", encoding="utf-8")
    (scripts_agent / "inner.py").write_text("print('y')\n", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(repo_root), agents_only=True)
    files = a.find_code_files()
    assert all(p.is_relative_to(scripts_agent) for p in files)


def test_max_files_limits_results(agent_module, repo_root: Path):
    (repo_root / "a.py").write_text("print('a')\n", encoding="utf-8")
    (repo_root / "b.py").write_text("print('b')\n", encoding="utf-8")
    (repo_root / "c.py").write_text("print('c')\n", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(repo_root), max_files=2)
    assert len(a.find_code_files()) == 2


def test_is_ignored_matches_globs(agent_module, repo_root: Path):
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


def test_run_stats_update_invokes_subprocess(agent_module, repo_root: Path, monkeypatch: pytest.MonkeyPatch):
    called = {}

    def fake_run(cmd, **kwargs):
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


def test_run_tests_no_test_file_does_not_invoke_subprocess(agent_module, repo_root: Path, monkeypatch: pytest.MonkeyPatch):
    def boom(*_args, **_kwargs):
        raise AssertionError("subprocess.run should not be called")

    monkeypatch.setattr(agent_module.subprocess, "run", boom, raising=True)

    sample_file = repo_root / "sample.py"
    sample_file.write_text("print('x')\n", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(repo_root))
    a.run_tests(sample_file)


def test_run_tests_with_test_file_invokes_pytest(agent_module, repo_root: Path, monkeypatch: pytest.MonkeyPatch):
    called = {}

    def fake_run(cmd, **kwargs):
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
