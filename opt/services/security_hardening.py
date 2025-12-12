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
Security Hardening for DebVisor Phase 4

Provides security middleware, input validation, and protection against common attacks:
- CSRF protection
- XSS prevention
- SQL injection prevention
- CORS configuration
- Rate limiting
- Security headers
- Helmet-style protections
- HTTPS/TLS enforcement

Author: DebVisor Team
Date: 2025-11-26
"""

import secrets
import hashlib
import logging
import re
from typing import Optional, Dict, List, Callable, Any, Tuple, cast
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta, timezone
from functools import wraps

_logger = logging.getLogger(__name__)


class AttackType(Enum):
    """Types of attacks to protect against"""

    CSRF = "csrf"
    XSS = "xss"
    SQL_INJECTION = "sql_injection"
    CLICKJACKING = "clickjacking"
    CORS = "cors"
    RATE_LIMIT = "rate_limit"
    BRUTE_FORCE = "brute_force"
    COMMAND_INJECTION = "command_injection"
    XXE = "xxe"
    INSECURE_DESERIALIZATION = "insecure_deserialization"


@dataclass


class SecurityEvent:
    """Security event for audit logging"""

    event_type: AttackType
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[str] = None
    ip_address: str = ""
    description: str = ""
    severity: str = "warning"    # info, warning, error, critical
    request_path: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "description": self.description,
            "severity": self.severity,
            "request_path": self.request_path,
            "user_agent": self.user_agent,
            "metadata": self.metadata,
        }


@dataclass


class CSRFToken:
    """CSRF protection token"""

    token: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    used: bool = False
    used_at: Optional[datetime] = None

    @property

    def is_valid(self) -> bool:
        """Check if token is still valid"""
        if self.used:
            return False
        # Tokens valid for 1 hour
        age = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return age < 3600

    def verify(self, other_token: str) -> bool:
        """Verify token with timing-safe comparison"""
        if not self.is_valid:
            return False

        # Timing-safe comparison
        if len(other_token) != len(self.token):
            return False

        result = 0
        for a, b in zip(other_token, self.token):
            result |= ord(a) ^ ord(b)

        if result == 0:
            self.used = True
            self.used_at = datetime.now(timezone.utc)
            return True

        return False


class CSRFProtection:
    """CSRF attack prevention"""

    def __init__(self) -> None:
        self.tokens: Dict[str, List[CSRFToken]] = {}
        self.exempt_methods = {"GET", "HEAD", "OPTIONS"}

    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token"""
        token_data = secrets.token_bytes(32)
        token_str = hashlib.sha256(token_data).hexdigest()

        if session_id not in self.tokens:
            self.tokens[session_id] = []

        csrf_token = CSRFToken(token=token_str)
        self.tokens[session_id].append(csrf_token)

        # Keep only last 10 tokens
        if len(self.tokens[session_id]) > 10:
            self.tokens[session_id].pop(0)

        return token_str

    def verify_token(self, session_id: str, token: str) -> Tuple[bool, str]:
        """Verify CSRF token"""
        if session_id not in self.tokens:
            return False, "No tokens for session"

        for csrf_token in reversed(self.tokens[session_id]):
            if csrf_token.verify(token):
                return True, "Token verified"

        return False, "Invalid or expired token"

    def is_token_required(self, method: str) -> bool:
        """Check if token required for method"""
        return method not in self.exempt_methods


class InputValidator:
    """Validate and sanitize user input"""

    # Patterns for detection
    SQL_KEYWORDS = re.compile(
        r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|EXEC|SCRIPT)\b", re.IGNORECASE
    )

    XSS_PATTERNS = re.compile(
        r"(<script|javascript:|on\w+\s*=|<iframe|<img|<svg|alert|confirm)",
        re.IGNORECASE,
    )

    COMMAND_INJECTION = re.compile(r"[;&|`$(){}[\]<>]")

    @staticmethod

    def sanitize_string(value: Any, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return ""

        # Truncate
        value = value[:max_length]

        # Remove null bytes
        value = value.replace("\0", "")

        # Encode non-printable characters
        value = "".join(
            c if ord(c) >= 32 and ord(c) != 127 else f"\\x{ord(c):02x}" for c in value
        )

        return str(value.strip())

    @staticmethod

    def detect_sql_injection(value: str) -> bool:
        """Detect potential SQL injection"""
        return bool(InputValidator.SQL_KEYWORDS.search(value))

    @staticmethod

    def detect_xss(value: str) -> bool:
        """Detect potential XSS"""
        return bool(InputValidator.XSS_PATTERNS.search(value))

    @staticmethod

    def detect_command_injection(value: str) -> bool:
        """Detect potential command injection"""
        return bool(InputValidator.COMMAND_INJECTION.search(value))

    @staticmethod

    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2, }$"
        return re.match(pattern, email) is not None

    @staticmethod

    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = (
            r"^https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9._-]*)*(?:\?[a-zA-Z0-9._=-]*)?$"
        )
        return re.match(pattern, url) is not None


class RateLimiter:
    """Rate limiting protection"""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.request_history: Dict[str, List[datetime]] = {}

    def is_rate_limited(self, identifier: str) -> bool:
        """Check if identifier is rate limited"""
        now = datetime.now(timezone.utc)
        one_minute_ago = now - timedelta(minutes=1)

        if identifier not in self.request_history:
            self.request_history[identifier] = []

        # Clean old requests
        self.request_history[identifier] = [
            t for t in self.request_history[identifier] if t > one_minute_ago
        ]

        if len(self.request_history[identifier]) >= self.requests_per_minute:
            return True

        self.request_history[identifier].append(now)
        return False

    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        if identifier not in self.request_history:
            return self.requests_per_minute

        return max(0, self.requests_per_minute - len(self.request_history[identifier]))


class CORSPolicy:
    """CORS protection policy"""

    def __init__(
        self,
        allowed_origins: Optional[List[str]] = None,
        allowed_methods: Optional[List[str]] = None,
        allowed_headers: Optional[List[str]] = None,
        max_age: int = 3600,
    ):
        self.allowed_origins = allowed_origins or ["http://localhost:3000"]
        self.allowed_methods = allowed_methods or [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ]
        self.allowed_headers = allowed_headers or ["Content-Type", "Authorization"]
        self.max_age = max_age

    def is_origin_allowed(self, origin: str) -> bool:
        """Check if origin is allowed"""
        # Allow any origin that matches pattern
        for allowed in self.allowed_origins:
            if allowed == "*":
                return True
            if allowed == origin:
                return True
            # Support wildcards
            if allowed.startswith("*.") and origin.endswith(allowed[1:]):
                return True
        return False

    def get_response_headers(self, origin: str) -> Dict[str, str]:
        """Get CORS response headers"""
        headers = {
            "Access-Control-Allow-Methods": ", ".join(self.allowed_methods),
            "Access-Control-Allow-Headers": ", ".join(self.allowed_headers),
            "Access-Control-Max-Age": str(self.max_age),
        }

        if self.is_origin_allowed(origin):
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"

        return headers


class SecurityHeaderManager:
    """Manage security headers"""

    @staticmethod

    def get_security_headers() -> Dict[str, str]:
        """Get recommended security headers"""
        return {
        # Prevent clickjacking
            "X-Frame-Options": "DENY",
            # Prevent MIME sniffing
            "X-Content-Type-Options": "nosniff",
            # Enable XSS filter
            "X-XSS-Protection": "1; mode=block",
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'sel' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            ),
            # HSTS (for HTTPS only)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            # Feature policy
            "Permissions-Policy": (
                "accelerometer=(), "
                "camera=(), "
                "geolocation=(), "
                "gyroscope=(), "
                "magnetometer=(), "
                "microphone=(), "
                "payment=(), "
                "usb=()"
            ),
        }


class SecurityAuditLog:
    """Security event audit logging"""

    def __init__(self, max_events: int = 10000):
        self.events: List[SecurityEvent] = []
        self.max_events = max_events

    def log_event(self, event: SecurityEvent) -> None:
        """Log security event"""
        self.events.append(event)

        # Keep only recent events
        if len(self.events) > self.max_events:
            self.events.pop(0)

        # Also log to logger
        logger.warning(
            f"Security Event: {event.event_type.value} - {event.description} "
            f"(IP: {event.ip_address})"
        )

    def get_events(
        self,
        attack_type: Optional[AttackType] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[SecurityEvent]:
        """Get security events with filtering"""
        events: List[SecurityEvent] = self.events

        if attack_type:
            events = [e for e in events if e.event_type == attack_type]

        if severity:
            events = [e for e in events if e.severity == severity]

        return events[-limit:]

    def get_event_summary(self) -> Dict[str, Any]:
        """Get summary of security events"""
        summary: Dict[str, Any] = {
            "total_events": len(self.events),
            "by_type": {},
            "by_severity": {},
            "recent_events": [],
        }

        for event in self.events:
            type_key = event.event_type.value
            by_type = cast(Dict[str, int], summary["by_type"])
            by_type[type_key] = by_type.get(type_key, 0) + 1

            by_severity = cast(Dict[str, int], summary["by_severity"])
            by_severity[event.severity] = (
                by_severity.get(event.severity, 0) + 1
            )

        # Get 10 most recent critical events
        critical_events = [e for e in self.events if e.severity == "critical"]
        summary["recent_events"] = [e.to_dict() for e in critical_events[-10:]]

        return summary


class SecurityManager:
    """Central security management for DebVisor"""

    def __init__(self) -> None:
        self.csrf = CSRFProtection()
        self.input_validator = InputValidator()
        self.rate_limiter = RateLimiter(requests_per_minute=100)
        self.cors = CORSPolicy()
        self.audit_log = SecurityAuditLog()

    def validate_request(
        self,
        method: str,
        path: str,
        ip_address: str,
        user_agent: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, Optional[SecurityEvent]]:
        """Validate incoming request"""
        # Check rate limit
        identifier = f"{ip_address}:{path}"
        if self.rate_limiter.is_rate_limited(identifier):
            event = SecurityEvent(
                _event_type = AttackType.RATE_LIMIT,
                _ip_address = ip_address,
                _severity = "warning",
                _description = "Rate limit exceeded",
                _request_path = path,
                _user_agent = user_agent,
            )
            self.audit_log.log_event(event)
            return False, event

        # Validate input data
        if data:
            for key, value in data.items():
                if isinstance(value, str):
                    if self.input_validator.detect_sql_injection(value):
                        event = SecurityEvent(
                            _event_type = AttackType.SQL_INJECTION,
                            _ip_address = ip_address,
                            _severity = "critical",
                            _description = f"SQL injection detected in {key}",
                            _request_path = path,
                            _user_agent = user_agent,
                            _metadata = {"field": key},
                        )
                        self.audit_log.log_event(event)
                        return False, event

                    if self.input_validator.detect_xss(value):
                        event = SecurityEvent(
                            _event_type = AttackType.XSS,
                            _ip_address = ip_address,
                            _severity = "critical",
                            _description = f"XSS detected in {key}",
                            _request_path = path,
                            _user_agent = user_agent,
                            _metadata = {"field": key},
                        )
                        self.audit_log.log_event(event)
                        return False, event

        return True, None

    def get_security_status(self) -> Dict[str, Any]:
        """Get overall security status"""
        return {
            "csrf_protection": "enabled",
            "input_validation": "enabled",
            "rate_limiting": "enabled",
            "cors_policy": "configured",
            "security_headers": "enabled",
            "audit_logging": "enabled",
            "events_summary": self.audit_log.get_event_summary(),
        }


# Global security manager
_security_manager: Optional[SecurityManager] = None


def get_security_manager() -> SecurityManager:
    """Get or create global security manager"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


def require_csrf_protection(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to require CSRF protection"""

    @wraps(func)
    async def wrapper(request: Any, *args: Any, **kwargs: Any) -> Any:
        _manager = get_security_manager()

        # Get session and token
        session_id = request.cookies.get("session_id", "")
        token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")

        if not token:
            raise ValueError("CSRF token required")

        # Verify token
        valid, message = manager.csrf.verify_token(session_id, token)
        if not valid:
            raise ValueError(f"CSRF validation failed: {message}")

        return await func(request, *args, **kwargs)

    return wrapper
