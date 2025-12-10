from datetime import datetime
#!/usr/bin/env python3
"""
DebVisor Network Configuration TUI - Mock Mode
===============================================

Provides mock implementations for CI/CD testing of the network
configuration TUI without requiring actual system access.

Features:
- Simulated network interfaces
- Mock NetworkManager/iproute2 operations
- Deterministic test data
- CI environment auto-detection
"""

import os
from typing import Set
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

# Check CI environment
IS_CI = os.getenv("CI", "").lower() in ("true", "1", "yes")
IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
MOCK_ENABLED = os.getenv("NETCFG_MOCK", "").lower() in ("true", "1", "yes") or IS_CI


class MockInterfaceType(Enum):
    """Mock interface types."""

    ETHERNET = "ethernet"
    LOOPBACK = "loopback"
    BRIDGE = "bridge"
    BOND = "bond"
    VLAN = "vlan"
    WIFI = "wifi"


class MockConnectionState(Enum):
    """Mock connection states."""

    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"


@dataclass
class MockInterface:
    """Mock network interface."""

    name: str
    type: MockInterfaceType
    state: MockConnectionState
    mac_address: str
    mtu: int = 1500
    ipv4_addresses: List[str] = field(default_factory=list)
    ipv6_addresses: List[str] = field(default_factory=list)
    gateway: Optional[str] = None
    dns_servers: List[str] = field(default_factory=list)
    speed_mbps: Optional[int] = None
    driver: str = "mock"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "state": self.state.value,
            "mac_address": self.mac_address,
            "mtu": self.mtu,
            "ipv4_addresses": self.ipv4_addresses,
            "ipv6_addresses": self.ipv6_addresses,
            "gateway": self.gateway,
            "dns_servers": self.dns_servers,
            "speed_mbps": self.speed_mbps,
            "driver": self.driver,
        }


@dataclass
class MockWiFiNetwork:
    """Mock WiFi network."""

    ssid: str
    bssid: str
    signal_strength: int    # dBm
    channel: int
    frequency_mhz: int
    security: str    # WPA2, WPA3, Open
    connected: bool = False


class MockNetworkState:
    """Global mock network state manager."""

    _instance: Optional["MockNetworkState"] = None
    _initialized: bool

    def __new__(cls) -> "MockNetworkState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.interfaces: Dict[str, MockInterface] = {}
        self.wifi_networks: List[MockWiFiNetwork] = []
        self.routes: List[Dict[str, Any]] = []
        self.dns_config: Dict[str, Any] = {}
        self.operation_log: List[Dict[str, Any]] = []
        self._seed = 42

        # Initialize default mock data
        self._generate_default_interfaces()
        self._generate_wifi_networks()
        self._generate_routes()

    def reset(self, seed: int = 42) -> None:
        """Reset mock state with optional seed."""
        self._seed = seed
        random.seed(seed)
        self.interfaces.clear()
        self.wifi_networks.clear()
        self.routes.clear()
        self.operation_log.clear()
        self._generate_default_interfaces()
        self._generate_wifi_networks()
        self._generate_routes()

    def _generate_default_interfaces(self) -> None:
        """Generate default mock interfaces."""
        random.seed(self._seed)

        # Loopback
        self.interfaces["lo"] = MockInterface(
            name="lo",
            type=MockInterfaceType.LOOPBACK,
            state=MockConnectionState.UP,
            mac_address="00:00:00:00:00:00",
            mtu=65536,
            ipv4_addresses=["127.0.0.1/8"],
            ipv6_addresses=["::1/128"],
        )

        # Primary Ethernet
        self.interfaces["eth0"] = MockInterface(
            name="eth0",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.UP,
            mac_address=self._generate_mac(),
            mtu=1500,
            ipv4_addresses=["192.168.1.100/24"],
            ipv6_addresses=["fe80::1/64"],
            gateway="192.168.1.1",
            dns_servers=["8.8.8.8", "8.8.4.4"],
            speed_mbps=1000,
            driver="e1000e",
        )

        # Secondary Ethernet (disconnected)
        self.interfaces["eth1"] = MockInterface(
            name="eth1",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.DOWN,
            mac_address=self._generate_mac(),
            mtu=1500,
            speed_mbps=10000,
            driver="ixgbe",
        )

        # Management interface
        self.interfaces["mgmt0"] = MockInterface(
            name="mgmt0",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.UP,
            mac_address=self._generate_mac(),
            mtu=1500,
            ipv4_addresses=["10.0.0.10/24"],
            gateway="10.0.0.1",
            dns_servers=["10.0.0.1"],
            speed_mbps=1000,
            driver="virtio",
        )

        # WiFi interface
        self.interfaces["wlan0"] = MockInterface(
            name="wlan0",
            type=MockInterfaceType.WIFI,
            state=MockConnectionState.DOWN,
            mac_address=self._generate_mac(),
            mtu=1500,
            driver="iwlwifi",
        )

        # Bridge
        self.interfaces["br0"] = MockInterface(
            name="br0",
            type=MockInterfaceType.BRIDGE,
            state=MockConnectionState.UP,
            mac_address=self._generate_mac(),
            mtu=1500,
            ipv4_addresses=["172.16.0.1/24"],
            driver="bridge",
        )

    def _generate_wifi_networks(self) -> None:
        """Generate mock WiFi networks for scanning."""
        random.seed(self._seed + 1)

        networks = [
            ("DebVisor-Corp", "WPA2-Enterprise", -45),
            ("DebVisor-Guest", "WPA2", -55),
            ("Neighbor-5G", "WPA3", -70),
            ("OpenNetwork", "Open", -80),
            ("Hidden-Net", "WPA2", -65),
        ]

        for i, (ssid, security, signal) in enumerate(networks):
            self.wifi_networks.append(
                MockWiFiNetwork(
                    ssid=ssid,
                    bssid=self._generate_mac(),
                    signal_strength=signal + random.randint(-5, 5),    # nosec B311
                    channel=random.choice([1, 6, 11, 36, 40, 44, 48]),    # nosec B311
                    frequency_mhz=2412 if random.random() > 0.5 else 5180,    # nosec B311
                    security=security,
                    connected=False,
                )
            )

    def _generate_routes(self) -> None:
        """Generate mock routing table."""
        self.routes = [
            {
                "destination": "default",
                "gateway": "192.168.1.1",
                "interface": "eth0",
                "metric": 100,
            },
            {
                "destination": "10.0.0.0/24",
                "gateway": "10.0.0.1",
                "interface": "mgmt0",
                "metric": 200,
            },
            {
                "destination": "172.16.0.0/24",
                "gateway": None,
                "interface": "br0",
                "metric": 0,
            },
            {
                "destination": "192.168.1.0/24",
                "gateway": None,
                "interface": "eth0",
                "metric": 100,
            },
        ]

    def _generate_mac(self) -> str:
        """Generate a random MAC address."""
        return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))    # nosec B311

    def log_operation(self, operation: str, params: Dict[str, Any], result: bool) -> None:
        """Log a mock operation for verification."""
        self.operation_log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": operation,
                "params": params,
                "result": "success" if result else "failed",
            }
        )


# Global mock state singleton
_mock_state = MockNetworkState()


def get_mock_state() -> MockNetworkState:
    """Get the global mock network state."""
    return _mock_state


def reset_mock_state(seed: int = 42) -> None:
    """Reset mock state to initial values."""
    _mock_state.reset(seed)


@contextmanager
def mock_network_mode(seed: int = 42) -> Any:
    """Context manager for mock network mode."""
    reset_mock_state(seed)
    try:
        yield _mock_state
    finally:
        pass    # Keep state for inspection


# =============================================================================
# Mock Network Operations
# =============================================================================


class MockNetworkBackend:
    """Mock network backend for testing."""

    def __init__(self) -> None:
        self.state = get_mock_state()

    def list_interfaces(self) -> List[Dict[str, Any]]:
        """List all network interfaces."""
        return [iface.to_dict() for iface in self.state.interfaces.values()]

    def get_interface(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific interface."""
        iface = self.state.interfaces.get(name)
        return iface.to_dict() if iface else None

    def set_interface_up(self, name: str) -> bool:
        """Bring interface up."""
        if name not in self.state.interfaces:
            return False

        self.state.interfaces[name].state = MockConnectionState.UP
        self.state.log_operation("set_interface_up", {"name": name}, True)
        return True

    def set_interface_down(self, name: str) -> bool:
        """Bring interface down."""
        if name not in self.state.interfaces:
            return False

        self.state.interfaces[name].state = MockConnectionState.DOWN
        self.state.log_operation("set_interface_down", {"name": name}, True)
        return True

    def add_ip_address(self, interface: str, address: str) -> bool:
        """Add IP address to interface."""
        if interface not in self.state.interfaces:
            return False

        iface = self.state.interfaces[interface]

        if ":" in address.split("/")[0]:    # IPv6
            if address not in iface.ipv6_addresses:
                iface.ipv6_addresses.append(address)
        else:    # IPv4
            if address not in iface.ipv4_addresses:
                iface.ipv4_addresses.append(address)

        self.state.log_operation(
            "add_ip_address", {"interface": interface, "address": address}, True
        )
        return True

    def remove_ip_address(self, interface: str, address: str) -> bool:
        """Remove IP address from interface."""
        if interface not in self.state.interfaces:
            return False

        iface = self.state.interfaces[interface]

        if ":" in address.split("/")[0]:    # IPv6
            if address in iface.ipv6_addresses:
                iface.ipv6_addresses.remove(address)
        else:    # IPv4
            if address in iface.ipv4_addresses:
                iface.ipv4_addresses.remove(address)

        self.state.log_operation(
            "remove_ip_address", {"interface": interface, "address": address}, True
        )
        return True

    def set_gateway(self, interface: str, gateway: str) -> bool:
        """Set default gateway."""
        if interface not in self.state.interfaces:
            return False

        self.state.interfaces[interface].gateway = gateway
        self.state.log_operation(
            "set_gateway", {"interface": interface, "gateway": gateway}, True
        )
        return True

    def set_dns_servers(self, servers: List[str]) -> bool:
        """Set DNS servers."""
        self.state.dns_config["servers"] = servers
        self.state.log_operation("set_dns_servers", {"servers": servers}, True)
        return True

    def set_mtu(self, interface: str, mtu: int) -> bool:
        """Set interface MTU."""
        if interface not in self.state.interfaces:
            return False

        if not (576 <= mtu <= 9000):
            return False

        self.state.interfaces[interface].mtu = mtu
        self.state.log_operation("set_mtu", {"interface": interface, "mtu": mtu}, True)
        return True

    def create_vlan(
        self, parent: str, vlan_id: int, name: Optional[str] = None
    ) -> bool:
        """Create VLAN interface."""
        if parent not in self.state.interfaces:
            return False

        if not (1 <= vlan_id <= 4094):
            return False

        vlan_name = name or f"{parent}.{vlan_id}"

        self.state.interfaces[vlan_name] = MockInterface(
            name=vlan_name,
            type=MockInterfaceType.VLAN,
            state=MockConnectionState.DOWN,
            mac_address=self.state.interfaces[parent].mac_address,
            mtu=self.state.interfaces[parent].mtu,
            driver="8021q",
        )

        self.state.log_operation(
            "create_vlan",
            {"parent": parent, "vlan_id": vlan_id, "name": vlan_name},
            True,
        )
        return True

    def delete_vlan(self, name: str) -> bool:
        """Delete VLAN interface."""
        if name not in self.state.interfaces:
            return False

        if self.state.interfaces[name].type != MockInterfaceType.VLAN:
            return False

        del self.state.interfaces[name]
        self.state.log_operation("delete_vlan", {"name": name}, True)
        return True

    def create_bond(
        self, name: str, slaves: List[str], mode: str = "active-backup"
    ) -> bool:
        """Create bond interface."""
        # Verify slaves exist
        for slave in slaves:
            if slave not in self.state.interfaces:
                return False

        self.state.interfaces[name] = MockInterface(
            name=name,
            type=MockInterfaceType.BOND,
            state=MockConnectionState.DOWN,
            mac_address=self.state.interfaces[slaves[0]].mac_address,
            mtu=1500,
            driver="bonding",
        )

        self.state.log_operation(
            "create_bond", {"name": name, "slaves": slaves, "mode": mode}, True
        )
        return True

    def create_bridge(self, name: str, ports: Optional[List[str]] = None) -> bool:
        """Create bridge interface."""
        self.state.interfaces[name] = MockInterface(
            name=name,
            type=MockInterfaceType.BRIDGE,
            state=MockConnectionState.DOWN,
            mac_address=get_mock_state()._generate_mac(),
            mtu=1500,
            driver="bridge",
        )

        self.state.log_operation(
            "create_bridge", {"name": name, "ports": ports or []}, True
        )
        return True

    def scan_wifi(self, interface: str = "wlan0") -> List[Dict[str, Any]]:
        """Scan for WiFi networks."""
        if interface not in self.state.interfaces:
            return []

        if self.state.interfaces[interface].type != MockInterfaceType.WIFI:
            return []

        self.state.log_operation("scan_wifi", {"interface": interface}, True)

        return [
            {
                "ssid": net.ssid,
                "bssid": net.bssid,
                "signal_strength": net.signal_strength,
                "channel": net.channel,
                "frequency_mhz": net.frequency_mhz,
                "security": net.security,
                "connected": net.connected,
            }
            for net in self.state.wifi_networks
        ]

    def connect_wifi(
        self, interface: str, ssid: str, password: Optional[str] = None
    ) -> bool:
        """Connect to WiFi network."""
        if interface not in self.state.interfaces:
            return False

        network = next((n for n in self.state.wifi_networks if n.ssid == ssid), None)
        if not network:
            return False

        # Check if password required
        if network.security != "Open" and not password:
            return False

        # Mark as connected
        for net in self.state.wifi_networks:
            net.connected = net.ssid == ssid

        # Bring interface up with IP
        self.state.interfaces[interface].state = MockConnectionState.UP
        self.state.interfaces[interface].ipv4_addresses = ["192.168.50.100/24"]
        self.state.interfaces[interface].gateway = "192.168.50.1"

        self.state.log_operation(
            "connect_wifi", {"interface": interface, "ssid": ssid}, True
        )
        return True

    def get_routes(self) -> List[Dict[str, Any]]:
        """Get routing table."""
        return self.state.routes.copy()

    def add_route(
        self,
        destination: str,
        gateway: Optional[str],
        interface: str,
        metric: int = 100,
    ) -> bool:
        """Add a route."""
        self.state.routes.append(
            {
                "destination": destination,
                "gateway": gateway,
                "interface": interface,
                "metric": metric,
            }
        )
        self.state.log_operation(
            "add_route",
            {
                "destination": destination,
                "gateway": gateway,
                "interface": interface,
                "metric": metric,
            },
            True,
        )
        return True

    def delete_route(self, destination: str) -> bool:
        """Delete a route."""
        original_len = len(self.state.routes)
        self.state.routes = [
            r for r in self.state.routes if r["destination"] != destination
        ]

        deleted = len(self.state.routes) < original_len
        self.state.log_operation("delete_route", {"destination": destination}, deleted)
        return deleted


def get_network_backend() -> MockNetworkBackend:
    """Get the appropriate network backend (mock or real)."""
    if MOCK_ENABLED:
        return MockNetworkBackend()

    # In production, return real backend
    raise NotImplementedError("Real network backend not available in mock module")


# =============================================================================
# Test Helpers
# =============================================================================


def verify_operation_logged(
    operation: str, params: Optional[Dict[str, Any]] = None
) -> bool:
    """Verify an operation was logged."""
    state = get_mock_state()

    for log in state.operation_log:
        if log["operation"] == operation:
            if params is None:
                return True
            if all(log["params"].get(k) == v for k, v in params.items()):
                return True

    return False


def get_operation_count(operation: str) -> int:
    """Get count of a specific operation."""
    state = get_mock_state()
    return sum(1 for log in state.operation_log if log["operation"] == operation)


def export_mock_state() -> str:
    """Export mock state as JSON for debugging."""
    state = get_mock_state()
    return json.dumps(
        {
            "interfaces": {
                name: iface.to_dict() for name, iface in state.interfaces.items()
            },
            "wifi_networks": [
                {
                    "ssid": n.ssid,
                    "bssid": n.bssid,
                    "signal": n.signal_strength,
                    "security": n.security,
                }
                for n in state.wifi_networks
            ],
            "routes": state.routes,
            "operation_log": state.operation_log,
        },
        indent=2,
    )


if __name__ == "__main__":
    # Demo
    print("DebVisor Network Configuration Mock Mode")
    print("=" * 50)

    backend = MockNetworkBackend()

    print("\n[Interfaces]")
    for iface in backend.list_interfaces():
        status = "UP" if iface["state"] == "up" else "DOWN"
        ips = ", ".join(iface["ipv4_addresses"]) or "no IP"
        print(f"  {iface['name']:10} [{status:4}] {iface['type']:10} {ips}")

    print("\n[WiFi Networks]")
    for network in backend.scan_wifi("wlan0"):
        print(
            f"  {network['ssid']:20} {network['signal_strength']:4}dBm {network['security']}"
        )

    print("\n[Routes]")
    for route in backend.get_routes():
        gw = route["gateway"] or "direct"
        print(f"  {route['destination']:20} via {gw:15} dev {route['interface']}")

    # Test some operations
    print("\n[Testing Operations]")

    backend.set_interface_down("eth1")
    eth1 = backend.get_interface("eth1")
    if eth1:
        print(f"  Set eth1 down: {eth1['state']}")

    backend.add_ip_address("eth1", "192.168.2.100/24")
    eth1 = backend.get_interface("eth1")
    if eth1:
        print(f"  Added IP to eth1: {eth1['ipv4_addresses']}")

    backend.set_interface_up("eth1")
    eth1 = backend.get_interface("eth1")
    if eth1:
        print(f"  Set eth1 up: {eth1['state']}")

    backend.create_vlan("eth0", 100)
    print("  Created VLAN: eth0.100")

    print("\n[Operation Log]")
    state = get_mock_state()
    for log in state.operation_log[-5:]:
        print(f"  {log['operation']}: {log['params']} -> {log['result']}")
