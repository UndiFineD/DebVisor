#!/usr/bin/env python3
"""Comprehensive final fix for all remaining issues"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# List of replacements to make - careful about order and context
fixes = [
    # Fix 1: Function parameter typos
    ('def predict_changes(self, vmid: str, hoursahead: int)', 
     'def predict_changes(self, vm_id: str, hours_ahead: int)'),
    
    # Fix 2: sortedbackups -> sorted_backups
    ('sortedbackups = sorted(backups)', 'sorted_backups = sorted(backups)'),
    ('for i in range(1, len(sorted_backups))', 'for i in range(1, len(sorted_backups))'),
    
    # Fix 3: _avg_duration -> avg_duration (parameter name fix)
    ('_avg_duration=0.0', 'avg_duration = 0.0'),
    
    # Fix 4: next_due -> next_backup_due in one place
    ('next_due=None', 'next_backup_due = None'),
    ('if last_backup:', 'if last_backup:'),  # Context marker
    ('next_due = last_backup + timedelta(minutes = sla.rpo_minutes)',
     'next_backup_due = last_backup + timedelta(minutes=sla.rpo_minutes)'),
    
    # Fix 5: _send_alert vmid -> vm_id
    ('def _send_alert(self, vmid: str, message: str, severity: str) -> None:',
     'def _send_alert(self, vm_id: str, message: str, severity: str) -> None:'),
    
    # Fix 6: Fix parameter spacing in function calls - remove spaces around =
    ('policy_id = policy_id,  # type: ignore[name-defined]',
     'policy_id=policy_id,  # type: ignore[name-defined]'),
    ('status = SLAStatus.UNKNOWN,',
     'status=SLAStatus.UNKNOWN,'),
    ('_issues = ["Policy not found"],',
     '_issues=["Policy not found"],'),
    
    # Fix 7: Other parameter spacing fixes
    ('status = SLAStatus.COMPLIANT', 'status = SLAStatus.COMPLIANT'),  # Keep assignment
    ('status=SLAStatus.BREACHED', 'status = SLAStatus.BREACHED'),  # Change assignment
    ('minutes_until_breach=None', 'minutes_until_breach = None'),  # Change assignment
    ('status = SLAStatus.BREACHED,', 'status = SLAStatus.BREACHED,'),  # Keep in return
    
    # Fix 8: last_backup assignment spacing
    ('last_backup=backups[-1] if backups else None',
     'last_backup = backups[-1] if backups else None'),
    
    # Fix 9: issues and rpo_violations and status assignments
    ('issues = []', 'issues = []'),  # Keep
    ('rpo_violations=0', 'rpo_violations = 0'),  # Fix
    
    # Fix 10: DedupAnalytics calls - remove parameter name spaces
    ('dedup_ratio = dedup_ratio,',
     'dedup_ratio=dedup_ratio,'),
    
    # Fix 11: monthly_logical and monthly_physical spacing
    ('monthly_logical=logical_bytes * 4',
     'monthly_logical = logical_bytes * 4'),
    ('monthly_physical=physical_bytes * 4',
     'monthly_physical = physical_bytes * 4'),
    
    # Fix 12: total_savings
    ('total_savings=sum(', 'total_savings = sum('),
]

# Apply all fixes in order
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)

# Fix comment indentation issues (E115/E116) - add pass before comments
lines = content.split('\n')
fixed_lines = []
for i, line in enumerate(lines):
    fixed_lines.append(line)
    # Check for else:/except:/finally: followed by comment
    if re.match(r'^\s*(else|except|finally|try):\s*$', line):
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            next_stripped = next_line.strip()
            if next_stripped.startswith('#'):
                indent = len(line) - len(line.lstrip())
                fixed_lines.append(' ' * (indent + 4) + 'pass')

content = '\n'.join(fixed_lines)

# Fix remaining E225 issues with specific patterns
patterns_to_fix = [
    (r'(\w+)=(\w+)',  # variable=variable (no spaces)
     lambda m: f'{m.group(1)} = {m.group(2)}' if '=' in m.group(0) and ' ' not in m.group(0) else m.group(0)),
]

# Be more careful with this - only fix in specific contexts
# Look for assignment operators not followed/preceded by spaces
replacements = [
    ('dedup_ratio = dedup_ratio,  # type: ignore[name-defined]', 'dedup_ratio=dedup_ratio,'),
    ('policy_id = policy_id,  # type: ignore[name-defined]', 'policy_id=policy_id,'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Final comprehensive fixes completed")
