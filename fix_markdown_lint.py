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

        # Numbered list: e.g., 1.Item -> 1. Item
        if len(line) > 2 and line[0].isdigit():
            # find the run of digits
            j = 0
            while j < len(line) and line[j].isdigit():
                j += 1
            if j < len(line) and line[j] == '.' and (j + 1) < len(line) and line[j + 1] != ' ':
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
