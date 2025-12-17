#!/usr/bin/env python3
"""Fix E225 errors in core agent files"""
import re
from pathlib import Path

def fix_assignment_spacing(file_path):
    """Fix missing spaces around = in assignments (class vars, enums, etc)."""
    path = Path(file_path)
    content = path.read_text(encoding='utf-8')
    original = content
    
    # Pattern: identifier followed immediately by = (no spaces)
    # Match: WORD= or word= or _word=
    # Need spaces around the =
    content = re.sub(r'(\w+)=(?!=)', r'\1 = ', content)
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False

# Process only core (non-test) agent files
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
        if fix_assignment_spacing(str(file_path)):
            print(f"✓ {file_name}")
            fixed_count += 1
        else:
            print(f"  {file_name} (no changes)")

print(f"\n✅ Fixed {fixed_count} files")
