#!/usr/bin/env python3
"""
Certificate Manager for DebVisor

Automates the management of internal Certificate Authorities (CA) and
service certificates. Handles rotation, issuance, and validation.

Features:
- Internal CA creation and management
- Service certificate issuance (signed by Internal CA)
- Automated rotation based on expiration threshold
- Service reload hooks
"""

import argparse

import datetime
import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class CertConfig:
    """Certificate configuration."""

    common_name: str
    country: str = "US"
    state: str = "State"
    locality: str = "City"
    organization: str = "DebVisor"
    validity_days: int = 365
    key_size: int = 2048
    sans: List[str] = None


class CertificateAuthority:
    """Manages the Internal CA."""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.ca_key_path = self.base_dir / "ca.key"
        self.ca_cert_path = self.base_dir / "ca.crt"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def exists(self) -> bool:
        """Check if CA exists."""
        return self.ca_key_path.exists() and self.ca_cert_path.exists()

    def create(self, config: CertConfig) -> None:
        """Create a new Internal CA."""
        logger.info(f"Creating Internal CA: {config.common_name}")

        # Generate Private Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

        # Generate Self-Signed Root Certificate
        subject = issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, config.country),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, config.state),
                x509.NameAttribute(NameOID.LOCALITY_NAME, config.locality),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, config.organization),
                x509.NameAttribute(NameOID.COMMON_NAME, config.common_name),
            ]
        )

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
            .not_valid_after(
                + datetime.timedelta(days=3650)    # 10 years for CA
            )
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True,
            )
            .sign(private_key, hashes.SHA256())
        )

        # Save Key
        with open(self.ca_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Save Cert
        with open(self.ca_cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        logger.info("Internal CA created successfully.")

    def load_key(self) -> rsa.RSAPrivateKey:
        with open(self.ca_key_path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def load_cert(self) -> x509.Certificate:
        with open(self.ca_cert_path, "rb") as f:
            return x509.load_pem_x509_certificate(f.read())


class CertificateManager:
    """Manages service certificates."""

    def __init__(self, ca: CertificateAuthority, cert_dir: str):
        self.ca = ca
        self.cert_dir = Path(cert_dir)
        self.cert_dir.mkdir(parents=True, exist_ok=True)

    def issue_cert(self, name: str, config: CertConfig) -> Tuple[Path, Path]:
        """Issue a certificate signed by the Internal CA."""
        logger.info(f"Issuing certificate for {name} ({config.common_name})")

        key_path = self.cert_dir / f"{name}.key"
        cert_path = self.cert_dir / f"{name}.crt"

        # Generate Private Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=config.key_size,
        )

        # Generate CSR
        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(
                x509.Name(
                    [
                        x509.NameAttribute(NameOID.COUNTRY_NAME, config.country),
                        x509.NameAttribute(
                            NameOID.STATE_OR_PROVINCE_NAME, config.state
                        ),
                        x509.NameAttribute(NameOID.LOCALITY_NAME, config.locality),
                        x509.NameAttribute(
                            NameOID.ORGANIZATION_NAME, config.organization
                        ),
                        x509.NameAttribute(NameOID.COMMON_NAME, config.common_name),
                    ]
                )
            )
            .sign(private_key, hashes.SHA256())
        )

        # Sign with CA
        ca_key = self.ca.load_key()
        ca_cert = self.ca.load_cert()

        builder = (
            x509.CertificateBuilder()
            .subject_name(csr.subject)
            .issuer_name(ca_cert.subject)
            .public_key(csr.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_after(
                + datetime.timedelta(days=config.validity_days)
            )
        )

        if config.sans:
            san_list = [x509.DNSName(san) for san in config.sans]
            builder = builder.add_extension(
                x509.SubjectAlternativeName(san_list), critical=False
            )

        cert = builder.sign(ca_key, hashes.SHA256())

        # Save Key
        with open(key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Save Cert
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        logger.info(f"Certificate issued: {cert_path}")
        return key_path, cert_path

    def check_expiration(self, name: str) -> Optional[int]:
        """
        Check days until expiration.
        Returns None if cert doesn't exist.
        """
        cert_path = self.cert_dir / f"{name}.crt"
        if not cert_path.exists():
            return None

        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())

        remaining = cert.not_valid_after_utc - datetime.datetime.now(
        )
        return remaining.days

    def rotate_if_needed(
        self,
        name: str,
        config: CertConfig,
        threshold_days: int = 30,
        restart_cmd: Optional[str] = None,
    ) -> bool:
        """
        Rotate certificate if expiring soon.
        Returns True if rotated.
        """
        days_left = self.check_expiration(name)

        if days_left is None:
            logger.info(f"Certificate {name} missing. Issuing new one.")
            self.issue_cert(name, config)
            return True

        if days_left < threshold_days:
            logger.warning(f"Certificate {name} expires in {days_left} days. Rotating.")
            self.issue_cert(name, config)

            if restart_cmd:
                logger.info(f"Running restart command: {restart_cmd}")
                try:
                    subprocess.run(restart_cmd, shell=True, check=True)    # nosec B602
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to restart service: {e}")
            return True

        logger.info(f"Certificate {name} is valid for {days_left} days.")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="DebVisor Certificate Manager")
    parser.add_argument("--ca-dir", default="/etc/debvisor/pki/ca", help="CA directory")
    parser.add_argument(
        "--cert-dir", default="/etc/debvisor/pki/certs", help="Cert directory"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init CA
    init_parser = subparsers.add_parser("init-ca", help="Initialize Internal CA")
    init_parser.add_argument("--cn", default="DebVisor Internal CA", help="Common Name")

    # Issue Cert
    issue_parser = subparsers.add_parser("issue", help="Issue a certificate")
    issue_parser.add_argument("name", help="Certificate name (filename base)")
    issue_parser.add_argument("--cn", required=True, help="Common Name")
    issue_parser.add_argument("--sans", help="Comma-separated SANs")

    # Rotate
    rotate_parser = subparsers.add_parser("rotate", help="Rotate certificate if needed")
    rotate_parser.add_argument("name", help="Certificate name")
    rotate_parser.add_argument("--cn", required=True, help="Common Name")
    rotate_parser.add_argument(
        "--threshold", type=int, default=30, help="Days threshold"
    )
    rotate_parser.add_argument("--restart", help="Command to restart service")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    ca = CertificateAuthority(args.ca_dir)
    mgr = CertificateManager(ca, args.cert_dir)

    if args.command == "init-ca":
        if ca.exists():
            logger.info("CA already exists.")
            return 0
        ca.create(CertConfig(common_name=args.cn))

    elif args.command == "issue":
        if not ca.exists():
            logger.error("CA does not exist. Run init-ca first.")
            return 1
        sans = args.sans.split(", ") if args.sans else []
        mgr.issue_cert(args.name, CertConfig(common_name=args.cn, sans=sans))

    elif args.command == "rotate":
        if not ca.exists():
            logger.error("CA does not exist.")
            return 1
        mgr.rotate_if_needed(
            args.name,
            CertConfig(common_name=args.cn),
            threshold_days=args.threshold,
            restart_cmd=args.restart,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
