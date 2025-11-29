import sys
import os


def is_text_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    # Common text/code/doc extensions
    text_exts = {
        ".py", ".js", ".ts", ".json", ".yml", ".yaml", ".md", ".txt",
        ".sh", ".ps1", ".bat", ".ini", ".cfg", ".conf", ".properties",
        ".css", ".html", ".rego"
    }
    return ext in text_exts


def check_file(path: str) -> list[tuple[int, str]]:
    issues = []
    try:
        with open(path, "rb") as f:
            data = f.read()
        # Try decoding as ASCII strictly
        try:
            text = data.decode("ascii")
        except UnicodeDecodeError:
            # Find offending bytes by scanning
            for i, b in enumerate(data):
                if b > 0x7F:
                    issues.append((i, f"non-ASCII byte 0x{b:02X}"))
            return issues
        # If decodes, also check for BOM or control chars beyond \n,\r,\t
        for idx, ch in enumerate(text):
            code = ord(ch)
            if code > 0x7F:
                issues.append((idx, f"non-ASCII char U+{code:04X}"))
            elif code < 0x20 and ch not in ("\n", "\r", "\t"):
                issues.append((idx, f"control char U+{code:04X}"))
    except Exception as e:
        issues.append((-1, f"error reading file: {e}"))
    return issues


def main(paths: list[str]) -> int:
    if not paths:
        print("Usage: python scripts/check_ascii.py <paths...>")
        return 2
    failures = 0
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for name in files:
                    fp = os.path.join(root, name)
                    if not is_text_file(fp):
                        continue
                    issues = check_file(fp)
                    if issues:
                        failures += 1
                        print(f"[NON-ASCII] {fp}")
                        # Show up to first 10 issues to keep output readable
                        for pos, msg in issues[:10]:
                            print(f"  at byte/char {pos}: {msg}")
        else:
            if not is_text_file(p):
                continue
            issues = check_file(p)
            if issues:
                failures += 1
                print(f"[NON-ASCII] {p}")
                for pos, msg in issues[:10]:
                    print(f"  at byte/char {pos}: {msg}")
    if failures:
        print(f"\nFound non-ASCII content in {failures} file(s).")
        return 1
    print("All checked files are ASCII-only.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
