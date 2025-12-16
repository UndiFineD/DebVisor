#!/usr/bin/env python3
"""Fix E302/E305 - Missing blank lines before class/function definitions"""

import subprocess
from pathlib import Path
import re

# Get E302/E305 issues
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', 
     '--select=E302,E305'],
    capture_output=True,
    text=True
)

issues_by_file = {}
for line in result.stdout.split('\n'):
    if 'E302' in line or 'E305' in line:
        parts = line.split(':')
        if len(parts) >= 2:
            filename = parts[0]
            try:
                line_num = int(parts[1])
                if filename not in issues_by_file:
                    issues_by_file[filename] = []
                issues_by_file[filename].append(line_num)
            except ValueError:
                pass

if not issues_by_file:
    print("No E302/E305 issues found!")
else:
    print(f"Found E302/E305 issues in {len(issues_by_file)} files")
    total_fixes = 0
    
    for filepath, line_nums in issues_by_file.items():
        if not Path(filepath).exists():
            continue
        
        try:
            lines = Path(filepath).read_text(encoding='utf-8').split('\n')
        except:
            continue
        
        fixes = 0
        processed = set()  # Track which lines we've modified
        
        # Sort in reverse to avoid index shifting issues
        for line_num in sorted(set(line_nums), reverse=True):
            if line_num in processed or line_num <= 0 or line_num > len(lines):
                continue
            
            current_line = lines[line_num - 1]
            
            # Check if this is a class or function definition
            if re.match(r'\s*(class|def|async def)\s+', current_line):
                # Count blank lines before this line
                blank_count = 0
                idx = line_num - 2
                while idx >= 0 and lines[idx].strip() == '':
                    blank_count += 1
                    idx -= 1
                
                # We need 2 blank lines (except at start of file or after decorators)
                if idx >= 0:
                    prev_line = lines[idx]
                    
                    # Don't add if previous line is a decorator, import, or we're at file start
                    if not prev_line.strip().startswith('@') and not prev_line.strip().startswith('import') and not prev_line.strip().startswith('from'):
                        # If we have less than 2 blank lines, add them
                        if blank_count < 2:
                            needed = 2 - blank_count
                            for _ in range(needed):
                                lines.insert(line_num - 1, '')
                                processed.add(line_num - 1)
                            fixes += needed
        
        if fixes > 0:
            new_content = '\n'.join(lines)
            try:
                Path(filepath).write_text(new_content, encoding='utf-8')
                print(f"  {Path(filepath).name}: {fixes} blank line fixes")
                total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal E302/E305 fixes: {total_fixes}")
