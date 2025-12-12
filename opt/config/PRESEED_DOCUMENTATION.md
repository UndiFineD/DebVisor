# Preseed Configuration & Build Customization

## Preseed File Overview
The `preseed.cfg` automates Debian installer decisions during first-boot:
### Key Configuration Areas
### Localization
    d-i debian-installer/language string en
    d-i debian-installer/country string US
    d-i debian-installer/locale string en_US.UTF-8
### Networking
- DHCP: `d-i netcfg/choose_interface select auto`

- Static: Configure IP, netmask, gateway, nameservers
### Storage
- Method: LVM recommended for flexibility

- Partitioning: `/boot`(1GB),`/`(50GB),`/var` (50GB), remainder for data
### Root/User
    d-i passwd/root-password password PASSWORD
    d-i passwd/user-fullname string Admin
    d-i passwd/username string admin
### Packages
    tasksel tasksel/first multiselect standard
    d-i pkgsel/include string openssh-server ceph kubernetes curl
## Variable Substitution
Support environment-specific customization:
    DEBVISOR_HOSTNAME=node-1 \
    DEBVISOR_IP=192.168.1.100 \
    ./opt/build/build-debvisor.sh
Preseed template:
    d-i netcfg/get_hostname string {{HOSTNAME}}
    d-i netcfg/get_ipaddress string {{IP}}
## Package Lists
- *base.list**- Core system packages

- *storage.list**- Ceph and ZFS

- *network.list**- Networking (Calico, etc)

- *optional.list**- Optional components
## Build Hooks
- *00-preseed**- Validate preseed syntax

- *10-packages**- Validate package availability

- *20-chroot**- Apply filesystem customizations
## Security Hardening
- Store passwords securely (use variables, not plaintext)

- Configure SSH hardening via hooks

- Enable firewall (ufw) automatically

- Configure automatic security updates

- Use strong passwords or disable root login
## Validation
## Check preseed syntax
    python3 opt/config/validate-packages.py --list opt/config/package-lists/base.list
## Verify build
    ./opt/build/build-debvisor.sh
## Architecture Support
## Build for ARM64
    LIVE_BUILD_ARCH=arm64 ./opt/build/build-debvisor.sh
## Build for AMD64 (default)
    LIVE_BUILD_ARCH=amd64 ./opt/build/build-debvisor.sh
## Post-Installation
Preseed can execute commands after install:
    d-i preseed/late_command string \
      in-target apt-get update; \
      in-target apt-get install -y additional-packages; \
      in-target systemctl enable ceph-health.timer
