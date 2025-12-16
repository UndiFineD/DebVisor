#!/usr/bin/env python3
"""Remove obviously unused imports - simple approach"""

import subprocess
from pathlib import Path
import re

# Get F401 issues
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', '--select=F401'],
    capture_output=True,
    text=True
)

issues = {}
for line in result.stdout.split('\n'):
    if 'F401' in line:
        parts = line.split("'")
        if len(parts) >= 2:
            filename = line.split(':')[0]
            unused_name = parts[1]  # The imported name
            if filename not in issues:
                issues[filename] = []
            issues[filename].append(unused_name)

if not issues:
    print("No F401 issues found!")
else:
    print(f"Found F401 issues in {len(issues)} files - being conservative with changes")
    total_fixes = 0
    
    for filepath, unused_names in issues.items():
        if not Path(filepath).exists():
            continue
        
        try:
            content = Path(filepath).read_text(encoding='utf-8')
        except:
            continue
        
        original = content
        fixes = 0
        
        # Simple approach: only remove if it's a standalone import line
        # and the name appears only in the import (once)
        for name in unused_names:
            usage_count = len(re.findall(rf'\b{re.escape(name)}\b', content))
            
            # Only remove if it appears exactly once (in import only)
            if usage_count == 1:
                # Try to remove the line with just this import
                pattern = rf'^from\s+[\w.]+\s+import\s+{re.escape(name)}\s*\n'
                if re.search(pattern, content, re.MULTILINE):
                    content = re.sub(pattern, '', content, flags=re.MULTILINE)
                    fixes += 1
                else:
                    # Try removing from multi-import line
                    pattern = rf',\s*{re.escape(name)}(?=\s*(?:[,\)]|$))'
                    if re.search(pattern, content):
                        content = re.sub(pattern, '', content)
                        fixes += 1
        
        if content != original:
            try:
                Path(filepath).write_text(content, encoding='utf-8')
                if fixes > 0:
                    print(f"  {Path(filepath).name}: {fixes} unused imports removed")
                    total_fixes += fixes
            except Exception as e:
                print(f"  Error writing {filepath}: {e}")
    
    print(f"\nTotal F401 fixes: {total_fixes}")
