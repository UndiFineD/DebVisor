"""
Utility to apply straightforward mypy fixes based on mypy_errors.txt.

Handles low-risk categories:
- Add "-> None" to functions flagged with missing return type.
- Remove unused "type: ignore" comments.
- Add Any generics for bare Dict/List/Tuple/Set/Callable/LoggerAdapter/Queue.
- Add ``: Any`` for obvious empty literal assignments flagged for annotation.

Run in dry-run by default to review planned edits.
"""
from __future__ import annotations
from typing import Callable
from typing import Tuple
from typing import Set

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ErrorEntry:
    path: Path
    line_no: int
    message: str


GENERIC_PATTERNS: List[tuple[str, str]] = [
    (r"\bDict\b(?!\[)", "Dict[str, Any]"),
    (r"\bdict\b(?!\[)", "dict[str, Any]"),
    (r"\bList\b(?!\[)", "List[Any]"),
    (r"\blist\b(?!\[)", "list[Any]"),
    (r"\bTuple\b(?!\[)", "Tuple[Any, ...]"),
    (r"\btuple\b(?!\[)", "tuple[Any, ...]"),
    (r"\bSet\b(?!\[)", "Set[Any]"),
    (r"\bset\b(?!\[)", "set[Any]"),
    (r"\bCallable\b(?!\[)", "Callable[..., Any]"),
    (r"\bLoggerAdapter\b(?!\[)", "LoggerAdapter[Any]"),
    (r"\bQueue\b(?!\[)", "Queue[Any]"),
]


def parse_errors(error_file: Path) -> List[ErrorEntry]:
    entries: List[ErrorEntry] = []
    pattern = re.compile(r"(.+?):(\d+): error: (.+)")
    for raw in error_file.read_text(encoding="utf-8").splitlines():
        m = pattern.match(raw)
        if not m:
            continue
        path_str, line_no, message = m.groups()
        entries.append(
            ErrorEntry(path=Path(path_str), line_no=int(line_no), message=message)
        )
    return entries


def ensure_any_import(lines: List[str]) -> List[str]:
    if any("from typing import Any" in ln for ln in lines):
        return lines
    for idx, ln in enumerate(lines):
        if ln.startswith("from typing import"):
            parts = ln.strip().split()
            if len(parts) >= 4 and parts[0] == "from" and parts[1] == "typing":
                # Merge into existing import
                if "Any" not in ln:
                    lines[idx] = ln.rstrip() + ", Any"
                return lines
No typing import found; insert near top (after shebang/encoding/docstring handled simply)
    insert_at = 0
    if lines and lines[0].startswith("  #!"):
        insert_at = 1
    lines.insert(insert_at, "from typing import Any")
    return lines


def add_return_none(line: str) -> tuple[str, bool, bool]:
    if "->" in line or ":" not in line:
        return line, False, False
    stripped = line.lstrip()
    if not (stripped.startswith("def ") or stripped.startswith("async def ")):
        return line, False, False
    prefix, colon, suffix = line.partition(":")
    new_line = f"{prefix} -> None:{suffix}"
    return new_line, True, False


def remove_unused_ignore(line: str) -> tuple[str, bool, bool]:
    if "type: ignore" not in line:
        return line, False, False
    return line.split("  # type: ignore", 1)[0].rstrip(), True, False


def add_var_annotation(line: str) -> tuple[str, bool, bool]:
    m = re.match(r"(\s*)([A-Za-z_][\w]*)\s*=\s*(\{\}|\[\]|\(\))\s*$", line)
    if not m:
        return line, False, False
    indent, name, literal = m.groups()
    return f"{indent}{name}: Any = {literal}", True, True


def add_generic_any(line: str) -> tuple[str, bool, bool]:
    changed = False
    needs_any = False
    for pattern, repl in GENERIC_PATTERNS:
        new_line, count = re.subn(pattern, repl, line)
        if count:
            line = new_line
            changed = True
            needs_any = True
    return line, changed, needs_any


def apply_fix(lines: List[str], entry: ErrorEntry) -> tuple[List[str], bool, bool]:
    idx = entry.line_no - 1
    if idx < 0 or idx >= len(lines):
        return lines, False, False

    line = lines[idx]
    changed = False
    needs_any = False

    msg = entry.message
    if "missing a return type annotation" in msg:
        line, changed, _ = add_return_none(line)
    elif "Unused \"type: ignore\" comment" in msg:
        line, changed, _ = remove_unused_ignore(line)
    elif "Need type annotation" in msg:
        line, changed, needs_any = add_var_annotation(line)
    elif "Missing type parameters for generic type" in msg:
        line, changed, needs_any = add_generic_any(line)

    if changed:
        lines[idx] = line
    return lines, changed, needs_any


def process_file(path: Path, entries: List[ErrorEntry], apply: bool) -> dict[str, Any]:
    original = path.read_text(encoding="utf-8").splitlines()
    lines = list(original)
    touched = False
    needs_any_import = False

    for entry in entries:
        lines, changed, needs_any = apply_fix(lines, entry)
        touched = touched or changed
        needs_any_import = needs_any_import or needs_any

    if needs_any_import:
        lines = ensure_any_import(lines)
        touched = True

    if touched and apply:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "file": str(path),
        "changed": touched,
        "applied": apply and touched,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply easy mypy fixes")
    parser.add_argument(
        "--errors-file",
        type=Path,
        default=Path("mypy_errors.txt"),
        help="Path to mypy error output file",
    )
    parser.add_argument("--apply", action="store_true", help="Write changes")
    args = parser.parse_args()

    if not args.errors_file.exists():
        print(f"Errors file not found: {args.errors_file}", file=sys.stderr)
        return 1

    entries = parse_errors(args.errors_file)
    grouped: Dict[Path, List[ErrorEntry]] = {}
    for e in entries:
        grouped.setdefault(e.path, []).append(e)

    summaries = []
    for path, errs in grouped.items():
        if not path.exists():
            continue
        summaries.append(process_file(path, errs, apply=args.apply))

    changed = [s for s in summaries if s["changed"]]
    if not changed:
        print("No changes suggested.")
        return 0

    for s in changed:
        status = "applied" if s["applied"] else "planned"
        print(f"{status}: {s['file']}")

    if not args.apply:
        print("Run again with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
