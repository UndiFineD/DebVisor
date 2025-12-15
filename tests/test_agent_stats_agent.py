from __future__ import annotations
from pathlib import Path
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


def test_stats_agent_counts_expected_files(tmp_path: Path):
    with agent_sys_path():
        mod = load_module_from_path("_dv_agent_stats", AGENT_DIR / "agent-stats.py")

    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_text("print('a')", encoding="utf-8")
    b.write_text("print('b')", encoding="utf-8")

    # For a.py: create all companion files
    (tmp_path / "a.description.md").write_text("x", encoding="utf-8")
    (tmp_path / "a.changes.md").write_text("x", encoding="utf-8")
    (tmp_path / "a.errors.md").write_text("x", encoding="utf-8")
    (tmp_path / "a.improvements.md").write_text("x", encoding="utf-8")
    (tmp_path / "test_a.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    agent = mod.StatsAgent([str(a), str(b)])
    stats = agent.calculate_stats()

    assert stats["total_files"] == 2
    assert stats["files_with_context"] == 1
    assert stats["files_with_changes"] == 1
    assert stats["files_with_errors"] == 1
    assert stats["files_with_improvements"] == 1
    assert stats["files_with_tests"] == 1
