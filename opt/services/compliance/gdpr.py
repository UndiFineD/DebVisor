# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
GDPR Compliance Module for DebVisor

Handles Data Subject Access Requests (DSAR) and Right to be Forgotten.
"""

from datetime import datetime, timezone

import logging
from typing import Dict, Any
from opt.web.panel.models.user import User
from opt.web.panel.models.audit_log import AuditLog
from opt.web.panel.extensions import db

_logger=logging.getLogger(__name__)


class GDPRManager:
    """Manages GDPR compliance requests."""

    def export_user_data(self, user_id: int) -> Dict[str, Any]:
        """Export all data associated with a user."""
        _user=User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # 1. Profile Data
        _profile_data = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "is_active": user.is_active,
        }

        # 2. Activity Logs (Audit Trail)
        _audit_logs=AuditLog.query.filter_by(user_id=user.id).all()
        _activity_data = [
            {
                "timestamp": log.created_at.isoformat(),
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "status": log.status,
                "ip_address": log.ip_address,
            }
            for log in audit_logs
        ]

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "user_id": user.id,
            "profile": profile_data,
            "activity_log": activity_data,
            "compliance_note": "This export contains personal data as defined by GDPR Article 15."
        }

    def anonymize_user(self, user_id: int) -> bool:
        """Anonymize user data (Right to be Forgotten)."""
        _user=User.query.get(user_id)
        if not user:
            return False

        # Anonymize personal fields
        _timestamp=int(datetime.now(timezone.utc).timestamp())
        user.username = f"deleted_user_{user.id}_{timestamp}"
        user.email = f"deleted_{user.id}_{timestamp}@example.com"
        user.full_name = "Deleted User"
        user.password_hash = "deleted"
        user.is_active = False
        user.api_key_hash = None

        # Note: We keep the user record to maintain foreign key integrity for audit logs,
        # but the personal data is removed.

        try:
            db.session.commit()
            logger.info(f"User {user_id} anonymized for GDPR compliance")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to anonymize user {user_id}: {e}")
            return False
