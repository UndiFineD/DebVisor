# Synthetic Metrics Fixtures (Optional)

DebVisor includes optional synthetic metrics fixtures to help test dashboards and alerting in environments without real workloads.

- Delivery: ConfigMap manifests under `monitoring/fixtures/*.yaml`.
- Optional: Not applied by default; enable per environment as needed.
- Scope: Minimal noise; aim for realistic shapes without masking real signals.

## Usage

- Apply a fixture ConfigMap manually to a test cluster:

    kubectl apply -f monitoring/fixtures/edge-lab.yaml

- Remove when done:

    kubectl delete -f monitoring/fixtures/edge-lab.yaml

- Optionally deploy the synthetic metrics generator and Service:

    kubectl apply -f monitoring/fixtures/edge-lab-deployment.yaml

- Teardown the generator when finished:

    kubectl delete -f monitoring/fixtures/edge-lab-deployment.yaml

## Authoring New Fixtures

- Create a new file `monitoring/fixtures/.yaml`.
- Use a ConfigMap to carry small synthetic series definitions; larger generators should live in a dedicated Deployment.
- Keep naming consistent (prefix `debvisor-fixture-`).
- Document intended use and limits in comments.

## Building a Custom Generator Image (Optional)

DebVisor includes a tiny generator based on `prometheus_client`:

- Source: `monitoring/fixtures/generator/`
- Build locally:

    docker build -t debvisor/synthetic-metrics:local monitoring/fixtures/generator

- Use in the provided Deployment (`edge-lab-deployment.yaml`already references`debvisor/synthetic-metrics:local`).

If you prefer a registry, push the image and update the Deployment `image:` accordingly.

## Using a Published Image (GHCR)

A GitHub Actions workflow builds and pushes multi-arch images to GHCR:

- Workflow: `.github/workflows/push-generator.yml`
- Tags: `ghcr.io//synthetic-metrics:latest` and a commit tag.
- The deployment references `ghcr.io//synthetic-metrics:latest` by default.

You can override `REPO_OWNER` via environment to point the Deployment at a different owner if needed.

## Example Contents

- Example below sets up a simple time-series generator for edge lab demos.
- Metrics are exposed via `/metrics` using a small sidecar (when deployed) or consumed by an existing collector.

See `edge-lab.yaml` for a simple, self-documented example.
See `edge-lab-deployment.yaml` for an optional generator Deployment and Service.
