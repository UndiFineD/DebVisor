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

"""Legacy tests for agent-improvements.py."""

from __future__ import annotations
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


def test_improvements_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-improvements.py")

    def fake_run_subagent(self: Any, description: str, prompt: str, original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True)
    target = tmp_path / "x.improvements.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ImprovementsAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "IMPROVED"
