from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


def _safe_module_name(path: Path) -> str:
    safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
    if not safe or safe[0].isdigit():
        safe = f"m_{safe}"
    return f"_dv_legacy_test_{safe}"


def _legacy_test_scripts() -> list[Path]:
    return sorted(p for p in AGENT_DIR.glob("test_*.py") if p.is_file())


@pytest.mark.parametrize("module_path", _legacy_test_scripts(), ids=lambda p: p.name)
def test_legacy_agent_test_scripts_compile(module_path: Path):
    source = module_path.read_text(encoding="utf-8")
    compile(source, str(module_path), "exec")


@pytest.mark.parametrize("module_path", _legacy_test_scripts(), ids=lambda p: p.name)
def test_legacy_agent_test_scripts_import_without_running_subprocess(
    monkeypatch: pytest.MonkeyPatch, module_path: Path
):
    # If any legacy test script tries to run external tools at import time, fail fast.
    import os
    import subprocess

    def _boom(*_args, **_kwargs):
        raise AssertionError("External process invoked during module import")

    monkeypatch.setattr(subprocess, "run", _boom, raising=True)
    monkeypatch.setattr(os, "system", _boom, raising=True)

    with agent_sys_path():
        mod = load_module_from_path(_safe_module_name(module_path), module_path)

    # Ensure the module actually defines tests (not just empty placeholders).
    has_test = any(
        name.startswith("test_") for name in vars(mod).keys()
    ) or any(name.startswith("Test") for name in vars(mod).keys())
    assert has_test
