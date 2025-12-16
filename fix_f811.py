#!/usr/bin/env python3
"""Fix F811 - redefinition of unused name patterns"""

import subprocess
from pathlib import Path
import re

# Get F811 issues
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', 
     '--select = F811,F806'],
    capture_output = True,
    text = True
)

issues_by_file = {}
for line in result.stdout.split('\n'):
    if 'F811' in line or 'F806' in line:
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
    print("No F811/F806 issues found!")
else:
    print(f"Found issues in {len(issues_by_file)} files")
    
    total_fixes = 0
    for filepath, line_nums in issues_by_file.items():
        if not Path(filepath).exists():
            continue
        
        try:
            lines = Path(filepath).read_text(encoding = 'utf-8').split('\n')
        except:
            continue
        
        fixes = 0
        
        # Remove duplicate import statements (keep first occurrence)
        seen_imports = {}
        for i, line in enumerate(lines):
            # Match import patterns: "from X import Y" or "import X"
            import_match = re.match(r'\s*(from .+ import .+|import .+)$', line)
            if import_match:
                import_stmt = import_match.group(1).strip()
                if import_stmt in seen_imports:
                    # Duplicate import - remove it
                    lines[i] = ''
                    fixes += 1
                else:
                    seen_imports[import_stmt] = i
        
        if fixes > 0:
            new_content = '\n'.join(lines)
            try:
                Path(filepath).write_text(new_content, encoding = 'utf-8')
                print(f"  {Path(filepath).name}: {fixes} duplicate imports removed")
                total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal F811 fixes: {total_fixes}")
