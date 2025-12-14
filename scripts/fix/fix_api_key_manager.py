#!/usr/bin/env python3
"""Fix api_key_manager.py flake8 errors"""

import re

with open('opt/services/api_key_manager.py', 'r') as f:
    content = f.read()

# Fix 1: Remove unused 'os' import (line 33)
content = re.sub(r'import os\n', '', content, count=1)

# Fix 2: Fix logger assignment spacing (line 40)
content = content.replace('_logger=logging.getLogger(__name__)', 
                          '_logger = logging.getLogger(__name__)')

# Fix 3: Fix Enum value spacing (lines 46-49)
replacements = [
    ('ACTIVE="active"', 'ACTIVE = "active"'),
    ('EXPIRING="expiring"', 'EXPIRING = "expiring"'),
    ('EXPIRED="expired"', 'EXPIRED = "expired"'),
    ('REVOKED="revoked"', 'REVOKED = "revoked"'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Fix 4: Fix dataclass field spacing (lines 49-54)
content = content.replace('key_hash: str    # SHA-256 hash', 
                          'key_hash: str  # SHA-256 hash')
content = content.replace('rotation_id: Optional[str] = None    # Links keys', 
                          'rotation_id: Optional[str] = None  # Links keys')

# Fix 5: Fix _data pattern - remove underscore prefix and fix spacing
content = re.sub(r'_data=asdict\(self\)', 'data = asdict(self)', content)
content = re.sub(r'_data=datetime\.now\(', 'now = datetime.now(', content)
content = re.sub(r'_data=time\.time\(\)', 'timestamp = time.time()', content)
content = re.sub(r'_data=\[', 'data = [', content)

# Fix 6: Fix underscore variable assignments to remove underscore and add spacing
content = re.sub(r'_(\w+)=([^=])', r'\1 = \2', content)

# Fix 7: Fix KeyRotationConfig parameter spacing
content = content.replace('expiration_days: int=90', 
                          'expiration_days: int = 90')
content = content.replace('overlap_days: int=7', 
                          'overlap_days: int = 7')
content = content.replace('warning_days: int=14', 
                          'warning_days: int = 14')
content = content.replace('auto_rotate: bool=True', 
                          'auto_rotate: bool = True')
content = content.replace('max_active_keys_per_principal: int=3', 
                          'max_active_keys_per_principal: int = 3')

# Fix 8: Fix __main__ pattern
content = content.replace('if __name__=__main__:', 
                          'if __name__ == "__main__":')

# Fix 9: Fix parameter equals spacing in function signatures
# Pattern: description: str="", custom_expiration_days: Optional[int] = None, skip_audit: bool=False
content = re.sub(r'description: str=""', 'description: str = ""', content)
content = re.sub(r'skip_audit: bool=', 'skip_audit: bool = ', content)
content = re.sub(r'days: int=', 'days: int = ', content)
content = re.sub(r'skip_audit: bool=', 'skip_audit: bool = ', content)

# Fix 10: Comment indentation issue at line 244
content = content.replace(
    '        return False\n        # Key hash not found\n        return False',
    '        return False'
)

with open('opt/services/api_key_manager.py', 'w') as f:
    f.write(content)

print("API Key Manager fixes applied")
