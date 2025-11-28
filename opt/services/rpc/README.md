# DebVisor RPC service (`debvisor.v1`)

This directory contains the DebVisor RPC API definition and service implementation.

## API surface

- The gRPC API is described in `proto/debvisor.proto`, currently versioned as `debvisor.v1`.
- It exposes cluster, tenant, VM, and storage operations over a stable machine interface.
- The API is designed to be consumed by the web panel, CLI tooling, and external automation.

## Intended clients

- __Web panel__: a thin UI that calls the RPC service to list and manage projects, workloads, and tenants.
- __CLI tooling__: on-box commands under `usr/local/bin/` (and future off-box CLIs) that talk to `debvisor.v1`.
- __Automation__: CI/CD systems or operators can use the RPC service as a single, audited entrypoint.

## Service Architecture

The RPC daemon (`server.py`) is a production-ready implementation featuring:

- __Security__: mTLS authentication, RBAC authorization, and input validation.
- __Observability__: Structured audit logging and health monitoring.
- __Reliability__: Rate limiting and graceful shutdown.

## Generating Python stubs

Python stubs for the `debvisor.v1` API are generated into `rpc/gen/` using `grpcio-tools`:

    cd rpc
    make python

This runs `python -m grpc_tools.protoc` against `proto/debvisor.proto`.

## Packaging and deployment model

- `debvisor-rpcd` runs as a systemd service (`debvisor-rpcd.service`).
- It uses a dedicated virtual environment at `/var/lib/debvisor-rpc/venv`.
- Configuration is loaded from `/etc/debvisor/rpc/config.json`.

## Security

- __TLS/mTLS__: Enabled by default. Requires valid certificates in `/etc/debvisor/rpc/tls/`.
- __RBAC__: Permissions are checked for every RPC call.
- __Audit__: All operations are logged to `/var/log/debvisor/rpc-audit.log`.

See [SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md) for details.
