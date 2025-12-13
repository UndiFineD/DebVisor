# DebVisor dns-secondary role\n\nThis role configures Bind9 secondary DNS servers for a

DebVisor\ndeployment, consuming zones from the HA primaries managed by the\n`dns-ha`role.\n\n##
Expectations\n\n- Target hosts are members of a group such as`debvisor_dns_secondary`.\n\n- Primary
DNS endpoints, TSIG keys, and zone lists are defined in\n\n group variables (for example under
`group_vars/debvisor_dns_secondary.yml`).\n\n- Secondaries are allowed to perform IXFR/AXFR from the
HA primaries\n\n and are reachable from DebVisor nodes that rely on them for DNS.\n\n## Inputs\n\n-
`debvisor_dns_secondary_primaries`(list of strings, required):\n\n- IPs or hostnames of the HA
primaries managed by`dns-ha`from\n\n which this secondary should transfer
zones.\n\n-`debvisor_dns_secondary_zones`(list of strings, required):\n\n- Zones for which this host
should act as a secondary\n\n (for example`['debvisor.local']`).\n\n-
`debvisor_dns_secondary_tsig_keys`(mapping, optional):\n\n- TSIG key names and include paths used
for securing zone transfers\n\n from the primaries. As with`dns-ha`, TSIG material is normally\n
created and rotated by on-node tooling; the role wires those\n files into Bind9.\n\n##
Usage\n\nInclude this role in a play that targets your DNS secondary group, for example:\n\n- hosts:
debvisor_dns_secondary\n\n become: true\n roles:\n\n- dns-secondary\n\nThis role complements
`dns-ha` by providing additional DNS capacity and\nresilience without owning the authoritative,
TSIG-protected primaries.\n\n
