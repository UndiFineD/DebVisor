# DebVisor dns-ha role

This role configures a high-availability DNS setup for DebVisor using two
(or more) Bind9 primaries behind a Keepalived/VRRP virtual IP.

## Expectations

- Target hosts are members of a group such as `debvisor_dns_ha`.

- TSIG keys and zone data are provided via templates and group variables

  (for example under `group_vars/debvisor_dns_ha.yml`).

- A VRRP/Keepalived configuration is present or managed alongside this

  role, exposing a VIP that other DebVisor components use for DNS.

## Inputs

- `debvisor_dns_ha_vip` (string, required):

- The virtual IP address that Keepalived should expose for DNS

    (for example `10.10.20.53`). Used by other components as their
    primary resolver.

- `debvisor_dns_ha_interface` (string, required):

- Network interface on which the VIP should be bound (for example

    `br0`).

- `debvisor_dns_ha_zones` (list of strings, required):

- Zones served authoritatively by this HA pair (for example

    `['debvisor.local']`).

- `debvisor_dns_ha_tsig_keys` (mapping, optional):

- TSIG key names and file paths or templates used by zone update

    clients. In most deployments, on-node TSIG rotation tooling owns
    the actual secrets; this role is responsible for referencing those
    files from Bind9 configs.

## Usage

Include this role in a play that targets your DNS HA group, for example:

- hosts: debvisor_dns_ha

      become: true
      roles:

- dns-ha

This role is intended to work in concert with the `dns-secondary` role
for additional secondaries and with on-node TSIG rotation tooling.
