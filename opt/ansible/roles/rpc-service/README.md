# `rpc-service`role\n\nPurpose:\n\n- Placeholder role for the future DebVisor RPC / sync

service\n\n

(for example`debvisor-rpcd`).\n\n- Creates a marker directory on nodes where the RPC addon
is\n\n
conceptually enabled.\nStatus:\n\n- Stub / non-operational.\n\n- Does**not**deploy or
start any RPC
daemon yet. It only lays\n\n down `/opt/debvisor-rpc`and a README file.\nKey
variables:\n\n- None at
present. Future versions are expected to use variables for\n\n listen addresses, TLS/mTLS
configuration, and upstream endpoints.\nControl paths:\n\n- Until the RPC service is
implemented,
coordination between nodes is\n\n driven by existing tooling (Ceph, Kubernetes, Ansible)
and any\n
documented GitOps flows.\n\n- The intended API surface and security model for the RPC
service
are\n\n described in`docs/rpc-service.md`.\n\n
