#!/usr/bin/env python3
"""Fix remaining issues in api_key_manager.py"""

import re

with open('opt/services/api_key_manager.py', 'r') as f:
    content = f.read()

# Fix keyword argument spacing in function/method calls
# Pattern: func(key = value) should become func(key=value)
# But: func(param: type = default) in def should stay as is

# First, fix assignments with equals but no spaces (E225)
# Only in non-function-definition context
lines = content.split('\n')
result_lines = []

for line in lines:
    # Skip def lines - those need spaces around =
    if ' def ' not in line and '->' not in line:
        # Fix assignments: variable=value to variable = value (for regular assignments, not kwargs)
        # But this is tricky with regex...
        
        # For now, fix specific patterns we know about
        line = line.replace('key_obj=', 'key_obj = ')
        line = line.replace('log_entry=', 'log_entry = ')
        
        # Fix keyword argument spacing in function calls (remove spaces)
        # Pattern: (\w+) = (.*?)(,|\)) should become \1=\2\3
        # But only if not in a function definition
        if '(' in line and ')' in line and 'def ' not in line:
            # Try to fix keyword args
            line = re.sub(r'(\w+) = ([\w\'"_.-]+)(,|\))', r'\1=\2\3', line)
        
        # Fix underscore prefixes on keyword arguments
        line = line.replace('_created_at=', 'created_at=')
        line = line.replace('_expires_at=', 'expires_at=')
        line = line.replace('_last_used_at=', 'last_used_at=')
        line = line.replace('_use_count=', 'use_count=')
        line = line.replace('_status=', 'status=')
        line = line.replace('_description=', 'description=')
        line = line.replace('_principal_id=', 'principal_id=')
        line = line.replace('_key_id=', 'key_id=')
        line = line.replace('_key_hash=', 'key_hash=')
        line = line.replace('_event=', 'event=')
        line = line.replace('_details=', 'details=')
    
    result_lines.append(line)

# Rejoin and fix __main__ pattern
content = '\n'.join(result_lines)
content = content.replace('if __name__ = "__main__":', 'if __name__ == "__main__":')

with open('opt/services/api_key_manager.py', 'w') as f:
    f.write(content)

print("Remaining fixes applied")
