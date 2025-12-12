# DebVisor Blocklist Configuration

This directory contains IP/CIDR blocklists and whitelists used for network security filtering in DebVisor deployments.
## Purpose
Blocklists provide a way to deny traffic from or to specific IP address ranges, while whitelists allow exceptions to blocking rules. They are used to:

- Block known malicious IP ranges and attackers

- Restrict access to internal networks from untrusted sources

- Allow critical infrastructure exceptions to blocking rules

- Enforce network security policies across the cluster
## File Format Specification
### Basic Rules
- **One entry per line**: Each CIDR block or IP address occupies its own line

- **Comments**: Lines starting with `#` are ignored

- **Blank lines**: Empty lines are ignored and can be used for readability

- **Inline comments**: Comments after entries are supported (e.g., `10.0.0.0/8 # Private RFC1918`)

- **Trailing whitespace**: Automatically trimmed
### Supported Format Specifications
#### IPv4 CIDR Notation
Standard IPv4 CIDR notation with network prefix length:
    192.168.1.0/24
    10.0.0.0/8
    172.16.0.0/12
#### IPv6 CIDR Notation
IPv6 CIDR notation for IPv6 network blocks:
    2001:db8::/32
    fe80::/10
    ff00::/8
#### Single IP Addresses
Individual IPv4 or IPv6 addresses (treated as /32 and /128 respectively):
    10.0.0.1
    192.168.1.100
    2001:db8::1
#### Inline Comments
Comments can follow entries on the same line:
    10.0.0.0/8 # Private RFC1918 network
    192.168.0.0/16 # Private network range
    172.16.0.0/12 # Private network range
    203.0.113.0/24 # TEST-NET-3 (documentation)
### IPv6-Specific Considerations
IPv6 blocklists require careful handling due to the expanded address space and special address ranges. This section documents IPv6-specific behaviors and best practices.
#### IPv6 Address Categories
### Global Unicast Addresses (2000::/3)
These are routable IPv6 addresses equivalent to IPv4 public addresses. Block or allow as you would IPv4 ranges.
## Example: Malicious actor IPv6 range (documentation)
    2001:db8:cafe::/48 # Global unicast prefix
## Example: Cloud provider IPv6 range
    2600:1f00::/32 # Major cloud provider (example)
## Unique Local Addresses (fc00::/7)
IPv6 equivalent of RFC1918 private ranges. Typically whitelisted internally.
## Internal organizational networks
    fc00:1234::/32 # Organization A internal network
    fc00:5678::/32 # Organization B internal network
    fd00:1111::/32 # Department-specific ULA (documentation format)
## Link-Local Addresses (fe80::/10)
Used for direct communication between nodes on the same link. Rarely blocked but may be whitelisted for specific security zones.
## Typically DO NOT block link-local in cluster environments
## fe80::/10     # All link-local (usually safe)
## But may whitelist if blocking all IPv6
    fe80::/10      # Allow cluster heartbeats
## Multicast Addresses (ff00::/8)
Reserved for multicast traffic. Blocking depends on use case (mDNS, neighbor discovery, etc.).
## Example: Restrict multicast to trusted sources only
    ff00::/8       # All multicast (typically blocked or restricted)
    ff02::1        # All nodes link-local multicast (for ND)
    ff02::2        # All routers link-local multicast (for RA)
## Loopback and Unspecified (::1/128, ::/128)
IPv6 loopback equivalent to 127.0.0.1. Should almost never be blocked.
## NEVER BLOCK in production
## ::1/128        # IPv6 loopback (critical infrastructure)
## ::/128         # Unspecified address (internal use)
## Documentation Prefix (2001:db8::/32)
Reserved for documentation and examples. Safe to use in labs/tests.
## Example ranges (documentation only)
    2001:db8:bad::/48     # Malicious range (example)
    2001:db8:cafe::/48    # Partner network (example)
    2001:db8:test::/48    # Test range (example)
## Dual-Stack Considerations
When operating with both IPv4 and IPv6:
1.**Independent Filtering**: IPv4 and IPv6 are filtered separately. A blocked IPv4 range does NOT automatically block its IPv6 equivalent.
1.**Dual Entries**: For comprehensive filtering, add both IPv4 and IPv6 entries:
## Block both IPv4 and IPv6 for the same actor
    203.0.113.0/24        # Malicious IPv4 range
    2001:db8:bad::/48     # Same actor's IPv6 range
1.**IPv4-Mapped IPv6 Addresses**: Some systems use `::ffff:192.0.2.0/120` to represent IPv4 addresses in IPv6 format. Decide whether to block both or just one.
## IPv4 blocklist entry
    192.0.2.0/24
## IPv6-mapped version (optional, for defense-in-depth)
    ::ffff:192.0.2.0/120
1.**Dual-Stack Testing**: When validating, test both IPv4 and IPv6 traffic:
## Test IPv4 traffic from blocked range
    curl --ipv4 --source-address 203.0.113.1 [https://internal.example.com](https://internal.example.com)
## Test IPv6 traffic from blocked range
    curl --ipv6 --source-address 2001:db8:bad::1 [https://internal.example.com](https://internal.example.com)
## Test via DNS (may resolve to either)
    curl [https://internal.example.com](https://internal.example.com)
## IPv6 Validation with validate-blocklists.sh
The validation script automatically detects and validates both IPv4 and IPv6 entries:
## Validate mixed IPv4/IPv6 blocklist
    ./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt --verbose
Check for IPv6-specific issues:
    ./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt --json | grep -E '"address_family".*"IPv6"'
Output will show:

- Total entries (IPv4 + IPv6)

- IPv4 entry count

- IPv6 entry count

- Any validation errors with address family
## IPv6 in Firewall Rules
Different firewall backends handle IPv6 differently:

- *nftables**:
## IPv4 rules
    nft add rule filter input ip saddr 203.0.113.0/24 drop
## IPv6 rules (separate)
    nft add rule filter input ip6 saddr 2001:db8:bad::/48 drop

- *iptables vs ip6tables**:
## IPv4 rules use iptables
    iptables -A INPUT -s 203.0.113.0/24 -j DROP
## IPv6 rules use separate ip6tables command
    ip6tables -A INPUT -s 2001:db8:bad::/48 -j DROP
Ansible playbooks should handle both:

- name: Block IPv4 range
      iptables:
        chain: INPUT
        source: 203.0.113.0/24
        jump: DROP

- name: Block IPv6 range
      ip6tables:
        chain: INPUT
        source: 2001:db8:bad::/48
        jump: DROP
## blocklist-example.txt
The main blocklist containing entries to**deny**. Traffic matching these entries will be blocked.
Example contents:
## Known malicious ranges (example only - use real threat intelligence)
    203.0.113.0/24 # TEST-NET-3
    198.51.100.0/24 # TEST-NET-2
## Botnets and known C&C infrastructure
    198.51.100.50/32
## Tor exit nodes (if policy requires blocking)
## Note: Keep separate file if frequently updated
## blocklist-whitelist-example.txt
The whitelist containing**exceptions**to blocking rules. Entries here are allowed even if they match blocking rules.
Example contents:
## Critical infrastructure that must bypass blocklist
    10.0.0.1/32 # Primary DNS server
    10.0.0.2/32 # Secondary DNS server
    203.0.113.100/32 # Trusted partner gateway
## Internal networks that should not be blocked
    10.0.0.0/8 # Internal RFC1918
    172.16.0.0/12 # Internal RFC1918
    192.168.0.0/16 # Internal RFC1918
## Common Use Cases
### Internal Networks
Allow internal networks through whitelisting:
    10.0.0.0/8 # Class A private
    172.16.0.0/12 # Class B private
    192.168.0.0/16 # Class C private
    fc00::/7 # IPv6 Unique Local Addresses (ULA)
### Known Malicious IPs
Block ranges from threat intelligence feeds:
## Example: Botnet ranges
    203.0.113.0/24
    198.51.100.0/24
## Example: Known attack infrastructure
    192.0.2.0/24
## Gateway/Load Balancer Access
Whitelist gateways and load balancers that should bypass filters:
    10.1.1.1/32 # Primary gateway
    10.1.1.2/32 # Secondary gateway
    10.2.0.0/16 # Load balancer pool
### Multicast and Special Ranges
Block or allow multicast and special-use ranges:
## Multicast (typically blocked)
    224.0.0.0/4
## Link-local (IPv6)
    fe80::/10
## Loopback (typically whitelisted for localhost)
    127.0.0.1/8
    ::1/128
## Difference Between Blocklist and Whitelist
| Aspect | Blocklist | Whitelist |
|--------|-----------|-----------|
|**Purpose**| Deny traffic | Allow exceptions |
|**Effect**| Drops/rejects traffic from blocked ranges | Permits traffic from whitelisted ranges |
|**Override**| Whitelist entries override blocklist | Takes precedence over blocklist |
|**File**| `blocklist-example.txt`|`blocklist-whitelist-example.txt` |
|**Use case**| Block malicious/untrusted IPs | Permit critical infrastructure |
### Processing Order
1.**Whitelist check first**: If an IP is in the whitelist, traffic is allowed (fastest path)
1.**Blocklist check**: If not whitelisted, check against blocklist
1.**Default policy**: Allow (if not in blocklist)
## Integration with DebVisor Systems
### Firewall Integration Points
Blocklists are consumed by the firewall at:

- **nftables rules**(`/etc/nftables.d/debvisor-blocklist.nft`)

- **iptables rules**(if using legacy iptables)

- **Cloud provider security groups**(if applicable)
### Ansible Integration
DebVisor Ansible variables for deploying blocklists:
## Enable/disable blocklist filtering globally
    debvisor_blocklist_enabled: true
## Paths to blocklist files (can be multiple)
    debvisor_blocklist_sources:

- /etc/debvisor/blocklist-example.txt

- /etc/debvisor/blocklist-malware.txt

- /etc/debvisor/blocklist-p2p.txt
## Paths to whitelist files
    debvisor_whitelist_sources:

- /etc/debvisor/blocklist-whitelist-example.txt

- /etc/debvisor/whitelist-internal-infrastructure.txt
## Reload firewall after applying lists
    debvisor_blocklist_reload_firewall: true
## DNS Integration
Blocklists can also be used for DNS filtering:

- DNS queries from blocked ranges are rejected

- Queries for blocked domains are filtered

- Whitelist entries receive fast-track DNS responses
## Performance Considerations
### Blocklist Size Guidelines
| Size | Impact | Recommendation |
|------|--------|-----------------|
| < 10k entries | Minimal | Safe for most environments |
| 10k - 50k entries | Low impact | Monitor firewall performance |
| 50k - 100k entries | Moderate impact | Consider segmentation |
| > 100k entries | Significant | Requires optimization/tuning |
### Memory Footprint
Approximate memory usage for firewall rules:

- nftables: ~10-100 bytes per rule (depending on complexity)

- iptables: ~50-200 bytes per rule

- Example: 50k rules ? 5-10 MB memory
### Performance Optimization Strategies
#### Segmentation
Split large blocklists by category:
    blocklist-malware.txt # Known malicious IPs
    blocklist-p2p.txt # Peer-to-peer networks
    blocklist-botnets.txt # Botnet infrastructure
    blocklist-scanners.txt # Known network scanners
Load only needed categories per environment:
    debvisor_blocklist_sources:

- /etc/debvisor/blocklist-malware.txt # Always load

- /etc/debvisor/blocklist-p2p.txt # Load in restrictive environments
#### Tiered Blocking
Implement priority levels:
## Critical blocks (evaluated first)
    203.0.113.0/24
## Warning-only blocks (logged but may be allowed)
    198.51.100.0/24 # Monitored but not blocked
## Caching
For static blocklists:
## Cache blocklist in memory with TTL
    debvisor_blocklist_cache_ttl: 3600 # seconds
## Re-validate periodically
    debvisor_blocklist_validation_interval: 86400 # daily
## Benchmarking
Test performance impact in your environment:
## Benchmark script (example)
    ./etc/debvisor/benchmark-blocklist.sh \

      - -blocklist /etc/debvisor/blocklist-example.txt \

      - -packets 100000 \

      - -output /tmp/benchmark-results.json
## Version Control and Updates
### Versioning
Blocklists are versioned using:
## Version format: YYYY-MM-DD-HHMMSS
    2025-11-26-143022
## Or semantic versioning
    v1.2.3
## Metadata File
`blocklist-metadata.json` tracks:
    {
      "blocklist_version": "2025-11-26-143022",
      "blocklist_count": 1250,
      "whitelist_count": 45,
      "sources": [
        {
          "name": "malware",
          "url": "[https://threatintel.example.com/malware.txt",](https://threatintel.example.com/malware.txt",)
          "updated": "2025-11-26T14:30:22Z",
          "sha256": "abc123..."
        }
      ],
      "caveats": [
        "Malware list is 2 days old; recommend daily refresh",
        "Tor exit nodes list may be incomplete"
      ],
      "applicable_versions": [
        "bookworm",
        "trixie"
      ]
    }
### Automated Updates
Enable automated blocklist updates:
## Scheduled CI job (example with GitHub Actions)
- cron: '0 2 ** *' # Daily at 2 AM UTC
## Tasks
## 1. Check upstream for updates
## 2. Validate syntax and ranges
## 3. Detect anomalies (size changes, new sources)
## 4. Create PR with changes
## 5. Notify operators
## Security Considerations
### Supply Chain Security
- **Verify sources**: Ensure blocklist URLs are correct (typosquatting risk)

- **GPG signatures**: Verify GPG signatures if available from upstream

- **HTTPS only**: Always fetch blocklists over HTTPS

- **Checksums**: Compare SHA256 against known-good values
### Integrity Checking
## Generate and store checksums
    sha256sum /etc/debvisor/blocklist-example.txt > /etc/debvisor/blocklist-example.txt.sha256
## Verify on deployment
    sha256sum -c /etc/debvisor/blocklist-example.txt.sha256
## Denial-of-Service Risks
- Very large blocklists can consume memory/CPU

- Overlapping ranges waste resources

- Frequent updates can cause firewall reload storms
### Rollback Procedure
If a blocklist causes problems:
## Disable blocklist immediately
    sudo systemctl set-environment DEBVISOR_BLOCKLIST_ENABLED=false
    sudo systemctl restart nftables
## Restore previous version
    sudo cp /etc/debvisor/blocklist-example.txt.backup /etc/debvisor/blocklist-example.txt
## Capture firewall state for debugging
    sudo nft list ruleset > /tmp/firewall-before-fix.nft
    sudo nft flush ruleset
## Re-apply with older blocklist
## Testing and Validation
### Unit Testing
Test blocklist syntax and correctness:
    ./etc/debvisor/validate-blocklists.sh \

      - -blocklist /etc/debvisor/blocklist-example.txt \

      - -check-overlaps \

      - -verbose
### Integration Testing
Verify blocklists work in practice:
## Test environment deployment
    ansible-playbook opt/ansible/playbooks/deploy-blocklist.yml \

      - i inventory.test \

      - -tags blocklist
## Verify firewall rules loaded
    sudo nft list chain filter input | grep blocklist
## Test traffic from blocked IP
    curl --source-address 203.0.113.1 [https://internal.example.com](https://internal.example.com) # Should fail
## Smoke Tests
Post-deployment validation:
## 1. Verify firewall rules are active
    sudo nft list ruleset | grep -c "drop from"
## 2. Check for rule conflicts
    sudo nft validate
## 3. Monitor logs for excessive drops
    sudo journalctl -u nftables -n 100
## 4. Verify whitelist exceptions work
    curl --source-address 10.0.0.1 [https://internal.example.com](https://internal.example.com) # Should succeed
## Continuous Integration (CI) Validation
### GitHub Actions Workflow
Blocklists are automatically validated on every commit and pull request using the**validate-blocklists.yml**workflow.
#### Workflow Triggers
The CI workflow runs when:

- Files in `etc/debvisor/` are modified

- The `.github/workflows/validate-blocklists.yml` workflow itself is changed

- Manually triggered via `workflow_dispatch`

- On pull requests to `main`or`develop` branches

- On push to `main`or`develop` branches
#### Validation Steps
The workflow performs the following checks:
1.**CIDR Syntax Validation**

- Verifies each entry is valid IPv4 or IPv6 CIDR notation

- Detects invalid formats before deployment

- Reports line numbers for errors
1.**Overlap Detection**

- Identifies duplicate entries (wasted resources)

- Warns about ranges contained in multiple files

- Detects blocklist/whitelist conflicts
1.**File Permissions Check**

- Ensures files are readable by firewall service

- Verifies validation script is executable

- Checks file modes and ownership
1.**Security Pattern Scanning**

- Warns if localhost/loopback addresses are blocked (127.0.0.0/8, ::1/128)

- Detects blocked RFC1918 private ranges without comments

- Flags potential security issues
1.**Entry Statistics**

- Counts entries in each file

- Tracks size changes over time

- Generates comparison reports
#### Using CI Validation in PRs
When you open a pull request modifying blocklists:
    ? Blocklist Validation passed

- blocklist-example.txt: Passed (1,250 entries)

- blocklist-whitelist-example.txt: Passed (45 entries)

- No overlaps detected

- All entries valid CIDR format
If validation fails:
    ? Blocklist Validation failed

- blocklist-example.txt: Failed
        Line 42: Invalid CIDR syntax "192.168.1.0/33"

- Overlap detected: 10.0.0.0/8 in both blocklist and whitelist
#### Artifacts and Reports
After workflow completion, detailed reports are available:

- **blocklist-validation-reports/**artifact contains:

- `summary.md` - Validation summary with pass/fail status

- `etc_debvisor_*.json` - Detailed validation output per file

- `etc_debvisor_*.log` - Error logs and warnings
### Validation Script Command Reference
The `validate-blocklists.sh` script can be run locally:
## Basic validation
    ./etc/debvisor/validate-blocklists.sh --blocklist /path/to/blocklist.txt
Validate whitelist:
    ./etc/debvisor/validate-blocklists.sh --whitelist /path/to/whitelist.txt
Check for overlaps between files:
    ./etc/debvisor/validate-blocklists.sh \

      - -blocklist blocklist-example.txt \

      - -whitelist blocklist-whitelist-example.txt \

      - -check-overlaps
Verbose output (debugging):
    ./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt --verbose
Machine-readable JSON output:
    ./etc/debvisor/validate-blocklists.sh --blocklist blocklist-example.txt --json
## Pre-Deployment Checks
Before merging blocklist changes:
## 1. Run full validation suite
    bash etc/debvisor/validate-blocklists.sh \

      - -blocklist etc/debvisor/blocklist-example.txt \

      - -whitelist etc/debvisor/blocklist-whitelist-example.txt \

      - -check-overlaps \

      - -verbose
Review changes:
    git diff etc/debvisor/
Check file stats:
    wc -l etc/debvisor/blocklist*.txt
Verify no emergency access blocks:
    grep -i "emergency\|backup\|oob" etc/debvisor/blocklist-example.txt
## Customizing CI Validation
To modify CI behavior, edit `.github/workflows/validate-blocklists.yml`:
## Change validation schedule
- cron: '0 2 ** *'  # Run daily at 2 AM UTC
## Add additional validation steps
- name: Custom Validation
      run: |
## Your custom checks here
## Ansible Deployment
### Variables
The `debvisor-blocklist` Ansible role manages blocklist deployment with the following variables:
#### Required Variables
- **`debvisor_blocklist_enabled`**(bool, default:`true`)

- Enable or disable blocklist filtering on target hosts

- Set to `false` to skip all blocking rules

- **`debvisor_blocklist_sources`**(list)

- List of blocklist file paths to copy to target systems

- Example: `['/path/to/blocklist-example.txt', '/path/to/blocklist-malware.txt']`

- Must contain at least one entry when blocklist is enabled

- **`debvisor_whitelist_sources`**(list)

- List of whitelist file paths to copy to target systems

- Example: `['/path/to/blocklist-whitelist-example.txt']`

- Whitelist entries override blocklist entries
#### Optional Variables
- **`debvisor_blocklist_dir`**(string, default:`/etc/debvisor`)

- Target directory where blocklists are deployed on remote hosts
#### Per-Host Overrides
You can override variables per host in your Ansible inventory:
    [firewall_hosts]
    fw1.example.com debvisor_blocklist_enabled=true debvisor_blocklist_sources="['blocklist-production.txt']"
    fw2.example.com debvisor_blocklist_enabled=true debvisor_blocklist_sources="['blocklist-lab.txt']"
    staging.example.com debvisor_blocklist_enabled=false
### Example Playbook: Deploy Blocklists
- --

- name: Deploy DebVisor Blocklists
      hosts: firewall_hosts
      become: yes
      roles:

- role: debvisor-blocklist
          vars:
            debvisor_blocklist_enabled: true
            debvisor_blocklist_sources:

- "{{ playbook_dir }}/../etc/debvisor/blocklist-example.txt"

- "{{ playbook_dir }}/../etc/debvisor/blocklist-malware.txt"
            debvisor_whitelist_sources:

- "{{ playbook_dir }}/../etc/debvisor/blocklist-whitelist-example.txt"
      pre_tasks:

- name: Verify Ansible version
          assert:
            that:

- ansible_version.full is version('2.9', '>=')
            fail_msg: "Ansible >= 2.9 required"
      post_tasks:

- name: Verify blocklists deployed
          stat:
            path: "{{ debvisor_blocklist_dir }}/{{ item | basename }}"
          loop: "{{ debvisor_blocklist_sources + debvisor_whitelist_sources }}"
          register: deployed_files

- name: Report deployment status
          debug:
            msg: |
              Blocklist Deployment Status:
              =============================
              Host: {{ inventory_hostname }}
              Status: {{ 'ENABLED' if debvisor_blocklist_enabled else 'DISABLED' }}
              Blocklists: {{ debvisor_blocklist_sources | length }}
              Whitelists: {{ debvisor_whitelist_sources | length }}
              Validation: {{ 'PASSED' if validation_result.rc | default(0) == 0 else 'FAILED' }}
### Firewall Rule Reloading
After blocklists are deployed, firewall rules are automatically reloaded via handlers in the role. The role supports multiple firewall backends:
#### nftables (Recommended)
## Reload all rules
    nft flush ruleset && nft -f /etc/debvisor/firewall.nft
## Validate rules are loaded
    nft list ruleset | head -20
## iptables (IPv4) + ip6tables (IPv6)
## IPv4 rules [2]
    iptables-restore -n < /etc/debvisor/iptables.rules
## IPv6 rules
    ip6tables-restore -n < /etc/debvisor/ip6tables.rules
## Verify
    iptables -L -n | grep -i drop | wc -l
    ip6tables -L -n | grep -i drop | wc -l
## Validation After Reload
## Check firewall is active
    sudo systemctl status nftables # or iptables, depending on backend
## Verify blocklist rules are present
    sudo nft list chain filter input | grep -i drop | head -5

- --
## Performance & Scalability
### Performance Guidelines
Blocklist filtering performance depends on several factors:
#### Rule Count Impact
| Entries | Memory | Lookup Time | Recommendation |
|---------|--------|-------------|-----------------|
| < 10k   | ~1 MB  | ~50 ?s      | Minimal overhead; safe for all deployments |
| 10k-50k | ~6 MB  | ~75 ?s      | Monitor performance; consider segmentation above 30k |
| 50k-100k| ~13 MB | ~100 ?s     | Segmentation recommended; use tiered blocking |
| > 100k  | ~128 MB| ~150 ?s     | Definitely segment; consider specialized rule engines |
#### Memory Footprint Calculation
    Estimated Memory = Entry Count ? 128 bytes (per rule)
    Example:

- 10,000 entries ? 128 bytes = 1.28 MB

- 50,000 entries ? 128 bytes = 6.4 MB

- 100,000 entries ? 128 bytes = 12.8 MB
### Segmentation Strategies
For large blocklists (> 30k entries), organize by category:
## Split blocklist by threat category
    blocklist-malware.txt          # High-confidence malicious IPs
    blocklist-p2p.txt             # P2P and torrenting networks
    blocklist-geoip.txt           # Geographic restrictions
    blocklist-cloud-abuse.txt     # Abusive cloud provider ranges
    blocklist-spamhaus.txt        # Email spam sources
## In inventory or group_vars
    debvisor_blocklist_sources:

- blocklist-malware.txt           # Always load

- blocklist-p2p.txt               # Load on production

- blocklist-geoip.txt             # Load on production

- "{{ optional_category }}"       # Conditional per environment
## Caching Recommendations
For blocklists that rarely change:
## Generate cache of compiled rules
    nft list ruleset > /tmp/firewall-cache.nft
## Cache invalidation: regenerate cache every X days
    0 2 ** 0 /usr/local/bin/regenerate-firewall-cache.sh
## Benchmark Script
Create a simple benchmark to measure firewall performance:
    #!/bin/bash
## Benchmark blocklist rule lookup performance
    ITERATIONS=100000
    TEST_IP="203.0.113.42"  # Should match blocklist
    echo "Benchmarking firewall lookup performance..."
    time {
      for i in $(seq 1 $ITERATIONS); do
        nft test inet filter input meta protocol ip saddr $TEST_IP
      done
    }
## Output shows time to perform 100k lookups
## Divide by 100k to get per-lookup time
- --
## Version Control & Updates
### Versioning Scheme
Blocklists follow semantic versioning with git commit hash:
    MAJOR.MINOR.PATCH+g
    Example: 1.2.3+g1a2b3c4
#### Version Bump Rules
- **MAJOR**: Breaking changes (e.g., format incompatibility, major performance regression)

- Requires operator acknowledgment before deployment

- **MINOR**: New features or significant content updates (e.g., new threat categories)

- Safe to auto-deploy in CI/CD pipelines

- **PATCH**: Bug fixes or minor content corrections (e.g., typos, single entry fixes)

- Safe to auto-deploy in CI/CD pipelines
### Blocklist Metadata File
Each blocklist distribution includes `blocklist-metadata.json`:
    {
      "version": "1.0.0+g1a2b3c4",
      "last_updated": "2025-11-26T14:30:00Z",
      "blocklists": {
        "blocklist-example.txt": {
          "description": "Example blocklist with...",
          "sources": ["Internal feed", "OSINT sources"],
          "sha256": "abc123def456...",
          "entry_count": 143,
          "applicable_versions": ["2.0.0", "2.1.0"],
          "caveats": ["IPv6 link-local caution", "Multicast impact"]
        }
      }
    }
The metadata file documents:

- Blocklist sources and origins

- Update timestamps for freshness awareness

- SHA256 checksums for integrity verification

- Entry counts and categorization

- Applicable DebVisor versions

- Known limitations and caveats
### Automated Update Workflow
CI/CD job to check for upstream blocklist updates:

- --
## .github/workflows/blocklist-auto-update.yml
    name: Check Blocklist Updates
    on:
      schedule:

- cron: '0 6 ** *'  # Daily at 6 AM UTC
    jobs:
      check-updates:
        runs-on: ubuntu-latest
        steps:

- uses: actions/checkout@v3

- name: Check upstream blocklists
            run: |
              ./scripts/check-blocklist-updates.sh

- name: Create PR if changes detected
            if: steps.check.outputs.updates_found == 'true'
            uses: peter-evans/create-pull-request@v4
            with:
              commit-message: "Update: Blocklists auto-updated from upstream sources"
              title: "Auto-update: Blocklists (PATCH v${{ steps.check.outputs.new_version }})"
              body: |
### Upstream Blocklist Updates Detected
- Old version: ${{ steps.check.outputs.old_version }}

- New version: ${{ steps.check.outputs.new_version }}

- Changes: ${{ steps.check.outputs.change_summary }}
                Validation result: ${{ steps.validate.outputs.result }}

- --
## Security Standards and Best Practices
### Risks of External Blocklists
#### Typosquatting
Ensure blocklist URLs are correct:
## Bad
    [https://example.com/blocklist.txt](https://example.com/blocklist.txt)     # Could be typosquatted
    [https://example.txt/blocklist](https://example.txt/blocklist)        # Non-standard domain
## Good
    [https://blocklists.example.com/v1.0/malware.txt](https://blocklists.example.com/v1.0/malware.txt)  # Clear version path
    [https://osint.example.org/ipv4/c2.txt](https://osint.example.org/ipv4/c2.txt)            # Explicit path
## Supply Chain Verification
Verify blocklist source authenticity:
## Check GPG signature
    gpg --verify blocklist-example.txt.asc blocklist-example.txt
## Import trusted key (once)
    gpg --import trusted-key.asc
## Verify within playbook
- name: Verify blocklist GPG signature
      ansible.builtin.command:
        cmd: gpg --verify blocklist-example.txt.asc blocklist-example.txt
      register: gpg_result
      failed_when: gpg_result.rc != 0
## Denial-of-Service via Blocklist
Very large blocklists can impact performance:
## Estimate impact before deployment
    wc -l blocklist-test.txt           # Count entries
    ls -lh blocklist-test.txt          # Check size
## Test in staging first
    ansible-playbook deploy-blocklist.yml \

      - -limit staging_firewall \

      - -check \

      - -diff
## Checksum Verification and Integrity
Compute and verify SHA256 checksums:
## Generate checksums for distribution
    sha256sum /etc/debvisor/blocklist*.txt > CHECKSUMS.SHA256
## Verify on deployment [2]
    verify-blocklist-integrity.sh \

      - -blocklist /etc/debvisor/blocklist-example.txt \

      - -sha256 abc123def456... \

      - -abort-on-failure
The `verify-blocklist-integrity.sh` script automates validation:
## Verify single file with explicit hash
    ./etc/debvisor/verify-blocklist-integrity.sh \

      - -blocklist blocklist-example.txt \

      - -sha256 abc123def456... \

      - -verbose
## Verify using metadata file
    ./etc/debvisor/verify-blocklist-integrity.sh \

      - -metadata blocklist-metadata.json \

      - -abort-on-failure
## Compute hash for new file
    ./etc/debvisor/verify-blocklist-integrity.sh \

      - -blocklist new-blocklist.txt
## Rollback Procedures
If a blocklist causes issues:
### Quick Disable
## Temporarily disable blocklists (no rules loaded)
    sudo systemctl stop nftables
## or
    sudo iptables -F  # Flush all rules (WARNING: removes ALL rules)
## Graceful Rollback
## Using Ansible
    ansible-playbook deploy-blocklist.yml \

      - -extra-vars "debvisor_blocklist_enabled=false"
## This disables filtering while keeping config files intact
## Restore Previous Version [2]
## Blocklists are backed up on deployment
    ls -la /etc/debvisor/blocklist-example.txt*
## Restore from backup
    sudo cp /etc/debvisor/blocklist-example.txt.backup /etc/debvisor/blocklist-example.txt
    sudo systemctl restart nftables
## Capture Before/After State
## Before deployment
    sudo nft list ruleset > /tmp/firewall-before.nft
    sudo iptables-save > /tmp/iptables-before.rules
    sudo ip6tables-save > /tmp/ip6tables-before.rules
## After deployment - if issues, compare
    diff /tmp/firewall-before.nft /tmp/firewall-after.nft | head -50

- --
## Troubleshooting
### Validation Errors
- *Problem**: "Invalid CIDR syntax in blocklist-example.txt:42"

- *Solution**:
## Check line 42
    sed -n '42p' /etc/debvisor/blocklist-example.txt
## Validate CIDR format
    python3 -c "from ipaddress import ip_network; ip_network('192.168.1.0/24')"
## Performance Issues
- *Problem**: Firewall is slow after enabling blocklists

- *Solution**:
## Profile firewall performance
    nft -e list ruleset | wc -l # Count rules
## Segment blocklists by category
## Measure before/after
    time curl [https://internal.example.com](https://internal.example.com)
## Traffic Unexpectedly Blocked
- *Problem**: Legitimate traffic is being dropped

- *Solution**:
## Check blocklist for source IP
    grep -E "203\.0\.113\.(1|2|3)" /etc/debvisor/blocklist-*.txt
## Verify whitelist
    grep -E "203\.0\.113\.(1|2|3)" /etc/debvisor/blocklist-whitelist-*.txt
## Temporarily disable and test
    sudo nft flush ruleset
    curl --source-address 203.0.113.1 [https://internal.example.com](https://internal.example.com)
## Overlapping Ranges
- *Problem**: Multiple rules for the same IP (performance issue)

- *Solution**:
## Find overlaps
    ./etc/debvisor/validate-blocklists.sh --check-overlaps --verbose
## Consolidate overlapping ranges
## Example: 10.0.0.0/16 and 10.0.1.0/24 -> consolidate to 10.0.0.0/16
## References and External Resources
- [RFC 4632: IPv4 CIDR Address Aggregation](https://tools.ietf.org/html/rfc4632)

- [IPv6 Address Architecture (RFC 4291)](https://tools.ietf.org/html/rfc4291)

- [Python ipaddress Module](https://docs.python.org/3/library/ipaddress.html)

- [nftables Documentation](https://wiki.nftables.org/)

- [IANA Special-Use IPv4 Addresses](https://www.iana.org/assignments/iana-ipv4-special-registry/)
## Support and Questions
For questions about blocklist deployment:

- Check `docs/networking.md` for network configuration details

- Review Ansible playbook at `opt/ansible/playbooks/deploy-blocklist.yml`

- Check system logs: `sudo journalctl -u debvisor-firewall`

- Run validation script: `./etc/debvisor/validate-blocklists.sh --verbose`
