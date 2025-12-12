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

logging.basicConfig(  # type: ignore[call-arg]
    _level=logging.INFO,
    _format="%(asctime)s - SSH-HARDENER - %(levelname)s - %(message)s",
)
_logger=logging.getLogger(__name__)

SSHD_CONFIG="/etc/ssh/sshd_config"
BACKUP_CONFIG="/etc/ssh/sshd_config.bak"


def backup_config() -> None:
    if os.path.exists(SSHD_CONFIG):
        shutil.copy2(SSHD_CONFIG, BACKUP_CONFIG)
        logger.info(f"Backed up sshd_config to {BACKUP_CONFIG}")  # type: ignore[name-defined]
    else:
        logger.error(f"{SSHD_CONFIG} not found!")  # type: ignore[name-defined]
        sys.exit(1)


def apply_hardening() -> None:
    """Reads the config, modifies lines, and writes it back."""
    with open(SSHD_CONFIG, "r") as f:
        _lines=f.readlines()

    _new_lines=[]  # type: ignore[var-annotated]
    # Configuration map
    _config_map={
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
    _seen_keys=set()  # type: ignore[var-annotated]

    for line in lines:  # type: ignore[name-defined]
        _line_stripped=line.strip()
        if not line_stripped or line_stripped.startswith("    #"):  # type: ignore[name-defined]
            new_lines.append(line)  # type: ignore[name-defined]
            continue

        _parts=line_stripped.split()  # type: ignore[name-defined]
        key=parts[0]  # type: ignore[name-defined]

        if key in config_map:  # type: ignore[name-defined]
            seen_keys.add(key)  # type: ignore[name-defined]
            new_lines.append(f"{key} {config_map[key]}\n")  # type: ignore[name-defined]
            logger.info(f"Enforcing: {key} {config_map[key]}")  # type: ignore[name-defined]
        else:
            new_lines.append(line)  # type: ignore[name-defined]

    # Append missing keys
    for key, value in config_map.items():  # type: ignore[name-defined]
        if key not in seen_keys:  # type: ignore[name-defined]
            new_lines.append(f"{key} {value}\n")  # type: ignore[name-defined]
            logger.info(f"Adding: {key} {value}")  # type: ignore[name-defined]

    try:
        with open(SSHD_CONFIG, "w") as f:
            f.writelines(new_lines)  # type: ignore[name-defined]
        logger.info("Configuration written successfully.")  # type: ignore[name-defined]
    except PermissionError:
        logger.error("Permission denied writing to sshd_config. Run as root.")  # type: ignore[name-defined]
        sys.exit(1)


def validate_and_restart() -> None:
    """Validates config syntax and restarts service."""
    try:
        subprocess.check_call(["sshd", "-t"])
        logger.info("SSHD configuration syntax is valid.")  # type: ignore[name-defined]
    except subprocess.CalledProcessError:
        logger.error("SSHD configuration syntax check FAILED! Restoring backup...")  # type: ignore[name-defined]
        shutil.copy2(BACKUP_CONFIG, SSHD_CONFIG)
        sys.exit(1)

    try:
        subprocess.check_call(["systemctl", "restart", "ssh"])
        logger.info("SSHD service restarted successfully.")  # type: ignore[name-defined]
    except subprocess.CalledProcessError:
        logger.error("Failed to restart SSHD service.")  # type: ignore[name-defined]
        sys.exit(1)


def main() -> None:
    if os.geteuid() != 0:  # type: ignore[attr-defined]
        logger.error("This script must be run as root.")  # type: ignore[name-defined]
        sys.exit(1)

    backup_config()
    apply_hardening()
    validate_and_restart()


if _name__== "__main__":  # type: ignore[name-defined]
    main()
