# !/usr/bin/env python3
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


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

"""Check that source files carry the DebVisor Apache 2.0 header."""
from __future__ import annotations
from collections.abc import Iterable

import argparse
import os
import sys
from pathlib import Path

HASH_PREFIX_EXTS = {
    ".py",
    ".sh",
    ".bash",
    ".ps1",
    ".psm1",
    ".psd1",
    ".rb",
    ".pl",
    ".yml",
    ".yaml",
}
SLASH_PREFIX_EXTS = {
    ".go",
    ".rs",
    ".kt",
    ".kts",
    ".php",
}
BLOCK_COMMENT_EXTS = {
    ".c",
    ".h",
    ".cpp",
    ".cc",
    ".cxx",
    ".cs",
    ".js",
    ".ts",
    ".tsx",
    ".java",
    ".scala",
    ".swift",
    ".css",
}
SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "dist",
    "build",
    "venv",
    ".venv",
    "__pycache__",
    "target",
    ".idea",
    ".vscode",
    "coverage",
    ".mypy_cache",
    ".pytest_cache",
    "tests",
}

LINE_TEMPLATE = [
    "{prefix} Copyright (c) 2025 DebVisor contributors",
    "{prefix} Licensed under the Apache License, Version 2.0 (the \"License\");",
    "{prefix} you may not use this file except in compliance with the License.",
    "{prefix} You may obtain a copy of the License at",
    "{prefix}     http://www.apache.org/licenses/LICENSE-2.0",
    "{prefix} Unless required by applicable law or agreed to in writing, software",
    "{prefix} distributed under the License is distributed on an \"AS IS\" BASIS,",
    "{prefix} WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
    "{prefix} See the License for the specific language governing permissions and",
    "{prefix} limitations under the License.",
]
BLOCK_TEMPLATE = [
    "/*",
    " * Copyright (c) 2025 DebVisor contributors",
    " * Licensed under the Apache License, Version 2.0 (the \"License\");",
    " * you may not use this file except in compliance with the License.",
    " * You may obtain a copy of the License at",
    " *     http://www.apache.org/licenses/LICENSE-2.0",
    " * Unless required by applicable law or agreed to in writing, software",
    " * distributed under the License is distributed on an \"AS IS\" BASIS,",
    " * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
    " * See the License for the specific language governing permissions and",
    " * limitations under the License.",
    " */",
]


def header_for_extension(ext: str) -> list[str] | None:
    if ext in HASH_PREFIX_EXTS:
        return [line.format(prefix="#") for line in LINE_TEMPLATE]
    if ext in SLASH_PREFIX_EXTS:
        return [line.format(prefix="//") for line in LINE_TEMPLATE]
    if ext in BLOCK_COMMENT_EXTS:
        return BLOCK_TEMPLATE
    return None


def should_skip_dir(dirname: str) -> bool:
    return dirname in SKIP_DIRS


def has_header(path: Path, header: list[str]) -> bool:
    try:
        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return False

    start = 1 if lines and lines[0].startswith("#!") else 0
    if len(lines) < start + len(header):
        return False
    return lines[start : start + len(header)] == header


def iter_files(root: Path, extensions: Iterable[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix in extensions:
                yield path


def apply_header(path: Path, header: list[str]) -> bool:
    try:
        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return False

    start = 1 if lines and lines[0].startswith("#!") else 0
    body = lines[start:]
    new_lines = lines[:start] + header + [""] + body

    try:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(new_lines) + "\n")
        return True
    except OSError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Apache 2.0 headers")
    parser.add_argument("--root", type=Path, default=Path("."), help="Root to scan")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=None,
        help="File extensions to check (e.g. .py .sh). Defaults to all supported.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Automatically insert missing headers where possible",
    )
    args = parser.parse_args()

    extensions = (
        set(args.extensions)
        if args.extensions
        else HASH_PREFIX_EXTS | SLASH_PREFIX_EXTS | BLOCK_COMMENT_EXTS
    )
    missing: list[Path] = []

    for file_path in iter_files(args.root, extensions):
        header = header_for_extension(file_path.suffix)
        if header is None:
            continue
        if not has_header(file_path, header):
            missing.append(file_path)

    if args.apply:
        applied: list[Path] = []
        for path in missing:
            header = header_for_extension(path.suffix)
            if header and apply_header(path, header):
                applied.append(path)
        # Re-evaluate after applying
        missing = [p for p in missing if not has_header(p, header_for_extension(p.suffix) or [])]
        if applied:
            print("Inserted headers into:")
            for path in sorted(applied):
                print(f" - {path}")
        if missing:
            print("Still missing header in:")
            for path in sorted(missing):
                print(f" - {path}")
            return 1
        print("All checked files contain the required license header.")
        return 0
    else:
        if missing:
            rel_paths = [str(path.relative_to(args.root)) for path in sorted(missing)]
            print("Missing license header in:")
            for rel_path in rel_paths:
                print(f" - {rel_path}")
            return 1

        print("All checked files contain the required license header.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
