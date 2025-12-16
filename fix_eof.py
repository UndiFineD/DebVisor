#!/usr/bin/env python3
"""Fix W391 - blank lines at end of file, and other trailing issues"""

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
    fixes = 0
    
    # Fix W391 - remove blank lines at end of file
    # Keep only one trailing newline
    while content.endswith('\n\n'):
        content = content[:-1]
        fixes += 1
    
    # Ensure file ends with exactly one newline (not zero, not more than one)
    if not content.endswith('\n'):
        content += '\n'
        fixes += 1
    elif content.endswith('\n\n'):
        content = content[:-1]
        fixes += 1
    
    if content != original:
        try:
            py_file.write_text(content, encoding='utf-8')
            if fixes > 0:
                print(f"{py_file.name}: {fixes} EOF/W391 fixes")
                total_fixes += fixes
        except Exception as e:
            print(f"Error writing {py_file.name}: {e}")

print(f"\nTotal EOF fixes: {total_fixes}")
