#!/usr/bin/env python3
"""Remove W293 blank lines containing whitespace"""

from pathlib import Path

agent_dir = Path('scripts/agent')
total_fixes = 0

for py_file in sorted(agent_dir.glob('*.py')):
    if not py_file.is_file():
        continue
    
    try:
        content = py_file.read_text(encoding='utf-8')
    except:
        continue
    
    original = content
    lines = content.split('\n')
    fixes = 0
    
    # Remove whitespace from blank lines
    for i, line in enumerate(lines):
        # If line is only whitespace, make it empty
        if line and line.strip() == '':
            lines[i] = ''
            fixes += 1
    
    new_content = '\n'.join(lines)
    
    if new_content != original:
        try:
            py_file.write_text(new_content, encoding='utf-8')
            if fixes > 0:
                print(f"{py_file.name}: {fixes} W293 fixes")
                total_fixes += fixes
        except Exception as e:
            print(f"Error writing {py_file.name}: {e}")

print(f"\nTotal W293 fixes: {total_fixes}")
