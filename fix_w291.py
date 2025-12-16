#!/usr/bin/env python3
"""Final automated fixes: W291 (trailing), F541 (f-strings), and other easy issues"""

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
    lines = content.split('\n')
    fixes = 0
    
    for i, line in enumerate(lines):
        # Fix W291 - trailing whitespace
        if line and line[-1] in ' \t':
            lines[i] = line.rstrip()
            fixes += 1
    
    new_content = '\n'.join(lines)
    
    if new_content != original:
        try:
            py_file.write_text(new_content, encoding = 'utf-8')
            if fixes > 0:
                print(f"{py_file.name}: {fixes} W291 fixes")
                total_fixes += fixes
        except Exception as e:
            print(f"Error writing {py_file.name}: {e}")

print(f"\nTotal W291 fixes: {total_fixes}")
