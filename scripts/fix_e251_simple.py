#!/usr/bin/env python3
"""Simple global E251 fix"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# Simple approach: globally replace word = word with word=word
# But only within function/method calls (between parentheses)
# We'll do multiple passes to handle nested calls

for _ in range(10):  # Multiple passes for nested calls
    old_len = len(content)
    # Match: word = word pattern and replace with word=word
    content = re.sub(r'(\w+)\s+=\s+(\w+)', r'\1=\2', content)

    if len(content) == old_len:
        break  # No more changes

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Simple global E251 fixes applied")
