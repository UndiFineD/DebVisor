from __future__ import annotations
import logging
import sys
from pathlib import Path
import pytest
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def base_agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_base_agent", AGENT_DIR / "base_agent.py")


def test_read_previous_content_existing(tmp_path: Path, base_agent_module):
    target = tmp_path / "file.md"
    target.write_text("hello", encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() == "hello"


def test_read_previous_content_missing_uses_default(tmp_path: Path, base_agent_module):
    target = tmp_path / "missing.md"

    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()

    assert "Default content" in content
    assert agent.previous_content == content


def test_improve_content_calls_run_subagent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    target = tmp_path / "doc.md"
    target.write_text("before", encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    agent.read_previous_content()

    def fake_run_subagent(description: str, prompt: str, original_content: str = "") -> str:
        assert "Improve" in description
        assert prompt == "do it"
        assert original_content == "before"
        return "after"

    monkeypatch.setattr(agent, "run_subagent", fake_run_subagent)

    assert agent.improve_content("do it") == "after"
    assert agent.current_content == "after"


def test_improve_content_on_exception_keeps_previous(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    target = tmp_path / "doc.md"
    target.write_text("before", encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    agent.read_previous_content()

    def boom(*args, **kwargs):
        raise RuntimeError("nope")

    monkeypatch.setattr(agent, "run_subagent", boom)

    assert agent.improve_content("prompt") == "before"
    assert agent.current_content == "before"


def test_update_file_applies_markdown_fix_only_for_markdown(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module):
    md = tmp_path / "x.md"
    py = tmp_path / "x.py"

    fixed = []

    def fake_fix(text: str) -> str:
        fixed.append(text)
        return text + "\nFIXED"

    monkeypatch.setattr(base_agent_module, "fix_markdown_content", fake_fix)

    agent_md = base_agent_module.BaseAgent(str(md))
    agent_md.current_content = "content"
    agent_md.update_file()
    assert md.read_text(encoding="utf-8").endswith("FIXED")
    assert fixed

    fixed.clear()
    agent_py = base_agent_module.BaseAgent(str(py))
    agent_py.current_content = "print('hi')"
    agent_py.update_file()
    assert py.read_text(encoding="utf-8") == "print('hi')"
    assert fixed == []


def test_get_diff_contains_changes(base_agent_module):
    agent = base_agent_module.BaseAgent("/tmp/does-not-matter")
    agent.previous_content = "a\n"
    agent.current_content = "b\n"
    diff = agent.get_diff()
    assert "-a" in diff
    assert "+b" in diff


def test_run_subagent_no_cli_returns_original(monkeypatch: pytest.MonkeyPatch, base_agent_module):
    # Ensure backend selection doesn't pick up host environment variables.
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.delenv("GITHUB_MODELS_BASE_URL", raising=False)
    monkeypatch.delenv("GITHUB_MODELS_MODEL", raising=False)
    monkeypatch.delenv("DV_AGENT_MODEL", raising=False)

    # Simulate both commands missing
    def fake_run(args, **kwargs):
        raise FileNotFoundError("missing")

    monkeypatch.setattr(base_agent_module.subprocess, "run", fake_run)

    agent = base_agent_module.BaseAgent("x.md")
    assert agent.run_subagent("desc", "prompt", "ORIG") == "ORIG"


def test_run_subagent_copilot_success(monkeypatch: pytest.MonkeyPatch, base_agent_module):
    # Ensure backend selection doesn't pick up host environment variables.
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.delenv("GITHUB_MODELS_BASE_URL", raising=False)
    monkeypatch.delenv("GITHUB_MODELS_MODEL", raising=False)
    monkeypatch.delenv("DV_AGENT_MODEL", raising=False)

    calls = []

    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = ""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(args, **kwargs):
        calls.append(args)
        if args[:2] == ["copilot", "--version"]:
            return Result(0, "copilot 1.0")
        if args and args[0] == "copilot":
            return Result(0, "IMPROVED")
        raise AssertionError(f"Unexpected call: {args}")

    monkeypatch.setattr(base_agent_module.subprocess, "run", fake_run)

    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "IMPROVED"
    assert calls


def test_create_main_function_writes_and_reports_diff(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys, base_agent_module, caplog):
    target = tmp_path / "a.md"
    target.write_text("before\n", encoding="utf-8")

    class DemoAgent(base_agent_module.BaseAgent):
        def improve_content(self, prompt: str) -> str:
            self.current_content = "after\n"
            return self.current_content

    monkeypatch.setattr(base_agent_module, "fix_markdown_content", lambda s: s)

    main = base_agent_module.create_main_function(DemoAgent, "desc", "help")
    monkeypatch.setattr(sys, "argv", ["prog", "--context", str(target), "--prompt", "p"])

    with caplog.at_level(logging.INFO):
        main()

    assert target.read_text(encoding="utf-8") == "after\n"
    captured = caplog.text
    assert "updated" in captured.lower() or "changes" in captured.lower() or "--- previous" in captured


def test_describe_backends_does_not_leak_token(monkeypatch: pytest.MonkeyPatch, base_agent_module):
    monkeypatch.setenv("GITHUB_TOKEN", "SUPER_SECRET_VALUE")

    # Avoid calling real executables in unit tests.
    def fake_run(args, **kwargs):
        raise FileNotFoundError("missing")

    monkeypatch.setattr(base_agent_module.subprocess, "run", fake_run)

    text = base_agent_module.BaseAgent.describe_backends()
    assert "SUPER_SECRET_VALUE" not in text
    assert "token set" in text
