# Kustomize Overlays for Synthetic Metrics Generator

Use Kustomize overlays to select deployment options, including which registry/owner hosts the generator image.
## Structure
- `base/`: references the fixture ConfigMap and the Deployment/Service.

- `overlays/debvisor/`: uses`ghcr.io/debvisor/synthetic-metrics:latest`.

- `overlays/customer-sample/`: example overlay using`ghcr.io/customer-sample/synthetic-metrics:latest`.
## Usage
- Apply the DebVisor default overlay:
    kubectl apply -k monitoring/fixtures/kustomize/overlays/debvisor

- Apply a custom overlay (replace `customer-sample` with your org):
    kubectl apply -k monitoring/fixtures/kustomize/overlays/customer-sample
## Creating Your Overlay
1. Copy `overlays/customer-sample`to`overlays/`.

1. Edit `kustomization.yaml`to set the`images:` block with your GHCR owner.

1. Optionally add patches for namespace, replicas, or labels.
## Notes
- Overlays update the image via Kustomize `images:`. Ensure the base deployment image name matches the target for replacement.

- You can still override via environment (`REPO_OWNER`) if deploying without Kustomize; overlays are the recommended approach.
