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

"""
SSH Hardener for DebVisor
Enforces strict SSH security configurations:
- Disables Password Authentication
- Enforces Public Key Authentication
- Disables Root Login (or restricts to prohibit-password)
- Enforces Protocol 2
"""

import os
import shutil
import subprocess
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - SSH-HARDENER - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

SSHD_CONFIG = "/etc/ssh/sshd_config"
BACKUP_CONFIG = "/etc/ssh/sshd_config.bak"


def backup_config() -> None:
    if os.path.exists(SSHD_CONFIG):
        shutil.copy2(SSHD_CONFIG, BACKUP_CONFIG)
        logger.info(f"Backed up sshd_config to {BACKUP_CONFIG}")
    else:
        logger.error(f"{SSHD_CONFIG} not found!")
        sys.exit(1)


def apply_hardening() -> None:
    """Reads the config, modifies lines, and writes it back."""
    with open(SSHD_CONFIG, "r") as f:
        lines = f.readlines()

    new_lines = []
    # Configuration map
    config_map = {
        "PasswordAuthentication": "no",
        "PermitRootLogin": "prohibit-password",
        "PubkeyAuthentication": "yes",
        "ChallengeResponseAuthentication": "no",
        "UsePAM": "yes",    # PAM is often needed for session setup, but auth is handled by keys
        "X11Forwarding": "no",
        "PermitEmptyPasswords": "no",
        "Protocol": "2",
    }

    # Track what we've seen to append missing keys later
    seen_keys = set()

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("    #"):
            new_lines.append(line)
            continue

        parts = line_stripped.split()
        key = parts[0]

        if key in config_map:
            seen_keys.add(key)
            new_lines.append(f"{key} {config_map[key]}\n")
            logger.info(f"Enforcing: {key} {config_map[key]}")
        else:
            new_lines.append(line)

    # Append missing keys
    for key, value in config_map.items():
        if key not in seen_keys:
            new_lines.append(f"{key} {value}\n")
            logger.info(f"Adding: {key} {value}")

    try:
        with open(SSHD_CONFIG, "w") as f:
            f.writelines(new_lines)
        logger.info("Configuration written successfully.")
    except PermissionError:
        logger.error("Permission denied writing to sshd_config. Run as root.")
        sys.exit(1)


def validate_and_restart() -> None:
    """Validates config syntax and restarts service."""
    try:
        subprocess.check_call(["sshd", "-t"])
        logger.info("SSHD configuration syntax is valid.")
    except subprocess.CalledProcessError:
        logger.error("SSHD configuration syntax check FAILED! Restoring backup...")
        shutil.copy2(BACKUP_CONFIG, SSHD_CONFIG)
        sys.exit(1)

    try:
        subprocess.check_call(["systemctl", "restart", "ssh"])
        logger.info("SSHD service restarted successfully.")
    except subprocess.CalledProcessError:
        logger.error("Failed to restart SSHD service.")
        sys.exit(1)


def main() -> None:
    if os.geteuid() != 0:  # type: ignore[attr-defined]
        logger.error("This script must be run as root.")
        sys.exit(1)

    backup_config()
    apply_hardening()
    validate_and_restart()


if __name__ == "__main__":
    main()
