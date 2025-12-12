# `wireguard-mesh` role

Purpose:

- Configure a simple WireGuard-based mesh interface (`wg0`) for

  DebVisor nodes.

- Generate and store a node-local WireGuard keypair under

  `/etc/debvisor/wireguard/`.

- Render `/etc/wireguard/wg0.conf`from`wg0.conf.j2` and enable the

  `wg-quick@wg0` systemd unit.
Status:

- Usable, but intentionally minimal - it does not implement a

  full mesh controller. It expects per-node configuration
  (IPs/peers) to be provided via inventory/`group_vars`.
Key variables (typically in `host_vars`or`group_vars`):

- `mesh_vpn_ip` (required):

- The VPN address for this node, for example `"10.200.1.10/32"`.

- `mesh_listen_port` (optional):

- UDP port WireGuard listens on. Defaults to `51820`.

- `mesh_peers` (optional but recommended):

- List of peer definitions, for example:

    mesh_peers:

- name: "debvisor-2"

        public_key: "PUBKEY2..."
        endpoint: "debvisor-2.example.com:51820"
        allowed_ips: "10.200.1.11/32"
Interactions:

- This role is a building block for the secure DebVisor mesh

  described in `docs/operations.md`; higher-level automation is
  expected to distribute keys and peer definitions.
