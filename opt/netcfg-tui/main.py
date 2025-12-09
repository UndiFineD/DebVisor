#!/usr/bin/env python3
"""
DebVisor Network Configuration TUI (Text User Interface)

Interactive terminal UI for managing network configurations:
- Interactive menu-driven interface
- Network interface management (up/down, address configuration)
- Route management (add/delete/view routes)
- DNS configuration
- Network diagnostics
- Configuration persistence
- Dry-run preview before applying changes

Usage:
    python opt/netcfg-tui/main.py
    python opt/netcfg-tui/main.py --apply <config_file>
"""

import os
import sys
import json
import subprocess
import argparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import curses
import traceback


class InterfaceStatus(Enum):
    """Network interface status."""

    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"


class ConfigChangeType(Enum):
    """Type of configuration change."""

    INTERFACE_UP = "interface_up"
    INTERFACE_DOWN = "interface_down"
    INTERFACE_ADDRESS = "interface_address"
    ROUTE_ADD = "route_add"
    ROUTE_DELETE = "route_delete"
    DNS_SET = "dns_set"
    HOSTNAME_SET = "hostname_set"


@dataclass
class NetworkInterface:
    """Network interface configuration."""

    name: str
    status: InterfaceStatus
    mtu: int = 1500
    addresses: List[str] = field(default_factory=list)
    gateway: Optional[str] = None
    dns_servers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "status": self.status.value,
            "mtu": self.mtu,
            "addresses": self.addresses,
            "gateway": self.gateway,
            "dns_servers": self.dns_servers,
        }


@dataclass
class RouteEntry:
    """Network route entry."""

    destination: str
    gateway: str
    metric: int = 0
    interface: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "destination": self.destination,
            "gateway": self.gateway,
            "metric": self.metric,
            "interface": self.interface,
        }


@dataclass
class ConfigChange:
    """Pending configuration change."""

    change_type: ConfigChangeType
    timestamp: str
    target: str
    details: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "change_type": self.change_type.value,
            "timestamp": self.timestamp,
            "target": self.target,
            "details": self.details,
            "description": self.description,
            "applied": self.applied,
        }


class NetworkConfig:
    """Network configuration management."""

    def __init__(self) -> None:
        """Initialize network config."""
        self.interfaces: Dict[str, NetworkInterface] = {}
        self.routes: List[RouteEntry] = []
        self.hostname: str = ""
        self.dns_servers: List[str] = []
        self.changes: List[ConfigChange] = []
        self.load_current_config()

    def load_current_config(self) -> None:
        """Load current network configuration from system."""
        try:
            # Try Linux first
            if os.path.exists("/sys/class/net"):
                self._load_linux_config()
            # Try Windows
            elif os.name == "nt":
                self._load_windows_config()
        except Exception as e:
            print(f"Warning: Could not load network config: {e}")

    def _load_linux_config(self) -> None:
        """Load Linux network configuration."""
        try:
            result = subprocess.run(
                ["ip", "link", "show"], capture_output=True, text=True, timeout=5
            )  # nosec B603, B607
            for line in result.stdout.split("\n"):
                if ":" in line and not line.startswith(" "):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        name = parts[1].strip()
                        status = (
                            InterfaceStatus.UP if "UP" in line else InterfaceStatus.DOWN
                        )
                        self.interfaces[name] = NetworkInterface(
                            name=name, status=status
                        )

            # Get addresses
            result = subprocess.run(
                ["ip", "addr", "show"], capture_output=True, text=True, timeout=5
            )  # nosec B603, B607
            current_iface = None
            for line in result.stdout.split("\n"):
                if line and not line.startswith(" "):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        current_iface = parts[1].strip()
                elif "inet" in line and current_iface:
                    addr = line.strip().split()[1]
                    if current_iface in self.interfaces:
                        self.interfaces[current_iface].addresses.append(addr)

            # Get routes
            result = subprocess.run(
                ["ip", "route", "show"], capture_output=True, text=True, timeout=5
            )  # nosec B603, B607
            for line in result.stdout.split("\n"):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        route = RouteEntry(
                            destination=parts[0],
                            gateway=(
                                parts[2] if parts[1] == "via" else "0.0.0.0"
                            ),  # nosec B104
                        )
                        self.routes.append(route)

            # Get hostname
            try:
                with open("/etc/hostname", "r") as f:
                    self.hostname = f.read().strip()
            except BaseException:
                pass

        except Exception as e:
            print(f"Error loading Linux config: {e}")

    def _load_windows_config(self) -> None:
        """Load Windows network configuration."""
        try:
            result = subprocess.run(
                ["ipconfig", "/all"], capture_output=True, text=True, timeout=5
            )  # nosec B603, B607
            current_adapter = None

            for line in result.stdout.split("\n"):
                if "adapter" in line.lower():
                    parts = line.split(":")
                    if len(parts) >= 1:
                        current_adapter = parts[0].strip()
                        if current_adapter not in self.interfaces:
                            self.interfaces[current_adapter] = NetworkInterface(
                                name=current_adapter, status=InterfaceStatus.UNKNOWN
                            )
                elif "IPv4" in line and current_adapter:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        addr = parts[1].strip()
                        if current_adapter in self.interfaces:
                            self.interfaces[current_adapter].addresses.append(addr)

        except Exception as e:
            print(f"Error loading Windows config: {e}")

    def add_change(
        self,
        change_type: ConfigChangeType,
        target: str,
        details: Optional[Dict[str, Any]] = None,
        description: str = "",
    ) -> None:
        """
        Add a pending configuration change.

        Args:
            change_type: Type of change
            target: Target (interface/route name)
            details: Additional details
            description: Human-readable description
        """
        change = ConfigChange(
            change_type=change_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            target=target,
            details=details or {},
            description=description,
        )
        self.changes.append(change)

    def save_config(self, filepath: str) -> bool:
        """
        Save configuration to file.

        Args:
            filepath: Path to save configuration

        Returns:
            True if successful
        """
        try:
            config_dict = {
                "interfaces": {k: v.to_dict() for k, v in self.interfaces.items()},
                "routes": [r.to_dict() for r in self.routes],
                "hostname": self.hostname,
                "dns_servers": self.dns_servers,
                "changes": [c.to_dict() for c in self.changes],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

            with open(filepath, "w") as f:
                json.dump(config_dict, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def load_config(self, filepath: str) -> bool:
        """
        Load configuration from file.

        Args:
            filepath: Path to load configuration

        Returns:
            True if successful
        """
        try:
            with open(filepath, "r") as f:
                config_dict = json.load(f)

            # Load interfaces
            for name, iface_dict in config_dict.get("interfaces", {}).items():
                status = InterfaceStatus(iface_dict.get("status", "unknown"))
                iface = NetworkInterface(
                    name=name,
                    status=status,
                    mtu=iface_dict.get("mtu", 1500),
                    addresses=iface_dict.get("addresses", []),
                    gateway=iface_dict.get("gateway"),
                    dns_servers=iface_dict.get("dns_servers", []),
                )
                self.interfaces[name] = iface

            # Load routes
            self.routes = [RouteEntry(**r) for r in config_dict.get("routes", [])]

            self.hostname = config_dict.get("hostname", "")
            self.dns_servers = config_dict.get("dns_servers", [])

            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def apply_changes(self, dry_run: bool = False) -> Tuple[bool, List[str]]:
        """
        Apply all pending changes.

        Args:
            dry_run: If True, only preview changes without applying

        Returns:
            Tuple of (success, list of executed commands)
        """
        commands = []

        try:
            for change in self.changes:
                if change.applied:
                    continue

                cmd = self._build_command(change)
                if cmd:
                    commands.append(cmd)

                    if not dry_run:
                        try:
                            subprocess.run(
                                cmd, shell=True, check=True, timeout=10
                            )  # nosec B602
                            change.applied = True
                        except subprocess.CalledProcessError as e:
                            return False, commands + [f"FAILED: {cmd} ({e})"]

            return True, commands

        except Exception as e:
            return False, commands + [f"ERROR: {e}"]

    def _build_command(self, change: ConfigChange) -> Optional[str]:
        """Build shell command for a change."""
        if os.name == "nt":
            return self._build_windows_command(change)
        else:
            return self._build_linux_command(change)

    def _build_linux_command(self, change: ConfigChange) -> Optional[str]:
        """Build Linux command for a change."""
        if change.change_type == ConfigChangeType.INTERFACE_UP:
            return f"ip link set {change.target} up"
        elif change.change_type == ConfigChangeType.INTERFACE_DOWN:
            return f"ip link set {change.target} down"
        elif change.change_type == ConfigChangeType.INTERFACE_ADDRESS:
            addr = change.details.get("address", "")
            return f"ip addr add {addr} dev {change.target}"
        elif change.change_type == ConfigChangeType.ROUTE_ADD:
            dest = change.details.get("destination", "")
            gw = change.details.get("gateway", "")
            return f"ip route add {dest} via {gw}"
        elif change.change_type == ConfigChangeType.ROUTE_DELETE:
            dest = change.details.get("destination", "")
            return f"ip route del {dest}"
        elif change.change_type == ConfigChangeType.HOSTNAME_SET:
            return f"hostnamectl set-hostname {change.target}"

        return None

    def _build_windows_command(self, change: ConfigChange) -> Optional[str]:
        """Build Windows command for a change."""
        if change.change_type == ConfigChangeType.INTERFACE_UP:
            return f"netsh interface set interface {change.target} admin=enabled"
        elif change.change_type == ConfigChangeType.INTERFACE_DOWN:
            return f"netsh interface set interface {change.target} admin=disabled"
        elif change.change_type == ConfigChangeType.HOSTNAME_SET:
            return f"netdom renamecomputer %COMPUTERNAME% /newname:{change.target}"

        return None


class NetworkConfigTUI:
    """Text User Interface for Network Configuration."""

    def __init__(self) -> None:
        """Initialize TUI."""
        self.config = NetworkConfig()
        self.current_menu = "main"
        self.selected = 0

    def run(self, stdscr: Any) -> None:
        """
        Run the TUI.

        Args:
            stdscr: Curses window
        """
        curses.curs_set(0)
        stdscr.nodelay(1)

        while True:
            try:
                stdscr.clear()
                self._render_menu(stdscr)

                key = stdscr.getch()
                if key == ord("q"):
                    break
                elif key == ord("w"):
                    self.config.save_config("network_config.json")
                elif key == curses.KEY_UP:
                    self.selected = max(0, self.selected - 1)
                elif key == curses.KEY_DOWN:
                    self.selected += 1
                elif key == ord("\n"):
                    if self._handle_selection():
                        break

                stdscr.refresh()
            except KeyboardInterrupt:
                break
            except Exception as e:
                stdscr.addstr(0, 0, f"Error: {e}")
                stdscr.refresh()

    def _render_menu(self, stdscr: Any) -> None:
        """Render the current menu."""
        rows, cols = stdscr.getmaxyx()

        if self.current_menu == "main":
            self._render_main_menu(stdscr, rows, cols)
        elif self.current_menu == "interfaces":
            self._render_interfaces_menu(stdscr, rows, cols)
        elif self.current_menu == "routes":
            self._render_routes_menu(stdscr, rows, cols)
        elif self.current_menu == "pending":
            self._render_pending_changes_menu(stdscr, rows, cols)

    def _render_main_menu(self, stdscr: Any, rows: int, cols: int) -> None:
        """Render main menu."""
        menu_items = [
            "Manage Interfaces",
            "Manage Routes",
            "Configure DNS",
            "View Pending Changes",
            "Save Configuration",
            "Load Configuration",
            "Exit",
        ]

        stdscr.addstr(0, 0, "DebVisor Network Configuration", curses.A_BOLD)
        stdscr.addstr(2, 0, "Health Score:", curses.A_BOLD)

        for i, item in enumerate(menu_items):
            if i == self.selected:
                stdscr.addstr(4 + i, 2, f"> {item}", curses.A_REVERSE)
            else:
                stdscr.addstr(4 + i, 2, f"  {item}")

        stdscr.addstr(
            rows - 2, 0, "[UP/DOWN] Navigate | [ENTER] Select | [W] Save | [Q] Quit"
        )

    def _render_interfaces_menu(self, stdscr: Any, rows: int, cols: int) -> None:
        """Render interfaces menu."""
        stdscr.addstr(0, 0, "Network Interfaces", curses.A_BOLD)

        row = 2
        for i, (name, iface) in enumerate(self.config.interfaces.items()):
            status_str = f"[{iface.status.value.upper()}]"
            addr_str = ", ".join(iface.addresses) if iface.addresses else "No addresses"

            if i == self.selected:
                stdscr.addstr(
                    row, 2, f"> {name} {status_str} - {addr_str}", curses.A_REVERSE
                )
            else:
                stdscr.addstr(row, 2, f"  {name} {status_str} - {addr_str}")

            row += 1

    def _render_routes_menu(self, stdscr: Any, rows: int, cols: int) -> None:
        """Render routes menu."""
        stdscr.addstr(0, 0, "Network Routes", curses.A_BOLD)

        row = 2
        for i, route in enumerate(self.config.routes):
            route_str = f"{route.destination} via {route.gateway}"

            if i == self.selected:
                stdscr.addstr(row, 2, f"> {route_str}", curses.A_REVERSE)
            else:
                stdscr.addstr(row, 2, f"  {route_str}")

            row += 1

    def _render_pending_changes_menu(self, stdscr: Any, rows: int, cols: int) -> None:
        """Render pending changes menu."""
        stdscr.addstr(
            0, 0, f"Pending Changes ({len(self.config.changes)})", curses.A_BOLD
        )

        row = 2
        for i, change in enumerate(self.config.changes):
            change_str = f"{change.change_type.value}: {change.target}"

            if i == self.selected:
                stdscr.addstr(row, 2, f"> {change_str}", curses.A_REVERSE)
            else:
                stdscr.addstr(row, 2, f"  {change_str}")

            row += 1

        if self.config.changes:
            row += 1
            stdscr.addstr(row, 2, "[A] Apply Changes | [D] Discard")

    def _handle_selection(self) -> bool:
        """Handle menu selection. Returns True if should exit."""
        if self.current_menu == "main":
            if self.selected == 0:
                self.current_menu = "interfaces"
            elif self.selected == 1:
                self.current_menu = "routes"
            elif self.selected == 6:
                return True  # Exit

        return False

    def run_interactive(self) -> None:
        """Run interactive mode."""
        try:
            curses.wrapper(self.run)
        except Exception as e:
            print(f"TUI Error: {e}")
            traceback.print_exc()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="DebVisor Network Configuration TUI")
    parser.add_argument(
        "--apply", metavar="CONFIG", help="Apply configuration from file"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without applying"
    )
    parser.add_argument("--save", metavar="FILE", help="Save configuration to file")
    parser.add_argument("--load", metavar="FILE", help="Load configuration from file")

    args = parser.parse_args()

    config = NetworkConfig()

    if args.load:
        if not config.load_config(args.load):
            return 1
        print(f"? Loaded configuration from {args.load}")

    if args.apply:
        if not config.load_config(args.apply):
            return 1

        print(f"Applying configuration from {args.apply}...")
        success, commands = config.apply_changes(dry_run=args.dry_run)

        print("\nCommands to execute:")
        for cmd in commands:
            print(f"  {cmd}")

        if args.dry_run:
            print("\n[DRY RUN] No changes applied")
        elif success:
            print("\n? Configuration applied successfully")
            return 0
        else:
            print("\n? Configuration application failed")
            return 1

    if args.save:
        if config.save_config(args.save):
            print(f"? Saved configuration to {args.save}")
        else:
            return 1

    if not args.apply and not args.save:
        # Interactive mode
        tui = NetworkConfigTUI()
        tui.run_interactive()

    return 0


if __name__ == "__main__":
    sys.exit(main())
