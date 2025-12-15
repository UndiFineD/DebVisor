from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


def _to_module_name(path: Path) -> str:
    # importlib needs a valid module name; file stems in scripts/agent can contain '-'.
    safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
    if not safe or safe[0].isdigit():
        safe = f"m_{safe}"
    return f"_dv_smoke_{safe}"


def _iter_agent_modules() -> list[Path]:
    paths = sorted(p for p in AGENT_DIR.glob("*.py") if p.is_file())
    # Exclude legacy tests living next to the agent scripts.
    return [p for p in paths if not p.name.startswith("test_")]


@pytest.mark.parametrize("module_path", _iter_agent_modules(), ids=lambda p: p.name)
def test_agent_modules_compile_and_import(module_path: Path):
    source = module_path.read_text(encoding="utf-8")
    compile(source, str(module_path), "exec")

    with agent_sys_path():
        load_module_from_path(_to_module_name(module_path), module_path)
