#!/usr/bin/env python3
"""Fix spacing in Enum assignments"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# Fix Enum assignments - they need spaces around =
enum_fixes = [
    'CRITICAL=1', 'CRITICAL = 1',
    'HIGH=2', 'HIGH = 2',
    'MEDIUM=3', 'MEDIUM = 3',
    'LOW=4', 'LOW = 4',
    'ARCHIVE=5', 'ARCHIVE = 5',
    'COMPLIANT="compliant"', 'COMPLIANT = "compliant"',
    'AT_RISK="at_risk"', 'AT_RISK = "at_risk"',
    'BREACHED="breached"', 'BREACHED = "breached"',
    'UNKNOWN="unknown"', 'UNKNOWN = "unknown"',
    'PENDING="pending"', 'PENDING = "pending"',
    'PROVISIONING="provisioning"', 'PROVISIONING = "provisioning"',
    'RESTORING="restoring"', 'RESTORING = "restoring"',
    'VALIDATING="validating"', 'VALIDATING = "validating"',
    'SUCCESS="success"', 'SUCCESS = "success"',
    'FAILED="failed"', 'FAILED = "failed"',
    'CANCELLED="cancelled"', 'CANCELLED = "cancelled"',
    'BOOT="boot"', 'BOOT = "boot"',
    'NETWORK="network"', 'NETWORK = "network"',
    'SERVICE="service"', 'SERVICE = "service"',
    'DATA="data"', 'DATA = "data"',
    'APPLICATION="application"', 'APPLICATION = "application"',
]

for i in range(0, len(enum_fixes), 2):
    content = content.replace(enum_fixes[i], enum_fixes[i + 1])

# Also fix the field() calls that have spacing issues
# These should have NO spaces: field(default_factory=dict)
# Fix "field(x = value)" to "field(x=value)"
content = re.sub(r'field\(\s*_?(\w+)\s*=\s*', r'field(\1=', content)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Enum spacing fixes applied")
