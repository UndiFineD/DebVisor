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

"""Legacy tests for agent-stats.py."""

from __future__ import annotations
from pathlib import Path
from agent_test_utils import agent_dir_on_path, load_agent_module


def test_stats_agent_counts_files(tmp_path: Path):
    with agent_dir_on_path():
        mod = load_agent_module("agent-stats.py")

    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_text("print('a')\n", encoding="utf-8")
    b.write_text("print('b')\n", encoding="utf-8")

    # Only `a` has companions.
    (tmp_path / "a.description.md").write_text("desc", encoding="utf-8")
    (tmp_path / "a.changes.md").write_text("chg", encoding="utf-8")
    (tmp_path / "a.errors.md").write_text("err", encoding="utf-8")
    (tmp_path / "a.improvements.md").write_text("imp", encoding="utf-8")
    (tmp_path / "test_a.py").write_text("def test_a():\n    assert True\n", encoding="utf-8")

    agent = mod.StatsAgent([str(a), str(b)])
    stats = agent.calculate_stats()

    assert stats["total_files"] == 2
    assert stats["files_with_context"] == 1
    assert stats["files_with_changes"] == 1
    assert stats["files_with_errors"] == 1
    assert stats["files_with_improvements"] == 1
    assert stats["files_with_tests"] == 1
