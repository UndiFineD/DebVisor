# DebVisor web panel (prototype)

This directory contains a small Flask-based web application that serves as a**placeholder panel**for DebVisor.

## Purpose

- Demonstrate how a web UI could interact with the DebVisor RPC service.

- Experiment with basic workflows such as listing nodes, tenants, or workloads.

- Provide a place to iterate on UX before committing to a production-ready panel.

The current app is**not production-ready**:

- Authentication, authorization, and multi-tenant isolation are incomplete.

- Error handling, logging, and auditability are minimal.

- Hardening (TLS, headers, CSRF, session management) has not been completed.

## Relation to the RPC service

In the long term, this panel is intended to proxy and visualize data from the `debvisor.v1` RPC API:

- The panel should not shell out directly to hypervisor tools.

- All state-changing operations should flow through the RPC service.

## Deployment notes

- The app is intended to run close to the DebVisor RPC service,

  typically on the hypervisor itself as a systemd service that talks
  to `debvisor-rpcd`on`127.0.0.1:7443`.

- `requirements.txt` describes the Python dependencies; a common

  pattern is to create a dedicated virtual environment (for example
  under `/var/lib/debvisor-panel/venv`) and install the requirements
  there.

- Packagers and image build scripts can use the

  `systemd/debvisor-panel.service.example` unit as a starting point
  for wiring the panel into the base image.
Do not expose this prototype directly on the Internet without additional hardening.
