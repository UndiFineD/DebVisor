# DebVisor Helper Scripts

This directory contains small helper scripts that are injected into the
DebVisor image or used during operations.

- `debvisor-vm-convert.sh` - Convert VM disk images between common

  formats (`qcow2`,`raw`,`vmdk`) using`qemu-img`. This is typically
  used when importing appliances from other hypervisors into DebVisor or
  exporting DebVisor VMs out to another platform.

- `debvisor-cloudinit-iso.sh`- Build a minimal cloud-init`cidata`

  ISO for a VM (user-data + meta-data) so that cloud-style images can
  be imported and configured easily under libvirt.

- `debvisor-migrate.sh` - Wrapper around live migration primitives for

  moving a running VM between DebVisor hosts. Use this when you want a
  safe, repeatable way to evacuate a node for maintenance without
  hand-crafting `virsh migrate` invocations.

- `debvisor-join.sh` - Join a new node to an existing DebVisor

  cluster (Ceph + Kubernetes). Use this when adding capacity; it will
  turn eligible disks into OSDs and run the appropriate kubeadm join
  flow.

- `debvisor-upgrade.sh` - Orchestrate a node upgrade with Ceph and

  Kubernetes aware steps (APT upgrades, Ceph `noout`, Kubernetes
  drain/uncordon). Use this when performing routine patching or planned
  upgrades.

- `debvisor-dns-update.sh` - Low-level helper to update DNS records

  (and, where applicable, TSIG-signed zones) for DebVisor-managed
  services. Most operators should rely on the higher-level hostname
  registration and VM registration flows documented in
  `docs/operations.md`and`docs/networking.md`; this script is
  primarily intended for advanced automation or tooling that already
  manages TSIG material.

- `debvisor-console-ticket.sh` - Generate a short-lived "console

  ticket" or token for VM/tenant access, suitable for feeding into the
  web panel or external tooling.
Additional scripts may be added over time; refer to `docs/operations.md`
for day-2 operational guidance and more detailed usage examples.

## Examples

- Live migration wrapper:

      scripts/debvisor-migrate.sh vm1 debvisor-host02

- Join a new node to an existing cluster (Ceph + K8s):

      scripts/debvisor-join.sh

- Orchestrated upgrade on a node:

          scripts/debvisor-upgrade.sh
          scripts/debvisor-upgrade.sh --dry-run   # planned path only

- Update DNS entries for DebVisor endpoints:

          scripts/debvisor-dns-update.sh --zone example.internal --host api --ip 10.0.0.10

- Generate a console ticket for a VM:

  scripts/debvisor-console-ticket.sh --vm vm1 --ttl 600
