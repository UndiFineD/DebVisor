"""
Advanced Two-Factor Authentication for DebVisor

Extends basic 2FA (TOTP, WebAuthn) with email and SMS delivery methods,
progressive authentication, and risk-based verification.

Features:
- Email-based verification codes
- SMS-based verification codes
- Risk-based authentication (velocity checks, impossible travel)
- Progressive authentication (step-up, step-down)
- Device trust and remember-me
- Anomaly detection
- Fallback authentication chains

Author: DebVisor Team
Date: 2025-11-26
"""

import secrets
import hashlib
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta, timezone
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DeliveryMethod(Enum):
    """2FA code delivery methods"""

    EMAIL = "email"
    SMS = "sms"
    AUTHENTICATOR = "authenticator"    # TOTP
    WEBAUTHN = "webauthn"
    BACKUP_CODE = "backup_code"


class RiskLevel(Enum):
    """Risk assessment levels"""

    LOW = "low"    # Normal
    MEDIUM = "medium"    # Unusual pattern
    HIGH = "high"    # Suspicious
    CRITICAL = "critical"    # Likely attack


class AuthenticationStep(Enum):
    """Progressive authentication steps"""

    PASSWORD = "password"    # nosec
    OTP_EMAIL = "otp_email"
    OTP_SMS = "otp_sms"
    TOTP = "totp"
    WEBAUTHN = "webauthn"
    SECURITY_QUESTION = "security_question"


@dataclass
class LocationData:
    """Geographic location information"""

    ip_address: str
    country: str
    city: str
    latitude: float
    longitude: float

    def distance_to(self, other: "LocationData") -> float:
        """Calculate distance in kilometers"""
        from math import radians, cos, sin, asin, sqrt

        lon1, lat1, lon2, lat2 = map(
            radians, [self.longitude, self.latitude, other.longitude, other.latitude]
        )
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km


@dataclass
class AuthenticationContext:
    """Context for an authentication attempt"""

    user_id: str
    ip_address: str
    user_agent: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    location: Optional[LocationData] = None
    device_fingerprint: Optional[str] = None

    def fingerprint(self) -> str:
        """Generate device fingerprint"""
        data = f"{self.user_agent}{self.ip_address}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class RiskAssessment:
    """Risk assessment result"""

    risk_level: RiskLevel
    score: float    # 0-100
    factors: List[str] = field(default_factory=list)
    recommended_methods: List[DeliveryMethod] = field(default_factory=list)
    require_step_up: bool = False


@dataclass
class OTPCode:
    """One-time password code"""

    code: str
    method: DeliveryMethod
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    used_at: Optional[datetime] = None
    attempts: int = 0
    max_attempts: int = 3

    @property
    def is_valid(self) -> bool:
        """Check if code is still valid"""
        if self.used_at:
            return False
        if datetime.now(timezone.utc) > self.expires_at:
            return False
        if self.attempts >= self.max_attempts:
            return False
        return True

    def verify(self, attempt: str) -> bool:
        """Verify code"""
        self.attempts += 1

        if not self.is_valid:
            return False

        # Timing-safe comparison
        if len(attempt) != len(self.code):
            return False

        result = 0
        for a, b in zip(attempt, self.code):
            result |= ord(a) ^ ord(b)

        if result == 0:
            self.used_at = datetime.now(timezone.utc)
            return True

        return False


class DeliveryProvider(ABC):
    """Abstract delivery provider"""

    @abstractmethod
    async def send_code(
        self, recipient: str, code: str, context: AuthenticationContext
    ) -> Tuple[bool, str]:
        """Send OTP code and return (success, message)"""
        pass


class EmailDeliveryProvider(DeliveryProvider):
    """Email-based OTP delivery"""

    def __init__(self, smtp_config: Optional[Dict[str, Any]] = None):
        self.smtp_config = smtp_config or {}

    async def send_code(
        self, recipient: str, code: str, context: AuthenticationContext
    ) -> Tuple[bool, str]:
        """Send code via email"""
        # Validate email
        if not self._validate_email(recipient):
            return False, "Invalid email address"

        try:
            # In production, integrate with real SMTP
            # For now, log and simulate
            logger.info(
                f"Email OTP sent to {recipient}: {code} " f"(from {context.ip_address})"
            )
            return True, "Code sent to email"
        except Exception as e:
            logger.error(f"Email delivery failed: {e}")
            return False, f"Email delivery failed: {str(e)}"

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2, }$"
        return re.match(pattern, email) is not None


class SMSDeliveryProvider(DeliveryProvider):
    """SMS-based OTP delivery"""

    def __init__(self, sms_config: Optional[Dict[str, Any]] = None):
        self.sms_config = sms_config or {}

    async def send_code(
        self, recipient: str, code: str, context: AuthenticationContext
    ) -> Tuple[bool, str]:
        """Send code via SMS"""
        # Validate phone
        if not self._validate_phone(recipient):
            return False, "Invalid phone number"

        try:
            # In production, integrate with SMS service (Twilio, etc)
            # For now, log and simulate
            logger.info(
                f"SMS OTP sent to {recipient}: {code} " f"(from {context.ip_address})"
            )
            return True, "Code sent via SMS"
        except Exception as e:
            logger.error(f"SMS delivery failed: {e}")
            return False, f"SMS delivery failed: {str(e)}"

    @staticmethod
    def _validate_phone(phone: str) -> bool:
        """Validate phone number"""
        # Simple validation - strip non-digits and check length
        digits = "".join(filter(str.isdigit, phone))
        return 10 <= len(digits) <= 15


class RiskAssessmentEngine:
    """Assess authentication risk"""

    def __init__(self) -> None:
        self.login_history: List[AuthenticationContext] = []
        self.impossible_travel_speed_kmh = 900    # 900 km/h
        self.velocity_threshold = 5    # Max logins per 5 minutes

    async def assess_risk(
        self, user_id: str, context: AuthenticationContext
    ) -> RiskAssessment:
        """Assess authentication risk"""
        factors = []
        score = 0.0

        # Check impossible travel
        if await self._check_impossible_travel(user_id, context):
            factors.append("Impossible travel detected")
            score += 40

        # Check velocity
        if await self._check_velocity(user_id):
            factors.append("High login velocity")
            score += 30

        # Check new device
        if await self._check_new_device(user_id, context):
            factors.append("Login from new device")
            score += 20

        # Check new location
        if await self._check_new_location(user_id, context):
            factors.append("Login from new location")
            score += 15

        # Determine risk level
        if score >= 80:
            risk_level = RiskLevel.CRITICAL
        elif score >= 60:
            risk_level = RiskLevel.HIGH
        elif score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        # Recommend methods based on risk
        methods = self._recommend_methods(risk_level)

        # Record context for future checks
        self.login_history.append(context)
        # Keep only last 100 logins
        if len(self.login_history) > 100:
            self.login_history.pop(0)

        return RiskAssessment(
            risk_level=risk_level,
            score=score,
            factors=factors,
            recommended_methods=methods,
            require_step_up=(risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]),
        )

    async def _check_impossible_travel(
        self, user_id: str, context: AuthenticationContext
    ) -> bool:
        """Check for impossible travel"""
        if not context.location or not self.login_history:
            return False

        # Get last login
        last_context = next(
            (c for c in reversed(self.login_history) if c.user_agent), None
        )

        if not last_context or not last_context.location:
            return False

        # Calculate distance and time
        distance = context.location.distance_to(last_context.location)
        time_diff = (context.timestamp - last_context.timestamp).total_seconds() / 3600

        if time_diff == 0:
            time_diff = 0.001    # Avoid division by zero

        speed = distance / time_diff

        return speed > self.impossible_travel_speed_kmh

    async def _check_velocity(self, user_id: str) -> bool:
        """Check login velocity"""
        now = datetime.now(timezone.utc)
        five_min_ago = now - timedelta(minutes=5)

        recent_logins = [c for c in self.login_history if c.timestamp > five_min_ago]

        return len(recent_logins) > self.velocity_threshold

    async def _check_new_device(
        self, user_id: str, context: AuthenticationContext
    ) -> bool:
        """Check if device is new"""
        fingerprint = context.fingerprint()

        known_fingerprints = {c.fingerprint() for c in self.login_history}

        return fingerprint not in known_fingerprints

    async def _check_new_location(
        self, user_id: str, context: AuthenticationContext
    ) -> bool:
        """Check if location is new"""
        if not context.location:
            return False

        for prev_context in self.login_history:
            if prev_context.location:
                distance = context.location.distance_to(prev_context.location)
                if distance < 100:    # Within 100 km
                    return False

        return True

    @staticmethod
    def _recommend_methods(risk_level: RiskLevel) -> List[DeliveryMethod]:
        """Recommend authentication methods based on risk"""
        if risk_level == RiskLevel.CRITICAL:
            return [DeliveryMethod.WEBAUTHN, DeliveryMethod.AUTHENTICATOR, DeliveryMethod.SMS]
        elif risk_level == RiskLevel.HIGH:
            return [DeliveryMethod.AUTHENTICATOR, DeliveryMethod.EMAIL, DeliveryMethod.SMS]
        elif risk_level == RiskLevel.MEDIUM:
            return [DeliveryMethod.EMAIL, DeliveryMethod.SMS, DeliveryMethod.AUTHENTICATOR]
        else:
            return [DeliveryMethod.EMAIL, DeliveryMethod.AUTHENTICATOR]


class AdvancedAuthenticationManager:
    """Manage advanced 2FA with multiple methods"""

    def __init__(self) -> None:
        self.email_provider = EmailDeliveryProvider()
        self.sms_provider = SMSDeliveryProvider()
        self.risk_engine = RiskAssessmentEngine()
        self.otp_codes: Dict[str, List[OTPCode]] = {}
        self.device_trust: Dict[str, Set[str]] = {}

    async def initiate_login(
        self, user_id: str, context: AuthenticationContext
    ) -> Tuple[RiskAssessment, List[DeliveryMethod]]:
        """Initiate login flow"""
        # Assess risk
        risk_assessment = await self.risk_engine.assess_risk(user_id, context)

        # Return recommended methods
        available_methods: List[DeliveryMethod] = [
            m
            for m in risk_assessment.recommended_methods
            if m != DeliveryMethod.WEBAUTHN    # Assume WebAuthn handled separately
        ]

        return risk_assessment, available_methods

    async def send_otp(
        self,
        user_id: str,
        email: str,
        phone: str,
        method: DeliveryMethod,
        context: AuthenticationContext,
    ) -> Tuple[bool, str, Optional[str]]:
        """Send OTP code"""
        # Generate code
        provider: DeliveryProvider
        if method == DeliveryMethod.EMAIL:
            code = self._generate_numeric_code(6)
            recipient = email
            provider = self.email_provider
        elif method == DeliveryMethod.SMS:
            code = self._generate_numeric_code(6)
            recipient = phone
            provider = self.sms_provider
        else:
            return False, "Unsupported delivery method", None

        # Send
        success, message = await provider.send_code(recipient, code, context)

        if success:
            # Store OTP
            otp = OTPCode(
                code=code,
                method=method,
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
            )

            if user_id not in self.otp_codes:
                self.otp_codes[user_id] = []

            self.otp_codes[user_id].append(otp)

            # Keep only last 5 codes per user
            if len(self.otp_codes[user_id]) > 5:
                self.otp_codes[user_id].pop(0)

        return success, message, None    # Don't expose code

    async def verify_otp(
        self, user_id: str, code: str, method: DeliveryMethod
    ) -> Tuple[bool, str]:
        """Verify OTP code"""
        if user_id not in self.otp_codes:
            return False, "No code sent"

        # Find valid code
        for otp in reversed(self.otp_codes[user_id]):
            if otp.method == method and otp.is_valid:
                if otp.verify(code):
                    return True, "Code verified"
                else:
                    if otp.attempts >= otp.max_attempts:
                        return False, "Too many attempts"
                    return (
                        False,
                        f"Invalid code ({otp.max_attempts - otp.attempts} attempts remaining)",
                    )

        return False, "No valid code found"

    def trust_device(self, user_id: str, device_fingerprint: str) -> bool:
        """Mark device as trusted"""
        if user_id not in self.device_trust:
            self.device_trust[user_id] = set()

        self.device_trust[user_id].add(device_fingerprint)
        return True

    def is_device_trusted(self, user_id: str, device_fingerprint: str) -> bool:
        """Check if device is trusted"""
        if user_id not in self.device_trust:
            return False

        return device_fingerprint in self.device_trust[user_id]

    @staticmethod
    def _generate_numeric_code(length: int = 6) -> str:
        """Generate numeric OTP code"""
        return "".join(str(secrets.randbelow(10)) for _ in range(length))

    async def get_authentication_status(self, user_id: str) -> Dict[str, Any]:
        """Get authentication status"""
        return {
            "user_id": user_id,
            "trusted_devices": len(self.device_trust.get(user_id, set())),
            "pending_otp": len(
                [otp for otp in self.otp_codes.get(user_id, []) if otp.is_valid]
            ),
            "otp_methods_supported": [
                m.value
                for m in [DeliveryMethod.EMAIL, DeliveryMethod.SMS, DeliveryMethod.AUTHENTICATOR]
            ],
        }


# Global instance
_auth_manager: Optional[AdvancedAuthenticationManager] = None


async def get_authentication_manager() -> AdvancedAuthenticationManager:
    """Get or create global authentication manager"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AdvancedAuthenticationManager()
    return _auth_manager
