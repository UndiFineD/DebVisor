# Networking Design

## Objectives
- Support single-node and multi-node clusters.

- Provide consistent VM networking (bridged + overlay).

- Automate address assignment while allowing reservations.

- Offer internal DNS/DHCP plus forward external queries.
## Network Configuration Tool
For interactive configuration of wired, wireless, InfiniBand, VLANs, bridging, and bonding, see the [Network Config TUI](network-config-tui.md). The TUI generates systemd-networkd or Netplan files with a single-bridge default (`br0`), STP enabled, and optional bonding support.
## Layers
1. Physical NICs (ens*, enp*): discovered at first boot.

1. Linux bridge `br0`: attaches primary NIC; VMs attach here.

1. Pod network (Kubernetes): Calico default CIDR `192.168.0.0/16` (adjust via profile/variable).

1. Optional tenant VLANs: supported via [Network Config TUI](../netcfg-tui/README.md) (e.g. `br0.100`).
## DHCP Strategy
- Centralized dnsmasq or ISC DHCP on designated "monitor" node.

- MAC reservations for infrastructure nodes (admin/monitor/storage roles).

- Dynamic range for tenant VMs: e.g. `10.10.20.100-10.10.20.254`.

- Lease information exported to panel (for tenant IP visibility).
## DNS Strategy
- Authoritative internal zone: `debvisor.local`.

- Records: `node1.debvisor.local`,`node2.debvisor.local`, etc.

- Dynamic updates (TSIG) for VM hostnames upon provisioning.

- Forwarders: Cloudflare (1.1.1.1) / Google (8.8.8.8) / local resolver chain.
## Multi-Node Considerations
- Keep consistent bridge naming across nodes (`br0`).

- Ensure identical MTU for overlay + physical networks.

- Optionally enable Calico BGP for external route advertisement.
## Sample dnsmasq Configuration (excerpt)
    interface=br0
    domain=debvisor.local
    dhcp-range=10.10.20.100,10.10.20.254,12h
    dhcp-host=AA:BB:CC:DD:EE:01,node1,10.10.20.10
    dhcp-host=AA:BB:CC:DD:EE:02,node2,10.10.20.11
    server=1.1.1.1
    server=8.8.8.8
## Dynamic DNS Update Flow
1. VM create event triggers the libvirt `qemu` hook.

1. The hook calls the local helper
  `/usr/local/sbin/debvisor-vm-register.sh` (when present), which
  reads on-node TSIG key material and performs authenticated
  updates.

1. `vm123.debvisor.local` A record is inserted; reverse PTR records
  are added when appropriate.
For most environments, this host-local helper and the hostname
registration service are the canonical DNS update clients. The
lower-level `/usr/local/bin/debvisor-dns-update.sh` script can also be
used by advanced automation, but is not the primary operator-facing
interface.
## Future Enhancements
- VRRP/keepalived for highly available DNS/DHCP pair.

- nftables segmentation for tenant VLANs.

- Per-tenant DNS subzones (e.g. `tenantA.debvisor.local`).
## Troubleshooting
- Check `ip addr show br0` for interface attachment.

- Verify Calico node status: `kubectl get nodes -o wide`.

- DNS resolution: `dig +short node1.debvisor.local @`.
