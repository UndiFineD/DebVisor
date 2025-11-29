# Example Workloads

DebVisor is containers?first: most example workloads are designed to
run as containers or Kubernetes applications, with VMs available for
cases where containerization is not yet practical.

Use containers when:

- You are deploying stateless, scalable, or cloud-native services.
- You want to lean on Kubernetes for rollout, rollback, and health checks.
- You are iterating quickly on application code.

Use VMs when:

- You are running legacy, appliance, or OS-level workloads.
- You need strong isolation or guest-level customization.
- You are dealing with vendors that only ship VM images.

## VM Templates

- Ubuntu Server cloud image (latest LTS) preloaded under `/srv/cephfs/images/ubuntu/`.
- Debian cloud image preloaded under `/srv/cephfs/images/debian/`.

For importing other VM images, see the helpers documented in
`migration.md`:

- `scripts/debvisor-vm-convert.sh`- convert disks between`vmdk`,

  `raw`, and`qcow2`.

- `scripts/debvisor-cloudinit-iso.sh`- build a cloud-init`cidata`

  ISO to attach alongside imported cloud images.

## Docker / Compose Stacks (placed in `docker\addons\compose\`)

- Traefik reverse proxy (auto TLS / dashboard).
- Nextcloud (CephFS-backed persistent volume).
- GitLab Runner (CI agent integration).

## Kubernetes Helm / Manifests (placed in `docker\addons\k8s\`)

- WordPress chart with CephFS RWX PVC.
- Prometheus + Grafana monitoring stack.
- NGINX ingress controller.

## Workload Conventions

- All persistent data for shared workloads defaults to CephFS (RWX).
- RBD used for performance-sensitive single-writer volumes (databases, VM disks).
- ZFS datasets (if mixed profile) used for ephemeral build/cache layers.

## Expansion Ideas

- Add CI/CD example: ArgoCD + sample app.
- Add ML workload: Jupyter + PVC on CephFS.
- Add Windows VM provisioning example (virtio drivers pre-linked).

## Quick Start

## Compose example

    cd docker\addons\compose\traefik
    docker compose up -d

## Kubernetes example (assuming KUBECONFIG ready)

    helm install wp docker\addons\k8s\wordpress-chart\ -f values.yaml
