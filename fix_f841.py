#!/usr/bin/env python3
"""Remove unused exception variables like 'except Exception as e:' where e is never used"""

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
    
    # Simply remove "as e" from except clauses (leaves the exception handling intact)
    # Pattern: "except SomeException as variable:"
    new_content = re.sub(
        r'except\s+(\w+(?:\s*,\s*\w+)*)\s+as\s+\w+:',
        r'except \1:',
        content
    )
    
    if new_content != original:
        fixes = content.count(' as ') - new_content.count(' as ')
        try:
            py_file.write_text(new_content, encoding = 'utf-8')
            if fixes > 0:
                print(f"{py_file.name}: {fixes} fixes")
                total_fixes += fixes
        except Exception as e:
            print(f"Error writing {py_file.name}: {e}")

print(f"\nTotal fixes: {total_fixes}")
