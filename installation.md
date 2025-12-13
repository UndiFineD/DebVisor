# DebVisor Installation Guide\n\n## System Requirements\n\n- **CPU**: 64-bit (x86_64)

processor, 2+

cores recommended.\n\n- **RAM**: 4GB minimum, 8GB+ recommended.\n\n-
**Storage**: 20GB
minimum for
OS, additional for data.\n\n- **Network**: Ethernet interface.\n\n##
Installation
Methods\n\n###
Method 1: ISO Installation (Recommended)\n\n1. Download the
`debvisor-installer.iso`.\n\n1. Flash it
to a USB drive (using Etcher, Rufus, or `dd`).\n\n1. Boot the target machine
from the USB
drive.\n\n1. Follow the on-screen prompts to install DebVisor to your hard
drive.\n\n1.
The system
will reboot into the DebVisor Console Menu.\n\n### Method 2: Install on Existing
Debian 12
(Bookworm)\n\nIf you already have a minimal Debian 12 installation:\n\n1.
**Clone the
Repository**:\n\n ```bash\n git clone
]([https://github.com/your-org/debvisor.git]([https://github.com/your-org/debvisor.gi]([https://github.com/your-org/debvisor.g]([https://github.com/your-org/debvisor.]([https://github.com/your-org/debvisor]([https://github.com/your-org/debviso]([https://github.com/your-org/debvis]([https://github.com/your-org/debvi]([https://github.com/your-org/debv]([https://github.com/your-org/deb]([https://github.com/your-org/de]([https://github.com/your-org/d]([https://github.com/your-org/]([https://github.com/your-org]([https://github.com/your-or]([https://github.com/your-o]([https://github.com/your-]([https://github.com/your]([https://github.com/you]([https://github.com/yo]([https://github.com/y]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)y)o)u)r)-)o)r)g)/)d)e)b)v)i)s)o)r).)g)i)t)>)
/opt/debvisor\n cd /opt/debvisor\n```text\n\n cd /opt/debvisor\n```text\n git
clone
[https://github.com/your-org/debvisor.git]([https://github.com/your-org/debvisor.gi]([https://github.com/your-org/debvisor.g]([https://github.com/your-org/debvisor.]([https://github.com/your-org/debvisor]([https://github.com/your-org/debviso]([https://github.com/your-org/debvis]([https://github.com/your-org/debvi]([https://github.com/your-org/debv]([https://github.com/your-org/deb]([https://github.com/your-org/de]([https://github.com/your-org/d]([https://github.com/your-org/]([https://github.com/your-org]([https://github.com/your-or]([https://github.com/your-o]([https://github.com/your-]([https://github.com/your]([https://github.com/you]([https://github.com/yo]([https://github.com/y]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)y)o)u)r)-)o)r)g)/)d)e)b)v)i)s)o)r).)g)i)t)
/opt/debvisor\n cd /opt/debvisor\n```text\n\n cd /opt/debvisor\n```text\n git
clone
[https://github.com/your-org/debvisor.git]([https://github.com/your-org/debvisor.gi]([https://github.com/your-org/debvisor.g]([https://github.com/your-org/debvisor.]([https://github.com/your-org/debvisor]([https://github.com/your-org/debviso]([https://github.com/your-org/debvis]([https://github.com/your-org/debvi]([https://github.com/your-org/debv]([https://github.com/your-org/deb]([https://github.com/your-org/de]([https://github.com/your-org/d]([https://github.com/your-org/]([https://github.com/your-org]([https://github.com/your-or]([https://github.com/your-o]([https://github.com/your-]([https://github.com/your]([https://github.com/you]([https://github.com/yo]([https://github.com/y]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)y)o)u)r)-)o)r)g)/)d)e)b)v)i)s)o)r).)g)i)t)
/opt/debvisor\n cd /opt/debvisor\n```text\n\n cd /opt/debvisor\n```text\n cd
/opt/debvisor\n```text\n```text\n\n1. **Install Dependencies**:\n\n

```bash\n\n1.
**Install
Dependencies**:\n\n ```bash\n\n1. **Install Dependencies**:\n\n ```bash\n\n1.
**Install
Dependencies**:\n\n ```bash\n\n1. **Install Dependencies**:\n\n ```bash\n\n1.
**Install
Dependencies**:\n\n ```bash\n\n1. **Install Dependencies**:\n\n ```bash\n\n1.
**Install
Dependencies**:\n\n ```bash\n apt update\n apt install -y python3-venv
python3-pip
build-essential
libssl-dev libffi-dev\n```text\n\n apt install -y python3-venv python3-pip
build-essential
libssl-dev libffi-dev\n```text\n apt update\n apt install -y python3-venv
python3-pip
build-essential libssl-dev libffi-dev\n```text\n\n apt install -y python3-venv
python3-pip
build-essential libssl-dev libffi-dev\n```text\n apt update\n apt install -y
python3-venv
python3-pip build-essential libssl-dev libffi-dev\n```text\n\n apt install -y
python3-venv
python3-pip build-essential libssl-dev libffi-dev\n```text\n apt install -y
python3-venv
python3-pip
build-essential libssl-dev libffi-dev\n```text\n```text\n\n1. **Run the
Installer
Script**:\n\n

```bash\n\n1. **Run the Installer Script**:\n\n ```bash\n\n1. **Run the Installer Script**:\n\n

```bash\n\n1. **Run the Installer Script**:\n\n ```bash\n\n1. **Run the Installer Script**:\n\n

```bash\n\n1. **Run the Installer Script**:\n\n ```bash\n\n1. **Run the Installer Script**:\n\n

```bash\n\n1. **Run the Installer Script**:\n\n ```bash\n ./install.sh\n```text\n```text\n

./install.sh\n```text\n```text\n
./install.sh\n```text\n```text\n```text\n```text\n\n-
(Note: You
may need to create this script based on the manual steps below)*\n\n1. **Manual
Setup (if
no
script)**:\n\n ```bash\n\n- (Note: You may need to create this script based on
the manual
steps
below)*\n\n1. **Manual Setup (if no script)**:\n\n ```bash\n\n- (Note: You may
need to
create this
script based on the manual steps below)*\n\n1. **Manual Setup (if no
script)**:\n\n

```bash\n\n-

(Note: You may need to create this script based on the manual steps
below)*\n\n1. **Manual
Setup (if
no script)**:\n\n ```bash\n\n- (Note: You may need to create this script based
on the
manual steps
below)*\n\n1. **Manual Setup (if no script)**:\n\n ```bash\n\n- (Note: You may
need to
create this
script based on the manual steps below)*\n\n1. **Manual Setup (if no
script)**:\n\n

```bash\n\n-

(Note: You may need to create this script based on the manual steps
below)*\n\n1. **Manual
Setup (if
no script)**:\n\n ```bash\n\n- (Note: You may need to create this script based
on the
manual steps
below)*\n\n1. **Manual Setup (if no script)**:\n\n ```bash\n python3 -m venv
.venv\n
source
.venv/bin/activate\n pip install -r requirements.txt\n # Install Systemd
Services\n cp
etc/systemd/system/*.service /etc/systemd/system/\n systemctl daemon-reload\n
systemctl
enable --now
debvisor-rpcd debvisor-panel\n```text\n\n source .venv/bin/activate\n pip
install -r
requirements.txt\n # Install Systemd Services\n cp etc/systemd/system/*.service
/etc/systemd/system/\n systemctl daemon-reload\n systemctl enable --now
debvisor-rpcd
debvisor-panel\n```text\n python3 -m venv .venv\n source .venv/bin/activate\n
pip install
-r
requirements.txt\n # Install Systemd Services\n cp etc/systemd/system/*.service
/etc/systemd/system/\n systemctl daemon-reload\n systemctl enable --now
debvisor-rpcd
debvisor-panel\n```text\n\n source .venv/bin/activate\n pip install -r
requirements.txt\n

## Install

Systemd Services\n cp etc/systemd/system/*.service /etc/systemd/system/\n
systemctl
daemon-reload\n
systemctl enable --now debvisor-rpcd debvisor-panel\n```text\n python3 -m venv
.venv\n
source
.venv/bin/activate\n pip install -r requirements.txt\n # Install Systemd
Services\n cp
etc/systemd/system/*.service /etc/systemd/system/\n systemctl daemon-reload\n
systemctl
enable --now
debvisor-rpcd debvisor-panel\n```text\n\n source .venv/bin/activate\n pip
install -r
requirements.txt\n # Install Systemd Services\n cp etc/systemd/system/*.service
/etc/systemd/system/\n systemctl daemon-reload\n systemctl enable --now
debvisor-rpcd
debvisor-panel\n```text\n source .venv/bin/activate\n pip install -r
requirements.txt\n #
Install
Systemd Services\n cp etc/systemd/system/*.service /etc/systemd/system/\n
systemctl
daemon-reload\n
systemctl enable --now debvisor-rpcd debvisor-panel\n```text\n pip install -r
requirements.txt\n #
Install Systemd Services\n cp etc/systemd/system/*.service
/etc/systemd/system/\n
systemctl
daemon-reload\n systemctl enable --now debvisor-rpcd debvisor-panel\n```text\n##
Post-Installation\n1. **Access the Web Panel**:\n Open a browser and navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting\n-
**Logs**:
Check logs in
`/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl status
debvisor-rpcd`.\n## Post-Installation (2)\n1. **Access the Web Panel**:\n Open a
browser
and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (2)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n## Post-Installation (3)\n1. **Access the Web Panel**:\n
Open a
browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (3)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n## Post-Installation (4)\n1. **Access the Web Panel**:\n
Open a
browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (4)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n\n1. **Access the Web Panel**:\n Open a browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (5)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n## Post-Installation (5)\n1. **Access the Web Panel**:\n
Open a
browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (6)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n## Post-Installation (6)\n1. **Access the Web Panel**:\n
Open a
browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (7)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n## Post-Installation (7)\n1. **Access the Web Panel**:\n
Open a
browser and
navigate to
`[https://`.>>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>>]([https://`.>>>>>>>>>>>>]([https://`.>>>>>>>>>>>]([https://`.>>>>>>>>>>]([https://`.>>>>>>>>>]([https://`.>>>>>>>>]([https://`.>>>>>>>]([https://`.>>>>>>]([https://`.>>>>>]([https://`.>>>>]([https://`.>>>]([https://`.>>]([https://`.>]([https://`.]([https://`](https://`).)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)>)
Default credentials (if configured) or follow the initial setup wizard.\n\n1.
**Console
Access**:\n
Log in to the physical console or SSH. You will be greeted by the DebVisor
Console Menu
(`debvisor-menu`).\n\n1. **Network Configuration**:\n Use the "Network
Configuration"
option in the
console menu to set up static IPs, bonds, or bridges.\n## Troubleshooting (8)\n-
**Logs**:
Check
logs in `/var/log/debvisor/`or use`journalctl -u debvisor-rpcd`.\n\n- **Service
Status**:
`systemctl
status debvisor-rpcd`.\n\n
