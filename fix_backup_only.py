#!/usr/bin/env python3
"""Fix backup_intelligence.py issues systematically"""
import re
from pathlib import Path

path = Path('opt/services/backup/backup_intelligence.py')
content = path.read_text(encoding='utf-8')
lines = content.split('\n')

# Step 1: Fix variable names with underscore prefixes and undefined references
fixes_needed = {}

# Track which underscore variables we have and which undefined vars reference them
for i, line in enumerate(lines):
    # Look for _variable assignments
    if '_window =' in line or '_score =' in line or '_check_date =' in line:
        # These variables should not have underscores
        # Later code references them without underscores (causing F821)
        pass
    
    # Look for undefined variable references
    if 'window' in line and '_window =' not in line and 'window=' not in line:
        if 'undefined' not in line.lower() or 'comment' not in line.lower():
            # This is likely referencing window that was assigned as _window
            pass

# Let's be more direct: replace the problematic assignments
replacements = [
    ('_window=', '_window = '),
    ('_score=', '_score = '),
    ('_check_date=', '_check_date = '),
    ('_logger=', '_logger = '),
    ('_datetime=', '_datetime = '),
    ('_hour_rate=', '_hour_rate = '),
    ('_day_rate=', '_day_rate = '),
    ('_now=', '_now = '),
    ('_testid=', '_testid = '),
    ('_policy_id=', '_policy_id = '),
    # Fix parameter spacing
    ('=', ' = '),  # This is too broad, so let's be specific
]

# Process each line carefully
for i, line in enumerate(lines):
    original = line
    
    # Only fix E225 (missing spaces) in assignments, not default parameters
    if 'def ' not in line and 'lambda' not in line and '==' not in line:
        # Fix _var= patterns
        line = re.sub(r'_([a-zA-Z_]\w*)\s*=([^=\s])', r'_\1 = \2', line)
        # Fix var= patterns (but not in keyword arguments)
        if '(' not in line or not any(c in line.split('(')[-1] for c in ['var=', 'func=']):
            pass
    
    lines[i] = line

# Now fix the F821 undefined variables
# The issue is that variables like window are referenced but defined as _window
# This likely means the underscore should be removed
content = '\n'.join(lines)

# Replace undefined references by removing underscore from assignment
# But we need to check what's actually undefined
undefined_vars_map = {
    '_window': 'window',
    '_score': 'score',  
    '_check_date': 'check_date',
    '_logger': 'logger',
}

for underscore_var, normal_var in undefined_vars_map.items():
    # Only replace if normal_var is referenced without underscore
    if normal_var in content and underscore_var in content:
        # This is complex - let's just remove underscores where they cause issues
        # Replace the assignment
        content = re.sub(rf'^(\s*){re.escape(underscore_var)}\s*=', rf'\1{normal_var} =', content, flags=re.MULTILINE)

lines = content.split('\n')
path.write_text('\n'.join(lines), encoding='utf-8')
print(f"✓ Fixed {path}")
