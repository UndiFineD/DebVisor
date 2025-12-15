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
from typing import Any, Dict, List, Optional, Union
import pytest
from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


def test_read_previous_content_existing_file(tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "x.md"
    target.write_text("HELLO", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() == "HELLO"


def test_read_previous_content_missing_file_uses_default(tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "missing.md"
    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    assert "Default content" in content


def test_improve_content_uses_run_subagent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "x.md"
    target.write_text("BEFORE", encoding="utf-8")

    def fake_run_subagent(self: Any, description: str, prompt: str, original_content: str = "") -> str:
        assert "Improve" in description
        assert prompt == "prompt"
        assert original_content == "BEFORE"
        return "AFTER"

    monkeypatch.setattr(base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True)
    agent = base_agent_module.BaseAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "AFTER"


def test_update_file_writes_content(tmp_path: Path, base_agent_module: Any) -> None:
    # Use a non-markdown extension so the markdown fixer won't interfere.
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.current_content = "CONTENT"
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "CONTENT"


def test_get_diff_contains_unified_markers(tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.previous_content = "A\n"
    agent.current_content = "B\n"
    diff = agent.get_diff()
    assert "--- previous" in diff
    assert "+++ current" in diff


def test_run_subagent_prefers_local_copilot_cli(monkeypatch: pytest.MonkeyPatch, base_agent_module: Any) -> None:
    calls: list[list[str]] = []

    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(args: List[str], **kwargs: Any) -> Result:
        # Record args only (not env/token).
        calls.append(list(args))
        # "copilot --version" probe succeeds.
        if args[:2] == ["copilot", "--version"]:
            return Result(0, "copilot 1.2.3")
        # Actual copilot invocation returns a response.
        if args and args[0] == "copilot":
            assert "--prompt" in args
            assert "--deny-tool" in args
            assert "--silent" in args
            return Result(0, "OK_FROM_COPILOT")
        raise AssertionError(f"Unexpected subprocess call: {args}")
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.subprocess, "run", fake_run)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "OK_FROM_COPILOT"
    assert calls[0][:2] == ["copilot", "--version"]


def test_run_subagent_falls_back_to_gh_copilot_explain(monkeypatch: pytest.MonkeyPatch, base_agent_module: Any) -> None:
    calls: list[list[str]] = []
    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(args: List[str], **kwargs: Any) -> Result:
        calls.append(list(args))
        # "copilot" missing.
        if args[:2] == ["copilot", "--version"]:
            raise FileNotFoundError("copilot not found")
        # "gh" is present.
        if args[:2] == ["gh", "--version"]:
            return Result(0, "gh version 2.x")
        # gh copilot explain returns text.
        if args[:3] == ["gh", "copilot", "explain"]:
            return Result(0, "EXPLAINED")
        raise AssertionError(f"Unexpected subprocess call: {args}")
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.subprocess, "run", fake_run)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "git status", "ORIG")
    assert "EXPLAINED" in out
    assert any(c[:3] == ["gh", "copilot", "explain"] for c in calls)


def test_llm_chat_via_github_models_builds_request_and_parses_response(
    monkeypatch: pytest.MonkeyPatch, base_agent_module: Any
) -> None:
    posted: Dict[str, Any] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> Dict[str, Any]:
            return {"choices": [{"message": {"content": "  hello  "}}]}

    def fake_post(url: str, headers: Optional[Dict[str, str]] = None, data: Optional[str] = None, timeout: Optional[int] = None) -> FakeResponse:
        posted["url"] = url
        posted["headers"] = headers
        posted["data"] = data
        posted["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(base_agent_module.requests, "post", fake_post)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.llm_chat_via_github_models(
        prompt="Say hi",
        model="some-model",
        system_prompt="system",
        base_url="https://example.test",
        token="TOKEN",
        timeout_s=12,
    )
    assert out == "hello"
    assert posted["url"] == "https://example.test/v1/chat/completions"
    assert posted["headers"]["Authorization"] == "Bearer TOKEN"
    assert posted["timeout"] == 12
    assert '"model": "some-model"' in posted["data"]
    assert '"role": "user"' in posted["data"]


def test_llm_chat_via_github_models_requires_token_and_base_url(base_agent_module: Any) -> None:
    agent = base_agent_module.BaseAgent("x.md")
    with pytest.raises(RuntimeError, match=r"Missing token"):
        agent.llm_chat_via_github_models(prompt="x", model="m", base_url="https://x", token=None)
    with pytest.raises(RuntimeError, match=r"Missing base URL"):
        agent.llm_chat_via_github_models(prompt="x", model="m", base_url=None, token="t")


def test_run_subagent_uses_github_models_backend(monkeypatch: pytest.MonkeyPatch, base_agent_module: Any) -> None:
    # Force backend selection.
    monkeypatch.setenv("DV_AGENT_BACKEND", "github-models")
    monkeypatch.setenv("GITHUB_MODELS_BASE_URL", "https://example.test")
    monkeypatch.setenv("DV_AGENT_MODEL", "unit-test-model")
    monkeypatch.setenv("GITHUB_TOKEN", "TOKEN")
    # If subprocess is used, fail.
    def boom(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("subprocess.run should not be called for github-models backend")
    monkeypatch.setattr(base_agent_module.subprocess, "run", boom)

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> Dict[str, Any]:
            return {"choices": [{"message": {"content": "OK_FROM_MODELS"}}]}

    def fake_post(url: str, headers: Optional[Dict[str, str]] = None, data: Optional[str] = None, timeout: Optional[int] = None) -> FakeResponse:
        assert url == "https://example.test/v1/chat/completions"
        assert headers is not None and headers["Authorization"] == "Bearer TOKEN"
        assert data is not None and '"model": "unit-test-model"' in data
        return FakeResponse()

    monkeypatch.setattr(base_agent_module.requests, "post", fake_post)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "OK_FROM_MODELS"
