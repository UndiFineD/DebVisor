# DebVisor Threat Model (Overview)

This document summarizes the high-level threat model for DebVisor and
links to more detailed security documentation.
It is intentionally opinionated and focuses on realistic deployment
scenarios rather than exhaustive possibilities.

## Assumed Deployment Scenarios

DebVisor is primarily designed for:

- **Single-tenant labs and homelabs**

- One operator (or a small trusted team) administers the hypervisor.

- Physical access to the host is assumed; attackers are usually remote.

- Internet access is often available but can be firewalled tightly.

- **Small clusters in trusted networks**

- A handful of DebVisor nodes share storage (Ceph, ZFS replication)

    and run a Kubernetes control plane and workloads.

- Management access is restricted to an internal network or VPN.

- **Secure multi-operator meshes (advanced)**

- Many DebVisor nodes are connected via a VPN mesh with strong

    identity and host firewalls (see `operations.md`).

- Only a subset of nodes host sensitive control-plane services; the

    rest are treated as semi-trusted workers.
DebVisor is**not**currently aimed at:

- Anonymous, internet-facing multi-tenant hosting with untrusted

  tenants deploying arbitrary workloads directly on the hypervisor.

- Environments where hardware-level attackers (e.g. malicious

  firmware, physical theft without encryption) are the primary threat.

## High-Level Security Goals

Across these scenarios, DebVisor aims to:

- Minimize attack surface on the hypervisor host.

- Keep management APIs and consoles off the public internet by

  default.

- Prefer containers/VMs as the boundary for untrusted code.

- Provide clear hooks for:

- firewall blocklists/whitelists,

- identity and MFA enforcement,

- supply-chain verification of images and software.

Details for these areas live in:

- `security.md` - baseline hardening for ISO, installer and host.

- `failover-identity-access.md` - identity, MFA, and access control

  during failover and degraded scenarios.

- `supply-chain.md` - image signing, trusted registries and update

  provenance.

## Trust Boundaries and Roles

At a minimum, DebVisor distinguishes between:

- **Hypervisor administrators**

- Full control over the host OS, storage, and virtualization stack.

- Should authenticate with SSH keys and, where enabled, SSH MFA.

- **Cluster/platform operators**

- Manage Kubernetes, Ceph and higher-level services.

- May have limited or indirect access to the underlying hypervisor.

- **Application operators / tenants**

- Deploy workloads into Kubernetes or onto VMs.

- Should not need direct shell access to the hypervisor.

The goal is to keep untrusted or semi-trusted tenants at the
container/VM boundary, with DebVisor itself treated as a trusted
infrastructure component.

## Network and Identity Assumptions

- Management access (SSH, web panel, RPC) is expected to be reachable

  only from:

- a VPN,

- a bastion host,

- or a tightly firewalled management subnet.

- DNS, storage and monitoring endpoints may be shared across many

  nodes, but should still be protected by:

- host-level firewalls (`nftables`),

- optional TLS/mTLS on higher-level services,

- and IP-based allowlists where appropriate.

- SSH MFA, when enabled, is enforced via the documented

  `enforce-mfa.yml` playbook and PAM configuration (see
  `security.md`and`operations.md`).

## Supply Chain and Update Trust

DebVisor assumes:

- ISO images and packages are obtained from trusted sources (Debian,

  Ceph, Kubernetes and DebVisor-provided repositories).

- When enabled, ISO signing and checksums are verified before

  installation (see `security.md`).

- Container images and Helm charts used on DebVisor clusters are:

- stored in registries you control,

- optionally signed (e.g. via Sigstore),

- and admitted into clusters only via GitOps or similar workflows

    (see `supply-chain.md`).
Operators should treat any deviation from these practices (for
example, pulling arbitrary images from the public internet directly
on production nodes) as a conscious risk decision.

## Failure and Degradation Modes

In degraded scenarios, DebVisor prefers:

- **Fail-closed**for management access (e.g. broken VPN means no

  direct admin access, not a fallback to wide-open SSH).

- **Fail-open with audit**for automation where strict blocking would

  cause more harm than good, but every action is logged and can be
  rolled back.
Examples and guidance are covered in more depth in
`failover-identity-access.md`.

## Where to Read Next

- Start with `security.md` for host and ISO hardening.

- Read `supply-chain.md` for image and artifact trust.

- Use `failover-identity-access.md` for planning identity and access

  during outages.

- See `operations.md` for day-2 operations, including blocklists,

  DNS/TSIG tooling, and multi-node meshes.
