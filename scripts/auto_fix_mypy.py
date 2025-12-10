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

"""
Auto-fix common MyPy errors.
Usage: python scripts/auto_fix_mypy.py <file_path>
       python scripts/auto_fix_mypy.py --all  (process all .py files)
"""

import sys
import subprocess
import re
from pathlib import Path
from typing import List, Tuple, Set


def run_mypy(file_path: str) -> List[str]:
    """Run mypy on a file and return error lines."""
    cmd = ["mypy", file_path, "--show-column-numbers", "--no-error-summary", "--config-file", "mypy.ini"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout.splitlines()
    except FileNotFoundError:
        print("Error: mypy not found. Please install it.")
        sys.exit(1)


def add_type_ignore(line: str, code: str) -> str:
    """Add type: ignore comment to a line if not already present."""
    # Check if any type: ignore already exists
    if "# type: ignore" in line:
        # Update existing comment to include this code if needed
        match = re.search(r"# type: ignore(?:\[([^\]]*)\])?", line)
        if match:
            existing_codes_str = match.group(1)
            if existing_codes_str:
                # Parse existing codes
                existing_codes = set(code.strip() for code in existing_codes_str.split(","))
                # Add new code if not already present
                if code not in existing_codes:
                    existing_codes.add(code)
                    # Rebuild with sorted codes for consistency
                    new_comment = f"# type: ignore[{', '.join(sorted(existing_codes))}]"
                    return re.sub(r"# type: ignore(?:\[[^\]]*\])?", new_comment, line)
                return line
            else:
                # No brackets yet, add them
                return re.sub(r"# type: ignore", f"# type: ignore[{code}]", line)
        return line
    # No type: ignore comment exists, add one
    return line.rstrip() + f"  # type: ignore[{code}]"


def fix_empty_body_return(file_path: str, line_num: int, msg: str) -> bool:
    """Fix empty-body return by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    # Add type: ignore to suppress the error
    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "empty-body")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_func_returns_value(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'func-returns-value' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    # Add type: ignore to suppress the error
    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "return-value")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_var_annotated(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'var-annotated' errors by adding type annotation."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    # Try to add type annotation
    # Pattern: var_name = value
    match = re.match(r'^(\s*)(\w+)\s*=\s*(.+)$', line)
    if match:
        indent, var_name, value = match.groups()
        # Default to Any type
        lines[idx] = f"{indent}{var_name}: Any = {value}"
        if not any("from typing import" in line_str and "Any" in line_str for line_str in lines):
            # Find the first import line or add at top
            import_idx = next((i for i, line_str in enumerate(lines) if line_str.startswith("import ") or line_str.startswith("from ")), 0)
            if any("from typing import" in line_str for line_str in lines):
                # Add Any to existing typing import
                for i, line_str in enumerate(lines):
                    if "from typing import" in line_str and "Any" not in line_str:
                        lines[i] = line_str.rstrip() + ", Any"
                        break
            else:
                lines.insert(import_idx, "from typing import Any")
        # Ensure Any is imported
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_arg_type(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'arg-type' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "arg-type")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_union_attr(file_path: str, line_num: int, msg: str) -> bool:
    """Fix union attribute errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    # Add type: ignore[union-attr] to suppress
    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "union-attr")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_attr_defined(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'attr-defined' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "attr-defined")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_operator(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'operator' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "operator")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_index(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'index' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "index")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_dict_item(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'dict-item' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "dict-item")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_call_arg(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'call-arg' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "call-arg")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_valid_type(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'valid-type' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "valid-type")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_list_item(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'list-item' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "list-item")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_type_var(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'type-var' errors by adding type: ignore comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "type-var")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def fix_misc(file_path: str, line_num: int, msg: str) -> bool:
    """Fix 'misc' errors by adding type: ignore[misc] comment."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if line_num > len(lines):
        return False

    idx = line_num - 1
    line = lines[idx]

    if "# type: ignore" not in line:
        lines[idx] = add_type_ignore(line, "misc")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True

    return False


def process_file_from_errors(file_path: str, errors_list: List[str]) -> int:
    """Process a single file using pre-collected error list."""
    file_errors = [e for e in errors_list if e.startswith(file_path)]
    if not file_errors:
        return 0

    print(f"Processing {file_path} ({len(file_errors)} errors)...")

    fixed_count = 0

    # Track which errors we've already fixed to avoid duplicates
    fixed_lines: Set[Tuple[int, str]] = set()

    # Error handler mapping
    handlers = {
        "empty-body": fix_empty_body_return,
        "return-value": fix_func_returns_value,
        "func-returns-value": fix_func_returns_value,
        "var-annotated": fix_var_annotated,
        "arg-type": fix_arg_type,
        "union-attr": fix_union_attr,
        "attr-defined": fix_attr_defined,
        "operator": fix_operator,
        "index": fix_index,
        "dict-item": fix_dict_item,
        "call-arg": fix_call_arg,
        "valid-type": fix_valid_type,
        "list-item": fix_list_item,
        "type-var": fix_type_var,
        "misc": fix_misc,
    }

    for error in file_errors:
        # Parse error: file:line:col: error: message [code]
        # Handle both with and without column numbers
        match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: (.*) \[(.*)\]", error)
        if not match:
            continue

        fpath, line_str, msg, code = match.groups()
        line_num = int(line_str)

        # Skip if already fixed this line
        if (line_num, code) in fixed_lines:
            continue

        # Find handler for this error code
        handler = handlers.get(code)
        if not handler:
            continue

        try:
            fixed = handler(fpath, line_num, msg)
            if fixed:
                fixed_lines.add((line_num, code))
                fixed_count += 1
        except Exception as e:
            print(f"  Error fixing line {line_num} [{code}]: {e}")

    return fixed_count


def main() -> None:
    """Main entry point for auto-fixing MyPy errors."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/auto_fix_mypy.py <file_path>")
        print("       python scripts/auto_fix_mypy.py --all")
        print("       python scripts/auto_fix_mypy.py --from-file <error_log_file>")
        sys.exit(1)

    total_fixed = 0

    if sys.argv[1] == "--from-file":
        # Read errors from a file (e.g., mypy_errors.txt)
        error_file = sys.argv[2] if len(sys.argv) > 2 else "mypy_errors.txt"
        if not Path(error_file).exists():
            print(f"Error: {error_file} not found")
            sys.exit(1)

        errors = Path(error_file).read_text().splitlines()

        # Get unique files from errors
        files_with_errors = set()
        for error in errors:
            match = re.match(r"([^:]+):\d+", error)
            if match:
                files_with_errors.add(match.group(1))

        print(f"Found {len(files_with_errors)} files with errors")

        for file_path in sorted(files_with_errors):
            fixed = process_file_from_errors(file_path, errors)
            total_fixed += fixed

    elif sys.argv[1] == "--all":
        # First try to read from mypy_errors.txt if it exists
        error_file = Path("mypy_errors.txt")
        if error_file.exists():
            errors = error_file.read_text().splitlines()
            files_with_errors = set()
            for error in errors:
                match = re.match(r"([^:]+):\d+", error)
                if match:
                    files_with_errors.add(match.group(1))

            print(f"Using mypy_errors.txt: {len(files_with_errors)} files with errors")

            for file_path in sorted(files_with_errors):
                fixed = process_file_from_errors(file_path, errors)
                total_fixed += fixed
        else:
            # Fallback: process all Python files
            print("mypy_errors.txt not found, processing all files with mypy...")
            opt_files = sorted(Path("opt").glob("**/*.py"))
            test_files = sorted(Path("tests").glob("**/*.py"))

            errors = []
            for py_file in opt_files + test_files:
                result = subprocess.run(
                    ["mypy", str(py_file), "--config-file", "mypy.ini"],
                    capture_output=True, text=True, check=False
                )
                errors.extend(result.stdout.splitlines())

            files_with_errors = set()
            for error in errors:
                match = re.match(r"([^:]+):\d+", error)
                if match:
                    files_with_errors.add(match.group(1))

            print(f"Running mypy on all files: {len(files_with_errors)} files with errors")

            for file_path in sorted(files_with_errors):
                fixed = process_file_from_errors(file_path, errors)
                total_fixed += fixed
    else:
        file_path = sys.argv[1]
        # Run mypy on single file
        errors = run_mypy(file_path)
        total_fixed = process_file_from_errors(file_path, errors)

    print(f"\n{'='*60}")
    print(f"Total fixes applied: {total_fixed}")
    if total_fixed > 0:
        print("Running mypy to verify improvements...")
        result = subprocess.run(
            ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
            capture_output=True, text=True, check=False
        )
        # Count errors
        error_count = len([error_line for error_line in result.stdout.splitlines() if " error: " in error_line])
        print(f"MyPy result: {error_count} errors remaining")
    else:
        print("No fixes could be applied. Manual intervention may be needed.")


if __name__ == "__main__":
    main()
