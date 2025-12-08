#!/usr/bin/env python3
"""
DebVisor Network Configuration TUI Application.
Uses urwid for the interface and netcfg_tui_full for backend logic.
"""

from netcfg_tui_full import (
    NetworkConfigurationManager,
    Iproute2Backend
)
import urwid
import logging
import sys
import os

# Ensure opt is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Setup logging
logging.basicConfig(filename='netcfg_tui.log', level=logging.DEBUG)


class NetCfgApp:
    def __init__(self):
        # Initialize backend
        self.backend = Iproute2Backend()
        self.manager = NetworkConfigurationManager(backend=self.backend)

        self.palette = [
            ('body', 'black', 'light gray'),
            ('header', 'white', 'dark blue', 'bold'),
            ('button', 'black', 'dark cyan'),
            ('button_focus', 'white', 'dark blue', 'bold'),
            ('status', 'white', 'dark blue'),
            ('status_ok', 'light green', 'dark blue', 'bold'),
            ('status_err', 'light red', 'dark blue', 'bold'),
            ('title', 'white', 'dark blue', 'bold'),
        ]

        self.main_loop = None
        self.status_bar = urwid.Text("Ready - Press 'q' to quit")

    def create_interface_list(self):
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
            state_color = 'status_ok' if iface.state.value == "up" else 'status_err'
            
            label = f"{state_symbol} {iface.name:<10} | {iface.interface_type.value:<10} | {iface.state.value}"
            button = urwid.Button(label)
            urwid.connect_signal(button, 'click', self.on_interface_click, iface.name)
            body.append(urwid.AttrMap(button, 'button', 'button_focus'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def on_interface_click(self, button, interface_name):
        """Handle interface selection."""
        self.status_bar.set_text(f"Selected: {interface_name}")
        self.show_edit_dialog(interface_name)

    def show_edit_dialog(self, interface_name):
        """Show dialog to edit interface settings."""
        # Fetch current config
        try:
            iface = self.manager.get_interface_config(interface_name)
            current_ip = ""
            current_mask = "24"
            current_gw = ""
            
            if iface and iface.addresses:
                addr = iface.addresses[0]
                current_ip = addr.address
                current_mask = str(addr.netmask)
                current_gw = addr.gateway or ""
        except Exception as e:
            logging.error(f"Error fetching config for {interface_name}: {e}")
            current_ip = ""
            current_mask = "24"
            current_gw = ""

        # Create edit widgets
        self.edit_ip = urwid.Edit("IP Address: ", current_ip)
        self.edit_mask = urwid.Edit("Netmask (CIDR): ", current_mask)
        self.edit_gw = urwid.Edit("Gateway: ", current_gw)
        
        # Buttons
        btn_save = urwid.Button("Save")
        urwid.connect_signal(btn_save, 'click', self.save_interface_config, interface_name)
        
        btn_cancel = urwid.Button("Cancel")
        urwid.connect_signal(btn_cancel, 'click', self.close_dialog)

        # Layout
        pile = urwid.Pile([
            urwid.Text(f"Edit Interface: {interface_name}", align='center'),
            urwid.Divider(),
            self.edit_ip,
            self.edit_mask,
            self.edit_gw,
            urwid.Divider(),
            urwid.Columns([
                urwid.AttrMap(btn_save, 'button', 'button_focus'),
                urwid.AttrMap(btn_cancel, 'button', 'button_focus')
            ])
        ])

        self.overlay = urwid.Overlay(
            urwid.LineBox(pile),
            self.main_loop.widget,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50)
        )
        self.main_loop.widget = self.overlay

    def close_dialog(self, button):
        """Close the overlay dialog."""
        if hasattr(self, 'overlay'):
            self.main_loop.widget = self.overlay.bottom_w

    def save_interface_config(self, button, interface_name):
        """Save the new configuration."""
        ip = self.edit_ip.edit_text
        mask = self.edit_mask.edit_text
        gw = self.edit_gw.edit_text
        
        logging.info(f"Saving config for {interface_name}: IP={ip}/{mask} GW={gw}")
        
        try:
            # Construct IPAddress object
            from netcfg_tui_full import IPAddress, AddressFamily
            
            # Basic validation
            if not ip:
                raise ValueError("IP Address is required")
            
            try:
                netmask = int(mask)
            except ValueError:
                raise ValueError("Netmask must be an integer (CIDR)")

            new_addr = IPAddress(
                address=ip,
                netmask=netmask,
                family=AddressFamily.IPV4, # Default to IPv4 for now
                gateway=gw if gw else None,
                is_primary=True
            )

            if not new_addr.is_valid():
                raise ValueError("Invalid IP configuration")

            # Apply via backend
            # Note: In a real implementation, we would clear existing IPs first or handle multiple IPs
            # For this TUI, we assume replacing the primary IP
            
            # 1. Get current config to ensure interface exists
            iface_config = self.manager.backend.get_interface_config(interface_name)
            if not iface_config:
                raise ValueError(f"Interface {interface_name} not found")

            # 2. Remove existing primary IP if any (simplification)
            # In a full implementation, we'd be more careful
            if iface_config.addresses:
                # Clear existing addresses for this simple editor
                iface_config.addresses = []

            # 3. Add new address
            success = self.manager.backend.set_ip_address(interface_name, new_addr)
            
            if success:
                self.status_bar.set_text(f"Saved configuration for {interface_name}")
                # Refresh the list to show updated status if we had status indicators based on IP
                self.main_loop.widget.body = urwid.AttrMap(self.create_interface_list(), 'body')
            else:
                self.status_bar.set_text(f"Failed to apply configuration for {interface_name}")

        except Exception as e:
            self.status_bar.set_text(f"Error saving: {e}")
            logging.error(f"Save error: {e}")
            
        self.close_dialog(button)


    def run(self):
        """Run the application."""
        header = urwid.AttrMap(urwid.Text("DebVisor Network Configuration"), 'header')
        footer = urwid.AttrMap(self.status_bar, 'status')

        list_box = self.create_interface_list()
        view = urwid.Frame(urwid.AttrMap(list_box, 'body'), header=header, footer=footer)

        self.main_loop = urwid.MainLoop(view, self.palette, unhandled_input=self.handle_input)
        try:
            self.main_loop.run()
        except Exception as e:
            print(f"Error running TUI: {e}")

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key in ('r', 'R'):
            # Refresh list
            self.main_loop.widget.body = urwid.AttrMap(self.create_interface_list(), 'body')
            self.status_bar.set_text("Refreshed")


if __name__ == '__main__':
    NetCfgApp().run()
