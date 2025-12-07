#!/usr/bin/env python3
"""
DebVisor Console Menu (debvisor-menu)
A TUI for managing the DebVisor system from the physical console or SSH.
"""

import urwid
import os
import subprocess
import socket
import psutil
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

PALETTE = [
    ('body', 'white', 'black'),
    ('header', 'black', 'light cyan'),
    ('footer', 'white', 'dark blue'),
    ('button', 'black', 'light gray'),
    ('button_focus', 'white', 'dark red'),
    ('text', 'white', 'black'),
    ('title', 'white,bold', 'black'),
]

# ============================================================================
# Helper Functions
# ============================================================================


def get_ip_addresses():
    """Get list of IP addresses."""
    ips = []
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET:
                if interface != 'lo':
                    ips.append(f"{interface}: {snic.address}")
    return ", ".join(ips) if ips else "No IP detected"


def get_system_status():
    """Get basic system status."""
    load = os.getloadavg()
    mem = psutil.virtual_memory()
    uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Load: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f} | Mem: {mem.percent}% | {uptime}"

# ============================================================================
# Menu Actions
# ============================================================================


def run_command(command):
    """Run a shell command and wait."""
    # Suspend urwid, run command, resume
    raise urwid.ExitMainLoop()


def action_network_config(button):
    """Launch netcfg-tui."""
    # We need to exit the loop, run the command, then restart the script?
    # Or just use os.system inside a suspended screen.
    # Urwid is tricky with external commands.
    # The simplest way in this architecture is to exit with a specific code
    # and have a wrapper script relaunch, OR use the proper suspend method.
    pass  # Handled by main loop logic


class MenuApp:
    def __init__(self):
        self.main_loop = None

    def create_menu(self):
        header_text = urwid.Text(u" DebVisor Enterprise Console ", align='center')
        header = urwid.AttrMap(header_text, 'header')

        self.status_text = urwid.Text(get_system_status(), align='center')
        self.ip_text = urwid.Text(
            f"Management URL: https://{socket.gethostname()}:8443\nIPs: {get_ip_addresses()}",
            align='center')

        body_content = [
            urwid.Divider(),
            self.status_text,
            urwid.Divider(),
            self.ip_text,
            urwid.Divider(),
            self.create_button("Network Configuration", self.on_network_config),
            self.create_button("System Shell", self.on_shell),
            self.create_button("View System Logs", self.on_logs),
            self.create_button("Reboot System", self.on_reboot),
            self.create_button("Shutdown System", self.on_shutdown),
            urwid.Divider(),
            self.create_button("Exit Menu", self.on_exit),
        ]

        listbox = urwid.ListBox(urwid.SimpleListWalker(body_content))
        view = urwid.Frame(urwid.AttrMap(listbox, 'body'), header=header)
        return view

    def create_button(self, label, callback):
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, 'button', focus_map='button_focus')

    def on_network_config(self, button):
        self.run_external("python3 -m opt.netcfg_tui.main")

    def on_shell(self, button):
        self.run_external("/bin/bash")

    def on_logs(self, button):
        self.run_external("journalctl -f")

    def on_reboot(self, button):
        # Confirmation dialog could be added here
        self.run_external("reboot")

    def on_shutdown(self, button):
        self.run_external("poweroff")

    def on_exit(self, button):
        raise urwid.ExitMainLoop()

    def run_external(self, command):
        # Stop the loop, run command, restore loop
        self.main_loop.stop()
        subprocess.run(['/usr/bin/clear'])
        try:
            # Use shlex to split command safely and avoid shell=True
            import shlex
            args = shlex.split(command)
            subprocess.call(args, shell=False)
        except Exception as e:
            print(f"Error executing command: {e}")
            input("Press Enter to continue...")
        self.main_loop.start()

    def update_status(self, loop, user_data):
        self.status_text.set_text(get_system_status())
        self.ip_text.set_text(
            f"Management URL: https://{socket.gethostname()}:8443\nIPs: {get_ip_addresses()}")
        loop.set_alarm_in(2, self.update_status)

    def run(self):
        self.main_loop = urwid.MainLoop(self.create_menu(), PALETTE)
        self.main_loop.set_alarm_in(2, self.update_status)
        self.main_loop.run()


if __name__ == '__main__':
    # Ensure we are root for some commands
    if os.geteuid() != 0:
        print("Warning: Not running as root. Some functions may fail.")

    try:
        app = MenuApp()
        app.run()
    except KeyboardInterrupt:
        pass
