
import re
from pathlib import Path

FILES_TO_FIX = [
    "opt/web/panel/routes/auth.py",
    "scripts/auto_fix_mypy.py",
    "scripts/license_header_check.py",
    "tests/test_acme_certificates.py",
    "tests/test_api_key_rotation.py",
    "tests/test_audit_chain.py",
    "tests/test_audit_encryption.py",
    "tests/test_backup_manager_encryption.py",
    "tests/test_compliance_remediation.py",
    "tests/test_dns_hosting.py",
    "tests/test_hvctl_xen.py",
    "tests/test_integration_suite.py",
    "tests/test_licensing.py",
    "tests/test_marketplace_governance.py",
    "tests/test_migrations.py",
    "tests/test_runbooks.py",
    "tests/test_ssh_hardening.py",
]

def undo_fixes():
    root = Path(".")
    pattern = re.compile(r"^(\s*)    # (from|import)(.*)$")

    for file_path_str in FILES_TO_FIX:
        file_path = root / file_path_str
        if not file_path.exists():
            print(f"Skipping {file_path} (not found)")
            continue

        print(f"Repairing {file_path}...")
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        fixed_count = 0
        for line in lines:
            match = pattern.match(line)
            if match:
                # match.group(1) is original indentation (before my script added 4 spaces? No, my script added 4 spaces to the *indentation*)
                # Wait, my script did: lines[line_num] = " " * indent + "    # " + line.lstrip()
                # So the line is: <indent>    # <content>
                # I want to restore: <indent><content>
                
                # The regex `^(\s*)    # (from|import)(.*)$` captures:
                # group 1: the indentation before `    # `
                # group 2: `from` or `import`
                # group 3: the rest of the line
                
                indent = match.group(1)
                keyword = match.group(2)
                rest = match.group(3)
                
                # Restore: indent + keyword + rest
                # But wait, my script calculated indent as `len(line) - len(line.lstrip())` of the ORIGINAL line.
                # And then constructed: " " * indent + "    # " + line.lstrip()
                # So `match.group(1)` IS the original indentation.
                
                restored_line = f"{indent}{keyword}{rest}\n"
                new_lines.append(restored_line)
                fixed_count += 1
            else:
                new_lines.append(line)

        if fixed_count > 0:
            with file_path.open("w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"  Restored {fixed_count} lines.")
        else:
            print("  No lines matched.")

if __name__ == "__main__":
    undo_fixes()
