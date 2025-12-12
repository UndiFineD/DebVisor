# Operations & Safeguards

## Resilience

- ZFS weekly scrub (systemd timer) when ZFS present
- Ceph OSD scrubs staggered (future enhancement)
- Snapshots: ZFS datasets (vm, docker); CephFS backup policy (Implemented)

## Networking

- Bridge `br0` preconfigured on primary NIC
- Firewall: nftables with default-deny inbound; SSH allowed by default, other services enabled via explicit rules in `debvisor.nft`/`debvisor-local.nft`(including RPC on`rpc_port = 9443`)
- Calico pod subnet: 192.168.0.0/16 (adjustable)

### Hostname Registration & DNS

- `hostname-register.service`runs once after`network-online.target`and calls`/usr/local/bin/hostname-register.sh`
- The script writes the node's primary IP and FQDN into a per-host file under `/etc/dnsmasq.d/hosts/`and reloads`dnsmasq`
- Cluster-aware behavior (when etcd is reachable and `/debvisor/self/node_id` is set):
- If `/debvisor/nodes//info/fqdn` exists and is non-empty, that FQDN overrides the local one for DNS registration
- This allows centrally-assigned names in multi-node clusters while still working if etcd is down or absent
- The Ansible `node-register` role is a non-operational stub; its

  `dns-register.sh.j2` script template is kept as a__reference-only
  example__of how a TSIG-based `nsupdate` flow might look. It is not
  deployed or executed in normal DebVisor installs, to avoid
  conflicting with the built-in hostname registration and TSIG
  rotation tooling.

### Helper Scripts and Control Points

- TSIG key generation is performed on-node by

  `/usr/local/bin/tsig-keygen.sh`, which creates Bind9 include files
  (for example `/etc/bind/tsig-debvisor.conf`) and a client key under
  `/etc/debvisor/` with strict permissions.

- TSIG rotation is coordinated by `tsig-rotate.service` and

  `tsig-rotate.timer`, which invoke the helper
  `/usr/local/bin/run-tsig-rotation.sh`. That script delegates to the
  Ansible playbook `ansible/rotate-tsig-ha.yml` when present, and logs
  a clear message and exits cleanly when no playbook or inventory is
  available.

- Node hostname registration is handled by

  `/usr/local/bin/hostname-register.sh` (via
  `hostname-register.service`), which writes per-host entries under
  `/etc/dnsmasq.d/hosts/`and reloads`dnsmasq`.

- VM DNS registration on lifecycle events is driven by the libvirt

  hook `/etc/libvirt/hooks/qemu` and the helper
  `/usr/local/sbin/debvisor-vm-register.sh` (installed by the
  `vm-register` Ansible role), which both rely on on-node TSIG
  configuration rather than embedding any secrets in Ansible.

- The `node-register`,`mfa`, and`rpc-service` Ansible roles are

  deliberately kept as non-operational stubs so that enabling them is
  safe and cannot partially configure critical services; operators
  should instead use the documented playbooks and systemd units as the
  authoritative control points.

### DNS update clients

DebVisor has a few different entrypoints for updating DNS records;
only some of them are intended for day-to-day use:

- **Hostnames (nodes)**:

- The canonical path is `/usr/local/bin/hostname-register.sh`, run

    via `hostname-register.service`. It writes per-host entries under
    `/etc/dnsmasq.d/hosts/`and reloads`dnsmasq` as needed.

- **VM lifecycle updates**:

- The preferred flow is the libvirt `qemu` hook calling

    `/usr/local/sbin/debvisor-vm-register.sh` (when installed by the
    `vm-register` role). That helper is responsible for performing any
    TSIG-authenticated updates using the on-node TSIG key material and
    logs its actions for auditing.

- **Low-level DNS helper**:

- `/usr/local/bin/debvisor-dns-update.sh` is a low-level wrapper

    around `nsupdate` that can add/remove A and PTR records for a
    given host/IP. It expects TSIG keys to be present in
    `/etc/debvisor/dns.update.key` and is primarily intended for
    advanced automation or tooling that already manages TSIG material.

Most operators should not call `debvisor-dns-update.sh` directly.
Instead, prefer the hostname and VM registration paths above, which
integrate cleanly with DebVisor's TSIG rotation and logging.

## Security

- SSH password auth disabled (first?boot) unless explicitly retained
- Kubernetes PodSecurity admission (future tightening)

### SSH MFA

- DebVisor supports SSH multi-factor authentication using Google

  Authenticator (`libpam-google-authenticator`).

- The canonical way to enable and enforce MFA is via the

  `ansible/playbooks/enforce-mfa.yml` playbook, which:

- Installs the PAM module (expecting the package to be available from

    the DebVisor image or local repositories, not the public internet).

- Configures `/etc/pam.d/sshd` to require

    `pam_google_authenticator.so`(without`nullok`).

- Ensures `ChallengeResponseAuthentication yes`and`UsePAM yes` in

    `sshd_config`.

- Installs a small enrollment helper script so users can initialize

    their TOTP secrets.

- The `mfa` Ansible role is a non-operational stub that only ensures the

  package is present and then fails with a message pointing to
  `enforce-mfa.yml`, to avoid partially configuring MFA by mistake.

### Firewall blocklists and whitelists

- DebVisor uses `nftables` as the host firewall. Core rules live in

  `/etc/nftables.conf` and include DebVisor-specific snippets from
  `/etc/nftables.d/`.

- Dynamic IP blocking is managed by the `blocklist` Ansible role, which

  parses simple text-based blocklists (and optional whitelists) into an
  nftables set.

- Blocklist/whitelist files are plain text with one IPv4 address or CIDR

  per non-comment line; lines starting with `#` are ignored.

- The role computes an effective list `blocklist ? whitelist` and

  renders `/etc/nftables.d/10-blocklist.conf`, defining:

- `table inet debvisor_blocklist`
- `set blocked_ips { ? }` with all effective entries
- a `debvisor_blocklist_input`chain that drops`ip saddr @blocked_ips`.
- The main `input` chain in your nftables policy should jump to this

  chain, for example:

      chain input {
        type filter hook input priority 0;

## ... your existing rules

        jump debvisor_blocklist_input
      }

- Operators can configure source files via inventory or `group_vars`,

      for example:

  debvisor_blocklist_sources:

- /etc/debvisor/blocklist.txt

  debvisor_whitelist_sources:

- /etc/debvisor/blocklist-whitelist.txt

- Example templates are provided (not active by default):
- `/etc/debvisor/blocklist-example.txt`
- `/etc/debvisor/blocklist-whitelist-example.txt`

## Updates

- DKMS handles ZFS module rebuild on kernel upgrades
- Version pinning recommended for Ceph & Kubernetes

## Admin & Service Accounts

- Service: `webpanel`(DebVisor web UI),`debvisor-rpc`(RPC daemon),`tsig-rotator` (TSIG rotation helper); created on first boot via helper scripts and not intended for interactive login

### TSIG key generation & rotation

- On first boot, DebVisor tooling generates TSIG keys for DNS updates

      (for example, `/etc/bind/tsig-node.conf`and`/etc/bind/tsig-vm.conf`)
      using strong random secrets and strict file permissions.

- A dedicated `tsig-rotate.service` (with a corresponding timer) is

      responsible for periodically rotating these keys and reloading Bind9.

- Ansible templates `tsig-node.conf.j2`and`tsig-vm.conf.j2` are kept as

      reference-only examples of the expected file format; they do not embed
      secrets and are not normally rendered over the real key files.

## Logging & Observability

- `hostname-register.service`uses`SyslogIdentifier=hostname-register`and logs successful registrations via`logger`

## UPS Integration (Optional)

- Network UPS Tools (NUT) templates are shipped in `/etc/nut/`(`ups.conf`,`upsd.conf`,`upsmon.conf`), mostly commented
- Enables and starts `nut-server`and`nut-monitor`if`/etc/nut/ups.conf` is non-empty
- Leaves NUT services disabled otherwise

## Monitoring

DebVisor includes a comprehensive monitoring stack based on Prometheus and Grafana.

- **Prometheus**: Collects metrics from Node Exporter, Ceph, ZFS, and Kubernetes.
- **Grafana**: Visualizes metrics with pre-built dashboards.
- **Alerting**: Configured for critical system events (disk failure, high usage).

See [opt/monitoring/README.md](../monitoring/README.md) for details.

## First-boot runbook and idempotency

    DebVisor uses a single, opinionated first-boot script,
    `debvisor-firstboot.sh`, invoked by the`debvisor-firstboot.service`
    systemd unit. It is designed to be**mostly idempotent**but there are
    some operations that are intentionally one-time and potentially
    destructive.

### What first-boot does

    At a high level, first-boot is responsible for:

- Reading `/etc/debvisor-profile` (set by the installer) to choose the

      storage profile (CephFS-first, ZFS, or mixed).

- Creating and hardening core users and service accounts.
- Bringing up the primary bridge (`br0`) on the main NIC.
- Bootstrapping Ceph MON/MGR/MDS or creating ZFS pools/datasets based

      on detected extra disks.

- Enabling and wiring Cockpit, libvirt, and base firewall rules.
- Optionally seeding Docker/Kubernetes configuration for

      containers-first workloads.

    The systemd unit disables itself once the script completes
    successfully.

### When it is safe to re-run

    Re-running `debvisor-firstboot.sh` manually (for example via:

sudo /usr/local/sbin/debvisor-firstboot.sh

    is generally safe**only**for operations that are explicitly
    idempotent, such as:

- Re-creating or verifying system users and groups.
- Re-applying systemd enablement for Cockpit, libvirt, and helper

      services.

- Re-writing configuration files that are generated from the current

      profile without destroying underlying data (for example some
      kubeadm or daemon JSON templates).

    Before re-running first-boot, ensure that:

- Any storage pools (Ceph or ZFS) are in a healthy state.
- You have backups or snapshots for critical datasets.

### Operations that should**not**be repeated lightly

    Some parts of first-boot are intentionally destructive when they run
    the first time, for example:

- Wiping and partitioning "extra" disks for Ceph OSDs or ZFS pools.
- Creating new Ceph OSDs on disks that do not yet belong to a cluster.
- Creating fresh ZFS zpools with `ashift`/feature flags.

    Re-running those sections on a node that is already in service can
    result in**data loss**if the script re-detects disks as
    "available". In particular:

- Do not re-run first-boot to "change" storage profiles; instead,

      follow the documented Ceph/ZFS migration paths.

- Avoid re-running first-boot on a node that already has production

      VMs or containers unless you understand precisely which blocks of the
      script will execute.

### Recommended practice

- Treat first-boot as a**build-time step for a node**, not a general

      configuration tool.

- For correcting misconfigurations or changing policies on an existing

      node, prefer:

- Targeted Ansible playbooks.
- Manual adjustment of specific systemd units or configs.
- If a first-boot run failed part-way through and left the node in an

      unknown state, it is often safer to:

- Wipe and reinstall the node with a fresh ISO, or
- Restore from known-good ZFS or Ceph snapshots,

      rather than trying to "partially" re-run the entire script.

## Build vs runtime changes

    DebVisor intentionally separates**image build-time**from

- *runtime/day-2**changes.

    As a rule of thumb:

- Change things under `config/`+`build/` when you need a__different

      OS image__(for example to change what is on the ISO, how the
      installer behaves, or what packages are present on *every* fresh
      node).

- Use `debvisor-firstboot.sh` and Ansible roles/playbooks when you need

      to**configure or reconfigure running nodes**.

    Some concrete examples from this repository:

- Ceph/ZFS base packages and kernel modules:
- Build-time: the presence of Ceph/ZFS packages in the image is

        controlled via package lists under `config/`and the`build/`
        tooling.

- Runtime: Ceph cluster layout, pools, and ZFS datasets are managed

        by first-boot logic and Ansible, not by rebuilding the ISO.

- DNS HA vs secondary DNS behavior:
- Build-time: shipping the DNS tooling and any default resolver

        config lives in `config/`.

- Runtime: enabling `dns-ha`vs`dns-secondary`, rotating TSIG keys,

        and wiring zones to actual upstreams is done via Ansible playbooks
        and roles.

- Firewall blocklists and security hardening:
- Build-time: if a package needed for firewall management is missing

        entirely, add it to the image via `config/` and rebuild.

- Runtime: the actual blocklists, allowlists, and host-specific rules

        are maintained by Ansible roles such as the `blocklist` role and by
        security automation (for example the Argo/AWX remediation
        workflow).

- Monitoring and dashboards:
- Build-time: whether the base image includes Helm, `kubectl`, or

        other bootstrap tools is decided in `config/`.

- Runtime: which Prometheus rules, Grafana dashboards, and synthetic

        jobs are deployed is driven by Kubernetes manifests in
        `monitoring/` and any associated automation described in
        `docs/monitoring-automation.md`.

- Web panel and RPC service:
- Build-time: placeholder directories and any future packages for

        these services will be added via `config/`and`build/` when they
        are ready.

- Runtime: enabling/disabling the web panel or RPC daemon, and

        configuring their endpoints and access controls, will be handled by
        the corresponding Ansible roles once implemented.

    If you are unsure whether a change belongs to the image or to
    runtime:

- Prefer Ansible or first-boot if the change is per-cluster or

      per-node and might differ between environments.

- Prefer updating `config/`+`build/` if the change should apply to

      every fresh DebVisor installation in exactly the same way.

### Checking the installed profile on a node

    During installation, the chosen storage/profile is written to
    `/etc/debvisor-profile` on the target system. To see which profile a
    node was installed with, run:

cat /etc/debvisor-profile

    In future revisions, DebVisor may also drop a small summary file under
    `/var/log/debvisor/install-profile.log` or a similar path so that
    configuration management and monitoring systems can discover the
    profile without shell access.

## Monitoring Stack Addon (monitoring-stack role)

- DebVisor can enable a basic monitoring stack using Debian packages

      for Prometheus, node_exporter, and Grafana.

- The `monitoring-stack` Ansible role installs:
- `prometheus`and`prometheus-node-exporter`.
- `grafana` (Grafana server).
- A base directory `/opt/debvisor-monitoring` with a README

        describing the stack and its offline expectations.

- Packages are expected to be provided by the DebVisor image or local

      repositories; the role does not attempt to reach the public
      internet.

- After applying the role on a node:
- Prometheus and node_exporter run with their default Debian

        configurations (Prometheus typically scraping node_exporter on
        `localhost:9100`).

- Grafana runs as `grafana-server` and is enabled at boot, but data

        sources and dashboards must be provisioned separately (for example
        using the existing DebVisor Grafana provisioning under
        `monitoring/grafana/provisioning/`).

- Operators can point a central Grafana instance at the Prometheus

      endpoint on DebVisor nodes or use local Grafana on each node,
      depending on their aggregation model.

## Containers vs VMs

- DebVisor is**containers-first**: the default is to run

      applications, microservices, and most workloads as Docker
      containers or Kubernetes pods on the hypervisor.

- Use**containers**when:
- You are deploying new or refactored applications.
- The workload is stateless or horizontally scalable.
- You already build container images in CI/CD.
- Use**VMs**when:
- You must run a legacy OS or appliance that only ships as a VM

        image.

- You need strong OS-level isolation or custom kernels/modules that

        do not fit the host.

- You are integrating with environments that still expect VM

        formats (qcow2, raw, vmdk) and cloud-init.

    For how these choices map onto the storage profiles (`usb-zfs`,
    `ceph`,`zfs`,`mixed`), see the matrix in`profiles.md` and the
    examples in `workloads.md`.

### VM conversion helper (`debvisor-vm-convert.sh`)

- DebVisor ships a small helper script

      `scripts/debvisor-vm-convert.sh` to convert VM disk images between
      common formats using `qemu-img`.

- Supported formats today are:
- `qcow2`
- `raw`
- `vmdk`
- The script is intentionally conservative: it only runs when

      `qemu-img` is installed and the source file exists, and it creates
      the destination directory if needed.

- Basic usage:

      debvisor-vm-convert.sh \

        - -from vmdk \
        - -to qcow2 \
        - -in  /path/to/source.vmdk \
        - -out /var/lib/libvirt/images/source.qcow2

- Typical workflows include:
- Importing an existing appliance from another hypervisor by

    converting its `vmdk`or`raw`disk into`qcow2` before creating a
    libvirt domain.

- Exporting a DebVisor VM disk into a different format for use in an

    external platform.

## VM storage model

- DebVisor supports multiple storage backends for VMs; the exact

  choices depend on whether you are running a single-node hypervisor
  or a multi-node cluster.

- Common patterns and formats:

- **Local/ZFS-backed storage**:

- VM disks are typically `qcow2`or`raw` files under

      `/var/lib/libvirt/images` (for example ZFS datasets such as
      `tank/vm`mounted at`/srv/vm` with a bind-mount into
      `/var/lib/libvirt/images`).

- `qcow2` is recommended for most cases (supports snapshots and

      thin provisioning); `raw` is useful for maximum simplicity or
      when passing through entire devices.

- **Ceph RBD**:

- When using Ceph profiles, VM root disks live in a dedicated RBD

      pool (for example `vm-pool`) and are attached as block devices
      to libvirt guests.

- The guest sees a block device (for example `vda`), while Ceph

      handles redundancy and distribution across the cluster.

- **Plain files on ext4/xfs**:

- Suitable for very small or lab setups; VM disks are usually

      `qcow2`files under`/var/lib/libvirt/images` on a simple
      filesystem.

- Recommended defaults:
- For single-node or small lab deployments, use ZFS-backed `qcow2`

    images under `/var/lib/libvirt/images` so you can snapshot and
    replicate at the ZFS layer.

- For clusters, prefer Ceph RBD for VM root disks and use ZFS for

    local scratch and container storage.

- Backups and replication:
- ZFS datasets holding VM images should be snapshotted regularly and

    replicated off-node using `zfs send | zfs receive` or equivalent
    tooling.

- Ceph-based VMs can rely on Ceph's own redundancy; additional

    off-cluster backup (for example via RBD export) is encouraged for
    critical workloads.

- When mixing containers and VMs:
- Keep container image storage (for example `/var/lib/containerd` or

    `/var/lib/docker`) on its own ZFS dataset or Ceph pool, separate
    from VM disks.

- Apply consistent naming for datasets and pools (for example

    `zroot/vm`,`zroot/containers`) so that automation and monitoring
    can distinguish them.

### Cloud-init workflow for imported images

- Many cloud images (for example Ubuntu Cloud, GenericCloud) expect a

  `cidata`ISO providing cloud-init`user-data`and`meta-data`.

- DebVisor includes `scripts/debvisor-cloudinit-iso.sh` to build such

  an ISO so imported images behave like they would in a cloud.

- Basic workflow:

    1. Download or otherwise obtain a cloud image (for example

     `ubuntu-22.04-server-cloudimg-amd64.img`) into your VM storage
     pool.

    1. Create a cloud-init ISO for the VM:

     debvisor-cloudinit-iso.sh \

       - -name vm1 \
       - -out /var/lib/libvirt/images/vm1-seed.iso

        1. Define a libvirt domain that attaches both the cloud image (as

         the primary disk) and the generated `vm1-seed.iso` as a CD-ROM
         with `bus=virtio`or`sata`.

        1. Boot the VM; cloud-init will configure hostname, SSH and other

         settings from the ISO.

- Operators can pass custom `--user-data`and`--meta-data` files to

      the helper when more advanced cloud-init configuration is needed.

## RPC Service Addon (Placeholder)

- DebVisor reserves an RPC/sync service addon to support future

      remote management and orchestration workflows between DebVisor nodes
      and external tools.

- The `rpc-service` Ansible role is currently a non-operational stub:

      it creates `/opt/debvisor-rpc` and a README only; it does**not**
      deploy or start any RPC daemon yet.

- When implemented, the RPC service and its systemd units and

      configuration files are expected to live under `/opt/debvisor-rpc`
      and to be managed by this role. Until then, enabling the addon is a
      no-risk marker for future expansion.

## VNC/noVNC Console (vnc-console role)

- DebVisor can expose per-VM consoles via a VNC backend and an HTML5

      noVNC frontend, similar to Proxmox.

- The `vnc-console` Ansible role (Debian 13 + nginx) installs:
- `tigervnc-standalone-server`,`novnc`,`websockify`, and`nginx`.
- Helper scripts under `/usr/local/sbin/` such as

        `debvisor-vnc-target.sh`and`debvisor-vnc-ensure.sh`.

- A `debvisor-websockify@.service` systemd template to run

        websockify for individual VMs.

- An nginx config that serves noVNC from `/usr/share/novnc` and

        proxies `/vnc/` WebSocket connections to websockify on
        localhost.

- To use the console for a VM `vm1` after the role is applied:
- Ensure the VM has a libvirt VNC graphics device listening on

        `127.0.0.1`.

- Run `debvisor-vnc-ensure.sh vm1` on the hypervisor to start the

        corresponding `debvisor-websockify@vm1.service`.

- Open the URL printed by the helper (for example

        `/novnc/vnc.html?path=/vnc/vm1`) via the DebVisor host's nginx
        endpoint.

- Operators should restrict access to the console using host

      firewall rules (nftables) and nginx access controls and may later
      integrate it behind the DebVisor webpanel over HTTPS.

## Expansion (Implemented/Planned)

- Multi-node join scripts for Ceph OSD & MON roles (Implemented)
- kubeadm join automation with taint removal guidance (Implemented)

## Secure Multi-Operator DebVisor Mesh

    This section describes how to connect many DebVisor nodes over the internet as
    a loosely coupled "supercomputer" while maintaining strong security
    boundaries between operators and only running trusted workloads.

### 1. Secure Node-to-Node Connectivity

- Use a mesh VPN (e.g. WireGuard or Nebula) to create a private overlay

      network between DebVisor nodes.

- Each node receives:
- A unique node keypair (identity).
- A stable VPN address (for example from 10.200.0.0/16).
- A small control node (which can be a DebVisor) acts as the authority to:
- Issue and revoke node identities.
- Group nodes into trust levels, such as `trusted_local` and
- VPN ACLs and host-level `nftables` rules work together so that:
- Only specific groups can reach management endpoints (Kubernetes API, RPC,

        storage, monitoring).

- The DebVisor firewall still enforces which ports and IPs are allowed, and

        can use blocklists/whitelists to rapidly isolate misbehaving nodes.

### 2. Trusted Applications via Signing and Policy

- Define one or more signing keys for workloads, for example:
- `debvisor-app-signer` for official images and charts.
- Optional partner-specific keys for third-party workloads.
- Distribute the corresponding public keys to all DebVisor nodes (for

      example under `/etc/debvisor/trusted-signers/`) and manage them like CA
      certificates.

- For container images:
- Use Sigstore cosign or a similar tool in CI to sign images hosted in your

        registry.

- Enforce image verification in Kubernetes using admission policies (such

        as Kyverno, Gatekeeper, or ImagePolicyWebhook) so that only images from
        approved registries and signed by trusted keys are allowed.

- For manifests and Helm charts:
- Store them in a Git repository under your control.
- Use GitOps tools (such as Argo CD or Flux) so clusters sync only from

        that repository and optionally verify commit or artifact signatures.

- Prefer running arbitrary code inside containers/VMs so the Kubernetes

      admission policy is the primary gate; keep the DebVisor host as a relatively
      fixed, signed image.

### 3. Trust Boundaries Between Local and External DebVisors

- Local DebVisors (owned by you) can host control planes, storage, and other

      critical services.

- External or community DebVisors join the VPN mesh but are treated as

      semi-trusted:

- They are usually restricted to worker or job-runner roles.
- They do not receive broad access to hypervisor management or sensitive

        services unless explicitly allowed.

- Use:
- Node labels and taints to distinguish trusted vs semi-trusted workers in

        Kubernetes.

- Scheduling policies to control which workloads may run on which nodes.
- Central monitoring (Prometheus/Grafana) runs on trusted DebVisors so that

      logs and metrics from all participants can be observed in one place.

### 4. Practical Minimal Design

- Deploy a mesh VPN across all participating DebVisor nodes.
- Use Ansible to manage VPN keys/configs and to enforce `nftables` policies,

      including the dynamic blocklist/whitelist sets documented above.

- Stand up a container registry for DebVisor workloads and adopt image

      signing in CI.

- Configure Kubernetes clusters running on DebVisor with admission policies

      that only permit signed images from approved registries.

- To participate in the mesh, an operator should:
- Accept a node identity issued by the shared control authority.
- Agree to run only workloads from the signed registry (enforced by

        policy).

- Understand that their node may be categorized as semi-trusted with

        limited access.

- If a node misbehaves, you can:
- Revoke its VPN identity at the control node.
- Add its VPN IP address to DebVisor blocklists so host firewalls

        immediately drop its traffic.

## DNS HA service (dns-ha role)

    DebVisor can run a small, highly-available DNS pair for `debvisor.local`
    using Bind9 and Keepalived.

- The `dns-ha` Ansible role:
- Installs `bind9`,`keepalived`and`nftables`.
- Deploys Bind9 zone/includes from templates

        (`named.conf.local.j2`,`db.debvisor.local.j2`,`tsig-node.conf.j2`,
        `tsig-vm.conf.j2`).

- Configures Keepalived to float a virtual IP for DNS.
- Installs DNS-facing nftables rules in `/etc/nftables.d/20-dns.conf`

        and ensures `/etc/nftables.d/*.conf` is included by the main config.

- TSIG keys and rotation:
- The role**does not generate or rotate TSIG secrets itself**.
- TSIG material is managed by the dedicated rotation service

        (`tsig-rotate.service`/`tsig-rotate.timer` and helper scripts).

- The `tsig-*.conf.j2` templates are expected to reference key files

        that the rotation service creates and refreshes.

- Usage:
- Apply `dns-ha` to the hosts that should form the DNS HA pair

        (for example, an Ansible group such as `dns_ha_nodes`).

- Ensure the TSIG rotation units and scripts are installed on those

        nodes so that key material stays fresh.

- Combine with the "Firewall blocklists and whitelists" section above

        to control which clients may talk to the DNS VIP.

    Example inventory and playbook snippet:

[dns_ha_nodes]
dns1.debvisor.local
dns2.debvisor.local

- --

- name: Configure HA DNS pair

  hosts: dns_ha_nodes
  become: yes
  roles:

- dns-ha

  pre_tasks:

- name: Ensure TSIG rotation units are present

      stat:
        path: /etc/systemd/system/tsig-rotate.service
      register: tsig_rotate_service

- name: Fail if TSIG rotation service is missing

      fail:
        msg: "tsig-rotate.service not found; install TSIG rotation tooling before running dns-ha role."
      when: not tsig_rotate_service.stat.exists

## VM Registration Hook (vm-register role)

- DebVisor can optionally install a libvirt `qemu` hook script on

  hypervisor nodes via the `vm-register` Ansible role.

- The role ensures `/etc/libvirt/hooks/` exists and deploys a

  `qemu` hook that can trigger VM-related registration logic (for
  example, calling a local helper that updates DNS records).

- The hook itself does**not**embed TSIG secrets; any TSIG-based

  updates are expected to use the on-node TSIG key files and rotation
  tooling described in "TSIG key generation & rotation".

- When the hook sees a VM `started` event and is able to

   discover an IPv4 address via `virsh domifaddr`, it invokes the
   local helper `/usr/local/sbin/debvisor-vm-register.sh` (if present)
   with the VM name and IP. That helper owns the actual TSIG-authenticated
   DNS update and logs the outcome.
