#!/usr/bin/env python3
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

"""Security Hardening Scanner.

Audits system security posture:
- Kernel parameter checks (sysctl)
- SSH configuration audit
- File permission verification
- TPM/Secure Boot status
- CIS Benchmark compliance (partial)

Production ready for basic checks.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import logging
import os
import re
import subprocess

logger = logging.getLogger(__name__)


@dataclass
class AuditResult:
    check_id: str
    name: str
    passed: bool
    details: str
    severity: str    # low|medium|high|critical
    remediation: Optional[str] = None


class HardeningScanner:
    def __init__(self) -> None:
        self.results: List[AuditResult] = []

    def run_scan(self) -> List[AuditResult]:
        self.results = []
        self._check_ssh_root_login()
        self._check_ssh_password_auth()
        self._check_kernel_forwarding()
        self._check_secure_boot()
        self._check_firewall_enabled()
        self._check_unattended_upgrades()
        self._check_world_writable_files()
        return self.results

    def _check_ssh_root_login(self) -> None:
        """CIS 5.2.10 - Ensure SSH root login is disabled."""
        config_path = "/etc/ssh/sshd_config"
        passed = False
        details = "Unable to check"

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read()
                match = re.search(r"^PermitRootLogin\s+(\w+)", content, re.MULTILINE)
                if match:
                    value = match.group(1).lower()
                    passed = value in ("no", "prohibit-password")
                    details = f"PermitRootLogin is '{value}'"
                else:
                    details = "PermitRootLogin not explicitly set (defaults may vary)"
            except PermissionError:
                details = "Permission denied reading sshd_config"
        else:
            details = "sshd_config not found (SSH not installed?)"

        self.results.append(
            AuditResult(
                "SSH-001",
                "Disable Root Login",
                passed,
                details,
                "high",
                "Set 'PermitRootLogin no' in /etc/ssh/sshd_config",
            )
        )

    def _check_ssh_password_auth(self) -> None:
        """CIS 5.2.12 - Ensure SSH PasswordAuthentication is disabled."""
        config_path = "/etc/ssh/sshd_config"
        passed = False
        details = "Unable to check"

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read()
                match = re.search(
                    r"^PasswordAuthentication\s+(\w+)", content, re.MULTILINE
                )
                if match:
                    passed = match.group(1).lower() == "no"
                    details = f"PasswordAuthentication is '{match.group(1)}'"
                else:
                    details = "PasswordAuthentication not explicitly set"
            except PermissionError:
                details = "Permission denied"

        self.results.append(
            AuditResult(
                "SSH-002",
                "Disable Password Auth",
                passed,
                details,
                "medium",
                "Set 'PasswordAuthentication no' in /etc/ssh/sshd_config",
            )
        )

    def _check_kernel_forwarding(self) -> None:
        """CIS 3.1.1 - Ensure IP forwarding is disabled (if not a router)."""
        passed = True
        details = "Unable to check"

        sysctl_path = "/proc/sys/net/ipv4/ip_forward"
        if os.path.exists(sysctl_path):
            try:
                with open(sysctl_path, "r") as f:
                    value = f.read().strip()
                passed = value == "0"
                details = f"net.ipv4.ip_forward = {value}"
            except PermissionError:
                details = "Permission denied"

        self.results.append(
            AuditResult(
                "NET-001",
                "IP Forwarding Disabled",
                passed,
                details,
                "medium",
                "Run: sysctl -w net.ipv4.ip_forward=0",
            )
        )

    def _check_secure_boot(self) -> None:
        """Check if Secure Boot is enabled."""
        passed = False
        details = "Unable to determine"

        sb_path = (
            "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
        )
        if os.path.exists(sb_path):
            try:
                with open(sb_path, "rb") as f:
                    data = f.read()
                # Last byte indicates state (1 = enabled)
                if len(data) >= 5:
                    passed = data[4] == 1
                    details = "Secure Boot is " + ("enabled" if passed else "disabled")
            except PermissionError:
                details = "Permission denied reading SecureBoot status"
        elif os.path.exists("/sys/firmware/efi"):
            details = "EFI system but SecureBoot var not found"
        else:
            details = "Legacy BIOS system (no EFI)"

        self.results.append(
            AuditResult(
                "BOOT-001",
                "Secure Boot Enabled",
                passed,
                details,
                "high",
                "Enable Secure Boot in UEFI firmware settings",
            )
        )

    def _check_firewall_enabled(self) -> None:
        """Check if firewall (ufw/nftables) is active."""
        passed = False
        details = "No firewall detected"

        # Check ufw
        try:
            result = subprocess.run(
                ["ufw", "status"], capture_output=True, text=True, timeout=5
            )    # nosec B603, B607
            if "active" in result.stdout.lower():
                passed = True
                details = "UFW firewall is active"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Check nftables
        if not passed:
            try:
                result = subprocess.run(
                    ["nft", "list", "ruleset"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )    # nosec B603, B607
                if result.returncode == 0 and result.stdout.strip():
                    passed = True
                    details = "nftables rules are configured"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

        self.results.append(
            AuditResult(
                "FW-001",
                "Firewall Enabled",
                passed,
                details,
                "critical",
                "Enable firewall: ufw enable OR configure nftables",
            )
        )

    def _check_unattended_upgrades(self) -> None:
        """Check if automatic security updates are enabled."""
        passed = False
        details = "Unattended-upgrades not configured"

        config_path = "/etc/apt/apt.conf.d/20auto-upgrades"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read()
                if 'Unattended-Upgrade "1"' in content:
                    passed = True
                    details = "Automatic security updates enabled"
            except PermissionError:
                details = "Permission denied"

        self.results.append(
            AuditResult(
                "PKG-001",
                "Auto Security Updates",
                passed,
                details,
                "medium",
                "Install and configure unattended-upgrades package",
            )
        )

    def _check_world_writable_files(self) -> None:
        """Check for world-writable files in sensitive directories."""
        passed = True
        details = "No world-writable files found in /etc"

        try:
            result = subprocess.run(
                ["find", "/etc", "-type", "", "-perm", "-0002", "-print"],
                capture_output=True,
                text=True,
                timeout=30,
            )    # nosec B603, B607
            if result.stdout.strip():
                files = result.stdout.strip().split("\n")
                passed = False
                details = f"Found {len(files)} world-writable files: {files[:3]}"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            details = "Unable to scan"

        self.results.append(
            AuditResult(
                "FS-001",
                "No World-Writable Config Files",
                passed,
                details,
                "high",
                "Run: chmod o-w <file> for each affected file",
            )
        )

    def generate_report(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        score = int((passed / total) * 100) if total > 0 else 0

        lines = [
            "    # Security Hardening Report",
            f"Score: {score}% ({passed}/{total} checks passed)",
            "",
            "    ## Results",
            "",
        ]

        for r in sorted(self.results, key=lambda x: x.passed):
            status = "? PASS" if r.passed else "? FAIL"
            lines.append(f"    ### [{r.check_id}] {r.name}")
            lines.append(f"**Status:** {status} | **Severity:** {r.severity.upper()}")
            lines.append(f"**Details:** {r.details}")
            if not r.passed and r.remediation:
                lines.append(f"**Remediation:** {r.remediation}")
            lines.append("")

        return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = HardeningScanner()
    results = scanner.run_scan()
    print(scanner.generate_report())
