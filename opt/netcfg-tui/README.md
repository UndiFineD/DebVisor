# DebVisor Network Config TUI

A curses-based terminal UI to configure network interfaces on Linux hosts, with support for:

- Wired, wireless, and InfiniBand interfaces
- Single-bridge default: enslaves interfaces into one bridge (e.g., `br0`)

  and configures IP on the bridge

- Spanning Tree Protocol (STP) is enabled by default on the bridge
- Adjustable STP timers (ForwardDelay, HelloTime, MaxAge)
- Optional bonding (e.g., `bond0`) with common modes (active-backup, 802.3ad, ...)
- DHCP or static addressing, gateway and DNS
- VLAN subinterfaces (e.g., `eth0.100`) via systemd-networkd`.netdev`
- Wi?Fi (SSID/PSK) via `wpa_supplicant-.conf`
- Advanced scenarios: multi-bridge, IPv6, network isolation, tenant separation

By default, it writes config files to a local output directory so you can review and apply them safely.

## Requirements

- Python 3.8+
- Linux target for practical detection and application
- systemd-networkd, netplan, or iproute2 on the target for applying configs

## Quick Start

### New Urwid-based TUI (Recommended)

Run the new, comprehensive TUI application:

    python3 opt/netcfg_tui_app.py

### Legacy Curses TUI

Run the legacy TUI (non-privileged). By default, a single bridge `br0`is created and all interfaces are enslaved to it; IP is configured on`br0`:

    python3 netcfg_tui.py --output-dir ./out-networkd

## Keys

- Up/Down or j/k: Navigate interfaces
- e: Edit selected interface settings
- s: Save config files to `--output-dir`
- r: Reload interface list
- q: Quit

To generate Netplan instead of networkd, add:

    python3 netcfg_tui.py --backend netplan --output-dir ./out-netplan

## Generated Files

- `10-br0.netdev`,`10-br0.network` (when single-bridge is enabled)
- `10-.network`(and`10-..netdev` if VLAN specified)
- `wpa_supplicant/wpa_supplicant-.conf` for Wi?Fi with SSID/PSK
- Netplan backend: `99-debvisor.yaml`
- iproute2 backend: `apply.sh`(shell script with`ip` commands)
- nmcli backend: `apply.sh`(shell script with`nmcli` commands)

## Apply on Target (systemd-networkd)

Copy the generated files to your host and apply:

    sudo cp -v out-networkd/*.network /etc/systemd/network/
    sudo cp -v out-networkd/*.netdev /etc/systemd/network/ 2>/dev/null || true
    sudo systemctl restart systemd-networkd

For Wi?Fi:

    sudo install -d -m 750 /etc/wpa_supplicant
    sudo cp -v out-networkd/wpa_supplicant/wpa_supplicant-.conf /etc/wpa_supplicant/
    sudo systemctl enable --now wpa_supplicant@.service

For Netplan:

    sudo cp -v out-netplan/99-debvisor.yaml /etc/netplan/
    sudo netplan apply

## Advanced Use Cases

### Bonding (Active-Backup, LACP)

Create bonded interfaces for high availability:

## In TUI, configure bond0 with eth0 and eth1

    python3 netcfg_tui.py --output-dir ./out-networkd

## Generated

## - 10-bond0.netdev (Kind=bond, BondMode=active-backup)

## - 10-eth0.network (Bond=bond0)

## - 10-eth1.network (Bond=bond0)

## - 10-bond0.network (IP configuration on bond)

## Apply on target

    sudo cp out-networkd/10-*.netdev /etc/systemd/network/
    sudo cp out-networkd/10-*.network /etc/systemd/network/
    sudo systemctl restart systemd-networkd

## Bond Modes Supported

- active-backup (Active/Passive failover)
- 802.3ad (LACP - requires switch support)
- balance-alb (Adaptive Load Balancing)
- balance-xor (XOR mode for link aggregation)

### VLAN Trunking

Configure multiple VLANs on a single physical interface:

## eth0 carries multiple VLANs

## eth0.100 -> Management (192.168.100.x)

## eth0.200 -> Storage (192.168.200.x)

## eth0.300 -> Tenant (10.0.0.x)

    python3 netcfg_tui.py --backend networkd --output-dir ./out-vlan

## Generated [2]

## - 10-eth0.100.netdev (VLAN ID 100)

## - 10-eth0.100.network (Management IP)

## - 10-eth0.200.netdev (VLAN ID 200)

## - 10-eth0.200.network (Storage IP)

## Use Cases

- Tenant isolation in multi-tenant clusters
- Separation of management and data traffic
- Network segmentation for security compliance

### Multi-Bridge Setup (Hypervisor)

Create multiple bridges for VM connectivity:

    Physical Interfaces: eth0, eth1, eth2, eth3, eth4, eth5

    br-mgmt (Management)
    +-- eth0 (active)
    +-- eth1 (backup, STP)
    +-- IP: 192.168.1.254/24

    br-data (Storage)
    +-- eth2 (active)
    +-- eth3 (backup, STP)
    +-- IP: 192.168.2.254/24

    br-tenant (Tenant)
    +-- eth4 (active)
    +-- eth5 (backup, STP)
    +-- IP: 10.0.0.254/24

Each bridge isolated, no cross-talk between bridges. VMs connect to appropriate bridge based on function.

### IPv6 Support

Configure both IPv4 and IPv6 addressing:

## eth0

## IPv4: 192.168.1.10/24

## IPv6: 2001:db8::10/64

## Gateway (v4): 192.168.1.1

## Gateway (v6): 2001:db8::1

## Generated .network file includes both

## Address=192.168.1.10/24

## Address=2001:db8::10/64

## Gateway=192.168.1.1

## Gateway=2001:db8::1

## Network Isolation for Multi-Tenant

Isolate customer networks using VLAN + separate bridges:

## Customer A: eth0.100 -> br-cust-a -> 10.0.0.0/24

## Customer B: eth0.200 -> br-cust-b -> 10.1.0.0/24

## Customer C: eth0.300 -> br-cust-c -> 10.2.0.0/24

## No cross-talk between customers

## Firewall rules add additional security layer

## Backend Options

### systemd-networkd (Default, Recommended for Servers)

### Pros

- Native to systemd (most modern Linux distros)
- Lightweight, minimal dependencies
- Excellent integration with Kubernetes/systemd
- Fast startup
- Good IPv6 support

### Use When

- Deploying on server OS (Debian, Ubuntu 20.04+, RHEL 8+)
- Running containerized workloads
- Need fast, reliable networking

### Netplan (Ubuntu, Some Desktops)

### Pros [2]

- Default on Ubuntu 18.04+
- Simple YAML syntax
- Supports both systemd-networkd and NetworkManager backends

### Use When [2]

- Deploying on Ubuntu systems
- Want YAML-based configuration
- Using desktop/laptop systems

### iproute2 (Universal)

### Pros [3]

- Works on any Linux distro
- Direct, immediate application
- Human-readable commands
- Easy to debug and modify

### Use When [3]

- Need universal Linux support
- Running non-systemd systems (older distros)
- Want simple, direct commands

### nmcli / NetworkManager (Desktops)

### Pros [4]

- Default on many desktop Linux distros
- GUI tools available
- Persistent storage
- Easy rollback

### Use When [4]

- Using desktop/laptop systems
- Want GUI management tools
- Running NetworkManager-based distros

## Error Handling & Validation

The tool includes comprehensive error checking:

    ? Address format validation (192.168.1.x, 2001:db8::x)
    ? CIDR block conflict detection
    ? Duplicate interface name detection
    ? DNS server reachability check
    ? WPA PSK length validation (8-63 chars)
    ? Gateway reachability validation
    ? Prefix length bounds checking
    ? VLAN ID bounds checking (1-4094)

**Example:**If you configure overlapping CIDR:

    eth0: 192.168.1.1/24 (192.168.1.0 - 192.168.1.255)
    eth1: 192.168.1.128/25 (192.168.1.128 - 192.168.1.255)

    TUI displays: ? CIDR Conflict: eth0 and eth1 overlap
                 Both define 192.168.1.128 - 192.168.1.255

## Testing & Validation

### Unit Tests

Run comprehensive tests:

## All tests

    python3 -m pytest tests/test_config_generation.py -v

## Specific test class

    python3 -m pytest tests/test_config_generation.py::TestAddressValidation -v

## With coverage report

    python3 -m pytest tests/test_config_generation.py --cov=netcfg_tui

## Pre-Flight Validation

Check configuration before applying:

    python3 netcfg_tui.py --check --backend networkd

## Output

## Validating configuration

## ? eth0: DHCP

## ? eth1: Static 192.168.1.10/24

## ? br0: Bridge with 2 members

## ? No CIDR conflicts detected

## ? All DNS servers reachable

## ? systemd-networkd available on target

    #

## Pre-flight checks: PASSED ?

## Apply with Safety

Apply configuration directly (with confirmation and rollback):

    python3 netcfg_tui.py --apply --backend networkd

## Prompts

## About to apply

## eth0: DHCP

## eth1: Static 192.168.1.10/24

## br0: Bridge

    #

## Continue? (y/n) y

    #

## Applying

## ? Backup created: /var/backups/network-2025-01-15-10-30.tar.gz

## ? Configuration applied

## ? Connectivity verified

## ? Changes permanent

    #

## To rollback

## tar -xzf /var/backups/network-2025-01-15-10-30.tar.gz -C /etc/systemd/network/

## systemctl restart systemd-networkd

## Mock Mode (Lab Testing)

Test without real hardware:

    export MOCK_INTERFACES="eth0:wired,eth1:wired,wlan0:wireless"

    python3 netcfg_tui.py --mock-mode --output-dir ./out-test

## Generates full config as if interfaces existed

## Great for CI/CD pipelines, training, demos

## Notes & Limitations

- InfiniBand support covers basic IP setup; advanced P_Key/partitioning is out of scope for now.
- Wireless interfaces in station (client) mode often cannot participate in a true L2 bridge due to 802.11 constraints and driver limitations.
- The app does not modify your system directly; it only writes files to the chosen output directory.
- On non-Linux systems, the UI runs but interface detection will be empty.

## Troubleshooting

### Wireless Connection Fails

**Problem:**Wi-Fi interface shows "No SSID" after applying config

### Solution

## Check wpa_supplicant status

    systemctl status wpa_supplicant@wlan0

## View connection attempts

    journalctl -u wpa_supplicant@wlan0 -f

## Common issues

## 1. PSK too short (<8 chars) - fix in TUI

## 2. SSID has special chars - ensure quoted properly

## 3. Interface doesn't support wireless - verify hardware

## Bridge Not Forwarding Traffic

**Problem:**Interfaces connected to bridge can't communicate

### Solution [2]

## Verify STP is working

    brctl show br0

## Check if spanning tree is blocking ports

    brctl showstp br0

## Verify bridge is up

    ip link show br0

## Should show: UP, BROADCAST, RUNNING

## Configuration Not Persistent

**Problem:**Network config reverts after reboot

### Solution [3]

- Ensure files are in correct directory: `/etc/systemd/network/`
- Check file permissions: `chmod 644 /etc/systemd/network/*.network`
- Verify systemd-networkd is enabled: `systemctl enable --now systemd-networkd`

## Roadmap

- [x] Core TUI functionality (interface selection, DHCP/static config)
- [x] Bridge configuration with STP
- [x] VLAN support
- [x] Wi-Fi configuration
- [x] systemd-networkd output
- [x] Netplan output backend
- [x] Bonding support (active-backup, LACP)
- [x] iproute2 backend
- [x] nmcli backend
- [x] Unit tests and error handling
- [x] Pre-flight validation checks
- [x] --apply flag with safe rollback
- [ ] IPv6 full support (ULA, global unicast)
- [ ] Multi-bridge scenarios
- [ ] Wireless scanning (iw integration)
- [ ] Mock mode for CI/CD
- [ ] Performance optimization (100+ interfaces)

## Related Documentation

- [Testing and Enhancement Guide](./TESTING_AND_ENHANCEMENTS.md)
- [systemd-networkd Documentation](https://man7.org/linux/man-pages/man5/systemd.network.5.html)
- [Netplan Documentation](https://netplan.io/)
- [Linux Bridge Documentation](https://linux-bridge.wiki.kernel.org/)
- [DebVisor Networking Guide](../docs/networking.md)
