# Profiles

## usb-zfs (default)

ZFS pool across removable USB sticks for fast, simple lab setups.

- Detects removable disks via `/sys/block/*/removable == 1`, excluding the OS disk.

- Requires at least 3 empty USB sticks; creates `tank`as`raidz1` across them.

- Datasets: `tank/vm`,`tank/docker`,`tank/k8s`mounted under`/srv/*`.

- Compression `lz4` enabled by default.

- Skips any USB device that appears to contain existing data (conservative by default).

## ceph

Shared-first hyper?converged mode on non?USB disks.

- Non?OS, non-removable disks become Ceph OSDs.

- Pools: rbd (VM disks), cephfs.data/meta (CephFS).

- MDS enabled; CephFS mounted at `/srv/cephfs`.

- Libvirt prefers RBD; shared workloads use CephFS RWX.

## zfs

Local performance & simplicity on non?USB disks.

- Non?OS, non-removable disks form ZFS pool `tank`.

- Datasets: `tank/vm`,`tank/docker`,`tank/k8s`.

- Compression `lz4`; snapshots enabled for vm & docker.

## mixed

Combines shared Ceph with local ZFS datasets on non?USB disks.

- CephFS for RWX, RBD for VM disks needing network mobility.

- ZFS for fast local container/VM ephemeral datasets.

## Selection Mechanism

- Installer (curses) writes `/etc/debvisor-profile`.

- First?boot systemd unit exports PROFILE for provisioning script.

- Profiles:

- `usb-zfs` - default; ZFS across USB sticks.

- `ceph` - CephFS/RBD on non?USB storage.

- `zfs` - ZFS on non?USB storage.

- `mixed` - Ceph + ZFS combo on non?USB storage.

- Override: kernel cmdline or manually editing profile file before first boot.

## Observability

To make the selected storage profile easy to consume by automation without shell access:

- Summary files are written under `/var/log/debvisor/` on first boot:

- `/var/log/debvisor/profile-summary.txt` (human-readable)

- `/var/log/debvisor/profile-summary.json` (machine-readable)

- Source: Profile is read from `/etc/debvisor-profile` and captured with a timestamp.

- Regeneration: Re-run `debvisor-profile-summary.sh` if the profile changes.

Example JSON:
    {
      "profile": "ceph",
      "source": "/etc/debvisor-profile",
      "generated_at": "2025-11-25T12:00:00Z"
    }

## Profiles and Workloads Matrix

The table below summarizes how each profile is typically used and
where data is stored. This is a guideline; advanced deployments may
customize further.
| Profile  | Typical Use Cases                          | VM Storage                          | Container / App Storage                  |
|----------|--------------------------------------------|-------------------------------------|------------------------------------------|
| usb-zfs  | Single-node labs, experimentation, demos   | ZFS datasets under `tank/vm`| ZFS datasets under`tank/docker`/`k8s` |
| ceph     | Multi-node clusters, shared workloads      | Ceph RBD pool (e.g. `rbd`)          | CephFS at`/srv/cephfs`                  |
| zfs      | Single-node or small clusters, simplicity  | ZFS datasets under `tank/vm`| ZFS datasets under`tank/docker`/`k8s` |
| mixed    | Hybrid: shared + local performance         | Ceph RBD for highly-available VMs   | CephFS for shared, ZFS for local caches  |
For day-2 operational guidance on these profiles, see also
`operations.md`and`workloads.md`.
