# DebVisor RPC service (`debvisor.v1`)

This directory contains the DebVisor RPC API definition and service implementation.

## API surface

- The gRPC API is described in `proto/debvisor.proto`, currently versioned as `debvisor.v1`.

- It exposes cluster, tenant, VM, and storage operations over a stable machine interface.

- The API is designed to be consumed by the web panel, CLI tooling, and external automation.

## Intended clients

- **Web panel**: a thin UI that calls the RPC service to list and manage projects, workloads, and tenants.

- **CLI tooling**: on-box commands under `usr/local/bin/` (and future off-box CLIs) that talk to `debvisor.v1`.

- **Automation**: CI/CD systems or operators can use the RPC service as a single, audited entrypoint.

## Service Architecture

The RPC daemon (`server.py`) is a production-ready implementation featuring:

- **Security**: mTLS authentication, RBAC authorization, and input validation.

- **Observability**: Structured audit logging and health monitoring.

- **Reliability**: Rate limiting and graceful shutdown.

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

- **TLS/mTLS**: Enabled by default. Requires valid certificates in `/etc/debvisor/rpc/tls/`.

- **RBAC**: Permissions are checked for every RPC call.

- **Audit**: All operations are logged to `/var/log/debvisor/rpc-audit.log`.

See [SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md) for details.
