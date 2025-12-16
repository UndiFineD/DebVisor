#!/usr/bin/env python3
"""Fix E501 - Lines too long (smart breaking for obvious cases)"""

import subprocess
from pathlib import Path
import re

# Get E501 issues
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', 
     '--select = E501', '--max-line-length = 120'],
    capture_output = True,
    text = True
)

issues_by_file = {}
for line in result.stdout.split('\n'):
    if 'E501' in line:
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
    print("No E501 issues found!")
else:
    print(f"Found E501 issues in {len(issues_by_file)} files")
    total_fixes = 0
    
    for filepath, line_nums in issues_by_file.items():
        if not Path(filepath).exists():
            continue
        
        try:
            lines = Path(filepath).read_text(encoding = 'utf-8').split('\n')
        except:
            continue
        
        fixes = 0
        
        for line_num in line_nums:
            if line_num > 0 and line_num <= len(lines):
                line = lines[line_num - 1]
                
                # Only fix lines that are slightly over (121-150 chars)
                # Skip very long lines that need more complex refactoring
                if len(line) <= 150:
                    # Pattern 1: Long string concatenation
                    if ' + ' in line and len(line) > 120:
                        # Try to break at the last +
                        match = re.search(r'(.{0,120})\s*\+\s*(.+)', line)
                        if match:
                            indent = len(line) - len(line.lstrip())
                            part1 = match.group(1).rstrip()
                            part2 = match.group(2).lstrip()
                            lines[line_num - 1] = part1 + ' +'
                            lines.insert(line_num, ' ' * (indent + 4) + part2)
                            fixes += 1
                    
                    # Pattern 2: Function call with many arguments on one line
                    elif '(' in line and ')' in line and len(line) > 120:
                        # Try to find opening paren and break after comma
                        match = re.match(r'(\s*)(.+?)\((.{50,})\)', line)
                        if match:
                            indent = len(match.group(1))
                            func = match.group(2)
                            args = match.group(3)
                            # Find last comma within 120 chars
                            truncated = args[:120-len(func)-2]
                            last_comma = truncated.rfind(',')
                            if last_comma > 0:
                                part1 = args[:last_comma + 1]
                                part2 = args[last_comma + 1:].lstrip()
                                lines[line_num - 1] = ' ' * indent + func + '(' + part1
                                lines.insert(line_num, ' ' * (indent + 4) + part2 + ')')
                                fixes += 1
        
        if fixes > 0:
            new_content = '\n'.join(lines)
            try:
                Path(filepath).write_text(new_content, encoding = 'utf-8')
                print(f"  {Path(filepath).name}: {fixes} line length fixes")
                total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal E501 fixes: {total_fixes}")
