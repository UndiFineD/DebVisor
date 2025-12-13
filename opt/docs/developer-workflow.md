# Developer Workflow\n\nThis document outlines typical contributor actions for

DebVisor.\n\n## Build

Cycle\n\n1. Modify package manifest or hooks.\n\n1. Run `make build`to regenerate
ISO.\n\n1. Test in
a VM with multiple disks (Ceph/ZFS provisioning).\n\n1. Validate services:`ceph -s`,`zpool
status`,`kubectl get nodes`, Cockpit UI.\n\n## Local Test Matrix\n\n- Profiles:
`ceph`,`zfs`,`mixed`.\n\n- Migration: two-node environment with shared Ceph cluster.\n\n-
Networking: verify bridge + Calico overlay.\n\n## Recommended Tools\n\n- `virt-install`for
scripted
VM creation.\n\n-`rbd`CLI for snapshot/clone tests.\n\n-`helm`for app deployment
validation.\n\n##
Release Steps\n\n1. Tag build commit (e.g.`v0.1.0`).\n\n1. Generate ISO + checksum.\n\n1.
Smoke test
migration + provisioning.\n\n1. Publish release artifacts.\n\n## Future Enhancements\n\n-
CI
pipeline to automatically lint manifests and validate first-boot script in a containerized
test
harness.\n\n- Integration tests for live migration and failover triggers.\n\n
