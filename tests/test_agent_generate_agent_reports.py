from __future__ import annotations
from pathlib import Path
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


def test_pytest_import_problem_detection():
    with agent_sys_path():
        mod = load_module_from_path("_dv_generate_agent_reports", AGENT_DIR / "generate_agent_reports.py")

    assert mod._looks_like_pytest_import_problem(Path("test_agent-changes.py"))
    assert mod._looks_like_pytest_import_problem(Path("test_agent.changes.py"))
    assert mod._looks_like_pytest_import_problem(Path("test_agent-changes.tests.py"))
    assert mod._looks_like_pytest_import_problem(Path("test_ok.py")) is None


def test_render_description_contains_expected_sections(tmp_path: Path):
    with agent_sys_path():
        mod = load_module_from_path("_dv_generate_agent_reports2", AGENT_DIR / "generate_agent_reports.py")

    src = """\
\"\"\"Doc.\"\"\"\n\nimport sys\n\ndef f():\n    return 1\n\nclass C:\n    pass\n\nif __name__ == '__main__':\n    print('x')\n"""

    tree, err = mod._try_parse_python(src, "x.py")
    assert err is None
    text = mod.render_description(tmp_path / "x.py", src, tree)

    assert "# Description" in text
    assert "## Location" in text
    assert "## Public surface" in text
    assert "## File fingerprint" in text


def test_render_errors_detects_git_and_copilot_hazards(tmp_path: Path):
    with agent_sys_path():
        mod = load_module_from_path("_dv_generate_agent_reports3", AGENT_DIR / "generate_agent_reports.py")

    src = "import subprocess\nsubprocess.run(['git','status'])\nsubprocess.run(['copilot','--prompt','x'])\n"
    compile_result = mod.CompileResult(ok=True)
    out = mod.render_errors(tmp_path / "agent.py", src, compile_result)

    assert "Runs `git`" in out
    assert "Invokes `copilot`" in out
