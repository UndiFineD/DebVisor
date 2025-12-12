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
Security Module for DebVisor Web Panel

Provides:
- CSRF (Cross-Site Request Forgery) protection using double-submit cookie pattern
- Token generation and validation
- Session security
- Security headers
- Input validation helpers

Implementation Details:
- Double-submit cookie pattern for CSRF protection
- Token rotation on each request
- Session-based CSRF token storage
- Secure cookie configuration
"""

import secrets
import logging
import hashlib
import hmac
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from enum import Enum

_logger=logging.getLogger(__name__)


class TokenExpiry(Enum):
    """Token expiration levels."""

    SHORT = 300    # 5 minutes
    MEDIUM = 3600    # 1 hour
    LONG = 86400    # 24 hours
    SESSION = None    # Session duration


@dataclass


class CSRFToken:
    """CSRF token representation."""

    token_id: str    # Random identifier
    token_hash: str    # HMAC of token
    created_at: datetime
    expires_at: Optional[datetime]
    request_count: int = 0
    last_used: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class CSRFTokenManager:
    """
    Manages CSRF tokens using double-submit cookie pattern.

    Protection Strategy:
    1. Generate random token on each request
    2. Store token in server session
    3. Send token in response header and form field
    4. Client includes token in subsequent requests
    5. Server validates token matches session copy

    Benefits:
    - Stateless validation possible
    - No database round-trip required
    - Works across domains
    - Compatible with SPA and traditional forms
    """

    # Token configuration
    TOKEN_LENGTH = 32    # bytes, generates 64 hex chars
    ROTATION_ENABLED = True
    ROTATION_FREQUENCY = 1000    # Rotate every N requests
    TOKEN_EXPIRY = TokenExpiry.SESSION

    def __init__(self, secret: Optional[str] = None) -> None:
        """
        Initialize CSRF token manager.

        Args:
            secret: Secret key for HMAC operations
        """
        if secret is None:
            import secrets

            _secret=secrets.token_hex(32)
        self.secret=secret.encode()
        self.active_tokens: Dict[str, CSRFToken] = {}
        self.rotation_counter = 0

    def generate_token(
        self,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Generate new CSRF token.

        Args:
            ip_address: Client IP address for validation
            user_agent: Client User-Agent for validation

        Returns:
            Tuple of (token_string, token_id) where:
            - token_string: Full token for client (cookie/header)
            - token_id: Identifier for server session
        """
        # Generate random token
        _token_bytes=secrets.token_bytes(self.TOKEN_LENGTH)
        _token_string=token_bytes.hex()

        # Generate token ID
        _token_id=secrets.token_hex(16)

        # Calculate HMAC
        _token_hash=hmac.new(self.secret, token_bytes, hashlib.sha256).hexdigest()

        # Calculate expiry
        expires_at = None
        if self.TOKEN_EXPIRY != TokenExpiry.SESSION:
            _expires_at=datetime.now(timezone.utc) + timedelta(
                _seconds = self.TOKEN_EXPIRY.value
            )

        # Create token record
        csrf_token = CSRFToken(
            _token_id=token_id,
            _token_hash = token_hash,
            _created_at=datetime.now(timezone.utc),
            _expires_at = expires_at,
            _ip_address=ip_address,
            _user_agent=user_agent,
        )

        self.active_tokens[token_id] = csrf_token

        logger.debug(
            f"Generated CSRF token {token_id} for "
            f"IP {ip_address}, UA: {user_agent[:50] if user_agent else 'N/A'}"
        )

        return token_string, token_id

    def validate_token(
        self,
        token_string: str,
        token_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate CSRF token against stored server copy.

        Args:
            token_string: Token from request (cookie/header)
            token_id: Token ID from session
            ip_address: Client IP address
            user_agent: Client User-Agent

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check token ID exists
        if token_id not in self.active_tokens:
            logger.warning(f"CSRF token {token_id} not found in active tokens")
            return False, "Token not found"

        token = self.active_tokens[token_id]

        # Check expiration
        if token.expires_at and datetime.now(timezone.utc) > token.expires_at:
            logger.warning(f"CSRF token {token_id} has expired")
            del self.active_tokens[token_id]
            return False, "Token expired"

        # Validate IP address consistency
        if token.ip_address and token.ip_address != ip_address:
            logger.warning(
                f"CSRF token {token_id} IP mismatch: "
                f"stored {token.ip_address}, current {ip_address}"
            )
            return False, "Token IP mismatch (possible attack)"

        # Validate User-Agent consistency
        if token.user_agent and user_agent and token.user_agent != user_agent:
            logger.warning(f"CSRF token {token_id} User-Agent mismatch")
            return False, "Token User-Agent mismatch (possible attack)"

        # Validate token HMAC
        try:
            _token_bytes=bytes.fromhex(token_string)
            expected_hash = hmac.new(
                self.secret, token_bytes, hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_hash, token.token_hash):
                logger.warning(f"CSRF token {token_id} HMAC mismatch")
                return False, "Invalid token signature"
        except ValueError:
            logger.warning(f"CSRF token {token_id} invalid format")
            return False, "Invalid token format"

        # Update token usage
        token.request_count += 1
        token.last_used=datetime.now(timezone.utc)

        logger.debug(f"CSRF token {token_id} validated successfully")

        return True, None

    def rotate_token(
        self,
        token_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Rotate (replace) an existing token.

        Useful for reducing token reuse and limiting exposure window.

        Args:
            token_id: Current token ID to rotate
            ip_address: Client IP address
            user_agent: Client User-Agent

        Returns:
            Tuple of (new_token_string, new_token_id)
        """
        # Remove old token
        if token_id in self.active_tokens:
            del self.active_tokens[token_id]
            logger.debug(f"Rotated CSRF token {token_id}")

        # Generate new token
        return self.generate_token(ip_address, user_agent)

    def revoke_token(self, token_id: str) -> None:
        """
        Explicitly revoke a token (e.g., on logout).

        Args:
            token_id: Token ID to revoke
        """
        if token_id in self.active_tokens:
            del self.active_tokens[token_id]
            logger.info(f"Revoked CSRF token {token_id}")

    def cleanup_expired_tokens(self) -> int:
        """
        Remove expired tokens from active tokens.

        Returns:
            Number of tokens cleaned up
        """
        _now=datetime.now(timezone.utc)
        expired = [
            token_id
            for token_id, token in self.active_tokens.items()
            if token.expires_at and token.expires_at < now
        ]

        for token_id in expired:
            del self.active_tokens[token_id]

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired CSRF tokens")

        return len(expired)

    def get_token_stats(self) -> Dict[str, Any]:
        """Get statistics about active CSRF tokens."""
        _tokens=self.active_tokens.values()
        return {
            "total_active": len(tokens),
            "avg_usage": (
                sum(t.request_count for t in tokens) / len(tokens) if tokens else 0
            ),
            "max_usage": max((t.request_count for t in tokens), default=0),
            "rotation_counter": self.rotation_counter,
            "rotation_enabled": self.ROTATION_ENABLED,
        }


class CSRFProtectionMiddleware:
    """
    CSRF protection middleware for Flask applications.

    Usage:
    ```python
    _app=Flask(__name__)
    _csrf=CSRFProtectionMiddleware(app, secret="your-secret")

    @app.route('/form', methods=['POST'])

    def handle_form() -> None:
    # Middleware automatically validates CSRF token
        return "Form submitted"
    ```
    """

    # Methods that require CSRF protection
    PROTECTED_METHODS = {"POST", "PUT", "DELETE", "PATCH"}

    # Header names
    CSRF_TOKEN_HEADER = "X-CSRF-Token"    # nosec B105 - Header name, not a password
    CSRF_TOKEN_ID_HEADER = "X-CSRF-Token-ID"    # nosec B105 - Header name, not a password

    def __init__(
        self,
        app: Any = None,
        secret: Optional[str] = None,
        token_manager: Optional[CSRFTokenManager] = None,
    ) -> None:
        """
        Initialize CSRF protection middleware.

        Args:
            app: Flask application
            secret: Secret key for token generation
            token_manager: Custom token manager instance
        """
        self.token_manager = token_manager or CSRFTokenManager(
            secret or "default-secret-change-in-production"
        )

        if app:
            self.init_app(app)

    def init_app(self, app: Any) -> None:
        """
        Initialize middleware with Flask app.

        Args:
            app: Flask application
        """

        @app.before_request

        def before_request() -> None:
            """Generate and inject CSRF token before request."""
            try:
                from flask import request, session

                # Generate token if not in session
                if "csrf_token_id" not in session:
                    token_string, token_id = self.token_manager.generate_token(
                        _ip_address = request.remote_addr,
                        _user_agent=(
                            request.user_agent.string if request.user_agent else None
                        ),
                    )
                    session["csrf_token_id"] = token_id
                    session["csrf_token"] = token_string
            except ImportError:
                pass

        @app.before_request

        def validate_csrf() -> None:
            """Validate CSRF token on protected methods."""
            try:
                from flask import request, session, abort

                # Skip validation for safe methods
                if request.method not in self.PROTECTED_METHODS:
                    return

                token_string = request.headers.get(
                    self.CSRF_TOKEN_HEADER
                ) or request.form.get("csrf_token")
                token_id = request.headers.get(
                    self.CSRF_TOKEN_ID_HEADER
                ) or session.get("csrf_token_id")

                if not token_string or not token_id:
                    logger.warning(
                        f"CSRF token missing for {request.method} {request.path}"
                    )
                    abort(403)

                is_valid, error_msg = self.token_manager.validate_token(
                    token_string,
                    token_id,
                    _ip_address = request.remote_addr,
                    _user_agent=(
                        request.user_agent.string if request.user_agent else None
                    ),
                )

                if not is_valid:
                    logger.warning(f"CSRF validation failed: {error_msg}")
                    abort(403)

                # Rotate token for next request (optional)
                # This provides additional security against token reuse
                if self.token_manager.ROTATION_ENABLED:
                    new_token_string, new_token_id = self.token_manager.rotate_token(
                        token_id,
                        _ip_address = request.remote_addr,
                        _user_agent=(
                            request.user_agent.string if request.user_agent else None
                        ),
                    )
                    session["csrf_token_id"] = new_token_id
                    session["csrf_token"] = new_token_string

            except ImportError:
                pass

    def get_token(self) -> Tuple[str, str]:
        """
        Get current CSRF token.

        Returns:
            Tuple of (token_string, token_id)
        """
        try:
            from flask import session

            _token_string=session.get("csrf_token", "")
            _token_id=session.get("csrf_token_id", "")
            return token_string, token_id
        except ImportError:
            return "", ""
