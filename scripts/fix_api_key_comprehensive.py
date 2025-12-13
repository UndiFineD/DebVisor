#!/usr/bin/env python3
"""Comprehensive fix for api_key_manager.py with all known issues"""

with open('opt/services/api_key_manager.py', 'r') as f:
    lines = f.readlines()

result = []
for i, line in enumerate(lines):
    # Remove unused os import
    if 'import os' in line and i < 50:
        continue
    
    # Fix logger assignment spacing
    line = line.replace('_logger=logging', '_logger = logging')
    
    # Fix Enum value assignments
    line = line.replace('ACTIVE="active"', 'ACTIVE = "active"')
    line = line.replace('EXPIRING="expiring"', 'EXPIRING = "expiring"')
    line = line.replace('EXPIRED="expired"', 'EXPIRED = "expired"')
    line = line.replace('REVOKED="revoked"', 'REVOKED = "revoked"')
    
    # Fix dataclass field assignments
    line = line.replace('key_hash: str    #', 'key_hash: str  #')
    line = line.replace('rotation_id: Optional[str] = None    #', 
                        'rotation_id: Optional[str] = None  #')
    
    # Fix KeyRotationConfig defaults
    line = line.replace('expiration_days: int=90', 'expiration_days: int = 90')
    line = line.replace('overlap_days: int=7', 'overlap_days: int = 7')
    line = line.replace('warning_days: int=14', 'warning_days: int = 14')
    line = line.replace('auto_rotate: bool=True', 'auto_rotate: bool = True')
    line = line.replace('max_active_keys_per_principal: int=3', 
                        'max_active_keys_per_principal: int = 3')
    
    # Fix __init__ parameter and body
    line = line.replace('storagepath: str', 'storage_path: str')
    line = line.replace('self.config=config', 'self.config = config')
    line = line.replace('self.storage_path=Path', 'self.storage_path = Path')
    line = line.replace('self.keys_file=self.storage_path', 'self.keys_file = self.storage_path')
    line = line.replace('self.audit_log=self.storage_path', 'self.audit_log = self.storage_path')
    
    # Fix logger references to use _logger
    if 'logger.info' in line or 'logger.warning' in line or 'logger.error' in line:
        # Replace logger with _logger but avoid __logger
        line = line.replace('logger.', '_logger.')
    
    # Fix underscore-prefixed variable assignments to remove underscores
    line = line.replace('_data=asdict(self)', 'data = asdict(self)')
    line = line.replace('_data=json.load(f)', 'data = json.load(f)')
    line = line.replace('_data={key_id:', 'data = {key_id:')
    line = line.replace('_api_key=', 'api_key = ')
    line = line.replace('_key_hash=', 'key_hash = ')
    line = line.replace('_key_id=', 'key_id = ')
    line = line.replace('_now=', 'now = ')
    line = line.replace('_expires_at=', 'expires_at = ')
    line = line.replace('_key_obj=', 'key_obj = ')
    line = line.replace('_event=', 'event = ')
    line = line.replace('_principal_id=', 'principal_id = ')
    line = line.replace('_details=', 'details = ')
    line = line.replace('_new_key_obj=', 'new_key_obj = ')
    line = line.replace('_old_key=', 'old_key = ')
    line = line.replace('_rotation_id=', 'rotation_id = ')
    line = line.replace('_last_used_at=', 'last_used_at = ')
    line = line.replace('_use_count=', 'use_count = ')
    line = line.replace('_status=', 'status = ')
    line = line.replace('_description=', 'description = ')
    
    # Fix parameter equals spacing in function signatures (add spaces)
    line = line.replace('description: str="', 'description: str = "')
    line = line.replace('skip_audit: bool=', 'skip_audit: bool = ')
    
    # Fix parameter equals in function calls (remove spaces)
    # Only in function call context (after function name with parenthesis)
    # Be careful not to affect function definitions
    if '(' in line and 'def ' not in line:
        # This is likely a function call, remove spaces around = in kwargs
        import re
        line = re.sub(r'(\w+)\s+=\s+', r'\1=', line)
    
    # Remove type: ignore comments that are no longer needed
    line = line.replace('  # type: ignore[name-defined]', '')
    line = line.replace('  # type: ignore[call-arg]', '')
    
    result.append(line)

with open('opt/services/api_key_manager.py', 'w') as f:
    f.writelines(result)

print("Comprehensive fixes applied to api_key_manager.py")
