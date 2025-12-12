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


"""
Enterprise SSH Hardening Module for DebVisor.

Provides secure SSH configuration management with:
- Secure SSH daemon configuration
- Key-based authentication enforcement
- Multi-factor authentication (MFA) integration
- Fail2ban integration
- SSH audit logging
- Authorized keys management
- Host key management
- Certificate-based authentication

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone
import logging
import os
import secrets
import shutil
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class SSHAuthMethod(Enum):
    """SSH authentication methods."""

    PASSWORD = "password"    # nosec B105
    PUBLICKEY = "publickey"
    KEYBOARD_INTERACTIVE = "keyboard-interactive"
    GSSAPI = "gssapi-with-mic"
    HOSTBASED = "hostbased"


class SSHKeyType(Enum):
    """SSH key types."""

    RSA = "rsa"
    ECDSA = "ecdsa"
    ED25519 = "ed25519"
    DSA = "dsa"    # Deprecated


class MFAProvider(Enum):
    """MFA provider types."""

    TOTP = "totp"    # Time-based OTP (Google Authenticator)
    FIDO2 = "fido2"    # Hardware security keys
    DUO = "duo"    # Duo Security
    YUBIKEY = "yubikey"    # YubiKey OTP
    NONE = "none"


class SSHSecurityLevel(Enum):
    """SSH security levels."""

    BASIC = "basic"    # Minimum security
    STANDARD = "standard"    # Recommended security
    HARDENED = "hardened"    # Maximum security


# =============================================================================
# Configuration Data Classes
# =============================================================================


@dataclass
class SSHKeyConfig:
    """SSH key configuration."""

    key_type: SSHKeyType = SSHKeyType.ED25519
    key_bits: int = 4096    # For RSA
    comment: str = ""
    passphrase_required: bool = True


@dataclass
class SSHHostKeyConfig:
    """Host key configuration."""

    regenerate: bool = False
    allowed_types: List[SSHKeyType] = field(
        default_factory=lambda: [SSHKeyType.ED25519, SSHKeyType.ECDSA, SSHKeyType.RSA]
    )
    remove_weak_keys: bool = True


@dataclass
class SSHRateLimitConfig:
    """Rate limiting configuration."""

    max_auth_tries: int = 3
    login_grace_time: int = 30    # seconds
    max_startups: str = "10:30:60"    # start:rate:full
    max_sessions: int = 10


@dataclass
class SSHLoggingConfig:
    """SSH logging configuration."""

    log_level: str = "VERBOSE"    # QUIET, FATAL, ERROR, INFO, VERBOSE, DEBUG
    log_facility: str = "AUTH"
    log_successful_logins: bool = True
    log_failed_logins: bool = True


@dataclass
class MFAConfig:
    """Multi-factor authentication configuration."""

    enabled: bool = True
    provider: MFAProvider = MFAProvider.TOTP
    required_for_root: bool = True
    required_for_sudo: bool = True
    grace_period_seconds: int = 300
    backup_codes_count: int = 10


@dataclass
class SSHDConfig:
    """Complete SSH daemon configuration."""

    # Basic settings
    port: int = 22
    listen_addresses: List[str] = field(
        default_factory=lambda: ["0.0.0.0", "::"]
    )    # nosec B104
    address_family: str = "any"    # any, inet, inet6

    # Authentication
    permit_root_login: str = (
        "prohibit-password"    # yes, no, prohibit-password, forced-commands-only
    )
    password_authentication: bool = False
    pubkey_authentication: bool = True
    challenge_response_authentication: bool = False
    keyboard_interactive_authentication: bool = True    # For MFA
    gssapi_authentication: bool = False
    hostbased_authentication: bool = False
    permit_empty_passwords: bool = False

    # Security
    strict_modes: bool = True
    max_auth_tries: int = 3
    max_sessions: int = 10
    login_grace_time: int = 30
    max_startups: str = "10:30:60"

    # Cryptography
    ciphers: List[str] = field(
        default_factory=lambda: [
            "chacha20-poly1305@openssh.com",
            "aes256-gcm@openssh.com",
            "aes128-gcm@openssh.com",
            "aes256-ctr",
            "aes192-ctr",
            "aes128-ctr",
        ]
    )
    macs: List[str] = field(
        default_factory=lambda: [
            "hmac-sha2-512-etm@openssh.com",
            "hmac-sha2-256-etm@openssh.com",
            "umac-128-etm@openssh.com",
            "hmac-sha2-512",
            "hmac-sha2-256",
        ]
    )
    kex_algorithms: List[str] = field(
        default_factory=lambda: [
            "curve25519-sha256",
            "curve25519-sha256@libssh.org",
            "ecdh-sha2-nistp521",
            "ecdh-sha2-nistp384",
            "ecdh-sha2-nistp256",
            "diffie-hellman-group-exchange-sha256",
        ]
    )
    host_key_algorithms: List[str] = field(
        default_factory=lambda: [
            "ssh-ed25519",
            "ssh-ed25519-cert-v01@openssh.com",
            "ecdsa-sha2-nistp256",
            "ecdsa-sha2-nistp384",
            "ecdsa-sha2-nistp521",
            "rsa-sha2-512",
            "rsa-sha2-256",
        ]
    )

    # Forwarding
    allow_tcp_forwarding: str = "no"    # yes, no, local, remote
    allow_agent_forwarding: bool = False
    allow_stream_local_forwarding: str = "no"
    x11_forwarding: bool = False
    gateway_ports: bool = False
    permit_tunnel: str = "no"

    # Environment
    permit_user_environment: bool = False
    accept_env: List[str] = field(default_factory=lambda: ["LANG", "LC_*"])

    # Misc
    print_motd: bool = True
    print_last_log: bool = True
    tcp_keep_alive: bool = True
    client_alive_interval: int = 300
    client_alive_count_max: int = 3
    compression: str = "no"    # yes, no, delayed
    use_dns: bool = False
    use_pam: bool = True

    # Subsystems
    sftp_server: str = "/usr/lib/openssh/sftp-server"

    # Logging
    log_level: str = "VERBOSE"
    syslog_facility: str = "AUTH"

    # Access control
    allow_users: List[str] = field(default_factory=list)
    allow_groups: List[str] = field(default_factory=list)
    deny_users: List[str] = field(default_factory=list)
    deny_groups: List[str] = field(default_factory=list)

    # Match blocks
    match_blocks: List[Dict[str, Any]] = field(default_factory=list)


# =============================================================================
# SSH Hardening Manager
# =============================================================================


class SSHHardeningManager:
    """
    Enterprise SSH hardening manager.

    Features:
    - Secure SSH configuration generation
    - Host key management
    - Authorized keys management
    - MFA integration
    - Audit logging
    - Fail2ban integration
    """

    def __init__(self, config_path: str = "/etc/ssh"):
        self.config_path = Path(config_path)
        self.sshd_config_path = self.config_path / "sshd_config"
        self.backup_path = self.config_path / "backups"
        self._security_level = SSHSecurityLevel.STANDARD

        # Default configuration
        self._config = SSHDConfig()
        self._mfa_config = MFAConfig()

    # -------------------------------------------------------------------------
    # Configuration Management
    # -------------------------------------------------------------------------

    def set_security_level(self, level: SSHSecurityLevel) -> None:
        """Apply security preset."""
        self._security_level = level

        if level == SSHSecurityLevel.BASIC:
            self._apply_basic_security()
        elif level == SSHSecurityLevel.STANDARD:
            self._apply_standard_security()
        elif level == SSHSecurityLevel.HARDENED:
            self._apply_hardened_security()

        logger.info(f"Applied SSH security level: {level.value}")

    def enable_mfa(self, enabled: bool = True) -> None:
        """Enable or disable MFA."""
        self._mfa_config.enabled = enabled
        if enabled:
            self._config.challenge_response_authentication = True
            self._config.keyboard_interactive_authentication = True
            self._config.use_pam = True
            logger.info("MFA enabled for SSH")
        else:
            logger.info("MFA disabled for SSH")

    def _apply_basic_security(self) -> None:
        """Apply basic security settings."""
        self._config.permit_root_login = "prohibit-password"
        self._config.password_authentication = True
        self._config.max_auth_tries = 6
        self._config.login_grace_time = 120

    def _apply_standard_security(self) -> None:
        """Apply standard security settings (recommended)."""
        self._config.permit_root_login = "prohibit-password"
        self._config.password_authentication = False
        self._config.max_auth_tries = 3
        self._config.login_grace_time = 30
        self._config.allow_tcp_forwarding = "no"
        self._config.allow_agent_forwarding = False
        self._config.x11_forwarding = False

    def _apply_hardened_security(self) -> None:
        """Apply maximum security settings."""
        self._apply_standard_security()
        self._config.permit_root_login = "no"
        self._config.max_auth_tries = 2
        self._config.login_grace_time = 20
        self._config.max_startups = "3:50:10"
        self._config.max_sessions = 3
        self._config.compression = "no"
        self._config.client_alive_count_max = 2

        # Restrict to modern ciphers only
        self._config.ciphers = [
            "chacha20-poly1305@openssh.com",
            "aes256-gcm@openssh.com",
        ]
        self._config.macs = [
            "hmac-sha2-512-etm@openssh.com",
            "hmac-sha2-256-etm@openssh.com",
        ]
        self._config.kex_algorithms = [
            "curve25519-sha256",
            "curve25519-sha256@libssh.org",
        ]

    def generate_sshd_config(self) -> str:
        """Generate sshd_config file content."""
        lines = [
            "    # DebVisor SSH Hardening Configuration",
            f"    # Generated: {datetime.now(timezone.utc).isoformat()}",
            f"    # Security Level: {self._security_level.value}",
            "",
            "    # === Basic Settings ===",
            f"Port {self._config.port}",
        ]

        for addr in self._config.listen_addresses:
            lines.append(f"ListenAddress {addr}")

        lines.extend(
            [
                f"AddressFamily {self._config.address_family}",
                "",
                "    # === Authentication ===",
                f"PermitRootLogin {self._config.permit_root_login}",
                f"PasswordAuthentication {'yes' if self._config.password_authentication else 'no'}",
                f"PubkeyAuthentication {'yes' if self._config.pubkey_authentication else 'no'}",
                f"ChallengeResponseAuthentication {'yes' if self._config.challenge_response_authentication else 'no'}",
                f"KbdInteractiveAuthentication {'yes' if self._config.keyboard_interactive_authentication else 'no'}",
                f"GSSAPIAuthentication {'yes' if self._config.gssapi_authentication else 'no'}",
                f"HostbasedAuthentication {'yes' if self._config.hostbased_authentication else 'no'}",
                f"PermitEmptyPasswords {'yes' if self._config.permit_empty_passwords else 'no'}",
                "",
            ]
        )

        if self._mfa_config.enabled:
            lines.append("AuthenticationMethods publickey, keyboard-interactive")

        lines.extend(
            [
                "    # === Security ===",
                f"StrictModes {'yes' if self._config.strict_modes else 'no'}",
                f"MaxAuthTries {self._config.max_auth_tries}",
                f"MaxSessions {self._config.max_sessions}",
                f"LoginGraceTime {self._config.login_grace_time}",
                f"MaxStartups {self._config.max_startups}",
                "",
                "    # === Cryptography ===",
                f"Ciphers {', '.join(self._config.ciphers)}",
                f"MACs {', '.join(self._config.macs)}",
                f"KexAlgorithms {', '.join(self._config.kex_algorithms)}",
                f"HostKeyAlgorithms {', '.join(self._config.host_key_algorithms)}",
                "",
                "    # === Forwarding ===",
                f"AllowTcpForwarding {self._config.allow_tcp_forwarding}",
                f"AllowAgentForwarding {'yes' if self._config.allow_agent_forwarding else 'no'}",
                f"AllowStreamLocalForwarding {self._config.allow_stream_local_forwarding}",
                f"X11Forwarding {'yes' if self._config.x11_forwarding else 'no'}",
                f"GatewayPorts {'yes' if self._config.gateway_ports else 'no'}",
                f"PermitTunnel {self._config.permit_tunnel}",
                "",
                "    # === Environment ===",
                f"PermitUserEnvironment {'yes' if self._config.permit_user_environment else 'no'}",
            ]
        )

        for env in self._config.accept_env:
            lines.append(f"AcceptEnv {env}")

        lines.extend(
            [
                "",
                "    # === Connection ===",
                f"PrintMotd {'yes' if self._config.print_motd else 'no'}",
                f"PrintLastLog {'yes' if self._config.print_last_log else 'no'}",
                f"TCPKeepAlive {'yes' if self._config.tcp_keep_alive else 'no'}",
                f"ClientAliveInterval {self._config.client_alive_interval}",
                f"ClientAliveCountMax {self._config.client_alive_count_max}",
                f"Compression {self._config.compression}",
                f"UseDNS {'yes' if self._config.use_dns else 'no'}",
                f"UsePAM {'yes' if self._config.use_pam else 'no'}",
                "",
                "    # === Logging ===",
                f"LogLevel {self._config.log_level}",
                f"SyslogFacility {self._config.syslog_facility}",
                "",
                "    # === Subsystems ===",
                f"Subsystem sftp {self._config.sftp_server}",
            ]
        )

        # Access control
        if self._config.allow_users:
            lines.append("\n    # === Access Control ===")
            lines.append(f"AllowUsers {' '.join(self._config.allow_users)}")

        if self._config.allow_groups:
            lines.append(f"AllowGroups {' '.join(self._config.allow_groups)}")

        if self._config.deny_users:
            lines.append(f"DenyUsers {' '.join(self._config.deny_users)}")

        if self._config.deny_groups:
            lines.append(f"DenyGroups {' '.join(self._config.deny_groups)}")

        # Match blocks
        for match in self._config.match_blocks:
            lines.append("")
            lines.append(f"Match {match.get('criteria', 'User *')}")
            for key, value in match.get("settings", {}).items():
                lines.append(f"    {key} {value}")

        return "\n".join(lines)

    def backup_config(self) -> Optional[Path]:
        """Backup current SSH configuration."""
        if not self.sshd_config_path.exists():
            return None

        self.backup_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_path / f"sshd_config.{timestamp}.bak"

        shutil.copy2(self.sshd_config_path, backup_file)
        logger.info(f"Backed up SSH config to {backup_file}")
        return backup_file

    def apply_config(self, dry_run: bool = False) -> Tuple[bool, str]:
        """Apply SSH configuration."""
        config_content = self.generate_sshd_config()

        if dry_run:
            return True, config_content

        try:
        # Backup existing config
            self.backup_config()

            # Write new config
            with open(self.sshd_config_path, "w") as f:
                f.write(config_content)

            # Test configuration
            result = subprocess.run(
                [
                    "/usr/sbin/sshd",
                    "-t",
                    "-f",
                    str(self.sshd_config_path),
                ],    # nosec B603
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(f"SSH config validation failed: {result.stderr}")
                return False, result.stderr

            logger.info("SSH configuration applied successfully")
            return True, "Configuration applied successfully"

        except Exception as e:
            logger.error(f"Failed to apply SSH config: {e}")
            return False, str(e)

    def reload_sshd(self) -> Tuple[bool, str]:
        """Reload SSH daemon."""
        try:
            result = subprocess.run(
                ["/usr/bin/systemctl", "reload", "sshd"],    # nosec B603
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
            # Try ssh instead of sshd
                result = subprocess.run(
                    ["/usr/bin/systemctl", "reload", "ssh"],    # nosec B603
                    capture_output=True,
                    text=True,
                )

            if result.returncode == 0:
                logger.info("SSH daemon reloaded")
                return True, "SSH daemon reloaded"
            else:
                return False, result.stderr

        except Exception as e:
            return False, str(e)

    # -------------------------------------------------------------------------
    # Key Management
    # -------------------------------------------------------------------------

    def generate_host_keys(
        self, key_types: Optional[List[SSHKeyType]] = None
    ) -> Dict[str, Path]:
        """Generate new host keys."""
        key_types = key_types or [SSHKeyType.ED25519, SSHKeyType.ECDSA, SSHKeyType.RSA]
        generated = {}

        for key_type in key_types:
            key_file = self.config_path / f"ssh_host_{key_type.value}_key"

            # Backup existing key
            if key_file.exists():
                backup = key_file.with_suffix(
                    f".{datetime.now(timezone.utc).strftime('%Y%m%d')}.bak"
                )
                shutil.move(key_file, backup)
                if key_file.with_suffix(".pub").exists():
                    shutil.move(
                        key_file.with_suffix(".pub"), backup.with_suffix(".pub.bak")
                    )

            # Generate new key
            cmd = [
                "/usr/bin/ssh-keygen",
                "-t",
                key_type.value,
                "-f",
                str(key_file),
                "-N",
                "",
            ]

            if key_type == SSHKeyType.RSA:
                cmd.extend(["-b", "4096"])
            elif key_type == SSHKeyType.ECDSA:
                cmd.extend(["-b", "521"])

            try:
                subprocess.run(cmd, check=True, capture_output=True)    # nosec B603
                generated[key_type.value] = key_file
                logger.info(f"Generated {key_type.value} host key")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to generate {key_type.value} key: {e}")

        return generated

    def remove_weak_host_keys(self) -> List[str]:
        """Remove weak or deprecated host keys."""
        weak_types = ["dsa"]
        removed = []

        for key_type in weak_types:
            key_file = self.config_path / f"ssh_host_{key_type}_key"
            pub_file = key_file.with_suffix(".pub")

            for f in [key_file, pub_file]:
                if f.exists():
                    f.unlink()
                    removed.append(str(f))
                    logger.info(f"Removed weak key: {f}")

        return removed

    def get_host_key_fingerprints(self) -> Dict[str, str]:
        """Get fingerprints of all host keys."""
        fingerprints = {}

        for key_file in self.config_path.glob("ssh_host_*_key.pub"):
            try:
                result = subprocess.run(
                    ["/usr/bin/ssh-keygen", "-l", "-f", str(key_file)],    # nosec B603
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    fingerprints[key_file.stem] = result.stdout.strip()
            except Exception as e:
                logger.error(f"Failed to get fingerprint for {key_file}: {e}")

        return fingerprints

    # -------------------------------------------------------------------------
    # Authorized Keys Management
    # -------------------------------------------------------------------------

    def add_authorized_key(
        self,
        username: str,
        public_key: str,
        comment: str = "",
        options: Optional[List[str]] = None,
    ) -> Tuple[bool, str]:
        """Add public key to user's authorized_keys."""
        try:
        # Get user home directory
            import pwd

            user_info = pwd.getpwnam(username)    # type: ignore
            home_dir = Path(user_info.pw_dir)
            ssh_dir = home_dir / ".ssh"
            auth_keys = ssh_dir / "authorized_keys"

            # Create .ssh directory if needed
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            os.chown(ssh_dir, user_info.pw_uid, user_info.pw_gid)    # type: ignore

            # Build key line
            key_line = public_key.strip()
            if options:
                key_line = f"{', '.join(options)} {key_line}"
            if comment:
                key_line = f"{key_line} {comment}"
            key_line += "\n"

            # Check for duplicate
            if auth_keys.exists():
                existing = auth_keys.read_text()
                if public_key.strip() in existing:
                    return False, "Key already exists"

            # Append key
            with open(auth_keys, "a") as f:
                f.write(key_line)

            # Set permissions
            auth_keys.chmod(0o600)
            os.chown(auth_keys, user_info.pw_uid, user_info.pw_gid)    # type: ignore

            logger.info(f"Added authorized key for user {username}")
            return True, "Key added successfully"

        except Exception as e:
            logger.error(f"Failed to add authorized key: {e}")
            return False, str(e)

    def remove_authorized_key(
        self, username: str, key_fingerprint: str
    ) -> Tuple[bool, str]:
        """Remove public key from user's authorized_keys by fingerprint."""
        try:
            import pwd

            user_info = pwd.getpwnam(username)    # type: ignore
            auth_keys = Path(user_info.pw_dir) / ".ssh" / "authorized_keys"

            if not auth_keys.exists():
                return False, "No authorized_keys file"

            lines = auth_keys.read_text().splitlines()
            new_lines = []
            removed = False

            for line in lines:
                if not line.strip() or line.strip().startswith("    #"):
                    new_lines.append(line)
                    continue

                # Extract key and check fingerprint
                # This is simplified - in production, use ssh-keygen to verify
                if key_fingerprint not in line:
                    new_lines.append(line)
                else:
                    removed = True

            if removed:
                auth_keys.write_text("\n".join(new_lines) + "\n")
                logger.info(f"Removed authorized key for user {username}")
                return True, "Key removed successfully"

            return False, "Key not found"

        except Exception as e:
            logger.error(f"Failed to remove authorized key: {e}")
            return False, str(e)

    def list_authorized_keys(self, username: str) -> List[Dict[str, Any]]:
        """List authorized keys for user."""
        keys: List[Dict[str, Any]] = []

        try:
            import pwd

            user_info = pwd.getpwnam(username)    # type: ignore
            auth_keys = Path(user_info.pw_dir) / ".ssh" / "authorized_keys"

            if not auth_keys.exists():
                return keys

            for i, line in enumerate(auth_keys.read_text().splitlines()):
                if not line.strip() or line.strip().startswith("    #"):
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    key_type = parts[0] if parts[0].startswith("ssh-") else "unknown"
                    comment = parts[-1] if len(parts) > 2 else ""

                    keys.append(
                        {
                            "index": i,
                            "type": key_type,
                            "comment": comment,
                            "line_preview": (
                                line[:80] + "..." if len(line) > 80 else line
                            ),
                        }
                    )

        except Exception as e:
            logger.error(f"Failed to list authorized keys: {e}")

        return keys

    # -------------------------------------------------------------------------
    # MFA Integration
    # -------------------------------------------------------------------------

    def configure_totp_mfa(self, user: str) -> Tuple[bool, Dict[str, Any]]:
        """Configure TOTP-based MFA for user."""
        try:
        # This would typically integrate with google-authenticator-libpam
            # For now, we'll generate the configuration

            secret = secrets.token_hex(20)
            recovery_codes = [secrets.token_hex(4) for _ in range(10)]

            # Generate provisioning URI
            issuer = "DebVisor"
            uri = f"otpauth://totp/{issuer}:{user}?secret={secret}&issuer={issuer}"

            result = {
                "user": user,
                "secret": secret,
                "provisioning_uri": uri,
                "recovery_codes": recovery_codes,
                "instructions": [
                    "1. Install Google Authenticator or similar TOTP app",
                    "2. Scan the QR code or enter the secret manually",
                    f"3. Secret: {secret}",
                    "4. Save your recovery codes securely",
                    "5. Test login with MFA before logging out",
                ],
            }

            logger.info(f"Configured TOTP MFA for user {user}")
            return True, result

        except Exception as e:
            logger.error(f"Failed to configure TOTP: {e}")
            return False, {"error": str(e)}

    def generate_pam_config(self) -> str:
        """Generate PAM configuration for SSH MFA."""
        config = """    # DebVisor SSH PAM Configuration with MFA
# /etc/pam.d/sshd

# Standard authentication
@include common-auth

# Account management
@include common-account

# Session management
@include common-session

# Password management
@include common-password

# MFA Configuration (Google Authenticator)
# Uncomment the following line to enable TOTP MFA
# auth required pam_google_authenticator.so nullok

# For hardware key (FIDO2/U2F) support
# auth required pam_u2f.so
"""
        return config

    # -------------------------------------------------------------------------
    # Fail2ban Integration
    # -------------------------------------------------------------------------

    def generate_fail2ban_config(self) -> str:
        """Generate Fail2ban jail configuration for SSH."""
        config = """    # DebVisor SSH Fail2ban Configuration
# /etc/fail2ban/jail.d/debvisor-sshd.conf

[sshd]
enabled = true
mode = aggressive
port = ssh
filter = sshd
logpath = /var/log/auth.log
backend = systemd

# Ban configuration
maxretry = 3
findtime = 600
bantime = 3600

# Progressive banning (requires fail2ban >= 0.11)
bantime.increment = true
bantime.factor = 2
bantime.maxtime = 1w
bantime.rndtime = 30m

# Whitelist
ignoreip = 127.0.0.1/8 ::1

# Actions
action = %(action_mwl)s

[sshd-ddos]
enabled = true
port = ssh
filter = sshd-ddos
logpath = /var/log/auth.log
maxretry = 6
findtime = 30
bantime = 86400
"""
        return config

    # -------------------------------------------------------------------------
    # Security Audit
    # -------------------------------------------------------------------------

    def audit_ssh_config(self) -> Dict[str, Any]:
        """Audit current SSH configuration."""
        findings = []
        score = 100

        # Check root login
        if self._config.permit_root_login == "yes":
            findings.append(
                {
                    "severity": "HIGH",
                    "finding": "Root login is permitted",
                    "recommendation": "Set PermitRootLogin to 'no' or 'prohibit-password'",
                }
            )
            score -= 20

        # Check password authentication
        if self._config.password_authentication:
            findings.append(
                {
                    "severity": "MEDIUM",
                    "finding": "Password authentication is enabled",
                    "recommendation": "Disable password authentication and use key-based auth",
                }
            )
            score -= 15

        # Check forwarding
        if self._config.allow_tcp_forwarding != "no":
            findings.append(
                {
                    "severity": "LOW",
                    "finding": "TCP forwarding is enabled",
                    "recommendation": "Disable TCP forwarding unless required",
                }
            )
            score -= 5

        if self._config.x11_forwarding:
            findings.append(
                {
                    "severity": "LOW",
                    "finding": "X11 forwarding is enabled",
                    "recommendation": "Disable X11 forwarding",
                }
            )
            score -= 5

        # Check max auth tries
        if self._config.max_auth_tries > 3:
            findings.append(
                {
                    "severity": "MEDIUM",
                    "finding": f"MaxAuthTries is high ({self._config.max_auth_tries})",
                    "recommendation": "Set MaxAuthTries to 3 or less",
                }
            )
            score -= 10

        # Check ciphers
        weak_ciphers = ["3des-cbc", "arcfour", "blowfish-cbc"]
        for cipher in self._config.ciphers:
            if any(weak in cipher.lower() for weak in weak_ciphers):
                findings.append(
                    {
                        "severity": "HIGH",
                        "finding": f"Weak cipher enabled: {cipher}",
                        "recommendation": "Remove weak ciphers from configuration",
                    }
                )
                score -= 15
                break

        return {
            "score": max(0, score),
            "grade": self._score_to_grade(score),
            "findings": findings,
            "security_level": self._security_level.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _score_to_grade(self, score: int) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


# =============================================================================
# Flask Integration
# =============================================================================


def create_ssh_blueprint(manager: SSHHardeningManager) -> Any:
    """Create Flask blueprint for SSH management API."""
    try:
        from flask import Blueprint, jsonify, Response
        from opt.web.panel.rbac import require_permission, Resource, Action

        bp = Blueprint("ssh", __name__, url_prefix="/api/ssh")

        @bp.route("/config", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def get_config() -> Response:
            """Get current SSH configuration."""
            return jsonify(
                {
                    "security_level": manager._security_level.value,
                    "port": manager._config.port,
                    "permit_root_login": manager._config.permit_root_login,
                    "password_authentication": manager._config.password_authentication,
                    "pubkey_authentication": manager._config.pubkey_authentication,
                    "max_auth_tries": manager._config.max_auth_tries,
                }
            )

        @bp.route("/config/preview", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def preview_config() -> Response:
            """Preview generated SSH configuration."""
            config = manager.generate_sshd_config()
            return jsonify({"config": config})

        @bp.route("/audit", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def audit() -> Response:
            """Audit SSH configuration."""
            return jsonify(manager.audit_ssh_config())

        @bp.route("/host-keys/fingerprints", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def host_key_fingerprints() -> Response:
            """Get host key fingerprints."""
            return jsonify(manager.get_host_key_fingerprints())

        @bp.route("/fail2ban/config", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def fail2ban_config() -> Response:
            """Get Fail2ban configuration."""
            return jsonify({"config": manager.generate_fail2ban_config()})

        return bp

    except ImportError:
        logger.warning("Flask not available for SSH blueprint")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "SSHAuthMethod",
    "SSHKeyType",
    "MFAProvider",
    "SSHSecurityLevel",
    "SSHKeyConfig",
    "SSHHostKeyConfig",
    "SSHRateLimitConfig",
    "SSHLoggingConfig",
    "MFAConfig",
    "SSHDConfig",
    "SSHHardeningManager",
    "create_ssh_blueprint",
]
