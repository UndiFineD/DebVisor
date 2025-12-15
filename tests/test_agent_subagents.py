from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def base_agent_module():
    with agent_sys_path():
        # Import the module by its canonical name so patches apply to agents
        # that do `from base_agent import BaseAgent`.
        mod = importlib.import_module("base_agent")
        return importlib.reload(mod)


def _load_agent_script(name: str, filename: str):
    with agent_sys_path():
        return load_module_from_path(name, AGENT_DIR / filename)


def test_changes_agent_keyword_prompt_generates_suggestions(tmp_path: Path):
    mod = _load_agent_script("_dv_agent_changes", "agent-changes.py")

    target = tmp_path / "x.changes.md"
    agent = mod.ChangesAgent(str(target))
    agent.previous_content = "ORIGINAL"

    out = agent.improve_content("Please improve the changelog")
    assert "AI Changelog Improvement Suggestions" in out
    assert "ORIGINAL" in out


def test_changes_agent_non_keyword_delegates_to_base(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    mod = _load_agent_script("_dv_agent_changes2", "agent-changes.py")

    # Patch BaseAgent.run_subagent to produce deterministic output for the super() call
    def fake_run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True)

    target = tmp_path / "x.changes.md"
    target.write_text("BEFORE", encoding="utf-8")

    agent = mod.ChangesAgent(str(target))
    agent.read_previous_content()
    out = agent.improve_content("noop")
    assert out == "IMPROVED"


def test_coder_agent_keyword_prompt_generates_suggestions(tmp_path: Path):
    mod = _load_agent_script("_dv_agent_coder", "agent-coder.py")

    target = tmp_path / "x.py"
    agent = mod.CoderAgent(str(target))
    agent.previous_content = "ORIGINAL"

    out = agent.improve_content("Improve this code")
    assert "AI Code Improvement Suggestions" in out
    assert "ORIGINAL" in out


def test_context_errors_improvements_agents_delegate_to_base(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    def fake_run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True)

    for filename, cls_name in [
        ("agent-context.py", "ContextAgent"),
        ("agent-errors.py", "ErrorsAgent"),
        ("agent-improvements.py", "ImprovementsAgent"),
    ]:
        mod = _load_agent_script(f"_dv_{filename}", filename)
        target = tmp_path / f"{filename}.md"
        target.write_text("BEFORE", encoding="utf-8")
        agent_cls = getattr(mod, cls_name)
        agent = agent_cls(str(target))
        agent.read_previous_content()
        assert agent.improve_content("prompt") == "IMPROVED"


def test_tests_agent_update_file_does_not_fix_markdown(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    mod = _load_agent_script("_dv_agent_tests", "agent-tests.py")

    target = tmp_path / "test_something.py"
    agent = mod.TestsAgent(str(target))
    agent.current_content = "print('hi')\n"

    # If markdown fixer were called, we'd see it here, but TestsAgent.update_file
    # overrides BaseAgent.update_file and writes raw.
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "print('hi')\n"
