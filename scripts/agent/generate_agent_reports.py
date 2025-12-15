#!/usr/bin/env python3
"""Generate per-file agent reports.

For every Python file under `scripts/agent/*.py`, this script writes:
- `<stem>.description.md`
- `<stem>.errors.md`
- `<stem>.improvements.md`

The output is intentionally lightweight and based on static inspection and
basic syntax/compile checks.
"""

from __future__ import annotations

import ast
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


AGENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = AGENT_DIR.parents[1]


@dataclass(frozen=True)
class CompileResult:
    ok: bool
    error: Optional[str] = None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _try_parse_python(source: str, filename: str) -> Tuple[Optional[ast.AST], Optional[str]]:
    try:
        return ast.parse(source, filename=filename), None
    except SyntaxError as exc:
        location = f"{exc.filename}:{exc.lineno}:{exc.offset}" if exc.lineno else exc.filename
        return None, f"SyntaxError at {location}: {exc.msg}"


def _compile_check(path: Path) -> CompileResult:
    source = _read_text(path)
    tree, err = _try_parse_python(source, str(path))
    if tree is None:
        return CompileResult(ok=False, error=err)
    # If AST parse succeeded, consider syntax check OK.
    return CompileResult(ok=True)


def _is_pytest_test_file(path: Path) -> bool:
    return path.name.startswith("test_") and path.suffix == ".py"


def _looks_like_pytest_import_problem(path: Path) -> Optional[str]:
    # pytest imports test modules; hyphens/dots in the filename make import fail.
    name = path.name
    if not _is_pytest_test_file(path):
        return None
    if "-" in name or name.count(".") > 1:
        return (
            "Filename is not import-friendly for pytest collection (contains '-' or extra '.') "
            "and may fail test discovery/import."
        )
    return None


def _find_top_level_defs(tree: ast.AST) -> Tuple[List[str], List[str]]:
    functions: List[str] = []
    classes: List[str] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            functions.append(f"async {node.name}")
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return functions, classes


def _find_imports(tree: ast.AST) -> List[str]:
    imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.append(mod)
    # De-dupe while preserving order
    seen = set()
    out: List[str] = []
    for item in imports:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _detect_cli_entry(source: str) -> bool:
    return "if __name__ == '__main__'" in source or 'if __name__ == "__main__"' in source


def _detect_argparse(source: str) -> bool:
    return "argparse" in source


def _placeholder_test_note(path: Path, source: str) -> Optional[str]:
    if not _is_pytest_test_file(path):
        return None
    if re.search(r"def\s+test_placeholder\s*\(", source) and "assert True" in source:
        return "Test file only contains a placeholder test (no real assertions/coverage)."
    return None


def _write_md(path: Path, content: str) -> None:
    # Normalize newlines for Windows repos.
    path.write_text(content.replace("\r\n", "\n").rstrip() + "\n", encoding="utf-8")


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def render_description(py_path: Path, source: str, tree: ast.AST) -> str:
    doc = ast.get_docstring(tree) or ""
    functions, classes = _find_top_level_defs(tree)
    imports = _find_imports(tree)

    lines: List[str] = []
    lines.append(f"# Description: `{py_path.name}`")
    lines.append("")
    if doc.strip():
        lines.append("## Module purpose")
        lines.append(doc.strip())
        lines.append("")
    else:
        lines.append("## Module purpose")
        lines.append("(No module docstring found.)")
        lines.append("")

    lines.append("## Location")
    lines.append(f"- Path: `{_rel(py_path)}`")
    lines.append("")

    lines.append("## Public surface")
    lines.append(f"- Classes: {', '.join(classes) if classes else '(none)'}")
    lines.append(f"- Functions: {', '.join(functions) if functions else '(none)'}")
    lines.append("")

    lines.append("## Behavior summary")
    behavior_bits: List[str] = []
    if _detect_cli_entry(source):
        behavior_bits.append("Has a CLI entrypoint (`__main__`).")
    if _detect_argparse(source):
        behavior_bits.append("Uses `argparse` for CLI parsing.")
    if "subprocess" in source:
        behavior_bits.append("Invokes external commands via `subprocess`.")
    if "sys.path.insert" in source:
        behavior_bits.append("Mutates `sys.path` to import sibling modules.")
    if not behavior_bits:
        behavior_bits.append("Pure module (no obvious CLI/side effects).")
    for bit in behavior_bits:
        lines.append(f"- {bit}")
    lines.append("")

    lines.append("## Key dependencies")
    if imports:
        # Keep it short; imports can be long.
        shown = imports[:12]
        lines.append("- Top imports: " + ", ".join(f"`{x}`" for x in shown) + (" …" if len(imports) > len(shown) else ""))
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append("## File fingerprint")
    lines.append(f"- SHA256(source): `{_sha256_text(source)[:16]}…`")

    return "\n".join(lines)


def render_errors(py_path: Path, source: str, compile_result: CompileResult) -> str:
    lines: List[str] = []
    lines.append(f"# Errors: `{py_path.name}`")
    lines.append("")
    lines.append("## Scan scope")
    lines.append("- Static scan (AST parse) + lightweight compile/syntax check")
    lines.append("- VS Code/Pylance Problems are not embedded by this script")
    lines.append("")

    lines.append("## Syntax / compile")
    if compile_result.ok:
        lines.append("- `py_compile` equivalent: OK (AST parse succeeded)")
    else:
        lines.append("- `py_compile` equivalent: FAILED")
        lines.append(f"- Error: {compile_result.error}")
    lines.append("")

    known: List[str] = []
    pytest_name_issue = _looks_like_pytest_import_problem(py_path)
    if pytest_name_issue:
        known.append(pytest_name_issue)

    placeholder_note = _placeholder_test_note(py_path, source)
    if placeholder_note:
        known.append(placeholder_note)

    # High-level runtime hazards (facts based on static scan)
    if "subprocess.run([\"git\"" in source or "subprocess.run(['git'" in source:
        known.append("Runs `git` via `subprocess`; will fail if git is not installed or repo has no remote.")
    if "copilot" in source and "subprocess.run" in source:
        known.append("Invokes `copilot` CLI; will be a no-op/fallback if Copilot CLI is not installed.")

    lines.append("## Known issues / hazards")
    if known:
        for item in known:
            lines.append(f"- {item}")
    else:
        lines.append("- None detected by the lightweight scan")

    return "\n".join(lines)


def render_improvements(py_path: Path, source: str, tree: ast.AST) -> str:
    functions, classes = _find_top_level_defs(tree)

    suggestions: List[str] = []

    if "sys.path.insert" in source:
        suggestions.append("Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.")
    if "subprocess.run" in source:
        suggestions.append("Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting).")
    if _detect_cli_entry(source) and _detect_argparse(source):
        suggestions.append("Add `--help` examples and validate CLI args (paths, required files).")
    if _is_pytest_test_file(py_path) and re.search(r"def\s+test_placeholder\s*\(", source):
        suggestions.append("Replace placeholder tests with real assertions; target the most important behaviors first.")
    if _looks_like_pytest_import_problem(py_path):
        suggestions.append("Rename the file to be pytest-importable (avoid '-' and extra '.'), then update references.")

    # Generic quality improvements
    if not ast.get_docstring(tree):
        suggestions.append("Add a concise module docstring describing purpose/usage.")
    if classes and "__init__" not in source:
        suggestions.append("Consider documenting class construction/expected invariants.")
    if "print(" in source and "logging" not in source:
        suggestions.append("Consider using `logging` instead of `print` for controllable verbosity.")

    # Keep it short and deterministic.
    suggestions = suggestions[:10]

    lines: List[str] = []
    lines.append(f"# Improvements: `{py_path.name}`")
    lines.append("")
    lines.append("## Suggested improvements")
    if suggestions:
        for s in suggestions:
            lines.append(f"- {s}")
    else:
        lines.append("- No obvious improvements detected by the lightweight scan")

    lines.append("")
    lines.append("## Notes")
    lines.append("- These are suggestions based on static inspection; validate behavior with tests/runs.")
    lines.append(f"- File: `{_rel(py_path)}`")

    return "\n".join(lines)


def iter_agent_py_files() -> Iterable[Path]:
    return sorted(AGENT_DIR.glob("*.py"))


def main(argv: Sequence[str]) -> int:
    py_files = list(iter_agent_py_files())
    if not py_files:
        print(f"No .py files found under {AGENT_DIR}")
        return 1

    for py_path in py_files:
        source = _read_text(py_path)
        tree, parse_err = _try_parse_python(source, str(py_path))
        compile_result = _compile_check(py_path)

        # If parse failed, still emit minimal files.
        if tree is None:
            description = (
                f"# Description: `{py_path.name}`\n\n"
                f"## Module purpose\n\n"
                f"(Unable to parse file: {parse_err})\n"
            )
            errors = render_errors(py_path, source, compile_result)
            improvements = (
                f"# Improvements: `{py_path.name}`\n\n"
                "## Suggested improvements\n"
                "- Fix the syntax errors first; then re-run report generation\n"
            )
        else:
            description = render_description(py_path, source, tree)
            errors = render_errors(py_path, source, compile_result)
            improvements = render_improvements(py_path, source, tree)

        stem = py_path.stem
        _write_md(AGENT_DIR / f"{stem}.description.md", description)
        _write_md(AGENT_DIR / f"{stem}.errors.md", errors)
        _write_md(AGENT_DIR / f"{stem}.improvements.md", improvements)

    print(f"Wrote reports for {len(py_files)} files under {_rel(AGENT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
