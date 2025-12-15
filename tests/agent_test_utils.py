from __future__ import annotations

import importlib.util
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = REPO_ROOT / "scripts" / "agent"


@contextmanager
def agent_sys_path() -> ModuleType:
    """Temporarily add scripts/agent to sys.path for legacy imports."""
    old_sys_path = list(sys.path)
    sys.path.insert(0, str(AGENT_DIR))
    try:
        yield
    finally:
        sys.path[:] = old_sys_path


def load_module_from_path(module_name: str, file_path: Path) -> ModuleType:
    """Load a Python module from an arbitrary path (supports hyphen filenames)."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    # Python 3.11+ (and especially 3.14 w/ string annotations) expects
    # dynamically-loaded modules to be present in sys.modules while executing.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    except Exception:
        sys.modules.pop(module_name, None)
        raise
