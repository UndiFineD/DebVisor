# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

"""
DebVisor Network Configuration TUI Application.
Uses urwid for the interface and netcfg_tui_full for backend logic.
"""

from netcfg_tui_full import NetworkConfigurationManager, Iproute2Backend
import urwid
import logging
import sys
import os
from typing import Optional

# Ensure opt is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Setup logging
logging.basicConfig(filename="netcfg_tui.log", level=logging.DEBUG)


class NetCfgApp:
    def __init__(self) -> None:
    # Initialize backend
        self.backend = Iproute2Backend()
        self.manager = NetworkConfigurationManager(backend=self.backend)

        self.palette = [
            ("body", "black", "light gray"),
            ("header", "white", "dark blue", "bold"),
            ("button", "black", "dark cyan"),
            ("button_focus", "white", "dark blue", "bold"),
            ("status", "white", "dark blue"),
            ("status_ok", "light green", "dark blue", "bold"),
            ("status_err", "light red", "dark blue", "bold"),
            ("title", "white", "dark blue", "bold"),
        ]

        self.main_loop: Optional[urwid.MainLoop] = None
        self.status_bar = urwid.Text("Ready - Press 'q' to quit")

    def create_interface_list(self) -> urwid.ListBox:
        """Create the list of interfaces."""
        try:
            interfaces = self.manager.get_all_interfaces_status()
        except Exception as e:
            logging.error(f"Error getting interfaces: {e}")
            interfaces = []

        body = []
        if not interfaces:
            body.append(urwid.Text("No interfaces found or backend error."))

        for iface in interfaces:
        # Use Unicode symbols for state if available (kmscon supports this)
            state_symbol = "●" if iface.state.value == "up" else "○"

            label = f"{state_symbol} {iface.name:<10} | {iface.interface_type.value:<10} | {iface.state.value}"
            button = urwid.Button(label)
            urwid.connect_signal(button, "click", self.on_interface_click, iface.name)
            body.append(urwid.AttrMap(button, "button", "button_focus"))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def on_interface_click(self, button: urwid.Button, interface_name: str) -> None:
        """Handle interface selection."""
        self.status_bar.set_text(f"Selected: {interface_name}")
        self.show_edit_dialog(interface_name)

    def show_edit_dialog(self, interface_name: str) -> None:
        """Show dialog to edit interface settings."""
        # Fetch current config
        try:
            iface = self.manager.get_interface_config(interface_name)
            current_ip = ""
            current_mask = "24"
            current_gw = ""
            current_ip6 = ""
            current_mask6 = "64"
            current_gw6 = ""

            if iface and iface.addresses:
                for addr in iface.addresses:
                    if addr.family.value == "ipv4":
                        current_ip = addr.address
                        current_mask = str(addr.netmask)
                        current_gw = addr.gateway or ""
                    elif addr.family.value == "ipv6":
                        current_ip6 = addr.address
                        current_mask6 = str(addr.netmask)
                        current_gw6 = addr.gateway or ""

        except Exception as e:
            logging.error(f"Error fetching config for {interface_name}: {e}")
            current_ip = ""
            current_mask = "24"
            current_gw = ""
            current_ip6 = ""
            current_mask6 = "64"
            current_gw6 = ""

        # Create edit widgets
        self.edit_ip = urwid.Edit("IPv4 Address: ", current_ip)
        self.edit_mask = urwid.Edit("IPv4 Netmask (CIDR): ", current_mask)
        self.edit_gw = urwid.Edit("IPv4 Gateway: ", current_gw)

        self.edit_ip6 = urwid.Edit("IPv6 Address: ", current_ip6)
        self.edit_mask6 = urwid.Edit("IPv6 Prefix (CIDR): ", current_mask6)
        self.edit_gw6 = urwid.Edit("IPv6 Gateway: ", current_gw6)

        # Buttons
        btn_save = urwid.Button("Save")
        urwid.connect_signal(
            btn_save, "click", self.save_interface_config, interface_name
        )

        btn_cancel = urwid.Button("Cancel")
        urwid.connect_signal(btn_cancel, "click", self.close_dialog)

        # Layout
        pile = urwid.Pile(
            [
                urwid.Text(f"Edit Interface: {interface_name}", align="center"),
                urwid.Divider(),
                urwid.Text("IPv4 Configuration", align="left"),
                self.edit_ip,
                self.edit_mask,
                self.edit_gw,
                urwid.Divider(),
                urwid.Text("IPv6 Configuration", align="left"),
                self.edit_ip6,
                self.edit_mask6,
                self.edit_gw6,
                urwid.Divider(),
                urwid.Columns(
                    [
                        urwid.AttrMap(btn_save, "button", "button_focus"),
                        urwid.AttrMap(btn_cancel, "button", "button_focus"),
                    ]
                ),
            ]
        )

        if not self.main_loop:
            return

        self.overlay = urwid.Overlay(
            urwid.LineBox(pile),
            self.main_loop.widget,
            align="center",
            width=("relative", 50),
            valign="middle",
            height=("relative", 50),
        )
        self.main_loop.widget = self.overlay

    def close_dialog(self, button: urwid.Button) -> None:
        """Close the overlay dialog."""
        if hasattr(self, "overlay") and self.main_loop:
            self.main_loop.widget = self.overlay.bottom_w

    def save_interface_config(self, button: urwid.Button, interface_name: str) -> None:
        """Save the new configuration."""
        ip = self.edit_ip.edit_text
        mask = self.edit_mask.edit_text
        gw = self.edit_gw.edit_text

        ip6 = self.edit_ip6.edit_text
        mask6 = self.edit_mask6.edit_text
        gw6 = self.edit_gw6.edit_text

        logging.info(
            f"Saving config for {interface_name}: IPv4={ip}/{mask}, IPv6={ip6}/{mask6}"
        )

        try:
        # Construct IPAddress objects
            from netcfg_tui_full import IPAddress, AddressFamily

            new_addresses = []

            # IPv4
            if ip:
                try:
                    netmask = int(mask)
                except ValueError:
                    raise ValueError("IPv4 Netmask must be an integer (CIDR)")

                ipv4_addr = IPAddress(
                    address=ip,
                    netmask=netmask,
                    family=AddressFamily.IPV4,
                    gateway=gw if gw else None,
                    is_primary=True,
                )
                if not ipv4_addr.is_valid():
                    raise ValueError("Invalid IPv4 configuration")
                new_addresses.append(ipv4_addr)

            # IPv6
            if ip6:
                try:
                    netmask6 = int(mask6)
                except ValueError:
                    raise ValueError("IPv6 Prefix must be an integer (CIDR)")

                ipv6_addr = IPAddress(
                    address=ip6,
                    netmask=netmask6,
                    family=AddressFamily.IPV6,
                    gateway=gw6 if gw6 else None,
                    is_primary=False,
                )
                if not ipv6_addr.is_valid():
                    raise ValueError("Invalid IPv6 configuration")
                new_addresses.append(ipv6_addr)

            if not new_addresses:
                raise ValueError("At least one IP address (IPv4 or IPv6) is required")

            # Apply via backend
            iface_config = self.manager.backend.get_interface_config(interface_name)
            if not iface_config:
                raise ValueError(f"Interface {interface_name} not found")

            # Update addresses directly (since backend is in-memory for now)
            iface_config.addresses = new_addresses

            self.status_bar.set_text(f"Saved configuration for {interface_name}")

            # Refresh the list
            if self.main_loop:
                self.main_loop.widget.body = urwid.AttrMap(
                    self.create_interface_list(), "body"
                )

        except Exception as e:
            self.status_bar.set_text(f"Error saving: {e}")
            logging.error(f"Save error: {e}")

        self.close_dialog(button)

    def run(self) -> None:
        """Run the application."""
        header = urwid.AttrMap(urwid.Text("DebVisor Network Configuration"), "header")
        footer = urwid.AttrMap(self.status_bar, "status")

        list_box = self.create_interface_list()
        view = urwid.Frame(
            urwid.AttrMap(list_box, "body"), header=header, footer=footer
        )

        self.main_loop = urwid.MainLoop(
            view, self.palette, unhandled_input=self.handle_input
        )
        try:
            self.main_loop.run()
        except Exception as e:
            print(f"Error running TUI: {e}")

    def handle_input(self, key: str) -> None:
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()
        elif key in ("r", "R"):
        # Refresh list
            if self.main_loop:
                self.main_loop.widget.body = urwid.AttrMap(
                    self.create_interface_list(), "body"
                )
            self.status_bar.set_text("Refreshed")


if __name__ == "__main__":
    NetCfgApp().run()
