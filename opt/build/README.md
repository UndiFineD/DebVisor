# DebVisor build tooling

This directory contains scripts and helpers for building DebVisor images.

## `build-debvisor.sh`

`build-debvisor.sh` is the main entrypoint for producing a DebVisor
ISO using Debian live-build. It is the canonical way to turn the
content of `config/` into a bootable installer image.

At a high level it:

- Verifies that required host tools are present (`lb`,`debootstrap`,

  `xorriso`; optionally warns if`shellcheck` or a modern Debian host
  are missing).

- Runs Debian live-build with the DebVisor configuration in `config/`.
- Produces an installable ISO artifact in the project root

  (for example `debvisor--.hybrid.iso`).

Key environment variables (see the script header for the
authoritative list):

- `DEBVISOR_DIST`: Debian release to target (for example`trixie`).
- `DEBVISOR_ARCH`: Architecture to build (for example`amd64`).
- `DEBVISOR_FAST`: Control whether`lb clean`/`lb config` are

  skipped to speed up rebuilds.

- `DEBVISOR_VERSION`: Optional version tag embedded in the ISO

  filename.

- `DEBVISOR_DRYRUN`: When set to`1`, validates and configures

  live-build but skips the actual `lb build` step.

Changes under `config/`or`build/` that affect packages,
preseeding, or filesystem layout require a new ISO to be built via
this script; runtime configuration changes should instead flow
through first-boot scripts and Ansible playbooks.

## `sync-addons-playbook.sh`

`sync-addons-playbook.sh` is a small helper that keeps the
bootstrap-addons Ansible playbook under `config/includes.chroot/`
in sync with the source addons definitions in `docker\addons\` and the
corresponding roles. This script is invoked automatically by
`build-debvisor.sh` (when present and executable) so that changes to
addons are picked up on the next ISO build without manual steps.

If you edit `docker\addons\` or their Ansible roles and want to verify the
result without running a full build, you can execute this helper
directly and inspect the synced playbook in `config/includes.chroot/`.

## `test-firstboot.sh`

`test-firstboot.sh` runs a smoke test of the first-boot script and
related units. It is designed to be called from CI or manually after
changes to `debvisor-firstboot.sh` and its helpers.

Typical uses:

- Run `shellcheck` over first-boot scripting.
- Exercise the `--dry-run`path of`debvisor-firstboot.sh` to catch
- Run `shellcheck` over first-boot scripting.
- Exercise the `--dry-run`path of`debvisor-firstboot.sh` to catch

  obvious regressions before booting a real node.

In most setups this script is wired into GitHub Actions so that
changes to `build/`or`config/includes.chroot/` trigger a quick
first-boot validation.

## Build hooks and includes

DebVisor uses Debian live-build hooks and staged includes to prepare the image.

- Hooks under `config/hooks/normal/` run inside the chroot during build:
- `ZZ-debvisor-perms.chroot`ensures helper scripts are executable (`0755`).
- `99-debvisor-firstboot-enable.chroot`installs and enables`debvisor-firstboot.service`.

- Includes under `config/includes.chroot/` are copied into the target filesystem:
- `/usr/local/sbin/debvisor-firstboot.sh` – main first-boot provisioning script.
- `/usr/local/sbin/debvisor-profile-summary.sh`– writes`/var/log/debvisor/profile-summary.{txt,json}`.
- `/opt/debvisor/systemd/debvisor-firstboot.service` – staged unit installed by the enable hook.

On first boot, `debvisor-firstboot.sh` runs once (via the systemd unit), performs
initial provisioning according to `/etc/debvisor-profile`, and writes the profile
summary for automation.
