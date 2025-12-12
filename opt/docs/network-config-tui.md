# Network Configuration TUI

A curses-based terminal UI for configuring network interfaces on Linux hosts. It supports a single-bridge-by-default design (e.g., `br0`) with STP enabled, optional bonding, VLAN subinterfaces, and either systemd-networkd or Netplan backends.

## Features

- Single bridge: enslaves interfaces into one bridge (default `br0`) and configures IP on the bridge

- STP enabled by default; adjustable timers (ForwardDelay, HelloTime, MaxAge)

- Bonding: `bond0` with common modes (active-backup, 802.3ad, balance-xor, broadcast, balance-tlb, balance-alb)

- Interfaces: wired, wireless (SSID/PSK), InfiniBand (basic IP)

- VLANs: per-interface VLAN subinterfaces (e.g., `eth0.100`)

- Backends: generate systemd-networkd files or a single Netplan YAML

- Apply script: `apply.sh` generated for safe, repeatable rollout

## Requirements

- Python 3.8+

- Linux target for detection and application

- Backend prerequisites:

- systemd-networkd (if using `--backend networkd`)

- netplan.io (if using `--backend netplan`)

## Quick Start

- Networkd backend (default):

    python3 tools/netcfg-tui/netcfg_tui.py --output-dir ./out-networkd

- Netplan backend:

    python3 tools/netcfg-tui/netcfg_tui.py --backend netplan --output-dir ./out-netplan

## TUI Controls

- Up/Down or j/k: navigate

- e: edit selected entry (bridge, bond, or interface)

- s: save files to the output directory and generate `apply.sh`

- r: reload interface list

- q: quit

## Generated Files

- Networkd backend:

- `10-br0.netdev`and`10-br0.network` (when single-bridge is enabled)

- `10-.network`for each member (with`Bridge=br0`or`Bond=bond0`), and`10-..netdev` if VLAN set

- `wpa_supplicant/wpa_supplicant-.conf` when Wi?Fi SSID/PSK provided

- Netplan backend:

- `99-debvisor.yaml`

- Apply helper:

- `apply.sh` to copy files into place and restart services (review before running with sudo)

## Apply on Target

- Networkd:

    ./out-networkd/apply.sh

- Netplan:

    ./out-netplan/apply.sh

## Notes & Limitations

- Wi?Fi in client (station) mode generally cannot participate in a true L2 bridge due to 802.11/driver constraints; use routed/NAT or AP mode when needed

- InfiniBand support covers basic IP; advanced partitioning (P_Key) is not included

- Bond members can be auto-selected (all wired) or specified by name

- The tool writes to an output directory and does not modify the system until you apply

## Location

- TUI script: `tools/netcfg-tui/netcfg_tui.py`

- Documentation: this file (`docs/network-config-tui.md`)
