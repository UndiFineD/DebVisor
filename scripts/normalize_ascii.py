import sys
import os
import subprocess

COMMON_MAP = {
    # Dashes
    "\u2014": "--",  # em dash
    "\u2013": "-",   # en dash
    "\u2012": "-",   # figure dash
    # Quotes
    "\u2018": "'", "\u2019": "'",
    "\u201C": '"', "\u201D": '"',
    # Arrows
    "\u2192": "->",
    "\u2190": "<-",
    "\u2191": "^",
    "\u2193": "v",
    # Copyright / symbols
    "\u00A9": "(c)",
    "\u00AE": "(R)",
    # Box drawing (map to simple ASCII)
    "\u2500": "-", "\u2501": "-", "\u2502": "|", "\u2503": "|",
    "\u250C": "+", "\u2510": "+", "\u2514": "+", "\u2518": "+",
    "\u251C": "+", "\u2524": "+", "\u252C": "+", "\u2534": "+", "\u253C": "+",
    # Bullet
    "\u2022": "*",
    # Emojis / misc (lock, warning, info etc) -> textual tags
    "\u2699": "[gear]",
    "\u26A0": "[warn]",
    # Generic replacement for any remaining non-ASCII handled later
}

TEXT_EXTS = {
    ".md", ".txt", ".py", ".js", ".ts", ".json", ".yml", ".yaml", ".sh", ".ps1", ".bat",
    ".html", ".css", ".cfg", ".ini", ".conf", ".rego", ".sql"
}

def is_text(path: str) -> bool:
    return os.path.splitext(path)[1].lower() in TEXT_EXTS

def normalize_content(content: str) -> tuple[str, int]:
    changed = 0
    out_chars = []
    for ch in content:
        if ord(ch) < 128:
            out_chars.append(ch)
            continue
        replacement = COMMON_MAP.get(ch)
        if replacement is None:
            # Fallback: describe hex code in brackets if emoji-like, else '?'
            code = ord(ch)
            if code > 0xFFFF:
                replacement = f"[U+{code:04X}]"
            else:
                replacement = "?"
        out_chars.append(replacement)
        changed += 1
    return "".join(out_chars), changed

def git_tracked_files() -> list[str]:
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files

def main(argv: list[str]) -> int:
    write = "--write" in argv
    files = git_tracked_files()
    total_changed = 0
    affected = []
    for path in files:
        if path.startswith(".venv/") or not is_text(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                original = f.read()
        except Exception:
            continue
        new_content, changed = normalize_content(original)
        if changed:
            affected.append((path, changed))
            total_changed += changed
            if write:
                try:
                    with open(path, "w", encoding="ascii", errors="ignore") as f:
                        f.write(new_content)
                except Exception as e:
                    print(f"[ERROR] Writing {path}: {e}")
    if affected:
        print("Normalized non-ASCII characters in:")
        for p, c in affected[:50]:
            print(f"  {p} ({c} repl)")
        if len(affected) > 50:
            print(f"  ... {len(affected) - 50} more files")
        print(f"Total replacements: {total_changed}")
        if not write:
            print("Run with --write to apply changes.")
        return 1 if not write else 0
    else:
        print("No non-ASCII characters found.")
        return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
