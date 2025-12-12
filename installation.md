# DebVisor Installation Guide

## System Requirements

- **CPU**: 64-bit (x86_64) processor, 2+ cores recommended.
- **RAM**: 4GB minimum, 8GB+ recommended.
- **Storage**: 20GB minimum for OS, additional for data.
- **Network**: Ethernet interface.

## Installation Methods

### Method 1: ISO Installation (Recommended)

1. Download the `debvisor-installer.iso`.
1. Flash it to a USB drive (using Etcher, Rufus, or `dd`).
1. Boot the target machine from the USB drive.
1. Follow the on-screen prompts to install DebVisor to your hard drive.
1. The system will reboot into the DebVisor Console Menu.

### Method 2: Install on Existing Debian 12 (Bookworm)

If you already have a minimal Debian 12 installation:

1. **Clone the Repository**:

   ```bash

   git clone <https://github.com/your-org/debvisor.git> /opt/debvisor
   cd /opt/debvisor
```text

1. **Install Dependencies**:

   ```bash

   apt update
   apt install -y python3-venv python3-pip build-essential libssl-dev libffi-dev
```text

1. **Run the Installer Script**:

   ```bash

   ./install.sh
```text

- (Note: You may need to create this script based on the manual steps below)*

1. **Manual Setup (if no script)**:

   ```bash

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

   # Install Systemd Services
   cp etc/systemd/system/*.service /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable --now debvisor-rpcd debvisor-panel
```text

## Post-Installation

1. **Access the Web Panel**:

   Open a browser and navigate to `<<<<<<<<<<<<<<<<<<<<<<<<<<https://<server-ip>:8443>`.>>>>>>>>>>>>>>>>>>>>>>>>>   Default credentials (if configured) or follow the initial setup wizard.

1. **Console Access**:

   Log in to the physical console or SSH. You will be greeted by the DebVisor Console Menu (`debvisor-menu`).

1. **Network Configuration**:

   Use the "Network Configuration" option in the console menu to set up static IPs, bonds, or bridges.

## Troubleshooting

- **Logs**: Check logs in `/var/log/debvisor/` or use `journalctl -u debvisor-rpcd`.
- **Service Status**: `systemctl status debvisor-rpcd`.
