#!/usr/bin/env python3
"""Fix api_key_manager.py - targeted surgical fixes"""

with open('opt/services/api_key_manager.py', 'r') as f:
    lines = f.readlines()

# Build replacement map
replacements = [
    # Line 33: Remove unused os import - already done
    
    # Line 40: Logger spacing
    (39, '_logger = logging.getLogger(__name__)\n'),
    
    # Line 46-49: Enum spacing
    (45, '    ACTIVE = "active"\n'),
    (46, '    EXPIRING = "expiring"  # Within overlap period\n'),
    (47, '    EXPIRED = "expired"\n'),
    (48, '    REVOKED = "revoked"\n'),
    
    # Line 109: Fix storagepath parameter
    (108, '    def __init__(self, config: KeyRotationConfig, storage_path: str) -> None:\n'),
    
    # Line 110: Fix config assignment
    (109, '        self.config = config\n'),
    
    # Line 111: Fix storage_path assignment
    (110, '        self.storage_path = Path(storage_path)\n'),
    
    # Line 112: Fix mkdir call
    (111, '        self.storage_path.mkdir(parents=True, exist_ok=True)\n'),
    
    # Line 113: Fix keys_file attribute
    (112, '        self.keys_file = self.storage_path / "api_keys.json"\n'),
    
    # Line 114: Fix audit_log attribute
    (113, '        self.audit_log = self.storage_path / "api_key_audit.log"\n'),
    
    # Line 118: Add logger definition
    (117, '        logger = _logger\n'),
    
    # Line 130: Fix keys dictionary assignment
    (129, '                self.keys = {\n'),
    
    # Line 145-147: Fix audit log event variable naming
    (145, '        log_entry = {\n'),
    (149, '        with open(self.audit_log, "a") as f:\n'),
    (150, '            f.write(json.dumps(log_entry) + "\\n")\n'),
    
    # Line 155: Fix parameter spacing in function signature (at line where keyid appears)
    # This will be: "principal_id"
]

# Apply replacements
for line_num, new_content in replacements:
    if line_num < len(lines):
        lines[line_num] = new_content

with open('opt/services/api_key_manager.py', 'w') as f:
    f.writelines(lines)

print("API Key Manager surgical fixes applied")
