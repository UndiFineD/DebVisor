#!/usr/bin/env python3
"""Fix backup_intelligence.py comprehensively"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

result = []
i = 0

while i < len(lines):
    line = lines[i]

    # Find function definitions with parameter mismatches
    if 'def __init__' in line or 'def ' in line:
        # Look ahead for assignments using wrong parameter names
        j = i + 1
        func_lines = [line]

        # Collect function definition lines until we find the closing paren
        while j < len(lines) and not ('):' in lines[j] or ') ->' in lines[j]):
            func_lines.append(lines[j])
            j += 1

        if j < len(lines):
            func_lines.append(lines[j])

        # Now look for assignment patterns in the function body
        if j + 1 < len(lines):
            # Check the next few lines for assignments
            for k in range(j + 1, min(j + 10, len(lines))):
                body_line = lines[k]

                # Fix specific parameter naming issues
                body_line = body_line.replace('self.max_samples=max_samples', 'self.max_samples = max_samples')
                body_line = body_line.replace('self.prediction_horizon_hours=prediction_horizon_hours',
                                              'self.prediction_horizon_hours = prediction_horizon_hours')

                # Fix operators missing spaces
                if '=' in body_line and 'def' not in body_line and '->' not in body_line:
                    # This is an assignment, add spaces around =
                    body_line = re.sub(r'(\w+)=([^=])', r'\1 = \2', body_line)

                lines[k] = body_line

        # Add the function def lines as-is for now
        for func_line in func_lines:
            result.append(func_line)

        i = j + 1
        continue

    # General fixes for remaining lines

    # Fix parameter naming mismatches in def lines (add underscores to match assignments)
    if 'def ' in line and '(' in line and ')' in line:
        # Fix common parameter naming issues
        line = line.replace('maxsamples: int', 'max_samples: int')
        line = line.replace('predictionhorizon_hours: int', 'prediction_horizon_hours: int')
        line = line.replace('maxconcurrenttests: int', 'max_concurrent_tests: int')
        line = line.replace('testtimeout: int', 'test_timeout: int')
        line = line.replace('warningthreshold: float', 'warning_threshold: float')
        line = line.replace('retentiondaysint', 'retention_days: int')

    # Fix missing spaces around = in regular assignments (non-kwargs)
    if 'self.' in line and '=' in line and 'def' not in line:
        line = re.sub(r'(\w+)=([^=])', r'\1 = \2', line)

    # Fix E225 in function definitions with defaults
    if 'def ' in line:
        line = re.sub(r':\s*(\w+)=', r': \1 = ', line)

    result.append(line)
    i += 1

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(result)

print("Comprehensive fixes applied to backup_intelligence.py")
