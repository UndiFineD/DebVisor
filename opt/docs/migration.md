# Live Migration & Failover

## Overview

DebVisor enables low-downtime relocation of running VMs across nodes using libvirt/QEMU live migration and shared Ceph RBD storage.

## Requirements

- Shared RBD pools accessible from source & target nodes.
- Matching CPU feature sets (ideally identical hardware or `host-model`).
- Stable network for migration channel (TLS protected).
- Sufficient bandwidth; consider enabling compression.

## Modes

| Mode | Notes |
|------|-------|
| Pre-Copy | Iteratively copies dirtied pages; short final pause. Default. |
| Post-Copy | Starts VM on target then fetches remaining pages; risk if network unstable. |

## Command Examples

## Pre-copy live migration

    domain="vm1"
    virsh migrate --live --persistent --compressed --p2p --tunnelled qemu:///system qemu+tls://target/system $domain

## Post-copy trigger after pre-copy start

    virsh domjobinfo $domain
    virsh migrate-postcopy $domain

## Performance Tuning

- Enable compression: `--compressed --comp-methods zlib`.
- Use dedicated migration network (separate NIC/VLAN) for large VMs.
- Adjust dirty page rate with guest ballooning during migration if needed.

## Failover Strategy

1. Health monitor detects node failure (missed heartbeats).
1. Mark affected VMs for recovery (policy‑protected list).
1. Verify source host fencing (prevent double start).
1. Start VMs on target using existing RBD volumes.

## Fencing Considerations

- Soft failure: attempt graceful migration first.
- Hard failure: ensure power fencing (IPMI/Redfish) before restart to avoid split‑brain.

## Post-Migration Hooks

- Update VM location mapping table.
- Emit audit record (old_node, new_node, duration, result).
- Trigger optional re-registration in DNS if IP changes (rare if bridged static).

## Metrics

- Migration duration (total + downtime).
- Dirty page iterations count.
- Bandwidth utilized.
- Success/failure rate; reasons categorized (network, CPU mismatch, storage latency).

## Roadmap Enhancements

- Automatic selection of optimal target (least loaded, fastest network path).
- Predictive pre-warming using historical memory change rates.
- Integration with scheduling to defragment resource usage.

## Interoperability with Other Hypervisors

DebVisor is designed to coexist with, and migrate workloads to/from,
other virtualization platforms rather than replace them outright.

### Importing VMs into DebVisor

-__Disk format conversion__:

- Use `scripts/debvisor-vm-convert.sh` to convert guest disks from

      formats such as `vmdk`or`raw` into DebVisor's preferred
      `qcow2` (or vice versa).

- Example:

    debvisor-vm-convert.sh \
      --from vmdk \
      --to qcow2 \
      --in  /path/from-vsphere/appliance.vmdk \
      --out /var/lib/libvirt/images/appliance.qcow2

-__Cloud-style images and cloud-init__:

- For images that expect cloud-init (Ubuntu Cloud, GenericCloud,

        etc.), build a seed ISO with
        `scripts/debvisor-cloudinit-iso.sh` and attach it alongside the
        converted disk.

- This lets the guest configure hostname, SSH keys and basic

        settings exactly as it would in a cloud environment.

-__Networking alignment__:

- Map the imported VM's NICs to DebVisor bridges/VLANs that provide

        equivalent connectivity (for example mapping a "DMZ" network to a
        DebVisor VLAN-backed bridge).

- Where possible, keep IP addressing stable by reusing the same

        subnets and DHCP reservations or static mappings.

### Exporting VMs from DebVisor

- To move a VM out of DebVisor:
- Shut down the guest cleanly.
- Use `debvisor-vm-convert.sh` to produce a disk image in the

        target platform's preferred format (for example `vmdk` for
        vSphere, `raw` for some clouds or bare-metal orchestrators).

- Import or register that disk with the target hypervisor using its

        native tools, then recreate the VM definition (CPU, RAM, NIC
        mapping) to match.

- For cloud-init-based guests, you can often reuse the same

      `user-data`and`meta-data` content you used on DebVisor, adjusting
      only platform-specific fields.

#### Example: libvirt XML for imported cloud image

  vm1
  4096
  2

    hvm

- The first disk points to the imported or converted cloud image

  (for example from `debvisor-vm-convert.sh`).

- The CD-ROM attaches the `cidata` ISO created by

  `debvisor-cloudinit-iso.sh`, which cloud-init consumes at boot.

- Networking is bridged via `br0`; adjust bridge name, resources, and

  machine type to match your environment.

### Mixed Environments

- DebVisor can participate in a broader environment where some

  workloads run on external clouds or virtualization platforms while
  others live on DebVisor nodes.

- Recommended patterns:
- Use a shared configuration source (for example Git + Ansible or

    GitOps) to keep VM and container definitions consistent across
    platforms.

- Expose metrics from DebVisor Prometheus and from external

    platforms into a common Grafana instance for a unified view.

- Use DNS as the primary abstraction: service names remain stable

    while the backing VM or container can move between DebVisor and
    other environments.
