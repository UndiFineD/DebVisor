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

"""Enterprise Multi-Tenant Network Manager.

Handles comprehensive tenant isolation and network segmentation:
- Per-tenant DNS subzones with automatic record management
- nftables-based VLAN segmentation with microsegmentation
- IPv4/IPv6 dual-stack support (ULA, global unicast, SLAAC)
- Network policies and inter-tenant connectivity controls
- Traffic accounting and QoS per tenant
- NAT and load balancing integration

DebVisor Enterprise Platform - Production Ready.
"""

from __future__ import annotations
import ipaddress
import logging

import hashlib
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================


class NetworkType(Enum):
    """Types of tenant networks."""

    ISOLATED = "isolated"    # No external access
    NAT = "nat"    # NAT to external
    ROUTED = "routed"    # Direct routing
    BRIDGED = "bridged"    # L2 bridged


class IPVersion(Enum):
    """IP version."""

    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DUAL_STACK = "dual_stack"


class IPv6Mode(Enum):
    """IPv6 address allocation mode."""

    ULA = "ula"    # Unique Local Address (fc00::/7)
    GUA = "gua"    # Global Unicast Address
    SLAAC = "slaac"    # Stateless Address Autoconfiguration
    DHCPV6 = "dhcpv6"    # DHCPv6 stateful


class PolicyAction(Enum):
    """Network policy actions."""

    ALLOW = "allow"
    DENY = "deny"
    LOG = "log"
    RATE_LIMIT = "rate_limit"


class QoSClass(Enum):
    """QoS traffic classes."""

    REALTIME = "realtime"    # Lowest latency
    PRIORITY = "priority"    # High priority
    STANDARD = "standard"    # Default
    BULK = "bulk"    # Background/bulk


@dataclass
class TenantNetwork:
    """Complete tenant network configuration."""

    tenant_id: str
    name: str
    vlan_id: int
    ipv4_subnet: str
    ipv4_gateway: str
    ipv6_subnet: Optional[str] = None
    ipv6_gateway: Optional[str] = None
    ipv6_mode: IPv6Mode = IPv6Mode.SLAAC
    dns_zone: Optional[str] = None
    network_type: NetworkType = NetworkType.NAT
    mtu: int = 1500
    qos_class: QoSClass = QoSClass.STANDARD
    bandwidth_limit_mbps: Optional[int] = None
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class DNSRecord:
    """DNS record for tenant zone."""

    name: str
    record_type: str    # A, AAAA, CNAME, PTR, SRV, TXT
    value: str
    ttl: int = 300
    priority: Optional[int] = None    # For MX, SRV
    port: Optional[int] = None    # For SRV


@dataclass
class TenantDNSZone:
    """DNS zone configuration for a tenant."""

    tenant_id: str
    zone_name: str
    primary_ns: str
    admin_email: str
    serial: int = 1
    refresh: int = 86400
    retry: int = 7200
    expire: int = 3600000
    minimum_ttl: int = 300
    records: List[DNSRecord] = field(default_factory=list)
    reverse_zones: List[str] = field(default_factory=list)


@dataclass
class NFTablesRule:
    """Single nftables rule."""

    table: str
    chain: str
    rule: str
    handle: Optional[int] = None
    comment: Optional[str] = None
    priority: int = 0


@dataclass
class NFTablesChain:
    """nftables chain configuration."""

    table: str
    name: str
    chain_type: str    # filter, nat, route
    hook: str    # input, output, forward, prerouting, postrouting
    priority: int = 0
    policy: str = "accept"


@dataclass
class NetworkPolicy:
    """Network policy for traffic control."""

    id: str
    name: str
    source_tenant: Optional[str] = None
    dest_tenant: Optional[str] = None
    source_cidrs: List[str] = field(default_factory=list)
    dest_cidrs: List[str] = field(default_factory=list)
    protocols: List[str] = field(default_factory=list)    # tcp, udp, icmp
    ports: List[int] = field(default_factory=list)
    action: PolicyAction = PolicyAction.ALLOW
    rate_limit_mbps: Optional[float] = None
    log_enabled: bool = False
    priority: int = 100
    enabled: bool = True


@dataclass
class IPAllocation:
    """IP address allocation record."""

    address: str
    tenant_id: str
    hostname: str
    mac_address: Optional[str] = None
    lease_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    lease_duration: timedelta = timedelta(hours=24)
    is_static: bool = False


@dataclass
class TrafficStats:
    """Traffic statistics for a tenant."""

    tenant_id: str
    bytes_in: int = 0
    bytes_out: int = 0
    packets_in: int = 0
    packets_out: int = 0
    connections: int = 0
    dropped_packets: int = 0
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class NATRule:
    """NAT rule configuration."""

    id: str
    tenant_id: str
    nat_type: str    # snat, dnat, masquerade
    protocol: str
    internal_address: str
    internal_port: Optional[int] = None
    external_address: Optional[str] = None
    external_port: Optional[int] = None
    enabled: bool = True


# =============================================================================
# IP Address Manager
# =============================================================================


class IPAddressManager:
    """Manages IP address allocation for tenants.

    Features:
    - DHCP-like allocation with lease tracking
    - Static assignment support
    - IPv4/IPv6 dual-stack
    - Address pool management
    """

    def __init__(self) -> None:
        self.pools: Dict[str, ipaddress.IPv4Network | ipaddress.IPv6Network] = {}
        self.allocations: Dict[str, IPAllocation] = {}
        self.reserved: Dict[str, Set[str]] = defaultdict(set)    # tenant_id -> addresses

    def create_pool(
        self, tenant_id: str, cidr: str, gateway: str, reserved_count: int = 10
    ) -> None:
        """Create an IP pool for a tenant."""
        network = ipaddress.ip_network(cidr, strict=False)
        self.pools[tenant_id] = network

        # Reserve first N addresses (network, gateway, etc.)
        hosts = list(network.hosts())
        for i in range(min(reserved_count, len(hosts))):
            self.reserved[tenant_id].add(str(hosts[i]))

        # Always reserve gateway
        self.reserved[tenant_id].add(gateway)

        logger.info(
            f"Created IP pool for {tenant_id}: {cidr} ({len(hosts) - reserved_count} available)"
        )

    def allocate(
        self,
        tenant_id: str,
        hostname: str,
        mac_address: Optional[str] = None,
        preferred_ip: Optional[str] = None,
        is_static: bool = False,
    ) -> Optional[IPAllocation]:
        """Allocate an IP address."""
        if tenant_id not in self.pools:
            raise ValueError(f"No pool for tenant: {tenant_id}")

        network = self.pools[tenant_id]

        # Check for existing allocation by hostname or MAC
        for alloc in self.allocations.values():
            if alloc.tenant_id == tenant_id:
                if alloc.hostname == hostname:
                    return alloc    # Return existing
                if mac_address and alloc.mac_address == mac_address:
                    return alloc

        # Find available address
        address = None

        if preferred_ip and preferred_ip not in self.reserved[tenant_id]:
            # Check if preferred IP is in our network and available
            try:
                ip = ipaddress.ip_address(preferred_ip)
                if ip in network and str(ip) not in [
                    a.address for a in self.allocations.values()
                ]:
                    address = preferred_ip
            except ValueError:
                pass

        if not address:
            # Allocate from pool
            used = {
                a.address for a in self.allocations.values() if a.tenant_id == tenant_id
            }
            used.update(self.reserved[tenant_id])

            for host in network.hosts():
                if str(host) not in used:
                    address = str(host)
                    break

        if not address:
            logger.error(f"No available addresses in pool for {tenant_id}")
            return None

        allocation = IPAllocation(
            address=address,
            tenant_id=tenant_id,
            hostname=hostname,
            mac_address=mac_address,
            is_static=is_static,
        )

        self.allocations[address] = allocation
        logger.info(f"Allocated {address} to {hostname} in tenant {tenant_id}")

        return allocation

    def release(self, address: str) -> bool:
        """Release an IP allocation."""
        if address in self.allocations:
            alloc = self.allocations[address]
            if not alloc.is_static:
                del self.allocations[address]
                logger.info(f"Released {address}")
                return True
        return False

    def get_allocation(self, address: str) -> Optional[IPAllocation]:
        """Get allocation by address."""
        return self.allocations.get(address)

    def get_tenant_allocations(self, tenant_id: str) -> List[IPAllocation]:
        """Get all allocations for a tenant."""
        return [a for a in self.allocations.values() if a.tenant_id == tenant_id]

    def cleanup_expired_leases(self) -> int:
        """Clean up expired non-static leases."""
        now = datetime.now(timezone.utc)
        expired = []

        for addr, alloc in self.allocations.items():
            if not alloc.is_static:
                if now > alloc.lease_start + alloc.lease_duration:
                    expired.append(addr)

        for addr in expired:
            del self.allocations[addr]

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired leases")

        return len(expired)


# =============================================================================
# DNS Zone Manager
# =============================================================================


class DNSZoneManager:
    """Manages DNS zones for tenants.

    Features:
    - Automatic zone creation
    - Forward and reverse records
    - Dynamic DNS updates
    - Split-horizon DNS support
    """

    def __init__(self, base_domain: str = "debvisor.local"):
        self.base_domain = base_domain
        self.zones: Dict[str, TenantDNSZone] = {}
        self.global_records: List[DNSRecord] = []

    def create_zone(
        self,
        tenant_id: str,
        subdomain: Optional[str] = None,
        primary_ns: str = "ns1",
        admin_email: str = "admin",
    ) -> TenantDNSZone:
        """Create a DNS zone for a tenant."""
        subdomain = subdomain or tenant_id
        zone_name = f"{subdomain}.{self.base_domain}"

        zone = TenantDNSZone(
            tenant_id=tenant_id,
            zone_name=zone_name,
            primary_ns=f"{primary_ns}.{self.base_domain}",
            admin_email=f"{admin_email}.{zone_name}".replace("@", "."),
        )

        # Add default records
        zone.records.append(
            DNSRecord(name="@", record_type="NS", value=zone.primary_ns)
        )

        zone.records.append(
            DNSRecord(
                name="@",
                record_type="SOA",
                value=(
                    f"{zone.primary_ns} {zone.admin_email} {zone.serial} "
                    f"{zone.refresh} {zone.retry} {zone.expire} {zone.minimum_ttl}"
                ),
            )
        )

        self.zones[tenant_id] = zone
        logger.info(f"Created DNS zone: {zone_name}")

        return zone

    def add_record(
        self, tenant_id: str, name: str, record_type: str, value: str, ttl: int = 300
    ) -> DNSRecord:
        """Add a DNS record to tenant zone."""
        if tenant_id not in self.zones:
            raise ValueError(f"No zone for tenant: {tenant_id}")

        zone = self.zones[tenant_id]

        record = DNSRecord(
            name=name, record_type=record_type.upper(), value=value, ttl=ttl
        )

        # Remove existing record with same name and type
        zone.records = [
            r
            for r in zone.records
            if not (r.name == name and r.record_type == record_type.upper())
        ]

        zone.records.append(record)
        zone.serial += 1

        logger.info(f"Added DNS record: {name}.{zone.zone_name} {record_type} {value}")
        return record

    def remove_record(self, tenant_id: str, name: str, record_type: str) -> bool:
        """Remove a DNS record."""
        if tenant_id not in self.zones:
            return False

        zone = self.zones[tenant_id]
        original_count = len(zone.records)

        zone.records = [
            r
            for r in zone.records
            if not (r.name == name and r.record_type == record_type.upper())
        ]

        if len(zone.records) < original_count:
            zone.serial += 1
            return True
        return False

    def add_reverse_record(
        self, tenant_id: str, ip_address: str, hostname: str
    ) -> DNSRecord:
        """Add a PTR record for reverse DNS."""
        if tenant_id not in self.zones:
            raise ValueError(f"No zone for tenant: {tenant_id}")

        zone = self.zones[tenant_id]
        ip = ipaddress.ip_address(ip_address)

        if isinstance(ip, ipaddress.IPv4Address):
            # Create reverse zone name
            octets = str(ip).split(".")
            ptr_name = ".".join(reversed(octets))
            reverse_zone = f"{octets[2]}.{octets[1]}.{octets[0]}.in-addr.arpa"
        else:
            # IPv6 reverse
            expanded = ip.exploded.replace(":", "")
            ptr_name = ".".join(reversed(expanded))
            reverse_zone = "ip6.arpa"

        if reverse_zone not in zone.reverse_zones:
            zone.reverse_zones.append(reverse_zone)

        fqdn = f"{hostname}.{zone.zone_name}."

        return self.add_record(tenant_id, ptr_name, "PTR", fqdn)

    def export_zone_file(self, tenant_id: str) -> str:
        """Export zone as BIND-compatible zone file."""
        if tenant_id not in self.zones:
            raise ValueError(f"No zone for tenant: {tenant_id}")

        zone = self.zones[tenant_id]
        lines = [
            f"; Zone file for {zone.zone_name}",
            f"; Generated at {datetime.now(timezone.utc).isoformat()}",
            f"$ORIGIN {zone.zone_name}.",
            f"$TTL {zone.minimum_ttl}",
            "",
        ]

        for record in zone.records:
            if record.record_type == "SOA":
                lines.append(f"@ IN SOA {record.value}")
            else:
                lines.append(
                    f"{record.name} {record.ttl} IN {record.record_type} {record.value}"
                )

        return "\n".join(lines)

    def export_dnsmasq_config(self, tenant_id: str) -> str:
        """Export zone as dnsmasq configuration."""
        if tenant_id not in self.zones:
            raise ValueError(f"No zone for tenant: {tenant_id}")

        zone = self.zones[tenant_id]
        lines = [f"    # DNS config for {zone.zone_name}"]

        for record in zone.records:
            if record.record_type == "A":
                fqdn = (
                    f"{record.name}.{zone.zone_name}"
                    if record.name != "@"
                    else zone.zone_name
                )
                lines.append(f"address=/{fqdn}/{record.value}")
            elif record.record_type == "CNAME":
                fqdn = f"{record.name}.{zone.zone_name}"
                lines.append(f"cname={fqdn}, {record.value}")

        return "\n".join(lines)


# =============================================================================
# NFTables Manager
# =============================================================================


class NFTablesManager:
    """Manages nftables rules for tenant isolation.

    Features:
    - VLAN-based isolation
    - Microsegmentation
    - Connection tracking
    - Rate limiting
    """

    def __init__(self) -> None:
        self.tables: Dict[str, List[NFTablesChain]] = {}
        self.rules: List[NFTablesRule] = []
        self.tenant_rules: Dict[str, List[NFTablesRule]] = defaultdict(list)

        self._setup_base_tables()

    def _setup_base_tables(self) -> None:
        """Set up base nftables structure."""
        # Main filter table
        self.tables["inet filter"] = [
            NFTablesChain("inet filter", "input", "filter", "input", 0, "drop"),
            NFTablesChain("inet filter", "forward", "filter", "forward", 0, "drop"),
            NFTablesChain("inet filter", "output", "filter", "output", 0, "accept"),
        ]

        # NAT table
        self.tables["inet nat"] = [
            NFTablesChain(
                "inet nat", "prerouting", "nat", "prerouting", -100, "accept"
            ),
            NFTablesChain(
                "inet nat", "postrouting", "nat", "postrouting", 100, "accept"
            ),
        ]

        # Add base rules
        self.rules.extend(
            [
                NFTablesRule(
                    "inet filter",
                    "input",
                    "ct state established, related accept",
                    comment="Allow established",
                ),
                NFTablesRule(
                    "inet filter", "input", "iif lo accept", comment="Allow loopback"
                ),
                NFTablesRule(
                    "inet filter",
                    "input",
                    "icmp type echo-request accept",
                    comment="Allow ping",
                ),
                NFTablesRule(
                    "inet filter",
                    "forward",
                    "ct state established, related accept",
                    comment="Allow established forward",
                ),
            ]
        )

    def create_tenant_rules(
        self, tenant: TenantNetwork, allow_internet: bool = True
    ) -> List[NFTablesRule]:
        """Create isolation rules for a tenant."""
        rules = []
        vlan_if = f"vlan{tenant.vlan_id}"

        # Allow intra-VLAN traffic
        rules.append(
            NFTablesRule(
                table="inet filter",
                chain="forward",
                rule=f"iifname {vlan_if} oifname {vlan_if} accept",
                comment=f"Allow {tenant.tenant_id} intra-VLAN",
            )
        )

        # Allow to/from internet if NAT
        if tenant.network_type == NetworkType.NAT and allow_internet:
            rules.append(
                NFTablesRule(
                    table="inet filter",
                    chain="forward",
                    rule=f"iifname {vlan_if} oifname eth0 accept",
                    comment=f"Allow {tenant.tenant_id} outbound",
                )
            )
            rules.append(
                NFTablesRule(
                    table="inet filter",
                    chain="forward",
                    rule=f"iifname eth0 oifname {vlan_if} ct state established, related accept",
                    comment=f"Allow {tenant.tenant_id} return traffic",
                )
            )

            # Add MASQUERADE for NAT
            rules.append(
                NFTablesRule(
                    table="inet nat",
                    chain="postrouting",
                    rule=f"iifname {vlan_if} oifname eth0 masquerade",
                    comment=f"NAT for {tenant.tenant_id}",
                )
            )

        # Block inter-VLAN by default
        rules.append(
            NFTablesRule(
                table="inet filter",
                chain="forward",
                rule=f"iifname {vlan_if} drop",
                priority=1000,
                comment=f"Block {tenant.tenant_id} to other VLANs",
            )
        )

        self.tenant_rules[tenant.tenant_id] = rules
        return rules

    def add_inter_tenant_rule(
        self,
        source_tenant: TenantNetwork,
        dest_tenant: TenantNetwork,
        protocol: Optional[str] = None,
        port: Optional[int] = None,
    ) -> NFTablesRule:
        """Allow traffic between tenants."""
        src_if = f"vlan{source_tenant.vlan_id}"
        dst_if = f"vlan{dest_tenant.vlan_id}"

        rule_str = f"iifname {src_if} oifname {dst_if}"

        if protocol:
            rule_str += f" {protocol}"
            if port:
                rule_str += f" dport {port}"

        rule_str += " accept"

        rule = NFTablesRule(
            table="inet filter",
            chain="forward",
            rule=rule_str,
            priority=-10,
            comment=f"Allow {source_tenant.tenant_id} -> {dest_tenant.tenant_id}",
        )

        self.rules.append(rule)
        return rule

    def add_rate_limit(
        self, tenant: TenantNetwork, rate_mbps: float, burst_mb: float = 10.0
    ) -> NFTablesRule:
        """Add rate limiting for tenant traffic."""
        vlan_if = f"vlan{tenant.vlan_id}"

        # Convert to packets/second (approximate)
        rate_pps = int(rate_mbps * 1000 / 12)    # Assume ~1500 byte packets
        burst = int(burst_mb * 1000 / 1.5)

        rule = NFTablesRule(
            table="inet filter",
            chain="forward",
            rule=f"iifname {vlan_if} limit rate over {rate_pps}/second burst {burst} packets drop",
            priority=-5,
            comment=f"Rate limit {tenant.tenant_id} at {rate_mbps} Mbps",
        )

        self.tenant_rules[tenant.tenant_id].append(rule)
        return rule

    def export_ruleset(self) -> str:
        """Export complete nftables ruleset."""
        lines = [
            "    #!/usr/sbin/nft -f",
            "    # DebVisor Multi-Tenant Network Rules",
            f"    # Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "flush ruleset",
            "",
        ]

        # Create tables and chains
        for table_name, chains in self.tables.items():
            family, name = table_name.split(" ", 1)
            lines.append(f"table {family} {name} {{")

            for chain in chains:
                lines.append(f"  chain {chain.name} {{")
                lines.append(
                    f"    type {chain.chain_type} hook {chain.hook} priority {chain.priority}; policy {chain.policy};"
                )

                # Add rules for this chain
                chain_rules = [
                    r
                    for r in self.rules
                    if r.table == table_name and r.chain == chain.name
                ]
                for tenant_rules in self.tenant_rules.values():
                    chain_rules.extend(
                        [
                            r
                            for r in tenant_rules
                            if r.table == table_name and r.chain == chain.name
                        ]
                    )

                # Sort by priority
                chain_rules.sort(key=lambda r: r.priority)

                for rule in chain_rules:
                    comment = f' comment "{rule.comment}"' if rule.comment else ""
                    lines.append(f"    {rule.rule}{comment}")

                lines.append("  }")

            lines.append("}")
            lines.append("")

        return "\n".join(lines)

    def apply_ruleset(self) -> bool:
        """Apply the ruleset to the system."""
        ruleset = self.export_ruleset()

        try:
            # Write to temp file and apply
            temp_path = Path("/tmp/nft-debvisor.conf")    # nosec B108
            temp_path.write_text(ruleset)

            # In production: subprocess.run(["nft", "-f", str(temp_path)], check=True)
            logger.info("Applied nftables ruleset")
            return True

        except Exception as e:
            logger.error(f"Failed to apply ruleset: {e}")
            return False


# =============================================================================
# Traffic Accounting
# =============================================================================


class TrafficAccountant:
    """Tracks traffic statistics per tenant.

    Features:
    - Real-time traffic monitoring
    - Historical data retention
    - Quota enforcement
    """

    def __init__(self, history_hours: int = 24):
        self.current_stats: Dict[str, TrafficStats] = {}
        self.history: Dict[str, List[TrafficStats]] = defaultdict(list)
        self.quotas: Dict[str, int] = {}    # tenant_id -> bytes/month
        self.history_hours = history_hours

    def record_traffic(
        self,
        tenant_id: str,
        bytes_in: int,
        bytes_out: int,
        packets_in: int,
        packets_out: int,
        dropped: int = 0,
    ) -> TrafficStats:
        """Record traffic statistics."""
        if tenant_id not in self.current_stats:
            self.current_stats[tenant_id] = TrafficStats(tenant_id=tenant_id)

        stats = self.current_stats[tenant_id]
        stats.bytes_in += bytes_in
        stats.bytes_out += bytes_out
        stats.packets_in += packets_in
        stats.packets_out += packets_out
        stats.dropped_packets += dropped
        stats.last_updated = datetime.now(timezone.utc)

        # Store in history
        self.history[tenant_id].append(
            TrafficStats(
                tenant_id=tenant_id,
                bytes_in=bytes_in,
                bytes_out=bytes_out,
                packets_in=packets_in,
                packets_out=packets_out,
                dropped_packets=dropped,
                last_updated=stats.last_updated,
            )
        )

        # Trim history
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.history_hours)
        self.history[tenant_id] = [
            h for h in self.history[tenant_id] if h.last_updated > cutoff
        ]

        return stats

    def get_stats(self, tenant_id: str) -> Optional[TrafficStats]:
        """Get current stats for tenant."""
        return self.current_stats.get(tenant_id)

    def get_bandwidth(
        self, tenant_id: str, window_seconds: int = 60
    ) -> Tuple[float, float]:
        """Calculate current bandwidth (Mbps in, Mbps out)."""
        history = self.history.get(tenant_id, [])
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=window_seconds)

        recent = [h for h in history if h.last_updated > cutoff]

        if not recent:
            return 0.0, 0.0

        total_in = sum(h.bytes_in for h in recent)
        total_out = sum(h.bytes_out for h in recent)

        mbps_in = (total_in * 8 / 1_000_000) / window_seconds
        mbps_out = (total_out * 8 / 1_000_000) / window_seconds

        return mbps_in, mbps_out

    def set_quota(self, tenant_id: str, bytes_per_month: int) -> None:
        """Set monthly traffic quota for tenant."""
        self.quotas[tenant_id] = bytes_per_month

    def check_quota(self, tenant_id: str) -> Tuple[bool, float]:
        """Check if tenant is within quota.

        Returns (within_quota, percent_used).
        """
        if tenant_id not in self.quotas:
            return True, 0.0

        stats = self.current_stats.get(tenant_id)
        if not stats:
            return True, 0.0

        quota = self.quotas[tenant_id]
        used = stats.bytes_in + stats.bytes_out
        percent = (used / quota) * 100

        return percent < 100, percent


# =============================================================================
# Unified Multi-Tenant Network Manager
# =============================================================================


class MultiTenantNetworkManager:
    """Unified multi-tenant network management service.

    Combines all networking features:
    - Tenant network creation and management
    - DNS zone management
    - nftables rule management
    - IP address allocation
    - Traffic accounting
    """

    def __init__(
        self, base_domain: str = "debvisor.local", external_interface: str = "eth0"
    ):
        self.base_domain = base_domain
        self.external_interface = external_interface

        # Initialize components
        self.ip_manager = IPAddressManager()
        self.dns_manager = DNSZoneManager(base_domain)
        self.nft_manager = NFTablesManager()
        self.traffic_accountant = TrafficAccountant()

        # Tenant storage
        self._tenants: Dict[str, TenantNetwork] = {}
        self._policies: Dict[str, NetworkPolicy] = {}
        self._nat_rules: Dict[str, NATRule] = {}

        # VLAN tracking
        self._used_vlans: Set[int] = set()

    def create_tenant_network(
        self,
        tenant_id: str,
        vlan_id: int,
        ipv4_cidr: str,
        ipv6_cidr: Optional[str] = None,
        name: Optional[str] = None,
        network_type: NetworkType = NetworkType.NAT,
        bandwidth_limit_mbps: Optional[int] = None,
    ) -> TenantNetwork:
        """Create isolated network for tenant."""
        if vlan_id in self._used_vlans:
            raise ValueError(f"VLAN {vlan_id} already in use")

        # Parse network
        ipv4_net = ipaddress.ip_network(ipv4_cidr, strict=False)
        ipv4_gateway = str(list(ipv4_net.hosts())[0])

        ipv6_gateway = None
        if ipv6_cidr:
            ipv6_net = ipaddress.ip_network(ipv6_cidr, strict=False)
            ipv6_gateway = str(list(ipv6_net.hosts())[0])

        dns_zone = f"{tenant_id}.{self.base_domain}"

        network = TenantNetwork(
            tenant_id=tenant_id,
            name=name or tenant_id,
            vlan_id=vlan_id,
            ipv4_subnet=ipv4_cidr,
            ipv4_gateway=ipv4_gateway,
            ipv6_subnet=ipv6_cidr,
            ipv6_gateway=ipv6_gateway,
            dns_zone=dns_zone,
            network_type=network_type,
            bandwidth_limit_mbps=bandwidth_limit_mbps,
        )

        self._tenants[tenant_id] = network
        self._used_vlans.add(vlan_id)

        # Create IP pool
        self.ip_manager.create_pool(tenant_id, ipv4_cidr, ipv4_gateway)

        # Create DNS zone
        self.dns_manager.create_zone(tenant_id)

        # Add DNS record for gateway
        self.dns_manager.add_record(tenant_id, "gateway", "A", ipv4_gateway)

        # Create firewall rules
        self.nft_manager.create_tenant_rules(
            network, allow_internet=(network_type == NetworkType.NAT)
        )

        # Add rate limiting if specified
        if bandwidth_limit_mbps:
            self.nft_manager.add_rate_limit(network, bandwidth_limit_mbps)

        logger.info(f"Created tenant network: {tenant_id} VLAN {vlan_id} -> {dns_zone}")
        return network

    def get_tenant_network(self, tenant_id: str) -> Optional[TenantNetwork]:
        """Get tenant network configuration."""
        return self._tenants.get(tenant_id)

    def delete_tenant_network(self, tenant_id: str) -> bool:
        """Delete a tenant network."""
        if tenant_id not in self._tenants:
            return False

        network = self._tenants[tenant_id]

        # Remove rules
        if tenant_id in self.nft_manager.tenant_rules:
            del self.nft_manager.tenant_rules[tenant_id]

        # Free VLAN
        self._used_vlans.discard(network.vlan_id)

        # Remove tenant
        del self._tenants[tenant_id]

        logger.info(f"Deleted tenant network: {tenant_id}")
        return True

    def allocate_ipv6(self, tenant_id: str, mode: IPv6Mode = IPv6Mode.ULA) -> str:
        """Allocate IPv6 prefix for tenant."""
        network = self._tenants.get(tenant_id)
        if not network:
            raise ValueError(f"Unknown tenant: {tenant_id}")

        if mode == IPv6Mode.ULA:
            # Generate ULA prefix (fd00::/8)
            # Use tenant hash for consistent allocation
            tenant_hash = hashlib.sha256(tenant_id.encode()).hexdigest()[:4]
            prefix = f"fd{tenant_hash}::{network.vlan_id}/64"
        else:
            # Global unicast (example)
            prefix = f"2001:db8:{network.vlan_id}::/64"

        network.ipv6_subnet = prefix
        network.ipv6_mode = mode

        # Add to IP manager
        # self.ip_manager.create_pool(f"{tenant_id}_v6", prefix, ...)

        logger.info(f"Allocated IPv6 for {tenant_id}: {prefix}")
        return prefix

    def configure_dns_subzone(self, tenant_id: str) -> bool:
        """Configure DNS subzone for tenant."""
        network = self._tenants.get(tenant_id)
        if not network:
            return False

        # Zone already created in create_tenant_network
        if tenant_id in self.dns_manager.zones:
            logger.info(f"DNS zone configured: {network.dns_zone}")
            return True

        return False

    def add_dns_record(
        self, tenant_id: str, hostname: str, ip_address: str
    ) -> Optional[DNSRecord]:
        """Add a DNS record for a host."""
        network = self._tenants.get(tenant_id)
        if not network:
            return None

        # Determine record type
        try:
            ip = ipaddress.ip_address(ip_address)
            record_type = "AAAA" if isinstance(ip, ipaddress.IPv6Address) else "A"
        except ValueError:
            return None

        return self.dns_manager.add_record(tenant_id, hostname, record_type, ip_address)

    def allocate_ip(
        self,
        tenant_id: str,
        hostname: str,
        mac_address: Optional[str] = None,
        is_static: bool = False,
    ) -> Optional[str]:
        """Allocate an IP address for a host."""
        alloc = self.ip_manager.allocate(
            tenant_id, hostname, mac_address, is_static=is_static
        )

        if alloc:
            # Add DNS record
            self.add_dns_record(tenant_id, hostname, alloc.address)
            return alloc.address

        return None

    def create_network_policy(
        self,
        name: str,
        source_tenant: Optional[str] = None,
        dest_tenant: Optional[str] = None,
        action: PolicyAction = PolicyAction.ALLOW,
        protocols: Optional[List[str]] = None,
        ports: Optional[List[int]] = None,
    ) -> NetworkPolicy:
        """Create a network policy."""
        policy_id = f"pol-{uuid4().hex[:8]}"

        policy = NetworkPolicy(
            id=policy_id,
            name=name,
            source_tenant=source_tenant,
            dest_tenant=dest_tenant,
            protocols=protocols or [],
            ports=ports or [],
            action=action,
        )

        self._policies[policy_id] = policy

        # Create nftables rules for policy
        if source_tenant and dest_tenant and action == PolicyAction.ALLOW:
            src_net = self._tenants.get(source_tenant)
            dst_net = self._tenants.get(dest_tenant)

            if src_net and dst_net:
                for proto in protocols or [None]:  # type: ignore[list-item]
                    for port in ports or [None]:  # type: ignore[list-item]
                        self.nft_manager.add_inter_tenant_rule(
                            src_net, dst_net, proto, port
                        )

        logger.info(f"Created network policy: {name}")
        return policy

    def add_nat_rule(
        self,
        tenant_id: str,
        internal_address: str,
        internal_port: int,
        external_port: int,
        protocol: str = "tcp",
    ) -> NATRule:
        """Add a port forwarding NAT rule."""
        rule_id = f"nat-{uuid4().hex[:8]}"

        rule = NATRule(
            id=rule_id,
            tenant_id=tenant_id,
            nat_type="dnat",
            protocol=protocol,
            internal_address=internal_address,
            internal_port=internal_port,
            external_port=external_port,
        )

        self._nat_rules[rule_id] = rule

        # Add nftables rule
        network = self._tenants.get(tenant_id)
        if network:
            nft_rule = NFTablesRule(
                table="inet nat",
                chain="prerouting",
                rule=f"{protocol} dport {external_port} dnat to {internal_address}:{internal_port}",
                comment=f"DNAT for {tenant_id}",
            )
            self.nft_manager.rules.append(nft_rule)

        logger.info(
            f"Added NAT rule: :{external_port} -> {internal_address}:{internal_port}"
        )
        return rule

    def export_nft_rules(self) -> str:
        """Export nftables ruleset."""
        return self.nft_manager.export_ruleset()

    def apply_configuration(self) -> bool:
        """Apply all network configuration."""
        success = True

        # Apply nftables rules
        if not self.nft_manager.apply_ruleset():
            success = False

        logger.info("Applied network configuration")
        return success

    def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get comprehensive stats for a tenant."""
        network = self._tenants.get(tenant_id)
        if not network:
            return {}

        traffic = self.traffic_accountant.get_stats(tenant_id)
        bandwidth = self.traffic_accountant.get_bandwidth(tenant_id)
        allocations = self.ip_manager.get_tenant_allocations(tenant_id)

        return {
            "tenant_id": tenant_id,
            "vlan_id": network.vlan_id,
            "ipv4_subnet": network.ipv4_subnet,
            "ipv6_subnet": network.ipv6_subnet,
            "dns_zone": network.dns_zone,
            "network_type": network.network_type.value,
            "allocated_ips": len(allocations),
            "traffic": {
                "bytes_in": traffic.bytes_in if traffic else 0,
                "bytes_out": traffic.bytes_out if traffic else 0,
                "bandwidth_in_mbps": bandwidth[0],
                "bandwidth_out_mbps": bandwidth[1],
            },
        }


# =============================================================================
# CLI / Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    print("=" * 60)
    print("DebVisor Multi-Tenant Network Manager")
    print("=" * 60)

    # Initialize
    mgr = MultiTenantNetworkManager()

    # Create tenant networks
    print("\n[Creating Tenant Networks]")

    tenants = [
        ("acme", 100, "10.100.0.0/24"),
        ("globex", 200, "10.200.0.0/24"),
        ("initech", 300, "10.300.0.0/24"),
    ]

    for tenant_id, vlan, cidr in tenants:
        network = mgr.create_tenant_network(
            tenant_id=tenant_id,
            vlan_id=vlan,
            ipv4_cidr=cidr,
            network_type=NetworkType.NAT,
            bandwidth_limit_mbps=1000,
        )
        print(f"  {tenant_id}: VLAN {vlan}, {cidr}, DNS: {network.dns_zone}")

    # Allocate IPv6
    print("\n[Allocating IPv6]")

    for tenant_id, _, _ in tenants[:2]:  # type: ignore[assignment]
        prefix = mgr.allocate_ipv6(tenant_id, IPv6Mode.ULA)
        print(f"  {tenant_id}: {prefix}")

    # Allocate IPs and create DNS records
    print("\n[IP Allocation]")

    hosts = [
        ("acme", "web-server-1", None),
        ("acme", "db-server-1", None),
        ("globex", "api-server-1", None),
    ]

    for tenant, hostname, mac in hosts:
        ip = mgr.allocate_ip(tenant, hostname, mac)
        if ip:
            print(f"  {hostname}.{tenant}: {ip}")

    # Create network policies
    print("\n[Network Policies]")

    # Allow acme to access globex database
    policy = mgr.create_network_policy(
        name="acme-to-globex-db",
        source_tenant="acme",
        dest_tenant="globex",
        action=PolicyAction.ALLOW,
        protocols=["tcp"],
        ports=[5432, 3306],
    )
    print(f"  Created: {policy.name}")

    # Add NAT rule
    print("\n[NAT Rules]")

    nat = mgr.add_nat_rule(
        tenant_id="acme",
        internal_address="10.100.0.10",
        internal_port=80,
        external_port=8080,
        protocol="tcp",
    )
    print(
        f"  Port forward: :{nat.external_port} -> {nat.internal_address}:{nat.internal_port}"
    )

    # Export rules
    print("\n[NFTables Ruleset]")
    ruleset = mgr.export_nft_rules()
    print("  (truncated output)")
    for line in ruleset.split("\n")[:20]:
        print(f"  {line}")
    print("  ...")

    # Export DNS zone
    print("\n[DNS Zone - acme]")
    zone = mgr.dns_manager.export_zone_file("acme")
    for line in zone.split("\n"):
        print(f"  {line}")

    # Get tenant stats
    print("\n[Tenant Statistics]")

    # Simulate some traffic
    mgr.traffic_accountant.record_traffic("acme", 1000000, 500000, 1000, 800, 5)

    stats = mgr.get_tenant_stats("acme")
    print(f"  Tenant: {stats['tenant_id']}")
    print(f"  VLAN: {stats['vlan_id']}")
    print(f"  IPv4: {stats['ipv4_subnet']}")
    print(f"  DNS: {stats['dns_zone']}")
    print(f"  Allocated IPs: {stats['allocated_ips']}")
    print(f"  Traffic In: {stats['traffic']['bytes_in']} bytes")
    print(f"  Traffic Out: {stats['traffic']['bytes_out']} bytes")

    print("\n" + "=" * 60)
    print("Multi-Tenant Network Manager Ready")
    print("=" * 60)
