"""
TLS certificate management for DebVisor RPC service.

Provides:
- Certificate loading and validation
- Expiration checking and warnings
- Rotation and renewal procedures
- Certificate chain verification
"""

import ssl
from datetime import datetime
from typing import Set
from dataclasses import field
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


class CertificateInfo:
    """Information about a certificate."""

    def __init__(
        self,
        path: str,
        cert_type: str = "server",    # 'server', 'client', 'ca'
        subject: Optional[str] = None,
        issuer: Optional[str] = None,
        valid_from: Optional[datetime] = None,
        valid_until: Optional[datetime] = None,
        serial_number: Optional[str] = None,
    ):
        self.path = path
        self.cert_type = cert_type
        self.subject = subject
        self.issuer = issuer
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.serial_number = serial_number

    @property
    def days_until_expiry(self) -> int:
        """Days until certificate expires."""
        if not self.valid_until:
            return -1
        delta = self.valid_until - datetime.now(timezone.utc)
        return delta.days

    @property
    def is_expired(self) -> bool:
        """Check if certificate is expired."""
        return self.days_until_expiry <= 0

    @property
    def expiry_warning_level(self) -> str:
        """Get warning level based on expiry."""
        days = self.days_until_expiry
        if days < 0:
            return "expired"
        elif days < 7:
            return "critical"
        elif days < 30:
            return "warning"
        elif days < 90:
            return "notice"
        else:
            return "ok"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "type": self.cert_type,
            "subject": self.subject,
            "issuer": self.issuer,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "serial_number": self.serial_number,
            "days_until_expiry": self.days_until_expiry,
            "is_expired": self.is_expired,
            "expiry_warning_level": self.expiry_warning_level,
        }


class CertificateManager:
    """Manage TLS certificates for the RPC service."""

    def __init__(
        self,
        server_cert_path: str,
        server_key_path: str,
        ca_cert_path: Optional[str] = None,
        client_cert_path: Optional[str] = None,
        client_key_path: Optional[str] = None,
    ):
        self.server_cert_path = server_cert_path
        self.server_key_path = server_key_path
        self.ca_cert_path = ca_cert_path
        self.client_cert_path = client_cert_path
        self.client_key_path = client_key_path
        self._certificates: Dict[str, CertificateInfo] = {}

    def verify_certificates_exist(self) -> bool:
        """Verify all required certificate files exist."""
        required_paths = [self.server_cert_path, self.server_key_path]

        if self.ca_cert_path:
            required_paths.append(self.ca_cert_path)

        missing = []
        for path in required_paths:
            if not Path(path).exists():
                missing.append(path)

        if missing:
            logger.error(f"Missing certificate files: {missing}")
            return False

        return True

    def load_certificate_info(
        self, cert_path: str, cert_type: str = "server"
    ) -> Optional[CertificateInfo]:
        """Load and parse certificate information."""
        if not Path(cert_path).exists():
            logger.error(f"Certificate not found: {cert_path}")
            return None

        try:
            # Use openssl to extract certificate details
            result = subprocess.run(
                [
                    "/usr/bin/openssl",
                    "x509",
                    "-in",
                    cert_path,
                    "-noout",
                    "-text",
                    "-dates",
                ],    # nosec B603
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode != 0:
                logger.error(
                    f"Failed to parse certificate {cert_path}: {result.stderr}"
                )
                return None

            output = result.stdout

            # Parse dates
            valid_from = self._parse_date_from_output(output, "notBefore=")
            valid_until = self._parse_date_from_output(output, "notAfter=")

            # Get subject
            subject = self._extract_field(output, "Subject:")
            issuer = self._extract_field(output, "Issuer:")
            serial = self._extract_field(output, "Serial Number:")

            info = CertificateInfo(
                path=cert_path,
                cert_type=cert_type,
                subject=subject,
                issuer=issuer,
                valid_from=valid_from,
                valid_until=valid_until,
                serial_number=serial,
            )

            self._certificates[cert_path] = info

            # Log warning if expiring soon
            if info.expiry_warning_level in ("critical", "expired"):
                logger.critical(
                    f"Certificate {cert_path} expiring in {info.days_until_expiry} days"
                )
            elif info.expiry_warning_level == "warning":
                logger.warning(
                    f"Certificate {cert_path} expiring in {info.days_until_expiry} days"
                )

            return info

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout parsing certificate {cert_path}")
            return None
        except Exception as e:
            logger.error(f"Error parsing certificate {cert_path}: {str(e)}")
            return None

    def _parse_date_from_output(self, output: str, prefix: str) -> Optional[datetime]:
        """Parse date from openssl output."""
        for line in output.split("\n"):
            if prefix in line:
                date_str = line.split(prefix)[1].strip()
                try:
                    return datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
                except BaseException:
                    try:
                        return datetime.strptime(date_str, "%b  %d %H:%M:%S %Y %Z")
                    except BaseException:
                        return None
        return None

    def _extract_field(self, output: str, field: str) -> Optional[str]:
        """Extract field from openssl output."""
        for line in output.split("\n"):
            if field in line:
                return line.split(field)[1].strip()
        return None

    def check_all_certificates(self) -> Dict[str, CertificateInfo]:
        """Check all configured certificates."""
        results = {}

        cert_paths = {
            "server": (self.server_cert_path, "server"),
            "ca": (self.ca_cert_path, "ca"),
            "client": (self.client_cert_path, "client"),
        }

        for name, (path, cert_type) in cert_paths.items():
            if path:
                info = self.load_certificate_info(path, cert_type)
                if info:
                    results[name] = info

        return results

    def create_ssl_context(
        self,
        purpose: str = "server",
        verify_mode: ssl.VerifyMode = ssl.CERT_REQUIRED,
        protocol: int = ssl.PROTOCOL_TLS_SERVER,
    ) -> Optional[ssl.SSLContext]:
        """Create SSL context for the service."""
        try:
            context = ssl.SSLContext(protocol)

            # Load server certificate and key
            context.load_cert_chain(
                certfile=self.server_cert_path,
                keyfile=self.server_key_path,
                password=None,
            )

            # Set certificate verification if CA is available
            if self.ca_cert_path and Path(self.ca_cert_path).exists():
                context.load_verify_locations(self.ca_cert_path)
                context.verify_mode = verify_mode

            # Set strong cipher suite
            context.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20")

            # Set minimum TLS version
            context.minimum_version = ssl.TLSVersion.TLSv1_3

            return context

        except Exception as e:
            logger.error(f"Failed to create SSL context: {str(e)}")
            return None

    def validate_certificate_chain(self) -> bool:
        """Validate certificate chain."""
        if not self.ca_cert_path:
            return False

        try:
            result = subprocess.run(
                [
                    "/usr/bin/openssl",
                    "verify",
                    "-CAfile",
                    self.ca_cert_path,
                    self.server_cert_path,
                ],    # nosec B603
                capture_output=True,
                text=True,
                timeout=5,
            )

            is_valid = result.returncode == 0

            if not is_valid:
                logger.error(f"Certificate chain validation failed: {result.stderr}")

            return is_valid

        except Exception as e:
            logger.error(f"Error validating certificate chain: {str(e)}")
            return False

    def get_certificate_renewal_reminder(self) -> Optional[str]:
        """Get certificate renewal reminder if needed."""
        certs = self.check_all_certificates()

        for name, info in certs.items():
            if info.expiry_warning_level == "critical":
                return (
                    f"Certificate '{name}' ({info.path}) expires in {info.days_until_expiry} days. "
                    "Renew immediately to prevent service disruption."
                )
            elif info.expiry_warning_level == "warning":
                return (
                    f"Certificate '{name}' ({info.path}) expires in {info.days_until_expiry} days. "
                    "Plan renewal within the next week."
                )

        return None
