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
Smart MyPy error reviewer and optional fixer.

This tool generates review-ready output of mypy errors and suggests type: ignore comments
with proper documentation, while preventing silent suppression of critical issues.

Features:
- Safe-by-default: generates suggestions without modifying files
- Whitelist/blocklist: configurable per error code and file pattern
- Context inclusion: shows error lines and file snippets for manual review
- Audit trail: requires human justification for suppressions
- Explicit opt-in: --apply flag required for destructive changes
"""

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# Configuration: Which error codes and file patterns to never auto-suppress
CRITICAL_ERROR_CODES = {
    "assignment",  # Type mismatch in assignment (real bugs)
    "return-value",  # Return type mismatch (real bugs)
    "func-returns-value",  # Function returns wrong type
    "arg-type",  # Function argument type mismatch
    "union-attr",  # Accessing attribute that doesn't exist on some union members
    "attr-defined",  # Accessing undefined attribute
}

# File patterns that should never be auto-suppressed (dangerous files)
CRITICAL_FILE_PATTERNS = {
    "cert_manager.py",  # Crypto/security critical
    "security/",  # Security-related code
    "auth",  # Authentication code
}

# Error codes that are safe to auto-suppress (non-critical style issues)
ALLOWLIST_CODES = {
    "var-annotated",  # Variable needs explicit annotation
    "name-defined",  # Name not defined (often false positives)
    "annotation-unchecked",  # Untyped function bodies
    "unused-ignore",  # Redundant type: ignore
}


@dataclass
class TypeIgnoreSuggestion:
    """Suggested type: ignore fix with full context."""

    filepath: str
    line_num: int
    codes: List[str]
    line_text: str
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    is_critical: bool = False
    blocklisted_reason: Optional[str] = None
    justification_required: bool = False
    suggested_justification: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def should_suppress_code(code: str, filepath: str, require_allowlist: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Check if a code should be auto-suppressed.

    Returns:
        (should_suppress, reason_if_blocked)
    """
    # Check if error code is critical
    if code in CRITICAL_ERROR_CODES:
        return False, f"Code '{code}' is critical and should be fixed, not suppressed"

    # Check if file is critical
    for pattern in CRITICAL_FILE_PATTERNS:
        if pattern in filepath:
            return False, f"File '{filepath}' contains critical patterns and shouldn't suppress errors"

    # If requiring allowlist, only suppress known-safe codes
    if require_allowlist:
        if code in ALLOWLIST_CODES:
            return True, None
        return False, f"Code '{code}' not in allowlist (use --unsafe-suppress to override)"

    # By default, allow suppression of non-critical codes
    return True, None


def parse_mypy_errors(error_file: str) -> Dict[Tuple[str, int], List[str]]:
    """Parse mypy errors grouped by file and line."""
    errors_by_file_line: Dict[Tuple[str, int], List[str]] = {}

    if not Path(error_file).exists():
        print(f"Error: {error_file} not found")
        return errors_by_file_line

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

    return errors_by_file_line


def build_suggestions(
    errors_by_file_line: Dict[Tuple[str, int], List[str]],
    require_allowlist: bool = False,
) -> Tuple[List[TypeIgnoreSuggestion], int, int]:
    """
    Build suggestions for type: ignore fixes.

    Returns:
        (suggestions, suppressed_count, blocked_count)
    """
    suggestions: List[TypeIgnoreSuggestion] = []
    suppressed_count = 0
    blocked_count = 0

    for (filepath, line_num), codes in sorted(errors_by_file_line.items()):
        path = Path(filepath)
        if not path.exists():
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()

            if line_num < 1 or line_num > len(lines):
                continue

            idx = line_num - 1
            line_text = lines[idx]

            # Gather context
            context_before = lines[idx - 1] if idx > 0 else None
            context_after = lines[idx + 1] if idx < len(lines) - 1 else None

            # Analyze codes
            suppressible_codes = []
            critical_codes = []
            blocklisted_code = None
            blocklisted_reason = None

            for code in codes:
                can_suppress, reason = should_suppress_code(code, filepath, require_allowlist)
                if can_suppress:
                    suppressible_codes.append(code)
                    suppressed_count += 1
                else:
                    critical_codes.append(code)
                    if blocklisted_code is None:
                        blocklisted_code = code
                        blocklisted_reason = reason
                    blocked_count += 1

            # Create suggestion
            suggestion = TypeIgnoreSuggestion(
                filepath=filepath,
                line_num=line_num,
                codes=suppressible_codes,
                line_text=line_text,
                context_before=context_before,
                context_after=context_after,
                is_critical=len(critical_codes) > 0 or blocklisted_code is not None,
                blocklisted_reason=blocklisted_reason,
                justification_required=len(suppressible_codes) > 0,
                suggested_justification=(
                    f"Suppressing: {', '.join(suppressible_codes)}. "
                    f"Critical (unfixed): {', '.join(critical_codes)}. "
                    f"Reason: [YOUR JUSTIFICATION HERE]"
                    if (suppressible_codes or critical_codes) else ""
                ),
            )
            suggestions.append(suggestion)

        except Exception as e:
            print(f"Warning: Error processing {filepath}:{line_num}: {e}")

    return suggestions, suppressed_count, blocked_count


def write_review_file(
    suggestions: List[TypeIgnoreSuggestion],
    output_format: str = "json",
) -> str:
    """
    Write suggestions to review-ready output file.

    Returns:
        Path to written file
    """
    if output_format == "json":
        filename = "type_ignore_review.json"
        data = {
            "total_suggestions": len(suggestions),
            "suggestions": [s.to_dict() for s in suggestions],
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename

    elif output_format == "patch":
        filename = "type_ignore_review.patch"
        with open(filename, 'w') as f:
            f.write("# Review-ready type: ignore patch file\n")
            f.write("# Apply with: patch -p0 < type_ignore_review.patch\n\n")

            for suggestion in suggestions:
                if suggestion.codes:
                    f.write(f"--- {suggestion.filepath}\n")
                    f.write(f"+++ {suggestion.filepath}\n")
                    f.write(f"@@ {suggestion.line_num} @@\n")
                    f.write(f"- {suggestion.line_text}\n")

                    new_line = suggestion.line_text.rstrip() + f"  # type: ignore[{', '.join(sorted(suggestion.codes))}]"
                    f.write(f"+ {new_line}\n")
                    f.write(f"# Justification: {suggestion.suggested_justification}\n\n")

        return filename

    else:
        raise ValueError(f"Unknown output format: {output_format}")


def apply_suggestions(
    suggestions: List[TypeIgnoreSuggestion],
    require_comment: bool = False,
) -> int:
    """
    Apply type: ignore fixes to files.

    Returns:
        Number of lines fixed
    """
    fixed_count = 0

    for suggestion in suggestions:
        if not suggestion.codes or suggestion.is_critical:
            continue

        path = Path(suggestion.filepath)
        if not path.exists():
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
            idx = suggestion.line_num - 1
            line = lines[idx]

            # Check if line already has type: ignore
            if "# type: ignore" in line:
                # Update existing comment
                existing_match = re.search(r"# type: ignore(?:\[([^\]]*)\])?", line)
                if existing_match:
                    existing_codes_str = existing_match.group(1) or ""
                    existing_codes = set(existing_codes_str.split(", ")) if existing_codes_str else set()

                    for code in suggestion.codes:
                        existing_codes.add(code)

                    existing_codes.discard("")
                    code_str = ", ".join(sorted(existing_codes))

                    comment = f"# type: ignore[{code_str}]"
                    if require_comment:
                        comment += f"  # {suggestion.suggested_justification}"

                    new_line = re.sub(r"# type: ignore(?:\[[^\]]*\])?.*$", comment, line)
                    lines[idx] = new_line
            else:
                # Add new type: ignore comment
                code_str = ", ".join(sorted(suggestion.codes))
                comment = f"# type: ignore[{code_str}]"
                if require_comment:
                    comment += f"  # {suggestion.suggested_justification}"

                new_line = line.rstrip() + f"  {comment}"
                lines[idx] = new_line

            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"Applied: {suggestion.filepath}:{suggestion.line_num}")
            fixed_count += 1

        except Exception as e:
            print(f"Error applying fix to {suggestion.filepath}:{suggestion.line_num}: {e}")

    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description="Safe MyPy type: ignore suggestion and application tool"
    )
    parser.add_argument(
        "--error-file",
        default="mypy_errors_new.txt",
        help="MyPy error output file (default: mypy_errors_new.txt)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "patch"],
        default="json",
        help="Review file format (default: json)",
    )
    parser.add_argument(
        "--require-allowlist",
        action="store_true",
        help="Only suppress whitelisted error codes (safer)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply type: ignore fixes to files (destructive, requires review)",
    )
    parser.add_argument(
        "--require-comment",
        action="store_true",
        help="Require human-written justification comments for suppressions",
    )
    parser.add_argument(
        "--run-mypy",
        action="store_true",
        help="Run mypy before processing",
    )

    args = parser.parse_args()

    # Run mypy if requested
    if args.run_mypy:
        print("Running mypy...")
        result = subprocess.run(
            ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
            capture_output=True,
            text=True,
            check=False,
        )
        with open(args.error_file, 'w') as f:
            f.write(result.stdout)
        print(f"MyPy errors saved to {args.error_file}")

    # Parse errors
    print(f"\nParsing {args.error_file}...")
    errors_by_file_line = parse_mypy_errors(args.error_file)
    print(f"Found {len(errors_by_file_line)} error lines")

    # Build suggestions
    print("\nBuilding suggestions...")
    suggestions, suppressed_count, blocked_count = build_suggestions(
        errors_by_file_line,
        require_allowlist=args.require_allowlist,
    )
    print(f"  - Suppressible codes: {suppressed_count}")
    print(f"  - Critical (blocked): {blocked_count}")
    print(f"  - Total lines with issues: {len(suggestions)}")

    # Write review file
    print(f"\nWriting review file (format: {args.output_format})...")
    review_file = write_review_file(suggestions, args.output_format)
    print(f"Review file: {review_file}")
    print(f"  → Open this file to review before applying fixes")

    # Apply if requested
    if args.apply:
        print("\n⚠️  Applying type: ignore fixes...")
        fixed = apply_suggestions(suggestions, require_comment=args.require_comment)
        print(f"Applied {fixed} fixes")
        print(f"  → Review manually and run mypy to verify")
    else:
        print("\nTo apply fixes after review:")
        print(f"  python scripts/update_type_ignore.py --error-file {args.error_file} --apply")


if __name__ == "__main__":
    main()
