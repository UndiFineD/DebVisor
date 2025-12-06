# Kubernetes addons

This directory contains optional Kubernetes addons that can be enabled on a DebVisor cluster.

## Included addons

-**Monitoring stack**(`monitoring/`):

- `prometheus.yaml`,`grafana.yaml`, and

    `prometheus-grafana-placeholder.yaml` provide minimal, non-production
    examples of a monitoring namespace and core components.

- For real deployments, use Helm charts such as `kube-prometheus-stack`

    and follow `docs/monitoring-automation.md`.

-**Ingress**(`ingress/`):

- `nginx-ingress.yaml` sketches a very small ingress controller

    deployment and namespace. It is a placeholder only; use the official
    ingress-nginx Helm chart in production.

-**Storage CSI**(`csi/`):

- `ceph-csi-rbd.yaml`,`ceph-csi-cephfs.yaml`, and`zfs-localpv.yaml`

    reserve namespaces and CSIDriver objects for Ceph RBD/CephFS and ZFS
    LocalPV. Real clusters should apply upstream CSI manifests.

-**Security**(`security/`):

- `require-signed-images.yaml` demonstrates how to enforce image

    signing/verification for Kubernetes workloads.

-**Other examples**: Additional sample manifests used for validation
  or experimentation.

## Enabling addons

From a management shell on a DebVisor node with `kubectl` configured:

- Enable an addon group (for example monitoring) with:

      kubectl apply -f docker\addons\k8s\monitoring\

- Ensure cluster networking (Calico) is healthy and that any required

      storage backends (Ceph, ZFS) are online before applying storage CSI
      manifests.

## Disabling / rolling back

- Remove an addon by deleting the resources it created, for example:

  kubectl delete -f docker\addons\k8s\monitoring\

- Before removing storage-related addons, check for associated

  PersistentVolumeClaims, StorageClasses, and running pods that depend
  on them.

- For ingress-related addons, ensure that services are either moved to a

  different ingress implementation or have alternative access paths.

## Interaction with DebVisor networking, DNS, and monitoring

- Many addons expose Services that should be reachable via the DebVisor

  bridge network and HA DNS; use appropriate Service types and, where
  needed, Ingress objects.

- Monitoring-related addons should reuse existing label conventions so

  they integrate cleanly with the DebVisor Grafana dashboards and
  Prometheus alerting described in `docs/monitoring-automation.md`.

- When in doubt, prefer running addons on nodes sized for

  control-plane/monitoring workloads rather than general-purpose
  hypervisors.
