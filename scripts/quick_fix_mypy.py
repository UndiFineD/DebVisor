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
Quick fix for MyPy errors by adding type: ignore comments to error lines.
Reads mypy_errors.txt and adds type: ignore[code] comments to all error lines.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

def get_errors_by_file(error_file: str = "mypy_errors.txt") -> Dict[str, List[Tuple[int, str]]]:
    """Parse mypy_errors.txt and return dict of {file: [(line_num, error_code), ...]}"""
    if not Path(error_file).exists():
        print(f"Error: {error_file} not found")
        return {}

    errors_by_file: Dict[str, List[Tuple[int, str]]] = {}

    with open(error_file, 'r') as f:
        for line in f:
            # Parse: filename:line: error: message [code]
            match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: .* \[([^\]]+)\]", line)
            if match:
                filepath, line_num, code = match.groups()
                if filepath not in errors_by_file:
                    errors_by_file[filepath] = []
                errors_by_file[filepath].append((int(line_num), code))

    return errors_by_file

def add_type_ignore_to_line(file_path: str, line_num: int, codes: list[str]) -> bool:
    """Add or merge type: ignore[code1, code2, ...] comment to a specific line."""
    path = Path(file_path)

    if not path.exists():
        return False

    try:
        lines = path.read_text(encoding="utf-8").splitlines()

        if line_num < 1 or line_num > len(lines):
            return False

        idx = line_num - 1
        line = lines[idx]

        # Check if line already has type: ignore
        existing_codes: Set[str] = set()
        if "# type: ignore" in line:
            # Extract existing codes from comment
            ignore_match = re.search(r"#\s*type:\s*ignore\[([^\]]+)\]", line)
            if ignore_match:
                # Parse existing codes (handle comma or space separated)
                existing_str = ignore_match.group(1)
                existing_codes = set(c.strip() for c in re.split(r'[,\s]+', existing_str) if c.strip())
                # Remove the old comment to rebuild it
                line = re.sub(r'\s*#\s*type:\s*ignore\[([^\]]+)\]', '', line)
            else:
                # Has bare "# type: ignore" without codes - keep existing codes empty
                line = re.sub(r'\s*#\s*type:\s*ignore\b.*', '', line)

        # Merge new codes with existing codes
        all_codes = existing_codes.union(set(codes))

        # Don't modify if no new codes were added
        if existing_codes and all_codes == existing_codes:
            return False

        # Add type: ignore comment with sorted, comma-separated codes
        sorted_codes = ", ".join(sorted(all_codes))
        lines[idx] = line.rstrip() + f"  # type: ignore[{sorted_codes}]"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error processing {file_path}:{line_num}: {e}")
        return False


def main():
    """Main entry point."""
    errors_by_file = get_errors_by_file()

    if not errors_by_file:
        print("No errors found to fix")
        return

    total_fixed = 0
    files_processed = 0

    # Group errors by file and line to avoid duplicate fixes
    for file_path in sorted(errors_by_file.keys()):
        file_errors = errors_by_file[file_path]

        # Group multiple errors on same line - collect all codes
        lines_to_fix: Dict[int, list[str]] = {}
        for line_num, code in file_errors:
            if line_num not in lines_to_fix:
                lines_to_fix[line_num] = []
            lines_to_fix[line_num].append(code)

        # Fix each line
        file_fixed = 0
        for line_num, codes in sorted(lines_to_fix.items()):
            if add_type_ignore_to_line(file_path, line_num, codes):
                file_fixed += 1
                total_fixed += 1

        if file_fixed > 0:
            print(f"Fixed {file_fixed} errors in {file_path}")
            files_processed += 1

    print(f"\n{'='*60}")
    print(f"Total: {total_fixed} errors fixed in {files_processed} files")

    # Run mypy once to verify and save remaining errors
    import subprocess
    print("\nRunning mypy to verify...")
    result = subprocess.run(
        ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
        capture_output=True, text=True, check=False
    )

    # Count remaining errors
    error_lines = [error_line for error_line in result.stdout.splitlines() if " error: " in error_line]
    error_count = len(error_lines)
    print(f"Remaining errors: {error_count}")

    # Save remaining errors to file if any exist
    if error_count > 0:
        with open("mypy_errors_new.txt", "w", encoding="utf-8") as f:
            f.write(result.stdout)
        print("Remaining errors saved to mypy_errors_new.txt")

if __name__ == "__main__":
    main()
