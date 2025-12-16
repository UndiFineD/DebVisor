#!/usr/bin/env python3
"""Fix E999 syntax errors - incomplete import statements"""

import re
from pathlib import Path
import subprocess

# First, get files with E999 errors
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', 
     '--select=E999'],
    capture_output=True,
    text=True
)

e999_files = {}
for line in result.stdout.split('\n'):
    if line.strip():
        parts = line.split(':')
        if len(parts) >= 2:
            filename = parts[0]
            try:
                line_num = int(parts[1])
                if filename not in e999_files:
                    e999_files[filename] = []
                e999_files[filename].append(line_num)
            except ValueError:
                pass

if not e999_files:
    print("No E999 errors found!")
else:
    print(f"Found E999 errors in {len(e999_files)} files")
    
    total_fixes = 0
    for filepath in sorted(e999_files.keys()):
        if not Path(filepath).exists():
            continue
        
        try:
            content = Path(filepath).read_text(encoding='utf-8')
        except:
            continue
        
        original = content
        lines = content.split('\n')
        fixes = 0
        
        # Fix broken "from X import" statements
        # These appear as incomplete imports at end of file
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            # Pattern: "from X import" with nothing after or just comma/whitespace
            if re.match(r'\s*from\s+[\w\.]+\s+import\s*$', line):
                # Remove this line - it's incomplete
                lines.pop(i)
                fixes += 1
            elif re.match(r'\s*from\s+[\w\.]+\s+import\s*,\s*$', line):
                # Remove trailing comma and blank
                lines.pop(i)
                fixes += 1
            # Also fix lines that end with just "as"
            elif re.match(r'\s*from\s+[\w\.]+\s+import\s+.*\s+as\s*$', line):
                lines.pop(i)
                fixes += 1
        
        if fixes > 0:
            new_content = '\n'.join(lines)
            try:
                Path(filepath).write_text(new_content, encoding='utf-8')
                print(f"  {Path(filepath).name}: {fixes} fixes")
                total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal E999 fixes: {total_fixes}")
