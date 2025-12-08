# `rpc-service` role

Purpose:

- Placeholder role for the future DebVisor RPC / sync service

  (for example `debvisor-rpcd`).

- Creates a marker directory on nodes where the RPC addon is

  conceptually enabled.

Status:

- Stub / non-operational.
- Does**not**deploy or start any RPC daemon yet. It only lays

  down `/opt/debvisor-rpc` and a README file.

Key variables:

- None at present. Future versions are expected to use variables for

  listen addresses, TLS/mTLS configuration, and upstream endpoints.

Control paths:

- Until the RPC service is implemented, coordination between nodes is

  driven by existing tooling (Ceph, Kubernetes, Ansible) and any
  documented GitOps flows.

- The intended API surface and security model for the RPC service are

  described in `docs/rpc-service.md`.
