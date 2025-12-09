# DebVisor On-Box Quickstart

## Verify Core Services

    cephctl health
    hvctl list
    k8sctl nodes
    docker ps

## On-box tooling

The following helper commands are provided on DebVisor hosts to make
day-to-day operations easier:

- `k8sctl` - Convenience wrapper for common Kubernetes operations on

  the local cluster. Use this when you want short, opinionated commands
  for tasks like listing nodes, checking workloads, or applying core
  manifests.

- `hvctl` - Hypervisor management helper around libvirt/VM lifecycle

  operations. Use this when creating, listing, starting, or stopping
  VMs without having to remember the full `virsh` syntax.

- `cephctl` - Wrapper for frequently used Ceph commands. Use this

  when checking cluster health, OSD status, or CephFS/RBD pools.

- `debvisor-netcfg` - Generate a simple systemd-networkd bridge

  configuration (e.g. bridge `br0` over a physical NIC). Use this with
  extra care, as it writes into `/etc/systemd/network`; test in a lab
  or with console access available.

- VM/VNC helpers (`debvisor-vm-register.sh`,`debvisor-vnc-target.sh`,

  `debvisor-vnc-ensure.sh`) - Small tools to register VMs for
  management and ensure VNC access is wired up correctly.

## Create CephFS-backed WordPress (example)

    k8sctl add-cephfs
    helm install wp bitnami/wordpress -f /addons/k8s/wordpress/wordpress-values.yaml

## Launch VM (Ubuntu cloud image)

    cp /var/lib/libvirt/images/ubuntu-cloudimg.qcow2 /var/lib/libvirt/images/vm1.qcow2
    hvctl create vm1 /var/lib/libvirt/images/vm1.qcow2
    hvctl start vm1

## Apply Monitoring Stack (placeholder)

    kubectl apply -f /opt/docker/addons/k8s/monitoring/prometheus-grafana-placeholder.yaml

Refer to repository docs for full flows.
