#!/usr/bin/env python3
"""
Final Production Markdown Linting Fixer

Fixes all markdown linting errors with precise algorithms:
    MD004: Unordered list style (use dash -)
    MD007: Unordered list indentation (use 2 spaces per level)
    MD009: Trailing spaces
    MD012: Multiple blank lines
    MD022: Blank lines around headings
    MD024: Duplicate headings (make unique)
    MD025: Multiple top-level headings (convert to  ##)
    MD029: Ordered list markers (use 1.)
    MD031: Blank lines around code fences
    MD032: Blank lines around lists
    MD040: Code fence language specification
    MD051: Link fragments should be valid (fix broken anchor links)

Usage:
    python fix_markdown_lint.py <file.md>
    python fix_markdown_lint.py <file1.md> <file2.md> ...
    python fix_markdown_lint.py --dry-run <file.md>
"""

import sys
import re
import glob
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class FixStats:
    """Statistics for fixes applied."""

    trailing_spaces: int = 0
    multiple_blanks: int = 0
    list_style: int = 0
    list_indent: int = 0
    ordered_list: int = 0
    code_fence_lang: int = 0
    duplicate_headings: int = 0
    multiple_h1: int = 0
    link_fragments: int = 0
    strong_style: int = 0

    def total(self) -> int:
        return (
            self.trailing_spaces
            + self.multiple_blanks
            + self.list_style
            + self.list_indent
            + self.ordered_list
            + self.code_fence_lang
            + self.duplicate_headings
            + self.multiple_h1
            + self.link_fragments
            + self.strong_style
        )

    def __str__(self) -> str:
        parts = []
        if self.trailing_spaces:
            parts.append(f"MD009 trailing spaces: {self.trailing_spaces}")
        if self.multiple_blanks:
            parts.append(f"MD012 multiple blanks: {self.multiple_blanks}")
        if self.list_style:
            parts.append(f"MD004 list style: {self.list_style}")
        if self.list_indent:
            parts.append(f"MD007 list indent: {self.list_indent}")
        if self.ordered_list:
            parts.append(f"MD029 ordered list: {self.ordered_list}")
        if self.code_fence_lang:
            parts.append(f"MD040 code fence lang: {self.code_fence_lang}")
        if self.duplicate_headings:
            parts.append(f"MD024 duplicate headings: {self.duplicate_headings}")
        if self.multiple_h1:
            parts.append(f"MD025 multiple H1: {self.multiple_h1}")
        if self.link_fragments:
            parts.append(f"MD051 link fragments: {self.link_fragments}")
        if self.strong_style:
            parts.append(f"MD050 strong style: {self.strong_style}")
        return ", ".join(parts) if parts else "No fixes needed"


def fix_markdown(filepath: str, dry_run: bool = False) -> FixStats:
    """Fix all markdown linting issues in a file."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return FixStats()

    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
        lines = original.split("\n")

    print(f"Processing: {filepath}")
    stats = FixStats()

    # Fix in order - some fixes depend on others
    lines, stats.trailing_spaces = fix_trailing_spaces(lines)  # MD009
    lines, stats.multiple_blanks = fix_multiple_blank_lines(lines)  # MD012
    lines, stats.list_style = fix_unordered_list_style(lines)  # MD004
    lines, stats.list_indent = fix_unordered_list_indent(lines)  # MD007
    lines, stats.ordered_list = fix_ordered_list_markers(lines)  # MD029
    lines, stats.code_fence_lang = fix_code_fence_language(lines)  # MD040
    lines = fix_blank_around_fences(lines)  # MD031
    lines = fix_blank_around_lists(lines)  # MD032
    lines = fix_blank_around_headings(lines)  # MD022
    lines, stats.duplicate_headings = fix_duplicate_headings(lines)  # MD024
    lines, stats.multiple_h1 = fix_multiple_h1(lines)  # MD025
    lines, stats.link_fragments = fix_link_fragments(lines)  # MD051
    lines, stats.strong_style = fix_strong_style(lines)  # MD050

    result = "\n".join(lines)

    if dry_run:
        if result != original:
            print(f"[DRY-RUN] Would fix: {stats}")
        else:
            print("[DRY-RUN] No changes needed")
    else:
        if result != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"[OK] Fixed: {stats}")
        else:
            print("[OK] No changes needed")

    return stats


def fix_trailing_spaces(lines: List[str]) -> Tuple[List[str], int]:
    """MD009: Remove trailing spaces."""
    result = []
    count = 0
    for line in lines:
        stripped = line.rstrip()
        if stripped != line:
            count += 1
        result.append(stripped)
    return result, count


def fix_multiple_blank_lines(lines: List[str]) -> Tuple[List[str], int]:
    """MD012: Reduce multiple blank lines to single blank line."""
    result = []
    prev_blank = False
    count = 0

    for line in lines:
        is_blank = not line.strip()

        if is_blank:
            if not prev_blank:
                result.append(line)
                prev_blank = True
            else:
                count += 1  # Skipping extra blank line
        else:
            result.append(line)
            prev_blank = False

    return result, count


def fix_unordered_list_style(lines: List[str]) -> Tuple[List[str], int]:
    """MD004: Convert * and + to - for unordered lists."""
    result = []
    count = 0
    in_code_block = False

    for line in lines:
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Match unordered list with * or + (with optional leading spaces)
        match = re.match(r"^(\s*)([*+])(\s+)", line)
        if match:
            # Replace * or + with -
            new_line = (
                match.group(1) + "-" + match.group(3) + line[len(match.group(0)) :]
            )
            result.append(new_line)
            count += 1
        else:
            result.append(line)

    return result, count


def fix_unordered_list_indent(lines: List[str]) -> Tuple[List[str], int]:
    """MD007: Fix unordered list indentation.

    Handles two cases:
    1. Sub-lists that should use 2-space indent per level
    2. Incorrectly indented lists that should be at column 0

    The rule is: if a list item is indented but NOT part of a properly
    structured nested list, remove the indentation.
    """
    result = []
    count = 0
    in_code_block = False
    # in_ordered_list = False

    for i, line in enumerate(lines):
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Track if we're inside an ordered list context
        if re.match(r"^\d+\.\s+", line):
            pass  # in_ordered_list = True
        elif line.strip() == "":
            # Blank line might end the ordered list context
            # Check if next non-blank is also ordered list or sub-item
            pass
        elif not line.startswith(" ") and not re.match(r"^\s*[-*+]\s+", line):
            pass  # in_ordered_list = False

        # Match unordered list item with leading spaces (2 spaces specifically for MD007)
        match = re.match(r"^(\s+)([-*+])(\s+)(.*)$", line)
        if match:
            indent = match.group(1)
            marker = match.group(2)
            space_after = match.group(3)
            content = match.group(4)
            current_spaces = len(indent)

            # Check previous line to determine context
            prev_line = lines[i - 1] if i > 0 else ""
            prev_is_ordered = bool(re.match(r"^\d+\.\s+", prev_line))
            prev_is_unordered = bool(re.match(r"^\s*[-*+]\s+", prev_line))
            prev_is_blank = prev_line.strip() == ""

            # If this is a 2-space indented list after an ordered list item,
            # it's likely meant to be a sub-item. Convert to no-indent.
            if current_spaces == 2 and (
                prev_is_ordered
                or (prev_is_unordered and not prev_line.startswith("  "))
            ):
                # Remove the 2-space indent - this should be a standalone list
                new_line = f"{marker}{space_after}{content}"
                result.append(new_line)
                count += 1
            # If indent is 4-space based, convert to 2-space based
            elif current_spaces >= 4 and current_spaces % 4 == 0:
                new_indent_level = current_spaces // 4
                new_indent = "  " * new_indent_level
                new_line = f"{new_indent}{marker}{space_after}{content}"
                if new_line != line:
                    count += 1
                result.append(new_line)
            elif current_spaces == 4:
                # Single level 4-space -> 2-space
                new_line = f"  {marker}{space_after}{content}"
                count += 1
                result.append(new_line)
            elif current_spaces == 2:
                # 2-space indent that's not after ordered list - might be valid nested
                # Check if previous unordered list is at column 0
                if prev_is_unordered and not prev_line.startswith(" "):
                    # This is a valid nested list, keep it
                    result.append(line)
                elif prev_is_blank:
                    # After blank line with 2-space indent - remove indent
                    new_line = f"{marker}{space_after}{content}"
                    result.append(new_line)
                    count += 1
                else:
                    result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)

    return result, count


def is_heading(line: str) -> bool:
    """Check if line is a heading."""
    return bool(re.match(r"^  #{1, 6}\s+", line))


def is_list_item(line: str) -> bool:
    """Check if line is a list item."""
    return bool(re.match(r"^\s*([-*+]|\d+\.)\s+", line))


def is_code_fence(line: str) -> bool:
    """Check if line is a code fence marker."""
    return bool(re.match(r"^\s*([`~]{3, })", line))


def is_table_row(line: str) -> bool:
    """Check if line is a table row."""
    return bool(re.match(r"^\s*\|.+\|\s*$", line))


def fix_ordered_list_markers(lines: List[str]) -> Tuple[List[str], int]:
    """MD029: Use 1. prefix for all ordered list items."""
    result = []
    count = 0
    in_code_block = False

    for line in lines:
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if not in_code_block:
            match = re.match(r"^(\s*)(\d+)(\.\s+)", line)
            if match and match.group(2) != "1":
                # Replace number with 1
                new_line = (
                    match.group(1) + "1" + match.group(3) + line[len(match.group(0)) :]
                )
                result.append(new_line)
                count += 1
                continue

        result.append(line)

    return result, count


def fix_code_fence_language(lines: List[str]) -> Tuple[List[str], int]:
    """MD040: Add language to code fences."""
    result: List[str] = []
    count = 0

    for line in lines:
        if re.match(r"^\s*```\s*$", line):
            result.append("```text")
            count += 1
        elif re.match(r"^\s*~~~\s*$", line):
            result.append("~~~text")
            count += 1
        else:
            result.append(line)

    return result, count


def fix_blank_around_fences(lines: List[str]) -> List[str]:
    """MD031: Add blank lines around code fences."""
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if is_code_fence(line):
            # Add blank line before fence if needed
            if i > 0 and result and result[-1].strip():
                result.append("")

            result.append(line)
            i += 1

            # Find closing fence and collect everything
            match_char = re.match(r"^\s*([`~])", line)
            match_len = re.match(r"^\s*([`~]+)", line)

            if not match_char or not match_len:
                continue

            fence_char = match_char.group(1)
            fence_len = len(match_len.group(1))

            while i < len(lines):
                result.append(lines[i])
                # Check if this closes the fence
                if re.match(
                    rf"^\s*{re.escape(fence_char)}{{{fence_len}, }}\s*$", lines[i]
                ):
                    i += 1
                    # Add blank line after fence if needed
                    if i < len(lines) and lines[i].strip():
                        result.append("")
                    break
                i += 1
        else:
            result.append(line)
            i += 1

    return result


def fix_blank_around_lists(lines: List[str]) -> List[str]:
    """MD032: Add blank lines around lists.

    Lists should be surrounded by blank lines. This includes:
    - Before the first item of a list
    - After the last item of a list
    - Between different types of lists (ordered vs unordered)
    """
    result = []
    in_code_block = False
    prev_is_list = False
    prev_is_ordered = False
    prev_is_unordered = False

    for i, line in enumerate(lines):
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            prev_is_list = False
            prev_is_ordered = False
            prev_is_unordered = False
            continue

        if in_code_block:
            result.append(line)
            continue

        is_ordered = bool(re.match(r"^\s*\d+\.\s+", line))
        is_unordered = bool(re.match(r"^\s*[-*+]\s+", line))
        is_list = is_ordered or is_unordered
        is_heading_line = is_heading(line)
        # is_table = is_table_row(line)
        # is_blank = not line.strip()

        if is_list:
            # Add blank line before list if:
            # 1. Previous is not blank/list
2. Transitioning from ordered to unordered or vice versa
            if result and result[-1].strip():
                should_add_blank = False

Not coming from a list - need blank line
                if (
                    not prev_is_list
                    and not is_heading(result[-1])
                    and not is_table_row(result[-1])
                ):
                    should_add_blank = True

                # Transitioning between list types
                if prev_is_ordered and is_unordered:
                    should_add_blank = True
                if prev_is_unordered and is_ordered:
                    should_add_blank = True

                if should_add_blank:
                    result.append("")

            result.append(line)
            prev_is_list = True
            prev_is_ordered = is_ordered
            prev_is_unordered = is_unordered
        else:
            # Add blank line after list if this line is not blank and not a heading
            if prev_is_list and line.strip() and not is_heading_line:
                result.append("")

            result.append(line)
            prev_is_list = False
            prev_is_ordered = False
            prev_is_unordered = False

    return result


def fix_blank_around_headings(lines: List[str]) -> List[str]:
    """MD022: Add blank lines around headings."""
    result = []
    in_code_block = False

    for i, line in enumerate(lines):
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        if is_heading(line):
            # Add blank line before heading if needed
            if result and result[-1].strip():
                result.append("")

            result.append(line)

            # Add blank line after heading if needed
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() and not is_heading(next_line):
                    result.append("")
        else:
            result.append(line)

    return result


def fix_duplicate_headings(lines: List[str]) -> Tuple[List[str], int]:
    """MD024: Handle duplicate headings by making them unique."""
    heading_counts: dict[str, int] = {}
    result = []
    count = 0

    for line in lines:
        if is_heading(line):
            match = re.match(r"^(  #+\s+)(.+?)(\s*)$", line)
            if match:
                prefix = match.group(1)
                heading_text = match.group(2).strip()
                suffix = match.group(3)

Create key from heading level and text
                level = len(prefix.rstrip())
                key = f"{level}:{heading_text.lower()}"

                if key in heading_counts:
                    heading_counts[key] += 1
                    occurrence = heading_counts[key]
                    new_line = f"{prefix}{heading_text} ({occurrence}){suffix}"
                    result.append(new_line)
                    count += 1
                else:
                    heading_counts[key] = 1
                    result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)

    return result, count


def fix_multiple_h1(lines: List[str]) -> Tuple[List[str], int]:
    """MD025: Convert multiple H1 headings to H2 (keep first H1 only)."""
    result = []
    count = 0
    found_h1 = False
    in_code_block = False

    for line in lines:
        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Check for H1 (single #)
        match = re.match(r"^  #\s+(.+)$", line)
        if match:
            if not found_h1:
                found_h1 = True
                result.append(line)
            else:
                # Convert subsequent H1 to H2
                new_line = f"  ## {match.group(1)}"
                result.append(new_line)
                count += 1
        else:
            result.append(line)

    return result, count


def heading_to_anchor(heading_text: str) -> str:
    """Convert a heading text to a GitHub-style anchor.

    Rules:
    - Convert to lowercase
    - Replace spaces with hyphens
    - Remove special characters except hyphens and underscores
    - Strip leading/trailing hyphens
    """
    # Remove markdown formatting (bold, italic, code, links)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", heading_text)  # bold
    text = re.sub(r"\*(.+?)\*", r"\1", text)  # italic
    text = re.sub(r"`(.+?)`", r"\1", text)  # inline code
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)  # links

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and special chars with hyphens
    text = re.sub(r"[^\w\s-]", "", text)  # Remove special chars
    text = re.sub(r"\s+", "-", text)  # Spaces to hyphens
    text = re.sub(r"-+", "-", text)  # Multiple hyphens to single
    text = text.strip("-")  # Strip leading/trailing hyphens

    return text


def collect_heading_anchors(lines: List[str]) -> dict[str, str]:
    """Collect all headings and their anchors from the document.

    Returns a dict mapping anchor names to themselves (valid anchors).
    Handles:
    - Standard GitHub-style anchors from heading text
    - Custom anchors with {  #anchor-id} syntax
    - Duplicate anchors by appending -1, -2, etc.
    """
    anchor_counts: dict[str, int] = {}
    heading_map: dict[str, str] = {}  # anchor -> anchor (valid anchors)
    in_code_block = False

    for line in lines:
        if is_code_fence(line):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Check for heading
        heading_match = re.match(r"^(  #+)\s+(.+?)\s*$", line)
        if heading_match:
            heading_text = heading_match.group(2)

            # Check for custom anchor syntax: {#custom-anchor}
            custom_anchor_match = re.search(r"\{  #([^}]+)\}\s*$", heading_text)
            if custom_anchor_match:
                # Use the custom anchor
                actual_anchor = custom_anchor_match.group(1)
                heading_map[actual_anchor] = actual_anchor

Also create mapping from heading text (without custom anchor) to custom anchor
                heading_without_anchor = re.sub(r"\s*\{  #[^}]+\}\s*$", "", heading_text)
                base_anchor = heading_to_anchor(heading_without_anchor)
                heading_map[base_anchor] = actual_anchor
            else:
Standard anchor from heading text
                base_anchor = heading_to_anchor(heading_text)

                if base_anchor in anchor_counts:
                    anchor_counts[base_anchor] += 1
                    actual_anchor = f"{base_anchor}-{anchor_counts[base_anchor]}"
                else:
                    anchor_counts[base_anchor] = 0
                    actual_anchor = base_anchor

                # Store mapping
                if base_anchor not in heading_map:
                    heading_map[base_anchor] = actual_anchor

                # Also store the actual anchor pointing to itself
                heading_map[actual_anchor] = actual_anchor

    return heading_map


def fix_link_fragments(lines: List[str]) -> Tuple[List[str], int]:
    """MD051: Fix invalid link fragments.

    Handles two cases:
    1. Custom anchor syntax {  #anchor} - converts to HTML anchor
    2. Broken links due to heading modifications - updates link targets

    This function:
    - Converts {  #custom-anchor} syntax to HTML anchors
    - Updates ToC links that point to non-existent anchors
    """
    count = 0
    in_code_block = False

    # First pass: collect all valid anchors and build mapping
    valid_anchors: set[str] = set()
    anchor_counts: dict[str, int] = {}

    for line in lines:
        if is_code_fence(line):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Check for heading
        heading_match = re.match(r"^  #+\s+(.+?)\s*$", line)
        if heading_match:
            heading_text = heading_match.group(1)

            # Check for custom anchor syntax
            custom_match = re.search(r"\{  #([^}]+)\}\s*$", heading_text)
            if custom_match:
                valid_anchors.add(custom_match.group(1))
                # Also add the text-based anchor
                heading_without_custom = re.sub(r"\s*\{  #[^}]+\}\s*$", "", heading_text)
                text_anchor = heading_to_anchor(heading_without_custom)
                valid_anchors.add(text_anchor)
            else:
                # Standard heading - compute anchor
                anchor = heading_to_anchor(heading_text)

                # Handle duplicates (same logic as GitHub)
                if anchor in anchor_counts:
                    anchor_counts[anchor] += 1
                    actual_anchor = f"{anchor}-{anchor_counts[anchor]}"
                else:
                    anchor_counts[anchor] = 0
                    actual_anchor = anchor

                valid_anchors.add(actual_anchor)

    # Second pass: process lines - fix custom anchors AND broken links
    result = []
    in_code_block = False
    link_pattern = re.compile(r'\[([^\]]+)\]\(  #([^)\s"]+)([^)]*)\)')

    i = 0
    while i < len(lines):
        line = lines[i]

        if is_code_fence(line):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Check if this heading has a custom anchor
        heading_match = re.match(r"^(  #+\s+)(.+?)\s*\{#([^}]+)\}\s*$", line)
        if heading_match:
            prefix = heading_match.group(1)
            heading_text = heading_match.group(2)
            anchor_id = heading_match.group(3)

            # Add HTML anchor before heading
            result.append(f'<a id="{anchor_id}"></a>')
            result.append("")

            # Keep heading but remove the {#anchor} part
            result.append(f"{prefix}{heading_text}")
            count += 1
            i += 1
            continue

        # Check for links with fragments and fix broken ones
        new_line = line
        for match in link_pattern.finditer(line):
            link_text = match.group(1)
            fragment = match.group(2)
            rest = match.group(3)

            if fragment not in valid_anchors:
                # Try to find a matching anchor
                # Look for anchors that start with the fragment or vice versa
                best_match = None

                for anchor in valid_anchors:
                    # Exact prefix match (e.g., "config" matches "configuration")
                    if anchor.startswith(fragment + "-") or anchor.startswith(fragment):
                        if best_match is None or len(anchor) < len(best_match):
                            best_match = anchor
                    # The fragment might be the base of a modified heading
                    # e.g., "configuration" -> "configuration-2"
                    if anchor.startswith(fragment) and anchor != fragment:
                        if best_match is None or len(anchor) < len(best_match):
                            best_match = anchor

                if best_match:
                    old_link = match.group(0)
                    new_link = f"[{link_text}](  #{best_match}{rest})"
                    new_line = new_line.replace(old_link, new_link, 1)
                    count += 1

        result.append(new_line)
        i += 1

    return result, count


def fix_strong_style(lines: List[str]) -> Tuple[List[str], int]:
    """MD050: Use asterisks for strong emphasis instead of underscores."""
    result = []
    count = 0
    in_code_block = False

    # Regex to match code spans OR strong emphasis
    # Group 1: Code span (`...`)
    # Group 2: Strong emphasis (__...__)
    # We use a simplified code span regex that assumes no nested backticks for now
    pattern = re.compile(r"(`[^`]+`)|((?<!_)__(.+?)__(?!_))")

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        def replace_func(match: re.Match[str]) -> str:
            if match.group(1):  # Code span - preserve as is
                return match.group(1)
            else:  # Strong emphasis - replace with asterisks
                return f"**{match.group(3)}**"

        new_line = pattern.sub(replace_func, line)

        if new_line != line:
            count += 1
        result.append(new_line)

    return result, count


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv
    args = [f for f in sys.argv[1:] if not f.startswith("--")]

    if not args:
        print("No files specified")
        sys.exit(1)

    # Expand glob patterns
    files = []
    for pattern in args:
        if "*" in pattern or "?" in pattern:
            expanded = glob.glob(pattern, recursive=True)
            files.extend(expanded)
        else:
            files.append(pattern)

    if not files:
        print("No files matched the pattern(s)")
        sys.exit(1)

    total_stats = FixStats()
    for filepath in files:
        stats = fix_markdown(filepath, dry_run=dry_run)
        total_stats.trailing_spaces += stats.trailing_spaces
        total_stats.multiple_blanks += stats.multiple_blanks
        total_stats.list_style += stats.list_style
        total_stats.list_indent += stats.list_indent
        total_stats.ordered_list += stats.ordered_list
        total_stats.code_fence_lang += stats.code_fence_lang
        total_stats.duplicate_headings += stats.duplicate_headings
        total_stats.multiple_h1 += stats.multiple_h1
        total_stats.link_fragments += stats.link_fragments

    print(f"\nProcessed {len(files)} file(s)")
    if total_stats.total() > 0:
        print(f"Total fixes: {total_stats.total()}")
        print(f"  {total_stats}")


if __name__ == "__main__":
    main()
