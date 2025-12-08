import os
import re


def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "datetime.now(timezone.utc)" not in content:
        return False

    # 1. Fix imports
    # Look for "from datetime import ...", timezone
    # We want to ensure "timezone" is in there.

    # Regex for "from datetime import ...", timezone
    # It might be multi-line, but usually it's single line in this codebase based on grep.
    # We'll handle the simple case first.

    def add_timezone_to_import(match):
        imports = match.group(1)
        if "timezone" not in imports:
            return f"from datetime import {imports}, timezone"
        return match.group(0)

    new_content = re.sub(
        r"from datetime import ([^\n]+)", add_timezone_to_import, content
    )

    # If "import datetime" is used instead of "from datetime import ...",
    # we might need "datetime.timezone.utc"
    # But let's assume "from datetime import ..." is the norm for
    # "datetime.now(timezone.utc)" users.
    # If "timezone" is not imported, we might need to add it.

    # 2. Replace usage
    new_content = new_content.replace(
        "datetime.now(timezone.utc)", "datetime.now(timezone.utc)"
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def main():
    count = 0
    for root, dirs, files in os.walk("."):
        if "venv" in dirs:
            dirs.remove("venv")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    if fix_file(path):
                        print(f"Fixed: {path}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    print(f"Total files fixed: {count}")


if __name__ == "__main__":
    main()
