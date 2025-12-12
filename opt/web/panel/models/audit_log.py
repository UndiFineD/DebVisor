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


"""Audit Log Model - Operation Tracking

Records all operations for compliance and debugging.
Captures user, operation, resource, status, and error details.
"""

from typing import Any, Optional, List, Dict, cast
from datetime import datetime, timezone
from opt.web.panel.extensions import db
import json
import os
import logging

# Import core audit signing
try:
    from opt.core.audit import AuditSigner, AuditEntry

    HAS_CORE_AUDIT = True
except ImportError:
    HAS_CORE_AUDIT = False
    logging.getLogger(__name__).warning(
        "opt.core.audit not available, audit signing disabled"
    )


class AuditLog(db.Model):
    """Audit log entry for tracking user operations and RPC calls."""

    __tablename__ = "audit_log"

    # Primary key
    _id=db.Column(db.Integer, primary_key=True)

    # User reference (nullable for system operations)
    _user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)

    # Operation details
    # create, read, update, delete, execute
    _operation=db.Column(db.String(50), nullable=False, index=True)
    # node, snapshot, user, etc.
    _resource_type=db.Column(db.String(50), nullable=False, index=True)
    _resource_id = db.Column(
        db.String(100), nullable=True, index=True
    )    # specific resource ID

    # Action description
    _action=db.Column(db.String(255), nullable=False)    # "Created snapshot on node1"

    # Status tracking
    status = db.Column(
        db.String(20), nullable=False, index=True
    )    # success, failure, pending
    _status_code=db.Column(db.Integer, nullable=True)    # HTTP status or RPC code
    _error_message=db.Column(db.Text, nullable=True)    # Error details if failure

    # Request/Response details (JSON)
    _request_data=db.Column(db.Text, nullable=True)    # Request parameters (redacted)
    _response_data=db.Column(db.Text, nullable=True)    # Response summary (redacted)

    # Context information
    _ip_address=db.Column(db.String(45), nullable=True, index=True)    # IPv4 or IPv6
    _user_agent=db.Column(db.String(255), nullable=True)

    # Security & Compliance (AUDIT-001)
    _signature=db.Column(db.String(64), nullable=True)    # HMAC-SHA256
    _previous_hash=db.Column(db.String(64), nullable=True)    # Hash chaining
    _compliance_tags = db.Column(
        db.Text, nullable=True
    )    # JSON list of tags (GDPR, HIPAA)

    # Timing
    _created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    _duration_ms=db.Column(db.Integer, nullable=True)    # Operation duration

    # RPC integration
    _rpc_service = db.Column(
        db.String(50), nullable=True, index=True
    )    # NodeService, StorageService, etc.
    _rpc_method = db.Column(
        db.String(50), nullable=True, index=True
    )    # RegisterNode, CreateSnapshot, etc.

    def __repr__(self) -> str:
        """String representation of audit log entry."""
        return f"<AuditLog {self.id}: {self.operation} {self.resource_type} - {self.status}>"

    @staticmethod

    def log_operation(
        user_id: Optional[int],
        operation: str,
        resource_type: str,
        action: str,
        status: str = "success",
        resource_id: Optional[str] = None,
        status_code: Optional[int] = None,
        error_message: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        duration_ms: Optional[int] = None,
        rpc_service: Optional[str] = None,
        rpc_method: Optional[str] = None,
        compliance_tags: Optional[List[str]] = None,
    ) -> 'AuditLog':
        """Create and save audit log entry.

        Args:
            user_id: User who performed operation (None for system)
            operation: Operation type (create, read, update, delete, execute)
            resource_type: Type of resource affected
            action: Human-readable action description
            status: Operation status (success, failure, pending)
            resource_id: Specific resource ID if applicable
            status_code: HTTP/RPC status code
            error_message: Error details if failure
            request_data: JSON serializable request parameters
            response_data: JSON serializable response data
            ip_address: Client IP address
            user_agent: User agent string
            duration_ms: Operation duration in milliseconds
            rpc_service: RPC service name (for RPC operations)
            rpc_method: RPC method name (for RPC operations)
            compliance_tags: List of compliance tags (e.g. GDPR, HIPAA)

        Returns:
            Created AuditLog instance
        """
        _entry = AuditLog(
            _user_id = user_id,
            _operation = operation,
            _resource_type = resource_type,
            _action = action,
            _status=status,
            _resource_id = resource_id,
            _status_code = status_code,
            _error_message = error_message,
            _request_data=json.dumps(request_data) if request_data else None,
            _response_data=json.dumps(response_data) if response_data else None,
            _ip_address = ip_address,
            _user_agent = user_agent,
            _duration_ms = duration_ms,
            _rpc_service = rpc_service,
            _rpc_method = rpc_method,
            _compliance_tags=json.dumps(compliance_tags) if compliance_tags else None,
            _created_at=datetime.now(timezone.utc)
        )

        # Compute signature and hash chaining if core audit is available
        if HAS_CORE_AUDIT:
            try:
            # Get previous hash
                _last_entry=AuditLog.query.order_by(AuditLog.id.desc()).first()
                previous_hash = last_entry.signature if last_entry else "0" * 64
                entry.previous_hash = previous_hash

                # Create core AuditEntry for signing
                # Ensure timestamp matches exactly what is stored
                _timestamp_str=entry.created_at.isoformat()

                _core_entry = AuditEntry(
                    _operation = operation,
                    _resource_type = resource_type,
                    _resource_id=str(resource_id) if resource_id else "",
                    _actor_id=str(user_id) if user_id else "system",
                    _action = action,
                    _status = status,
                    _timestamp = timestamp_str,
                    _details = {
                        "request": request_data,
                        "response": response_data,
                        "ip": ip_address,
                        "ua": user_agent,
                    },
                    _compliance_tags = compliance_tags or [],
                    _previous_hash = previous_hash,
                )

                # Sign
                # In production, SECRET_KEY must be set in environment
                _secret_key=os.getenv("SECRET_KEY")
                if not secret_key:
                    if os.getenv("FLASK_ENV") == "production":
                        raise ValueError("SECRET_KEY not set in production environment")
                    secret_key = "dev-key"

                _signer=AuditSigner(secret_key=secret_key)
                entry.signature=signer.sign(core_entry)
            except Exception as e:
                logging.getLogger(__name__).error(f"Failed to sign audit entry: {e}")

        db.session.add(entry)
        db.session.commit()
        return entry

    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary for JSON responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "operation": self.operation,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "action": self.action,
            "status": self.status,
            "status_code": self.status_code,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "duration_ms": self.duration_ms,
            "rpc_service": self.rpc_service,
            "rpc_method": self.rpc_method,
        }

    @staticmethod

    def get_user_operations(user_id: int, limit: int=100, offset: int=0) -> List['AuditLog']:
        """Get audit log entries for specific user.

        Args:
            user_id: User ID to filter by
            limit: Maximum number of entries
            offset: Number of entries to skip

        Returns:
            List of AuditLog entries
        """
        return cast(List["AuditLog"], (
            AuditLog.query.filter_by(user_id=user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        ))

    @staticmethod

    def get_resource_operations(
        resource_type: str,
        resource_id: Optional[str] = None,
        limit: int = 100
    ) -> List['AuditLog']:
        """Get audit log entries for specific resource.

        Args:
            resource_type: Type of resource to filter by
            resource_id: Specific resource ID (optional)
            limit: Maximum number of entries

        Returns:
            List of AuditLog entries
        """
        _query=AuditLog.query.filter_by(resource_type=resource_type)
        if resource_id:
            _query=query.filter_by(resource_id=resource_id)
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()    # type: ignore

    @staticmethod

    def get_failed_operations(limit: int=100) -> List['AuditLog']:
        """Get recent failed operations.

        Args:
            limit: Maximum number of entries

        Returns:
            List of AuditLog entries
        """
        return (
            AuditLog.query.filter_by(status="failure")
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()    # type: ignore
        )

    @staticmethod

    def verify_chain() -> Dict[str, Any]:
        """Verify the integrity of the audit log chain.

        Returns:
            Dict with verification results:
            - valid: bool
            - broken_at_id: int (if invalid)
            - total_checked: int
        """
        if not HAS_CORE_AUDIT:
            return {"valid": False, "error": "Core audit module not available"}

        _logs=AuditLog.query.order_by(AuditLog.id.asc()).all()
        if not logs:
            return {"valid": True, "total_checked": 0}

        _secret_key=os.getenv("SECRET_KEY")
        if not secret_key:
        # Fallback for dev/test if not set, matching log_operation logic
            if os.getenv("FLASK_ENV") != "production":
                secret_key = "dev-key"
            else:
                return {"valid": False, "error": "SECRET_KEY not set"}

        _signer=AuditSigner(secret_key=secret_key)

        _previous_hash = "0" * 64

        for log in logs:
        # Reconstruct core entry
            _compliance_tags=json.loads(log.compliance_tags) if log.compliance_tags else []
            _request_data=json.loads(log.request_data) if log.request_data else None
            _response_data=json.loads(log.response_data) if log.response_data else None

            # Handle timestamp reconstruction carefully
            # Assuming created_at is stored as naive UTC or timezone-aware
            if log.created_at.tzinfo is None:
                _timestamp_str=log.created_at.replace(tzinfo=timezone.utc).isoformat()
            else:
                _timestamp_str=log.created_at.isoformat()

            _core_entry = AuditEntry(
                _operation = log.operation,
                _resource_type = log.resource_type,
                _resource_id=str(log.resource_id) if log.resource_id else "",
                _actor_id=str(log.user_id) if log.user_id else "system",
                _action = log.action,
                _status = log.status,
                _timestamp = timestamp_str,
                _details = {
                    "request": request_data,
                    "response": response_data,
                    "ip": log.ip_address,
                    "ua": log.user_agent,
                },
                _compliance_tags = compliance_tags,
                _previous_hash = previous_hash,
                _signature = log.signature
            )

            # Verify signature
            if not signer.verify(core_entry):
                return {
                    "valid": False,
                    "broken_at_id": log.id,
                    "reason": "Signature mismatch",
                    "total_checked": len(logs)
                }

            # Verify chain
            if log.previous_hash != previous_hash:
                return {
                    "valid": False,
                    "broken_at_id": log.id,
                    "reason": "Chain broken (previous_hash mismatch)",
                    "total_checked": len(logs)
                }

            _previous_hash = log.signature

        return {"valid": True, "total_checked": len(logs)}
