#!/usr/bin/env python3
"""Fix E251 errors - spaces around = in function parameters"""
import re
from pathlib import Path

def fix_e251_in_file(file_path):
    """Remove spaces around = in function parameter contexts."""
    path = Path(file_path)
    content = path.read_text(encoding='utf-8')
    original = content
    
    # Fix: parameter = value → parameter=value within function contexts
    # This pattern: word followed by spaces, =, spaces, then a value
    # Used in function calls and definitions
    content = re.sub(r'(\w+)\s+=\s+', r'\1=', content)
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False

# Core files to process
core_files = [
    'agent_backend.py',
    'agent-changes.py',
    'agent-coder.py',
    'agent-context.py',
    'agent-errors.py',
    'agent-improvements.py',
    'agent-stats.py',
    'agent-tests.py',
    'agent.py',
    'base_agent.py',
    'generate_agent_reports.py',
    'agent_test_utils.py',
]

agent_dir = Path('scripts/agent')
fixed_count = 0

for file_name in core_files:
    file_path = agent_dir / file_name
    if file_path.exists():
        if fix_e251_in_file(str(file_path)):
            print(f"✓ {file_name}")
            fixed_count += 1

print(f"\n✅ Fixed {fixed_count} files")
