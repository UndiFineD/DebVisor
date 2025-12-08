# DebVisor Security Overview

This document summarizes the baseline security posture for the DebVisor ISO,
installer, and installed system. It is intentionally concise; see the
referenced docs for deeper architecture.

## ISO Integrity

- Every released ISO SHOULD be accompanied by a SHA256 checksum file.
- Optionally, ISOs MAY be signed with a GPG key dedicated to DebVisor

  releases.

- The build script supports this via:
- `DEBVISOR_SIGN_ISO=1` to enable checksum + signature generation.
- `DEBVISOR_GPG_KEY=` to select a specific GPG key (optional).

Example (after importing the DebVisor release key):

    sha256sum -c debvisor--.hybrid.iso.sha256
    gpg --verify debvisor--.hybrid.iso.asc

## ISO and Live Environment

- The live environment aims to ship only the packages required to install and

  operate DebVisor as a headless hypervisor.

- Network-facing services in the live system SHOULD be minimized. SSH or other

  daemons SHOULD only be enabled when explicitly required for installation or
  remote automation.

- Default firewall policy SHOULD deny inbound traffic unless explicitly

  documented as required for the installer.

## Installation and First Boot

- The first-boot script (`debvisor-firstboot.sh`) is intended to be

  non-destructive when run in `--dry-run` mode, and its behavior is covered by
  `build/test-firstboot.sh`.

- The installed system MUST NOT ship with default or well-known passwords.

  Installers SHOULD either:

- Require a strong password at install time, or
- Prefer SSH key-based administration with no password login.
- The installed host SHOULD disable or remove services that are not required

  for a headless hypervisor (e.g., GUI components, desktop daemons, printers).

## Updates and Maintenance

- Security updates SHOULD be applied regularly. Operators are encouraged to

  enable unattended upgrades for security repositories where operationally
  compatible.

- Logs from first boot and key management actions SHOULD be written to a

  dedicated location (e.g., `/var/log/debvisor/`) to ease auditing.

## Operational Guidance

- Expose DebVisor management interfaces only over trusted channels

  (VPN, bastion hosts, or private networks).

- Avoid exposing management SSH or web consoles directly to the public

  internet without additional controls (firewalls, MFA, IP restrictions).

- Periodically review the package set and configuration against current

  hardening guidance for Debian and virtualization hosts.

Example threat scenarios, trust boundaries, and supply-chain
assumptions are summarized in `threat-model.md`; site operators may
have stricter policies that take precedence over these defaults.

## Blocklists and Whitelists

DebVisor ships**example**blocklist and whitelist files under
`/etc/debvisor/`:

- `blocklist-example.txt`
- `blocklist-whitelist-example.txt`

These are templates only; they are not active unless wired into the
`blocklist`Ansible role via inventory or`group_vars` (see
`operations.md`). Operators should copy and adapt these files, then
reference the real paths from Ansible configuration.

Using the example files as-is without connecting them to Ansible has
no effect on the running firewall.

This document is a starting point. Site operators may have stricter policies
that take precedence over these defaults.
