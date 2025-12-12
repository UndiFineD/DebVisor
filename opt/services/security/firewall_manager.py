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

"""
Enterprise Firewall Manager for DebVisor.

Provides Proxmox-style nftables firewall management with:
- Zone-based firewall rules
- Service-based rule templates
- Port groups and IP sets
- Rate limiting and connection tracking
- Integration with intrusion detection
- Cluster-wide rule synchronization
- Audit logging

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone
import logging
import subprocess
import threading
import tempfile
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class FirewallAction(Enum):
    """Firewall rule actions."""

    ACCEPT = "accept"
    DROP = "drop"
    REJECT = "reject"
    LOG = "log"
    MARK = "mark"
    RETURN = "return"


class FirewallDirection(Enum):
    """Traffic direction."""

    IN = "in"
    OUT = "out"
    FORWARD = "forward"


class Protocol(Enum):
    """Network protocols."""

    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ICMPV6 = "icmpv6"
    ANY = "any"


class FirewallZone(Enum):
    """Firewall zones (Proxmox-style)."""

    MANAGEMENT = "management"    # Management network
    CLUSTER = "cluster"    # Cluster communication
    STORAGE = "storage"    # Storage network
    VM = "vm"    # VM traffic
    MIGRATION = "migration"    # Live migration
    PUBLIC = "public"    # Public/untrusted
    DMZ = "dmz"    # Demilitarized zone
    INTERNAL = "internal"    # Internal trusted


class RuleType(Enum):
    """Rule types."""

    HOST = "host"    # Rules for the host
    VM = "vm"    # Rules for VMs
    GROUP = "group"    # Security group rules
    CLUSTER = "cluster"    # Cluster-wide rules


# =============================================================================
# Predefined Services
# =============================================================================

PREDEFINED_SERVICES: Dict[str, Dict[str, Union[str, int]]] = {
    # DebVisor services
    "debvisor-api": {"protocol": "tcp", "port": 8006},
    "debvisor-spice": {"protocol": "tcp", "port": "3128"},
    "debvisor-vnc": {"protocol": "tcp", "port": "5900:5999"},
    "debvisor-migration": {"protocol": "tcp", "port": 60000},
    # Proxmox-compatible services
    "pveproxy": {"protocol": "tcp", "port": 8006},
    "spice": {"protocol": "tcp", "port": 3128},
    "vnc": {"protocol": "tcp", "port": "5900:5999"},
    # Standard services
    "ssh": {"protocol": "tcp", "port": 22},
    "http": {"protocol": "tcp", "port": 80},
    "https": {"protocol": "tcp", "port": 443},
    "dns": {"protocol": "udp", "port": 53},
    "dhcp": {"protocol": "udp", "port": "67:68"},
    "ntp": {"protocol": "udp", "port": 123},
    "smtp": {"protocol": "tcp", "port": 25},
    "smtps": {"protocol": "tcp", "port": 465},
    "imap": {"protocol": "tcp", "port": 143},
    "imaps": {"protocol": "tcp", "port": 993},
    "pop3": {"protocol": "tcp", "port": 110},
    "pop3s": {"protocol": "tcp", "port": 995},
    "ftp": {"protocol": "tcp", "port": "20:21"},
    "mysql": {"protocol": "tcp", "port": 3306},
    "postgresql": {"protocol": "tcp", "port": 5432},
    "redis": {"protocol": "tcp", "port": 6379},
    "mongodb": {"protocol": "tcp", "port": 27017},
    "elasticsearch": {"protocol": "tcp", "port": 9200},
    # Clustering
    "corosync": {"protocol": "udp", "port": "5405:5412"},
    "ceph-mon": {"protocol": "tcp", "port": 6789},
    "ceph-osd": {"protocol": "tcp", "port": "6800:7300"},
    "ceph-mgr": {"protocol": "tcp", "port": "6800:6802"},
    "glusterfs": {"protocol": "tcp", "port": "24007:24008"},
    # Monitoring
    "prometheus": {"protocol": "tcp", "port": 9090},
    "grafana": {"protocol": "tcp", "port": 3000},
    "node-exporter": {"protocol": "tcp", "port": 9100},
}


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class IPSet:
    """IP address set."""

    name: str
    description: str = ""
    addresses: Set[str] = field(default_factory=set)
    comment: str = ""
    family: str = "ipv4"    # ipv4 or ipv6

    def add(self, address: str) -> None:
        """Add address to set."""
        self.addresses.add(address)

    def remove(self, address: str) -> None:
        """Remove address from set."""
        self.addresses.discard(address)

    def to_nftables(self) -> str:
        """Generate nftables set definition."""
        elements = ", ".join(sorted(self.addresses))
        type_str = "ipv6_addr" if self.family == "ipv6" else "ipv4_addr"
        return f"""
    set {self.name} {{
        type {type_str}
        comment "{self.description}"
        elements = {{ {elements} }}
    }}"""


@dataclass
class PortGroup:
    """Port group definition."""

    name: str
    description: str = ""
    ports: List[str] = field(default_factory=list)    # Can be single port or range
    protocol: Protocol = Protocol.TCP

    def add_port(self, port: Union[int, str]) -> None:
        """Add port to group."""
        self.ports.append(str(port))

    def to_nftables(self) -> str:
        """Generate nftables port set."""
        elements = ", ".join(self.ports)
        return f"""
    set {self.name} {{
        type inet_service
        comment "{self.description}"
        elements = {{ {elements} }}
    }}"""


@dataclass
class FirewallRule:
    """Individual firewall rule."""

    id: str
    action: FirewallAction
    direction: FirewallDirection
    protocol: Protocol = Protocol.ANY
    source: str = ""    # IP, CIDR, or IPSet reference
    destination: str = ""
    source_port: str = ""    # Port or PortGroup reference
    destination_port: str = ""
    interface: str = ""
    enabled: bool = True
    log: bool = False
    log_prefix: str = ""
    comment: str = ""
    position: int = 0    # Rule order

    # Rate limiting
    rate_limit: Optional[str] = None    # e.g., "10/second"

    # Connection tracking
    ct_state: List[str] = field(default_factory=list)    # new, established, related

    # Service macro
    service: Optional[str] = None

    def to_nftables(self) -> str:
        """Generate nftables rule."""
        parts = []

        # Protocol
        if self.protocol != Protocol.ANY:
            parts.append(self.protocol.value)

        # Source
        if self.source:
            if self.source.startswith("@"):
                if self.source.endswith("_v6"):
                    parts.append(f"ip6 saddr {self.source}")
                else:
                    parts.append(f"ip saddr {self.source}")
            elif ":" in self.source:
                parts.append(f"ip6 saddr {self.source}")
            else:
                parts.append(f"ip saddr {self.source}")

        # Destination
        if self.destination:
            if self.destination.startswith("@"):
                if self.destination.endswith("_v6"):
                    parts.append(f"ip6 daddr {self.destination}")
                else:
                    parts.append(f"ip daddr {self.destination}")
            elif ":" in self.destination:
                parts.append(f"ip6 daddr {self.destination}")
            else:
                parts.append(f"ip daddr {self.destination}")

        # Source port
        if self.source_port:
            parts.append(f"{self.protocol.value} sport {self.source_port}")

        # Destination port
        if self.destination_port:
            parts.append(f"{self.protocol.value} dport {self.destination_port}")

        # Connection tracking
        if self.ct_state:
            states = ", ".join(self.ct_state)
            parts.append(f"ct state {{ {states} }}")

        # Rate limiting
        if self.rate_limit:
            parts.append(f"limit rate {self.rate_limit}")

        # Logging
        if self.log:
            prefix = self.log_prefix or f"FW-{self.action.value.upper()}"
            parts.append(f'log prefix "{prefix}: "')

        # Action
        parts.append(self.action.value)

        # Comment
        rule_line = " ".join(parts)
        if self.comment:
            rule_line += f"    # {self.comment}"

        return rule_line


@dataclass
class SecurityGroup:
    """Security group (collection of rules)."""

    name: str
    description: str = ""
    rules: List[FirewallRule] = field(default_factory=list)
    enabled: bool = True

    def add_rule(self, rule: FirewallRule) -> None:
        """Add rule to group."""
        self.rules.append(rule)
        self._sort_rules()

    def remove_rule(self, rule_id: str) -> bool:
        """Remove rule from group."""
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                del self.rules[i]
                return True
        return False

    def _sort_rules(self) -> None:
        """Sort rules by position."""
        self.rules.sort(key=lambda r: r.position)


@dataclass
class FirewallConfig:
    """Complete firewall configuration."""

    enabled: bool = True
    default_input_policy: FirewallAction = FirewallAction.DROP
    default_output_policy: FirewallAction = FirewallAction.ACCEPT
    default_forward_policy: FirewallAction = FirewallAction.DROP

    # Logging
    log_level: str = "warning"
    log_limit: str = "5/minute"

    # Conntrack
    conntrack_enabled: bool = True
    conntrack_max: int = 1000000

    # SYN flood protection
    syn_flood_protection: bool = True
    syn_rate_limit: str = "100/second"

    # ICMP
    allow_ping: bool = True
    icmp_rate_limit: str = "5/second"

    # SSH
    ssh_port: int = 22
    ssh_rate_limit: str = "10/minute"


# =============================================================================
# Firewall Manager
# =============================================================================


class FirewallManager:
    """
    Enterprise firewall manager with nftables backend.

    Features:
    - Zone-based security model
    - Predefined service macros
    - IP sets and port groups
    - Security groups
    - Rate limiting
    - Intrusion detection integration
    - Cluster-wide synchronization
    """

    def __init__(self, config: Optional[FirewallConfig] = None):
        self.config = config or FirewallConfig()
        self._ip_sets: Dict[str, IPSet] = {}
        self._port_groups: Dict[str, PortGroup] = {}
        self._security_groups: Dict[str, SecurityGroup] = {}
        self._host_rules: List[FirewallRule] = []
        self._zones: Dict[FirewallZone, List[str]] = {}    # zone -> interfaces
        self._lock = threading.Lock()

        # Initialize default IP sets
        self._init_default_sets()

    def _init_default_sets(self) -> None:
        """Initialize default IP sets."""
        # Management IPs
        self.create_ipset("management", "Management network addresses")

        # Cluster nodes
        self.create_ipset("cluster_nodes", "Cluster node addresses")

        # Blacklist
        self.create_ipset("blacklist", "Blocked IP addresses")

        # Whitelist
        self.create_ipset("whitelist", "Always allowed IP addresses")

    # -------------------------------------------------------------------------
    # IP Set Management
    # -------------------------------------------------------------------------

    def create_ipset(self, name: str, description: str = "") -> IPSet:
        """Create new IP set."""
        ipset = IPSet(name=name, description=description)
        self._ip_sets[name] = ipset
        logger.info(f"Created IP set: {name}")
        return ipset

    def get_ipset(self, name: str) -> Optional[IPSet]:
        """Get IP set by name."""
        return self._ip_sets.get(name)

    def add_to_ipset(self, set_name: str, address: str) -> bool:
        """Add address to IP set."""
        ipset = self._ip_sets.get(set_name)
        if ipset:
            ipset.add(address)
            logger.info(f"Added {address} to IP set {set_name}")
            return True
        return False

    def remove_from_ipset(self, set_name: str, address: str) -> bool:
        """Remove address from IP set."""
        ipset = self._ip_sets.get(set_name)
        if ipset:
            ipset.remove(address)
            logger.info(f"Removed {address} from IP set {set_name}")
            return True
        return False

    # -------------------------------------------------------------------------
    # Port Group Management
    # -------------------------------------------------------------------------

    def create_port_group(
        self, name: str, description: str = "", protocol: Protocol = Protocol.TCP
    ) -> PortGroup:
        """Create new port group."""
        group = PortGroup(name=name, description=description, protocol=protocol)
        self._port_groups[name] = group
        return group

    def get_port_group(self, name: str) -> Optional[PortGroup]:
        """Get port group by name."""
        return self._port_groups.get(name)

    # -------------------------------------------------------------------------
    # Security Group Management
    # -------------------------------------------------------------------------

    def create_security_group(self, name: str, description: str = "") -> SecurityGroup:
        """Create new security group."""
        group = SecurityGroup(name=name, description=description)
        self._security_groups[name] = group
        logger.info(f"Created security group: {name}")
        return group

    def get_security_group(self, name: str) -> Optional[SecurityGroup]:
        """Get security group by name."""
        return self._security_groups.get(name)

    def delete_security_group(self, name: str) -> bool:
        """Delete security group."""
        if name in self._security_groups:
            del self._security_groups[name]
            logger.info(f"Deleted security group: {name}")
            return True
        return False

    # -------------------------------------------------------------------------
    # Rule Management
    # -------------------------------------------------------------------------

    def add_rule(self, rule: FirewallRule, security_group: Optional[str] = None) -> str:
        """Add firewall rule."""
        if not rule.id:
            rule.id = f"rule_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

        with self._lock:
            if security_group:
                group = self._security_groups.get(security_group)
                if group:
                    group.add_rule(rule)
                else:
                    raise ValueError(f"Security group not found: {security_group}")
            else:
                self._host_rules.append(rule)
                self._host_rules.sort(key=lambda r: r.position)

        logger.info(f"Added firewall rule: {rule.id}")
        return rule.id

    def remove_rule(self, rule_id: str, security_group: Optional[str] = None) -> bool:
        """Remove firewall rule."""
        with self._lock:
            if security_group:
                group = self._security_groups.get(security_group)
                if group:
                    return group.remove_rule(rule_id)
                return False
            else:
                for i, rule in enumerate(self._host_rules):
                    if rule.id == rule_id:
                        del self._host_rules[i]
                        logger.info(f"Removed firewall rule: {rule_id}")
                        return True
        return False

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a firewall rule."""
        rule = self._find_rule(rule_id)
        if rule:
            rule.enabled = True
            return True
        return False

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a firewall rule."""
        rule = self._find_rule(rule_id)
        if rule:
            rule.enabled = False
            return True
        return False

    def _find_rule(self, rule_id: str) -> Optional[FirewallRule]:
        """Find rule by ID."""
        for rule in self._host_rules:
            if rule.id == rule_id:
                return rule
        for group in self._security_groups.values():
            for rule in group.rules:
                if rule.id == rule_id:
                    return rule
        return None

    # -------------------------------------------------------------------------
    # Service Macros
    # -------------------------------------------------------------------------

    def create_service_rule(
        self,
        service_name: str,
        action: FirewallAction = FirewallAction.ACCEPT,
        source: str = "",
        direction: FirewallDirection = FirewallDirection.IN,
    ) -> Optional[FirewallRule]:
        """Create rule from predefined service."""
        service = PREDEFINED_SERVICES.get(service_name)
        if not service:
            logger.warning(f"Unknown service: {service_name}")
            return None

        rule = FirewallRule(
            id=f"svc_{service_name}_{datetime.now(timezone.utc).strftime('%H%M%S')}",
            action=action,
            direction=direction,
            protocol=Protocol(str(service["protocol"])),
            destination_port=str(service["port"]),
            source=source,
            service=service_name,
            comment=f"Service: {service_name}",
        )

        return rule

    def get_available_services(self) -> Dict[str, Dict[str, Any]]:
        """Get list of predefined services."""
        return {k: dict(v) for k, v in PREDEFINED_SERVICES.items()}

    # -------------------------------------------------------------------------
    # Zone Management
    # -------------------------------------------------------------------------

    def assign_interface_to_zone(self, interface: str, zone: FirewallZone) -> None:
        """Assign interface to firewall zone."""
        if zone not in self._zones:
            self._zones[zone] = []

        # Remove from other zones
        for z in self._zones.values():
            if interface in z:
                z.remove(interface)

        self._zones[zone].append(interface)
        logger.info(f"Assigned interface {interface} to zone {zone.value}")

    def get_zone_interfaces(self, zone: FirewallZone) -> List[str]:
        """Get interfaces in zone."""
        return self._zones.get(zone, [])

    # -------------------------------------------------------------------------
    # nftables Generation
    # -------------------------------------------------------------------------

    def generate_nftables_config(self) -> str:
        """Generate complete nftables configuration."""
        config_lines = [
            "    #!/usr/sbin/nft -f",
            "",
            "    # DebVisor Enterprise Firewall Configuration",
            f"    # Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "    # Flush existing rules",
            "flush ruleset",
            "",
            "    # Main table",
            "table inet debvisor_firewall {",
        ]

        # IP Sets
        for ipset in self._ip_sets.values():
            if ipset.addresses:
                config_lines.append(ipset.to_nftables())

        # Port Groups
        for port_group in self._port_groups.values():
            if port_group.ports:
                config_lines.append(port_group.to_nftables())

        config_lines.append("")

        # Input chain
        config_lines.extend(self._generate_input_chain())

        # Output chain
        config_lines.extend(self._generate_output_chain())

        # Forward chain
        config_lines.extend(self._generate_forward_chain())

        config_lines.append("}")

        return "\n".join(config_lines)

    def _generate_input_chain(self) -> List[str]:
        """Generate input chain rules."""
        lines = [
            "    # Input chain",
            "    chain input {",
            f"        type filter hook input priority 0; policy {self.config.default_input_policy.value};",
            "",
            "        # Allow established connections",
            "        ct state established, related accept",
            "",
            "        # Drop invalid",
            "        ct state invalid drop",
            "",
            "        # Allow loopback",
            "        iif lo accept",
            "",
        ]

        # SYN flood protection
        if self.config.syn_flood_protection:
            lines.extend(
                [
                    "        # SYN flood protection",
                    f"        tcp flags syn limit rate {self.config.syn_rate_limit} accept",
                    "",
                ]
            )

        # ICMP
        if self.config.allow_ping:
            lines.extend(
                [
                    "        # Allow ICMP (ping)",
                    f"        icmp type echo-request limit rate {self.config.icmp_rate_limit} accept",
                    f"        icmpv6 type echo-request limit rate {self.config.icmp_rate_limit} accept",
                    "",
                    "        # Allow IPv6 Neighbor Discovery",
                    "        icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert, "
                    "nd-router-solicit, nd-router-advert } accept",
                    "",
                ]
            )

        # SSH rate limiting
        lines.extend(
            [
                "        # SSH with rate limiting",
                f"        tcp dport {self.config.ssh_port} limit rate {self.config.ssh_rate_limit} accept",
                "",
            ]
        )

        # Whitelist
        if "whitelist" in self._ip_sets and self._ip_sets["whitelist"].addresses:
            lines.extend(
                [
                    "        # Whitelist",
                    "        ip saddr @whitelist accept",
                    "",
                ]
            )

        # Blacklist
        if "blacklist" in self._ip_sets and self._ip_sets["blacklist"].addresses:
            lines.extend(
                [
                    "        # Blacklist",
                    "        ip saddr @blacklist drop",
                    "",
                ]
            )

        # Host rules
        for rule in self._host_rules:
            if rule.enabled and rule.direction == FirewallDirection.IN:
                lines.append(f"        {rule.to_nftables()}")

        # Security group rules
        for group in self._security_groups.values():
            if group.enabled:
                for rule in group.rules:
                    if rule.enabled and rule.direction == FirewallDirection.IN:
                        lines.append(f"        {rule.to_nftables()}")

        lines.extend(
            [
                "",
                "        # Log dropped packets",
                f"        limit rate {self.config.log_limit} "
                f'log prefix "FW-INPUT-DROP: " level {self.config.log_level}',
                "    }",
                "",
            ]
        )

        return lines

    def _generate_output_chain(self) -> List[str]:
        """Generate output chain rules."""
        lines = [
            "    # Output chain",
            "    chain output {",
            f"        type filter hook output priority 0; policy {self.config.default_output_policy.value};",
            "",
            "        # Allow established",
            "        ct state established, related accept",
            "",
        ]

        # Output rules
        for rule in self._host_rules:
            if rule.enabled and rule.direction == FirewallDirection.OUT:
                lines.append(f"        {rule.to_nftables()}")

        lines.extend(
            [
                "    }",
                "",
            ]
        )

        return lines

    def _generate_forward_chain(self) -> List[str]:
        """Generate forward chain rules."""
        lines = [
            "    # Forward chain",
            "    chain forward {",
            f"        type filter hook forward priority 0; policy {self.config.default_forward_policy.value};",
            "",
            "        # Allow established",
            "        ct state established, related accept",
            "",
        ]

        # Forward rules
        for rule in self._host_rules:
            if rule.enabled and rule.direction == FirewallDirection.FORWARD:
                lines.append(f"        {rule.to_nftables()}")

        lines.extend(
            [
                "",
                "        # Log dropped packets",
                f'        limit rate {self.config.log_limit} log prefix "FW-FORWARD-DROP: "',
                "    }",
            ]
        )

        return lines

    # -------------------------------------------------------------------------
    # Apply & Reload
    # -------------------------------------------------------------------------

    def apply(self, dry_run: bool = False) -> Tuple[bool, str]:
        """Apply firewall configuration."""
        config = self.generate_nftables_config()

        if dry_run:
            return True, config

        try:
            # Write to temp file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".nft", delete=False
            ) as tmp:
                tmp.write(config)
                config_path = tmp.name

            try:
                # Validate
                result = subprocess.run(
                    ["/usr/sbin/nft", "-c", "-f", config_path],    # nosec B603
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    logger.error(f"Firewall config validation failed: {result.stderr}")
                    return False, result.stderr

                # Apply
                result = subprocess.run(
                    ["/usr/sbin/nft", "-f", config_path],    # nosec B603
                    capture_output=True,
                    text=True,
                )
            finally:
                if os.path.exists(config_path):
                    os.unlink(config_path)

            if result.returncode != 0:
                logger.error(f"Failed to apply firewall: {result.stderr}")
                return False, result.stderr

            logger.info("Firewall configuration applied successfully")
            return True, "Configuration applied successfully"

        except Exception as e:
            logger.error(f"Firewall apply error: {e}")
            return False, str(e)

    def save_persistent(self, path: str = "/etc/nftables.conf") -> Tuple[bool, str]:
        """Save configuration for persistence across reboots."""
        config = self.generate_nftables_config()

        try:
            # Backup existing
            config_path = Path(path)
            if config_path.exists():
                backup = config_path.with_suffix(
                    f".{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.bak"
                )
                config_path.rename(backup)

            config_path.write_text(config)
            logger.info(f"Saved persistent firewall config to {path}")
            return True, f"Saved to {path}"

        except Exception as e:
            logger.error(f"Failed to save firewall config: {e}")
            return False, str(e)

    # -------------------------------------------------------------------------
    # IDS Integration
    # -------------------------------------------------------------------------

    def block_ip(self, ip: str, reason: str = "") -> bool:
        """Block an IP address (for IDS integration)."""
        self.add_to_ipset("blacklist", ip)
        logger.warning(f"Blocked IP {ip}: {reason}")
        return True

    def unblock_ip(self, ip: str) -> bool:
        """Unblock an IP address."""
        self.remove_from_ipset("blacklist", ip)
        logger.info(f"Unblocked IP {ip}")
        return True

    def get_blocked_ips(self) -> Set[str]:
        """Get list of blocked IPs."""
        ipset = self._ip_sets.get("blacklist")
        return ipset.addresses if ipset else set()

    # -------------------------------------------------------------------------
    # Status & Reporting
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get firewall status."""
        return {
            "enabled": self.config.enabled,
            "default_policies": {
                "input": self.config.default_input_policy.value,
                "output": self.config.default_output_policy.value,
                "forward": self.config.default_forward_policy.value,
            },
            "ip_sets": {name: len(s.addresses) for name, s in self._ip_sets.items()},
            "security_groups": list(self._security_groups.keys()),
            "host_rules_count": len(self._host_rules),
            "zones": {z.value: ifaces for z, ifaces in self._zones.items()},
        }

    def get_rules(self, include_disabled: bool = False) -> List[Dict[str, Any]]:
        """Get all rules."""
        rules = []

        for rule in self._host_rules:
            if include_disabled or rule.enabled:
                rules.append(
                    {
                        "id": rule.id,
                        "action": rule.action.value,
                        "direction": rule.direction.value,
                        "protocol": rule.protocol.value,
                        "source": rule.source,
                        "destination": rule.destination,
                        "destination_port": rule.destination_port,
                        "enabled": rule.enabled,
                        "service": rule.service,
                        "comment": rule.comment,
                        "group": None,
                    }
                )

        for group_name, group in self._security_groups.items():
            for rule in group.rules:
                if include_disabled or rule.enabled:
                    rules.append(
                        {
                            "id": rule.id,
                            "action": rule.action.value,
                            "direction": rule.direction.value,
                            "protocol": rule.protocol.value,
                            "source": rule.source,
                            "destination": rule.destination,
                            "destination_port": rule.destination_port,
                            "enabled": rule.enabled,
                            "service": rule.service,
                            "comment": rule.comment,
                            "group": group_name,
                        }
                    )

        return rules


# =============================================================================
# Default Configuration Factory
# =============================================================================


def create_default_firewall() -> FirewallManager:
    """Create firewall with sensible defaults for DebVisor."""
    manager = FirewallManager()

    # Allow DebVisor services
    for service in ["debvisor-api", "ssh", "https"]:
        rule = manager.create_service_rule(service, FirewallAction.ACCEPT)
        if rule:
            manager.add_rule(rule)

    # Allow cluster communication
    manager.create_security_group("cluster", "Cluster communication rules")
    for service in ["corosync", "ceph-mon", "ceph-osd"]:
        rule = manager.create_service_rule(
            service, FirewallAction.ACCEPT, source="@cluster_nodes"
        )
        if rule:
            manager.add_rule(rule, "cluster")

    return manager


# =============================================================================
# Flask Integration
# =============================================================================


def create_firewall_blueprint(manager: FirewallManager) -> Any:
    """Create Flask blueprint for firewall API."""
    try:
        from flask import Blueprint, request, jsonify, Response
        from flask_login import current_user
        from opt.web.panel.rbac import require_permission, Resource, Action
        from opt.web.panel.models.audit_log import AuditLog

        bp = Blueprint("firewall", __name__, url_prefix="/api/firewall")

        @bp.route("/status", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def status() -> Response:
            """Get firewall status."""
            return jsonify(manager.get_status())

        @bp.route("/rules", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def list_rules() -> Response:
            """List all rules."""
            include_disabled = (
                request.args.get("include_disabled", "false").lower() == "true"
            )
            return jsonify({"rules": manager.get_rules(include_disabled)})

        @bp.route("/rules", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        def add_rule() -> Tuple[Response, int]:
            """Add new rule."""
            data = request.get_json() or {}

            rule = FirewallRule(
                id=data.get("id", ""),
                action=FirewallAction(data.get("action", "accept")),
                direction=FirewallDirection(data.get("direction", "in")),
                protocol=Protocol(data.get("protocol", "tcp")),
                source=data.get("source", ""),
                destination=data.get("destination", ""),
                destination_port=data.get("destination_port", ""),
                comment=data.get("comment", ""),
            )

            rule_id = manager.add_rule(rule, data.get("security_group"))

            AuditLog.log_operation(
                user_id=current_user.id,
                operation="create",
                resource_type="system",
                action="firewall_add_rule",
                status="success",
                request_data={"rule_id": rule_id, "rule": data},
                ip_address=request.remote_addr,
            )

            return jsonify({"id": rule_id}), 201

        @bp.route("/rules/<rule_id>", methods=["DELETE"])
        @require_permission(Resource.SYSTEM, Action.DELETE)
        def delete_rule(rule_id: str) -> Tuple[Response, int]:
            """Delete rule."""
            success = manager.remove_rule(rule_id)
            if success:
                AuditLog.log_operation(
                    user_id=current_user.id,
                    operation="delete",
                    resource_type="system",
                    action="firewall_delete_rule",
                    status="success",
                    resource_id=rule_id,
                    ip_address=request.remote_addr,
                )
                return jsonify({"status": "deleted"}), 200
            return jsonify({"error": "Rule not found"}), 404

        @bp.route("/services", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def list_services() -> Response:
            """List available services."""
            return jsonify(manager.get_available_services())

        @bp.route("/ipsets/<set_name>", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        def add_to_set(set_name: str) -> Tuple[Response, int]:
            """Add IP to set."""
            data = request.get_json() or {}
            address = data.get("address")

            if not address:
                return jsonify({"error": "address required"}), 400

            success = manager.add_to_ipset(set_name, address)
            if success:
                AuditLog.log_operation(
                    user_id=current_user.id,
                    operation="update",
                    resource_type="system",
                    action="firewall_ipset_add",
                    status="success",
                    request_data={"set_name": set_name, "address": address},
                    ip_address=request.remote_addr,
                )
                return jsonify({"status": "added"}), 200
            return jsonify({"error": "IP set not found"}), 404

        @bp.route("/apply", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        def apply_firewall() -> Tuple[Response, int]:
            """Apply firewall configuration."""
            dry_run = request.args.get("dry_run", "false").lower() == "true"
            success, message = manager.apply(dry_run)

            if success:
                if not dry_run:
                    AuditLog.log_operation(
                        user_id=current_user.id,
                        operation="update",
                        resource_type="system",
                        action="firewall_apply",
                        status="success",
                        ip_address=request.remote_addr,
                    )
                return jsonify(
                    {
                        "status": "applied" if not dry_run else "validated",
                        "config": message if dry_run else None,
                    }
                ), 200
            return jsonify({"error": message}), 500

        @bp.route("/blocked", methods=["GET"])
        @require_permission(Resource.SYSTEM, Action.READ)
        def get_blocked() -> Response:
            """Get blocked IPs."""
            return jsonify({"blocked": list(manager.get_blocked_ips())})

        @bp.route("/block", methods=["POST"])
        @require_permission(Resource.SYSTEM, Action.UPDATE)
        def block_ip() -> Tuple[Response, int]:
            """Block an IP."""
            data = request.get_json() or {}
            ip = data.get("ip")
            reason = data.get("reason", "Manual block")

            if not ip:
                return jsonify({"error": "ip required"}), 400

            manager.block_ip(ip, reason)
            AuditLog.log_operation(
                user_id=current_user.id,
                operation="update",
                resource_type="system",
                action="firewall_block_ip",
                status="success",
                request_data={"ip": ip, "reason": reason},
                ip_address=request.remote_addr,
            )
            return jsonify({"status": "blocked"}), 200

        return bp

    except ImportError:
        logger.warning("Flask not available for firewall blueprint")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
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
]
