# DebVisor Network Config TUI\n\nA curses-based terminal UI to configure network

interfaces on Linux

hosts, with support for:\n\n- Wired, wireless, and InfiniBand interfaces\n\n-
Single-bridge default:
enslaves interfaces into one bridge (e.g., `br0`)\n\n and configures IP on the
bridge\n\n-
Spanning
Tree Protocol (STP) is enabled by default on the bridge\n\n- Adjustable STP
timers
(ForwardDelay,
HelloTime, MaxAge)\n\n- Optional bonding (e.g., `bond0`) with common modes
(active-backup,
802.3ad,
...)\n\n- DHCP or static addressing, gateway and DNS\n\n- VLAN subinterfaces
(e.g.,
`eth0.100`) via
systemd-networkd`.netdev`\n\n- Wi?Fi (SSID/PSK) via `wpa_supplicant-.conf`\n\n-
Advanced
scenarios:
multi-bridge, IPv6, network isolation, tenant separation\n\nBy default, it
writes config
files to a
local output directory so you can review and apply them safely.\n\n##
Requirements\n\n-
Python
3.8+\n\n- Linux target for practical detection and application\n\n-
systemd-networkd,
netplan, or
iproute2 on the target for applying configs\n\n## Quick Start\n\n### New
Urwid-based TUI
(Recommended)\n\nRun the new, comprehensive TUI application:\n python3
opt/netcfg_tui_app.py\n\n###
Legacy Curses TUI\n\nRun the legacy TUI (non-privileged). By default, a single
bridge
`br0`is
created and all interfaces are enslaved to it; IP is configured on`br0`:\n
python3
netcfg_tui.py
--output-dir ./out-networkd\n\n## Keys\n\n- Up/Down or j/k: Navigate
interfaces\n\n- e:
Edit
selected interface settings\n\n- s: Save config files to `--output-dir`\n\n- r:
Reload
interface
list\n\n- q: Quit\n\nTo generate Netplan instead of networkd, add:\n python3
netcfg_tui.py
--backend
netplan --output-dir ./out-netplan\n\n## Generated Files\n\n-
`10-br0.netdev`,`10-br0.network`(when
single-bridge is enabled)\n\n-`10-.network`(and`10-..netdev`if VLAN
specified)\n\n-`wpa_supplicant/wpa_supplicant-.conf`for Wi?Fi with SSID/PSK\n\n-
Netplan
backend:`99-debvisor.yaml`\n\n- iproute2 backend: `apply.sh`(shell script
with`ip`commands)\n\n-
nmcli backend:`apply.sh`(shell script with`nmcli`commands)\n\n## Apply on Target
(systemd-networkd)\n\nCopy the generated files to your host and apply:\n sudo cp
-v
out-networkd/*.network /etc/systemd/network/\n sudo cp -v out-networkd/*.netdev
/etc/systemd/network/ 2>/dev/null || true\n sudo systemctl restart systemd-networkd\nFor
Wi?Fi:\n
sudo install -d -m 750 /etc/wpa_supplicant\n sudo cp -v
out-networkd/wpa_supplicant/wpa_supplicant-.conf /etc/wpa_supplicant/\n sudo
systemctl
enable --now
wpa_supplicant@.service\nFor Netplan:\n sudo cp -v out-netplan/99-debvisor.yaml
/etc/netplan/\n sudo
netplan apply\n\n## Advanced Use Cases\n\n### Bonding (Active-Backup,
LACP)\n\nCreate
bonded
interfaces for high availability:\n\n## In TUI, configure bond0 with eth0 and
eth1\n\n
python3
netcfg_tui.py --output-dir ./out-networkd\n\n## Generated\n\n## -
10-bond0.netdev
(Kind=bond,
BondMode=active-backup)\n\n## - 10-eth0.network (Bond=bond0)\n\n## -
10-eth1.network
(Bond=bond0)\n\n## - 10-bond0.network (IP configuration on bond)\n\n## Apply on
target\n\n
sudo cp
out-networkd/10-*.netdev /etc/systemd/network/\n sudo cp
out-networkd/10-*.network
/etc/systemd/network/\n sudo systemctl restart systemd-networkd\n\n## Bond Modes
Supported\n\n-
active-backup (Active/Passive failover)\n\n- 802.3ad (LACP - requires switch
support)\n\n-
balance-alb (Adaptive Load Balancing)\n\n- balance-xor (XOR mode for link
aggregation)\n\n### VLAN
Trunking\n\nConfigure multiple VLANs on a single physical interface:\n\n## eth0
carries
multiple
VLANs\n\n## eth0.100 -> Management (192.168.100.x)\n\n## eth0.200 -> Storage
(192.168.200.x)\n\n##
eth0.300 -> Tenant (10.0.0.x)\n\n python3 netcfg_tui.py --backend networkd
--output-dir
./out-vlan\n\n## Generated [2]\n\n## - 10-eth0.100.netdev (VLAN ID 100)\n\n## -
10-eth0.100.network
(Management IP)\n\n## - 10-eth0.200.netdev (VLAN ID 200)\n\n## -
10-eth0.200.network
(Storage
IP)\n\n## Use Cases\n\n- Tenant isolation in multi-tenant clusters\n\n-
Separation of
management and
data traffic\n\n- Network segmentation for security compliance\n\n###
Multi-Bridge Setup
(Hypervisor)\n\nCreate multiple bridges for VM connectivity:\n Physical
Interfaces: eth0,
eth1,
eth2, eth3, eth4, eth5\n br-mgmt (Management)\n +-- eth0 (active)\n +-- eth1
(backup,
STP)\n +-- IP:
192.168.1.254/24\n br-data (Storage)\n +-- eth2 (active)\n +-- eth3 (backup,
STP)\n +--
IP:
192.168.2.254/24\n br-tenant (Tenant)\n +-- eth4 (active)\n +-- eth5 (backup,
STP)\n +--
IP:
10.0.0.254/24\nEach bridge isolated, no cross-talk between bridges. VMs connect
to
appropriate
bridge based on function.\n\n### IPv6 Support\n\nConfigure both IPv4 and IPv6
addressing:\n\n##
eth0\n\n## IPv4: 192.168.1.10/24\n\n## IPv6: 2001:db8::10/64\n\n## Gateway (v4):
192.168.1.1\n\n##
Gateway (v6): 2001:db8::1\n\n## Generated .network file includes both\n\n##
Address=192.168.1.10/24\n\n## Address=2001:db8::10/64\n\n##
Gateway=192.168.1.1\n\n##
Gateway=2001:db8::1\n\n## Network Isolation for Multi-Tenant\n\nIsolate customer
networks
using VLAN

- separate bridges:\n\n## Customer A: eth0.100 -> br-cust-a -> 10.0.0.0/24\n\n##
Customer
B:
eth0.200 -> br-cust-b -> 10.1.0.0/24\n\n## Customer C: eth0.300 -> br-cust-c ->
10.2.0.0/24\n\n## No
cross-talk between customers\n\n## Firewall rules add additional security
layer\n\n##
Backend
Options\n\n### systemd-networkd (Default, Recommended for Servers)\n\n###
Pros\n\n- Native
to
systemd (most modern Linux distros)\n\n- Lightweight, minimal dependencies\n\n-
Excellent
integration with Kubernetes/systemd\n\n- Fast startup\n\n- Good IPv6
support\n\n### Use
When\n\n-
Deploying on server OS (Debian, Ubuntu 20.04+, RHEL 8+)\n\n- Running
containerized
workloads\n\n-
Need fast, reliable networking\n\n### Netplan (Ubuntu, Some Desktops)\n\n###
Pros [2]\n\n-
Default
on Ubuntu 18.04+\n\n- Simple YAML syntax\n\n- Supports both systemd-networkd and
NetworkManager
backends\n\n### Use When [2]\n\n- Deploying on Ubuntu systems\n\n- Want
YAML-based
configuration\n\n- Using desktop/laptop systems\n\n### iproute2
(Universal)\n\n### Pros
[3]\n\n-
Works on any Linux distro\n\n- Direct, immediate application\n\n- Human-readable
commands\n\n- Easy
to debug and modify\n\n### Use When [3]\n\n- Need universal Linux support\n\n-
Running
non-systemd
systems (older distros)\n\n- Want simple, direct commands\n\n### nmcli /
NetworkManager
(Desktops)\n\n### Pros [4]\n\n- Default on many desktop Linux distros\n\n- GUI
tools
available\n\n-
Persistent storage\n\n- Easy rollback\n\n### Use When [4]\n\n- Using
desktop/laptop
systems\n\n-
Want GUI management tools\n\n- Running NetworkManager-based distros\n\n## Error
Handling &
Validation\n\nThe tool includes comprehensive error checking:\n ? Address format
validation
(192.168.1.x, 2001:db8::x)\n ? CIDR block conflict detection\n ? Duplicate
interface name
detection\n ? DNS server reachability check\n ? WPA PSK length validation (8-63
chars)\n ?
Gateway
reachability validation\n ? Prefix length bounds checking\n ? VLAN ID bounds
checking
(1-4094)\n\n-
*Example:**If you configure overlapping CIDR:\n\n eth0: 192.168.1.1/24
(192.168.1.0 -
192.168.1.255)\n eth1: 192.168.1.128/25 (192.168.1.128 - 192.168.1.255)\n TUI
displays: ?
CIDR
Conflict: eth0 and eth1 overlap\n Both define 192.168.1.128 -
192.168.1.255\n\n## Testing
&
Validation\n\n### Unit Tests\n\nRun comprehensive tests:\n\n## All tests\n\n
python3 -m
pytest
tests/test_config_generation.py -v\n\n## Specific test class\n\n python3 -m
pytest
tests/test_config_generation.py::TestAddressValidation -v\n\n## With coverage
report\n\n
python3 -m
pytest tests/test_config_generation.py --cov=netcfg_tui\n\n## Pre-Flight
Validation\n\nCheck
configuration before applying:\n python3 netcfg_tui.py --check --backend
networkd\n\n##
Output\n\n##
Validating configuration\n\n## ? eth0: DHCP\n\n## ? eth1: Static
192.168.1.10/24\n\n## ?
br0: Bridge
with 2 members\n\n## ? No CIDR conflicts detected\n\n## ? All DNS servers
reachable\n\n##
?
systemd-networkd available on target\n\n #\n\n## Pre-flight checks: PASSED
?\n\n## Apply
with
Safety\n\nApply configuration directly (with confirmation and rollback):\n
python3
netcfg_tui.py
--apply --backend networkd\n\n## Prompts\n\n## About to apply\n\n## eth0:
DHCP\n\n## eth1:
Static
192.168.1.10/24\n\n## br0: Bridge\n\n #\n\n## Continue? (y/n) y\n\n #\n\n##
Applying\n\n##
? Backup
created: /var/backups/network-2025-01-15-10-30.tar.gz\n\n## ? Configuration
applied\n\n##
?
Connectivity verified\n\n## ? Changes permanent\n\n #\n\n## To rollback\n\n##
tar -xzf
/var/backups/network-2025-01-15-10-30.tar.gz -C /etc/systemd/network/\n\n##
systemctl
restart
systemd-networkd\n\n## Mock Mode (Lab Testing)\n\nTest without real hardware:\n
export
MOCK_INTERFACES="eth0:wired,eth1:wired,wlan0:wireless"\n python3 netcfg_tui.py
--mock-mode
--output-dir ./out-test\n\n## Generates full config as if interfaces
existed\n\n## Great
for CI/CD
pipelines, training, demos\n\n## Notes & Limitations\n\n- InfiniBand support
covers basic
IP setup;
advanced P_Key/partitioning is out of scope for now.\n\n- Wireless interfaces in
station
(client)
mode often cannot participate in a true L2 bridge due to 802.11 constraints and
driver
limitations.\n\n- The app does not modify your system directly; it only writes
files to
the chosen
output directory.\n\n- On non-Linux systems, the UI runs but interface detection
will be
empty.\n\n## Troubleshooting\n\n### Wireless Connection Fails\n\n-
*Problem:**Wi-Fi
interface shows
"No SSID" after applying config\n\n### Solution\n\n## Check wpa_supplicant
status\n\n
systemctl
status wpa_supplicant@wlan0\n\n## View connection attempts\n\n journalctl -u
wpa_supplicant@wlan0
-f\n\n## Common issues\n\n## 1. PSK too short (<8 chars) - fix in TUI\n\n## 2.
SSID has
special
chars - ensure quoted properly\n\n## 3. Interface doesn't support wireless -
verify
hardware\n\n##
Bridge Not Forwarding Traffic\n\n- *Problem:**Interfaces connected to bridge
can't
communicate\n\n### Solution [2]\n\n## Verify STP is working\n\n brctl show
br0\n\n## Check
if
spanning tree is blocking ports\n\n brctl showstp br0\n\n## Verify bridge is
up\n\n ip
link show
br0\n\n## Should show: UP, BROADCAST, RUNNING\n\n## Configuration Not
Persistent\n\n-
*Problem:**Network config reverts after reboot\n\n### Solution [3]\n\n- Ensure
files are
in correct
directory:`/etc/systemd/network/`\n\n- Check file permissions: `chmod 644
/etc/systemd/network/*.network`\n\n- Verify systemd-networkd is enabled:
`systemctl enable
--now
systemd-networkd`\n\n## Roadmap\n\n- [x] Core TUI functionality (interface
selection,
DHCP/static
config)\n\n- [x] Bridge configuration with STP\n\n- [x] VLAN support\n\n- [x]
Wi-Fi
configuration\n\n- [x] systemd-networkd output\n\n- [x] Netplan output
backend\n\n- [x]
Bonding
support (active-backup, LACP)\n\n- [x] iproute2 backend\n\n- [x] nmcli
backend\n\n- [x]
Unit tests
and error handling\n\n- [x] Pre-flight validation checks\n\n- [x] --apply flag
with safe
rollback\n\n- [] IPv6 full support (ULA, global unicast)\n\n- [] Multi-bridge
scenarios\n\n- []
Wireless scanning (iw integration)\n\n- [] Mock mode for CI/CD\n\n- [ ]
Performance
optimization
(100+ interfaces)\n\n## Related Documentation\n\n- [Testing and Enhancement
Guide](./TESTING_AND_ENHANCEMENTS.md)\n\n- [systemd-networkd
Documentation]([https://man7.org/linux/man-pages/man5/systemd.network.5.htm]([https://man7.org/linux/man-pages/man5/systemd.network.5.ht]([https://man7.org/linux/man-pages/man5/systemd.network.5.h]([https://man7.org/linux/man-pages/man5/systemd.network.5.]([https://man7.org/linux/man-pages/man5/systemd.network.5]([https://man7.org/linux/man-pages/man5/systemd.network.]([https://man7.org/linux/man-pages/man5/systemd.network]([https://man7.org/linux/man-pages/man5/systemd.networ]([https://man7.org/linux/man-pages/man5/systemd.netwo]([https://man7.org/linux/man-pages/man5/systemd.netw]([https://man7.org/linux/man-pages/man5/systemd.net]([https://man7.org/linux/man-pages/man5/systemd.ne]([https://man7.org/linux/man-pages/man5/systemd.n]([https://man7.org/linux/man-pages/man5/systemd.]([https://man7.org/linux/man-pages/man5/systemd]([https://man7.org/linux/man-pages/man5/system]([https://man7.org/linux/man-pages/man5/syste]([https://man7.org/linux/man-pages/man5/syst]([https://man7.org/linux/man-pages/man5/sys]([https://man7.org/linux/man-pages/man5/sy]([https://man7.org/linux/man-pages/man5/s]([https://man7.org/linux/man-pages/man5/]([https://man7.org/linux/man-pages/man5]([https://man7.org/linux/man-pages/man]([https://man7.org/linux/man-pages/ma]([https://man7.org/linux/man-pages/m]([https://man7.org/linux/man-pages/]([https://man7.org/linux/man-pages]([https://man7.org/linux/man-page]([https://man7.org/linux/man-pag]([https://man7.org/linux/man-pa]([https://man7.org/linux/man-p]([https://man7.org/linux/man-]([https://man7.org/linux/man]([https://man7.org/linux/ma]([https://man7.org/linux/m]([https://man7.org/linux/]([https://man7.org/linux]([https://man7.org/linu]([https://man7.org/lin]([https://man7.org/li]([https://man7.org/l]([https://man7.org/]([https://man7.org]([https://man7.or]([https://man7.o](https://man7.o)r)g)/)l)i)n)u)x)/)m)a)n)-)p)a)g)e)s)/)m)a)n)5)/)s)y)s)t)e)m)d).)n)e)t)w)o)r)k).)5).)h)t)m)l)\n\n-
[Netplan
Documentation]([https://netplan.io]([https://netplan.i]([https://netplan.]([https://netplan]([https://netpla]([https://netpl]([https://netp]([https://net]([https://ne]([https://n](https://n)e)t)p)l)a)n).)i)o)/)\n\n-
[Linux Bridge
Documentation]([https://linux-bridge.wiki.kernel.org]([https://linux-bridge.wiki.kernel.or]([https://linux-bridge.wiki.kernel.o]([https://linux-bridge.wiki.kernel.]([https://linux-bridge.wiki.kernel]([https://linux-bridge.wiki.kerne]([https://linux-bridge.wiki.kern]([https://linux-bridge.wiki.ker]([https://linux-bridge.wiki.ke]([https://linux-bridge.wiki.k]([https://linux-bridge.wiki.]([https://linux-bridge.wiki]([https://linux-bridge.wik]([https://linux-bridge.wi]([https://linux-bridge.w]([https://linux-bridge.]([https://linux-bridge]([https://linux-bridg]([https://linux-brid]([https://linux-bri]([https://linux-br]([https://linux-b]([https://linux-]([https://linux]([https://linu]([https://lin]([https://li]([https://l](https://l)i)n)u)x)-)b)r)i)d)g)e).)w)i)k)i).)k)e)r)n)e)l).)o)r)g)/)\n\n-
[DebVisor Networking Guide](../docs/networking.md)\n\n
