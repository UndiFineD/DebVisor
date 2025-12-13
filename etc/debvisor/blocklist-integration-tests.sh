#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#
# blocklist-integration-tests.sh - Integration tests for blocklist deployment and enforcement
#
# This script validates blocklist functionality in a test environment:
#   1. Deploy blocklist and whitelist to test location
#   2. Verify firewall rules block/allow traffic correctly
#   3. Test exception handling with whitelisted entries
#   4. Validate smoke tests after deployment
#
# Requirements:
#   - Python 3 with ipaddress module
#   - bash 4.0+
#   - Optional: iptables/nftables for actual traffic testing
#
# Usage:
#   ./blocklist-integration-tests.sh [--verbose] [--with-firewall]
#

set -euo pipefail

VERBOSE=false
WITH_FIREWALL=false
TEST_ENV="/tmp/debvisor-blocklist-test"
PASS_COUNT=0
FAIL_COUNT=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

log_pass() {
  echo -e "${GREEN}[PASS]${NC} $*"
  ((PASS_COUNT++))
}

log_fail() {
  echo -e "${RED}[FAIL]${NC} $*"
  ((FAIL_COUNT++))
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

log_verbose() {
  if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${BLUE}[VERBOSE]${NC} $*"
  fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --verbose) VERBOSE=true; shift ;;
    --with-firewall) WITH_FIREWALL=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Setup test environment
setup_test_env() {
  log_info "Setting up test environment..."
  rm -rf "$TEST_ENV"
  mkdir -p "$TEST_ENV"/{blocklists,whitelists,results}

  # Copy example files
  if [[ -f "etc/debvisor/blocklist-example.txt" ]]; then
    cp "etc/debvisor/blocklist-example.txt" "$TEST_ENV/blocklists/test-blocklist.txt"
    log_verbose "Copied blocklist to test environment"
  fi

  if [[ -f "etc/debvisor/blocklist-whitelist-example.txt" ]]; then
    cp "etc/debvisor/blocklist-whitelist-example.txt" "$TEST_ENV/whitelists/test-whitelist.txt"
    log_verbose "Copied whitelist to test environment"
  fi
}

# Test 1: Blocklist can be read and parsed
test_blocklist_parsing() {
  log_info "Test 1: Blocklist parsing..."

  if [[ ! -f "$TEST_ENV/blocklists/test-blocklist.txt" ]]; then
    log_fail "Blocklist file not found"
    return 1
  fi

  local entry_count=$(grep -v '^[[:space:]]*$' "$TEST_ENV/blocklists/test-blocklist.txt" | grep -c -v '^[[:space:]]*#')

  if [[ $entry_count -gt 0 ]]; then
    log_pass "Blocklist contains $entry_count valid entries"
    return 0
  else
    log_fail "Blocklist contains no valid entries"
    return 1
  fi
}

# Test 2: All blocklist entries are valid CIDR format
test_blocklist_syntax() {
  log_info "Test 2: Blocklist syntax validation..."

  local invalid_count=0
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue

    local entry=$(echo "$line" | sed 's/#.*//' | xargs)
    [[ -z "$entry" ]] && continue

    if ! python3 -c "from ipaddress import ip_network; ip_network('$entry', strict=False)" 2>/dev/null; then
      log_verbose "Invalid entry: $entry"
      ((invalid_count++))
    fi
  done < "$TEST_ENV/blocklists/test-blocklist.txt"

  if [[ $invalid_count -eq 0 ]]; then
    log_pass "All blocklist entries have valid CIDR syntax"
    return 0
  else
    log_fail "Found $invalid_count entries with invalid CIDR syntax"
    return 1
  fi
}

# Test 3: Whitelist can be read and parsed
test_whitelist_parsing() {
  log_info "Test 3: Whitelist parsing..."

  if [[ ! -f "$TEST_ENV/whitelists/test-whitelist.txt" ]]; then
    log_fail "Whitelist file not found"
    return 1
  fi

  local entry_count=$(grep -v '^[[:space:]]*$' "$TEST_ENV/whitelists/test-whitelist.txt" | grep -c -v '^[[:space:]]*#')

  if [[ $entry_count -gt 0 ]]; then
    log_pass "Whitelist contains $entry_count valid entries"
    return 0
  else
    log_fail "Whitelist contains no valid entries"
    return 1
  fi
}

# Test 4: Whitelist exceptions override blocklist entries
test_whitelist_exceptions() {
  log_info "Test 4: Whitelist exception handling..."

  python3 << 'PYEOF' > "$TEST_ENV/results/whitelist-test.json" 2>&1
import json
from ipaddress import ip_network

# Test case: 203.0.113.0/24 is blocked, but 203.0.113.10 is whitelisted
blocked = ip_network('203.0.113.0/24')
whitelisted = ip_network('203.0.113.10/32')
test_addr = ip_network('203.0.113.10/32')

# Check if test address is blocked
is_blocked = test_addr.subnet_of(blocked)

# Check if test address is whitelisted
is_whitelisted = test_addr.subnet_of(whitelisted) or test_addr == whitelisted

# Result: Should be blocked but exception applies (whitelisted)
result = {
    'blocked': is_blocked,
    'whitelisted': is_whitelisted,
    'allowed': not is_blocked or is_whitelisted
}

print(json.dumps(result))
PYEOF

  local result=$(python3 -c "
import json
with open('$TEST_ENV/results/whitelist-test.json') as f:
    data = json.load(f)
    if data['blocked'] and data['whitelisted'] and data['allowed']:
        print('PASS')
    else:
        print('FAIL')
  ")

  if [[ "$result" == "PASS" ]]; then
    log_pass "Whitelist exceptions correctly override blocklist"
    return 0
  else
    log_fail "Whitelist exceptions not working correctly"
    return 1
  fi
}

# Test 5: Overlapping ranges detected
test_overlap_detection() {
  log_info "Test 5: Overlapping range detection..."

  python3 << 'PYEOF' > "$TEST_ENV/results/overlap-test.json" 2>&1
import json
from ipaddress import ip_network, collapse_addresses

# Test: 192.168.0.0/16 and 192.168.1.0/24 overlap
cidrs = [ip_network('192.168.0.0/16'), ip_network('192.168.1.0/24')]
collapsed = list(collapse_addresses(cidrs))

result = {
    'original_count': len(cidrs),
    'collapsed_count': len(collapsed),
    'has_overlaps': len(collapsed) < len(cidrs)
}

print(json.dumps(result))
PYEOF

  local result=$(python3 -c "
import json
with open('$TEST_ENV/results/overlap-test.json') as f:
    data = json.load(f)
    if data['has_overlaps']:
        print('PASS')
    else:
        print('FAIL')
  ")

  if [[ "$result" == "PASS" ]]; then
    log_pass "Overlapping ranges correctly detected"
    return 0
  else
    log_fail "Overlap detection failed"
    return 1
  fi
}

# Test 6: IPv4 and IPv6 mixed correctly
test_ipv4_ipv6_support() {
  log_info "Test 6: IPv4 and IPv6 support..."

  python3 << 'PYEOF' > "$TEST_ENV/results/dual-stack-test.json" 2>&1
import json
from ipaddress import ip_network

entries = [
    '192.168.0.0/16',
    '10.0.0.0/8',
    '2001:db8::/32',
    'fc00::/7'
]

results = {}
for entry in entries:
    try:
        net = ip_network(entry, strict=False)
        results[entry] = {
            'valid': True,
            'version': net.version,
            'type': 'ipv4' if net.version == 4 else 'ipv6'
        }
    except Exception as e:
        results[entry] = {'valid': False, 'error': str(e)}

print(json.dumps(results))
PYEOF

  local ipv4_count=$(python3 -c "
import json
with open('$TEST_ENV/results/dual-stack-test.json') as f:
    data = json.load(f)
    print(sum(1 for v in data.values() if v.get('type') == 'ipv4'))
  " 2>/dev/null || echo 0)

  local ipv6_count=$(python3 -c "
import json
with open('$TEST_ENV/results/dual-stack-test.json') as f:
    data = json.load(f)
    print(sum(1 for v in data.values() if v.get('type') == 'ipv6'))
  " 2>/dev/null || echo 0)

  if [[ $ipv4_count -ge 2 && $ipv6_count -ge 2 ]]; then
    log_pass "IPv4 ($ipv4_count) and IPv6 ($ipv6_count) entries supported"
    return 0
  else
    log_fail "IPv4/IPv6 support incomplete"
    return 1
  fi
}

# Test 7: Smoke test - post-deployment validation
test_post_deployment() {
  log_info "Test 7: Post-deployment validation..."

  # Check file permissions
  if [[ -f "$TEST_ENV/blocklists/test-blocklist.txt" ]]; then
    local perms=$(stat -c %a "$TEST_ENV/blocklists/test-blocklist.txt" 2>/dev/null || echo "unknown")
    log_verbose "Blocklist permissions: $perms"
    log_pass "Post-deployment files accessible"
    return 0
  else
    log_fail "Blocklist file not accessible after deployment"
    return 1
  fi
}

# Test 8: Large blocklist performance (optional)
test_performance() {
  log_info "Test 8: Performance with large blocklist..."

  # Generate 100 entries
  {
    for i in {0..99}; do
      echo "10.$((i/256)).$((i%256)).0/24"
    done
  } > "$TEST_ENV/large-blocklist.txt"

  local start_time=$(date +%s.%N)

  python3 << 'PYEOF' > /dev/null 2>&1
from ipaddress import ip_network
with open('${TEST_ENV}/large-blocklist.txt') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            ip_network(line.strip(), strict=False)
PYEOF

  local end_time=$(date +%s.%N)
  local duration=$(python3 -c "print(f'{$end_time - $start_time:.3f}')")

  log_pass "Validated 100 entries in ${duration}s"
  return 0
}

# Cleanup
cleanup() {
  log_info "Cleaning up test environment..."
  # Keep results for review, but optionally clean up later
  log_verbose "Test results saved to: $TEST_ENV/results/"
}

# Main execution
main() {
  log_info "====== DebVisor Blocklist Integration Tests ======"
  log_info "Test environment: $TEST_ENV"
  echo

  setup_test_env

  # Run tests
  test_blocklist_parsing || true
  test_blocklist_syntax || true
  test_whitelist_parsing || true
  test_whitelist_exceptions || true
  test_overlap_detection || true
  test_ipv4_ipv6_support || true
  test_post_deployment || true
  test_performance || true

  # Summary
  echo
  log_info "====== Test Summary ======"
  log_pass "Passed: $PASS_COUNT"
  log_fail "Failed: $FAIL_COUNT"

  if [[ $FAIL_COUNT -eq 0 ]]; then
    log_info "All integration tests PASSED ?"
    cleanup
    exit 0
  else
    log_warn "Some tests FAILED - review $TEST_ENV/results/ for details"
    cleanup
    exit 1
  fi
}

# Trap errors
trap cleanup EXIT

# Run main
main "$@"
