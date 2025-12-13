# DebVisor Helper Scripts\n\nThis directory contains small helper scripts that are

injected into

the\nDebVisor image or used during operations.\n\n- `debvisor-vm-convert.sh`-
Convert VM
disk images
between common\n\n formats (`qcow2`,`raw`,`vmdk`) using`qemu-img`. This is
typically\n
used when
importing appliances from other hypervisors into DebVisor or\n exporting
DebVisor VMs out
to another
platform.\n\n-`debvisor-cloudinit-iso.sh`- Build a minimal
cloud-init`cidata`\n\n ISO for
a VM
(user-data + meta-data) so that cloud-style images can\n be imported and
configured easily
under
libvirt.\n\n- `debvisor-migrate.sh`- Wrapper around live migration primitives
for\n\n
moving a
running VM between DebVisor hosts. Use this when you want a\n safe, repeatable
way to
evacuate a
node for maintenance without\n hand-crafting`virsh
migrate`invocations.\n\n-`debvisor-join.sh`- Join
a new node to an existing DebVisor\n\n cluster (Ceph + Kubernetes). Use this
when adding
capacity;
it will\n turn eligible disks into OSDs and run the appropriate kubeadm join\n
flow.\n\n-`debvisor-upgrade.sh`- Orchestrate a node upgrade with Ceph and\n\n
Kubernetes
aware steps
(APT upgrades, Ceph`noout`, Kubernetes\n drain/uncordon). Use this when
performing routine
patching
or planned\n upgrades.\n\n- `debvisor-dns-update.sh`- Low-level helper to update
DNS
records\n\n
(and, where applicable, TSIG-signed zones) for DebVisor-managed\n services. Most
operators
should
rely on the higher-level hostname\n registration and VM registration flows
documented
in\n`docs/operations.md`and`docs/networking.md`; this script is\n primarily
intended for
advanced
automation or tooling that already\n manages TSIG material.\n\n-
`debvisor-console-ticket.sh`-
Generate a short-lived "console\n\n ticket" or token for VM/tenant access,
suitable for
feeding into
the\n web panel or external tooling.\nAdditional scripts may be added over time;
refer
to`docs/operations.md`\nfor day-2 operational guidance and more detailed usage
examples.\n\n##
Examples\n\n- Live migration wrapper:\n\n scripts/debvisor-migrate.sh vm1
debvisor-host02\n\n- Join
a new node to an existing cluster (Ceph + K8s):\n\n
scripts/debvisor-join.sh\n\n-
Orchestrated
upgrade on a node:\n\n scripts/debvisor-upgrade.sh\n scripts/debvisor-upgrade.sh
--dry-run

## planned

path only\n\n- Update DNS entries for DebVisor endpoints:\n\n
scripts/debvisor-dns-update.sh --zone
example.internal --host api --ip 10.0.0.10\n\n- Generate a console ticket for a
VM:\n\n
scripts/debvisor-console-ticket.sh --vm vm1 --ttl 600\n\n
