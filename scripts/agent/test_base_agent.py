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

"""Legacy tests for base_agent.py.

These live next to the agent scripts so they can be run directly via:

    pytest scripts/agent/test_base_agent.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def base_agent_module():
    with agent_dir_on_path():
        import base_agent

        return base_agent


def test_read_previous_content_existing_file(tmp_path: Path, base_agent_module):
    target = tmp_path / "x.md"
    target.write_text("HELLO", encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() == "HELLO"


def test_read_previous_content_missing_file_uses_default(tmp_path: Path, base_agent_module):
    target = tmp_path / "missing.md"

    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    assert "Default content" in content


def test_improve_content_uses_run_subagent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    target = tmp_path / "x.md"
    target.write_text("BEFORE", encoding="utf-8")

    def fake_run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        assert "Improve" in description
        assert prompt == "prompt"
        assert original_content == "BEFORE"
        return "AFTER"

    monkeypatch.setattr(base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True)

    agent = base_agent_module.BaseAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "AFTER"


def test_update_file_writes_content(tmp_path: Path, base_agent_module):
    # Use a non-markdown extension so the markdown fixer won't interfere.
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.current_content = "CONTENT"
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "CONTENT"


def test_get_diff_contains_unified_markers(tmp_path: Path, base_agent_module):
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.previous_content = "A\n"
    agent.current_content = "B\n"
    diff = agent.get_diff()
    assert "--- previous" in diff
    assert "+++ current" in diff
