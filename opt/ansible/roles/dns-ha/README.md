# DebVisor dns-ha role\n\nThis role configures a high-availability DNS setup for DebVisor using

two\n(or more) Bind9 primaries behind a Keepalived/VRRP virtual IP.\n\n## Expectations\n\n- Target
hosts are members of a group such as `debvisor_dns_ha`.\n\n- TSIG keys and zone data are provided
via templates and group variables\n\n (for example under `group_vars/debvisor_dns_ha.yml`).\n\n- A
VRRP/Keepalived configuration is present or managed alongside this\n\n role, exposing a VIP that
other DebVisor components use for DNS.\n\n## Inputs\n\n- `debvisor_dns_ha_vip`(string,
required):\n\n- The virtual IP address that Keepalived should expose for DNS\n\n (for
example`10.10.20.53`). Used by other components as their\n primary resolver.\n\n-
`debvisor_dns_ha_interface`(string, required):\n\n- Network interface on which the VIP should be
bound (for example\n\n`br0`).\n\n- `debvisor_dns_ha_zones`(list of strings, required):\n\n- Zones
served authoritatively by this HA pair (for example\n\n`['debvisor.local']`).\n\n-
`debvisor_dns_ha_tsig_keys`(mapping, optional):\n\n- TSIG key names and file paths or templates used
by zone update\n\n clients. In most deployments, on-node TSIG rotation tooling owns\n the actual
secrets; this role is responsible for referencing those\n files from Bind9 configs.\n\n##
Usage\n\nInclude this role in a play that targets your DNS HA group, for example:\n\n- hosts:
debvisor_dns_ha\n\n become: true\n roles:\n\n- dns-ha\n\nThis role is intended to work in concert
with the`dns-secondary` role\nfor additional secondaries and with on-node TSIG rotation tooling.\n\n
