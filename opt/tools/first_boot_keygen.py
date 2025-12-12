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

"""
First-Boot Key Generation Tool for DebVisor

Generates essential cryptographic keys on the first boot:
1. SSH Host Keys (if missing)
2. Internal Certificate Authority (CA)
3. Service Certificates (RPC, Web Panel)
4. Service Identity Keys (JWT Secrets)

Usage:
    python3 first_boot_keygen.py [--force]
"""

from opt.cert_manager import CertificateAuthority, CertificateManager, CertConfig
import argparse
import logging
import os
import secrets
import subprocess
import sys
from pathlib import Path

# Add opt to path to import cert_manager
sys.path.append(str(Path(__file__).resolve().parents[2]))


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_ssh_keys() -> None:
    """Generate SSH host keys if they don't exist."""
    logger.info("Checking SSH host keys...")
    key_types = ["rsa", "ecdsa", "ed25519"]
    for ktype in key_types:
        key_path = Path(f"/etc/ssh/ssh_host_{ktype}_key")
        if not key_path.exists():
            logger.info(f"Generating SSH {ktype} host key...")
            try:
                subprocess.run(
                    ["/usr/bin/ssh-keygen", "-t", ktype, "-", str(key_path), "-N", ""],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )    # nosec B603 - Hardcoded command arguments
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to generate SSH {ktype} key: {e}")


def generate_pki() -> None:
    """Initialize Internal CA and issue service certificates."""
    logger.info("Initializing PKI...")

    ca_dir = "/etc/debvisor/pki/ca"
    cert_dir = "/etc/debvisor/pki/certs"

    ca = CertificateAuthority(ca_dir)
    mgr = CertificateManager(ca, cert_dir)

    # 1. Init CA
    if not ca.exists():
        logger.info("Creating Internal CA...")
        hostname = (
            subprocess.check_output(["/usr/bin/hostname"]).decode().strip()
        )    # nosec B603 - Hostname command is trusted
        ca.create(
            CertConfig(
                common_name=f"DebVisor Internal CA ({hostname})",
                organization="DebVisor Cluster",
            )
        )
    else:
        logger.info("Internal CA already exists.")

    # 2. Issue RPC Cert
    if not (Path(cert_dir) / "rpc.crt").exists():
        logger.info("Issuing RPC certificate...")
        mgr.issue_cert(
            "rpc",
            CertConfig(
                common_name="debvisor-rpc", sans=["localhost", "127.0.0.1", "::1"]
            ),
        )

    # 3. Issue Panel Cert
    if not (Path(cert_dir) / "panel.crt").exists():
        logger.info("Issuing Web Panel certificate...")
        mgr.issue_cert(
            "panel",
            CertConfig(
                common_name="debvisor-panel", sans=["localhost", "127.0.0.1", "::1"]
            ),
        )


def generate_secrets() -> None:
    """Generate shared secrets (JWT, etc)."""
    logger.info("Generating service secrets...")
    secrets_dir = Path("/etc/debvisor/secrets")
    secrets_dir.mkdir(parents=True, exist_ok=True)

    # JWT Secret
    jwt_path = secrets_dir / "jwt_secret"
    if not jwt_path.exists():
        logger.info("Generating JWT secret...")
        secret = secrets.token_urlsafe(64)
        with open(jwt_path, "w") as f:
            f.write(secret)
        os.chmod(jwt_path, 0o600)

    # RPC Auth Token (for internal comms)
    rpc_token_path = secrets_dir / "rpc_token"
    if not rpc_token_path.exists():
        logger.info("Generating RPC internal token...")
        token = secrets.token_hex(32)
        with open(rpc_token_path, "w") as f:
            f.write(token)
        os.chmod(rpc_token_path, 0o600)


def main() -> int:
    parser = argparse.ArgumentParser(description="DebVisor First-Boot Key Gen")
    parser.add_argument("--force", action="store_true", help="Force regeneration")
    parser.parse_args()

    if os.geteuid() != 0:  # type: ignore[attr-defined]
        logger.error("Must run as root.")
        return 1

    try:
        generate_ssh_keys()
        generate_pki()
        generate_secrets()
        logger.info("Key generation complete.")
    except Exception as e:
        logger.error(f"Key generation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
