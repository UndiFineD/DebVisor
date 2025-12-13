#!/usr/bin/env python3
"""Comprehensive fixer for backup_intelligence.py"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# Step 1: Fix logger references (logger -> _logger)
# Match logger. references that aren't _logger.
content = re.sub(r'(?<!_)logger\.', '_logger.', content)

# Step 2: Fix remaining underscore variables not yet fixed
underscore_vars = [
    '_total_mb', '_backups', '_now', '_future_hour', '_future_day',
    '_hours_ahead', '_hour_rate', '_day_rate', '_window', '_score',
    '_check_time', '_sandbox_id', '_result', '_validator',
]

for var in underscore_vars:
    clean_var = var[1:]  # Remove underscore
    # Replace assignment: _var = -> var =
    content = re.sub(rf'{var}\s*=\s*', f'{clean_var} = ', content)

# Step 3: Fix function call parameter spacing (remove spaces around =)
# These patterns need NO spaces inside function calls: field(x=y), ChangeRateMetrics(x=y), etc.
# But they DO need spaces in other contexts like:  x: int = 5

# Find function calls with spaces around = and fix them
patterns_to_fix = [
    (r'field\(\s+(\w+)\s*=\s*', r'field(\1='),
    (r'ChangeRateMetrics\(\s+(\w+)\s*=\s*', r'ChangeRateMetrics(\1='),
    (r'BackupWindow\(\s+(\w+)\s*=\s*', r'BackupWindow(\1='),
    (r'RestoreTest\(\s+(\w+)\s*=\s*', r'RestoreTest(\1='),
    (r'SLAComplianceReport\(\s+(\w+)\s*=\s*', r'SLAComplianceReport(\1='),
    (r'DedupAnalytics\(\s+(\w+)\s*=\s*', r'DedupAnalytics(\1='),
]

for pattern, replacement in patterns_to_fix:
    content = re.sub(pattern, replacement, content)

# Step 4: Fix specific E225 errors (missing spaces around =)
# In assignments, we need spaces: x=5 -> x = 5
assignment_patterns = [
    (r'(\w+)=(\d+[.\d]*|["\']|True|False|None)', r'\1 = \2'),  # Variable assignments
]

# Step 5: Fix window_score naming issue
content = content.replace('windowscore', 'window_score')

# Step 6: Fix indentation issues with comments (E115/E116)
# These are typically "else:" or other blocks followed by comment instead of code
# We'll look for common patterns and add 'pass' where needed
lines = content.split('\n')
fixed_lines = []
for i, line in enumerate(lines):
    fixed_lines.append(line)
    # If this is an else/if/try/except/finally: followed by a comment, add pass
    if re.match(r'^\s*(else|except|finally):\s*$', line):
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('#'):
            # Next line is a comment, need to insert pass
            indent = len(line) - len(line.lstrip()) + 4
            fixed_lines.append(' ' * indent + 'pass')

content = '\n'.join(fixed_lines)

# Step 7: Fix remaining E225 errors - ensure spaces around = in assignments
# But NOT in function parameters or type hints
content = re.sub(r'(\w+)=([a-z_]\w*\.|\[|{|\()', r'\1 = \2', content)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Comprehensive fix completed")
