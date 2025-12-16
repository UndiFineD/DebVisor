#!/usr/bin/env python3
"""Fix F541 - empty f-strings, and E302/E305 blank line spacing"""

import re
from pathlib import Path

agent_dir = Path('scripts/agent')
total_fixes = 0

for py_file in sorted(agent_dir.glob('*.py')):
    if not py_file.is_file():
        continue
    
    try:
        content = py_file.read_text(encoding = 'utf-8')
    except:
        continue
    
    original = content
    fixes = 0
    
    # Fix F541 - empty f-strings like f"" or f'' should be regular strings
    # Pattern: f"" or f'' with no content between quotes
    new_content = re.sub(r"f(['\"])(?=['\"])", r"\1", content)
    if new_content != content:
        fixes += content.count('f""') + content.count("f''")
        content = new_content
    
    # Fix f-strings that only have whitespace
    new_content = re.sub(r"f(['\"])\s+\1", r"\1\1", content)
    if new_content != content:
        fixes += (len(content) - len(new_content)) // 2
        content = new_content
    
    if content != original:
        try:
            py_file.write_text(content, encoding = 'utf-8')
            if fixes > 0:
                print(f"{py_file.name}: {fixes} F541 fixes")
                total_fixes += fixes
        except Exception as e:
            print(f"Error writing {py_file.name}: {e}")

print(f"\nTotal F541 fixes: {total_fixes}")
