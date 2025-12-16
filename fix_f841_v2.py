#!/usr/bin/env python3
"""Fix F841 - Unused variables (only obvious patterns)"""

import subprocess
from pathlib import Path
import re

# Get F841 issues
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', '--select = F841'],
    capture_output = True,
    text = True
)

issues = {}
for line in result.stdout.split('\n'):
    if 'F841' in line:
        # Extract filename and variable name
        parts = line.split(':')
        if len(parts) >= 3:
            filename = parts[0]
            try:
                line_num = int(parts[1])
                # Extract variable name from message (between quotes)
                var_match = re.search(r"'(\w+)'", line)
                if var_match:
                    var_name = var_match.group(1)
                    if filename not in issues:
                        issues[filename] = []
                    issues[filename].append((line_num, var_name))
            except ValueError:
                pass

if not issues:
    print("No F841 issues found!")
else:
    print(f"Found F841 issues in {len(issues)} files - applying only safe fixes")
    total_fixes = 0
    
    for filepath, var_issues in issues.items():
        if not Path(filepath).exists():
            continue
        
        try:
            content = Path(filepath).read_text(encoding = 'utf-8')
            lines = content.split('\n')
        except:
            continue
        
        original_content = content
        fixes = 0
        
        for line_num, var_name in var_issues:
            if line_num <= 0 or line_num > len(lines):
                continue
            
            line = lines[line_num - 1]
            
            # Pattern 1: "x = something" where x is never used after
            # Only remove if it's a standalone assignment
            if re.match(rf'\s*{re.escape(var_name)}\s*=\s*.+', line):
                # Check if variable is used anywhere else in file
                usage_count = len(re.findall(rf'\b{re.escape(var_name)}\b', content))
                
                # If only appears once (in the assignment), remove the line
                if usage_count == 1:
                    # Try to remove just the assignment part
                    # But only if it's safe (not part of tuple unpacking, etc.)
                    if ',' not in line.split('=')[0]:
                        lines[line_num - 1] = ''
                        fixes += 1
            
            # Pattern 2: Assignments in try/except blocks that aren't used
            # Skip these - too risky
        
        new_content = '\n'.join(lines)
        if new_content != original_content:
            try:
                Path(filepath).write_text(new_content, encoding = 'utf-8')
                if fixes > 0:
                    print(f"  {Path(filepath).name}: {fixes} F841 fixes")
                    total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal F841 fixes: {total_fixes}")
