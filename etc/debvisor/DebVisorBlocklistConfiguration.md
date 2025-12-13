# DebVisor Blocklist Configuration\n\nThis directory contains IP/CIDR blocklists and

whitelists used

for network security filtering in DebVisor deployments.\n\n##
Purpose\n\nBlocklists
provide a way to
deny traffic from or to specific IP address ranges, while whitelists allow
exceptions to
blocking
rules. They are used to:\n\n- Block known malicious IP ranges and attackers\n\n-
Restrict
access to
internal networks from untrusted sources\n\n- Allow critical infrastructure
exceptions to
blocking
rules\n\n- Enforce network security policies across the cluster\n\n## File
Format
Specification\n\n### Basic Rules\n\n- **One entry per line**: Each CIDR block or
IP
address occupies
its own line\n\n- **Comments**: Lines starting with `#`are ignored\n\n- **Blank
lines**:
Empty lines
are ignored and can be used for readability\n\n- **Inline comments**: Comments
after
entries are
supported (e.g.,`10.0.0.0/8 # Private RFC1918`)\n\n- **Trailing whitespace**:
Automatically
trimmed\n\n### Supported Format Specifications\n\n#### IPv4 CIDR
Notation\n\nStandard IPv4
CIDR
notation with network prefix length:\n 192.168.1.0/24\n 10.0.0.0/8\n
172.16.0.0/12\n\n####
IPv6 CIDR
Notation\n\nIPv6 CIDR notation for IPv6 network blocks:\n 2001:db8::/32\n
fe80::/10\n
ff00::/8\n\n#### Single IP Addresses\n\nIndividual IPv4 or IPv6 addresses
(treated as /32
and /128
respectively):\n 10.0.0.1\n 192.168.1.100\n 2001:db8::1\n\n#### Inline
Comments\n\nComments can
follow entries on the same line:\n 10.0.0.0/8 # Private RFC1918 network\n
192.168.0.0/16 #
Private
network range\n 172.16.0.0/12 # Private network range\n 203.0.113.0/24 #
TEST-NET-3
(documentation)\n\n### IPv6-Specific Considerations\n\nIPv6 blocklists require
careful
handling due
to the expanded address space and special address ranges. This section documents
IPv6-specific
behaviors and best practices.\n\n#### IPv6 Address Categories\n\n### Global
Unicast
Addresses
(2000::/3)\n\nThese are routable IPv6 addresses equivalent to IPv4 public
addresses. Block
or allow
as you would IPv4 ranges.\n\n## Example: Malicious actor IPv6 range
(documentation)\n\n
2001:db8:cafe::/48 # Global unicast prefix\n\n## Example: Cloud provider IPv6
range\n\n
2600:1f00::/32 # Major cloud provider (example)\n\n## Unique Local Addresses
(fc00::/7)\n\nIPv6
equivalent of RFC1918 private ranges. Typically whitelisted internally.\n\n##
Internal
organizational networks\n\n fc00:1234::/32 # Organization A internal network\n
fc00:5678::/32 #
Organization B internal network\n fd00:1111::/32 # Department-specific ULA
(documentation
format)\n\n## Link-Local Addresses (fe80::/10)\n\nUsed for direct communication
between
nodes on the
same link. Rarely blocked but may be whitelisted for specific security
zones.\n\n##
Typically DO NOT
block link-local in cluster environments\n\n## fe80::/10 # All link-local
(usually
safe)\n\n## But
may whitelist if blocking all IPv6\n\n fe80::/10 # Allow cluster
heartbeats\n\n##
Multicast
Addresses (ff00::/8)\n\nReserved for multicast traffic. Blocking depends on use
case
(mDNS, neighbor
discovery, etc.).\n\n## Example: Restrict multicast to trusted sources only\n\n
ff00::/8 #
All
multicast (typically blocked or restricted)\n ff02::1 # All nodes link-local
multicast
(for ND)\n
ff02::2 # All routers link-local multicast (for RA)\n\n## Loopback and
Unspecified
(::1/128,
::/128)\n\nIPv6 loopback equivalent to 127.0.0.1. Should almost never be
blocked.\n\n##
NEVER BLOCK
in production\n\n## ::1/128 # IPv6 loopback (critical infrastructure)\n\n##
::/128 #
Unspecified
address (internal use)\n\n## Documentation Prefix (2001:db8::/32)\n\nReserved
for
documentation and
examples. Safe to use in labs/tests.\n\n## Example ranges (documentation
only)\n\n
2001:db8:bad::/48

## Malicious range (example)\n 2001:db8:cafe::/48 # Partner network (example)\n

2001:db8:test::/48 #

Test range (example)\n\n## Dual-Stack Considerations\n\nWhen operating with both
IPv4 and
IPv6:\n1.**Independent Filtering**: IPv4 and IPv6 are filtered separately. A
blocked IPv4
range does
NOT automatically block its IPv6 equivalent.\n1.**Dual Entries**: For
comprehensive
filtering, add
both IPv4 and IPv6 entries:\n\n## Block both IPv4 and IPv6 for the same
actor\n\n
203.0.113.0/24 #
Malicious IPv4 range\n 2001:db8:bad::/48 # Same actor's IPv6
range\n1.**IPv4-Mapped IPv6
Addresses**: Some systems use `::ffff:192.0.2.0/120`to represent IPv4 addresses
in IPv6
format.
Decide whether to block both or just one.\n\n## IPv4 blocklist entry\n\n
192.0.2.0/24\n\n##
IPv6-mapped version (optional, for defense-in-depth)\n\n
::ffff:192.0.2.0/120\n1.**Dual-Stack
Testing**: When validating, test both IPv4 and IPv6 traffic:\n\n## Test IPv4
traffic from
blocked
range\n\n curl --ipv4 --source-address 203.0.113.1
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)\n\n##
Test IPv6 traffic from blocked range\n\n curl --ipv6 --source-address
2001:db8:bad::1
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)\n\n##
Test via DNS (may resolve to either)\n\n curl
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)\n\n##
IPv6 Validation with validate-blocklists.sh\n\nThe validation script
automatically detects
and
validates both IPv4 and IPv6 entries:\n\n## Validate mixed IPv4/IPv6
blocklist\n\n
./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt
--verbose\nCheck
for
IPv6-specific issues:\n ./etc/debvisor/validate-blocklists.sh --blocklist
blocklist-example.txt
--json | grep -E '"address_family".*"IPv6"'\nOutput will show:\n\n- Total
entries (IPv4 +
IPv6)\n\n-
IPv4 entry count\n\n- IPv6 entry count\n\n- Any validation errors with address
family\n\n## IPv6 in
Firewall Rules\n\nDifferent firewall backends handle IPv6 differently:\n\n-
*nftables**:\n\n## IPv4
rules\n\n nft add rule filter input ip saddr 203.0.113.0/24 drop\n\n## IPv6
rules
(separate)\n\n nft
add rule filter input ip6 saddr 2001:db8:bad::/48 drop\n\n- *iptables vs
ip6tables**:\n\n## IPv4
rules use iptables\n\n iptables -A INPUT -s 203.0.113.0/24 -j DROP\n\n## IPv6
rules use
separate
ip6tables command\n\n ip6tables -A INPUT -s 2001:db8:bad::/48 -j DROP\nAnsible
playbooks
should
handle both:\n\n- name: Block IPv4 range\n\n iptables:\n chain: INPUT\n source:
203.0.113.0/24\n
jump: DROP\n\n- name: Block IPv6 range\n\n ip6tables:\n chain: INPUT\n source:
2001:db8:bad::/48\n
jump: DROP\n\n## blocklist-example.txt\n\nThe main blocklist containing entries
to**deny**. Traffic
matching these entries will be blocked.\nExample contents:\n\n## Known malicious
ranges
(example
only - use real threat intelligence)\n\n 203.0.113.0/24 # TEST-NET-3\n
198.51.100.0/24 #
TEST-NET-2\n\n## Botnets and known C&C infrastructure\n\n 198.51.100.50/32\n\n##
Tor exit
nodes (if
policy requires blocking)\n\n## Note: Keep separate file if frequently
updated\n\n##
blocklist-whitelist-example.txt\n\nThe whitelist containing**exceptions**to
blocking
rules. Entries
here are allowed even if they match blocking rules.\nExample contents:\n\n##
Critical
infrastructure
that must bypass blocklist\n\n 10.0.0.1/32 # Primary DNS server\n 10.0.0.2/32 #
Secondary
DNS
server\n 203.0.113.100/32 # Trusted partner gateway\n\n## Internal networks that
should
not be
blocked\n\n 10.0.0.0/8 # Internal RFC1918\n 172.16.0.0/12 # Internal RFC1918\n
192.168.0.0/16 #
Internal RFC1918\n\n## Common Use Cases\n\n### Internal Networks\n\nAllow
internal
networks through
whitelisting:\n 10.0.0.0/8 # Class A private\n 172.16.0.0/12 # Class B private\n
192.168.0.0/16 #
Class C private\n fc00::/7 # IPv6 Unique Local Addresses (ULA)\n\n### Known
Malicious
IPs\n\nBlock
ranges from threat intelligence feeds:\n\n## Example: Botnet ranges\n\n
203.0.113.0/24\n
198.51.100.0/24\n\n## Example: Known attack infrastructure\n\n
192.0.2.0/24\n\n##
Gateway/Load
Balancer Access\n\nWhitelist gateways and load balancers that should bypass
filters:\n
10.1.1.1/32 #
Primary gateway\n 10.1.1.2/32 # Secondary gateway\n 10.2.0.0/16 # Load balancer
pool\n\n###
Multicast and Special Ranges\n\nBlock or allow multicast and special-use
ranges:\n\n##
Multicast
(typically blocked)\n\n 224.0.0.0/4\n\n## Link-local (IPv6)\n\n fe80::/10\n\n##
Loopback
(typically
whitelisted for localhost)\n\n 127.0.0.1/8\n ::1/128\n\n## Difference Between
Blocklist
and
Whitelist\n\n| Aspect | Blocklist | Whitelist
|\n|--------|-----------|-----------|\n|**Purpose**|
Deny traffic | Allow exceptions |\n|**Effect**| Drops/rejects traffic from
blocked ranges
| Permits
traffic from whitelisted ranges |\n|**Override**| Whitelist entries override
blocklist |
Takes
precedence over blocklist
|\n|**File**|`blocklist-example.txt`|`blocklist-whitelist-example.txt`|\n|**Use case**| Block
malicious/untrusted IPs | Permit critical infrastructure |\n\n### Processing
Order\n\n1.**Whitelist
check first**: If an IP is in the whitelist, traffic is allowed (fastest
path)\n1.**Blocklist
check**: If not whitelisted, check against blocklist\n1.**Default policy**:
Allow (if not
in
blocklist)\n\n## Integration with DebVisor Systems\n\n### Firewall Integration
Points\n\nBlocklists
are consumed by the firewall at:\n\n- **nftables
rules**(`/etc/nftables.d/debvisor-blocklist.nft`)\n\n- **iptables rules**(if
using legacy
iptables)\n\n- **Cloud provider security groups**(if applicable)\n\n### Ansible
Integration\n\nDebVisor Ansible variables for deploying blocklists:\n\n##
Enable/disable
blocklist
filtering globally\n\n debvisor_blocklist_enabled: true\n\n## Paths to blocklist
files
(can be
multiple)\n\n debvisor_blocklist_sources:\n\n-
/etc/debvisor/blocklist-example.txt\n\n-
/etc/debvisor/blocklist-malware.txt\n\n- /etc/debvisor/blocklist-p2p.txt\n\n##
Paths to
whitelist
files\n\n debvisor_whitelist_sources:\n\n-
/etc/debvisor/blocklist-whitelist-example.txt\n\n-
/etc/debvisor/whitelist-internal-infrastructure.txt\n\n## Reload firewall after
applying
lists\n\n
debvisor_blocklist_reload_firewall: true\n\n## DNS Integration\n\nBlocklists can
also be
used for
DNS filtering:\n\n- DNS queries from blocked ranges are rejected\n\n- Queries
for blocked
domains
are filtered\n\n- Whitelist entries receive fast-track DNS responses\n\n##
Performance
Considerations\n\n### Blocklist Size Guidelines\n\n| Size | Impact |
Recommendation
|\n|------|--------|-----------------|\n|  100k entries | Significant | Requires
optimization/tuning
|\n\n### Memory Footprint\n\nApproximate memory usage for firewall rules:\n\n- nftables: ~10-100
bytes per rule (depending on complexity)\n\n- iptables: ~50-200 bytes per
rule\n\n-
Example: 50k
rules ? 5-10 MB memory\n\n### Performance Optimization Strategies\n\n####
Segmentation\n\nSplit
large blocklists by category:\n blocklist-malware.txt # Known malicious IPs\n
blocklist-p2p.txt #
Peer-to-peer networks\n blocklist-botnets.txt # Botnet infrastructure\n
blocklist-scanners.txt #
Known network scanners\nLoad only needed categories per environment:\n
debvisor_blocklist_sources:\n\n- /etc/debvisor/blocklist-malware.txt # Always
load\n\n-
/etc/debvisor/blocklist-p2p.txt # Load in restrictive environments\n\n####
Tiered
Blocking\n\nImplement priority levels:\n\n## Critical blocks (evaluated
first)\n\n
203.0.113.0/24\n\n## Warning-only blocks (logged but may be allowed)\n\n
198.51.100.0/24 #
Monitored
but not blocked\n\n## Caching\n\nFor static blocklists:\n\n## Cache blocklist in
memory
with TTL\n\n
debvisor_blocklist_cache_ttl: 3600 # seconds\n\n## Re-validate periodically\n\n
debvisor_blocklist_validation_interval: 86400 # daily\n\n## Benchmarking\n\nTest
performance impact
in your environment:\n\n## Benchmark script (example)\n\n
./etc/debvisor/benchmark-blocklist.sh
\\n\n - -blocklist /etc/debvisor/blocklist-example.txt \\n\n - -packets 100000
\\n\n -
-output
/tmp/benchmark-results.json\n\n## Version Control and Updates\n\n###
Versioning\n\nBlocklists are
versioned using:\n\n## Version format: YYYY-MM-DD-HHMMSS\n\n
2025-11-26-143022\n\n## Or
semantic
versioning\n\n v1.2.3\n\n## Metadata File\n\n`blocklist-metadata.json`tracks:\n
{\n
"blocklist_version": "2025-11-26-143022",\n "blocklist_count": 1250,\n
"whitelist_count":
45,\n
"sources": [\n {\n "name": "malware",\n "url":
"[https://threatintel.example.com/malware.txt",]([https://threatintel.example.com/malware.txt"]([https://threatintel.example.com/malware.txt]([https://threatintel.example.com/malware.tx]([https://threatintel.example.com/malware.t]([https://threatintel.example.com/malware.]([https://threatintel.example.com/malware]([https://threatintel.example.com/malwar]([https://threatintel.example.com/malwa]([https://threatintel.example.com/malw]([https://threatintel.example.com/mal]([https://threatintel.example.com/ma]([https://threatintel.example.com/m]([https://threatintel.example.com/]([https://threatintel.example.com]([https://threatintel.example.co]([https://threatintel.example.c]([https://threatintel.example.]([https://threatintel.example]([https://threatintel.exampl]([https://threatintel.examp]([https://threatintel.exam]([https://threatintel.exa]([https://threatintel.ex]([https://threatintel.e]([https://threatintel.]([https://threatintel]([https://threatinte]([https://threatint]([https://threatin]([https://threati]([https://threat]([https://threa]([https://thre]([https://thr]([https://th]([https://t](https://t)h)r)e)a)t)i)n)t)e)l).)e)x)a)m)p)l)e).)c)o)m)/)m)a)l)w)a)r)e).)t)x)t)"),)\n
"updated": "2025-11-26T14:30:22Z",\n "sha256": "abc123..."\n }\n ],\n "caveats":
[\n
"Malware list
is 2 days old; recommend daily refresh",\n "Tor exit nodes list may be
incomplete"\n ],\n
"applicable_versions": [\n "bookworm",\n "trixie"\n ]\n }\n\n### Automated
Updates\n\nEnable
automated blocklist updates:\n\n## Scheduled CI job (example with GitHub
Actions)\n\n-
cron: '0 2
***' # Daily at 2 AM UTC\n\n## Tasks\n\n## 1. Check upstream for updates\n\n##

1. Validate
syntax
and ranges\n\n## 3. Detect anomalies (size changes, new sources)\n\n## 4. Create
PR with
changes\n\n## 5. Notify operators\n\n## Security Considerations\n\n### Supply
Chain
Security\n\n-**Verify sources**: Ensure blocklist URLs are correct
(typosquatting
risk)\n\n- **GPG
signatures**: Verify GPG signatures if available from upstream\n\n- **HTTPS
only**: Always
fetch
blocklists over HTTPS\n\n- **Checksums**: Compare SHA256 against known-good
values\n\n###
Integrity
Checking\n\n## Generate and store checksums\n\n sha256sum
/etc/debvisor/blocklist-example.txt >
/etc/debvisor/blocklist-example.txt.sha256\n\n## Verify on deployment\n\n
sha256sum -c
/etc/debvisor/blocklist-example.txt.sha256\n\n## Denial-of-Service Risks\n\n-
Very large
blocklists
can consume memory/CPU\n\n- Overlapping ranges waste resources\n\n- Frequent
updates can
cause
firewall reload storms\n\n### Rollback Procedure\n\nIf a blocklist causes
problems:\n\n##
Disable
blocklist immediately\n\n sudo systemctl set-environment
DEBVISOR_BLOCKLIST_ENABLED=false\n sudo
systemctl restart nftables\n\n## Restore previous version\n\n sudo cp
/etc/debvisor/blocklist-example.txt.backup
/etc/debvisor/blocklist-example.txt\n\n##
Capture
firewall state for debugging\n\n sudo nft list ruleset >
/tmp/firewall-before-fix.nft\n
sudo nft
flush ruleset\n\n## Re-apply with older blocklist\n\n## Testing and
Validation\n\n### Unit
Testing\n\nTest blocklist syntax and correctness:\n
./etc/debvisor/validate-blocklists.sh
\\n\n -
-blocklist /etc/debvisor/blocklist-example.txt \\n\n - -check-overlaps \\n\n -
-verbose\n\n###
Integration Testing\n\nVerify blocklists work in practice:\n\n## Test
environment
deployment\n\n
ansible-playbook opt/ansible/playbooks/deploy-blocklist.yml \\n\n - i
inventory.test \\n\n

- -tags
blocklist\n\n## Verify firewall rules loaded\n\n sudo nft list chain filter input | grep
blocklist\n\n## Test traffic from blocked IP\n\n curl --source-address
203.0.113.1
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)

## Should fail\n\n## Smoke Tests\n\nPost-deployment validation:\n\n## 1. Verify firewall

rules are

active\n\n sudo nft list ruleset | grep -c "drop from"\n\n## 2. Check for rule
conflicts\n\n sudo
nft validate\n\n## 3. Monitor logs for excessive drops\n\n sudo journalctl -u
nftables -n
100\n\n##

- Verify whitelist exceptions work\n\n curl --source-address 10.0.0.1
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)

## Should succeed\n\n## Continuous Integration (CI) Validation\n\n### GitHub Actions

Workflow\n\nBlocklists are automatically validated on every commit and pull
request using
the**validate-blocklists.yml**workflow.\n\n#### Workflow Triggers\n\nThe CI
workflow runs
when:\n\n-
Files in`etc/debvisor/`are modified\n\n-
The`.github/workflows/validate-blocklists.yml`workflow
itself is changed\n\n- Manually triggered via`workflow_dispatch`\n\n- On pull
requests
to`main`or`develop`branches\n\n- On push to`main`or`develop`branches\n\n####
Validation
Steps\n\nThe
workflow performs the following checks:\n1.**CIDR Syntax Validation**\n\n-
Verifies each
entry is
valid IPv4 or IPv6 CIDR notation\n\n- Detects invalid formats before
deployment\n\n-
Reports line
numbers for errors\n\n1.**Overlap Detection**\n\n- Identifies duplicate entries
(wasted
resources)\n\n- Warns about ranges contained in multiple files\n\n- Detects
blocklist/whitelist
conflicts\n\n1.**File Permissions Check**\n\n- Ensures files are readable by
firewall
service\n\n-
Verifies validation script is executable\n\n- Checks file modes and
ownership\n\n1.**Security
Pattern Scanning**\n\n- Warns if localhost/loopback addresses are blocked
(127.0.0.0/8,
::1/128)\n\n- Detects blocked RFC1918 private ranges without comments\n\n- Flags
potential
security
issues\n\n1.**Entry Statistics**\n\n- Counts entries in each file\n\n- Tracks
size changes
over
time\n\n- Generates comparison reports\n\n#### Using CI Validation in
PRs\n\nWhen you open
a pull
request modifying blocklists:\n ? Blocklist Validation passed\n\n-
blocklist-example.txt:
Passed
(1,250 entries)\n\n- blocklist-whitelist-example.txt: Passed (45 entries)\n\n-
No overlaps
detected\n\n- All entries valid CIDR format\n\nIf validation fails:\n ?
Blocklist
Validation
failed\n\n- blocklist-example.txt: Failed\n\n Line 42: Invalid CIDR syntax
"192.168.1.0/33"\n\n-
Overlap detected: 10.0.0.0/8 in both blocklist and whitelist\n\n#### Artifacts
and
Reports\n\nAfter
workflow completion, detailed reports are available:\n\n-
**blocklist-validation-reports/**artifact
contains:\n\n-`summary.md`- Validation summary with pass/fail
status\n\n-`etc*debvisor**.json`-
Detailed validation output per file\n\n-`etc*debvisor**.log`- Error logs and
warnings\n\n###
Validation Script Command Reference\n\nThe`validate-blocklists.sh`script can be
run
locally:\n\n##
Basic validation\n\n ./etc/debvisor/validate-blocklists.sh --blocklist
/path/to/blocklist.txt\nValidate whitelist:\n
./etc/debvisor/validate-blocklists.sh
--whitelist
/path/to/whitelist.txt\nCheck for overlaps between files:\n
./etc/debvisor/validate-blocklists.sh
\\n\n - -blocklist blocklist-example.txt \\n\n - -whitelist
blocklist-whitelist-example.txt \\n\n -
-check-overlaps\n\nVerbose output (debugging):\n
./etc/debvisor/validate-blocklists.sh
--blocklist
blocklist-example.txt --verbose\nMachine-readable JSON output:\n
./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt
--json\n\n##
Pre-Deployment
Checks\n\nBefore merging blocklist changes:\n\n## 1. Run full validation
suite\n\n bash
etc/debvisor/validate-blocklists.sh \\n\n - -blocklist
etc/debvisor/blocklist-example.txt
\\n\n -
-whitelist etc/debvisor/blocklist-whitelist-example.txt \\n\n - -check-overlaps
\\n\n -
-verbose\n\nReview changes:\n git diff etc/debvisor/\nCheck file stats:\n wc -l
etc/debvisor/blocklist*.txt\nVerify no emergency access blocks:\n grep -i
"emergency\|backup\|oob"
etc/debvisor/blocklist-example.txt\n\n## Customizing CI Validation\n\nTo modify
CI
behavior,
edit`.github/workflows/validate-blocklists.yml`:\n\n## Change validation
schedule\n\n-
cron: '0 2
***' # Run daily at 2 AM UTC\n\n## Add additional validation steps\n\n- name:
Custom
Validation\n\n
run: |\n\n## Your custom checks here\n\n## Ansible Deployment\n\n###
Variables\n\nThe
`debvisor-blocklist`Ansible role manages blocklist deployment with the following
variables:\n\n####
Required Variables\n\n-**`debvisor_blocklist_enabled`**(bool,
default:`true`)\n\n- Enable
or disable
blocklist filtering on target hosts\n\n- Set to`false`to skip all blocking
rules\n\n-
**`debvisor_blocklist_sources`**(list)\n\n- List of blocklist file paths to copy
to target
systems\n\n- Example:`['/path/to/blocklist-example.txt',
'/path/to/blocklist-malware.txt']`\n\n-
Must contain at least one entry when blocklist is enabled\n\n-
**`debvisor_whitelist_sources`**(list)\n\n- List of whitelist file paths to copy
to target
systems\n\n- Example: `['/path/to/blocklist-whitelist-example.txt']`\n\n-
Whitelist
entries override
blocklist entries\n\n#### Optional Variables\n\n-
**`debvisor_blocklist_dir`**(string,
default:`/etc/debvisor`)\n\n- Target directory where blocklists are deployed on
remote
hosts\n\n####
Per-Host Overrides\n\nYou can override variables per host in your Ansible
inventory:\n
[firewall_hosts]\n fw1.example.com debvisor_blocklist_enabled=true
debvisor_blocklist_sources="['blocklist-production.txt']"\n fw2.example.com
debvisor_blocklist_enabled=true
debvisor_blocklist_sources="['blocklist-lab.txt']"\n
staging.example.com debvisor_blocklist_enabled=false\n\n### Example Playbook:
Deploy
Blocklists\n\n-
--\n\n- name: Deploy DebVisor Blocklists\n\n hosts: firewall_hosts\n become:
yes\n
roles:\n\n- role:
debvisor-blocklist\n\n vars:\n debvisor_blocklist_enabled: true\n
debvisor_blocklist_sources:\n\n-
"{{ playbook_dir }}/../etc/debvisor/blocklist-example.txt"\n\n- "{{ playbook_dir
}}/../etc/debvisor/blocklist-malware.txt"\n\n debvisor_whitelist_sources:\n\n-
"{{
playbook_dir
}}/../etc/debvisor/blocklist-whitelist-example.txt"\n\n pre_tasks:\n\n- name:
Verify
Ansible
version\n\n assert:\n that:\n\n- ansible_version.full is version('2.9',
'>=')\n\n
fail_msg: "Ansible

>= 2.9 required"\n post_tasks:\n\n- name: Verify blocklists deployed\n\n stat:\n
path: "{{
debvisor_blocklist_dir }}/{{ item | basename }}"\n loop: "{{
debvisor_blocklist_sources +
debvisor_whitelist_sources }}"\n register: deployed_files\n\n- name: Report
deployment
status\n\n
debug:\n msg: |\n Blocklist Deployment Status:\n =============================\n
Host: {{
inventory_hostname }}\n Status: {{ 'ENABLED' if debvisor_blocklist_enabled else
'DISABLED'
}}\n
Blocklists: {{ debvisor_blocklist_sources | length }}\n Whitelists: {{
debvisor_whitelist_sources |
length }}\n Validation: {{ 'PASSED' if validation_result.rc | default(0) == 0
else
'FAILED'
}}\n\n### Firewall Rule Reloading\n\nAfter blocklists are deployed, firewall
rules are
automatically
reloaded via handlers in the role. The role supports multiple firewall
backends:\n\n####
nftables
(Recommended)\n\n## Reload all rules\n\n nft flush ruleset && nft -f
/etc/debvisor/firewall.nft\n\n## Validate rules are loaded\n\n nft list ruleset
| head
-20\n\n##
iptables (IPv4) + ip6tables (IPv6)\n\n## IPv4 rules [2]\n\n iptables-restore -n
100k | ~128 MB| ~150 ?s | Definitely segment; consider specialized rule
engines
|\n\n#### Memory Footprint Calculation\n\n Estimated Memory = Entry Count ? 128 bytes (per rule)\n
Example:\n\n- 10,000 entries ? 128 bytes = 1.28 MB\n\n- 50,000 entries ? 128
bytes = 6.4
MB\n\n-
100,000 entries ? 128 bytes = 12.8 MB\n\n### Segmentation Strategies\n\nFor
large
blocklists (> 30k
entries), organize by category:\n\n## Split blocklist by threat category\n\n
blocklist-malware.txt #
High-confidence malicious IPs\n blocklist-p2p.txt # P2P and torrenting
networks\n
blocklist-geoip.txt # Geographic restrictions\n blocklist-cloud-abuse.txt #
Abusive cloud
provider
ranges\n blocklist-spamhaus.txt # Email spam sources\n\n## In inventory or
group_vars\n\n
debvisor_blocklist_sources:\n\n- blocklist-malware.txt # Always load\n\n-
blocklist-p2p.txt # Load
on production\n\n- blocklist-geoip.txt # Load on production\n\n- "{{
optional_category }}"

## 

Conditional per environment\n\n## Caching Recommendations\n\nFor blocklists that
rarely
change:\n\n## Generate cache of compiled rules\n\n nft list ruleset >
/tmp/firewall-cache.nft\n\n##
Cache invalidation: regenerate cache every X days\n\n 0 2 **0
/usr/local/bin/regenerate-firewall-cache.sh\n\n## Benchmark Script\n\nCreate a
simple
benchmark to
measure firewall performance:\n #!/bin/bash\n\n## Benchmark blocklist rule
lookup
performance\n\n
ITERATIONS=100000\n TEST_IP="203.0.113.42" # Should match blocklist\n echo
"Benchmarking
firewall
lookup performance..."\n time {\n for i in $(seq 1 $ITERATIONS); do\n nft test
inet filter
input
meta protocol ip saddr $TEST_IP\n done\n }\n\n## Output shows time to perform
100k
lookups\n\n##
Divide by 100k to get per-lookup time\n\n- --\n\n## Version Control &
Updates\n\n###
Versioning
Scheme\n\nBlocklists follow semantic versioning with git commit hash:\n
MAJOR.MINOR.PATCH+g\n
Example: 1.2.3+g1a2b3c4\n\n#### Version Bump Rules\n\n-**MAJOR**: Breaking
changes (e.g.,
format
incompatibility, major performance regression)\n\n- Requires operator
acknowledgment
before
deployment\n\n- **MINOR**: New features or significant content updates (e.g.,
new threat
categories)\n\n- Safe to auto-deploy in CI/CD pipelines\n\n- **PATCH**: Bug
fixes or minor
content
corrections (e.g., typos, single entry fixes)\n\n- Safe to auto-deploy in CI/CD
pipelines\n\n###
Blocklist Metadata File\n\nEach blocklist distribution includes
`blocklist-metadata.json`:\n {\n
"version": "1.0.0+g1a2b3c4",\n "last_updated": "2025-11-26T14:30:00Z",\n
"blocklists": {\n
"blocklist-example.txt": {\n "description": "Example blocklist with...",\n
"sources":
["Internal
feed", "OSINT sources"],\n "sha256": "abc123def456...",\n "entry_count": 143,\n
"applicable_versions": ["2.0.0", "2.1.0"],\n "caveats": ["IPv6 link-local
caution",
"Multicast
impact"]\n }\n }\n }\nThe metadata file documents:\n\n- Blocklist sources and
origins\n\n-
Update
timestamps for freshness awareness\n\n- SHA256 checksums for integrity
verification\n\n-
Entry
counts and categorization\n\n- Applicable DebVisor versions\n\n- Known
limitations and
caveats\n\n### Automated Update Workflow\n\nCI/CD job to check for upstream
blocklist
updates:\n\n-
--\n\n## .github/workflows/blocklist-auto-update.yml\n\n name: Check Blocklist
Updates\n
on:\n
schedule:\n\n- cron: '0 6 ***' # Daily at 6 AM UTC\n\n jobs:\n check-updates:\n
runs-on:
ubuntu-latest\n steps:\n\n- uses: actions/checkout@v3\n\n- name: Check upstream
blocklists\n\n run:
|\n ./scripts/check-blocklist-updates.sh\n\n- name: Create PR if changes detected\n\n if:
steps.check.outputs.updates_found == 'true'\n uses:
peter-evans/create-pull-request@v4\n
with:\n
commit-message: "Update: Blocklists auto-updated from upstream sources"\n title:
"Auto-update:
Blocklists (PATCH v${{ steps.check.outputs.new_version }})"\n body: |\n\n###
Upstream
Blocklist
Updates Detected\n\n- Old version: ${{ steps.check.outputs.old_version }}\n\n-
New
version: ${{
steps.check.outputs.new_version }}\n\n- Changes: ${{
steps.check.outputs.change_summary
}}\n\n
Validation result: ${{ steps.validate.outputs.result }}\n\n- --\n\n## Security
Standards
and Best
Practices\n\n### Risks of External Blocklists\n\n#### Typosquatting\n\nEnsure
blocklist
URLs are
correct:\n\n## Bad\n\n
[https://example.com/blocklist.txt]([https://example.com/blocklist.tx]([https://example.com/blocklist.t]([https://example.com/blocklist.]([https://example.com/blocklist]([https://example.com/blocklis]([https://example.com/blockli]([https://example.com/blockl]([https://example.com/block]([https://example.com/bloc]([https://example.com/blo]([https://example.com/bl]([https://example.com/b]([https://example.com/]([https://example.com]([https://example.co]([https://example.c]([https://example.]([https://example]([https://exampl]([https://examp]([https://exam]([https://exa]([https://ex]([https://e](https://e)x)a)m)p)l)e).)c)o)m)/)b)l)o)c)k)l)i)s)t).)t)x)t)

## Could be typosquatted\n

[https://example.txt/blocklist]([https://example.txt/blocklis]([https://example.txt/blockli]([https://example.txt/blockl]([https://example.txt/block]([https://example.txt/bloc]([https://example.txt/blo]([https://example.txt/bl]([https://example.txt/b]([https://example.txt/]([https://example.txt]([https://example.tx]([https://example.t]([https://example.]([https://example]([https://exampl]([https://examp]([https://exam]([https://exa]([https://ex]([https://e](https://e)x)a)m)p)l)e).)t)x)t)/)b)l)o)c)k)l)i)s)t)

## Non-standard domain\n\n## Good\n\n

[https://blocklists.example.com/v1.0/malware.txt]([https://blocklists.example.com/v1.0/malware.tx]([https://blocklists.example.com/v1.0/malware.t]([https://blocklists.example.com/v1.0/malware.]([https://blocklists.example.com/v1.0/malware]([https://blocklists.example.com/v1.0/malwar]([https://blocklists.example.com/v1.0/malwa]([https://blocklists.example.com/v1.0/malw]([https://blocklists.example.com/v1.0/mal]([https://blocklists.example.com/v1.0/ma]([https://blocklists.example.com/v1.0/m]([https://blocklists.example.com/v1.0/]([https://blocklists.example.com/v1.0]([https://blocklists.example.com/v1.]([https://blocklists.example.com/v1]([https://blocklists.example.com/v]([https://blocklists.example.com/]([https://blocklists.example.com]([https://blocklists.example.co]([https://blocklists.example.c]([https://blocklists.example.]([https://blocklists.example]([https://blocklists.exampl]([https://blocklists.examp]([https://blocklists.exam]([https://blocklists.exa]([https://blocklists.ex]([https://blocklists.e]([https://blocklists.]([https://blocklists]([https://blocklist]([https://blocklis]([https://blockli]([https://blockl]([https://block]([https://bloc]([https://blo]([https://bl]([https://b](https://b)l)o)c)k)l)i)s)t)s).)e)x)a)m)p)l)e).)c)o)m)/)v)1).)0)/)m)a)l)w)a)r)e).)t)x)t)

## Clear version path\n

[https://osint.example.org/ipv4/c2.txt]([https://osint.example.org/ipv4/c2.tx]([https://osint.example.org/ipv4/c2.t]([https://osint.example.org/ipv4/c2.]([https://osint.example.org/ipv4/c2]([https://osint.example.org/ipv4/c]([https://osint.example.org/ipv4/]([https://osint.example.org/ipv4]([https://osint.example.org/ipv]([https://osint.example.org/ip]([https://osint.example.org/i]([https://osint.example.org/]([https://osint.example.org]([https://osint.example.or]([https://osint.example.o]([https://osint.example.]([https://osint.example]([https://osint.exampl]([https://osint.examp]([https://osint.exam]([https://osint.exa]([https://osint.ex]([https://osint.e]([https://osint.]([https://osint]([https://osin]([https://osi]([https://os]([https://o](https://o)s)i)n)t).)e)x)a)m)p)l)e).)o)r)g)/)i)p)v)4)/)c)2).)t)x)t)

## Explicit path\n\n## Supply Chain Verification\n\nVerify blocklist source

authenticity:\n\n## Check

GPG signature\n\n gpg --verify blocklist-example.txt.asc
blocklist-example.txt\n\n##
Import trusted
key (once)\n\n gpg --import trusted-key.asc\n\n## Verify within playbook\n\n-
name: Verify
blocklist
GPG signature\n\n ansible.builtin.command:\n cmd: gpg --verify
blocklist-example.txt.asc
blocklist-example.txt\n register: gpg_result\n failed_when: gpg_result.rc !=
0\n\n##
Denial-of-Service via Blocklist\n\nVery large blocklists can impact
performance:\n\n##
Estimate
impact before deployment\n\n wc -l blocklist-test.txt # Count entries\n ls -lh
blocklist-test.txt #
Check size\n\n## Test in staging first\n\n ansible-playbook deploy-blocklist.yml
\\n\n -
-limit
staging_firewall \\n\n - -check \\n\n - -diff\n\n## Checksum Verification and
Integrity\n\nCompute
and verify SHA256 checksums:\n\n## Generate checksums for distribution\n\n
sha256sum
/etc/debvisor/blocklist*.txt > CHECKSUMS.SHA256\n\n## Verify on deployment
[2]\n\n
verify-blocklist-integrity.sh \\n\n - -blocklist
/etc/debvisor/blocklist-example.txt \\n\n

- -sha256
abc123def456... \\n\n - -abort-on-failure\n\nThe
`verify-blocklist-integrity.sh`script
automates
validation:\n\n## Verify single file with explicit hash\n\n
./etc/debvisor/verify-blocklist-integrity.sh \\n\n - -blocklist
blocklist-example.txt
\\n\n -
-sha256 abc123def456... \\n\n - -verbose\n\n## Verify using metadata file\n\n
./etc/debvisor/verify-blocklist-integrity.sh \\n\n - -metadata
blocklist-metadata.json
\\n\n -
-abort-on-failure\n\n## Compute hash for new file\n\n
./etc/debvisor/verify-blocklist-integrity.sh
\\n\n - -blocklist new-blocklist.txt\n\n## Rollback Procedures\n\nIf a blocklist
causes
issues:\n\n### Quick Disable\n\n## Temporarily disable blocklists (no rules
loaded)\n\n
sudo
systemctl stop nftables\n\n## or\n\n sudo iptables -F # Flush all rules
(WARNING: removes
ALL
rules)\n\n## Graceful Rollback\n\n## Using Ansible\n\n ansible-playbook
deploy-blocklist.yml \\n\n -
-extra-vars "debvisor_blocklist_enabled=false"\n\n## This disables filtering
while keeping
config
files intact\n\n## Restore Previous Version [2]\n\n## Blocklists are backed up
on
deployment\n\n ls
-la /etc/debvisor/blocklist-example.txt*\n\n## Restore from backup\n\n sudo cp
/etc/debvisor/blocklist-example.txt.backup /etc/debvisor/blocklist-example.txt\n
sudo
systemctl
restart nftables\n\n## Capture Before/After State\n\n## Before deployment\n\n
sudo nft
list ruleset

> /tmp/firewall-before.nft\n sudo iptables-save > /tmp/iptables-before.rules\n
sudo
ip6tables-save >
/tmp/ip6tables-before.rules\n\n## After deployment - if issues, compare\n\n diff
/tmp/firewall-before.nft /tmp/firewall-after.nft | head -50\n\n- --\n\n##
Troubleshooting\n\n###
Validation Errors\n\n-*Problem**: "Invalid CIDR syntax in
blocklist-example.txt:42"\n\n-
*Solution**:\n\n## Check line 42\n\n sed -n '42p'
/etc/debvisor/blocklist-example.txt\n\n## Validate
CIDR format\n\n python3 -c "from ipaddress import ip_network;
ip_network('192.168.1.0/24')"\n\n##
Performance Issues\n\n- *Problem**: Firewall is slow after enabling
blocklists\n\n-
*Solution**:\n\n## Profile firewall performance\n\n nft -e list ruleset | wc -l

## Count

rules\n\n##
Segment blocklists by category\n\n## Measure before/after\n\n time curl
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)\n\n##
Traffic Unexpectedly Blocked\n\n- *Problem**: Legitimate traffic is being
dropped\n\n-
*Solution**:\n\n## Check blocklist for source IP\n\n grep -E
"203\.0\.113\.(1|2|3)"
/etc/debvisor/blocklist-*.txt\n\n## Verify whitelist\n\n grep -E
"203\.0\.113\.(1|2|3)"
/etc/debvisor/blocklist-whitelist-*.txt\n\n## Temporarily disable and test\n\n
sudo nft
flush
ruleset\n curl --source-address 203.0.113.1
[https://internal.example.com]([https://internal.example.co]([https://internal.example.c]([https://internal.example.]([https://internal.example]([https://internal.exampl]([https://internal.examp]([https://internal.exam]([https://internal.exa]([https://internal.ex]([https://internal.e]([https://internal.]([https://internal]([https://interna]([https://intern]([https://inter]([https://inte]([https://int]([https://in]([https://i](https://i)n)t)e)r)n)a)l).)e)x)a)m)p)l)e).)c)o)m)\n\n##
Overlapping Ranges\n\n- *Problem**: Multiple rules for the same IP (performance
issue)\n\n-
*Solution**:\n\n## Find overlaps\n\n ./etc/debvisor/validate-blocklists.sh
--check-overlaps
--verbose\n\n## Consolidate overlapping ranges\n\n## Example: 10.0.0.0/16 and
10.0.1.0/24
->
consolidate to 10.0.0.0/16\n\n## References and External Resources\n\n- [RFC
4632: IPv4
CIDR Address
Aggregation]([https://tools.ietf.org/html/rfc463]([https://tools.ietf.org/html/rfc46]([https://tools.ietf.org/html/rfc4]([https://tools.ietf.org/html/rfc]([https://tools.ietf.org/html/rf]([https://tools.ietf.org/html/r]([https://tools.ietf.org/html/]([https://tools.ietf.org/html]([https://tools.ietf.org/htm]([https://tools.ietf.org/ht]([https://tools.ietf.org/h]([https://tools.ietf.org/]([https://tools.ietf.org]([https://tools.ietf.or]([https://tools.ietf.o]([https://tools.ietf.]([https://tools.ietf]([https://tools.iet]([https://tools.ie]([https://tools.i]([https://tools.]([https://tools]([https://tool]([https://too]([https://to]([https://t](https://t)o)o)l)s).)i)e)t)f).)o)r)g)/)h)t)m)l)/)r)f)c)4)6)3)2)\n\n-
[IPv6 Address Architecture (RFC
4291)]([https://tools.ietf.org/html/rfc429]([https://tools.ietf.org/html/rfc42]([https://tools.ietf.org/html/rfc4]([https://tools.ietf.org/html/rfc]([https://tools.ietf.org/html/rf]([https://tools.ietf.org/html/r]([https://tools.ietf.org/html/]([https://tools.ietf.org/html]([https://tools.ietf.org/htm]([https://tools.ietf.org/ht]([https://tools.ietf.org/h]([https://tools.ietf.org/]([https://tools.ietf.org]([https://tools.ietf.or]([https://tools.ietf.o]([https://tools.ietf.]([https://tools.ietf]([https://tools.iet]([https://tools.ie]([https://tools.i]([https://tools.]([https://tools]([https://tool]([https://too]([https://to]([https://t](https://t)o)o)l)s).)i)e)t)f).)o)r)g)/)h)t)m)l)/)r)f)c)4)2)9)1)\n\n-
[Python ipaddress
Module]([https://docs.python.org/3/library/ipaddress.htm]([https://docs.python.org/3/library/ipaddress.ht]([https://docs.python.org/3/library/ipaddress.h]([https://docs.python.org/3/library/ipaddress.]([https://docs.python.org/3/library/ipaddress]([https://docs.python.org/3/library/ipaddres]([https://docs.python.org/3/library/ipaddre]([https://docs.python.org/3/library/ipaddr]([https://docs.python.org/3/library/ipadd]([https://docs.python.org/3/library/ipad]([https://docs.python.org/3/library/ipa]([https://docs.python.org/3/library/ip]([https://docs.python.org/3/library/i]([https://docs.python.org/3/library/]([https://docs.python.org/3/library]([https://docs.python.org/3/librar]([https://docs.python.org/3/libra]([https://docs.python.org/3/libr]([https://docs.python.org/3/lib]([https://docs.python.org/3/li]([https://docs.python.org/3/l]([https://docs.python.org/3/]([https://docs.python.org/3]([https://docs.python.org/]([https://docs.python.org]([https://docs.python.or]([https://docs.python.o]([https://docs.python.]([https://docs.python]([https://docs.pytho]([https://docs.pyth]([https://docs.pyt]([https://docs.py]([https://docs.p]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)p)y)t)h)o)n).)o)r)g)/)3)/)l)i)b)r)a)r)y)/)i)p)a)d)d)r)e)s)s).)h)t)m)l)\n\n-
[nftables
Documentation]([https://wiki.nftables.org]([https://wiki.nftables.or]([https://wiki.nftables.o]([https://wiki.nftables.]([https://wiki.nftables]([https://wiki.nftable]([https://wiki.nftabl]([https://wiki.nftab]([https://wiki.nfta]([https://wiki.nft]([https://wiki.nf]([https://wiki.n]([https://wiki.]([https://wiki]([https://wik]([https://wi]([https://w](https://w)i)k)i).)n)f)t)a)b)l)e)s).)o)r)g)/)\n\n-
[IANA Special-Use IPv4
Addresses]([https://www.iana.org/assignments/iana-ipv4-special-registry]([https://www.iana.org/assignments/iana-ipv4-special-registr]([https://www.iana.org/assignments/iana-ipv4-special-regist]([https://www.iana.org/assignments/iana-ipv4-special-regis]([https://www.iana.org/assignments/iana-ipv4-special-regi]([https://www.iana.org/assignments/iana-ipv4-special-reg]([https://www.iana.org/assignments/iana-ipv4-special-re]([https://www.iana.org/assignments/iana-ipv4-special-r]([https://www.iana.org/assignments/iana-ipv4-special-]([https://www.iana.org/assignments/iana-ipv4-special]([https://www.iana.org/assignments/iana-ipv4-specia]([https://www.iana.org/assignments/iana-ipv4-speci]([https://www.iana.org/assignments/iana-ipv4-spec]([https://www.iana.org/assignments/iana-ipv4-spe]([https://www.iana.org/assignments/iana-ipv4-sp]([https://www.iana.org/assignments/iana-ipv4-s]([https://www.iana.org/assignments/iana-ipv4-]([https://www.iana.org/assignments/iana-ipv4]([https://www.iana.org/assignments/iana-ipv]([https://www.iana.org/assignments/iana-ip]([https://www.iana.org/assignments/iana-i]([https://www.iana.org/assignments/iana-]([https://www.iana.org/assignments/iana]([https://www.iana.org/assignments/ian]([https://www.iana.org/assignments/ia]([https://www.iana.org/assignments/i]([https://www.iana.org/assignments/]([https://www.iana.org/assignments]([https://www.iana.org/assignment]([https://www.iana.org/assignmen]([https://www.iana.org/assignme]([https://www.iana.org/assignm]([https://www.iana.org/assign]([https://www.iana.org/assig]([https://www.iana.org/assi]([https://www.iana.org/ass]([https://www.iana.org/as]([https://www.iana.org/a]([https://www.iana.org/]([https://www.iana.org]([https://www.iana.or]([https://www.iana.o]([https://www.iana.]([https://www.iana]([https://www.ian]([https://www.ia]([https://www.i]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)i)a)n)a).)o)r)g)/)a)s)s)i)g)n)m)e)n)t)s)/)i)a)n)a)-)i)p)v)4)-)s)p)e)c)i)a)l)-)r)e)g)i)s)t)r)y)/)\n\n##
Support and Questions\n\nFor questions about blocklist deployment:\n\n-
Check`docs/networking.md`for
network configuration details\n\n- Review Ansible playbook
at`opt/ansible/playbooks/deploy-blocklist.yml`\n\n- Check system logs: `sudo
journalctl -u
debvisor-firewall`\n\n- Run validation script:
`./etc/debvisor/validate-blocklists.sh
--verbose`\n\n
