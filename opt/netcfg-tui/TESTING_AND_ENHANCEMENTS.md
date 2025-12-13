# Network Config TUI - Testing & Enhancement Guide\n\n## Overview\n\nThis guide documents

testing

procedures, enhancement opportunities, and advanced use cases for the DebVisor
Network
Configuration
Terminal User Interface (netcfg-tui).\n\n## Current State\n\n### Implemented
Features\n\n-
?
Curses-based TUI interface (Legacy)\n\n- ? **New Urwid-based
TUI**(`opt/netcfg_tui_app.py`)\n\n- ?
Interface detection (wired, wireless, InfiniBand)\n\n- ? Single-bridge default
mode\n\n- ?
DHCP/static addressing\n\n- ? VLAN configuration\n\n- ? Wi-Fi SSID/PSK
support\n\n- ? STP
configuration with timer tuning\n\n- ? systemd-networkd output\n\n- ? Netplan
output
backend\n\n- ?
Safe output-only mode (no direct system modification)\n\n- ? Unit tests for
configuration
generation\n\n- ? --apply flag with sudo support and automatic rollback\n\n- ?
Pre-flight
validation
checks\n\n- ?**Advanced Features:** Bonding, Bridges, VLANs, Rollback,
Validation\n\n###
Pending
Enhancements\n\n- None. All planned enhancements have been implemented.\n\n##
Testing
Framework\n\n### Unit Tests\n\nCreate `tests/test_config_generation.py`:\n

## !/usr/bin/env

python3\n
"""Unit tests for network configuration generation."""\n import unittest\n
import
tempfile\n import
os\n import json\n from pathlib import Path\n\n## Import from parent
directory\n\n import
sys\n
sys.path.insert(0, os.path.join(os.path.dirname(**file**), '..'))\n from
netcfg_tui import
(\n
InterfaceConfig,\n BridgeConfig,\n generate_networkd_network,\n
generate_netplan_yaml,\n
validate_cidr,\n validate_ipv4_address,\n detect_interfaces,\n )\n class
TestInterfaceConfig(unittest.TestCase):\n """Tests for InterfaceConfig
class."""\n def
test_create_wired_interface(self):\n """Test creating wired interface
configuration."""\n
iface =
InterfaceConfig("eth0", "wired")\n self.assertEqual(iface.name, "eth0")\n
self.assertEqual(iface.kind, "wired")\n self.assertEqual(iface.method, "dhcp")\n
def
test_create_wireless_interface(self):\n """Test creating wireless interface with
SSID/PSK."""\n
iface = InterfaceConfig("wlan0", "wireless")\n iface.ssid = "MyNetwork"\n
iface.psk =
"password123"\n self.assertEqual(iface.ssid, "MyNetwork")\n
self.assertEqual(iface.psk,
"password123")\n def test_vlan_interface(self):\n """Test creating VLAN
interface."""\n
iface =
InterfaceConfig("eth0", "wired")\n iface.vlan_id = 100\n
self.assertEqual(iface.vlan_id,
100)\n
self.assertIn("vlan=100", iface.summary())\n def test_static_addressing(self):\n
"""Test
static IP
configuration."""\n iface = InterfaceConfig("eth0", "wired")\n iface.method =
"static"\n
iface.address = "192.168.1.10"\n iface.prefix = 24\n iface.gateway =
"192.168.1.1"\n
iface.dns =
["8.8.8.8", "8.8.4.4"]\n summary = iface.summary()\n self.assertIn("static",
summary)\n
self.assertIn("192.168.1.10", summary)\n self.assertIn("gateway", summary)\n def
test_infiniband_interface(self):\n """Test InfiniBand interface
configuration."""\n iface
=
InterfaceConfig("ib0", "infiniband")\n iface.method = "static"\n iface.address =
"10.0.0.1"\n
iface.prefix = 16\n summary = iface.summary()\n self.assertIn("infiniband",
summary)\n
class
TestBridgeConfig(unittest.TestCase):\n """Tests for BridgeConfig class."""\n def
test_create_bridge(self):\n """Test creating bridge configuration."""\n bridge =
BridgeConfig("br0")\n self.assertEqual(bridge.name, "br0")\n
self.assertEqual(bridge.method,
"dhcp")\n self.assertTrue(bridge.stp)\n def
test_bridge_static_addressing(self):\n """Test
bridge
with static IP."""\n bridge = BridgeConfig("br0")\n bridge.method = "static"\n
bridge.address =
"192.168.1.254"\n bridge.prefix = 24\n bridge.gateway = "192.168.1.1"\n
bridge.dns =
["8.8.8.8"]\n
summary = bridge.summary()\n self.assertIn("static", summary)\n
self.assertIn("192.168.1.254",
summary)\n def test_bridge_stp_configuration(self):\n """Test bridge STP
settings."""\n
bridge =
BridgeConfig("br0")\n bridge.stp = True\n bridge.forward_delay = 15\n
bridge.hello_time =
2\n
bridge.max_age = 20\n summary = bridge.summary()\n self.assertIn("stp=on",
summary)\n
self.assertIn("fd=15", summary)\n class
TestAddressValidation(unittest.TestCase):\n
"""Tests for
address validation."""\n def test_valid_ipv4_addresses(self):\n """Test valid
IPv4 address
detection."""\n valid_ips = [\n "192.168.1.1",\n "10.0.0.1",\n "172.16.0.1",\n
"8.8.8.8",\n ]\n for
ip in valid_ips:\n result, msg = validate_ipv4_address(ip)\n
self.assertTrue(result, f"IP
{ip}
should be valid: {msg}")\n def test_invalid_ipv4_addresses(self):\n """Test
invalid IPv4
address
detection."""\n invalid_ips = [\n "256.1.1.1", # Octet > 255\n "192.168.1", #
Missing
octet\n
"192.168.1.1.1", # Too many octets\n "192.168.a.1", # Non-numeric\n
"192.168.-1.1", #
Negative\n ]\n
for ip in invalid_ips:\n result, msg = validate_ipv4_address(ip)\n
self.assertFalse(result, f"IP
{ip} should be invalid")\n def test_valid_cidr_blocks(self):\n """Test valid
CIDR block
detection."""\n valid_cidrs = [\n ("192.168.1.0", 24),\n ("10.0.0.0", 8),\n
("172.16.0.0",
12),\n
("192.168.1.128", 25),\n ]\n for ip, prefix in valid_cidrs:\n result, msg =
validate_cidr(ip,
prefix)\n self.assertTrue(result, f"CIDR {ip}/{prefix} should be valid:
{msg}")\n def
test_invalid_cidr_blocks(self):\n """Test invalid CIDR block detection."""\n
invalid_cidrs
= [\n
("192.168.1.0", 33), # Prefix > 32\n ("192.168.1.0", -1), # Negative prefix\n
("256.1.1.1", 24), #
Invalid IP\n ]\n for ip, prefix in invalid_cidrs:\n result, msg =
validate_cidr(ip,
prefix)\n
self.assertFalse(result, f"CIDR {ip}/{prefix} should be invalid")\n class
TestNetworkdGeneration(unittest.TestCase):\n """Tests for systemd-networkd file
generation."""\n def
setUp(self):\n """Create temporary directory for test output."""\n self.temp_dir
=
tempfile.mkdtemp()\n def tearDown(self):\n """Clean up temporary directory."""\n
import
shutil\n
shutil.rmtree(self.temp_dir)\n def test_generate_simple_dhcp(self):\n """Test
generating
DHCP
network file."""\n iface = InterfaceConfig("eth0", "wired")\n iface.method =
"dhcp"\n
config =
generate_networkd_network(iface, is_bridge_member=False)\n\n## Verify
structure\n\n
self.assertIn("[Match]", config)\n self.assertIn("Name=eth0", config)\n
self.assertIn("[Network]",
config)\n self.assertIn("DHCP=ipv4", config)\n def
test_generate_static_addressing(self):\n """Test
generating static address network file."""\n iface = InterfaceConfig("eth0",
"wired")\n
iface.method
= "static"\n iface.address = "192.168.1.10"\n iface.prefix = 24\n iface.gateway
=
"192.168.1.1"\n
iface.dns = ["8.8.8.8", "8.8.4.4"]\n config = generate_networkd_network(iface,
is_bridge_member=False)\n self.assertIn("[Match]", config)\n
self.assertIn("[Network]",
config)\n
self.assertIn("Address=192.168.1.10/24", config)\n
self.assertIn("Gateway=192.168.1.1",
config)\n
self.assertIn("DNS=8.8.8.8", config)\n def test_generate_bridge_member(self):\n
"""Test
generating
network file for bridge member."""\n iface = InterfaceConfig("eth0", "wired")\n
config =
generate_networkd_network(iface, is_bridge_member=True, bridge_name="br0")\n
self.assertIn("Bridge=br0", config)\n def test_generate_vlan_netdev(self):\n
"""Test
generating VLAN
.netdev file."""\n iface = InterfaceConfig("eth0.100", "wired")\n iface.vlan_id
= 100\n
config =
generate_networkd_netdev_vlan(iface)\n self.assertIn("[NetDev]", config)\n
self.assertIn("Name=eth0.100", config)\n self.assertIn("Kind=vlan", config)\n
self.assertIn("[VLAN]", config)\n self.assertIn("Id=100", config)\n class
TestNetplanGeneration(unittest.TestCase):\n """Tests for Netplan YAML
generation."""\n def
test_generate_netplan_dhcp(self):\n """Test generating Netplan DHCP
configuration."""\n
iface =
InterfaceConfig("eth0", "wired")\n iface.method = "dhcp"\n config =
generate_netplan_yaml([iface],
BridgeConfig())\n self.assertIn("eth0:", config)\n self.assertIn("dhcp4: true",
config)\n
def
test_generate_netplan_static(self):\n """Test generating Netplan static address
configuration."""\n
iface = InterfaceConfig("eth0", "wired")\n iface.method = "static"\n
iface.address =
"192.168.1.10"\n iface.prefix = 24\n iface.gateway = "192.168.1.1"\n config =
generate_netplan_yaml([iface], BridgeConfig())\n self.assertIn("eth0:",
config)\n
self.assertIn("addresses:", config)\n self.assertIn("192.168.1.10/24", config)\n
class
TestErrorHandling(unittest.TestCase):\n """Tests for error handling and edge
cases."""\n
def
test_missing_required_static_address(self):\n """Test validation when static
method lacks
address."""\n iface = InterfaceConfig("eth0", "wired")\n iface.method =
"static"\n
iface.address =
"" # Missing!\n errors = validate_interface_config(iface)\n
self.assertIn("address",
errors[0].lower())\n def test_invalid_prefix_length(self):\n """Test validation
of prefix
length."""\n iface = InterfaceConfig("eth0", "wired")\n iface.method =
"static"\n
iface.address =
"192.168.1.1"\n iface.prefix = 33 # Invalid!\n errors =
validate_interface_config(iface)\n
self.assertTrue(len(errors) > 0)\n def test_duplicate_interface_names(self):\n
"""Test
detection of
duplicate interface names."""\n ifaces = [\n InterfaceConfig("eth0", "wired"),\n
InterfaceConfig("eth0", "wired"), # Duplicate!\n ]\n errors =
detect_duplicate_names(ifaces)\n
self.assertTrue(len(errors) > 0)\n def test_conflicting_cidr_blocks(self):\n
"""Test
detection of
conflicting CIDR allocations."""\n configs = [\n InterfaceConfig("eth0",
"wired"),\n
InterfaceConfig("eth1", "wired"),\n ]\n configs[0].method = "static"\n
configs[0].address
=
"192.168.1.1"\n configs[0].prefix = 24\n configs[1].method = "static"\n
configs[1].address
=
"192.168.1.128" # Same subnet!\n configs[1].prefix = 25\n errors =
detect_cidr_conflicts(configs)\n
self.assertTrue(len(errors) > 0)\n class
TestInterfaceDetection(unittest.TestCase):\n
"""Tests for
network interface detection."""\n def
test_detect_interfaces_returns_list(self):\n """Test
that
interface detection returns a list."""\n interfaces = detect_interfaces()\n
self.assertIsInstance(interfaces, list)\n def
test_detected_interfaces_have_names(self):\n
"""Test
that all detected interfaces have names."""\n interfaces = detect_interfaces()\n
for iface
in
interfaces:\n self.assertIsNotNone(iface.name)\n self.assertTrue(len(iface.name)

> 0)\n
def
test_no_loopback_in_detection(self):\n """Test that loopback is filtered
out."""\n
interfaces =
detect_interfaces()\n names = [iface.name for iface in interfaces]\n
self.assertNotIn("lo", names)\n
class TestIntegration(unittest.TestCase):\n """Integration tests for complete
workflows."""\n def
setUp(self):\n """Create temporary directory for test output."""\n self.temp_dir
=
tempfile.mkdtemp()\n def tearDown(self):\n """Clean up temporary directory."""\n
import
shutil\n
shutil.rmtree(self.temp_dir)\n def test_complete_workflow_networkd(self):\n
"""Test
complete
workflow: interface config -> networkd files."""\n\n## Create configurations\n\n
bridge =
BridgeConfig("br0")\n bridge.method = "static"\n bridge.address =
"192.168.1.254"\n
bridge.prefix =
24\n iface1 = InterfaceConfig("eth0", "wired")\n iface2 =
InterfaceConfig("eth1",
"wired")\n\n##
Generate files\n\n files = generate_networkd_files(\n [iface1, iface2],\n
bridge,\n
self.temp_dir\n
)\n\n## Verify files created\n\n
self.assertTrue(os.path.exists(os.path.join(self.temp_dir,
"10-br0.netdev")))\n self.assertTrue(os.path.exists(os.path.join(self.temp_dir,
"10-br0.network")))\n self.assertTrue(os.path.exists(os.path.join(self.temp_dir,
"10-eth0.network")))\n def test_complete_workflow_netplan(self):\n """Test
complete
workflow:
interface config -> netplan YAML."""\n bridge = BridgeConfig("br0")\n iface =
InterfaceConfig("eth0", "wired")\n yaml_content = generate_netplan_yaml([iface],
bridge)\n
self.assertIn("network:", yaml_content)\n self.assertIn("version: 2",
yaml_content)\n
if**name**==
"**main**":\n unittest.main()\n\n## Running Tests\n\n## Run all tests\n\n
python3 -m
pytest
tests/test_config_generation.py -v\n\n## Run with coverage\n\n python3 -m pytest
tests/test_config_generation.py --cov=netcfg_tui\n\n## Run specific test
class\n\n python3
-m pytest
tests/test_config_generation.py::TestInterfaceConfig -v\n\n## Enhanced Error
Handling\n\n### Edge
Cases to Handle\n\n### 1. Interface Removal During Configuration\n\n## Problem:
User
unplugs
interface while TUI is running\n\n## Solution: Catch OSError when reading
/sys/class/net/\n\n def
get_interface_status(iface_name: str) -> bool:\n """Check if interface still
exists."""\n
try:\n
with open(f"/sys/class/net/{iface_name}/carrier", "r") as f:\n return
int(f.read().strip()) == 1\n
except (OSError, FileNotFoundError):\n\n## Interface disappeared\n\n return
False\n\n## 2.
Invalid
CIDR Ranges\n\n def validate_cidr(address: str, prefix: int) -> tuple[bool,
str]:\n
"""Validate CIDR
block."""\n if not (0  tuple[bool, List[str]]:\n """Validate DNS
server
IPs."""\n errors = []\n for server in servers:\n try:\n
ipaddress.IPv4Address(server)\n
except
ValueError:\n errors.append(f"Invalid DNS server: {server}")\n return
len(errors) == 0,
errors\n\n### 4. Wi-Fi Security Key Length\n\n def validate_wpa_psk(psk: str) ->
tuple[bool, str]:\n
"""Validate WPA PSK (8-63 chars)."""\n if len(psk) 63:\n return False, "PSK must
be at most 63 characters"\n
return True,
"OK"\n\n## Pre-Flight Validation\n\nAdd `--check`mode to validate before
applying:\n
python3
netcfg_tui.py --check --output-dir ./out-networkd\n\n## Output\n\n## Validating
configuration\n\n##
? eth0: DHCP\n\n## ? eth1: Static 192.168.1.10/24\n\n## ? br0: Bridge with 2
members\n\n##
? DNS
servers: 8.8.8.8, 8.8.4.4 (reachable)\n\n## ? No CIDR conflicts detected\n\n## ?
All
interface names
valid\n\n## ? Systemd-networkd available\n\n #\n\n## Pre-flight checks:
PASSED\n\n##
Implementation\n\n def run_preflight_checks(interfaces, bridge, backend):\n
"""Run all
pre-flight
checks."""\n checks = [\n ("Configuration syntax", validate_syntax),\n ("CIDR
conflicts",
check_cidr_conflicts),\n ("DNS servers", check_dns_servers),\n ("Required
tools",
check_required_tools(backend)),\n ("System readiness",
check_system_ready(backend)),\n ]\n
results =
[]\n for name, check_fn in checks:\n try:\n result = check_fn()\n
results.append((name,
result,
None))\n except Exception as e:\n results.append((name, False, str(e)))\n return
results\n\n## Apply
Flag\n\nAdd`--apply` flag for direct system application (with confirmation):\n
python3
netcfg_tui.py
--apply --backend networkd\n\n## Prompts\n\n## About to apply network
configuration\n\n##

- eth0:
DHCP\n\n## - eth1: Static 192.168.1.10/24\n\n## - br0: Bridge\n\n #\n\n##
Continue? (y/n)
y\n\n

## \n\n## Applying configuration\n\n## ? Copied 10-br0.netdev to

/etc/systemd/network/\n\n## ? Copied

10-br0.network to /etc/systemd/network/\n\n## ? Restarted systemd-networkd\n\n##
?
Verified network
connectivity\n\n## ? COMPLETE\n\n #\n\n## To rollback\n\n##
./apply-rollback.sh\n\n## Key
Features\n\n- Backup current config before applying\n\n- Verify connectivity
after
applying\n\n-
Generate rollback script\n\n- Timeout mechanism (revert if no confirmation after
2min)\n\n- Detailed
logging\n\n## Advanced Use Cases\n\n### Bonding Configuration\n\n Bonded
Interfaces:\n
bond0:\n\n-
eth0 (Active)\n\n- eth1 (Backup)\n\n- Mode: active-backup\n\n- IP:
192.168.1.10/24\n\n
Generated:\n\n- 10-bond0.netdev (Kind=bond, BondMode=active-backup)\n\n-
10-eth0.network
(Bond=bond0)\n\n- 10-eth1.network (Bond=bond0)\n\n- 10-bond0.network (Address,
Gateway,
DNS)\n\n###
VLAN Trunking\n\n Trunk Interface (eth0) with Multiple VLANs:\n eth0.100 (VLAN
100):
192.168.100.10/24\n eth0.200 (VLAN 200): 192.168.200.10/24\n eth0.300 (VLAN
300):
192.168.300.10/24\n Generated:\n\n- 10-eth0.100.netdev (Kind=vlan, Id=100)\n\n-
10-eth0.100.network
(Address, Gateway)\n\n- 10-eth0.200.netdev (Kind=vlan, Id=200)\n\n-
10-eth0.200.network
(Address,
Gateway)\n\n### Multi-Bridge Setup\n\n Multiple Bridges for Tenant Isolation:\n
br-mgmt
(Management):\n\n- eth0, eth1\n\n- 192.168.1.254/24\n\n br-storage
(Storage):\n\n- eth2,
eth3\n\n-
192.168.2.254/24\n\n br-tenant (Tenant):\n\n- eth4, eth5\n\n- 10.0.0.254/24\n\n
Generated:
3 bridge
configurations with no cross-talk\n\n### IPv6 Support\n\n Mixed IPv4/IPv6:\n
eth0:\n\n-
IPv4:
192.168.1.10/24\n\n- IPv6: 2001:db8::1/64\n\n- Gateway (v4): 192.168.1.1\n\n-
Gateway
(v6):
2001:db8::1\n\n Generated:\n\n- .network file with both Address= lines\n\n-
DHCP6=true or
static
IPv6 as configured\n\n## Documentation Updates\n\nExisting README.md needs
expansion
for:\n1.**Backend Options:**networkd (default), netplan, iproute2,
nmcli\n1.**Advanced
Scenarios:**Bonding, VLAN trunking, multi-bridge, IPv6\n1.**Error
Handling:**What to do if
config
fails\n1.**Testing:**Using fixtures to test without real
hardware\n1.**Troubleshooting:**Common
issues and solutions\n1.**Rollback Procedures:**How to recover if things
break\n\n##
Testing with
Fixtures\n\nFor lab/CI environments without real hardware:\n\n## Mock network
interfaces\n\n export
MOCK_INTERFACES="eth0:wired,eth1:wired,wlan0:wireless"\n python3 netcfg_tui.py
--mock-mode
--output-dir ./out-test\n\n## Generates all config files as if interfaces
existed\n\n##
Useful for
CI/CD validation without hardware\n\n## Performance & Scalability\n\n### Handle
large
interface
counts\n\n- Cache interface list (refresh every 5s)\n\n- Paginate interface
display (50
interfaces
per page)\n\n- Lazy-load per-interface details\n\n- Optimize refresh rate for
100+
interfaces\n\n##
Next Steps\n\n1.**Phase 1:**Add comprehensive unit test framework (1-2
weeks)\n1.**Phase
2:**Implement error handling for edge cases (1 week)\n1.**Phase 3:**Add --apply
flag with
safety
(1-2 weeks)\n1.**Phase 4:**Expand documentation (1 week)\n\n## References\n\n-
[systemd-networkd
Documentation]([https://man7.org/linux/man-pages/man5/systemd.network.5.htm]([https://man7.org/linux/man-pages/man5/systemd.network.5.ht]([https://man7.org/linux/man-pages/man5/systemd.network.5.h]([https://man7.org/linux/man-pages/man5/systemd.network.5.]([https://man7.org/linux/man-pages/man5/systemd.network.5]([https://man7.org/linux/man-pages/man5/systemd.network.]([https://man7.org/linux/man-pages/man5/systemd.network]([https://man7.org/linux/man-pages/man5/systemd.networ]([https://man7.org/linux/man-pages/man5/systemd.netwo]([https://man7.org/linux/man-pages/man5/systemd.netw]([https://man7.org/linux/man-pages/man5/systemd.net]([https://man7.org/linux/man-pages/man5/systemd.ne]([https://man7.org/linux/man-pages/man5/systemd.n]([https://man7.org/linux/man-pages/man5/systemd.]([https://man7.org/linux/man-pages/man5/systemd]([https://man7.org/linux/man-pages/man5/system]([https://man7.org/linux/man-pages/man5/syste]([https://man7.org/linux/man-pages/man5/syst]([https://man7.org/linux/man-pages/man5/sys]([https://man7.org/linux/man-pages/man5/sy]([https://man7.org/linux/man-pages/man5/s]([https://man7.org/linux/man-pages/man5/]([https://man7.org/linux/man-pages/man5]([https://man7.org/linux/man-pages/man]([https://man7.org/linux/man-pages/ma]([https://man7.org/linux/man-pages/m]([https://man7.org/linux/man-pages/]([https://man7.org/linux/man-pages]([https://man7.org/linux/man-page]([https://man7.org/linux/man-pag]([https://man7.org/linux/man-pa]([https://man7.org/linux/man-p]([https://man7.org/linux/man-]([https://man7.org/linux/man]([https://man7.org/linux/ma]([https://man7.org/linux/m]([https://man7.org/linux/]([https://man7.org/linux]([https://man7.org/linu]([https://man7.org/lin]([https://man7.org/li]([https://man7.org/l](https://man7.org/l)i)n)u)x)/)m)a)n)-)p)a)g)e)s)/)m)a)n)5)/)s)y)s)t)e)m)d).)n)e)t)w)o)r)k).)5).)h)t)m)l)\n\n-
[Netplan
Documentation]([https://netplan.io]([https://netplan.i]([https://netplan.]([https://netplan]([https://netpla]([https://netpl]([https://netp]([https://net]([https://ne]([https://n](https://n)e)t)p)l)a)n).)i)o)/)\n\n-
[iproute2
Manual]([https://linux.die.net/man/8/i]([https://linux.die.net/man/8/]([https://linux.die.net/man/8]([https://linux.die.net/man/]([https://linux.die.net/man]([https://linux.die.net/ma]([https://linux.die.net/m]([https://linux.die.net/]([https://linux.die.net]([https://linux.die.ne]([https://linux.die.n]([https://linux.die.]([https://linux.die]([https://linux.di]([https://linux.d]([https://linux.]([https://linux]([https://linu]([https://lin]([https://li]([https://l](https://l)i)n)u)x).)d)i)e).)n)e)t)/)m)a)n)/)8)/)i)p)\n\n-
[NetworkManager
nmcli]([https://networkmanager.dev/docs/api/latest/nmcli.htm]([https://networkmanager.dev/docs/api/latest/nmcli.ht]([https://networkmanager.dev/docs/api/latest/nmcli.h]([https://networkmanager.dev/docs/api/latest/nmcli.]([https://networkmanager.dev/docs/api/latest/nmcli]([https://networkmanager.dev/docs/api/latest/nmcl]([https://networkmanager.dev/docs/api/latest/nmc]([https://networkmanager.dev/docs/api/latest/nm]([https://networkmanager.dev/docs/api/latest/n]([https://networkmanager.dev/docs/api/latest/]([https://networkmanager.dev/docs/api/latest]([https://networkmanager.dev/docs/api/lates]([https://networkmanager.dev/docs/api/late]([https://networkmanager.dev/docs/api/lat]([https://networkmanager.dev/docs/api/la]([https://networkmanager.dev/docs/api/l]([https://networkmanager.dev/docs/api/]([https://networkmanager.dev/docs/api]([https://networkmanager.dev/docs/ap]([https://networkmanager.dev/docs/a]([https://networkmanager.dev/docs/]([https://networkmanager.dev/docs]([https://networkmanager.dev/doc]([https://networkmanager.dev/do]([https://networkmanager.dev/d]([https://networkmanager.dev/]([https://networkmanager.dev]([https://networkmanager.de]([https://networkmanager.d]([https://networkmanager.]([https://networkmanager]([https://networkmanage]([https://networkmanag]([https://networkmana]([https://networkman]([https://networkma]([https://networkm]([https://network]([https://networ]([https://netwo]([https://netw]([https://net](https://net)w)o)r)k)m)a)n)a)g)e)r).)d)e)v)/)d)o)c)s)/)a)p)i)/)l)a)t)e)s)t)/)n)m)c)l)i).)h)t)m)l)\n\n-
[Python unittest
Documentation]([https://docs.python.org/3/library/unittest.htm]([https://docs.python.org/3/library/unittest.ht]([https://docs.python.org/3/library/unittest.h]([https://docs.python.org/3/library/unittest.]([https://docs.python.org/3/library/unittest]([https://docs.python.org/3/library/unittes]([https://docs.python.org/3/library/unitte]([https://docs.python.org/3/library/unitt]([https://docs.python.org/3/library/unit]([https://docs.python.org/3/library/uni]([https://docs.python.org/3/library/un]([https://docs.python.org/3/library/u]([https://docs.python.org/3/library/]([https://docs.python.org/3/library]([https://docs.python.org/3/librar]([https://docs.python.org/3/libra]([https://docs.python.org/3/libr]([https://docs.python.org/3/lib]([https://docs.python.org/3/li]([https://docs.python.org/3/l]([https://docs.python.org/3/]([https://docs.python.org/3]([https://docs.python.org/]([https://docs.python.org]([https://docs.python.or]([https://docs.python.o]([https://docs.python.]([https://docs.python]([https://docs.pytho]([https://docs.pyth]([https://docs.pyt]([https://docs.py]([https://docs.p]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)p)y)t)h)o)n).)o)r)g)/)3)/)l)i)b)r)a)r)y)/)u)n)i)t)t)e)s)t).)h)t)m)l)\n\n-
[pytest
Documentation]([https://docs.pytest.org]([https://docs.pytest.or]([https://docs.pytest.o]([https://docs.pytest.]([https://docs.pytest]([https://docs.pytes]([https://docs.pyte]([https://docs.pyt]([https://docs.py]([https://docs.p]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)p)y)t)e)s)t).)o)r)g)/)\n\n
