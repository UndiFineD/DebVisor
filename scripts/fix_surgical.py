#!/usr/bin/env python3
"""Surgical fixes for underscore variables one at a time"""

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

# Go through line by line and fix specific issues
for i, line in enumerate(lines):
    # Fix _timestamp = -> timestamp =
    if '_timestamp=' in line:
        lines[i] = line.replace('_timestamp=', 'timestamp = ')
    # Fix m= -> m =
    if line.strip().startswith('m=') and 'self.metrics' in line:
        lines[i] = line.replace('m=', 'm = ')
    # Fix _rate_per_hour= -> rate_per_hour =
    if '_rate_per_hour=' in line:
        lines[i] = line.replace('_rate_per_hour=', 'rate_per_hour = ')
    # Fix hour= -> hour =
    if line.strip().startswith('hour=') and 'timestamp.hour' in line:
        lines[i] = line.replace('hour=', 'hour = ')
    # Fix _weekday= -> weekday =
    if '_weekday=' in line:
        lines[i] = line.replace('_weekday=', 'weekday = ')
    # Fix alpha= -> alpha =
    if line.strip().startswith('alpha='):
        lines[i] = line.replace('alpha=', 'alpha = ')
    # Fix all other spacing issues around = for simple assignments
    if '=' in line and not any(x in line for x in ['==', '!=', '<=', '>=', '  # type', 'field(', 'default_factory']):
        # Look for patterns like word=word
        import re
        lines[i] = re.sub(r'(\w+)=(\w+)', r'\1 = \2', lines[i])

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(lines)

print("Surgical fixes applied")
