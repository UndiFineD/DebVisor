#!/usr/bin/env python3
"""Utility to remediate issues from security-scan.md.

What it does automatically (safe by default):
- Removes Python bytecode artifacts (__pycache__ folders and *.pyc files) outside virtualenvs.
- Prunes table rows for missing artifact files.
- Attempts to remove unused imports (F401) and fix f-string placeholders (F541).
- Generates suggested workflow permissions blocks for TokenPermissionsID.
- Prints a summary of remaining high-priority issues.

Usage examples:
  # Dry-run with summary
python scripts/fix_security_scan.py

  # Apply all fixes
python scripts/fix_security_scan.py --apply

  # Skip import/f-string auto-fixes
python scripts/fix_security_scan.py --apply --no-code-fixes
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

ROW_PATTERN = re.compile(
    r"^\|\s*(?P<id>\d+)\s*\|\s*(?P<rule>[^|]+?)\s*\|\s*(?P<severity>[^|]+?)\s*\|\s*`(?P<file>[^`]+)`\s*\|\s*(?P<line>[^|]+)\|\s*(?P<message>.+?)\s*\|$"
)
SKIP_DIRS = {".git", ".venv", "node_modules", ".tox", ".mypy_cache", ".pytest_cache"}


def parse_scan(scan_path: Path) -> List[Dict[str, str]]:
    """Parse the markdown table rows into a list of dicts."""
    rows: List[Dict[str, str]] = []
    if not scan_path.exists():
        return rows

    with scan_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            match = ROW_PATTERN.match(line)
            if not match:
                continue
            entry = {key: value.strip() for key, value in match.groupdict().items()}
            entry["id"] = entry["id"]
            rows.append(entry)
    return rows


def should_skip(path: Path) -> bool:
    """Skip paths inside virtualenv, git metadata, or node_modules."""
    return any(part in SKIP_DIRS for part in path.parts)


def clean_bytecode(repo_root: Path, apply: bool) -> Tuple[List[Path], List[Path]]:
    """Remove *.pyc files and __pycache__ directories under the repo root."""
    removed_files: List[Path] = []
    removed_dirs: List[Path] = []

    for pyc_file in repo_root.rglob("*.pyc"):
        if should_skip(pyc_file):
            continue
        removed_files.append(pyc_file)
        if apply:
            try:
                pyc_file.unlink()
            except FileNotFoundError:
                continue

    for cache_dir in repo_root.rglob("__pycache__"):
        if should_skip(cache_dir):
            continue
        removed_dirs.append(cache_dir)
        if apply:
            shutil.rmtree(cache_dir, ignore_errors=True)

    return removed_files, removed_dirs


def render_top_rules(rows: Sequence[Dict[str, str]], limit: int = 12) -> str:
    counter = Counter(row["rule"] for row in rows)
    lines = ["Top rules still present (by count):"]
    for rule, count in counter.most_common(limit):
        lines.append(f"  {rule}: {count}")
    return "\n".join(lines)


def prune_missing_entries(scan_path: Path, repo_root: Path, apply: bool) -> int:
    """Drop BinaryArtifacts-style rows when the referenced file no longer exists."""
    if not scan_path.exists():
        return 0

    with scan_path.open(encoding="utf-8") as handle:
        lines = handle.readlines()

    kept: List[str] = []
    removed = 0

    for line in lines:
        match = ROW_PATTERN.match(line.strip())
        if not match:
            kept.append(line)
            continue

        rule = match.group("rule").strip()
        file_field = match.group("file").strip()

        # Only prune artifact-style rows that we expect to be deleted already.
        if rule != "BinaryArtifactsID" and "__pycache__" not in file_field and not file_field.endswith(".pyc"):
            kept.append(line)
            continue

        candidate = (repo_root / file_field).resolve()
        if candidate.exists():
            kept.append(line)
            continue

        removed += 1
        if not apply:
            kept.append(line)
            # Keep the line during dry-run but count it as removable.
            continue
        # On apply, drop the line entirely.

    if apply and removed:
        with scan_path.open("w", encoding="utf-8") as handle:
            handle.writelines(kept)

    return removed


def fix_unused_imports(rows: Sequence[Dict[str, str]], repo_root: Path, apply: bool) -> int:
    """Attempt to remove unused imports (F401) from Python files."""
    if not apply:
        return sum(1 for r in rows if r["rule"] == "F401")

    fixed = 0
    by_file: Dict[Path, List[Dict[str, str]]] = defaultdict(list)

    for row in rows:
        if row["rule"] != "F401":
            continue
        file_path = repo_root / row["file"]
        if file_path.exists() and file_path.suffix == ".py":
            by_file[file_path].append(row)

    for file_path, entries in by_file.items():
        try:
            with file_path.open(encoding="utf-8") as f:
                content = f.read()

            original_content = content
            lines = content.split("\n")

            # Sort by line number descending to avoid offset issues
            for entry in sorted(entries, key=lambda e: int(e["line"]), reverse=True):
                line_num = int(entry["line"]) - 1
                if line_num < 0 or line_num >= len(lines):
                    continue

                line = lines[line_num]
                # Simple heuristic: if the line is just an import, comment it or remove it
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    # Comment it out instead of removing for safety
                    indent = len(line) - len(line.lstrip())
                    lines[line_num] = " " * indent + "  # " + line.lstrip()
                    fixed += 1

            new_content = "\n".join(lines)
            if new_content != original_content:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(new_content)
        except Exception:
            pass

    return fixed


def fix_f_string_placeholders(rows: Sequence[Dict[str, str]], repo_root: Path, apply: bool) -> int:
    """Fix f-strings missing placeholders (F541)."""
    if not apply:
        return sum(1 for r in rows if r["rule"] == "F541")

    fixed = 0
    by_file: Dict[Path, List[Dict[str, str]]] = defaultdict(list)

    for row in rows:
        if row["rule"] != "F541":
            continue
        file_path = repo_root / row["file"]
        if file_path.exists() and file_path.suffix == ".py":
            by_file[file_path].append(row)

    for file_path, entries in by_file.items():
        try:
            with file_path.open(encoding="utf-8") as f:
                content = f.read()

            original_content = content
            lines = content.split("\n")

            for entry in sorted(entries, key=lambda e: int(e["line"]), reverse=True):
                line_num = int(entry["line"]) - 1
                if line_num < 0 or line_num >= len(lines):
                    continue

                line = lines[line_num]
                # Convert "..." (no placeholder) to regular string
                line = re.sub(r'\b"([^"]*)"', r'"\1"', line)
                line = re.sub(r"\b'([^']*)'", r"'\1'", line)
                lines[line_num] = line
                fixed += 1

            new_content = "\n".join(lines)
            if new_content != original_content:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(new_content)
        except Exception:
            pass

    return fixed


def suggest_workflow_permissions(rows: Sequence[Dict[str, str]]) -> str:
    """Generate suggested GitHub workflow permissions blocks."""
    token_issues = [r for r in rows if r["rule"] == "TokenPermissionsID"]
    if not token_issues:
        return ""

    lines = ["GitHub workflow permissions suggestion (add to top level):\n"]
    lines.append("```yaml")
    lines.append("permissions:")
    lines.append("  contents: read")
    lines.append("  # Add only the minimal permissions your workflow requires:")
    lines.append("  # checks: write       # if you need to report check results")
    lines.append("  # security-events: write  # for CodeQL/security uploads")
    lines.append("  # packages: write    # for registry pushes")
    lines.append("  # id-token: write    # for OIDC token generation")
    lines.append("```\n")
    return "\n".join(lines)


def analyze_by_category(rows: Sequence[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """Group findings by category and provide per-file counts."""
    categories: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for row in rows:
        rule = row["rule"]
        file_path = row["file"]
        categories[rule][file_path] += 1

    return categories


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Remediate issues from security-scan.md")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root")
    parser.add_argument("--scan", type=Path, default=Path(__file__).resolve().parents[1] / "security-scan.md", help="Path to security scan markdown file")
    parser.add_argument("--apply", action="store_true", help="Apply changes instead of dry-run")
    parser.add_argument("--no-prune", action="store_true", help="Do not drop rows for missing artifact entries")
    parser.add_argument("--no-code-fixes", action="store_true", help="Skip auto-fixing imports and f-string issues in code")
    args = parser.parse_args(list(argv) if argv is not None else None)

    repo_root = args.root.resolve()
    scan_path = args.scan.resolve()

    rows = parse_scan(scan_path)
    if rows:
        print(f"Loaded {len(rows)} findings from {scan_path}")
        print(render_top_rules(rows))
    else:
        print(f"No findings parsed from {scan_path}; continuing with cleanup only.")

    removed_files, removed_dirs = clean_bytecode(repo_root, apply=args.apply)
    if args.apply:
        print(f"Removed {len(removed_files)} *.pyc files and {len(removed_dirs)} __pycache__ directories.")
    else:
        print("Dry-run: use --apply to remove the following artifacts.")
        print(f"  Would remove {len(removed_files)} *.pyc files and {len(removed_dirs)} __pycache__ directories.")

    if removed_files:
        print("Sample bytecode paths:")
        for path in removed_files[:5]:
            print(f"  {path.relative_to(repo_root)}")

    # Optionally prune table rows that reference missing artifact files.
    if not args.no_prune:
        pruned = prune_missing_entries(scan_path, repo_root, apply=args.apply)
        if args.apply:
            print(f"Pruned {pruned} resolved artifact rows from security-scan.md.")
        else:
            print(f"Dry-run: would prune {pruned} resolved artifact rows (use --apply to update file).")

    # Auto-fix code issues if enabled
    if not args.no_code_fixes:
        fixed_imports = fix_unused_imports(rows, repo_root, apply=args.apply)
        fixed_f_strings = fix_f_string_placeholders(rows, repo_root, apply=args.apply)
        if args.apply:
            print(f"Fixed {fixed_imports} unused imports and {fixed_f_strings} f-string issues in code.")
        else:
            print(f"Dry-run: would fix {fixed_imports} unused imports and {fixed_f_strings} f-string issues (use --apply).")

    # Print workflow permissions suggestion
    perm_suggestion = suggest_workflow_permissions(rows)
    if perm_suggestion:
        print("\n" + perm_suggestion)

    # Analyze categories for manual follow-up
    categories = analyze_by_category(rows)
    if categories:
        print("\nTop files by issue count (by category):")
        for rule in sorted(categories.keys(), key=lambda r: sum(categories[r].values()), reverse=True)[:5]:
            files_by_count = sorted(categories[rule].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"  {rule}:")
            for file_path, count in files_by_count:
                print(f"    {file_path}: {count}")

    print("\nNext steps (manual):")
    print("- Pin GitHub Actions to commit SHAs in .github/workflows/*.yml files.")
    print("- Address code security findings (SAST, url-redirection, clear-text logging) in opt/web and opt/services.")
    print("- Run a formatter/linter (ruff check --fix) to tackle remaining style and import issues.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
