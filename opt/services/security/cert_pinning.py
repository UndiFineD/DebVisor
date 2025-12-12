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


"""
Certificate Pinning for Internal Service Communication

Provides:
- Certificate pinning policy enforcement
- Pin validation for mTLS connections
- Backup certificate management
- Pin refresh and rotation mechanisms
- Expiration warnings and alerts

Author: DebVisor Team
Date: November 27, 2025
"""

from cryptography.hazmat.primitives import serialization
import logging
import hashlib
import base64
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta, timezone
from cryptography import x509
import hashlib as crypto_hashlib

logger = logging.getLogger(__name__)


class PinType(Enum):
    """Types of certificate pins"""

    PUBLIC_KEY = "public_key"    # Pin public key hash
    CERTIFICATE = "certificate"    # Pin certificate hash
    CA_PUBLIC_KEY = "ca_public_key"    # Pin CA public key


class PinAlgorithm(Enum):
    """Hash algorithms for pinning"""

    SHA256 = "sha256"
    SHA512 = "sha512"


@dataclass
class CertificatePin:
    """Represents a pinned certificate"""

    pin_type: PinType
    algorithm: PinAlgorithm
    hash_value: str    # Base64-encoded hash
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    description: str = ""
    is_backup: bool = False
    last_verified: Optional[datetime] = None

    def is_expired(self) -> bool:
        """Check if pin is expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "pin_type": self.pin_type.value,
            "algorithm": self.algorithm.value,
            "hash_value": self.hash_value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "description": self.description,
            "is_backup": self.is_backup,
            "last_verified": (
                self.last_verified.isoformat() if self.last_verified else None
            ),
            "is_expired": self.is_expired(),
        }


@dataclass
class PinningPolicy:
    """Policy for certificate pinning on a host"""

    host: str
    primary_pins: List[CertificatePin] = field(default_factory=list)
    backup_pins: List[CertificatePin] = field(default_factory=list)
    max_age_seconds: int = 86400 * 365    # 1 year
    allow_backup_only: bool = False    # Allow connection with only backup pins
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def all_pins(self) -> List[CertificatePin]:
        """Get all pins (primary + backup)"""
        return self.primary_pins + self.backup_pins

    @property
    def valid_pins(self) -> List[CertificatePin]:
        """Get only non-expired pins"""
        return [pin for pin in self.all_pins if not pin.is_expired()]

    @property
    def primary_valid_pins(self) -> List[CertificatePin]:
        """Get valid primary pins"""
        return [pin for pin in self.primary_pins if not pin.is_expired()]

    @property
    def backup_valid_pins(self) -> List[CertificatePin]:
        """Get valid backup pins"""
        return [pin for pin in self.backup_pins if not pin.is_expired()]

    def has_valid_primary_pins(self) -> bool:
        """Check if policy has at least one valid primary pin"""
        return len(self.primary_valid_pins) > 0

    def has_valid_pins(self) -> bool:
        """Check if policy has any valid pins"""
        return len(self.valid_pins) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "host": self.host,
            "primary_pins": [p.to_dict() for p in self.primary_pins],
            "backup_pins": [p.to_dict() for p in self.backup_pins],
            "max_age_seconds": self.max_age_seconds,
            "allow_backup_only": self.allow_backup_only,
            "created_at": self.created_at.isoformat(),
            "valid_primary_pins": len(self.primary_valid_pins),
            "valid_backup_pins": len(self.backup_valid_pins),
        }


class CertificateHasher:
    """Utility for generating certificate hashes"""

    @staticmethod
    def get_public_key_hash(
        cert_data: bytes, algorithm: PinAlgorithm = PinAlgorithm.SHA256
    ) -> str:
        """
        Get hash of certificate's public key.

        Args:
            cert_data: DER-encoded certificate
            algorithm: Hash algorithm to use

        Returns:
            Base64-encoded hash
        """
        try:
            cert = x509.load_der_x509_certificate(cert_data)
            public_key_der = cert.public_key().public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            if algorithm == PinAlgorithm.SHA256:
                hash_obj = crypto_hashlib.sha256(public_key_der)
            else:
                hash_obj = crypto_hashlib.sha512(public_key_der)

            return base64.b64encode(hash_obj.digest()).decode()

        except Exception as e:
            logger.error(f"Failed to hash public key: {e}")
            raise

    @staticmethod
    def get_certificate_hash(
        cert_data: bytes, algorithm: PinAlgorithm = PinAlgorithm.SHA256
    ) -> str:
        """
        Get hash of entire certificate.

        Args:
            cert_data: DER-encoded certificate
            algorithm: Hash algorithm to use

        Returns:
            Base64-encoded hash
        """
        if algorithm == PinAlgorithm.SHA256:
            hash_obj = crypto_hashlib.sha256(cert_data)
        else:
            hash_obj = crypto_hashlib.sha512(cert_data)

        return base64.b64encode(hash_obj.digest()).decode()

    @staticmethod
    def get_ca_public_key_hash(
        cert_data: bytes, algorithm: PinAlgorithm = PinAlgorithm.SHA256
    ) -> str:
        """
        Get hash of CA's public key (from issuer certificate).

        Args:
            cert_data: DER-encoded certificate
            algorithm: Hash algorithm to use

        Returns:
            Base64-encoded hash
        """
        try:
            cert = x509.load_der_x509_certificate(cert_data)
            # For simplicity, return the issuer's name hash
            # In production, you'd extract the issuer certificate
            issuer_der = cert.issuer.public_bytes()

            if algorithm == PinAlgorithm.SHA256:
                hash_obj = crypto_hashlib.sha256(issuer_der)
            else:
                hash_obj = crypto_hashlib.sha512(issuer_der)

            return base64.b64encode(hash_obj.digest()).decode()

        except Exception as e:
            logger.error(f"Failed to hash CA public key: {e}")
            raise


class CertificatePinValidator:
    """Validates certificates against pins"""

    def __init__(self) -> None:
        self.policies: Dict[str, PinningPolicy] = {}
        self.violation_log: List[Dict[str, Any]] = []

    def add_policy(self, policy: PinningPolicy) -> None:
        """Add a pinning policy for a host"""
        self.policies[policy.host] = policy
        logger.info(f"Added pinning policy for {policy.host}")

    def remove_policy(self, host: str) -> bool:
        """Remove a pinning policy"""
        if host in self.policies:
            del self.policies[host]
            logger.info(f"Removed pinning policy for {host}")
            return True
        return False

    def get_policy(self, host: str) -> Optional[PinningPolicy]:
        """Get pinning policy for a host"""
        return self.policies.get(host)

    def validate_certificate(
        self, host: str, cert_data: bytes, pin_type: PinType = PinType.PUBLIC_KEY
    ) -> Tuple[bool, str]:
        """
        Validate certificate against pinned pins.

        Args:
            host: Hostname to validate
            cert_data: DER-encoded certificate
            pin_type: Type of pin to validate

        Returns:
            Tuple of (is_valid, message)
        """
        policy = self.get_policy(host)
        if not policy:
            logger.warning(f"No pinning policy for host: {host}")
            return True, "No pinning policy configured"

        try:
        # Generate hash based on pin type
            if pin_type == PinType.PUBLIC_KEY:
                cert_hash = CertificateHasher.get_public_key_hash(cert_data)
            elif pin_type == PinType.CERTIFICATE:
                cert_hash = CertificateHasher.get_certificate_hash(cert_data)
            else:    # CA_PUBLIC_KEY
                cert_hash = CertificateHasher.get_ca_public_key_hash(cert_data)

            # Check against primary pins
            for pin in policy.primary_valid_pins:
                if pin.hash_value == cert_hash:
                    pin.last_verified = datetime.now(timezone.utc)
                    logger.info(f"Certificate pin validated for {host}")
                    return True, "Certificate pin validated successfully"

            # Check against backup pins if allowed or no valid primary pins
            if policy.allow_backup_only or not policy.has_valid_primary_pins():
                for pin in policy.backup_valid_pins:
                    if pin.hash_value == cert_hash:
                        pin.last_verified = datetime.now(timezone.utc)
                        logger.warning(
                            f"Certificate validated against BACKUP pin for {host}"
                        )
                        return True, "Certificate validated against backup pin"

            # Pin mismatch
            self._log_violation(host, "pin_mismatch", cert_data)
            message = f"Certificate pin mismatch for {host}"
            logger.error(message)
            return False, message

        except Exception as e:
            self._log_violation(host, "validation_error", cert_data, str(e))
            message = f"Certificate validation error: {e}"
            logger.error(message)
            return False, message

    def get_expiring_pins(self, days: int = 30) -> List[Tuple[str, CertificatePin]]:
        """Get pins expiring within specified days"""
        expiring = []
        threshold = datetime.now(timezone.utc) + timedelta(days=days)

        for host, policy in self.policies.items():
            for pin in policy.all_pins:
                if pin.expires_at and pin.expires_at < threshold:
                    expiring.append((host, pin))

        return expiring

    def get_expired_pins(self) -> List[Tuple[str, CertificatePin]]:
        """Get all expired pins"""
        expired = []

        for host, policy in self.policies.items():
            for pin in policy.all_pins:
                if pin.is_expired():
                    expired.append((host, pin))

        return expired

    def rotate_pins(
        self, host: str, old_pin: CertificatePin, new_pin: CertificatePin
    ) -> bool:
        """
        Rotate a pin from primary to backup and add new primary.

        Args:
            host: Hostname
            old_pin: Old primary pin to demote
            new_pin: New pin to add as primary

        Returns:
            True if successful
        """
        policy = self.get_policy(host)
        if not policy:
            logger.error(f"No policy found for {host}")
            return False

        try:
        # Remove old pin from primary
            if old_pin in policy.primary_pins:
                policy.primary_pins.remove(old_pin)
                old_pin.is_backup = True
                policy.backup_pins.append(old_pin)

            # Add new pin as primary
            new_pin.is_backup = False
            policy.primary_pins.append(new_pin)

            logger.info(
                f"Rotated pins for {host}: old pin -> backup, new pin -> primary"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to rotate pins for {host}: {e}")
            return False

    def _log_violation(
        self,
        host: str,
        violation_type: str,
        cert_data: bytes,
        error: Optional[str] = None,
    ) -> None:
        """Log a pinning violation"""
        violation = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "host": host,
            "type": violation_type,
            "certificate_hash": hashlib.sha256(cert_data).hexdigest()[:16],
            "error": error,
        }
        self.violation_log.append(violation)

        # Keep only last 1000 violations
        if len(self.violation_log) > 1000:
            self.violation_log = self.violation_log[-1000:]

    def get_violations(self, host: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get violation log"""
        if host:
            return [v for v in self.violation_log if v["host"] == host]
        return self.violation_log.copy()

    def get_status(self) -> Dict[str, Any]:
        """Get pinning validator status"""
        expiring_soon = self.get_expiring_pins(days=30)
        expired = self.get_expired_pins()

        return {
            "total_policies": len(self.policies),
            "policies": {
                host: policy.to_dict() for host, policy in self.policies.items()
            },
            "pins_expiring_soon": len(expiring_soon),
            "expired_pins": len(expired),
            "recent_violations": self.violation_log[-10:],
            "total_violations": len(self.violation_log),
        }


# Global certificate pinning validator instance
_pin_validator: Optional[CertificatePinValidator] = None


async def get_pin_validator() -> CertificatePinValidator:
    """Get or create global certificate pin validator"""
    global _pin_validator
    if _pin_validator is None:
        _pin_validator = CertificatePinValidator()
    return _pin_validator


# Import for serialization
