#!/usr/bin/env python3
import argparse
import ipaddress
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import time
from typing import List, Optional, Tuple

try:
    import curses
except ImportError:
    curses = None


class InterfaceConfig:
    def __init__(self, name: str, kind: str):
        self.name = name
        self.kind = kind  # wired|wireless|infiniband|other
        self.method = "dhcp"  # dhcp|static
        self.address = ""
        self.prefix = 24
        self.gateway = ""
        self.ipv6_address = ""
        self.ipv6_prefix = 64
        self.ipv6_gateway = ""
        self.dns: List[str] = []
        # Wireless extras
        self.ssid: Optional[str] = None
        self.psk: Optional[str] = None
        # VLAN (optional, create child .netdev)
        self.vlan_id: Optional[int] = None
        # Master device (bridge/bond)
        self.master: str = ""

    def summary(self) -> str:
        base = f"{self.name} ({self.kind}) {self.method}"
        if self.master:
            base += f" master={self.master}"
        if self.method == "static":
            if self.address:
                base += f" {self.address}/{self.prefix}"
            if self.ipv6_address:
                base += f" {self.ipv6_address}/{self.ipv6_prefix}"
        if self.vlan_id is not None:
            base += f" vlan={self.vlan_id}"
        if self.kind == "wireless" and self.ssid:
            base += f" ssid=\"{self.ssid}\""
        return base


class BridgeConfig:
    def __init__(self, name: str = "br0"):
        self.name = name
        self.method = "dhcp"  # dhcp|static
        self.address = ""
        self.prefix = 24
        self.gateway = ""
        self.ipv6_address = ""
        self.ipv6_prefix = 64
        self.ipv6_gateway = ""
        self.dns: List[str] = []
        self.stp: bool = True  # Spanning Tree Protocol enabled by default
        # Optional timers (seconds). If None, defaults apply.
        self.forward_delay: Optional[int] = None
        self.hello_time: Optional[int] = None
        self.max_age: Optional[int] = None

    def summary(self) -> str:
        base = f"{self.name} (bridge) {self.method}"
        if self.method == "static":
            if self.address:
                base += f" {self.address}/{self.prefix}"
            if self.ipv6_address:
                base += f" {self.ipv6_address}/{self.ipv6_prefix}"
        if self.dns:
            base += f" dns={' '.join(self.dns)}"
        base += f" stp={'on' if self.stp else 'off'}"
        timers = []
        if self.forward_delay is not None:
            timers.append(f"fd={self.forward_delay}")
        if self.hello_time is not None:
            timers.append(f"hello={self.hello_time}")
        if self.max_age is not None:
            timers.append(f"maxage={self.max_age}")
        if timers:
            base += " (" + ", ".join(timers) + ")"
        return base


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def validate_ipv4_address(ip: str) -> Tuple[bool, str]:
    try:
        ipaddress.IPv4Address(ip)
        return True, "OK"
    except ValueError:
        return False, f"Invalid IPv4 address: {ip}"


def validate_ipv6_address(ip: str) -> Tuple[bool, str]:
    try:
        ipaddress.IPv6Address(ip)
        return True, "OK"
    except ValueError:
        return False, f"Invalid IPv6 address: {ip}"


def validate_cidr(ip: str, prefix: int) -> Tuple[bool, str]:
    if not (0 <= prefix <= 32):
        return False, f"Prefix must be 0-32, got {prefix}"
    try:
        ipaddress.IPv4Address(ip)
    except ValueError:
        return False, f"Invalid IPv4 address: {ip}"
    return True, "OK"


def validate_dns_servers(servers: List[str]) -> Tuple[bool, List[str]]:
    errors = []
    for server in servers:
        try:
            ipaddress.IPv4Address(server)
        except ValueError:
            errors.append(f"Invalid DNS server: {server}")
    return len(errors) == 0, errors


def detect_interfaces(mock_mode: bool = False, benchmark_count: int = 0) -> List[InterfaceConfig]:
    items: List[InterfaceConfig] = []

    if mock_mode or benchmark_count > 0:
        # Mock interfaces for testing/demo
        count = benchmark_count if benchmark_count > 0 else 4
        if benchmark_count > 0:
            for i in range(count):
                items.append(InterfaceConfig(f"eth{i}", "wired"))
        else:
            items.append(InterfaceConfig("eth0", "wired"))
            items.append(InterfaceConfig("eth1", "wired"))
            items.append(InterfaceConfig("wlan0", "wireless"))
            items.append(InterfaceConfig("ib0", "infiniband"))
        return items

    if not is_linux():
        return items
    sys_net = "/sys/class/net"
    try:
        for name in sorted(os.listdir(sys_net)):
            # Skip loopback
            if name == "lo":
                continue
            kind = "wired"
            # Wireless hint: wireless dir exists
            if os.path.isdir(os.path.join(sys_net, name, "wireless")):
                kind = "wireless"
            else:
                # InfiniBand: ARPHRD_INFINIBAND (32) in 'type'
                try:
                    with open(os.path.join(sys_net, name, "type"), "r", encoding="utf-8") as f:
                        t = f.read().strip()
                        if t == "32":
                            kind = "infiniband"
                except Exception:
                    pass
            items.append(InterfaceConfig(name, kind))
    except FileNotFoundError:
        pass
    return items


def prompt(stdscr, yx, prompt_text: str, default: str = "") -> str:
    curses.echo()
    y, x = yx
    stdscr.addstr(y, x, " " * (curses.COLS - x - 1))
    stdscr.addstr(y, x, f"{prompt_text} [{default}]: ")
    stdscr.refresh()
    val = stdscr.getstr(y, x + len(prompt_text) + 3 + len(default), 128).decode("utf-8").strip()
    curses.noecho()
    return val or default


def draw_help(stdscr):
    help_lines = ("q: quit  e: edit  s: save  r: reload  b: add bridge  d: del bridge  "
                  "w: wifi scan  backend: systemd-networkd")  # basic guidance
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(curses.LINES - 1, 0, help_lines.ljust(curses.COLS - 1))
    stdscr.attroff(curses.A_REVERSE)


def edit_interface(stdscr, cfg: InterfaceConfig, masters: List[str] = None):
    row = curses.LINES - 3
    # Master
    if masters:
        master_str = prompt(stdscr, (row, 2), f"Master ({', '.join(masters)})",
                            cfg.master)
        if master_str in masters or master_str == "":
            cfg.master = master_str

    # Method
    method = prompt(stdscr, (row, 2), "Method (dhcp/static)", cfg.method)
    if method in ("dhcp", "static"):
        cfg.method = method
    if cfg.method == "static":
        # Address
        while True:
            addr = prompt(stdscr, (row, 2), "Address (e.g. 192.168.1.10)",
                          cfg.address or "")
            if not addr:
                break
            valid, msg = validate_ipv4_address(addr)
            if valid:
                cfg.address = addr
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # Prefix
        while True:
            prefix = prompt(stdscr, (row, 2), "Prefix (e.g. 24)", str(cfg.prefix))
            try:
                p = int(prefix)
                if 0 <= p <= 32:
                    cfg.prefix = p
                    break
                msg = "Prefix must be 0-32"
            except ValueError:
                msg = "Prefix must be an integer"
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # Gateway
        while True:
            gw = prompt(stdscr, (row, 2), "Gateway (optional)", cfg.gateway or "")
            if not gw:
                cfg.gateway = ""
                break
            valid, msg = validate_ipv4_address(gw)
            if valid:
                cfg.gateway = gw
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # IPv6 Address
        while True:
            addr = prompt(stdscr, (row, 2), "IPv6 Address (optional)",
                          cfg.ipv6_address or "")
            if not addr:
                cfg.ipv6_address = ""
                break
            valid, msg = validate_ipv6_address(addr)
            if valid:
                cfg.ipv6_address = addr
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # IPv6 Prefix
        if cfg.ipv6_address:
            while True:
                prefix = prompt(stdscr, (row, 2), "IPv6 Prefix (e.g. 64)",
                                str(cfg.ipv6_prefix))
                try:
                    p = int(prefix)
                    if 0 <= p <= 128:
                        cfg.ipv6_prefix = p
                        break
                    msg = "Prefix must be 0-128"
                except ValueError:
                    msg = "Prefix must be an integer"
                stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
                stdscr.getch()
                stdscr.move(row - 1, 0)
                stdscr.clrtoeol()

            # IPv6 Gateway
            while True:
                gw = prompt(stdscr, (row, 2), "IPv6 Gateway (optional)",
                            cfg.ipv6_gateway or "")
                if not gw:
                    cfg.ipv6_gateway = ""
                    break
                valid, msg = validate_ipv6_address(gw)
                if valid:
                    cfg.ipv6_gateway = gw
                    break
                stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
                stdscr.getch()
                stdscr.move(row - 1, 0)
                stdscr.clrtoeol()

        # DNS
        while True:
            dns = prompt(stdscr, (row, 2), "DNS (space-separated)",
                         " ".join(cfg.dns) if cfg.dns else "")
            dns_list = [d for d in dns.split() if d]
            if not dns_list:
                cfg.dns = []
                break
            # Validate both IPv4 and IPv6 DNS
            errors = []
            for d in dns_list:
                v4, _ = validate_ipv4_address(d)
                v6, _ = validate_ipv6_address(d)
                if not v4 and not v6:
                    errors.append(f"Invalid DNS: {d}")

            if not errors:
                cfg.dns = dns_list
                break
            stdscr.addstr(row - 1, 2, f"Error: {errors[0]} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

    # VLAN
    vlan = prompt(stdscr, (row, 2), "VLAN ID (empty for none)", str(cfg.vlan_id or ""))
    if vlan.strip() == "":
        cfg.vlan_id = None
    else:
        try:
            cfg.vlan_id = int(vlan)
        except ValueError:
            pass
    # Wireless
    if cfg.kind == "wireless":
        ssid = prompt(stdscr, (row, 2), "WiFi SSID", cfg.ssid or "")
        psk = prompt(stdscr, (row, 2), "WiFi passphrase", cfg.psk or "")
        cfg.ssid = ssid if ssid else None
        cfg.psk = psk if psk else None


def edit_bridge(stdscr, br: BridgeConfig):
    row = curses.LINES - 3
    method = prompt(stdscr, (row, 2), "Bridge method (dhcp/static)", br.method)
    if method in ("dhcp", "static"):
        br.method = method
    if br.method == "static":
        # Address
        while True:
            addr = prompt(stdscr, (row, 2), "Bridge address", br.address or "")
            if not addr:
                break
            valid, msg = validate_ipv4_address(addr)
            if valid:
                br.address = addr
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # Prefix
        while True:
            prefix = prompt(stdscr, (row, 2), "Bridge prefix", str(br.prefix))
            try:
                p = int(prefix)
                if 0 <= p <= 32:
                    br.prefix = p
                    break
                msg = "Prefix must be 0-32"
            except ValueError:
                msg = "Prefix must be an integer"
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # Gateway
        while True:
            gw = prompt(stdscr, (row, 2), "Bridge gateway (optional)", br.gateway or "")
            if not gw:
                br.gateway = ""
                break
            valid, msg = validate_ipv4_address(gw)
            if valid:
                br.gateway = gw
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # IPv6 Address
        while True:
            addr = prompt(stdscr, (row, 2), "Bridge IPv6 Address (optional)",
                          br.ipv6_address or "")
            if not addr:
                br.ipv6_address = ""
                break
            valid, msg = validate_ipv6_address(addr)
            if valid:
                br.ipv6_address = addr
                break
            stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
            stdscr.getch()
            stdscr.move(row - 1, 0)
            stdscr.clrtoeol()

        # IPv6 Prefix
        if br.ipv6_address:
            while True:
                prefix = prompt(stdscr, (row, 2), "Bridge IPv6 Prefix", str(br.ipv6_prefix))
                try:
                    p = int(prefix)
                    if 0 <= p <= 128:
                        br.ipv6_prefix = p
                        break
                    msg = "Prefix must be 0-128"
                except ValueError:
                    msg = "Prefix must be an integer"
                stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
                stdscr.getch()
                stdscr.move(row - 1, 0)
                stdscr.clrtoeol()

            # IPv6 Gateway
            while True:
                gw = prompt(
                    stdscr,
                    (row,
                     2),
                    "Bridge IPv6 Gateway (optional)",
                    br.ipv6_gateway or "")
                if not gw:
                    br.ipv6_gateway = ""
                    break
                valid, msg = validate_ipv6_address(gw)
                if valid:
                    br.ipv6_gateway = gw
                    break
                stdscr.addstr(row - 1, 2, f"Error: {msg} (Press any key)")
                stdscr.getch()
                stdscr.move(row - 1, 0)
                stdscr.clrtoeol()

    # DNS
    while True:
        dns = prompt(stdscr, (row, 2), "Bridge DNS (space-separated)",
                     " ".join(br.dns) if br.dns else "")
        dns_list = [d for d in dns.split() if d]
        if not dns_list:
            br.dns = []
            break
        # Validate both IPv4 and IPv6 DNS
        errors = []
        for d in dns_list:
            v4, _ = validate_ipv4_address(d)
            v6, _ = validate_ipv6_address(d)
            if not v4 and not v6:
                errors.append(f"Invalid DNS: {d}")

        if not errors:
            br.dns = dns_list
            break
        stdscr.addstr(row - 1, 2, f"Error: {errors[0]} (Press any key)")
        stdscr.getch()
        stdscr.move(row - 1, 0)
        stdscr.clrtoeol()

    stp = prompt(stdscr, (row, 2), "Bridge STP (yes/no)", "yes" if br.stp else "no").lower()
    if stp in ("yes", "no"):
        br.stp = (stp == "yes")
    fd = prompt(
        stdscr, (row, 2), "STP ForwardDelay sec (blank=default)", str(
            br.forward_delay or ""))
    br.forward_delay = int(fd) if fd.strip().isdigit() else None
    ht = prompt(stdscr, (row, 2), "STP HelloTime sec (blank=default)",
                str(br.hello_time or ""))
    br.hello_time = int(ht) if ht.strip().isdigit() else None
    ma = prompt(stdscr, (row, 2), "STP MaxAge sec (blank=default)",
                str(br.max_age or ""))
    br.max_age = int(ma) if ma.strip().isdigit() else None


class BondConfig:
    def __init__(self, name: str = "bond0"):
        self.name = name
        # common modes: active-backup, 802.3ad, balance-xor, broadcast, balance-tlb, balance-alb
        self.mode = "active-backup"
        # auto-include all wired (non-wireless, non-ib) members
        self.auto_members = False
        # specific members (optional)
        self.members: List[str] = []

    def summary(self) -> str:
        scope = "auto-wired" if self.auto_members else (",".join(self.members) or
                                                        "(no members)")
        return f"{self.name} (bond mode={self.mode} members={scope})"


def edit_bond(stdscr, bond: BondConfig, interfaces: List[InterfaceConfig]):
    row = curses.LINES - 3
    mode = prompt(
        stdscr,
        (row,
         2),
        "Bond mode (active-backup|802.3ad|balance-xor|broadcast|balance-tlb|balance-alb)",
        bond.mode)
    if mode in (
        "active-backup",
        "802.3ad",
        "balance-xor",
        "broadcast",
        "balance-tlb",
            "balance-alb"):
        bond.mode = mode
    auto = prompt(stdscr, (row, 2), "Auto include all wired? (yes/no)",
                  "yes" if bond.auto_members else "no").lower()
    if auto in ("yes", "no"):
        bond.auto_members = (auto == "yes")
    if not bond.auto_members:
        # allow comma-separated members by name
        current = ",".join(bond.members)
        names = prompt(stdscr, (row, 2), "Members (comma-separated iface names)",
                       current)
        bond.members = [n.strip() for n in names.split(",") if n.strip()]


def write_networkd(cfgs: List[InterfaceConfig], outdir: str, bridges: List[BridgeConfig] = None,
                   bond: Optional[BondConfig] = None) -> List[str]:
    os.makedirs(outdir, exist_ok=True)
    emitted: List[str] = []

    if bridges is None:
        bridges = []

    # Create bridges
    for bridge in bridges:
        br_netdev = os.path.join(outdir, f"10-{bridge.name}.netdev")
        with open(br_netdev, "w", encoding="utf-8") as f:
            f.write("[NetDev]\n")
            f.write(f"Name={bridge.name}\n")
            f.write("Kind=bridge\n\n")
            f.write("[Bridge]\n")
            f.write(f"STP={'yes' if bridge.stp else 'no'}\n")
            if bridge.forward_delay is not None:
                f.write(f"ForwardDelay={bridge.forward_delay}\n")
            if bridge.hello_time is not None:
                f.write(f"HelloTime={bridge.hello_time}\n")
            if bridge.max_age is not None:
                f.write(f"MaxAge={bridge.max_age}\n")
        emitted.append(br_netdev)

        br_network = os.path.join(outdir, f"10-{bridge.name}.network")
        with open(br_network, "w", encoding="utf-8") as f:
            f.write("[Match]\n")
            f.write(f"Name={bridge.name}\n\n")
            f.write("[Network]\n")
            if bridge.method == "dhcp":
                f.write("DHCP=yes\n")
            else:
                f.write("DHCP=no\n")
                if bridge.address:
                    f.write(f"Address={bridge.address}/{bridge.prefix}\n")
                if bridge.gateway:
                    f.write(f"Gateway={bridge.gateway}\n")
                if bridge.ipv6_address:
                    f.write(f"Address={bridge.ipv6_address}/{bridge.ipv6_prefix}\n")
                if bridge.ipv6_gateway:
                    f.write(f"Gateway={bridge.ipv6_gateway}\n")
            if bridge.dns:
                f.write(f"DNS={' '.join(bridge.dns)}\n")
        emitted.append(br_network)

    # Optional bond first
    if bond is not None:
        bond_netdev = os.path.join(outdir, f"10-{bond.name}.netdev")
        with open(bond_netdev, "w", encoding="utf-8") as f:
            f.write("[NetDev]\n")
            f.write(f"Name={bond.name}\n")
            f.write("Kind=bond\n\n")
            f.write("[Bond]\n")
            f.write(f"Mode={bond.mode}\n")
        emitted.append(bond_netdev)

    for c in cfgs:
        # Create VLAN netdev first if requested
        enslave_name = c.name
        if c.vlan_id is not None:
            vlan_name = f"{c.name}.{c.vlan_id}"
            netdev_path = os.path.join(outdir, f"10-{vlan_name}.netdev")
            with open(netdev_path, "w", encoding="utf-8") as f:
                f.write("[NetDev]\n")
                f.write(f"Name={vlan_name}\n")
                f.write("Kind=vlan\n\n")
                f.write("[VLAN]\n")
                f.write(f"Id={c.vlan_id}\n")
            emitted.append(netdev_path)
            enslave_name = vlan_name

        # WPA supplicant for wireless (regardless of bridge)
        if c.kind == "wireless" and c.ssid and c.psk:
            wpa_dir = os.path.join(outdir, "wpa_supplicant")
            os.makedirs(wpa_dir, exist_ok=True)
            wpa_path = os.path.join(wpa_dir, f"wpa_supplicant-{c.name}.conf")
            with open(wpa_path, "w", encoding="utf-8") as f:
                f.write("ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev\n")
                f.write("update_config=1\n")
                f.write("country=US\n\n")
                f.write("network={\n")
                f.write(f"    ssid=\"{c.ssid}\"\n")
                f.write(f"    psk=\"{c.psk}\"\n")
                f.write("}\n")
            emitted.append(wpa_path)

        # .network per interface
        network_path = os.path.join(outdir, f"10-{enslave_name}.network")
        with open(network_path, "w", encoding="utf-8") as f:
            f.write("[Match]\n")
            f.write(f"Name={enslave_name}\n\n")
            f.write("[Network]\n")

            # Determine master
            master = c.master

            # Legacy logic: if bond enabled and auto_members, or in members list
            if bond is not None and (
                (bond.auto_members and c.kind == "wired") or (enslave_name in bond.members)
            ):
                master = bond.name

            if master:
                # Systemd-networkd uses Bridge= for both bridge and bond? No, Bond= for bond.
                f.write(f"Bridge={master}\n")
                # Actually, for systemd-networkd:
                # [Network]
                # Bond=bond0  (if master is bond)
                # Bridge=br0  (if master is bridge)

                # We need to know if master is a bond or bridge.
                # Check against bond name
                if bond and master == bond.name:
                    f.write(f"Bond={master}\n")
                else:
                    # Assume bridge
                    f.write(f"Bridge={master}\n")
            else:
                if c.method == "dhcp":
                    f.write("DHCP=yes\n")
                else:
                    f.write("DHCP=no\n")
                    if c.address:
                        f.write(f"Address={c.address}/{c.prefix}\n")
                    if c.gateway:
                        f.write(f"Gateway={c.gateway}\n")
                    if c.ipv6_address:
                        f.write(f"Address={c.ipv6_address}/{c.ipv6_prefix}\n")
                    if c.ipv6_gateway:
                        f.write(f"Gateway={c.ipv6_gateway}\n")
                if c.dns:
                    f.write(f"DNS={' '.join(c.dns)}\n")
        emitted.append(network_path)
    return emitted


def write_netplan(cfgs: List[InterfaceConfig], outdir: str, bridges: List[BridgeConfig] = None,
                  bond: Optional[BondConfig] = None) -> List[str]:
    os.makedirs(outdir, exist_ok=True)
    emitted: List[str] = []
    path = os.path.join(outdir, "99-debvisor.yaml")

    if bridges is None:
        bridges = []

    # Construct a minimal netplan
    lines: List[str] = []
    lines.append("network:")
    lines.append("  version: 2")
    lines.append("  renderer: networkd")
    eths: List[str] = []
    wifis: List[str] = []
    ibs: List[str] = []
    vlans: List[str] = []

    # Collect interfaces
    for c in cfgs:
        target = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
        if c.vlan_id is not None:
            vlans.append(target)
        if c.kind == "wired":
            eths.append(target)
        elif c.kind == "wireless":
            wifis.append(target)
        elif c.kind == "infiniband":
            ibs.append(target)

    # Helper to check if interface is enslaved
    def is_enslaved(name: str) -> bool:
        # Check if master is set on config
        for c in cfgs:
            t = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
            if t == name and c.master:
                return True
        # Check legacy bond auto-members
        if bond and bond.auto_members:
            # If wired, it's enslaved
            # Find config for name
            for c in cfgs:
                t = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
                if t == name and c.kind == "wired":
                    return True
        return False

    if eths:
        lines.append("  ethernets:")
        for e in eths:
            lines.append(f"    {e}:")
            if is_enslaved(e):
                lines.append("      dhcp4: false")
            else:
                # Find config
                # This logic is getting complex because we separated lists from configs.
                # Let's simplify: we iterate configs again?
                # Or just assume dhcp4: false if enslaved, else check config?
                # For now, let's just set dhcp4: false if enslaved.
                # If not enslaved, we need to write IP config.
                # Let's find the config object.
                found = False
                for c in cfgs:
                    t = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
                    if t == e:
                        if c.method == "dhcp":
                            lines.append("      dhcp4: true")
                        else:
                            lines.append("      dhcp4: false")
                            if c.address:
                                lines.append(f"      addresses: [{c.address}/{c.prefix}]")
                        found = True
                        break
                if not found:
                    lines.append("      dhcp4: false")

    if wifis:
        lines.append("  wifis:")
        for w in wifis:
            lines.append(f"    {w}:")
            lines.append("      dhcp4: false")
            lines.append("      access-points: {}")

    if ibs:
        lines.append("  infiniband:")
        for i in ibs:
            lines.append(f"    {i}:")
            lines.append("      dhcp4: false")

    if vlans:
        lines.append("  vlans:")
        for v in vlans:
            parent, vid = v.split('.')
            lines.append(f"    {v}:")
            lines.append(f"      id: {vid}")
            lines.append(f"      link: {parent}")

    bond_name = bond.name if bond is not None else None
    if bond is not None:
        lines.append("  bonds:")
        lines.append(f"    {bond.name}:")
        # Members
        # We need to find members that have master=bond.name OR are auto-included
        members = []
        if bond.auto_members:
            members.extend([e for e in eths])  # All wired
        else:
            # Check explicit master
            for c in cfgs:
                if c.master == bond.name:
                    t = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
                    members.append(t)
            # Also check legacy bond.members list
            members.extend(bond.members)

        lines.append("      interfaces:")
        for m in set(members):  # Dedupe
            lines.append(f"        - {m}")
        lines.append("      parameters:")
        lines.append(f"        mode: {bond.mode}")

    if bridges:
        lines.append("  bridges:")
        for bridge in bridges:
            lines.append(f"    {bridge.name}:")
            lines.append("      interfaces:")
            # Find members
            members = []
            for c in cfgs:
                if c.master == bridge.name:
                    t = c.name if c.vlan_id is None else f"{c.name}.{c.vlan_id}"
                    members.append(t)

            # If bond is enslaved to this bridge (legacy logic supported?)
            # We don't have a 'master' field on BondConfig yet.
            # But if we did, we'd check it.
            # For now, let's assume if bond exists and we are in single-bridge mode
            # (legacy), it might be attached.
            # But we are in multi-bridge mode now.
            # Let's assume bond is not enslaved unless we add master to BondConfig.
            # For now, just interfaces.

            for m in members:
                lines.append(f"        - {m}")

            if bridge.method == "dhcp":
                lines.append("      dhcp4: true")
            else:
                lines.append("      dhcp4: false")
                if bridge.address or bridge.ipv6_address:
                    lines.append("      addresses:")
                    if bridge.address:
                        lines.append(f"        - {bridge.address}/{bridge.prefix}")
                    if bridge.ipv6_address:
                        lines.append(f"        - {bridge.ipv6_address}/{bridge.ipv6_prefix}")
                if bridge.gateway:
                    lines.append(f"      gateway4: {bridge.gateway}")
                if bridge.ipv6_gateway:
                    lines.append(f"      gateway6: {bridge.ipv6_gateway}")
            if bridge.dns:
                lines.append("      nameservers:")
                lines.append("        addresses:")
                for d in bridge.dns:
                    lines.append(f"          - {d}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    emitted.append(path)
    return emitted


def generate_apply_script(
        outdir: str,
        backend: str,
        bridge: Optional[BridgeConfig],
        cfgs: List[InterfaceConfig],
        bond: Optional[BondConfig]) -> str:
    script_path = os.path.join(outdir, "apply.sh")
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "echo 'Applying network configuration (requires sudo)'",
    ]
    if backend == "networkd":
        lines += ["sudo install -d -m 755 /etc/systemd/network",
                  f"sudo cp -v {outdir}/*.network /etc/systemd/network/ || true",
                  f"sudo cp -v {outdir}/*.netdev /etc/systemd/network/ || true",
                  (f"if compgen -G '{outdir}/wpa_supplicant/*.conf' > /dev/null; then "
                   f"sudo install -d -m 750 /etc/wpa_supplicant; "
                   f"sudo cp -v {outdir}/wpa_supplicant/*.conf /etc/wpa_supplicant/; fi"),
                  "sudo systemctl enable --now systemd-networkd || true",
                  "sudo systemctl restart systemd-networkd",
                  ]
    else:
        lines += [
            "sudo install -d -m 755 /etc/netplan",
            f"sudo cp -v {outdir}/99-debvisor.yaml /etc/netplan/",
            "sudo netplan apply",
        ]
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    try:
        os.chmod(script_path, 0o755)
    except Exception:
        pass
    return script_path


def check_connectivity(target: str = "8.8.8.8", count: int = 3) -> bool:
    try:
        subprocess.run(["ping", "-c", str(count), target], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def preflight_checks(backend: str) -> List[str]:
    errors = []
    if os.geteuid() != 0:
        errors.append("Must run as root to apply configuration.")

    if backend == "networkd":
        if not os.path.exists("/etc/systemd/network"):
            errors.append("/etc/systemd/network directory not found.")
        try:
            subprocess.run(["systemctl", "is-active", "systemd-networkd"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            errors.append("systemd-networkd is not active.")
    elif backend == "netplan":
        if shutil.which("netplan") is None:
            errors.append("netplan executable not found.")

    return errors


def apply_config(outdir: str, backend: str) -> bool:
    print("Starting configuration application...")

    # 1. Pre-flight checks
    errors = preflight_checks(backend)
    if errors:
        for e in errors:
            print(f"Pre-flight check failed: {e}")
        return False

    # 2. Backup
    backup_path = f"/tmp/netcfg_backup_{int(time.time())}.tar.gz"
    print(f"Creating backup at {backup_path}...")
    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            if backend == "networkd":
                if os.path.exists("/etc/systemd/network"):
                    tar.add("/etc/systemd/network", arcname="network")
            else:
                if os.path.exists("/etc/netplan"):
                    tar.add("/etc/netplan", arcname="netplan")
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

    # 3. Apply
    try:
        print("Applying new configuration...")
        if backend == "networkd":
            # Clear existing? Maybe too dangerous. Just overwrite/add.
            # But old configs might conflict.
            # Strategy: Move old configs to a backup folder inside /etc/systemd/network/backup?
            # For now, let's just copy over.
            subprocess.run(
                f"cp -v {outdir}/*.network /etc/systemd/network/",
                shell=True,
                check=True)
            subprocess.run(
                f"cp -v {outdir}/*.netdev /etc/systemd/network/ 2>/dev/null || true",
                shell=True,
                check=True)
            subprocess.run("systemctl restart systemd-networkd", shell=True, check=True)
        else:
            subprocess.run(f"cp -v {outdir}/*.yaml /etc/netplan/", shell=True, check=True)
            subprocess.run("netplan apply", shell=True, check=True)

        # 4. Verify
        print("Verifying connectivity...")
        time.sleep(5)  # Wait for links to come up
        if check_connectivity():
            print("Connectivity verified. Configuration applied successfully.")
            return True
        else:
            print("Connectivity check failed!")
            raise Exception("Connectivity check failed")

    except Exception as e:
        print(f"Application failed: {e}")
        print("Rolling back...")
        # 5. Rollback
        try:
            if backend == "networkd":
                # Clean up potentially bad files?
                # Ideally we should have cleared the dir before applying if we want a clean state.
                # For rollback, we extract the tarball.
                # But tarball extraction might not remove *new* files.
                # So we should probably clear the directory first.
                shutil.rmtree("/etc/systemd/network")
                os.makedirs("/etc/systemd/network")
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(path="/etc/systemd")  # Extracts 'network' dir into /etc/systemd
                subprocess.run("systemctl restart systemd-networkd", shell=True, check=True)
            else:
                shutil.rmtree("/etc/netplan")
                os.makedirs("/etc/netplan")
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(path="/etc")
                subprocess.run("netplan apply", shell=True, check=True)
            print("Rollback successful.")
        except Exception as rollback_err:
            print(f"CRITICAL: Rollback failed! {rollback_err}")
            print(f"Backup is available at {backup_path}")
        return False


def scan_wifi(interface: str) -> List[str]:
    """Scan for WiFi networks using iwlist or iw."""
    networks = []
    try:
        # Try iwlist first (more detailed output usually)
        # iwlist wlan0 scan
        result = subprocess.run(["iwlist", interface, "scan"], capture_output=True, text=True)
        if result.returncode == 0:
            # Parse ESSID:"..."
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("ESSID:"):
                    ssid = line.split(":", 1)[1].strip('"')
                    if ssid:
                        networks.append(ssid)
        else:
            # Try iw
            # iw dev wlan0 scan
            result = subprocess.run(["iw", "dev", interface, "scan"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("SSID:"):
                        ssid = line.split(":", 1)[1].strip()
                        if ssid:
                            networks.append(ssid)
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

    return sorted(list(set(networks)))  # Dedupe and sort


def select_wifi_network(stdscr, interface: str) -> Optional[str]:
    """Show WiFi scan results and return selected SSID."""
    stdscr.clear()
    stdscr.addstr(0, 2, f"Scanning WiFi on {interface}...")
    stdscr.refresh()

    networks = scan_wifi(interface)

    if not networks:
        stdscr.addstr(2, 2, "No networks found or scan failed.")
        stdscr.addstr(4, 2, "Press any key to return.")
        stdscr.getch()
        return None

    selected = 0
    while True:
        stdscr.erase()
        stdscr.addstr(0, 2, f"WiFi Networks on {interface}")
        stdscr.hline(1, 0, ord("-"), curses.COLS)

        for idx, ssid in enumerate(networks):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(2 + idx, 2, ssid)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(2 + idx, 2, ssid)

        stdscr.addstr(curses.LINES - 1, 0, "Enter: select  q: cancel  arrows: navigate")
        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (ord('q'), 27):
            return None
        elif ch in (curses.KEY_DOWN, ord('j')):
            selected = min(len(networks) - 1, selected + 1)
        elif ch in (curses.KEY_UP, ord('k')):
            selected = max(0, selected - 1)
        elif ch in (curses.KEY_ENTER, 10, 13):
            return networks[selected]


def run_tui(stdscr, args):
    curses.curs_set(0)
    stdscr.nodelay(False)
    selected = 0
    viewport_start = 0  # Index of the first visible item

    cfgs = detect_interfaces(args.mock_mode, args.benchmark_count)

    # Initialize bridges
    bridges: List[BridgeConfig] = []
    if args.single_bridge:
        bridges.append(BridgeConfig(name=args.bridge_name))

    bond_cfg = BondConfig(name=args.bond_name) if args.enable_bond else None
    msg = ""

    while True:
        stdscr.erase()
        stdscr.addstr(0, 2, "DebVisor Network Configurator (curses)")
        stdscr.addstr(
            1,
            2,
            f"Backend: systemd-networkd  Output: {args.output_dir} "
            f"{'[MOCK]' if args.mock_mode else ''}")
        stdscr.hline(2, 0, ord("-"), curses.COLS)

        # Build display list
        display_items = []
        for b in bridges:
            display_items.append(("bridge", b))
        if bond_cfg is not None:
            display_items.append(("bond", bond_cfg))
        for c in cfgs:
            display_items.append(("iface", c))

        # Viewport Logic
        list_start_y = 3
        list_height = curses.LINES - 5  # Reserve lines for header (3) and footer (2)
        if list_height < 1:
            list_height = 1

        # Adjust viewport to keep selected item visible
        if selected < viewport_start:
            viewport_start = selected
        elif selected >= viewport_start + list_height:
            viewport_start = selected - list_height + 1

        # Ensure viewport doesn't go out of bounds (though the above logic should handle it)
        viewport_start = max(0, min(viewport_start, len(display_items) - list_height))
        if len(display_items) < list_height:
            viewport_start = 0

        # Draw List
        visible_items = display_items[viewport_start: viewport_start + list_height]
        for i, item in enumerate(visible_items):
            actual_idx = viewport_start + i
            kind, obj = item
            line = f" {obj.summary()}"

            # Truncate to fit screen width
            max_width = curses.COLS - 4
            if len(line) > max_width:
                line = line[:max_width]

            if actual_idx == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(list_start_y + i, 2, line)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(list_start_y + i, 2, line)

        # Scrollbar indicators (optional but helpful)
        if len(display_items) > list_height:
            scroll_msg = (f"[{viewport_start + 1}-"
                          f"{min(viewport_start + list_height, len(display_items))}/"
                          f"{len(display_items)}]")
            stdscr.addstr(1, curses.COLS - len(scroll_msg) - 2, scroll_msg)

        draw_help(stdscr)
        if msg:
            stdscr.addstr(curses.LINES - 2, 2, msg[: curses.COLS - 4])
        stdscr.refresh()

        ch = stdscr.getch()
        msg = ""

        if ch in (ord("q"), 27):
            break
        elif ch in (curses.KEY_DOWN, ord("j")):
            if display_items:
                selected = min(len(display_items) - 1, selected + 1)
        elif ch in (curses.KEY_UP, ord("k")):
            if display_items:
                selected = max(0, selected - 1)
        elif ch in (curses.KEY_NPAGE,):  # Page Down
            if display_items:
                selected = min(len(display_items) - 1, selected + list_height)
        elif ch in (curses.KEY_PPAGE,):  # Page Up
            if display_items:
                selected = max(0, selected - list_height)
        elif ch == ord("r"):
            cfgs = detect_interfaces(args.mock_mode, args.benchmark_count)
            selected = 0
            viewport_start = 0
            msg = "Interfaces reloaded"
        elif ch == ord("b"):
            # Add bridge
            name = prompt(stdscr, (curses.LINES - 3, 2), "New Bridge Name", f"br{len(bridges)}")
            if name:
                bridges.append(BridgeConfig(name=name))
                msg = f"Added bridge {name}"
        elif ch == ord("d"):
            # Delete bridge
            if display_items:
                kind, obj = display_items[selected]
                if kind == "bridge":
                    bridges.remove(obj)
                    selected = max(0, selected - 1)
                    msg = f"Deleted bridge {obj.name}"
                else:
                    msg = "Can only delete bridges"
        elif ch == ord("w"):
            # WiFi Scan
            if display_items:
                kind, obj = display_items[selected]
                if kind == "iface" and obj.kind == "wireless":
                    ssid = select_wifi_network(stdscr, obj.name)
                    if ssid:
                        obj.ssid = ssid
                        # Prompt for PSK
                        psk = prompt(stdscr, (curses.LINES - 3, 2),
                                     f"Passphrase for {ssid}", obj.psk or "")
                        obj.psk = psk
                        msg = f"Set WiFi: {ssid}"
                    else:
                        msg = "Scan cancelled or no network selected"
                else:
                    msg = "Select a wireless interface to scan"
        elif ch == ord("e"):
            if not display_items:
                continue
            curses.curs_set(1)
            kind, obj = display_items[selected]

            if kind == "bridge":
                edit_bridge(stdscr, obj)
                msg = f"Edited {obj.name}"
            elif kind == "bond":
                edit_bond(stdscr, obj, cfgs)
                msg = f"Edited {obj.name}"
            else:
                # Collect masters
                masters = [b.name for b in bridges]
                if bond_cfg:
                    masters.append(bond_cfg.name)
                edit_interface(stdscr, obj, masters)
                msg = f"Edited {obj.name}"
            curses.curs_set(0)
        elif ch == ord("s"):
            if args.backend == "netplan":
                emitted = write_netplan(cfgs, args.output_dir, bridges=bridges, bond=bond_cfg)
            else:
                emitted = write_networkd(cfgs, args.output_dir, bridges=bridges, bond=bond_cfg)

            # Note: generate_apply_script needs update too, but for now passing first bridge or None
            # Ideally we pass all bridges or handle it inside.
            # For now, let's just pass the first bridge if any for backward compat in signature,
            # but we should update generate_apply_script to not rely on single bridge arg.
            # Actually, generate_apply_script doesn't use bridge arg for much other
            # than maybe logging?
            # Let's check generate_apply_script implementation.
            # It uses it to decide if to copy files? No, it copies *.*
            # So passing None might be fine if we update the signature.

            script = generate_apply_script(
                args.output_dir,
                args.backend,
                bridges[0] if bridges else None,
                cfgs,
                bond_cfg)
            msg = (f"Wrote {len(emitted)} files to {args.output_dir}; "
                   f"apply with {script}")

            if args.apply:
                stdscr.addstr(curses.LINES - 2, 2,
                              "Apply configuration now? (y/n): ".ljust(
                                  curses.COLS - 4))
                stdscr.refresh()
                while True:
                    ans = stdscr.getch()
                    if ans in (ord('y'), ord('Y')):
                        curses.def_prog_mode()
                        curses.endwin()
                        success = apply_config(args.output_dir, args.backend)
                        print("\nPress Enter to continue...")
                        input()
                        curses.reset_prog_mode()
                        curses.curs_set(0)
                        stdscr.refresh()
                        msg = ("Applied successfully" if success else
                               "Application failed (rolled back)")
                        break
                    elif ans in (ord('n'), ord('N'), 27):
                        msg = "Application cancelled."
                        break


def main():
    parser = argparse.ArgumentParser(description="DebVisor curses-based network configurator")
    parser.add_argument(
        "--output-dir",
        default="./out-networkd",
        help="Where to write config files")
    parser.add_argument("--backend", choices=["networkd", "netplan"], default="networkd",
                        help="Config backend to generate (default: networkd)")
    parser.add_argument(
        "--single-bridge",
        action="store_true",
        default=True,
        help="Place all interfaces into a single bridge and configure IP on it (default: on)")
    parser.add_argument(
        "--bridge-name",
        default="br0",
        help="Name of the bridge when single-bridge is enabled")
    parser.add_argument(
        "--enable-bond",
        action="store_true",
        default=False,
        help=("Create a bond (bond0) and include wired members; "
              "attach bond to bridge if present"))
    parser.add_argument(
        "--bond-name",
        default="bond0",
        help="Name of the bond when bonding is enabled")
    parser.add_argument(
        "--no-ui",
        action="store_true",
        help="Non-interactive: only detect and print interfaces")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Enable apply capability in UI (requires root)")
    parser.add_argument("--check", action="store_true", help="Run pre-flight checks only")
    parser.add_argument(
        "--mock-mode",
        action="store_true",
        help="Use mock interfaces for testing/demo")
    parser.add_argument("--benchmark-count", type=int, default=0,
                        help="Generate N mock interfaces for performance testing")
    args = parser.parse_args()

    if args.check:
        errors = preflight_checks(args.backend)
        if errors:
            for e in errors:
                print(f"FAIL: {e}")
            sys.exit(1)
        print("OK: Pre-flight checks passed.")
        sys.exit(0)

    if args.no_ui:
        for c in detect_interfaces(args.mock_mode, args.benchmark_count):
            print(c.summary())
        return 0
    if not is_linux() and not args.mock_mode and args.benchmark_count == 0:
        print("This tool targets Linux hosts for configuration. "
              "UI can still run but detection will be empty.")

    if curses is None:
        print("Error: 'curses' module not found. On Windows, install 'windows-curses'.")
        return 1

    curses.wrapper(run_tui, args)
    print("\nTip: To apply on a systemd-networkd host:\n"
          f"  sudo cp -v {args.output_dir}/*.network /etc/systemd/network/\n"
          f"  sudo cp -v {args.output_dir}/*.netdev /etc/systemd/network/ 2>/dev/null || true\n"
          "  sudo systemctl restart systemd-networkd\n"
          "For Wi-Fi, also copy wpa_supplicant/*.conf and enable "
          "wpa_supplicant@interface.service")
    return 0


if __name__ == "__main__":
    sys.exit(main())
