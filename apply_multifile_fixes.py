#!/usr/bin/env python3
"""Apply multiple fixes across project files"""
import re
from pathlib import Path

paths = [
    'opt/services/marketplace/governance.py',
    'scripts/agent/base_agent.py',
    'scripts/agent/agent.py',
    'scripts/agent/agent-improvements.py',
    'scripts/agent/agent-stats.py',
    'scripts/agent/agent-tests.py',
]

total_fixed = 0

for file_path in paths:
    p = Path(file_path)
    if not p.exists():
        print(f'⊘ Skipped {file_path} (not found)')
        continue
        
    try:
        content = p.read_text(encoding='utf-8')
        original_content = content
        lines = content.split('\n')
        
        # Fix E225 missing whitespace around operators
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                continue
            # Fix _var= patterns
            line = re.sub(r'_([a-zA-Z_]\w*)\s*=([^=\s])', r'_\1 = \2', line)
            # Fix var= patterns (but not in keyword args/default params)
            if 'def ' not in line and 'lambda' not in line and '(' not in line:
                # Simple var=value at statement level
                line = re.sub(r'\b([a-zA-Z_]\w*)\s*=\s*([a-zA-Z_0-9"\'])', r'\1 = \2', line)
            lines[i] = line
        
        new_content = '\n'.join(lines)
        if new_content != original_content:
            p.write_text(new_content, encoding='utf-8')
            fixed = len([1 for o, n in zip(original_content.split('\n'), new_content.split('\n')) if o != n])
            print(f'✓ {file_path}: {fixed} fixes')
            total_fixed += fixed
    except Exception as e:
        print(f'✗ {file_path}: {e}')

print(f'\nTotal: {total_fixed} fixes applied')
