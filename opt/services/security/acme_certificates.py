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


"""
ACME/Let's Encrypt Certificate Manager for DebVisor.

Provides automated SSL/TLS certificate management with:
- Let's Encrypt integration via ACME protocol
- Multiple challenge types (HTTP-01, DNS-01)
- Automatic renewal with configurable thresholds
- Certificate storage and rotation
- Multi-domain and wildcard support
- Integration with web servers (nginx, Apache)
- Certificate transparency logging
- OCSP stapling support

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import hashlib
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import subprocess

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class ChallengeType(Enum):
    """ACME challenge types."""

    HTTP_01 = "http-01"    # HTTP challenge
    DNS_01 = "dns-01"    # DNS challenge
    TLS_ALPN_01 = "tls-alpn-01"    # TLS-ALPN challenge


class CertificateStatus(Enum):
    """Certificate status."""

    PENDING = "pending"
    VALID = "valid"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    REVOKED = "revoked"
    ERROR = "error"


class ACMEProvider(Enum):
    """ACME certificate providers."""

    LETSENCRYPT = "letsencrypt"
    LETSENCRYPT_STAGING = "letsencrypt_staging"
    ZEROSSL = "zerossl"
    BUYPASS = "buypass"
    GOOGLE = "google"


class DNSProvider(Enum):
    """DNS providers for DNS-01 challenges."""

    CLOUDFLARE = "cloudflare"
    ROUTE53 = "route53"
    DIGITALOCEAN = "digitalocean"
    GOOGLE_CLOUD = "google_cloud"
    AZURE = "azure"
    MANUAL = "manual"


# ACME Directory URLs
ACME_DIRECTORIES = {
    ACMEProvider.LETSENCRYPT: "https://acme-v02.api.letsencrypt.org/directory",
    ACMEProvider.LETSENCRYPT_STAGING: "https://acme-staging-v02.api.letsencrypt.org/directory",
    ACMEProvider.ZEROSSL: "https://acme.zerossl.com/v2/DV90",
    ACMEProvider.BUYPASS: "https://api.buypass.com/acme/directory",
    ACMEProvider.GOOGLE: "https://dv.acme-v02.api.pki.goog/directory",
}


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ACMEConfig:
    """ACME client configuration."""

    provider: ACMEProvider = ACMEProvider.LETSENCRYPT
    email: str = ""
    agree_tos: bool = True
    key_type: str = "ec256"    # rsa2048, rsa4096, ec256, ec384
    challenge_type: ChallengeType = ChallengeType.HTTP_01

    # DNS challenge settings
    dns_provider: DNSProvider = DNSProvider.MANUAL
    dns_credentials: Dict[str, str] = field(default_factory=dict)
    dns_propagation_wait: int = 60    # seconds

    # Renewal settings
    renewal_days: int = 30    # Renew when expires within N days
    renewal_check_interval: int = 86400    # Check every 24 hours

    # Paths
    cert_dir: str = "/etc/debvisor/ssl"
    account_dir: str = "/etc/debvisor/acme"
    webroot: str = "/var/www/acme-challenge"

    # Rate limiting
    max_certs_per_hour: int = 5
    max_renewals_per_day: int = 50


@dataclass
class Certificate:
    """Certificate record."""

    id: str
    domains: List[str]
    common_name: str
    status: CertificateStatus = CertificateStatus.PENDING
    provider: ACMEProvider = ACMEProvider.LETSENCRYPT

    # Paths
    cert_path: str = ""
    key_path: str = ""
    chain_path: str = ""
    fullchain_path: str = ""

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    last_renewed: Optional[datetime] = None

    # Metadata
    serial_number: str = ""
    fingerprint: str = ""
    issuer: str = ""

    # State
    renewal_attempts: int = 0
    last_error: str = ""

    @property
    def days_until_expiry(self) -> int:
        """Days until certificate expires."""
        if not self.expires_at:
            return 0
        delta = self.expires_at - datetime.now(timezone.utc)
        return max(0, delta.days)

    @property
    def is_valid(self) -> bool:
        """Check if certificate is currently valid."""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) < self.expires_at

    @property
    def needs_renewal(self) -> bool:
        """Check if certificate needs renewal."""
        return self.days_until_expiry <= 30

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "domains": self.domains,
            "common_name": self.common_name,
            "status": self.status.value,
            "provider": self.provider.value,
            "days_until_expiry": self.days_until_expiry,
            "is_valid": self.is_valid,
            "needs_renewal": self.needs_renewal,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "issuer": self.issuer,
            "fingerprint": self.fingerprint,
        }


@dataclass
class ChallengeRecord:
    """ACME challenge record."""

    domain: str
    challenge_type: ChallengeType
    token: str
    key_authorization: str
    status: str = "pending"    # pending, processing, valid, invalid
    validated_at: Optional[datetime] = None
    error: str = ""


# =============================================================================
# DNS Challenge Providers
# =============================================================================


class DNSChallengeProvider(ABC):
    """Abstract DNS challenge provider."""

    @abstractmethod
    async def create_record(self, domain: str, token: str, value: str) -> bool:
        """Create DNS TXT record for challenge."""
        pass

    @abstractmethod
    async def delete_record(self, domain: str, token: str) -> bool:
        """Delete DNS TXT record after challenge."""
        pass


class ManualDNSProvider(DNSChallengeProvider):
    """Manual DNS challenge provider."""

    def __init__(self, callback: Optional[Callable[[str, str, str], None]] = None):
        self.callback = callback
        self._records: Dict[str, str] = {}

    async def create_record(self, domain: str, token: str, value: str) -> bool:
        """Request manual DNS record creation."""
        record_name = f"_acme-challenge.{domain}"

        logger.info("Manual DNS challenge required:")
        logger.info(f"  Create TXT record: {record_name}")
        logger.info(f"  Value: {value}")

        self._records[record_name] = value

        if self.callback:
            self.callback("create", record_name, value)

        return True

    async def delete_record(self, domain: str, token: str) -> bool:
        """Request manual DNS record deletion."""
        record_name = f"_acme-challenge.{domain}"

        logger.info(f"DNS record can be removed: {record_name}")

        if record_name in self._records:
            del self._records[record_name]

        if self.callback:
            self.callback("delete", record_name, "")

        return True


class CloudflareDNSProvider(DNSChallengeProvider):
    """Cloudflare DNS challenge provider."""

    def __init__(self, api_token: str, zone_id: Optional[str] = None):
        self.api_token = api_token
        self.zone_id = zone_id
        self._record_ids: Dict[str, str] = {}

    async def create_record(self, domain: str, token: str, value: str) -> bool:
        """Create Cloudflare DNS TXT record."""
        try:
            import aiohttp

            record_name = f"_acme-challenge.{domain}"

            async with aiohttp.ClientSession() as session:
            # Get zone ID if not provided
                zone_id = self.zone_id
                if not zone_id:
                    zone_id = await self._get_zone_id(session, domain)

                if not zone_id:
                    logger.error(f"Could not find zone for {domain}")
                    return False

                # Create TXT record
                url = (
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
                )
                headers = {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                }
                data = {
                    "type": "TXT",
                    "name": record_name,
                    "content": value,
                    "ttl": 120,
                }

                async with session.post(url, headers=headers, json=data) as resp:
                    result = await resp.json()

                    if result.get("success"):
                        self._record_ids[record_name] = result["result"]["id"]
                        logger.info(f"Created Cloudflare DNS record: {record_name}")
                        return True
                    else:
                        logger.error(f"Cloudflare API error: {result.get('errors')}")
                        return False

        except ImportError:
            logger.error("aiohttp required for Cloudflare DNS provider")
            return False
        except Exception as e:
            logger.error(f"Failed to create Cloudflare record: {e}")
            return False

    async def delete_record(self, domain: str, token: str) -> bool:
        """Delete Cloudflare DNS TXT record."""
        try:
            import aiohttp

            record_name = f"_acme-challenge.{domain}"
            record_id = self._record_ids.get(record_name)

            if not record_id:
                return True

            async with aiohttp.ClientSession() as session:
                zone_id = self.zone_id or await self._get_zone_id(session, domain)

                url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
                headers = {"Authorization": f"Bearer {self.api_token}"}

                async with session.delete(url, headers=headers) as resp:
                    result = await resp.json()

                    if result.get("success"):
                        del self._record_ids[record_name]
                        logger.info(f"Deleted Cloudflare DNS record: {record_name}")
                        return True

            return False

        except Exception as e:
            logger.error(f"Failed to delete Cloudflare record: {e}")
            return False

    async def _get_zone_id(self, session: Any, domain: str) -> Optional[str]:
        """Get Cloudflare zone ID for domain."""
        # Extract root domain
        parts = domain.split(".")
        if len(parts) > 2:
            root_domain = ".".join(parts[-2:])
        else:
            root_domain = domain

        url = f"https://api.cloudflare.com/client/v4/zones?name={root_domain}"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        async with session.get(url, headers=headers) as resp:
            result = await resp.json()

            if result.get("success") and result.get("result"):
                return str(result["result"][0]["id"])

        return None


# =============================================================================
# ACME Certificate Manager
# =============================================================================


class ACMECertificateManager:
    """
    Enterprise ACME certificate manager.

    Features:
    - Let's Encrypt and other ACME providers
    - HTTP-01 and DNS-01 challenges
    - Automatic renewal
    - Multi-domain certificates
    - Wildcard support (DNS-01)
    - Certificate storage management
    """

    def __init__(self, config: Optional[ACMEConfig] = None):
        self.config = config or ACMEConfig()
        self._certificates: Dict[str, Certificate] = {}
        self._dns_provider: Optional[DNSChallengeProvider] = None
        self._lock = threading.Lock()
        self._renewal_task: Optional[asyncio.Task[None]] = None
        self._running = False

        # Ensure directories exist
        self._ensure_directories()

        # Initialize DNS provider
        self._init_dns_provider()

    def _ensure_directories(self) -> None:
        """Create required directories."""
        for path in [
            self.config.cert_dir,
            self.config.account_dir,
            self.config.webroot,
        ]:
            Path(path).mkdir(parents=True, exist_ok=True)

    def _init_dns_provider(self) -> None:
        """Initialize DNS challenge provider."""
        if self.config.dns_provider == DNSProvider.CLOUDFLARE:
            api_token = self.config.dns_credentials.get("api_token", "")
            zone_id = self.config.dns_credentials.get("zone_id")
            self._dns_provider = CloudflareDNSProvider(api_token, zone_id)
        else:
            self._dns_provider = ManualDNSProvider()

    # -------------------------------------------------------------------------
    # Certificate Operations
    # -------------------------------------------------------------------------

    async def request_certificate(
        self, domains: List[str], force: bool = False
    ) -> Tuple[bool, Certificate]:
        """Request new certificate for domains."""
        if not domains:
            raise ValueError("At least one domain required")

        common_name = domains[0]
        cert_id = hashlib.sha256(common_name.encode()).hexdigest()[:12]

        # Check for existing valid certificate
        existing = self._certificates.get(cert_id)
        if existing and existing.is_valid and not force:
            logger.info(f"Valid certificate exists for {common_name}")
            return True, existing

        # Create certificate record
        cert = Certificate(
            id=cert_id,
            domains=domains,
            common_name=common_name,
            provider=self.config.provider,
        )

        try:
        # Use certbot or acme.sh for actual certificate issuance
            success = await self._issue_certificate(cert)

            if success:
                cert.status = CertificateStatus.VALID
                cert.issued_at = datetime.now(timezone.utc)
                logger.info(f"Certificate issued for {common_name}")
            else:
                cert.status = CertificateStatus.ERROR

            with self._lock:
                self._certificates[cert_id] = cert

            return success, cert

        except Exception as e:
            cert.status = CertificateStatus.ERROR
            cert.last_error = str(e)
            logger.error(f"Certificate request failed for {common_name}: {e}")
            return False, cert

    async def _issue_certificate(self, cert: Certificate) -> bool:
        """Issue certificate using certbot."""
        try:
        # Build certbot command
            cmd = [
                "certbot",
                "certonly",
                "--non-interactive",
                "--agree-tos",
                "-m",
                self.config.email,
            ]

            # Add provider directory
            directory = ACME_DIRECTORIES.get(self.config.provider)
            if directory and self.config.provider != ACMEProvider.LETSENCRYPT:
                cmd.extend(["--server", directory])

            # Add challenge type
            if self.config.challenge_type == ChallengeType.HTTP_01:
                cmd.extend(
                    [
                        "--webroot",
                        "-w",
                        self.config.webroot,
                    ]
                )
            elif self.config.challenge_type == ChallengeType.DNS_01:
                if self.config.dns_provider == DNSProvider.CLOUDFLARE:
                    cmd.extend(
                        [
                            "--dns-cloudflare",
                            "--dns-cloudflare-credentials",
                            str(Path(self.config.account_dir) / "cloudflare.ini"),
                        ]
                    )
                else:
                    cmd.extend(["--manual", "--preferred-challenges", "dns"])

            # Add domains
            for domain in cert.domains:
                cmd.extend(["-d", domain])

            # Set certificate path
            cert_name = cert.common_name.replace("*", "wildcard").replace(".", "_")
            cmd.extend(["--cert-name", cert_name])

            # Run certbot
            result = subprocess.run(
                cmd,    # nosec B603
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
            # Update certificate paths
                live_path = Path("/etc/letsencrypt/live") / cert_name
                cert.cert_path = str(live_path / "cert.pem")
                cert.key_path = str(live_path / "privkey.pem")
                cert.chain_path = str(live_path / "chain.pem")
                cert.fullchain_path = str(live_path / "fullchain.pem")

                # Read certificate info
                self._parse_certificate_info(cert)

                return True
            else:
                cert.last_error = result.stderr
                logger.error(f"Certbot failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            cert.last_error = "Certificate request timed out"
            return False
        except FileNotFoundError:
            logger.warning("Certbot not found, using fallback")
            return await self._issue_certificate_fallback(cert)
        except Exception as e:
            cert.last_error = str(e)
            return False

    async def _issue_certificate_fallback(self, cert: Certificate) -> bool:
        """Fallback certificate issuance (generates self-signed for testing)."""
        logger.warning("Using self-signed certificate as fallback")

        cert_dir = Path(self.config.cert_dir) / cert.common_name.replace(
            "*", "wildcard"
        )
        cert_dir.mkdir(parents=True, exist_ok=True)

        key_path = cert_dir / "privkey.pem"
        cert_path = cert_dir / "cert.pem"

        # Generate self-signed certificate with OpenSSL
        cmd = [
            "/usr/bin/openssl",
            "req",
            "-x509",
            "-newkey",
            "ec",
            "-pkeyopt",
            "ec_paramgen_curve:prime256v1",
            "-keyout",
            str(key_path),
            "-out",
            str(cert_path),
            "-days",
            "90",
            "-nodes",
            "-subj",
            f"/CN={cert.common_name}",
        ]

        # Add SANs
        san_ext = ", ".join([f"DNS:{d}" for d in cert.domains])
        cmd.extend(["-addext", f"subjectAltName={san_ext}"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)    # nosec B603

            if result.returncode == 0:
                cert.cert_path = str(cert_path)
                cert.key_path = str(key_path)
                cert.fullchain_path = str(cert_path)
                cert.expires_at = datetime.now(timezone.utc) + timedelta(days=90)
                cert.issuer = "Self-Signed"
                return True

            return False

        except Exception as e:
            logger.error(f"Fallback certificate generation failed: {e}")
            return False

    def _parse_certificate_info(self, cert: Certificate) -> None:
        """Parse certificate information from file."""
        try:
            result = subprocess.run(
                [
                    "/usr/bin/openssl",
                    "x509",
                    "-in",
                    cert.cert_path,
                    "-noout",    # nosec B603
                    "-dates",
                    "-issuer",
                    "-fingerprint",
                    "-serial",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                output = result.stdout

                # Parse expiry
                for line in output.splitlines():
                    if "notAfter=" in line:
                        date_str = line.split("=")[1]
                        cert.expires_at = datetime.strptime(
                            date_str, "%b %d %H:%M:%S %Y %Z"
                        ).replace(tzinfo=timezone.utc)
                    elif "issuer=" in line:
                        cert.issuer = line.split("=", 1)[1]
                    elif "SHA256 Fingerprint=" in line:
                        cert.fingerprint = line.split("=")[1].strip()
                    elif "serial=" in line:
                        cert.serial_number = line.split("=")[1].strip()

        except Exception as e:
            logger.error(f"Failed to parse certificate info: {e}")

    async def renew_certificate(self, cert_id: str) -> Tuple[bool, str]:
        """Renew an existing certificate."""
        cert = self._certificates.get(cert_id)
        if not cert:
            return False, "Certificate not found"

        cert.renewal_attempts += 1

        try:
        # Use certbot renew
            result = subprocess.run(
                [
                    "/usr/bin/certbot",
                    "renew",
                    "--cert-name",    # nosec B603
                    cert.common_name.replace("*", "wildcard").replace(".", "_"),
                    "--non-interactive",
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                cert.last_renewed = datetime.now(timezone.utc)
                cert.renewal_attempts = 0
                self._parse_certificate_info(cert)
                cert.status = CertificateStatus.VALID
                logger.info(f"Renewed certificate for {cert.common_name}")
                return True, "Certificate renewed successfully"
            else:
                cert.last_error = result.stderr
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Renewal timed out"
        except FileNotFoundError:
        # Fallback: request new certificate
            success, _ = await self.request_certificate(cert.domains, force=True)
            return success, "Renewed via re-issuance"
        except Exception as e:
            cert.last_error = str(e)
            return False, str(e)

    async def revoke_certificate(
        self, cert_id: str, reason: str = ""
    ) -> Tuple[bool, str]:
        """Revoke a certificate."""
        cert = self._certificates.get(cert_id)
        if not cert:
            return False, "Certificate not found"

        try:
            result = subprocess.run(
                [
                    "/usr/bin/certbot",
                    "revoke",    # nosec B603
                    "--cert-path",
                    cert.cert_path,
                    "--non-interactive",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                cert.status = CertificateStatus.REVOKED
                logger.info(f"Revoked certificate for {cert.common_name}")
                return True, "Certificate revoked"
            else:
                return False, result.stderr

        except Exception as e:
            return False, str(e)

    # -------------------------------------------------------------------------
    # Certificate Management
    # -------------------------------------------------------------------------

    def get_certificate(self, cert_id: str) -> Optional[Certificate]:
        """Get certificate by ID."""
        return self._certificates.get(cert_id)

    def get_certificate_by_domain(self, domain: str) -> Optional[Certificate]:
        """Get certificate for domain."""
        for cert in self._certificates.values():
            if domain in cert.domains:
                return cert
        return None

    def list_certificates(self) -> List[Certificate]:
        """List all certificates."""
        return list(self._certificates.values())

    def get_expiring_certificates(self, days: int = 30) -> List[Certificate]:
        """Get certificates expiring within N days."""
        return [
            cert
            for cert in self._certificates.values()
            if cert.days_until_expiry <= days
            and cert.status != CertificateStatus.REVOKED
        ]

    def delete_certificate(self, cert_id: str) -> bool:
        """Delete certificate and files."""
        cert = self._certificates.get(cert_id)
        if not cert:
            return False

        # Delete files
        for path in [
            cert.cert_path,
            cert.key_path,
            cert.chain_path,
            cert.fullchain_path,
        ]:
            if path and Path(path).exists():
                try:
                    Path(path).unlink()
                except Exception as e:
                    logger.error(f"Failed to delete {path}: {e}")

        del self._certificates[cert_id]
        logger.info(f"Deleted certificate {cert_id}")
        return True

    # -------------------------------------------------------------------------
    # Auto-Renewal
    # -------------------------------------------------------------------------

    async def start_auto_renewal(self) -> None:
        """Start automatic renewal background task."""
        if self._running:
            return

        self._running = True
        self._renewal_task = asyncio.create_task(self._renewal_loop())
        logger.info("Started certificate auto-renewal")

    async def stop_auto_renewal(self) -> None:
        """Stop automatic renewal."""
        self._running = False
        if self._renewal_task:
            self._renewal_task.cancel()
            try:
                await self._renewal_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped certificate auto-renewal")

    async def _renewal_loop(self) -> None:
        """Background renewal loop."""
        while self._running:
            try:
                expiring = self.get_expiring_certificates(self.config.renewal_days)

                for cert in expiring:
                    if cert.renewal_attempts < 3:
                        logger.info(f"Auto-renewing certificate for {cert.common_name}")
                        await self.renew_certificate(cert.id)
                    else:
                        logger.error(
                            f"Too many renewal attempts for {cert.common_name}"
                        )

                await asyncio.sleep(self.config.renewal_check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Renewal loop error: {e}")
                await asyncio.sleep(3600)    # Retry in 1 hour

    # -------------------------------------------------------------------------
    # Web Server Integration
    # -------------------------------------------------------------------------

    def generate_nginx_config(
        self, cert: Certificate, server_name: Optional[str] = None
    ) -> str:
        """Generate nginx SSL configuration snippet."""
        server_name = server_name or cert.common_name

        return """    # SSL configuration for {server_name}
# Generated by DebVisor ACME Manager

ssl_certificate {cert.fullchain_path};
ssl_certificate_key {cert.key_path};

ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;    # noqa: E501
ssl_prefer_server_ciphers off;

ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;

# HSTS
add_header Strict-Transport-Security "max-age=63072000" always;
"""

    def generate_apache_config(self, cert: Certificate) -> str:
        """Generate Apache SSL configuration snippet."""
        return """    # SSL configuration for {cert.common_name}
# Generated by DebVisor ACME Manager

SSLEngine on
SSLCertificateFile {cert.cert_path}
SSLCertificateKeyFile {cert.key_path}
SSLCertificateChainFile {cert.chain_path}

SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384    # noqa: E501
SSLHonorCipherOrder off

SSLUseStapling On
SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"

Header always set Strict-Transport-Security "max-age=63072000"
"""

    # -------------------------------------------------------------------------
    # HTTP Challenge Handler
    # -------------------------------------------------------------------------

    def setup_http_challenge(self) -> None:
        """Setup HTTP challenge directory and nginx config."""
        webroot = Path(self.config.webroot) / ".well-known" / "acme-challenge"
        webroot.mkdir(parents=True, exist_ok=True)

        # Create nginx location block
        nginx_conf = """    # ACME HTTP-01 challenge location
location /.well-known/acme-challenge/ {{
    root {self.config.webroot};
    allow all;
}}
"""

        logger.info(f"HTTP challenge directory: {webroot}")
        logger.info("Add this to your nginx config:")
        logger.info(nginx_conf)

    # -------------------------------------------------------------------------
    # Status & Reporting
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get certificate manager status."""
        certs = list(self._certificates.values())

        return {
            "provider": self.config.provider.value,
            "challenge_type": self.config.challenge_type.value,
            "auto_renewal": self._running,
            "renewal_threshold_days": self.config.renewal_days,
            "certificates": {
                "total": len(certs),
                "valid": len([c for c in certs if c.status == CertificateStatus.VALID]),
                "expiring": len([c for c in certs if c.needs_renewal]),
                "expired": len(
                    [c for c in certs if c.status == CertificateStatus.EXPIRED]
                ),
                "error": len([c for c in certs if c.status == CertificateStatus.ERROR]),
            },
        }


# =============================================================================
# Flask Integration
# =============================================================================


def create_acme_blueprint(manager: ACMECertificateManager) -> Any:
    """Create Flask blueprint for ACME API."""
    try:
        from flask import Blueprint, request, jsonify, Response
        from flask_login import current_user
        from opt.web.panel.rbac import require_permission, Resource, Action
        from opt.web.panel.models.audit_log import AuditLog

        bp = Blueprint("acme", __name__, url_prefix="/api/acme")

        @bp.route("/status", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def status() -> Response:
            """Get ACME manager status."""
            return jsonify(manager.get_status())

        @bp.route("/certificates", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def list_certs() -> Response:
            """List all certificates."""
            return jsonify(
                {"certificates": [c.to_dict() for c in manager.list_certificates()]}
            )

        @bp.route("/certificates/<cert_id>", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def get_cert(cert_id: str) -> Tuple[Response, int]:
            """Get certificate details."""
            cert = manager.get_certificate(cert_id)
            if not cert:
                return jsonify({"error": "Certificate not found"}), 404
            return jsonify(cert.to_dict()), 200

        @bp.route("/certificates", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.CREATE)
        async def request_cert() -> Tuple[Response, int]:
            """Request new certificate."""
            data = request.get_json() or {}
            domains = data.get("domains", [])

            if not domains:
                return jsonify({"error": "domains required"}), 400

            success, cert = await manager.request_certificate(
                domains, force=data.get("force", False)
            )

            if success and cert:
                AuditLog.log_operation(
                    user_id=current_user.id,
                    operation="create",
                    resource_type="system",
                    action="acme_cert_request",
                    status="success",
                    request_data={"domains": domains, "force": data.get("force", False)},
                    ip_address=request.remote_addr,
                )
                return jsonify(cert.to_dict()), 201
            return jsonify({"error": cert.last_error if cert else "Unknown error"}), 400

        @bp.route("/certificates/<cert_id>/renew", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        async def renew_cert(cert_id: str) -> Tuple[Response, int]:
            """Renew certificate."""
            success, message = await manager.renew_certificate(cert_id)

            if success:
                AuditLog.log_operation(
                    user_id=current_user.id,
                    operation="update",
                    resource_type="system",
                    action="acme_cert_renew",
                    status="success",
                    request_data={"cert_id": cert_id},
                    ip_address=request.remote_addr,
                )
                return jsonify({"status": "renewed", "message": message}), 200
            return jsonify({"error": message}), 400

        @bp.route("/certificates/<cert_id>/revoke", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        async def revoke_cert(cert_id: str) -> Tuple[Response, int]:
            """Revoke certificate."""
            data = request.get_json() or {}
            reason = data.get("reason", "")
            success, message = await manager.revoke_certificate(cert_id, reason)

            if success:
                AuditLog.log_operation(
                    user_id=current_user.id,
                    operation="update",
                    resource_type="system",
                    action="acme_cert_revoke",
                    status="success",
                    request_data={"cert_id": cert_id, "reason": reason},
                    ip_address=request.remote_addr,
                )
                return jsonify({"status": "revoked"}), 200
            return jsonify({"error": message}), 400

        @bp.route("/expiring", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def expiring_certs() -> Response:
            """Get expiring certificates."""
            days = request.args.get("days", 30, type=int)
            certs = manager.get_expiring_certificates(days)
            return jsonify(
                {
                    "certificates": [c.to_dict() for c in certs],
                    "count": len(certs),
                }
            )

        return bp

    except ImportError:
        logger.warning("Flask not available for ACME blueprint")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "ChallengeType",
    "CertificateStatus",
    "ACMEProvider",
    "DNSProvider",
    "ACMEConfig",
    "Certificate",
    "ChallengeRecord",
    "DNSChallengeProvider",
    "ManualDNSProvider",
    "CloudflareDNSProvider",
    "ACMECertificateManager",
    "create_acme_blueprint",
    "ACME_DIRECTORIES",
]
