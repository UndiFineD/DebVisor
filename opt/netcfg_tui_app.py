#!/usr/bin/env python3
"""
DebVisor Network Configuration TUI Application.
Uses urwid for the interface and netcfg_tui_full for backend logic.
"""

import urwid
import logging
import sys
import os

# Ensure opt is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from netcfg_tui_full import (
    NetworkConfigurationManager, 
    Iproute2Backend, 
    InterfaceType,
    InterfaceStatus,
    ConnectionState
)

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
            label = f"{iface.name:<10} | {iface.interface_type.value:<10} | {iface.state.value}"
            button = urwid.Button(label)
            urwid.connect_signal(button, 'click', self.on_interface_click, iface.name)
            body.append(urwid.AttrMap(button, 'button', 'button_focus'))
            
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def on_interface_click(self, button, interface_name):
        """Handle interface selection."""
        self.status_bar.set_text(f"Selected: {interface_name}")
        # In a full implementation, this would open an edit dialog
        # For now, we just log it
        logging.info(f"Clicked interface: {interface_name}")

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
