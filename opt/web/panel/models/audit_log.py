"""Audit Log Model - Operation Tracking

Records all operations for compliance and debugging.
Captures user, operation, resource, status, and error details.
"""

from datetime import datetime, timezone
from typing import Any, Optional, List, Dict, Union, cast
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
    id = db.Column(db.Integer, primary_key=True)

    # User reference (nullable for system operations)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)

    # Operation details
    # create, read, update, delete, execute
    operation = db.Column(db.String(50), nullable=False, index=True)
    # node, snapshot, user, etc.
    resource_type = db.Column(db.String(50), nullable=False, index=True)
    resource_id = db.Column(
        db.String(100), nullable=True, index=True
    )  # specific resource ID

    # Action description
    action = db.Column(db.String(255), nullable=False)  # "Created snapshot on node1"

    # Status tracking
    status = db.Column(
        db.String(20), nullable=False, index=True
    )  # success, failure, pending
    status_code = db.Column(db.Integer, nullable=True)  # HTTP status or RPC code
    error_message = db.Column(db.Text, nullable=True)  # Error details if failure

    # Request/Response details (JSON)
    request_data = db.Column(db.Text, nullable=True)  # Request parameters (redacted)
    response_data = db.Column(db.Text, nullable=True)  # Response summary (redacted)

    # Context information
    ip_address = db.Column(db.String(45), nullable=True, index=True)  # IPv4 or IPv6
    user_agent = db.Column(db.String(255), nullable=True)

    # Security & Compliance (AUDIT-001)
    signature = db.Column(db.String(64), nullable=True)  # HMAC-SHA256
    previous_hash = db.Column(db.String(64), nullable=True)  # Hash chaining
    compliance_tags = db.Column(
        db.Text, nullable=True
    )  # JSON list of tags (GDPR, HIPAA)

    # Timing
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    duration_ms = db.Column(db.Integer, nullable=True)  # Operation duration

    # RPC integration
    rpc_service = db.Column(
        db.String(50), nullable=True, index=True
    )  # NodeService, StorageService, etc.
    rpc_method = db.Column(
        db.String(50), nullable=True, index=True
    )  # RegisterNode, CreateSnapshot, etc.

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

        Returns:
            Created AuditLog instance
        """
        entry = AuditLog(
            user_id=user_id,
            operation=operation,
            resource_type=resource_type,
            action=action,
            status=status,
            resource_id=resource_id,
            status_code=status_code,
            error_message=error_message,
            request_data=json.dumps(request_data) if request_data else None,
            response_data=json.dumps(response_data) if response_data else None,
            ip_address=ip_address,
            user_agent=user_agent,
            duration_ms=duration_ms,
            rpc_service=rpc_service,
            rpc_method=rpc_method,
        )

        # Compute signature and hash chaining if core audit is available
        if HAS_CORE_AUDIT:
            try:
                # Get previous hash
                last_entry = AuditLog.query.order_by(AuditLog.id.desc()).first()
                previous_hash = last_entry.signature if last_entry else "0" * 64
                entry.previous_hash = previous_hash

                # Create core AuditEntry for signing
                core_entry = AuditEntry(
                    operation=operation,
                    resource_type=resource_type,
                    resource_id=str(resource_id) if resource_id else "",
                    actor_id=str(user_id) if user_id else "system",
                    action=action,
                    status=status,
                    timestamp=entry.created_at.isoformat(),
                    details={
                        "request": request_data,
                        "response": response_data,
                        "ip": ip_address,
                        "ua": user_agent,
                    },
                    previous_hash=previous_hash,
                )

                # Sign
                # In production, SECRET_KEY must be set in environment
                secret_key = os.getenv("SECRET_KEY")
                if not secret_key:
                    if os.getenv("FLASK_ENV") == "production":
                        raise ValueError("SECRET_KEY not set in production environment")
                    secret_key = "dev-key"
                
                signer = AuditSigner(secret_key=secret_key)
                entry.signature = signer.sign(core_entry)
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
    def get_user_operations(user_id: int, limit: int = 100, offset: int = 0) -> List['AuditLog']:
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
    def get_resource_operations(resource_type: str, resource_id: Optional[str] = None, limit: int = 100) -> List['AuditLog']:
        """Get audit log entries for specific resource.

        Args:
            resource_type: Type of resource to filter by
            resource_id: Specific resource ID (optional)
            limit: Maximum number of entries

        Returns:
            List of AuditLog entries
        """
        query = AuditLog.query.filter_by(resource_type=resource_type)
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()  # type: ignore

    @staticmethod
    def get_failed_operations(limit: int = 100) -> List['AuditLog']:
        """Get recent failed operations.

        Args:
            limit: Maximum number of entries

        Returns:
            List of AuditLog entries
        """
        return AuditLog.query.filter_by(status="failure").order_by(AuditLog.created_at.desc()).limit(limit).all()  # type: ignore
