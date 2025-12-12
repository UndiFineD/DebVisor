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


"""
DebVisor Security Module.

Enterprise security services including:
- Certificate pinning for internal communication
- SSH hardening and management
- Firewall management (nftables)
- ACME/Let's Encrypt certificate automation
"""

from .cert_pinning import (
    PinType,
    CertificatePin,
    PinningPolicy,
    CertificatePinValidator,
)

from .ssh_hardening import (
    SSHAuthMethod,
    SSHKeyType,
    MFAProvider,
    SSHSecurityLevel,
    SSHKeyConfig,
    SSHHostKeyConfig,
    SSHRateLimitConfig,
    SSHLoggingConfig,
    MFAConfig,
    SSHDConfig,
    SSHHardeningManager,
    create_ssh_blueprint,
)

from .firewall_manager import (
    FirewallAction,
    FirewallDirection,
    Protocol,
    FirewallZone,
    RuleType,
    IPSet,
    PortGroup,
    FirewallRule,
    SecurityGroup,
    FirewallConfig,
    FirewallManager,
    create_default_firewall,
    create_firewall_blueprint,
    PREDEFINED_SERVICES,
)

from .acme_certificates import (
    ChallengeType,
    CertificateStatus,
    ACMEProvider,
    DNSProvider,
    ACMEConfig,
    Certificate,
    ChallengeRecord,
    ACMECertificateManager,
    create_acme_blueprint,
)

__all__ = [
    # Certificate Pinning
    "PinType",
    "CertificatePin",
    "PinningPolicy",
    "CertificatePinValidator",
    # SSH Hardening
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
    # Firewall
    "FirewallAction",
    "FirewallDirection",
    "Protocol",
    "FirewallZone",
    "RuleType",
    "IPSet",
    "PortGroup",
    "FirewallRule",
    "SecurityGroup",
    "FirewallConfig",
    "FirewallManager",
    "create_default_firewall",
    "create_firewall_blueprint",
    "PREDEFINED_SERVICES",
    # ACME/Let's Encrypt
    "ChallengeType",
    "CertificateStatus",
    "ACMEProvider",
    "DNSProvider",
    "ACMEConfig",
    "Certificate",
    "ChallengeRecord",
    "ACMECertificateManager",
    "create_acme_blueprint",
]
