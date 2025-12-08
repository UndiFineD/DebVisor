# Network Config TUI - Testing & Enhancement Guide

## Overview

This guide documents testing procedures, enhancement opportunities, and advanced use cases for the DebVisor Network Configuration Terminal User Interface (netcfg-tui).

## Current State

### Implemented Features

- ? Curses-based TUI interface (Legacy)
- ? **New Urwid-based TUI** (`opt/netcfg_tui_app.py`)
- ? Interface detection (wired, wireless, InfiniBand)
- ? Single-bridge default mode
- ? DHCP/static addressing
- ? VLAN configuration
- ? Wi-Fi SSID/PSK support
- ? STP configuration with timer tuning
- ? systemd-networkd output
- ? Netplan output backend
- ? Safe output-only mode (no direct system modification)
- ? Unit tests for configuration generation
- ? --apply flag with sudo support and automatic rollback
- ? Pre-flight validation checks
- ? **Advanced Features:** Bonding, Bridges, VLANs, Rollback, Validation

### Pending Enhancements

- None. All planned enhancements have been implemented.

## Testing Framework

### Unit Tests

Create `tests/test_config_generation.py`:

    #!/usr/bin/env python3
    """Unit tests for network configuration generation."""

    import unittest
    import tempfile
    import os
    import json
    from pathlib import Path

## Import from parent directory

    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(**file**), '..'))

    from netcfg_tui import (
        InterfaceConfig,
        BridgeConfig,
        generate_networkd_network,
        generate_netplan_yaml,
        validate_cidr,
        validate_ipv4_address,
        detect_interfaces,
    )

    class TestInterfaceConfig(unittest.TestCase):
        """Tests for InterfaceConfig class."""

        def test_create_wired_interface(self):
            """Test creating wired interface configuration."""
            iface = InterfaceConfig("eth0", "wired")
            self.assertEqual(iface.name, "eth0")
            self.assertEqual(iface.kind, "wired")
            self.assertEqual(iface.method, "dhcp")

        def test_create_wireless_interface(self):
            """Test creating wireless interface with SSID/PSK."""
            iface = InterfaceConfig("wlan0", "wireless")
            iface.ssid = "MyNetwork"
            iface.psk = "password123"
            self.assertEqual(iface.ssid, "MyNetwork")
            self.assertEqual(iface.psk, "password123")

        def test_vlan_interface(self):
            """Test creating VLAN interface."""
            iface = InterfaceConfig("eth0", "wired")
            iface.vlan_id = 100
            self.assertEqual(iface.vlan_id, 100)
            self.assertIn("vlan=100", iface.summary())

        def test_static_addressing(self):
            """Test static IP configuration."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "static"
            iface.address = "192.168.1.10"
            iface.prefix = 24
            iface.gateway = "192.168.1.1"
            iface.dns = ["8.8.8.8", "8.8.4.4"]

            summary = iface.summary()
            self.assertIn("static", summary)
            self.assertIn("192.168.1.10", summary)
            self.assertIn("gateway", summary)

        def test_infiniband_interface(self):
            """Test InfiniBand interface configuration."""
            iface = InterfaceConfig("ib0", "infiniband")
            iface.method = "static"
            iface.address = "10.0.0.1"
            iface.prefix = 16
            summary = iface.summary()
            self.assertIn("infiniband", summary)

    class TestBridgeConfig(unittest.TestCase):
        """Tests for BridgeConfig class."""

        def test_create_bridge(self):
            """Test creating bridge configuration."""
            bridge = BridgeConfig("br0")
            self.assertEqual(bridge.name, "br0")
            self.assertEqual(bridge.method, "dhcp")
            self.assertTrue(bridge.stp)

        def test_bridge_static_addressing(self):
            """Test bridge with static IP."""
            bridge = BridgeConfig("br0")
            bridge.method = "static"
            bridge.address = "192.168.1.254"
            bridge.prefix = 24
            bridge.gateway = "192.168.1.1"
            bridge.dns = ["8.8.8.8"]

            summary = bridge.summary()
            self.assertIn("static", summary)
            self.assertIn("192.168.1.254", summary)

        def test_bridge_stp_configuration(self):
            """Test bridge STP settings."""
            bridge = BridgeConfig("br0")
            bridge.stp = True
            bridge.forward_delay = 15
            bridge.hello_time = 2
            bridge.max_age = 20

            summary = bridge.summary()
            self.assertIn("stp=on", summary)
            self.assertIn("fd=15", summary)

    class TestAddressValidation(unittest.TestCase):
        """Tests for address validation."""

        def test_valid_ipv4_addresses(self):
            """Test valid IPv4 address detection."""
            valid_ips = [
                "192.168.1.1",
                "10.0.0.1",
                "172.16.0.1",
                "8.8.8.8",
            ]
            for ip in valid_ips:
                result, msg = validate_ipv4_address(ip)
                self.assertTrue(result, f"IP {ip} should be valid: {msg}")

        def test_invalid_ipv4_addresses(self):
            """Test invalid IPv4 address detection."""
            invalid_ips = [
                "256.1.1.1",        # Octet > 255
                "192.168.1",        # Missing octet
                "192.168.1.1.1",    # Too many octets
                "192.168.a.1",      # Non-numeric
                "192.168.-1.1",     # Negative
            ]
            for ip in invalid_ips:
                result, msg = validate_ipv4_address(ip)
                self.assertFalse(result, f"IP {ip} should be invalid")

        def test_valid_cidr_blocks(self):
            """Test valid CIDR block detection."""
            valid_cidrs = [
                ("192.168.1.0", 24),
                ("10.0.0.0", 8),
                ("172.16.0.0", 12),
                ("192.168.1.128", 25),
            ]
            for ip, prefix in valid_cidrs:
                result, msg = validate_cidr(ip, prefix)
                self.assertTrue(result, f"CIDR {ip}/{prefix} should be valid: {msg}")

        def test_invalid_cidr_blocks(self):
            """Test invalid CIDR block detection."""
            invalid_cidrs = [
                ("192.168.1.0", 33),   # Prefix > 32
                ("192.168.1.0", -1),   # Negative prefix
                ("256.1.1.1", 24),     # Invalid IP
            ]
            for ip, prefix in invalid_cidrs:
                result, msg = validate_cidr(ip, prefix)
                self.assertFalse(result, f"CIDR {ip}/{prefix} should be invalid")

    class TestNetworkdGeneration(unittest.TestCase):
        """Tests for systemd-networkd file generation."""

        def setUp(self):
            """Create temporary directory for test output."""
            self.temp_dir = tempfile.mkdtemp()

        def tearDown(self):
            """Clean up temporary directory."""
            import shutil
            shutil.rmtree(self.temp_dir)

        def test_generate_simple_dhcp(self):
            """Test generating DHCP network file."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "dhcp"

            config = generate_networkd_network(iface, is_bridge_member=False)

## Verify structure

            self.assertIn("[Match]", config)
            self.assertIn("Name=eth0", config)
            self.assertIn("[Network]", config)
            self.assertIn("DHCP=ipv4", config)

        def test_generate_static_addressing(self):
            """Test generating static address network file."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "static"
            iface.address = "192.168.1.10"
            iface.prefix = 24
            iface.gateway = "192.168.1.1"
            iface.dns = ["8.8.8.8", "8.8.4.4"]

            config = generate_networkd_network(iface, is_bridge_member=False)

            self.assertIn("[Match]", config)
            self.assertIn("[Network]", config)
            self.assertIn("Address=192.168.1.10/24", config)
            self.assertIn("Gateway=192.168.1.1", config)
            self.assertIn("DNS=8.8.8.8", config)

        def test_generate_bridge_member(self):
            """Test generating network file for bridge member."""
            iface = InterfaceConfig("eth0", "wired")

            config = generate_networkd_network(iface, is_bridge_member=True, bridge_name="br0")

            self.assertIn("Bridge=br0", config)

        def test_generate_vlan_netdev(self):
            """Test generating VLAN .netdev file."""
            iface = InterfaceConfig("eth0.100", "wired")
            iface.vlan_id = 100

            config = generate_networkd_netdev_vlan(iface)

            self.assertIn("[NetDev]", config)
            self.assertIn("Name=eth0.100", config)
            self.assertIn("Kind=vlan", config)
            self.assertIn("[VLAN]", config)
            self.assertIn("Id=100", config)

    class TestNetplanGeneration(unittest.TestCase):
        """Tests for Netplan YAML generation."""

        def test_generate_netplan_dhcp(self):
            """Test generating Netplan DHCP configuration."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "dhcp"

            config = generate_netplan_yaml([iface], BridgeConfig())

            self.assertIn("eth0:", config)
            self.assertIn("dhcp4: true", config)

        def test_generate_netplan_static(self):
            """Test generating Netplan static address configuration."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "static"
            iface.address = "192.168.1.10"
            iface.prefix = 24
            iface.gateway = "192.168.1.1"

            config = generate_netplan_yaml([iface], BridgeConfig())

            self.assertIn("eth0:", config)
            self.assertIn("addresses:", config)
            self.assertIn("192.168.1.10/24", config)

    class TestErrorHandling(unittest.TestCase):
        """Tests for error handling and edge cases."""

        def test_missing_required_static_address(self):
            """Test validation when static method lacks address."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "static"
            iface.address = ""  # Missing!

            errors = validate_interface_config(iface)
            self.assertIn("address", errors[0].lower())

        def test_invalid_prefix_length(self):
            """Test validation of prefix length."""
            iface = InterfaceConfig("eth0", "wired")
            iface.method = "static"
            iface.address = "192.168.1.1"
            iface.prefix = 33  # Invalid!

            errors = validate_interface_config(iface)
            self.assertTrue(len(errors) > 0)

        def test_duplicate_interface_names(self):
            """Test detection of duplicate interface names."""
            ifaces = [
                InterfaceConfig("eth0", "wired"),
                InterfaceConfig("eth0", "wired"),  # Duplicate!
            ]

            errors = detect_duplicate_names(ifaces)
            self.assertTrue(len(errors) > 0)

        def test_conflicting_cidr_blocks(self):
            """Test detection of conflicting CIDR allocations."""
            configs = [
                InterfaceConfig("eth0", "wired"),
                InterfaceConfig("eth1", "wired"),
            ]
            configs[0].method = "static"
            configs[0].address = "192.168.1.1"
            configs[0].prefix = 24

            configs[1].method = "static"
            configs[1].address = "192.168.1.128"  # Same subnet!
            configs[1].prefix = 25

            errors = detect_cidr_conflicts(configs)
            self.assertTrue(len(errors) > 0)

    class TestInterfaceDetection(unittest.TestCase):
        """Tests for network interface detection."""

        def test_detect_interfaces_returns_list(self):
            """Test that interface detection returns a list."""
            interfaces = detect_interfaces()
            self.assertIsInstance(interfaces, list)

        def test_detected_interfaces_have_names(self):
            """Test that all detected interfaces have names."""
            interfaces = detect_interfaces()
            for iface in interfaces:
                self.assertIsNotNone(iface.name)
                self.assertTrue(len(iface.name) > 0)

        def test_no_loopback_in_detection(self):
            """Test that loopback is filtered out."""
            interfaces = detect_interfaces()
            names = [iface.name for iface in interfaces]
            self.assertNotIn("lo", names)

    class TestIntegration(unittest.TestCase):
        """Integration tests for complete workflows."""

        def setUp(self):
            """Create temporary directory for test output."""
            self.temp_dir = tempfile.mkdtemp()

        def tearDown(self):
            """Clean up temporary directory."""
            import shutil
            shutil.rmtree(self.temp_dir)

        def test_complete_workflow_networkd(self):
            """Test complete workflow: interface config -> networkd files."""

## Create configurations

            bridge = BridgeConfig("br0")
            bridge.method = "static"
            bridge.address = "192.168.1.254"
            bridge.prefix = 24

            iface1 = InterfaceConfig("eth0", "wired")
            iface2 = InterfaceConfig("eth1", "wired")

## Generate files

            files = generate_networkd_files(
                [iface1, iface2],
                bridge,
                self.temp_dir
            )

## Verify files created

            self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "10-br0.netdev")))
            self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "10-br0.network")))
            self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "10-eth0.network")))

        def test_complete_workflow_netplan(self):
            """Test complete workflow: interface config -> netplan YAML."""
            bridge = BridgeConfig("br0")
            iface = InterfaceConfig("eth0", "wired")

            yaml_content = generate_netplan_yaml([iface], bridge)

            self.assertIn("network:", yaml_content)
            self.assertIn("version: 2", yaml_content)

    if**name**== "**main**":
        unittest.main()

## Running Tests

## Run all tests

    python3 -m pytest tests/test_config_generation.py -v

## Run with coverage

    python3 -m pytest tests/test_config_generation.py --cov=netcfg_tui

## Run specific test class

    python3 -m pytest tests/test_config_generation.py::TestInterfaceConfig -v

## Enhanced Error Handling

### Edge Cases to Handle

### 1. Interface Removal During Configuration

## Problem: User unplugs interface while TUI is running

## Solution: Catch OSError when reading /sys/class/net/

    def get_interface_status(iface_name: str) -> bool:
        """Check if interface still exists."""
        try:
            with open(f"/sys/class/net/{iface_name}/carrier", "r") as f:
                return int(f.read().strip()) == 1
        except (OSError, FileNotFoundError):

## Interface disappeared

            return False

## 2. Invalid CIDR Ranges

    def validate_cidr(address: str, prefix: int) -> tuple[bool, str]:
        """Validate CIDR block."""
        if not (0 <= prefix <= 32):
            return False, f"Prefix must be 0-32, got {prefix}"

## Verify address is valid IP

        try:
            ipaddress.IPv4Address(address)
        except ValueError:
            return False, f"Invalid IPv4 address: {address}"

        return True, "OK"

### 3. DNS Server Validation

    def validate_dns_servers(servers: List[str]) -> tuple[bool, List[str]]:
        """Validate DNS server IPs."""
        errors = []
        for server in servers:
            try:
                ipaddress.IPv4Address(server)
            except ValueError:
                errors.append(f"Invalid DNS server: {server}")

        return len(errors) == 0, errors

### 4. Wi-Fi Security Key Length

    def validate_wpa_psk(psk: str) -> tuple[bool, str]:
        """Validate WPA PSK (8-63 chars)."""
        if len(psk) < 8:
            return False, "PSK must be at least 8 characters"
        if len(psk) > 63:
            return False, "PSK must be at most 63 characters"
        return True, "OK"

## Pre-Flight Validation

Add `--check` mode to validate before applying:

    python3 netcfg_tui.py --check --output-dir ./out-networkd

## Output

## Validating configuration

## ? eth0: DHCP

## ? eth1: Static 192.168.1.10/24

## ? br0: Bridge with 2 members

## ? DNS servers: 8.8.8.8, 8.8.4.4 (reachable)

## ? No CIDR conflicts detected

## ? All interface names valid

## ? Systemd-networkd available

    #

## Pre-flight checks: PASSED

## Implementation

    def run_preflight_checks(interfaces, bridge, backend):
        """Run all pre-flight checks."""
        checks = [
            ("Configuration syntax", validate_syntax),
            ("CIDR conflicts", check_cidr_conflicts),
            ("DNS servers", check_dns_servers),
            ("Required tools", check_required_tools(backend)),
            ("System readiness", check_system_ready(backend)),
        ]

        results = []
        for name, check_fn in checks:
            try:
                result = check_fn()
                results.append((name, result, None))
            except Exception as e:
                results.append((name, False, str(e)))

        return results

## Apply Flag

Add `--apply` flag for direct system application (with confirmation):

    python3 netcfg_tui.py --apply --backend networkd

## Prompts

## About to apply network configuration

## - eth0: DHCP

## - eth1: Static 192.168.1.10/24

## - br0: Bridge

    #

## Continue? (y/n) y

    #

## Applying configuration

## ? Copied 10-br0.netdev to /etc/systemd/network/

## ? Copied 10-br0.network to /etc/systemd/network/

## ? Restarted systemd-networkd

## ? Verified network connectivity

## ? COMPLETE

    #

## To rollback

## ./apply-rollback.sh

## Key Features

- Backup current config before applying
- Verify connectivity after applying
- Generate rollback script
- Timeout mechanism (revert if no confirmation after 2min)
- Detailed logging

## Advanced Use Cases

### Bonding Configuration

    Bonded Interfaces:

    bond0:

- eth0 (Active)
- eth1 (Backup)
- Mode: active-backup
- IP: 192.168.1.10/24

    Generated:

- 10-bond0.netdev (Kind=bond, BondMode=active-backup)
- 10-eth0.network (Bond=bond0)
- 10-eth1.network (Bond=bond0)
- 10-bond0.network (Address, Gateway, DNS)

### VLAN Trunking

    Trunk Interface (eth0) with Multiple VLANs:

      eth0.100 (VLAN 100): 192.168.100.10/24
      eth0.200 (VLAN 200): 192.168.200.10/24
      eth0.300 (VLAN 300): 192.168.300.10/24

    Generated:

- 10-eth0.100.netdev (Kind=vlan, Id=100)
- 10-eth0.100.network (Address, Gateway)
- 10-eth0.200.netdev (Kind=vlan, Id=200)
- 10-eth0.200.network (Address, Gateway)

### Multi-Bridge Setup

    Multiple Bridges for Tenant Isolation:

    br-mgmt (Management):

- eth0, eth1
- 192.168.1.254/24

    br-storage (Storage):

- eth2, eth3
- 192.168.2.254/24

    br-tenant (Tenant):

- eth4, eth5
- 10.0.0.254/24

    Generated: 3 bridge configurations with no cross-talk

### IPv6 Support

    Mixed IPv4/IPv6:

    eth0:

- IPv4: 192.168.1.10/24
- IPv6: 2001:db8::1/64
- Gateway (v4): 192.168.1.1
- Gateway (v6): 2001:db8::1

    Generated:

- .network file with both Address= lines
- DHCP6=true or static IPv6 as configured

## Documentation Updates

Existing README.md needs expansion for:

1.**Backend Options:**networkd (default), netplan, iproute2, nmcli
1.**Advanced Scenarios:**Bonding, VLAN trunking, multi-bridge, IPv6
1.**Error Handling:**What to do if config fails
1.**Testing:**Using fixtures to test without real hardware
1.**Troubleshooting:**Common issues and solutions
1.**Rollback Procedures:**How to recover if things break

## Testing with Fixtures

For lab/CI environments without real hardware:

## Mock network interfaces

    export MOCK_INTERFACES="eth0:wired,eth1:wired,wlan0:wireless"

    python3 netcfg_tui.py --mock-mode --output-dir ./out-test

## Generates all config files as if interfaces existed

## Useful for CI/CD validation without hardware

## Performance & Scalability

### Handle large interface counts

- Cache interface list (refresh every 5s)
- Paginate interface display (50 interfaces per page)
- Lazy-load per-interface details
- Optimize refresh rate for 100+ interfaces

## Next Steps

1.**Phase 1:**Add comprehensive unit test framework (1-2 weeks)
1.**Phase 2:**Implement error handling for edge cases (1 week)
1.**Phase 3:**Add --apply flag with safety (1-2 weeks)
1.**Phase 4:**Expand documentation (1 week)

## References

- [systemd-networkd Documentation](https://man7.org/linux/man-pages/man5/systemd.network.5.html)
- [Netplan Documentation](https://netplan.io/)
- [iproute2 Manual](https://linux.die.net/man/8/ip)
- [NetworkManager nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [pytest Documentation](https://docs.pytest.org/)
