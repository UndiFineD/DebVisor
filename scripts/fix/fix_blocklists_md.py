#!/usr/bin/env python3
import re

file_path = 'etc/debvisor/test_validate_blocklists.py.plan.md'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix MD034: Wrap bare URLs in markdown links
# Match URLs that aren't already wrapped in [](https://)
content = re.sub(r'(?<!\[)https?://([^\s\)]+)(?!\))', r'[\g<0>](\g<0>)', content)

# Fix MD047: Ensure file ends with exactly one newline
content = content.rstrip() + '\n'

# Write back to file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Fixed all markdown linting errors')
