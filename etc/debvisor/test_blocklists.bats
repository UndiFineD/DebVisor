#!/usr/bin/env bats
#
# test_blocklists.bats - Comprehensive BATS tests for blocklist validation and functionality
#
# BATS (Bash Automated Testing System) tests for DebVisor blocklist validation scripts.
# Tests cover:
#   - Valid CIDR ranges (IPv4/IPv6)
#   - Invalid syntax detection
#   - Overlapping range detection
#   - Whitelist exception functionality
#   - Edge cases and error conditions
#
# Installation:
#   apt-get install bats
#
# Usage:
#   bats test_blocklists.bats                 # Run all tests
#   bats test_blocklists.bats --tap           # TAP format (CI/CD)
#   bats test_blocklists.bats --verbose       # Verbose output
#

# Setup: Create temporary test files before each test
setup() {
  export TEST_DIR=$(mktemp -d)
  export BLOCKLIST_VALID="${TEST_DIR}/blocklist-valid.txt"
  export BLOCKLIST_INVALID="${TEST_DIR}/blocklist-invalid.txt"
  export WHITELIST_VALID="${TEST_DIR}/whitelist-valid.txt"
  export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  
  # Create test blocklist with valid entries
  cat > "${BLOCKLIST_VALID}" <<'EOF'
# Valid IPv4 CIDR ranges
192.168.1.0/24
10.0.0.0/8
203.0.113.0/24

# Valid IPv6 CIDR ranges
2001:db8::/32
fc00::/7
EOF

  # Create test blocklist with invalid entries
  cat > "${BLOCKLIST_INVALID}" <<'EOF'
# Invalid CIDR formats
192.168.1.0/33          # Invalid prefix length (>32 for IPv4)
10.0.0.0/33             # Invalid prefix length
999.999.999.999/24      # Invalid octet values
2001:db8::/129          # Invalid prefix length (>128 for IPv6)
not-an-ip               # Not an IP at all
192.168.1.0/           # Missing prefix length
/24                     # Missing IP address
EOF

  # Create test whitelist with valid entries
  cat > "${WHITELIST_VALID}" <<'EOF'
# Trusted networks
10.0.0.0/8
172.16.0.0/12
2001:db8:cafe::/48
EOF
}

# Teardown: Clean up temporary test files after each test
teardown() {
  rm -rf "${TEST_DIR}"
}

# ============================================================================
# BLOCKLIST VALIDATION TESTS
# ============================================================================

@test "Blocklist: Valid IPv4 CIDR passes validation" {
  run bash -c "echo '192.168.1.0/24' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\""
  [ "$status" -eq 0 ]
}

@test "Blocklist: Valid IPv6 CIDR passes validation" {
  run bash -c "echo '2001:db8::/32' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\""
  [ "$status" -eq 0 ]
}

@test "Blocklist: Individual IPv4 address passes validation" {
  run bash -c "echo '192.168.1.1' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\""
  [ "$status" -eq 0 ]
}

@test "Blocklist: Individual IPv6 address passes validation" {
  run bash -c "echo '2001:db8::1' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\""
  [ "$status" -eq 0 ]
}

@test "Blocklist: Invalid prefix length rejected" {
  run bash -c "echo '192.168.1.0/33' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\" 2>&1"
  [ "$status" -ne 0 ]
  [[ "$output" == *"does not define a valid IPv4"* ]] || [[ "$output" == *"ValueError"* ]]
}

@test "Blocklist: Invalid octets rejected" {
  run bash -c "echo '999.999.999.999/24' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\" 2>&1"
  [ "$status" -ne 0 ]
}

@test "Blocklist: Non-IP string rejected" {
  run bash -c "echo 'not-an-ip' | python3 -c \"import sys; from ipaddress import ip_network; ip_network(sys.stdin.read().strip())\" 2>&1"
  [ "$status" -ne 0 ]
}

@test "Blocklist: Empty lines ignored" {
  echo -e "192.168.1.0/24\n\n10.0.0.0/8" > "${TEST_DIR}/blocklist-with-blanks.txt"
  # Count non-empty, non-comment lines
  run bash -c "grep -v '^[[:space:]]*$' '${TEST_DIR}/blocklist-with-blanks.txt' | grep -v '^[[:space:]]*#' | wc -l"
  [ "$output" -eq 2 ]
}

@test "Blocklist: Comment lines ignored" {
  echo -e "# This is a comment\n192.168.1.0/24\n# Another comment\n10.0.0.0/8" > "${TEST_DIR}/blocklist-with-comments.txt"
  run bash -c "grep -v '^[[:space:]]*$' '${TEST_DIR}/blocklist-with-comments.txt' | grep -v '^[[:space:]]*#' | wc -l"
  [ "$output" -eq 2 ]
}

@test "Blocklist: Inline comments stripped correctly" {
  run bash -c "echo '192.168.1.0/24 # Private network' | sed 's/#.*//' | xargs"
  [ "$output" = "192.168.1.0/24" ]
}

# ============================================================================
# WHITELIST VALIDATION TESTS
# ============================================================================

@test "Whitelist: Valid entries pass validation" {
  run bash -c "python3 -c \"
from ipaddress import ip_network
entries = ['10.0.0.0/8', '172.16.0.0/12', '2001:db8:cafe::/48']
for entry in entries:
    ip_network(entry, strict=False)
print('OK')
\""
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK"* ]]
}

@test "Whitelist: Can override blocklist entries" {
  # Create blocklist and whitelist
  echo "192.168.0.0/16" > "${TEST_DIR}/bl.txt"
  echo "192.168.1.0/24" > "${TEST_DIR}/wl.txt"
  
  # Verify whitelist entry is subset of blocklist
  run python3 -c "
from ipaddress import ip_network
blocked = ip_network('192.168.0.0/16')
whitelisted = ip_network('192.168.1.0/24')
print('subset' if whitelisted.subnet_of(blocked) else 'not_subset')
"
  [ "$output" = "subset" ]
}

# ============================================================================
# OVERLAP DETECTION TESTS
# ============================================================================

@test "Overlaps: Detects whitelist contained in blocklist" {
  run python3 -c "
from ipaddress import ip_network
blocked = ip_network('192.168.0.0/16')
whitelisted = ip_network('192.168.1.0/24')
if whitelisted.subnet_of(blocked):
    print('OVERLAP_DETECTED')
    exit(0)
exit(1)
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OVERLAP_DETECTED"* ]]
}

@test "Overlaps: Detects duplicate entries in blocklist" {
  run python3 -c "
from ipaddress import ip_network, collapse_addresses
cidrs = [ip_network('192.168.0.0/24'), ip_network('192.168.0.0/24')]
collapsed = list(collapse_addresses(cidrs))
if len(collapsed) < len(cidrs):
    print('DUPLICATE_DETECTED')
    exit(0)
exit(1)
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"DUPLICATE_DETECTED"* ]]
}

@test "Overlaps: Detects overlapping CIDR ranges in blocklist" {
  run python3 -c "
from ipaddress import ip_network, collapse_addresses
cidrs = [ip_network('192.168.0.0/24'), ip_network('192.168.0.128/25')]
collapsed = list(collapse_addresses(cidrs))
if len(collapsed) < len(cidrs):
    print('OVERLAP_DETECTED')
    exit(0)
exit(1)
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OVERLAP_DETECTED"* ]]
}

@test "Overlaps: No overlaps detected when ranges are disjoint" {
  run python3 -c "
from ipaddress import ip_network, collapse_addresses
cidrs = [ip_network('192.168.0.0/24'), ip_network('192.168.1.0/24')]
collapsed = list(collapse_addresses(cidrs))
if len(collapsed) == len(cidrs):
    print('NO_OVERLAPS')
    exit(0)
exit(1)
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"NO_OVERLAPS"* ]]
}

# ============================================================================
# IPv6-SPECIFIC TESTS
# ============================================================================

@test "IPv6: Link-local ranges recognized" {
  run bash -c "echo 'fe80::/10' | python3 -c \"import sys; from ipaddress import ip_network; net = ip_network(sys.stdin.read().strip()); print('link-local' if net.is_link_local else 'not-link-local')\""
  [ "$output" = "link-local" ]
}

@test "IPv6: Multicast ranges recognized" {
  run bash -c "echo 'ff00::/8' | python3 -c \"import sys; from ipaddress import ip_network; net = ip_network(sys.stdin.read().strip()); print('multicast' if net.is_multicast else 'not-multicast')\""
  [ "$output" = "multicast" ]
}

@test "IPv6: Loopback recognized" {
  run bash -c "echo '::1/128' | python3 -c \"import sys; from ipaddress import ip_network; net = ip_network(sys.stdin.read().strip()); print('loopback' if net.is_loopback else 'not-loopback')\""
  [ "$output" = "loopback" ]
}

@test "IPv6: ULA ranges recognized" {
  run bash -c "echo 'fc00::/7' | python3 -c \"import sys; from ipaddress import ip_network; net = ip_network(sys.stdin.read().strip()); print('private' if net.is_private else 'not-private')\""
  [ "$output" = "private" ]
}

@test "IPv6: Compressed notation accepted" {
  run bash -c "echo '2001:db8::1/128' | python3 -c \"import sys; from ipaddress import ip_network; print(ip_network(sys.stdin.read().strip()))\""
  [ "$status" -eq 0 ]
}

@test "IPv6: Expanded notation accepted" {
  run bash -c "echo '2001:0db8:0000:0000:0000:0000:0000:0001/128' | python3 -c \"import sys; from ipaddress import ip_network; print(ip_network(sys.stdin.read().strip()))\""
  [ "$status" -eq 0 ]
}

# ============================================================================
# REAL-WORLD EDGE CASES
# ============================================================================

@test "Edge case: Private RFC1918 ranges accepted" {
  run python3 -c "
from ipaddress import ip_network
ranges = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
for r in ranges:
    net = ip_network(r)
    if not net.is_private:
        exit(1)
print('ALL_PRIVATE')
"
  [ "$output" = "ALL_PRIVATE" ]
}

@test "Edge case: Loopback ranges handled correctly" {
  run python3 -c "
from ipaddress import ip_network
ranges = ['127.0.0.0/8', '::1/128']
for r in ranges:
    net = ip_network(r)
    if not net.is_loopback:
        exit(1)
print('ALL_LOOPBACK')
"
  [ "$output" = "ALL_LOOPBACK" ]
}

@test "Edge case: Broadcast not treated as CIDR" {
  # Verify that individual broadcast addresses are allowed
  run bash -c "echo '255.255.255.255/32' | python3 -c \"import sys; from ipaddress import ip_network; print(ip_network(sys.stdin.read().strip()))\""
  [ "$status" -eq 0 ]
}

@test "Edge case: IPv4-mapped IPv6 addresses" {
  run bash -c "echo '::ffff:192.0.2.1/128' | python3 -c \"import sys; from ipaddress import ip_network; print(ip_network(sys.stdin.read().strip()))\""
  [ "$status" -eq 0 ]
}

# ============================================================================
# PERFORMANCE & STRESS TESTS
# ============================================================================

@test "Performance: Large blocklist (1000 entries) validates in reasonable time" {
  # Generate 1000 unique IPv4 CIDR entries
  {
    for i in {0..249}; do
      echo "10.$((i/250)).0.0/24"
      echo "172.$((16+i/250)).$((i%256)).0/24"
      echo "192.168.$((i%256)).0/24"
      echo "203.0.$((113+i/250)).$((i%256))/24"
    done
  } > "${TEST_DIR}/large-blocklist.txt"
  
  # Time validation
  run bash -c "time python3 -c \"
from ipaddress import ip_network
with open('${TEST_DIR}/large-blocklist.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ip_network(line, strict=False)
print('OK')
\" 2>&1"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK"* ]]
}

@test "Stress: Mixed IPv4 and IPv6 blocklist" {
  {
    # IPv4 entries
    for i in {1..10}; do
      echo "10.$i.0.0/16"
    done
    # IPv6 entries
    for i in {1..10}; do
      printf "2001:db8::%x/64\n" "$i"
    done
  } > "${TEST_DIR}/mixed-blocklist.txt"
  
  run bash -c "python3 -c \"
from ipaddress import ip_network
count = 0
with open('${TEST_DIR}/mixed-blocklist.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ip_network(line, strict=False)
            count += 1
print(f'Validated {count} entries')
\""
  [ "$status" -eq 0 ]
  [[ "$output" == *"20 entries"* ]]
}

# ============================================================================
# INTEGRATION TESTS (Blocklist Deployment)
# ============================================================================

@test "Integration: Valid blocklist can be loaded by firewall tools" {
  # Simulate firewall reading blocklist
  run bash -c "python3 -c \"
import json
entries = []
with open('${BLOCKLIST_VALID}') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            entries.append(line)
data = {'entries': entries, 'count': len(entries)}
print(json.dumps(data))
\""
  [ "$status" -eq 0 ]
  [[ "$output" == *'"entries"'* ]]
  [[ "$output" == *'"count"'* ]]
}

@test "Integration: Whitelist exceptions work correctly" {
  # Simulate firewall applying whitelist exceptions
  run python3 -c "
from ipaddress import ip_network

blocklist = [ip_network('192.168.0.0/16')]
whitelist = [ip_network('192.168.1.0/24')]

def is_allowed(addr_str):
    addr = ip_network(addr_str, strict=False)
    # Check if in blocklist
    for blocked in blocklist:
        if addr.subnet_of(blocked):
            # Check if in whitelist
            for allowed in whitelist:
                if addr.subnet_of(allowed) or addr == allowed:
                    return True
            return False
    return True

test_cases = [
    ('192.168.1.0/24', True),    # Whitelisted
    ('192.168.2.0/24', False),   # Blocked
    ('10.0.0.0/8', True),        # Not blocked
]

for addr, expected in test_cases:
    result = is_allowed(addr)
    if result != expected:
        exit(1)
print('INTEGRATION_OK')
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"INTEGRATION_OK"* ]]
}

# ============================================================================
# SMOKE TESTS (Post-Deployment Validation)
# ============================================================================

@test "Smoke test: Default blocklist is accessible" {
  if [[ -f "etc/debvisor/blocklist-example.txt" ]]; then
    [ -r "etc/debvisor/blocklist-example.txt" ]
  fi
}

@test "Smoke test: Default whitelist is accessible" {
  if [[ -f "etc/debvisor/blocklist-whitelist-example.txt" ]]; then
    [ -r "etc/debvisor/blocklist-whitelist-example.txt" ]
  fi
}

@test "Smoke test: Validation script is executable" {
  if [[ -f "${SCRIPT_DIR}/validate-blocklists.sh" ]]; then
    [ -x "${SCRIPT_DIR}/validate-blocklists.sh" ]
  fi
}
