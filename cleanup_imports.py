#!/usr/bin/env python3
"""Remove remaining F401 unused imports."""

files_to_fix = [
    ("opt/migrations/env.py", "from myapp import mymodel", ""),
    (
        "opt/services/anomaly/api.py",
        "from typing import List, Dict, Optional, Any",
        "from typing import Dict, Optional, Any",
    ),
    (
        "opt/services/anomaly/cli.py",
        "from opt.core.cli_utils import print_error, print_success",
        "from opt.core.cli_utils import print_error",
    ),
    ("opt/services/cache.py", "from redis import Redis", ""),
    (
        "opt/services/compliance/api.py",
        "from flask import request, Blueprint, jsonify",
        "from flask import Blueprint, jsonify",
    ),
    (
        "opt/services/compliance/api.py",
        "from typing import Union, Dict, List, Optional, Any",
        "from typing import Dict, List, Optional, Any",
    ),
    (
        "opt/services/compliance/gdpr.py",
        "from typing import List, Dict, Optional, Any, Tuple",
        "from typing import Dict, Optional, Any, Tuple",
    ),
    (
        "opt/services/compliance/reporting.py",
        "from typing import Optional, Dict, List, Any",
        "from typing import Dict, List, Any",
    ),
    (
        "opt/services/compliance/reporting.py",
        "from opt.services.reporting_scheduler import ScheduledReport, ReportFrequency",
        "",
    ),
    (
        "opt/services/compliance/reporting.py",
        "from opt.web.panel.extensions import db, create_app",
        "from opt.web.panel.extensions import create_app",
    ),
    ("opt/services/connection_pool.py", "from redis import Redis", ""),
    (
        "opt/services/cost_optimization/cli.py",
        "from typing import Any, Dict, List, Optional, Tuple",
        "from typing import Dict, List, Optional, Tuple",
    ),
    (
        "opt/services/diagnostics.py",
        "from datetime import timedelta, datetime, timezone",
        "from datetime import datetime, timezone",
    ),
    (
        "opt/services/dns/hosting.py",
        "from dataclasses import asdict, dataclass, field",
        "from dataclasses import dataclass, field",
    ),
    (
        "opt/services/dns/hosting.py",
        "from typing import Any, Union, Dict, List, Optional",
        "from typing import Dict, List, Optional",
    ),
]

for file_path, old_line, new_line in files_to_fix:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_line in content:
            new_content = content.replace(old_line, new_line, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Fixed {file_path}")
        else:
            print(f"- Not found in {file_path}: {old_line[:60]}")
    except Exception as e:
        print(f"✗ Error in {file_path}: {e}")

print("\nDone!")
