# Developer Workflow

This document outlines typical contributor actions for DebVisor.

## Build Cycle

1. Modify package manifest or hooks.

1. Run `make build` to regenerate ISO.

1. Test in a VM with multiple disks (Ceph/ZFS provisioning).

1. Validate services: `ceph -s`,`zpool status`,`kubectl get nodes`, Cockpit UI.

## Local Test Matrix

- Profiles: `ceph`,`zfs`,`mixed`.

- Migration: two-node environment with shared Ceph cluster.

- Networking: verify bridge + Calico overlay.

## Recommended Tools

- `virt-install` for scripted VM creation.

- `rbd` CLI for snapshot/clone tests.

- `helm` for app deployment validation.

## Release Steps

1. Tag build commit (e.g. `v0.1.0`).

1. Generate ISO + checksum.

1. Smoke test migration + provisioning.

1. Publish release artifacts.

## Future Enhancements

- CI pipeline to automatically lint manifests and validate first-boot script in a containerized test harness.

- Integration tests for live migration and failover triggers.
