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


from __future__ import annotations
import importlib.util
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType


AGENT_DIR = Path(__file__).resolve().parent


@contextmanager
def agent_dir_on_path():
    old_sys_path = list(sys.path)
    sys.path.insert(0, str(AGENT_DIR))
    try:
        yield
    finally:
        sys.path[:] = old_sys_path


def load_agent_module(filename: str, module_name: str | None = None) -> ModuleType:
    """Load an agent module from scripts/agent by filename.

    Supports files that are not valid Python identifiers (e.g. `agent-changes.py`).
    """
    path = AGENT_DIR / filename
    if not path.exists():
        raise FileNotFoundError(path)

    if module_name is None:
        safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
        if not safe or safe[0].isdigit():
            safe = f"m_{safe}"
        module_name = f"_dv_legacy_{safe}"

    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load spec for {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    except Exception:
        sys.modules.pop(module_name, None)
        raise
