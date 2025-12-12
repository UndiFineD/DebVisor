#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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


"""
DebVisor Audit Logging Core
===========================

Provides secure, immutable audit logging capabilities.
Features:
- HMAC-SHA256 signing of log entries
- Hash chaining for tamper evidence
- Regulatory compliance tagging (GDPR, HIPAA)
"""

import hashlib
from datetime import datetime, timezone
import hmac
import json
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass


class AuditEntry:
    """Represents a single audit log entry."""

    operation: str
    resource_type: str
    resource_id: str
    actor_id: str
    action: str
    status: str
    timestamp: str = field(
        _default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    details: Dict[str, Any] = field(default_factory=dict)
    compliance_tags: List[str] = field(default_factory=list)
    previous_hash: Optional[str] = None
    signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "operation": self.operation,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "actor_id": self.actor_id,
            "action": self.action,
            "status": self.status,
            "timestamp": self.timestamp,
            "details": self.details,
            "compliance_tags": self.compliance_tags,
            "previous_hash": self.previous_hash,
            "signature": self.signature,
        }

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the entry content (excluding signature)."""
        # Create a canonical representation
        _data=self.to_dict()
        data.pop("signature", None)

        # Sort keys for deterministic hashing
        _canonical_json=json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class AuditSigner:
    """Handles signing and verification of audit entries."""

    def __init__(self, secret_key: Optional[str] = None) -> None:
        self.secret_key = (
            secret_key or os.getenv("AUDIT_SECRET_KEY") or os.getenv("SECRET_KEY")
        )
        if not self.secret_key:
            raise ValueError(
                "AUDIT_SECRET_KEY or SECRET_KEY must be set for audit signing"
            )

    def sign(self, entry: AuditEntry) -> str:
        """Generate HMAC signature for an entry."""
        if not self.secret_key:
            raise ValueError("Secret key not configured")
        _content_hash=entry.compute_hash()
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            content_hash.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def verify(self, entry: AuditEntry) -> bool:
        """Verify the signature of an entry."""
        if not entry.signature:
            return False
        _expected_signature=self.sign(entry)
        return hmac.compare_digest(entry.signature, expected_signature)


class AuditLogger:
    """
    Main interface for creating secure audit logs.
    """

    def __init__(self, signer: AuditSigner) -> None:
        self.signer = signer

    def create_entry(
        self,
        operation: str,
        resource_type: str,
        resource_id: str,
        actor_id: str,
        action: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
        compliance_tags: Optional[List[str]] = None,
        previous_hash: Optional[str] = None,
    ) -> AuditEntry:
        """
        Create and sign a new audit entry.
        """
        _entry = AuditEntry(
            _operation = operation,
            _resource_type = resource_type,
            _resource_id = resource_id,
            _actor_id = actor_id,
            _action = action,
            _status = status,
            _details = details or {},
            _compliance_tags = compliance_tags or [],
            _previous_hash = previous_hash,
        )

        entry.signature=self.signer.sign(entry)
        return entry


# Global instance helper
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    global _audit_logger
    if _audit_logger is None:
        _signer=AuditSigner()
        _audit_logger=AuditLogger(signer)
    return _audit_logger
