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
    PinStatus,
    CertificatePin,
    PinPolicy,
    PinValidationResult,
    CertificatePinningManager,
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
    "PinStatus",
    "CertificatePin",
    "PinPolicy",
    "PinValidationResult",
    "CertificatePinningManager",
    
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
