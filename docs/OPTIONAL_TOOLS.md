# Optional Tools for DebVisor

DebVisor is built on Debian, but many other Linux distributions offer excellent tools that can enhance the administrator experience. Below is a list of recommended optional tools to install.

## System Monitoring & Diagnostics

- **htop**: Interactive process viewer (better top).
- **iotop**: Simple top-like I/O monitor.
- **iftop**: Display bandwidth usage on an interface by host.
- **nmon**: Tuner and performance monitor.
- **glances**: Cross-platform system monitoring tool.
- **btop**: Resource monitor that shows usage and stats for processor, memory, disks, network and processes.

## Storage Management

- **ncdu**: NCurses Disk Usage - great for finding what's eating disk space.
- **parted**: Disk partitioning and partition resizing.
- **smartmontools**: Control and monitor storage systems using the Self-Monitoring, Analysis and Reporting Technology System (SMART).

## Network Utilities

- **tcpdump**: Command-line packet analyzer.
- **nmap**: Network exploration tool and security / port scanner.
- **mtr**: Network diagnostic tool that combines the functionality of traceroute and ping.
- **iperf3**: Tool for active measurements of the maximum achievable bandwidth on IP networks.
- **ethtool**: Query or control network driver and hardware settings.

## Terminal Multiplexers & Shell Enhancements

- **tmux**: Terminal multiplexer.
- **screen**: Full-screen window manager that multiplexes a physical terminal.
- **bash-completion**: Programmable completion for the bash shell.
- **zsh** + **oh-my-zsh**: A powerful shell with many plugins.

## File Management & Editing

- **mc (Midnight Commander)**: Visual file manager.
- **vim** / **neovim**: Highly configurable text editor.
- **nano**: Easy-to-use text editor (usually installed by default).
- **jq**: Command-line JSON processor.
- **yq**: Command-line YAML processor.

## Virtualization & Containers

- **virt-top**: 'top'-like utility for virtualization stats.
- **guestfs-tools**: Tools to access and modify virtual machine disk images.

## Development & Maintenance Tools

- **scripts/fix_markdown_lint_comprehensive.py**: A custom Python script included in this repository to automatically fix common Markdown linting errors (MD022, MD031, MD032, etc.).
- Usage: `python scripts/fix_markdown_lint_comprehensive.py`
- **gh (GitHub CLI)**: Essential for managing workflows, issues, and pull requests from the command line.
- **act**: Run GitHub Actions locally (useful for testing workflows before pushing).

## Installation

You can install these tools using `apt`:
```bash

apt update
apt install htop iotop iftop ncdu tmux tcpdump nmap mtr-tiny iperf3 jq
```python
