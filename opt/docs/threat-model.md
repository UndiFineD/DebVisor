# DebVisor Threat Model (Overview)\n\nThis document summarizes the high-level threat model

for

DebVisor and\nlinks to more detailed security documentation.\nIt is intentionally
opinionated and
focuses on realistic deployment\nscenarios rather than exhaustive possibilities.\n\n##
Assumed
Deployment Scenarios\n\nDebVisor is primarily designed for:\n\n- **Single-tenant labs and
homelabs**\n\n- One operator (or a small trusted team) administers the hypervisor.\n\n-
Physical
access to the host is assumed; attackers are usually remote.\n\n- Internet access is often
available
but can be firewalled tightly.\n\n- **Small clusters in trusted networks**\n\n- A handful
of
DebVisor nodes share storage (Ceph, ZFS replication)\n\n and run a Kubernetes control
plane and
workloads.\n\n- Management access is restricted to an internal network or VPN.\n\n-
**Secure
multi-operator meshes (advanced)**\n\n- Many DebVisor nodes are connected via a VPN mesh
with
strong\n\n identity and host firewalls (see `operations.md`).\n\n- Only a subset of nodes
host
sensitive control-plane services; the\n\n rest are treated as semi-trusted
workers.\nDebVisor
is**not**currently aimed at:\n\n- Anonymous, internet-facing multi-tenant hosting with
untrusted\n\n
tenants deploying arbitrary workloads directly on the hypervisor.\n\n- Environments where
hardware-level attackers (e.g. malicious\n\n firmware, physical theft without encryption)
are the
primary threat.\n\n## High-Level Security Goals\n\nAcross these scenarios, DebVisor aims
to:\n\n-
Minimize attack surface on the hypervisor host.\n\n- Keep management APIs and consoles off
the
public internet by\n\n default.\n\n- Prefer containers/VMs as the boundary for untrusted
code.\n\n-
Provide clear hooks for:\n\n- firewall blocklists/whitelists,\n\n- identity and MFA
enforcement,\n\n- supply-chain verification of images and software.\n\nDetails for these
areas live
in:\n\n- `security.md`- baseline hardening for ISO, installer and
host.\n\n-`failover-identity-access.md`- identity, MFA, and access control\n\n during
failover and
degraded scenarios.\n\n-`supply-chain.md`- image signing, trusted registries and
update\n\n
provenance.\n\n## Trust Boundaries and Roles\n\nAt a minimum, DebVisor distinguishes
between:\n\n-
**Hypervisor administrators**\n\n- Full control over the host OS, storage, and
virtualization
stack.\n\n- Should authenticate with SSH keys and, where enabled, SSH MFA.\n\n-
**Cluster/platform
operators**\n\n- Manage Kubernetes, Ceph and higher-level services.\n\n- May have limited
or
indirect access to the underlying hypervisor.\n\n- **Application operators /
tenants**\n\n- Deploy
workloads into Kubernetes or onto VMs.\n\n- Should not need direct shell access to the
hypervisor.\n\nThe goal is to keep untrusted or semi-trusted tenants at the\ncontainer/VM
boundary,
with DebVisor itself treated as a trusted\ninfrastructure component.\n\n## Network and
Identity
Assumptions\n\n- Management access (SSH, web panel, RPC) is expected to be reachable\n\n
only
from:\n\n- a VPN,\n\n- a bastion host,\n\n- or a tightly firewalled management
subnet.\n\n- DNS,
storage and monitoring endpoints may be shared across many\n\n nodes, but should still be
protected
by:\n\n- host-level firewalls (`nftables`),\n\n- optional TLS/mTLS on higher-level
services,\n\n-
and IP-based allowlists where appropriate.\n\n- SSH MFA, when enabled, is enforced via the
documented\n\n`enforce-mfa.yml`playbook and PAM configuration
(see\n`security.md`and`operations.md`).\n\n## Supply Chain and Update Trust\n\nDebVisor
assumes:\n\n- ISO images and packages are obtained from trusted sources (Debian,\n\n Ceph,
Kubernetes and DebVisor-provided repositories).\n\n- When enabled, ISO signing and
checksums are
verified before\n\n installation (see `security.md`).\n\n- Container images and Helm
charts used on
DebVisor clusters are:\n\n- stored in registries you control,\n\n- optionally signed (e.g.
via
Sigstore),\n\n- and admitted into clusters only via GitOps or similar workflows\n\n (see
`supply-chain.md`).\nOperators should treat any deviation from these practices
(for\nexample,
pulling arbitrary images from the public internet directly\non production nodes) as a
conscious risk
decision.\n\n## Failure and Degradation Modes\n\nIn degraded scenarios, DebVisor
prefers:\n\n-
**Fail-closed**for management access (e.g. broken VPN means no\n\n direct admin access,
not a
fallback to wide-open SSH).\n\n- **Fail-open with audit**for automation where strict
blocking
would\n\n cause more harm than good, but every action is logged and can be\n rolled
back.\nExamples
and guidance are covered in more depth in\n`failover-identity-access.md`.\n\n## Where to
Read
Next\n\n- Start with `security.md`for host and ISO hardening.\n\n-
Read`supply-chain.md`for image
and artifact trust.\n\n- Use`failover-identity-access.md`for planning identity and
access\n\n during
outages.\n\n- See`operations.md` for day-2 operations, including blocklists,\n\n DNS/TSIG
tooling,
and multi-node meshes.\n\n
