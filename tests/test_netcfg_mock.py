#!/usr/bin/env python3
"""
DebVisor Network Configuration TUI - Mock Mode Tests
=====================================================

Comprehensive test suite for the network configuration
mock mode infrastructure.
"""

import os
import sys

# Add netcfg-tui to path before opt/testing to prioritize it
_netcfg_path = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)),
    'opt',
    'netcfg-tui')
if _netcfg_path not in sys.path:
    sys.path.insert(0, _netcfg_path)

from mock_mode import (
    MockInterface,
    MockInterfaceType,
    MockConnectionState,
    MockNetworkState,
    MockNetworkBackend,
    get_mock_state,
    reset_mock_state,
    mock_network_mode,
    verify_operation_logged,
    get_operation_count,
    export_mock_state,
)
import pytest
import json

# Add paths for imports


class TestMockInterface:
    """Tests for MockInterface dataclass."""

    def test_interface_creation(self):
        """Test basic interface creation."""
        iface = MockInterface(
            name="test0",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.UP,
            mac_address="00:11:22:33:44:55"
        )

        assert iface.name == "test0"
        assert iface.type == MockInterfaceType.ETHERNET
        assert iface.state == MockConnectionState.UP
        assert iface.mac_address == "00:11:22:33:44:55"
        assert iface.mtu == 1500  # default

    def test_interface_with_addresses(self):
        """Test interface with IP addresses."""
        iface = MockInterface(
            name="eth0",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.UP,
            mac_address="00:11:22:33:44:55",
            ipv4_addresses=["192.168.1.100/24", "192.168.1.101/24"],
            ipv6_addresses=["fe80::1/64"],
            gateway="192.168.1.1",
            dns_servers=["8.8.8.8", "8.8.4.4"]
        )

        assert len(iface.ipv4_addresses) == 2
        assert len(iface.ipv6_addresses) == 1
        assert iface.gateway == "192.168.1.1"
        assert "8.8.8.8" in iface.dns_servers

    def test_interface_to_dict(self):
        """Test interface serialization to dict."""
        iface = MockInterface(
            name="eth0",
            type=MockInterfaceType.ETHERNET,
            state=MockConnectionState.UP,
            mac_address="00:11:22:33:44:55",
            speed_mbps=1000
        )

        data = iface.to_dict()

        assert data["name"] == "eth0"
        assert data["type"] == "ethernet"
        assert data["state"] == "up"
        assert data["speed_mbps"] == 1000


class TestMockNetworkState:
    """Tests for MockNetworkState singleton."""

    def test_singleton_pattern(self):
        """Test that MockNetworkState is a singleton."""
        state1 = MockNetworkState()
        state2 = MockNetworkState()

        assert state1 is state2

    def test_default_interfaces(self):
        """Test default interfaces are generated."""
        reset_mock_state(seed=42)
        state = get_mock_state()

        # Should have standard interfaces
        assert "lo" in state.interfaces
        assert "eth0" in state.interfaces
        assert "eth1" in state.interfaces
        assert "br0" in state.interfaces
        assert "wlan0" in state.interfaces

    def test_loopback_interface(self):
        """Test loopback interface configuration."""
        reset_mock_state()
        state = get_mock_state()

        lo = state.interfaces["lo"]
        assert lo.type == MockInterfaceType.LOOPBACK
        assert lo.state == MockConnectionState.UP
        assert "127.0.0.1/8" in lo.ipv4_addresses
        assert "::1/128" in lo.ipv6_addresses
        assert lo.mtu == 65536

    def test_ethernet_interface(self):
        """Test ethernet interface configuration."""
        reset_mock_state()
        state = get_mock_state()

        eth0 = state.interfaces["eth0"]
        assert eth0.type == MockInterfaceType.ETHERNET
        assert eth0.state == MockConnectionState.UP
        assert eth0.speed_mbps == 1000
        assert len(eth0.ipv4_addresses) > 0

    def test_wifi_networks_generated(self):
        """Test WiFi networks are generated."""
        reset_mock_state()
        state = get_mock_state()

        assert len(state.wifi_networks) > 0

        # Should have various security types
        securities = [n.security for n in state.wifi_networks]
        assert "WPA2" in securities or "WPA2-Enterprise" in securities

    def test_routes_generated(self):
        """Test routing table is generated."""
        reset_mock_state()
        state = get_mock_state()

        assert len(state.routes) > 0

        # Should have default route
        destinations = [r["destination"] for r in state.routes]
        assert "default" in destinations

    def test_reset_with_different_seeds(self):
        """Test reset with different seeds produces different MACs."""
        reset_mock_state(seed=1)
        state = get_mock_state()
        mac1 = state.interfaces["eth0"].mac_address

        reset_mock_state(seed=2)
        mac2 = state.interfaces["eth0"].mac_address

        assert mac1 != mac2

    def test_operation_logging(self):
        """Test operation logging."""
        reset_mock_state()
        state = get_mock_state()

        initial_count = len(state.operation_log)
        state.log_operation("test_op", {"key": "value"}, True)

        assert len(state.operation_log) == initial_count + 1

        last_log = state.operation_log[-1]
        assert last_log["operation"] == "test_op"
        assert last_log["params"]["key"] == "value"
        assert last_log["result"] == "success"


class TestMockNetworkBackend:
    """Tests for MockNetworkBackend operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset state before each test."""
        reset_mock_state(seed=42)
        self.backend = MockNetworkBackend()

    def test_list_interfaces(self):
        """Test listing all interfaces."""
        interfaces = self.backend.list_interfaces()

        assert isinstance(interfaces, list)
        assert len(interfaces) >= 5

        names = [i["name"] for i in interfaces]
        assert "lo" in names
        assert "eth0" in names

    def test_get_interface(self):
        """Test getting a specific interface."""
        iface = self.backend.get_interface("eth0")

        assert iface is not None
        assert iface["name"] == "eth0"
        assert iface["type"] == "ethernet"

    def test_get_interface_not_found(self):
        """Test getting non-existent interface."""
        iface = self.backend.get_interface("nonexistent0")
        assert iface is None

    def test_set_interface_up(self):
        """Test bringing interface up."""
        # First bring down
        self.backend.set_interface_down("eth1")
        assert self.backend.get_interface("eth1")["state"] == "down"

        # Now bring up
        result = self.backend.set_interface_up("eth1")
        assert result is True
        assert self.backend.get_interface("eth1")["state"] == "up"

    def test_set_interface_down(self):
        """Test bringing interface down."""
        result = self.backend.set_interface_down("eth0")

        assert result is True
        assert self.backend.get_interface("eth0")["state"] == "down"

    def test_set_interface_nonexistent(self):
        """Test operations on non-existent interface."""
        assert self.backend.set_interface_up("fake0") is False
        assert self.backend.set_interface_down("fake0") is False

    def test_add_ipv4_address(self):
        """Test adding IPv4 address."""
        result = self.backend.add_ip_address("eth1", "10.0.0.100/24")

        assert result is True
        iface = self.backend.get_interface("eth1")
        assert "10.0.0.100/24" in iface["ipv4_addresses"]

    def test_add_ipv6_address(self):
        """Test adding IPv6 address."""
        result = self.backend.add_ip_address("eth1", "2001:db8::100/64")

        assert result is True
        iface = self.backend.get_interface("eth1")
        assert "2001:db8::100/64" in iface["ipv6_addresses"]

    def test_add_duplicate_address(self):
        """Test adding duplicate address (should not duplicate)."""
        self.backend.add_ip_address("eth1", "10.0.0.100/24")
        self.backend.add_ip_address("eth1", "10.0.0.100/24")

        iface = self.backend.get_interface("eth1")
        assert iface["ipv4_addresses"].count("10.0.0.100/24") == 1

    def test_remove_ip_address(self):
        """Test removing IP address."""
        self.backend.add_ip_address("eth1", "10.0.0.100/24")
        result = self.backend.remove_ip_address("eth1", "10.0.0.100/24")

        assert result is True
        iface = self.backend.get_interface("eth1")
        assert "10.0.0.100/24" not in iface["ipv4_addresses"]

    def test_set_gateway(self):
        """Test setting gateway."""
        result = self.backend.set_gateway("eth1", "192.168.2.1")

        assert result is True
        assert self.backend.get_interface("eth1")["gateway"] == "192.168.2.1"

    def test_set_dns_servers(self):
        """Test setting DNS servers."""
        result = self.backend.set_dns_servers(["1.1.1.1", "1.0.0.1"])

        assert result is True
        assert verify_operation_logged("set_dns_servers")

    def test_set_mtu_valid(self):
        """Test setting valid MTU."""
        result = self.backend.set_mtu("eth0", 9000)

        assert result is True
        assert self.backend.get_interface("eth0")["mtu"] == 9000

    def test_set_mtu_invalid(self):
        """Test setting invalid MTU."""
        assert self.backend.set_mtu("eth0", 100) is False  # Too low
        assert self.backend.set_mtu("eth0", 10000) is False  # Too high

    def test_create_vlan(self):
        """Test creating VLAN interface."""
        result = self.backend.create_vlan("eth0", 100)

        assert result is True

        vlan = self.backend.get_interface("eth0.100")
        assert vlan is not None
        assert vlan["type"] == "vlan"
        assert vlan["mac_address"] == self.backend.get_interface("eth0")[
            "mac_address"]

    def test_create_vlan_custom_name(self):
        """Test creating VLAN with custom name."""
        result = self.backend.create_vlan("eth0", 200, name="management")

        assert result is True
        assert self.backend.get_interface("management") is not None

    def test_create_vlan_invalid_id(self):
        """Test creating VLAN with invalid ID."""
        assert self.backend.create_vlan("eth0", 0) is False
        assert self.backend.create_vlan("eth0", 4095) is False

    def test_delete_vlan(self):
        """Test deleting VLAN interface."""
        self.backend.create_vlan("eth0", 100)

        result = self.backend.delete_vlan("eth0.100")

        assert result is True
        assert self.backend.get_interface("eth0.100") is None

    def test_delete_non_vlan(self):
        """Test deleting non-VLAN interface fails."""
        assert self.backend.delete_vlan("eth0") is False

    def test_create_bond(self):
        """Test creating bond interface."""
        result = self.backend.create_bond(
            "bond0", ["eth0", "eth1"], mode="active-backup")

        assert result is True

        bond = self.backend.get_interface("bond0")
        assert bond is not None
        assert bond["type"] == "bond"

    def test_create_bond_invalid_slave(self):
        """Test creating bond with invalid slave fails."""
        result = self.backend.create_bond("bond0", ["eth0", "fake0"])
        assert result is False

    def test_create_bridge(self):
        """Test creating bridge interface."""
        result = self.backend.create_bridge("br1", ports=["eth0"])

        assert result is True

        bridge = self.backend.get_interface("br1")
        assert bridge is not None
        assert bridge["type"] == "bridge"


class TestWiFiOperations:
    """Tests for WiFi operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset state before each test."""
        reset_mock_state(seed=42)
        self.backend = MockNetworkBackend()

    def test_scan_wifi(self):
        """Test WiFi scanning."""
        networks = self.backend.scan_wifi("wlan0")

        assert isinstance(networks, list)
        assert len(networks) > 0

        # Check network structure
        network = networks[0]
        assert "ssid" in network
        assert "bssid" in network
        assert "signal_strength" in network
        assert "security" in network

    def test_scan_wifi_non_wifi_interface(self):
        """Test scanning on non-WiFi interface."""
        networks = self.backend.scan_wifi("eth0")
        assert networks == []

    def test_scan_wifi_nonexistent_interface(self):
        """Test scanning on non-existent interface."""
        networks = self.backend.scan_wifi("wlan99")
        assert networks == []

    def test_connect_wifi_open(self):
        """Test connecting to open WiFi."""
        # Find open network
        networks = self.backend.scan_wifi("wlan0")
        open_network = next(
            (n for n in networks if n["security"] == "Open"), None)

        if open_network:
            result = self.backend.connect_wifi("wlan0", open_network["ssid"])
            assert result is True

            # Interface should be up with IP
            iface = self.backend.get_interface("wlan0")
            assert iface["state"] == "up"
            assert len(iface["ipv4_addresses"]) > 0

    def test_connect_wifi_secured(self):
        """Test connecting to secured WiFi."""
        networks = self.backend.scan_wifi("wlan0")
        secured = next((n for n in networks if n["security"] != "Open"), None)

        if secured:
            # Without password should fail
            result = self.backend.connect_wifi("wlan0", secured["ssid"])
            assert result is False

            # With password should succeed
            result = self.backend.connect_wifi(
                "wlan0", secured["ssid"], password="secret123")
            assert result is True

    def test_connect_wifi_nonexistent_network(self):
        """Test connecting to non-existent network."""
        result = self.backend.connect_wifi(
            "wlan0", "NonExistent-Network-12345")
        assert result is False


class TestRoutingOperations:
    """Tests for routing operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset state before each test."""
        reset_mock_state(seed=42)
        self.backend = MockNetworkBackend()

    def test_get_routes(self):
        """Test getting routing table."""
        routes = self.backend.get_routes()

        assert isinstance(routes, list)
        assert len(routes) > 0

        # Check route structure
        route = routes[0]
        assert "destination" in route
        assert "interface" in route

    def test_add_route(self):
        """Test adding a route."""
        initial_count = len(self.backend.get_routes())

        result = self.backend.add_route(
            destination="10.10.0.0/16",
            gateway="192.168.1.254",
            interface="eth0",
            metric=50
        )

        assert result is True
        assert len(self.backend.get_routes()) == initial_count + 1

        # Verify route exists
        routes = self.backend.get_routes()
        new_route = next(
            (r for r in routes if r["destination"] == "10.10.0.0/16"), None)
        assert new_route is not None
        assert new_route["gateway"] == "192.168.1.254"

    def test_delete_route(self):
        """Test deleting a route."""
        # Add route first
        self.backend.add_route("10.10.0.0/16", "192.168.1.254", "eth0")

        result = self.backend.delete_route("10.10.0.0/16")

        assert result is True

        routes = self.backend.get_routes()
        deleted = next(
            (r for r in routes if r["destination"] == "10.10.0.0/16"), None)
        assert deleted is None

    def test_delete_nonexistent_route(self):
        """Test deleting non-existent route."""
        result = self.backend.delete_route("99.99.99.0/24")
        assert result is False


class TestOperationLogging:
    """Tests for operation logging and verification."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset state before each test."""
        reset_mock_state(seed=42)
        self.backend = MockNetworkBackend()

    def test_verify_operation_logged(self):
        """Test operation verification."""
        self.backend.set_interface_up("eth1")

        assert verify_operation_logged("set_interface_up") is True
        assert verify_operation_logged(
            "set_interface_up", {
                "name": "eth1"}) is True
        assert verify_operation_logged("nonexistent_op") is False

    def test_get_operation_count(self):
        """Test operation counting."""
        # Multiple interface operations
        self.backend.set_interface_up("eth1")
        self.backend.set_interface_down("eth1")
        self.backend.set_interface_up("eth1")

        assert get_operation_count("set_interface_up") == 2
        assert get_operation_count("set_interface_down") == 1


class TestMockNetworkContext:
    """Tests for mock_network_mode context manager."""

    def test_context_manager_reset(self):
        """Test context manager resets state."""
        with mock_network_mode(seed=100):
            backend = MockNetworkBackend()
            backend.set_interface_down("eth0")

            assert backend.get_interface("eth0")["state"] == "down"

        # New context should have fresh state
        with mock_network_mode(seed=100):
            backend = MockNetworkBackend()
            assert backend.get_interface("eth0")["state"] == "up"

    def test_context_manager_different_seeds(self):
        """Test context manager with different seeds."""
        with mock_network_mode(seed=1) as state1:
            mac1 = state1.interfaces["eth0"].mac_address

        with mock_network_mode(seed=2) as state2:
            mac2 = state2.interfaces["eth0"].mac_address

        assert mac1 != mac2


class TestExportMockState:
    """Tests for state export functionality."""

    def test_export_state_json(self):
        """Test exporting state as JSON."""
        reset_mock_state(seed=42)

        json_str = export_mock_state()

        # Should be valid JSON
        data = json.loads(json_str)

        assert "interfaces" in data
        assert "wifi_networks" in data
        assert "routes" in data
        assert "operation_log" in data

    def test_export_includes_operations(self):
        """Test export includes logged operations."""
        reset_mock_state()
        backend = MockNetworkBackend()

        backend.set_interface_up("eth1")
        backend.add_ip_address("eth1", "10.0.0.100/24")

        json_str = export_mock_state()
        data = json.loads(json_str)

        assert len(data["operation_log"]) >= 2


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset state before each test."""
        reset_mock_state(seed=42)
        self.backend = MockNetworkBackend()

    def test_operations_on_loopback(self):
        """Test operations on loopback interface."""
        # Should be able to add addresses
        result = self.backend.add_ip_address("lo", "127.0.0.2/8")
        assert result is True

    def test_multiple_ip_addresses(self):
        """Test adding multiple IP addresses to same interface."""
        for i in range(5):
            self.backend.add_ip_address("eth1", f"192.168.{i}.100/24")

        iface = self.backend.get_interface("eth1")
        assert len(iface["ipv4_addresses"]) == 5

    def test_concurrent_interface_types(self):
        """Test managing multiple interface types."""
        # Create various types
        self.backend.create_vlan("eth0", 100)
        self.backend.create_bond("bond0", ["eth0", "eth1"])
        self.backend.create_bridge("br1")

        # Verify all exist
        assert self.backend.get_interface("eth0.100") is not None
        assert self.backend.get_interface("bond0") is not None
        assert self.backend.get_interface("br1") is not None

    def test_state_persistence_across_operations(self):
        """Test state persists correctly across multiple operations."""
        # Perform multiple operations
        self.backend.set_interface_up("eth1")
        self.backend.add_ip_address("eth1", "10.0.0.100/24")
        self.backend.set_gateway("eth1", "10.0.0.1")
        self.backend.set_mtu("eth1", 9000)

        # Verify all changes persisted
        iface = self.backend.get_interface("eth1")
        assert iface["state"] == "up"
        assert "10.0.0.100/24" in iface["ipv4_addresses"]
        assert iface["gateway"] == "10.0.0.1"
        assert iface["mtu"] == 9000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
