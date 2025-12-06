#!/usr/bin/env python3
"""
Comprehensive tests for netcfg-tui network configuration system.

Tests for:
  - IP address configuration
  - Interface management
  - Bond configuration
  - VLAN configuration
  - Bridge configuration
  - Network backends (iproute2, nmcli)
  - Configuration management and backups
  - Validation and safety features
"""

import unittest
from datetime import datetime

from pathlib import Path

from netcfg_tui_full import (
    IPAddress, InterfaceConfig, BondConfiguration, VLANConfiguration,
    BridgeConfiguration, InterfaceStatus, InterfaceType, ConnectionState,
    AddressFamily, BondMode, Iproute2Backend, NmcliBackend,
    NetworkConfigurationManager, ConfigurationBackup
)

class TestIPAddress(unittest.TestCase):
    """Tests for IP address configuration."""

    def test_create_ipv4_address(self):
        """Test creating IPv4 address."""
        addr = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4,
            gateway="192.168.1.1"
        )

        self.assertEqual(addr.address, "192.168.1.100")
        self.assertEqual(addr.netmask, 24)
        self.assertTrue(addr.is_valid())

    def test_create_ipv6_address(self):
        """Test creating IPv6 address."""
        addr = IPAddress(
            address="2001:db8::1",
            netmask=64,
            family=AddressFamily.IPV6
        )

        self.assertEqual(addr.family, AddressFamily.IPV6)
        self.assertTrue(addr.is_valid())

    def test_invalid_netmask_ipv4(self):
        """Test invalid IPv4 netmask."""
        addr = IPAddress(
            address="192.168.1.1",
            netmask=33,
            family=AddressFamily.IPV4
        )

        self.assertFalse(addr.is_valid())

    def test_invalid_netmask_ipv6(self):
        """Test invalid IPv6 netmask."""
        addr = IPAddress(
            address="2001:db8::1",
            netmask=129,
            family=AddressFamily.IPV6
        )

        self.assertFalse(addr.is_valid())

    def test_ip_address_to_dict(self):
        """Test converting IP address to dictionary."""
        addr = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4,
            gateway="192.168.1.1",
            dns_servers=["8.8.8.8", "8.8.4.4"]
        )

        addr_dict = addr.to_dict()

        self.assertEqual(addr_dict["address"], "192.168.1.100")
        self.assertEqual(addr_dict["netmask"], 24)
        self.assertEqual(len(addr_dict["dns_servers"]), 2)

class TestInterfaceConfig(unittest.TestCase):
    """Tests for interface configuration."""

    def test_create_interface(self):
        """Test creating interface."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET,
            mtu=1500,
            enabled=True
        )

        self.assertEqual(config.name, "eth0")
        self.assertEqual(config.interface_type, InterfaceType.ETHERNET)

    def test_add_address_to_interface(self):
        """Test adding address to interface."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        addr = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4
        )

        result = config.add_address(addr)

        self.assertTrue(result)
        self.assertEqual(len(config.addresses), 1)

    def test_add_invalid_address(self):
        """Test adding invalid address."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        addr = IPAddress(
            address="",
            netmask=33,
            family=AddressFamily.IPV4
        )

        result = config.add_address(addr)

        self.assertFalse(result)

    def test_remove_address_from_interface(self):
        """Test removing address from interface."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        addr = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4
        )

        config.add_address(addr)
        result = config.remove_address("192.168.1.100")

        self.assertTrue(result)
        self.assertEqual(len(config.addresses), 0)

    def test_get_primary_address(self):
        """Test getting primary address."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        addr1 = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4,
            is_primary=True
        )

        addr2 = IPAddress(
            address="192.168.1.101",
            netmask=24,
            family=AddressFamily.IPV4,
            is_primary=False
        )

        config.add_address(addr1)
        config.add_address(addr2)

        primary = config.get_primary_address()

        self.assertEqual(primary.address, "192.168.1.100")

class TestBondConfiguration(unittest.TestCase):
    """Tests for bond configuration."""

    def test_create_bond(self):
        """Test creating bond."""
        bond = BondConfiguration(
            name="bond0",
            mode=BondMode.ACTIVE_BACKUP,
            slave_interfaces=["eth0", "eth1"]
        )

        self.assertEqual(bond.name, "bond0")
        self.assertTrue(bond.is_valid())

    def test_invalid_bond_single_slave(self):
        """Test invalid bond with single slave."""
        bond = BondConfiguration(
            name="bond0",
            mode=BondMode.BALANCE_RR,
            slave_interfaces=["eth0"]
        )

        self.assertFalse(bond.is_valid())

    def test_bond_with_lacp_mode(self):
        """Test bond with LACP mode."""
        bond = BondConfiguration(
            name="bond0",
            mode=BondMode.LACP,
            slave_interfaces=["eth0", "eth1", "eth2"]
        )

        self.assertEqual(bond.mode, BondMode.LACP)
        self.assertTrue(bond.is_valid())

class TestVLANConfiguration(unittest.TestCase):
    """Tests for VLAN configuration."""

    def test_create_vlan(self):
        """Test creating VLAN."""
        vlan = VLANConfiguration(
            name="eth0.100",
            parent_interface="eth0",
            vlan_id=100
        )

        self.assertEqual(vlan.vlan_id, 100)
        self.assertTrue(vlan.is_valid())

    def test_invalid_vlan_id_low(self):
        """Test invalid VLAN ID (too low)."""
        vlan = VLANConfiguration(
            name="eth0.0",
            parent_interface="eth0",
            vlan_id=0
        )

        self.assertFalse(vlan.is_valid())

    def test_invalid_vlan_id_high(self):
        """Test invalid VLAN ID (too high)."""
        vlan = VLANConfiguration(
            name="eth0.5000",
            parent_interface="eth0",
            vlan_id=5000
        )

        self.assertFalse(vlan.is_valid())

    def test_valid_vlan_range(self):
        """Test all valid VLAN IDs."""
        for vlan_id in [1, 100, 2000, 4094]:
            vlan = VLANConfiguration(
                name=f"eth0.{vlan_id}",
                parent_interface="eth0",
                vlan_id=vlan_id
            )

            self.assertTrue(vlan.is_valid())

class TestBridgeConfiguration(unittest.TestCase):
    """Tests for bridge configuration."""

    def test_create_bridge(self):
        """Test creating bridge."""
        bridge = BridgeConfiguration(
            name="br0",
            member_interfaces=["eth0", "eth1"]
        )

        self.assertEqual(bridge.name, "br0")
        self.assertTrue(bridge.is_valid())

    def test_bridge_with_stp(self):
        """Test bridge with STP."""
        bridge = BridgeConfiguration(
            name="br0",
            member_interfaces=["eth0", "eth1"],
            stp_enabled=True,
            forward_delay=15
        )

        self.assertTrue(bridge.stp_enabled)
        self.assertEqual(bridge.forward_delay, 15)

class TestInterfaceStatus(unittest.TestCase):
    """Tests for interface status."""

    def test_interface_status_up(self):
        """Test interface status up."""
        status = InterfaceStatus(
            name="eth0",
            state=ConnectionState.UP,
            addresses=[],
            mtu=1500,
            physical_address="00:11:22:33:44:55"
        )

        self.assertTrue(status.is_up())

    def test_interface_status_down(self):
        """Test interface status down."""
        status = InterfaceStatus(
            name="eth0",
            state=ConnectionState.DOWN,
            addresses=[],
            mtu=1500,
            physical_address="00:11:22:33:44:55"
        )

        self.assertFalse(status.is_up())

    def test_throughput_calculation(self):
        """Test throughput calculation."""
        status = InterfaceStatus(
            name="eth0",
            state=ConnectionState.UP,
            addresses=[],
            mtu=1500,
            physical_address="00:11:22:33:44:55",
            rx_bytes=1000000,
            tx_bytes=500000
        )

        rx_mbps = status.get_rx_throughput_mbps()
        tx_mbps = status.get_tx_throughput_mbps()

        self.assertGreater(rx_mbps, 0)
        self.assertGreater(tx_mbps, 0)

class TestIproute2Backend(unittest.TestCase):
    """Tests for iproute2 backend."""

    def setUp(self):
        """Set up test fixtures."""
        self.backend = Iproute2Backend()

    def test_create_interface(self):
        """Test creating interface."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        result = self.backend.create_interface(config)

        self.assertTrue(result)

    def test_get_interfaces(self):
        """Test getting interfaces."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)

        interfaces = self.backend.get_interfaces()

        self.assertIn("eth0", interfaces)

    def test_set_interface_up(self):
        """Test bringing interface up."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET,
            enabled=False
        )

        self.backend.create_interface(config)
        result = self.backend.set_interface_up("eth0")

        self.assertTrue(result)
        self.assertTrue(self.backend.interfaces["eth0"].enabled)

    def test_set_interface_down(self):
        """Test bringing interface down."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET,
            enabled=True
        )

        self.backend.create_interface(config)
        result = self.backend.set_interface_down("eth0")

        self.assertTrue(result)
        self.assertFalse(self.backend.interfaces["eth0"].enabled)

    def test_set_ip_address(self):
        """Test setting IP address."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)

        addr = IPAddress(
            address="192.168.1.100",
            netmask=24,
            family=AddressFamily.IPV4
        )

        result = self.backend.set_ip_address("eth0", addr)

        self.assertTrue(result)

class TestNmcliBackend(unittest.TestCase):
    """Tests for nmcli backend."""

    def setUp(self):
        """Set up test fixtures."""
        self.backend = NmcliBackend()

    def test_create_connection(self):
        """Test creating connection."""
        config = InterfaceConfig(
            name="connection1",
            interface_type=InterfaceType.ETHERNET
        )

        result = self.backend.create_connection(config)

        self.assertTrue(result)

    def test_get_connections(self):
        """Test getting connections."""
        config = InterfaceConfig(
            name="connection1",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_connection(config)

        connections = self.backend.get_interfaces()

        self.assertIn("connection1", connections)

class TestNetworkConfigurationManager(unittest.TestCase):
    """Tests for network configuration manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.backend = Iproute2Backend()
        self.manager = NetworkConfigurationManager(self.backend)

    def test_validate_configuration(self):
        """Test configuration validation."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.manager.register_validation_rule(
            "mtu_range",
            lambda cfg: 1500 <= cfg.mtu <= 65535
        )

        valid, errors = self.manager.validate_configuration(config)

        self.assertTrue(valid)

    def test_validation_failure(self):
        """Test validation failure."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET,
            mtu=100  # Too low
        )

        self.manager.register_validation_rule(
            "mtu_range",
            lambda cfg: cfg.mtu >= 1500
        )

        valid, errors = self.manager.validate_configuration(config)

        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)

    def test_create_backup(self):
        """Test creating backup."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)

        backup = self.manager.create_backup(description="Test backup")

        self.assertIsNotNone(backup)
        self.assertEqual(backup.description, "Test backup")
        self.assertIn(backup, self.manager.backups)

    def test_restore_backup(self):
        """Test restoring backup."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)

        backup = self.manager.create_backup()
        result = self.manager.restore_backup(backup.backup_id)

        self.assertTrue(result)

    def test_restore_nonexistent_backup(self):
        """Test restoring nonexistent backup."""
        result = self.manager.restore_backup("nonexistent")

        self.assertFalse(result)

    def test_create_bond(self):
        """Test creating bond."""
        # Create slave interfaces
        eth0 = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )
        eth1 = InterfaceConfig(
            name="eth1",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(eth0)
        self.backend.create_interface(eth1)

        bond = BondConfiguration(
            name="bond0",
            mode=BondMode.ACTIVE_BACKUP,
            slave_interfaces=["eth0", "eth1"]
        )

        result = self.manager.create_bond(bond)

        self.assertTrue(result)

    def test_create_invalid_bond(self):
        """Test creating invalid bond."""
        bond = BondConfiguration(
            name="bond0",
            mode=BondMode.BALANCE_RR,
            slave_interfaces=["eth0"]  # Only one slave
        )

        result = self.manager.create_bond(bond)

        self.assertFalse(result)

    def test_create_vlan(self):
        """Test creating VLAN."""
        eth0 = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(eth0)

        vlan = VLANConfiguration(
            name="eth0.100",
            parent_interface="eth0",
            vlan_id=100
        )

        result = self.manager.create_vlan(vlan)

        self.assertTrue(result)

    def test_create_bridge(self):
        """Test creating bridge."""
        eth0 = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )
        eth1 = InterfaceConfig(
            name="eth1",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(eth0)
        self.backend.create_interface(eth1)

        bridge = BridgeConfiguration(
            name="br0",
            member_interfaces=["eth0", "eth1"]
        )

        result = self.manager.create_bridge(bridge)

        self.assertTrue(result)

    def test_change_log(self):
        """Test change logging."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)
        self.manager.create_backup()

        log = self.manager.get_change_log(hours=1)

        self.assertGreater(len(log), 0)

    def test_export_configuration(self):
        """Test exporting configuration."""
        config = InterfaceConfig(
            name="eth0",
            interface_type=InterfaceType.ETHERNET
        )

        self.backend.create_interface(config)

        export = self.manager.export_configuration()

        self.assertIn("interfaces", export)
        self.assertIn("eth0", export["interfaces"])

if __name__ == "__main__":
    unittest.main()
