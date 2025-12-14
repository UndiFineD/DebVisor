#!/usr/bin/env python3
"""Comprehensive underscore variable removal"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# Replace all instances of _variablename= with variablename =
# But only when the underscore version is not defined elsewhere
content = re.sub(r'(\s)_([a-zA-Z_]\w*) = ', r'\1\2 = ', content)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Comprehensive underscore removal applied")
