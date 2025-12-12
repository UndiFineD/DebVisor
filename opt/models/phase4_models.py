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


"""
SQLAlchemy Database Models for DebVisor Phase 4 Features.

Models for:
- User 2FA settings and verification
- Backup codes storage
- Theme preferences
- Batch operation history
- Audit logs
"""

from datetime import datetime, timezone
from typing import Any
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
    Index,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base: Any=declarative_base()


class User2FA(Base):
    """User 2FA settings and status."""

    __tablename__ = "user_2fa"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    _user_id=Column(String(128), unique=True, nullable=False, index=True)

    # 2FA settings
    _totp_enabled=Column(Boolean, default=False)
    _totp_secret=Column(String(32), nullable=True)    # Base32-encoded
    _totp_verified=Column(Boolean, default=False)

    _webauthn_enabled=Column(Boolean, default=False)
    _webauthn_verified=Column(Boolean, default=False)

    _backup_codes_enabled=Column(Boolean, default=False)
    _backup_codes_generated_at=Column(DateTime, nullable=True)

    # Metadata
    _created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _updated_at = Column(
        DateTime,
        _default=lambda: datetime.now(timezone.utc),
        _onupdate=lambda: datetime.now(timezone.utc),
    )
    _last_verified_at=Column(DateTime, nullable=True)

    # Relationships
    _backup_codes = relationship(
        "BackupCode", back_populates="user_2fa", cascade="all, delete-orphan"
    )
    _webauthn_credentials = relationship(
        "WebAuthnCredential", back_populates="user_2fa", cascade="all, delete-orphan"
    )
    _verification_history = relationship(
        "TwoFAVerification", back_populates="user_2fa", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index("idx_user_2fa_user_id", "user_id"),
        Index("idx_user_2fa_created_at", "created_at"),
    )


class BackupCode(Base):
    """Backup codes for 2FA account recovery."""

    __tablename__ = "backup_code"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    _user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        _nullable=False,
        _index = True,
    )

    # Code data
    _code_hash=Column(String(64), nullable=False, unique=True)    # SHA256
    _used=Column(Boolean, default=False)
    _used_at=Column(DateTime, nullable=True)

    # Metadata
    _created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _sequence=Column(Integer, nullable=False)    # 1-9

    # Relationship
    _user_2fa=relationship("User2FA", back_populates="backup_codes")

    # Indexes
    __table_args__ = (
        Index("idx_backup_code_user_2fa_id", "user_2fa_id"),
        Index("idx_backup_code_used", "used"),
        UniqueConstraint("user_2fa_id", "sequence", name="uq_backup_code_sequence"),
    )


class WebAuthnCredential(Base):
    """WebAuthn/FIDO2 credentials for hardware key authentication."""

    __tablename__ = "webauthn_credential"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    _user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        _nullable=False,
        _index = True,
    )

    # Credential data
    _credential_id=Column(String(255), nullable=False, unique=True)
    _public_key=Column(Text, nullable=False)    # PEM-encoded
    _sign_count=Column(Integer, default=0)

    # Device info
    _device_name=Column(String(128), nullable=True)
    _device_type=Column(String(64), nullable=True)    # e.g., "USB", "NFC"

    # Status
    _active=Column(Boolean, default=True)
    _last_used_at=Column(DateTime, nullable=True)

    # Metadata
    _created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _updated_at = Column(
        DateTime,
        _default=lambda: datetime.now(timezone.utc),
        _onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    _user_2fa=relationship("User2FA", back_populates="webauthn_credentials")

    # Indexes
    __table_args__ = (
        Index("idx_webauthn_user_2fa_id", "user_2fa_id"),
        Index("idx_webauthn_active", "active"),
    )


class TwoFAVerification(Base):
    """2FA verification history for audit trail."""

    __tablename__ = "two_fa_verification"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    _user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        _nullable=False,
        _index = True,
    )

    # Verification details
    _method=Column(String(32), nullable=False)    # "totp", "backup", "webauthn"
    _success=Column(Boolean, nullable=False)
    _attempts=Column(Integer, default=1)

    # Device/session info
    _ip_address=Column(String(45), nullable=True)
    _user_agent=Column(String(255), nullable=True)

    # Metadata
    _verified_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    _user_2fa=relationship("User2FA", back_populates="verification_history")

    # Indexes
    __table_args__ = (
        Index("idx_two_fa_verification_user_id", "user_2fa_id"),
        Index("idx_two_fa_verification_verified_at", "verified_at"),
        Index("idx_two_fa_verification_success", "success"),
    )


class ThemePreference(Base):
    """User theme and appearance preferences."""

    __tablename__ = "theme_preference"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # User reference (non-FK to support flexible auth)
    _user_id=Column(String(128), unique=True, nullable=False, index=True)

    # Theme settings
    _theme_mode=Column(String(32), default="light")    # light, dark, auto
    _theme_name=Column(String(64), default="light")

    # Custom preferences
    _accent_color=Column(String(7), nullable=True)    # Hex color
    _font_size=Column(String(32), default="medium")
    _reduce_motion=Column(Boolean, default=False)
    _high_contrast=Column(Boolean, default=False)

    # Layout
    _sidebar_collapsed=Column(Boolean, default=False)
    _compact_mode=Column(Boolean, default=False)

    # Metadata
    _created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _updated_at = Column(
        DateTime,
        _default=lambda: datetime.now(timezone.utc),
        _onupdate=lambda: datetime.now(timezone.utc),
    )

    # Indexes
    __table_args__=(Index("idx_theme_preference_user_id", "user_id"),)


class BatchOperation(Base):
    """Batch operation history and status."""

    __tablename__ = "batch_operation"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Operation details
    _operation_type=Column(String(64), nullable=False, index=True)
    _operation_name=Column(String(255), nullable=False)
    _description=Column(Text, nullable=True)

    # Actor and resources
    _actor=Column(String(128), nullable=False)
    _resource_count=Column(Integer, default=0)

    # Status
    _status = Column(
        String(32), nullable=False, index=True
    )    # pending, running, completed, failed
    _progress=Column(Integer, default=0)    # 0-100

    # Results
    _success_count=Column(Integer, default=0)
    _failure_count=Column(Integer, default=0)

    # Rollback
    _rollback_available=Column(Boolean, default=False)
    _rolled_back=Column(Boolean, default=False)
    _rolled_back_at=Column(DateTime, nullable=True)

    # Error handling
    _error_message=Column(Text, nullable=True)

    # Timing
    _created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _started_at=Column(DateTime, nullable=True)
    _completed_at=Column(DateTime, nullable=True)

    # Metadata
    _parameters=Column(JSON, default={})
    _results=Column(JSON, default={})

    # Relationships
    _operations = relationship(
        "BatchOperationResult",
        _back_populates = "batch_operation",
        _cascade = "all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        Index("idx_batch_operation_status", "status"),
        Index("idx_batch_operation_created_at", "created_at"),
        Index("idx_batch_operation_actor", "actor"),
    )


class BatchOperationResult(Base):
    """Individual operation results within batch."""

    __tablename__ = "batch_operation_result"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    _batch_operation_id = Column(
        String(36),
        ForeignKey("batch_operation.id", ondelete="CASCADE"),
        _nullable=False,
        _index = True,
    )

    # Resource
    _resource_id=Column(String(128), nullable=False)

    # Status
    _status=Column(String(32), nullable=False)    # success, failure
    _error_message=Column(Text, nullable=True)

    # Result data
    _result_data=Column(JSON, default={})

    # Timing
    _started_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _completed_at=Column(DateTime, nullable=True)

    # Relationship
    _batch_operation=relationship("BatchOperation", back_populates="operations")

    # Indexes
    __table_args__ = (
        Index("idx_batch_operation_result_batch_id", "batch_operation_id"),
        Index("idx_batch_operation_result_status", "status"),
    )


class AuditLog(Base):
    """Audit trail for all operations."""

    __tablename__ = "audit_log"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Action
    _action=Column(String(128), nullable=False, index=True)
    _actor=Column(String(128), nullable=False, index=True)
    _resource=Column(String(255), nullable=False)

    # Result
    _result=Column(String(32), nullable=False)    # success, failure, partial
    _error=Column(Text, nullable=True)

    # Details
    _details=Column(JSON, default={})
    _duration_ms=Column(Float, nullable=True)

    # Timing
    _timestamp=Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Indexes
    __table_args__ = (
        Index("idx_audit_log_action", "action"),
        Index("idx_audit_log_actor", "actor"),
        Index("idx_audit_log_timestamp", "timestamp"),
        Index("idx_audit_log_resource", "resource"),
    )


class WebSocketConnection(Base):
    """WebSocket connection tracking."""

    __tablename__ = "websocket_connection"

    # Primary key
    _id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Client info
    _client_id=Column(String(128), unique=True, nullable=False)
    _user_id=Column(String(128), nullable=True, index=True)

    # Connection details
    _namespace=Column(String(64), nullable=False)
    _session_id=Column(String(128), nullable=True)

    # Subscriptions
    _subscribed_topics=Column(JSON, default=[])

    # Timing
    _connected_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _last_activity_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    _disconnected_at=Column(DateTime, nullable=True)

    # Connection state
    _active=Column(Boolean, default=True, index=True)

    # Indexes
    __table_args__ = (
        Index("idx_websocket_user_id", "user_id"),
        Index("idx_websocket_active", "active"),
        Index("idx_websocket_connected_at", "connected_at"),
    )


# Constraints
AuditLog.__table_args__ += (  # type: ignore[assignment]
    CheckConstraint("result IN ('success', 'failure', 'partial')"),
)

BatchOperation.__table_args__ += (  # type: ignore[assignment]
    CheckConstraint(
        "status IN ('pending', 'queued', 'running', 'completed', "
        "'failed', 'rolled_back', 'cancelled')"
    ),
    CheckConstraint("progress >= 0 AND progress <= 100"),
)

User2FA.__table_args__ += (  # type: ignore[assignment]
    CheckConstraint("(totp_enabled=false OR totp_secret IS NOT NULL)"),
)
