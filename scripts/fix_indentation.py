#!/usr/bin/env python3
"""Fix all indentation errors in backup_intelligence.py"""

# Read the entire file
with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

# Process to fix indentation issues
result = []
in_function = False
expected_indent = 0
paren_depth = 0

for i, line in enumerate(lines, 1):
    stripped = line.lstrip()
    current_indent = len(line) - len(stripped)

    # Track if we're in a function/method
    if stripped.startswith('def ') or stripped.startswith('async def '):
        in_function = True
        expected_indent = current_indent
        result.append(line)
        continue

    # Lines that start with statement keywords at wrong level
    assignment_keywords = [
        '_logger=', 'datetime=', 'hour_rate=', 'day_rate=', 'window=',
        'now=', 'sandbox_id=', 'started_at=', 'completed_at=',
        'start_time=', 'boot_time_seconds=', 'testid=', 'test=',
        'policy_id=', 'sla=', 'backups=', 'sorted_backups=',
        'backup_count=', 'restores=', 'recent_restores=',
        'successful=', 'failed=', 'avg_duration=', 'next_backup_due=',
        'all_tests=', 'check_time=', 'test_id=', 'data_integrity_percent=',
        'validator=', 'tests=', 'rpo_violations=', 'last_backup=',
        'issues=', '_in_window=', '_get_window=', 'hour=', 'weekday=',
        'recent_samples=', 'recent_avg=', 'total_mb=', 'dedup_ratio=',
        'monthly_logical=', 'monthly_physical=', 'total_logical=',
        'total_physical=', 'total_savings=', '_bi=', 'minutes_since_backup=',
        'minutes_until_breach=', 'rpo_deadline=', 'forty_days_ago=',
        'past_hour=', 'future_hour=', 'future_day=', 'score=', 'next_due=',
        'new_test_id=', 'new_test=', 'changed_mb=', 'interval_minutes=',
        'timestamp=', 'rate_per_hour=', 'm=', 'hour=', 'weekday=', 'alpha=',
        'start=', 'optimal_time=', 'hours_ahead=', '_=', 'estimated_duration=',
        'window=', 'schedule=', 'test=', 'report=', 'at_risk=', 'breached=',
        'dedup_stats=', 'recent_tests=', 'successful_tests=', '_restore_rate=',
        '_health_report=', 'health_report=', 'test_time=', 'backup_time=',
        '_logical=', '_physical=', 'vms=', 'for=', 'if=', 'predicted=',
        'cv=', 'sample_confidence=', 'variance_confidence=',
        'pattern_weight=', 'policy_id=', 'predicted_rate=', 'success='
    ]

    # Check if this line starts with an assignment that should be indented
    is_misindented_assignment = any(
        stripped.startswith(kw) for kw in assignment_keywords
    )

    # If we're in a function and this is at base level but looks like indented
    if (in_function and current_indent == 0 and is_misindented_assignment):
        # This should be indented 8 spaces (standard for function body)
        result.append('        ' + stripped)
    elif (in_function and current_indent == 0 and stripped and
          not any(stripped.startswith(x) for x in
                  ['def ', 'async def ', 'class ', '@', 'if __name__'])):
        # Check if this is a continuation that needs indentation
        if stripped and not stripped.startswith('#'):
            result.append('        ' + stripped)
        else:
            result.append(line)
    else:
        result.append(line)

# Write back
with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(result)

print("Indentation fixes applied")
