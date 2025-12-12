import sys
from pathlib import Path


def fix_markdown_content(text: str) -> str:
    lines = text.splitlines()
    fixed_lines = []

    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()

        # Replace tabs with 4 spaces
        line = line.replace("\t", "    ")

        # Ensure a space after heading markers (#)
        if line.startswith("#"):
            # Count leading #
            i = 0
            while i < len(line) and line[i] == '#':
                i += 1
            rest = line[i:]
            # If no space between hashes and text, add one
            if rest and not rest.startswith(" "):
                line = line[:i] + " " + rest

        # Ensure list markers have a space: -, *, +, and numbered lists
        for marker in ("-", "*", "+"):
            if line.startswith(marker) and not line.startswith(marker + " "):
                # Avoid horizontal rules (---) and code fences
                if not (marker == "-" and line.startswith("---")):
                    line = marker + " " + line[len(marker):]

        # Numbered list: add space only for patterns like "1.Item" -> "1. Item"
        # Avoid altering versions/decimals like "1.2", "v1.0.0", or file refs like "section1.2.md".
        if len(line) > 2 and line[0].isdigit():
            # find the run of leading digits
            j = 0
            while j < len(line) and line[j].isdigit():
                j += 1
            # must be followed by a single '.'
            if j < len(line) and line[j] == '.':
                # character after '.' must exist and not already be a space
                if (j + 1) < len(line) and line[j + 1] != ' ':
                    nxt = line[j + 1]
                    # Accept alphabetic list item starts or bracket/parenthesis (e.g., "1.(a)")
                    is_list_start = nxt.isalpha() or nxt in ('(', '[')
                    # Reject numeric/period continuation (likely version/decimal) e.g., "1.2", "1.."
                    is_numeric_or_period = nxt.isdigit() or nxt == '.'
                    # Also guard against immediate numeric/dot sequence like "1.2." or "1.2.3"
                    following = line[j + 1 : j + 5]  # small window
                    has_num_dot_sequence = False
                    # simple heuristic: any pattern digit '.' digit within the window signals versioning
                    for k in range(len(following) - 2):
                        if following[k].isdigit() and following[k + 1] == '.' and following[k + 2].isdigit():
                            has_num_dot_sequence = True
                            break

                    if is_list_start and not is_numeric_or_period and not has_num_dot_sequence:
                        line = line[: j + 1] + " " + line[j + 1 :]

        fixed_lines.append(line)

    fixed_text = "\n".join(fixed_lines)

    # Ensure file ends with a single newline
    if not fixed_text.endswith("\n"):
        fixed_text += "\n"

    return fixed_text


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fix_markdown_lint.py <markdown-file> [more files...]")
        return 2

    exit_code = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"Skipping missing file: {path}")
            exit_code = 1
            continue
        try:
            original = path.read_text(encoding="utf-8")
            fixed = fix_markdown_content(original)
            if fixed != original:
                path.write_text(fixed, encoding="utf-8")
                print(f"Fixed: {path}")
            else:
                print(f"No changes: {path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
