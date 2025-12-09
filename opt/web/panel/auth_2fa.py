"""
Two-Factor Authentication (2FA) implementation for DebVisor Web Panel.

Supports multiple 2FA methods:
- TOTP (Time-based One-Time Password)
- WebAuthn/FIDO2 (U2F keys, platform authenticators)
- Email-based backup codes

Features:
- User enrollment workflow with QR code generation
- Verification during login with rate limiting
- Recovery mechanisms with brute-force protection
- Account lockout protection
- Session management
- Rate limiting on verify endpoint (max 5 attempts per 5 minutes per IP)
- Audit logging for all failed attempts
"""

import secrets
import string
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

import pyotp
import qrcode
from io import BytesIO
import base64
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class RateLimitAttemppt:
    """Tracks a failed verification attempt."""

    timestamp: datetime
    ip_address: str
    method: str  # 'totp', 'backup', 'webauthn'
    user_account: Optional[str] = None


class TwoFAVerificationRateLimiter:
    """
    Rate limiter for 2FA verification endpoint.

    Policy:
    - Max 5 attempts per 5 minutes per IP address
    - Temporary lockout after threshold exceeded
    - Audit log for all failed attempts
    """

    MAX_ATTEMPTS = 5
    WINDOW_SECONDS = 300  # 5 minutes
    LOCKOUT_SECONDS = 300  # 5 minutes

    def __init__(self) -> None:
        """Initialize the rate limiter."""
        self.attempts: Dict[str, List[RateLimitAttemppt]] = defaultdict(list)
        self.lockouts: Dict[str, datetime] = {}
        self._lock = __import__("threading").Lock()

    def record_failed_attempt(
        self, ip_address: str, method: str, user_account: Optional[str] = None
    ) -> None:
        """
        Record a failed verification attempt.

        Args:
            ip_address: Client IP address
            method: 2FA method used ('totp', 'backup', 'webauthn')
            user_account: User account if known
        """
        with self._lock:
            now = datetime.now(timezone.utc)
            attempt = RateLimitAttemppt(
                timestamp=now,
                ip_address=ip_address,
                method=method,
                user_account=user_account,
            )
            self.attempts[ip_address].append(attempt)

            # Clean old attempts outside window
            window_start = now - timedelta(seconds=self.WINDOW_SECONDS)
            self.attempts[ip_address] = [
                a for a in self.attempts[ip_address] if a.timestamp > window_start
            ]

            # Audit log the failed attempt
            logger.warning(
                f"2FA verification failed: ip={ip_address}, "
                f"method={method}, account={user_account}, "
                f"attempt_count={len(self.attempts[ip_address])}"
            )

            # Trigger lockout if threshold exceeded
            if len(self.attempts[ip_address]) >= self.MAX_ATTEMPTS:
                self.lockouts[ip_address] = now + timedelta(
                    seconds=self.LOCKOUT_SECONDS
                )
                logger.error(
                    f"2FA verification rate limit exceeded for IP {ip_address}: "
                    f"{self.MAX_ATTEMPTS} attempts in "
                    f"{self.WINDOW_SECONDS} seconds. "
                    f"Temporary lockout enabled for {self.LOCKOUT_SECONDS} seconds."
                )

    def is_rate_limited(self, ip_address: str) -> Tuple[bool, Optional[int]]:
        """
        Check if an IP is currently rate limited.

        Args:
            ip_address: Client IP address

        Returns:
            (is_limited, seconds_until_available)
            If limited, seconds_until_available shows when lockout expires
        """
        with self._lock:
            now = datetime.now(timezone.utc)

            # Check active lockout
            if ip_address in self.lockouts:
                lockout_expires = self.lockouts[ip_address]
                if now < lockout_expires:
                    seconds_remaining = (lockout_expires - now).total_seconds()
                    return True, int(seconds_remaining)
                else:
                    # Lockout expired, clean it up
                    del self.lockouts[ip_address]

            # Check recent attempts in window
            window_start = now - timedelta(seconds=self.WINDOW_SECONDS)
            recent_attempts = [
                a
                for a in self.attempts.get(ip_address, [])
                if a.timestamp > window_start
            ]

            if len(recent_attempts) >= self.MAX_ATTEMPTS:
                return True, self.LOCKOUT_SECONDS

            return False, None

    def record_successful_attempt(self, ip_address: str) -> None:
        """
        Record a successful verification (clears attempt history).

        Args:
            ip_address: Client IP address
        """
        with self._lock:
            if ip_address in self.attempts:
                del self.attempts[ip_address]
            logger.info(f"2FA verification successful for IP {ip_address}")

    def get_attempt_count(self, ip_address: str) -> int:
        """
        Get current failed attempt count for an IP.

        Args:
            ip_address: Client IP address

        Returns:
            Number of failed attempts in current window
        """
        with self._lock:
            now = datetime.now(timezone.utc)
            window_start = now - timedelta(seconds=self.WINDOW_SECONDS)
            return len(
                [
                    a
                    for a in self.attempts.get(ip_address, [])
                    if a.timestamp > window_start
                ]
            )

    def get_audit_log(self, ip_address: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get audit log of verification attempts.

        Args:
            ip_address: Optional filter by IP address

        Returns:
            List of attempt records
        """
        with self._lock:
            if ip_address:
                attempts = self.attempts.get(ip_address, [])
            else:
                attempts = [a for ips in self.attempts.values() for a in ips]

            return [
                {
                    "timestamp": a.timestamp.isoformat(),
                    "ip_address": a.ip_address,
                    "method": a.method,
                    "user_account": a.user_account,
                }
                for a in sorted(attempts, key=lambda x: x.timestamp, reverse=True)
            ]


@dataclass
class TOTPConfig:
    """TOTP (Time-based One-Time Password) configuration."""

    issuer_name: str = "DebVisor"
    account_name_prefix: str = "DebVisor"
    window_size: int = 1  # Number of 30-second windows to accept
    digits: int = 6


@dataclass
class BackupCodeConfig:
    """Backup code configuration."""

    num_codes: int = 9
    code_length: int = 8
    expiration_days: Optional[int] = None  # None = never expire


class TOTPManager:
    """Manages TOTP (Time-based One-Time Password) authentication."""

    def __init__(self, config: Optional[TOTPConfig] = None):
        """
        Initialize TOTP manager.

        Args:
            config: TOTPConfig instance
        """
        self.config = config or TOTPConfig()

    def generate_secret(self) -> str:
        """
        Generate a new TOTP secret.

        Returns:
            Base32-encoded secret key
        """
        return pyotp.random_base32()

    def get_totp_uri(
        self, secret: str, account_name: str, issuer: Optional[str] = None
    ) -> str:
        """
        Get provisioning URI for TOTP.

        Args:
            secret: Base32-encoded secret
            account_name: User account identifier
            issuer: Issuer name (defaults to config.issuer_name)

        Returns:
            Provisioning URI for QR code
        """
        issuer = issuer or self.config.issuer_name
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=f"{self.config.account_name_prefix}:{account_name}",
            issuer_name=issuer,
        )

    def generate_qr_code(self, provisioning_uri: str) -> str:
        """
        Generate QR code for TOTP provisioning.

        Args:
            provisioning_uri: TOTP provisioning URI

        Returns:
            Base64-encoded PNG image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64, {img_base64}"

    def verify_token(self, secret: str, token: str) -> bool:
        """
        Verify TOTP token.

        Args:
            secret: Base32-encoded secret
            token: 6-digit token from authenticator app

        Returns:
            True if token is valid, False otherwise
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=self.config.window_size)

    def get_provisioning_info(self, secret: str, account_name: str) -> Dict[str, Any]:
        """
        Get complete provisioning information for enrollment.

        Args:
            secret: Base32-encoded secret
            account_name: User account identifier

        Returns:
            Dictionary with secret, provisioning URI, and QR code
        """
        provisioning_uri = self.get_totp_uri(secret, account_name)
        qr_code = self.generate_qr_code(provisioning_uri)

        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "qr_code": qr_code,
            "account_name": account_name,
            "issuer": self.config.issuer_name,
        }


class BackupCodeManager:
    """Manages backup codes for account recovery."""

    def __init__(self, config: Optional[BackupCodeConfig] = None):
        """
        Initialize backup code manager.

        Args:
            config: BackupCodeConfig instance
        """
        self.config = config or BackupCodeConfig()

    def generate_codes(self) -> List[str]:
        """
        Generate a set of backup codes.

        Returns:
            List of backup codes
        """
        alphabet = string.ascii_uppercase + string.digits
        codes = []

        for _ in range(self.config.num_codes):
            # Generate code with format: XXXX-XXXX
            code_part1 = "".join(
                secrets.choice(alphabet) for _ in range(self.config.code_length // 2)
            )
            code_part2 = "".join(
                secrets.choice(alphabet) for _ in range(self.config.code_length // 2)
            )
            code = f"{code_part1}-{code_part2}"
            codes.append(code)

        return codes

    def hash_code(self, code: str) -> str:
        """
        Hash a backup code for storage.

        Args:
            code: Backup code

        Returns:
            Hashed backup code
        """
        import hashlib

        # Normalize: remove spaces, convert to uppercase
        normalized = code.replace(" ", "").replace("-", "").upper()
        return hashlib.sha256(normalized.encode()).hexdigest()

    def verify_code(self, code: str, hashed_code: str) -> bool:
        """
        Verify a backup code.

        Args:
            code: Backup code to verify
            hashed_code: Stored hashed code

        Returns:
            True if code matches, False otherwise
        """
        return self.hash_code(code) == hashed_code

    def format_for_display(self, codes: List[str]) -> str:
        """
        Format backup codes for display/printing.

        Args:
            codes: List of backup codes

        Returns:
            Formatted string suitable for printing
        """
        formatted = "BACKUP CODES - Save these in a secure location\n"
        formatted += "=" * 50 + "\n\n"

        for i, code in enumerate(codes, 1):
            formatted += f"{i:2d}. {code}\n"

        formatted += "\n" + "=" * 50 + "\n"
        formatted += "Each code can only be used once.\n"
        formatted += "Store these codes in a safe place.\n"

        return formatted


@dataclass
class WebAuthnCredential:
    """WebAuthn credential data."""

    credential_id: str
    public_key: str
    sign_count: int
    created_at: datetime
    name: str
    is_primary: bool = False


class WebAuthnManager:
    """Manages WebAuthn/FIDO2 authentication."""

    def __init__(self) -> None:
        """Initialize WebAuthn manager."""
        try:
            import webauthn

            _ = webauthn
            self.available = True
        except ImportError:
            self.available = False

    def is_available(self) -> bool:
        """Check if WebAuthn is available."""
        return self.available

    def generate_registration_options(
        self, user_id: str, user_name: str, user_display_name: str
    ) -> Any:
        """
        Generate WebAuthn registration options.

        Args:
            user_id: Unique user identifier
            user_name: Username
            user_display_name: Display name

        Returns:
            Registration options for client
        """
        if not self.available:
            raise RuntimeError("WebAuthn not available")

        from webauthn import generate_registration_options
        from webauthn.helpers.structs import (
            AuthenticatorSelectionCriteria,
            AuthenticatorAttachment,
            ResidentKeyRequirement,
        )

        options = generate_registration_options(
            rp_id="debvisor.local",
            rp_name="DebVisor",
            user_id=user_id.encode(),
            user_name=user_name,
            user_display_name=user_display_name,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
                resident_key=ResidentKeyRequirement.PREFERRED,
            ),
        )

        from webauthn import options_to_json

        return options_to_json(options)

    def verify_registration_response(
        self, response_json: str, challenge: str
    ) -> Optional[WebAuthnCredential]:
        """
        Verify WebAuthn registration response.

        Args:
            response_json: JSON response from client
            challenge: Original challenge sent to client

        Returns:
            WebAuthnCredential if successful, None otherwise
        """
        if not self.available:
            raise RuntimeError("WebAuthn not available")

        from webauthn import verify_registration_response
        from webauthn.helpers.structs import RegistrationCredential
        from webauthn import base64url_to_bytes

        try:
            credential = RegistrationCredential.parse_raw(response_json)
            verification = verify_registration_response(
                credential=credential,
                expected_challenge=base64url_to_bytes(challenge),
                expected_origin="https://debvisor.local",  # Should be configurable
                expected_rp_id="debvisor.local",
            )

            return WebAuthnCredential(
                credential_id=(
                    verification.credential_id.decode("utf-8")
                    if isinstance(verification.credential_id, bytes)
                    else verification.credential_id
                ),
                public_key=base64.b64encode(verification.credential_public_key).decode(
                    "utf-8"
                ),
                sign_count=verification.sign_count,
                created_at=datetime.now(timezone.utc),
                name="WebAuthn Key",
                is_primary=True,
            )
        except Exception as e:
            logger.error(f"WebAuthn registration verification failed: {e}")
            return None

    def generate_authentication_options(self, credential_ids: List[str]) -> Any:
        """
        Generate WebAuthn authentication options.

        Args:
            credential_ids: List of registered credential IDs

        Returns:
            Authentication options for client
        """
        if not self.available:
            raise RuntimeError("WebAuthn not available")

        from webauthn import generate_authentication_options
        from webauthn import base64url_to_bytes
        from webauthn import options_to_json

        # Convert string IDs back to bytes if needed, depending on library version
        # Modern webauthn library handles bytes for allow_credentials
        allow_credentials = []
        for cid in credential_ids:
            try:
                allow_credentials.append(base64url_to_bytes(cid))
            except Exception:
                # nosec B112 - Skip invalid credential IDs during authentication options generation
                continue

        options = generate_authentication_options(
            rp_id="debvisor.local",
            allow_credentials=allow_credentials,
        )

        return options_to_json(options)

    def verify_authentication_response(
        self,
        response_json: str,
        challenge: str,
        credential_public_key: str,
        credential_sign_count: int,
    ) -> Tuple[bool, int]:
        """
        Verify WebAuthn authentication response.

        Args:
            response_json: JSON response from client
            challenge: Original challenge
            credential_public_key: Stored public key (base64 encoded)
            credential_sign_count: Stored sign count

        Returns:
            (success, new_sign_count)
        """
        if not self.available:
            raise RuntimeError("WebAuthn not available")

        from webauthn import verify_authentication_response
        from webauthn.helpers.structs import AuthenticationCredential
        from webauthn import base64url_to_bytes

        try:
            credential = AuthenticationCredential.parse_raw(response_json)

            verification = verify_authentication_response(
                credential=credential,
                expected_challenge=base64url_to_bytes(challenge),
                expected_origin="https://debvisor.local",
                expected_rp_id="debvisor.local",
                credential_public_key=base64.b64decode(credential_public_key),
                credential_current_sign_count=credential_sign_count,
            )

            return True, verification.new_sign_count
        except Exception as e:
            logger.error(f"WebAuthn authentication verification failed: {e}")
            return False, credential_sign_count


class TwoFactorAuthManager:
    """
    Unified 2FA manager orchestrating all authentication methods.

    Includes rate limiting protection on the verify endpoint to prevent
    brute force attacks. Max 5 verification attempts per 5 minutes per IP.
    """

    def __init__(
        self,
        totp_config: Optional[TOTPConfig] = None,
        backup_config: Optional[BackupCodeConfig] = None,
    ):
        """
        Initialize 2FA manager.

        Args:
            totp_config: TOTP configuration
            backup_config: Backup code configuration
        """
        self.totp_manager = TOTPManager(totp_config)
        self.backup_manager = BackupCodeManager(backup_config)
        self.webauthn_manager = WebAuthnManager()
        self.rate_limiter = TwoFAVerificationRateLimiter()

    def initiate_enrollment(self, account_name: str, use_totp: bool = True) -> Dict[str, Any]:
        """
        Initiate 2FA enrollment for a user.

        Args:
            account_name: User account name
            use_totp: Whether to include TOTP enrollment

        Returns:
            Enrollment data with secrets and QR codes
        """
        enrollment_data: Dict[str, Any] = {
            "account_name": account_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Generate TOTP secret and QR code
        if use_totp:
            secret = self.totp_manager.generate_secret()
            totp_info = self.totp_manager.get_provisioning_info(secret, account_name)
            enrollment_data["totp"] = totp_info

        # Generate backup codes
        backup_codes = self.backup_manager.generate_codes()
        enrollment_data["backup_codes"] = backup_codes
        enrollment_data["backup_codes_display"] = (
            self.backup_manager.format_for_display(backup_codes)
        )

        # WebAuthn registration options (if available)
        if self.webauthn_manager.is_available():
            webauthn_options = self.webauthn_manager.generate_registration_options(
                user_id=account_name,
                user_name=account_name,
                user_display_name=account_name,
            )
            enrollment_data["webauthn_options"] = webauthn_options

        return enrollment_data

    def verify_2fa_method(
        self, method: str, credential: str, stored_secret: Optional[str] = None
    ) -> bool:
        """
        Verify 2FA using specified method.

        Args:
            method: 2FA method ('totp', 'backup', 'webauthn')
            credential: User-provided credential
            stored_secret: Stored secret for method (e.g., TOTP secret)

        Returns:
            True if verification succeeds, False otherwise

        Raises:
            ValueError: If invalid method or missing credentials
        """
        if method == "totp":
            if stored_secret is None:
                raise ValueError("TOTP secret required")
            return self.totp_manager.verify_token(stored_secret, credential)

        elif method == "backup":
            if stored_secret is None:
                raise ValueError("Backup code hash required")
            return self.backup_manager.verify_code(credential, stored_secret)

        elif method == "webauthn":
            # WebAuthn verification
            # stored_secret is expected to be a JSON string containing:
            # {
            #   "challenge": "...",
            #   "public_key": "...",
            #   "sign_count": 123
            # }
            if not stored_secret:
                raise ValueError("WebAuthn context required")

            import json

            try:
                context = json.loads(stored_secret)
                challenge = context.get("challenge")
                public_key = context.get("public_key")
                sign_count = context.get("sign_count", 0)

                if not challenge or not public_key:
                    raise ValueError("Invalid WebAuthn context")

                success, new_count = (
                    self.webauthn_manager.verify_authentication_response(
                        response_json=credential,
                        challenge=challenge,
                        credential_public_key=public_key,
                        credential_sign_count=sign_count,
                    )
                )

                # Note: In a real app, we need to update the sign_count in DB here
                # Since this method only returns bool, the caller needs to handle persistence
                # if we wanted to be strict about sign counts.
                return success
            except Exception as e:
                logger.error(f"WebAuthn verification error: {e}")
                return False

        else:
            raise ValueError(f"Unknown 2FA method: {method}")

    def verify_2fa_with_rate_limit(
        self,
        method: str,
        credential: str,
        stored_secret: Optional[str] = None,
        ip_address: str = "127.0.0.1",
        user_account: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify 2FA using specified method with rate limiting.

        This is the endpoint method that should be used in web handlers.
        It enforces rate limiting on verification attempts.

        Args:
            method: 2FA method ('totp', 'backup', 'webauthn')
            credential: User-provided credential
            stored_secret: Stored secret for method (e.g., TOTP secret)
            ip_address: Client IP address for rate limiting
            user_account: User account identifier for audit logging

        Returns:
            Tuple of (success, error_message)
            - If rate limited: (False, "Rate limited, try in X seconds")
            - If verification fails: (False, None)
            - If verification succeeds: (True, None)
        """
        # Check rate limit first
        is_limited, seconds_remaining = self.rate_limiter.is_rate_limited(ip_address)
        if is_limited:
            return False, (
                "2FA verification rate limited. "
                f"Try again in {seconds_remaining} seconds."
            )

        # Attempt verification
        try:
            success = self.verify_2fa_method(method, credential, stored_secret)

            if success:
                # Clear attempt history on success
                self.rate_limiter.record_successful_attempt(ip_address)
                return True, None
            else:
                # Record failed attempt
                self.rate_limiter.record_failed_attempt(
                    ip_address, method, user_account
                )
                return False, None

        except ValueError:
            # Record failed attempt for invalid input
            self.rate_limiter.record_failed_attempt(ip_address, method, user_account)
            raise

    def get_rate_limiter_stats(self, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get rate limiter statistics.

        Args:
            ip_address: Optional IP to get specific stats for

        Returns:
            Statistics dictionary
        """
        return {
            "attempts": self.rate_limiter.get_attempt_count(ip_address or "unknown"),
            "audit_log": self.rate_limiter.get_audit_log(ip_address),
            "rate_limit_config": {
                "max_attempts": self.rate_limiter.MAX_ATTEMPTS,
                "window_seconds": self.rate_limiter.WINDOW_SECONDS,
                "lockout_seconds": self.rate_limiter.LOCKOUT_SECONDS,
            },
        }

    def get_enrollment_summary(self, enrollment_data: Dict[str, Any]) -> str:
        """
        Get human-readable enrollment summary.

        Args:
            enrollment_data: Enrollment data from initiate_enrollment()

        Returns:
            Formatted summary string
        """
        summary = "2FA Enrollment Summary\n"
        summary += f"Account: {enrollment_data['account_name']}\n"
        summary += f"Time: {enrollment_data['timestamp']}\n\n"

        if "totp" in enrollment_data:
            summary += "? TOTP configured\n"
            summary += f"  Secret: {enrollment_data['totp']['secret']}\n"

        if "webauthn_options" in enrollment_data:
            summary += "? WebAuthn available\n"

        if "backup_codes" in enrollment_data:
            summary += (
                f"? {len(enrollment_data['backup_codes'])} backup codes generated\n"
            )

        return summary
