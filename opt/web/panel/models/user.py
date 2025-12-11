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

"""User Model - Authentication and Authorization

Stores user accounts with password hashing via Argon2.
Integrates with Flask-Login for session management.
"""

from typing import Any, Optional
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from opt.web.panel.extensions import db, login_manager


class User(UserMixin, db.Model):
    """User account model with authentication and role management."""

    __tablename__ = "user"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User identification
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Password (hashed with Argon2)
    password_hash = db.Column(db.String(255), nullable=False)

    # User metadata
    full_name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_admin = db.Column(db.Boolean, default=False, index=True)

    # Authentication tracking
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Session tracking
    api_key_hash = db.Column(db.String(255), unique=True, nullable=True)
    api_key_created = db.Column(db.DateTime)
    api_key_last_used = db.Column(db.DateTime)

    # MFA (optional)
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(255))

    # Relationships
    audit_logs = db.relationship(
        "AuditLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        """Hash password using Argon2 and store hash.

        Args:
            password: Plain text password to hash
        """
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password_hash = generate_password_hash(password, method="argon2")

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches hash, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()

    def update_last_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.now(timezone.utc)
        db.session.commit()

    def get_id(self) -> str:
        """Return user ID for Flask-Login."""
        return str(self.id)

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission.

        Args:
            permission: Permission string to check

        Returns:
            True if user is admin or has explicit permission
        """
        if self.is_admin:
            return True
        # Additional permission checking would go here
        # e.g., check role-based permissions from RBAC system
        return False

    def is_authenticated(self) -> bool:
        """Return True if user is authenticated."""
        return bool(self.is_active)

    def is_anonymous(self) -> bool:
        """Return False (not an anonymous user)."""
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary for JSON responses."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


@login_manager.user_loader    # type: ignore
def load_user(user_id: str) -> Optional[User]:
    """Load user from database by ID.

    This callback is required by Flask-Login to reload user from session.
    """
    return User.query.get(int(user_id))    # type: ignore
