from __future__ import annotations
import sys
from pathlib import Path
import pytest
from tests.agent_test_utils import AGENT_DIR, REPO_ROOT, agent_sys_path, load_module_from_path


@pytest.fixture()
def agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent_orchestrator", AGENT_DIR / "agent.py")


def test_load_codeignore_reads_patterns(tmp_path: Path, agent_module):
    (tmp_path / ".codeignore").write_text("# comment\n*.tmp\nvenv\n\n", encoding="utf-8")
    patterns = agent_module.load_codeignore(tmp_path)
    assert "*.tmp" in patterns
    assert "venv" in patterns
    assert "# comment" not in patterns


def test_find_repo_root_prefers_readme(tmp_path: Path, agent_module):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(tmp_path))
    assert a.repo_root == tmp_path


def test_is_ignored_matches_patterns(tmp_path: Path, agent_module):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    a = agent_module.Agent(repo_root=str(tmp_path))
    a.ignored_patterns = {"*.tmp", "ignoreme"}

    assert a._is_ignored(tmp_path / "file.tmp")
    assert a._is_ignored(tmp_path / "ignoreme")
    assert not a._is_ignored(tmp_path / "keep.py")


def test_find_code_files_filters_extensions_and_ignores(tmp_path: Path, agent_module):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    (tmp_path / ".codeignore").write_text("ignored.py\n", encoding="utf-8")

    (tmp_path / "keep.py").write_text("print('x')", encoding="utf-8")
    (tmp_path / "ignored.py").write_text("print('x')", encoding="utf-8")
    (tmp_path / "keep.txt").write_text("x", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(tmp_path), max_files=10)
    files = a.find_code_files()

    names = {p.name for p in files}
    assert "keep.py" in names
    assert "ignored.py" not in names
    assert "keep.txt" not in names


def test_run_tests_invokes_pytest_when_test_file_exists(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, agent_module, capsys):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")

    code_file = tmp_path / "thing.py"
    test_file = tmp_path / "test_thing.py"
    code_file.write_text("x=1", encoding="utf-8")
    test_file.write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(tmp_path))

    calls = []

    class Result:
        def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(cmd, cwd=None, capture_output=False, text=False, check=False):
        calls.append(cmd)
        return Result(returncode=0)

    monkeypatch.setattr(agent_module.subprocess, "run", fake_run)

    a.run_tests(code_file)
    assert any("pytest" in str(part) for part in calls[0])

    out = capsys.readouterr().out
    assert "Tests passed" in out or "Running tests" in out


def test_update_changelog_context_tests_creates_missing_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, agent_module):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")

    code_file = tmp_path / "thing.py"
    code_file.write_text("print('x')", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(tmp_path))

    # Avoid markdown normalization side effects.
    monkeypatch.setattr(agent_module, "fix_markdown_content", lambda s: s)

    class Result:
        def __init__(self, stdout: str = "No changes made", stderr: str = "", returncode: int = 0):
            self.stdout = stdout
            self.stderr = stderr
            self.returncode = returncode

    monkeypatch.setattr(agent_module.subprocess, "run", lambda *args, **kwargs: Result())

    changed = a.update_changelog_context_tests(code_file)
    assert changed is True

    assert (tmp_path / "thing.changes.md").exists()
    assert (tmp_path / "thing.description.md").exists()
    assert (tmp_path / "test_thing.py").exists()


def test_process_file_handles_git_not_available(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, agent_module, capsys):
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    code_file = tmp_path / "thing.py"
    code_file.write_text("print('x')", encoding="utf-8")

    a = agent_module.Agent(repo_root=str(tmp_path))

    # Make the inner steps no-ops so we reach the git commit/push section quickly.
    monkeypatch.setattr(a, "run_stats_update", lambda files: None)
    monkeypatch.setattr(a, "run_tests", lambda cf: None)
    monkeypatch.setattr(a, "update_errors_improvements", lambda cf: False)
    monkeypatch.setattr(a, "update_code", lambda cf: False)
    monkeypatch.setattr(a, "update_changelog_context_tests", lambda cf: False)

    def fake_run(cmd, **kwargs):
        # Simulate git not present
        if isinstance(cmd, list) and cmd and cmd[0] == "git":
            raise FileNotFoundError("git")

        class Result:
            stdout = ""
            stderr = ""
            returncode = 0
        return Result()

    monkeypatch.setattr(agent_module.subprocess, "run", fake_run)

    a.process_file(code_file)
    out = capsys.readouterr().out
    assert "Git not available" in out
