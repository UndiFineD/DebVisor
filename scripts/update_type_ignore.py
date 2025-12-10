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
Smart MyPy error fixer that updates existing type: ignore comments.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

def fix_type_ignore_comments():
    """Update type: ignore comments to cover all error codes in mypy_errors_new.txt"""

    error_file = "mypy_errors_new.txt"
    if not Path(error_file).exists():
        print(f"Error: {error_file} not found")
        return

    # Parse errors grouped by file and line
    errors_by_file_line: Dict[Tuple[str, int], List[str]] = {}

    with open(error_file, 'r') as f:
        for line in f:
            # Skip note lines
            if " note: " in line:
                continue

            match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: .* \[([^\]]+)\]", line)
            if match:
                filepath, line_num, code = match.groups()
                key = (filepath, int(line_num))
                if key not in errors_by_file_line:
                    errors_by_file_line[key] = []
                errors_by_file_line[key].append(code)

    print(f"Found {len(errors_by_file_line)} error lines to fix")

    total_fixed = 0

    for (filepath, line_num), codes in sorted(errors_by_file_line.items()):
        path = Path(filepath)
        if not path.exists():
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()

            if line_num < 1 or line_num > len(lines):
                continue

            idx = line_num - 1
            line = lines[idx]

            # Check if line has type: ignore comment
            if "# type: ignore" in line:
                # Update existing comment to include all codes
                existing_match = re.search(r"# type: ignore(?:\[([^\]]*)\])?", line)
                if existing_match:
                    existing_codes_str = existing_match.group(1) or ""
                    existing_codes = set(existing_codes_str.split(", ")) if existing_codes_str else set()

                    # Add all new codes
                    for code in codes:
                        existing_codes.add(code)

                    # Remove empty strings
                    existing_codes.discard("")

                    # Rebuild the type: ignore comment
                    new_comment = f"# type: ignore[{', '.join(sorted(existing_codes))}]"
                    new_line = re.sub(r"# type: ignore(?:\[[^\]]*\])?", new_comment, line)

                    if new_line != line:
                        lines[idx] = new_line
                        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                        print(f"Updated {filepath}:{line_num} - codes: {', '.join(sorted(existing_codes))}")
                        total_fixed += 1
            else:
                # Add new type: ignore comment with all codes
                code_str = ", ".join(sorted(codes))
                new_line = line.rstrip() + f"  # type: ignore[{code_str}]"
                lines[idx] = new_line
                path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                print(f"Added type: ignore to {filepath}:{line_num} - codes: {code_str}")
                total_fixed += 1

        except Exception as e:
            print(f"Error processing {filepath}:{line_num}: {e}")

    print(f"\n{'='*60}")
    print(f"Total lines fixed: {total_fixed}")

    # Run mypy again
    import subprocess
    print("\nRunning mypy to verify...")
    result = subprocess.run(
        ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
        capture_output=True, text=True, check=False
    )

    error_count = len([error_line for error_line in result.stdout.splitlines() if " error: " in error_line])
    print(f"Remaining errors: {error_count}")

    if error_count > 0:
        with open("mypy_errors_new.txt", "w") as f:
            f.write(result.stdout)
        print("New errors saved to mypy_errors_new.txt")

if __name__ == "__main__":
    fix_type_ignore_comments()
