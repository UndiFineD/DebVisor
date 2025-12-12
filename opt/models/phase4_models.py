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

Base: Any = declarative_base()


class User2FA(Base):
    """User 2FA settings and status."""

    __tablename__ = "user_2fa"

    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    user_id = Column(String(128), unique=True, nullable=False, index=True)

    # 2FA settings
    totp_enabled = Column(Boolean, default=False)
    totp_secret = Column(String(32), nullable=True)    # Base32-encoded
    totp_verified = Column(Boolean, default=False)

    webauthn_enabled = Column(Boolean, default=False)
    webauthn_verified = Column(Boolean, default=False)

    backup_codes_enabled = Column(Boolean, default=False)
    backup_codes_generated_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_verified_at = Column(DateTime, nullable=True)

    # Relationships
    backup_codes = relationship(
        "BackupCode", back_populates="user_2fa", cascade="all, delete-orphan"
    )
    webauthn_credentials = relationship(
        "WebAuthnCredential", back_populates="user_2fa", cascade="all, delete-orphan"
    )
    verification_history = relationship(
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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Code data
    code_hash = Column(String(64), nullable=False, unique=True)    # SHA256
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sequence = Column(Integer, nullable=False)    # 1-9

    # Relationship
    user_2fa = relationship("User2FA", back_populates="backup_codes")

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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Credential data
    credential_id = Column(String(255), nullable=False, unique=True)
    public_key = Column(Text, nullable=False)    # PEM-encoded
    sign_count = Column(Integer, default=0)

    # Device info
    device_name = Column(String(128), nullable=True)
    device_type = Column(String(64), nullable=True)    # e.g., "USB", "NFC"

    # Status
    active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    user_2fa = relationship("User2FA", back_populates="webauthn_credentials")

    # Indexes
    __table_args__ = (
        Index("idx_webauthn_user_2fa_id", "user_2fa_id"),
        Index("idx_webauthn_active", "active"),
    )


class TwoFAVerification(Base):
    """2FA verification history for audit trail."""

    __tablename__ = "two_fa_verification"

    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    user_2fa_id = Column(
        String(36),
        ForeignKey("user_2fa.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Verification details
    method = Column(String(32), nullable=False)    # "totp", "backup", "webauthn"
    success = Column(Boolean, nullable=False)
    attempts = Column(Integer, default=1)

    # Device/session info
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)

    # Metadata
    verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    user_2fa = relationship("User2FA", back_populates="verification_history")

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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # User reference (non-FK to support flexible auth)
    user_id = Column(String(128), unique=True, nullable=False, index=True)

    # Theme settings
    theme_mode = Column(String(32), default="light")    # light, dark, auto
    theme_name = Column(String(64), default="light")

    # Custom preferences
    accent_color = Column(String(7), nullable=True)    # Hex color
    font_size = Column(String(32), default="medium")
    reduce_motion = Column(Boolean, default=False)
    high_contrast = Column(Boolean, default=False)

    # Layout
    sidebar_collapsed = Column(Boolean, default=False)
    compact_mode = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Indexes
    __table_args__ = (Index("idx_theme_preference_user_id", "user_id"),)


class BatchOperation(Base):
    """Batch operation history and status."""

    __tablename__ = "batch_operation"

    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Operation details
    operation_type = Column(String(64), nullable=False, index=True)
    operation_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Actor and resources
    actor = Column(String(128), nullable=False)
    resource_count = Column(Integer, default=0)

    # Status
    status = Column(
        String(32), nullable=False, index=True
    )    # pending, running, completed, failed
    progress = Column(Integer, default=0)    # 0-100

    # Results
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)

    # Rollback
    rollback_available = Column(Boolean, default=False)
    rolled_back = Column(Boolean, default=False)
    rolled_back_at = Column(DateTime, nullable=True)

    # Error handling
    error_message = Column(Text, nullable=True)

    # Timing
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Metadata
    parameters = Column(JSON, default={})
    results = Column(JSON, default={})

    # Relationships
    operations = relationship(
        "BatchOperationResult",
        back_populates="batch_operation",
        cascade="all, delete-orphan",
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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key
    batch_operation_id = Column(
        String(36),
        ForeignKey("batch_operation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Resource
    resource_id = Column(String(128), nullable=False)

    # Status
    status = Column(String(32), nullable=False)    # success, failure
    error_message = Column(Text, nullable=True)

    # Result data
    result_data = Column(JSON, default={})

    # Timing
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    # Relationship
    batch_operation = relationship("BatchOperation", back_populates="operations")

    # Indexes
    __table_args__ = (
        Index("idx_batch_operation_result_batch_id", "batch_operation_id"),
        Index("idx_batch_operation_result_status", "status"),
    )


class AuditLog(Base):
    """Audit trail for all operations."""

    __tablename__ = "audit_log"

    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Action
    action = Column(String(128), nullable=False, index=True)
    actor = Column(String(128), nullable=False, index=True)
    resource = Column(String(255), nullable=False)

    # Result
    result = Column(String(32), nullable=False)    # success, failure, partial
    error = Column(Text, nullable=True)

    # Details
    details = Column(JSON, default={})
    duration_ms = Column(Float, nullable=True)

    # Timing
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Client info
    client_id = Column(String(128), unique=True, nullable=False)
    user_id = Column(String(128), nullable=True, index=True)

    # Connection details
    namespace = Column(String(64), nullable=False)
    session_id = Column(String(128), nullable=True)

    # Subscriptions
    subscribed_topics = Column(JSON, default=[])

    # Timing
    connected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_activity_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    disconnected_at = Column(DateTime, nullable=True)

    # Connection state
    active = Column(Boolean, default=True, index=True)

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
    CheckConstraint("(totp_enabled = false OR totp_secret IS NOT NULL)"),
)
