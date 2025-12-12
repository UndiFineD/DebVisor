# DebVisor dns-secondary role

This role configures Bind9 secondary DNS servers for a DebVisor
deployment, consuming zones from the HA primaries managed by the
`dns-ha` role.

## Expectations

- Target hosts are members of a group such as `debvisor_dns_secondary`.

- Primary DNS endpoints, TSIG keys, and zone lists are defined in

  group variables (for example under `group_vars/debvisor_dns_secondary.yml`).

- Secondaries are allowed to perform IXFR/AXFR from the HA primaries

  and are reachable from DebVisor nodes that rely on them for DNS.

## Inputs

- `debvisor_dns_secondary_primaries` (list of strings, required):

- IPs or hostnames of the HA primaries managed by `dns-ha` from

    which this secondary should transfer zones.

- `debvisor_dns_secondary_zones` (list of strings, required):

- Zones for which this host should act as a secondary

    (for example `['debvisor.local']`).

- `debvisor_dns_secondary_tsig_keys` (mapping, optional):

- TSIG key names and include paths used for securing zone transfers

    from the primaries. As with `dns-ha`, TSIG material is normally
    created and rotated by on-node tooling; the role wires those
    files into Bind9.

## Usage

Include this role in a play that targets your DNS secondary group, for example:

- hosts: debvisor_dns_secondary

      become: true
      roles:

- dns-secondary

This role complements `dns-ha` by providing additional DNS capacity and
resilience without owning the authoritative, TSIG-protected primaries.
