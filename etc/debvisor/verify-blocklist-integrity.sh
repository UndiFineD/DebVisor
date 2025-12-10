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
# verify-blocklist-integrity.sh
#
# Verify SHA256 checksums and integrity of blocklist files before deployment.
# Supports both individual file verification and batch verification against
# blocklist-metadata.json.
#
# Usage:
#   verify-blocklist-integrity.sh --blocklist <file> --sha256 <hash>
#   verify-blocklist-integrity.sh --metadata blocklist-metadata.json
#   verify-blocklist-integrity.sh --blocklist <file> --metadata blocklist-metadata.json
#

set -euo pipefail

# Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERBOSE=false
METADATA_FILE=""
BLOCKLIST_FILE=""
EXPECTED_SHA256=""
ABORT_ON_FAILURE=false

# Logging functions
log_info() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[INFO]${NC} $*" >&2
    fi
}

log_success() {
    echo -e "${GREEN}[?]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --blocklist)
                BLOCKLIST_FILE="$2"
                shift 2
                ;;
            --sha256)
                EXPECTED_SHA256="$2"
                shift 2
                ;;
            --metadata)
                METADATA_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --abort-on-failure)
                ABORT_ON_FAILURE=true
                shift
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}

print_usage() {
    cat << 'EOF'
Usage: verify-blocklist-integrity.sh [OPTIONS]

Options:
  --blocklist <file>           Blocklist file to verify
  --sha256 <hash>              Expected SHA256 hash of blocklist
  --metadata <file>            Metadata file (blocklist-metadata.json) for batch verification
  --verbose                    Enable verbose output
  --abort-on-failure           Exit with error code if any verification fails
  --help                       Print this help message

Examples:
  # Verify single file with explicit SHA256
  verify-blocklist-integrity.sh --blocklist blocklist-example.txt --sha256 abc123...

  # Verify using metadata file (checks all listed blocklists)
  verify-blocklist-integrity.sh --metadata blocklist-metadata.json

  # Combine: verify specific file against metadata
  verify-blocklist-integrity.sh --blocklist blocklist-example.txt --metadata blocklist-metadata.json

  # Verify and abort on any failure
  verify-blocklist-integrity.sh --metadata blocklist-metadata.json --abort-on-failure --verbose
EOF
}

# Compute SHA256 hash of a file
compute_sha256() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi
    
    if command -v sha256sum &> /dev/null; then
        sha256sum "$file" | awk '{print $1}'
    elif command -v shasum &> /dev/null; then
        shasum -a 256 "$file" | awk '{print $1}'
    else
        log_error "Neither sha256sum nor shasum found. Install GNU coreutils or libdigest-sha-perl."
        return 1
    fi
}

# Verify single blocklist file against expected SHA256
verify_single_file() {
    local file="$1"
    local expected_hash="$2"
    
    if [[ ! -f "$file" ]]; then
        log_error "Blocklist file not found: $file"
        return 1
    fi
    
    log_info "Computing SHA256 for: $file"
    local actual_hash
    actual_hash=$(compute_sha256 "$file") || return 1
    
    log_info "Expected hash: $expected_hash"
    log_info "Actual hash:   $actual_hash"
    
    if [[ "$actual_hash" == "$expected_hash" ]]; then
        log_success "Integrity verified: $file"
        return 0
    else
        log_error "Integrity check FAILED for: $file"
        log_error "  Expected: $expected_hash"
        log_error "  Actual:   $actual_hash"
        return 1
    fi
}

# Extract blocklist path from metadata JSON (simple parser)
extract_from_json() {
    local json_file="$1"
    local key_path="$2"
    
    # Use Python if available (more reliable), else grep
    if command -v python3 &> /dev/null; then
        python3 -c "
import json
import sys
try:
    with open('$json_file', 'r') as f:
        data = json.load(f)
    keys = '$key_path'.split('.')
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            sys.exit(1)
    print(result)
except:
    sys.exit(1)
" 2>/dev/null
        return $?
    else
        # Fallback: simple grep-based extraction (limited)
        grep -o "\"$key_path\": *\"[^\"]*\"" "$json_file" | cut -d'"' -f4
        return $?
    fi
}

# Verify blocklists using metadata file
verify_from_metadata() {
    local metadata_file="$1"
    local specific_blocklist="${2:-}"  # Optional: verify only specific blocklist
    
    if [[ ! -f "$metadata_file" ]]; then
        log_error "Metadata file not found: $metadata_file"
        return 1
    fi
    
    log_info "Loading metadata from: $metadata_file"
    
    # Parse metadata using Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 required for metadata parsing"
        return 1
    fi
    
    local verification_failed=0
    
    python3 << PYTHON_SCRIPT
import json
import subprocess
import sys
import os

def verify_blocklist(name, info, metadata_file_dir):
    """Verify a single blocklist entry from metadata"""
    file_path = os.path.join(metadata_file_dir, name)
    
    if not os.path.exists(file_path):
        print(f"[WARN] Blocklist file not found: {file_path}", file=sys.stderr)
        return False
    
    expected_sha256 = info.get('sha256', 'placeholder-compute-after-generation')
    
    # Skip verification if hash is placeholder
    if expected_sha256.startswith('placeholder'):
        print(f"[INFO] Skipping {name}: SHA256 is placeholder (not yet computed)")
        return True
    
    # Compute actual SHA256
    try:
        result = subprocess.run(
            ['sha256sum', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        actual_sha256 = result.stdout.split()[0]
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(
                ['shasum', '-a', '256', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            actual_sha256 = result.stdout.split()[0]
        except subprocess.CalledProcessError:
            print(f"[ERROR] Failed to compute SHA256 for {file_path}", file=sys.stderr)
            return False
    
    if actual_sha256 == expected_sha256:
        print(f"[?] Integrity verified: {name}")
        return True
    else:
        print(f"[ERROR] Integrity check FAILED for {name}", file=sys.stderr)
        print(f"  Expected: {expected_sha256}", file=sys.stderr)
        print(f"  Actual:   {actual_sha256}", file=sys.stderr)
        return False

try:
    with open('$metadata_file', 'r') as f:
        metadata = json.load(f)
    
    blocklists = metadata.get('blocklists', {})
    metadata_dir = os.path.dirname(os.path.abspath('$metadata_file'))
    
    all_passed = True
    for blocklist_name, blocklist_info in blocklists.items():
        # If specific blocklist requested, only verify that one
        if "$specific_blocklist" and blocklist_name != "$specific_blocklist":
            continue
        
        if not verify_blocklist(blocklist_name, blocklist_info, metadata_dir):
            all_passed = False
    
    sys.exit(0 if all_passed else 1)
except Exception as e:
    print(f"[ERROR] Failed to parse metadata: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

    return $?
}

# Main verification logic
main() {
    parse_args "$@"
    
    local verification_failed=0
    
    # Case 1: Metadata file only - verify all blocklists
    if [[ -n "$METADATA_FILE" ]] && [[ -z "$BLOCKLIST_FILE" ]] && [[ -z "$EXPECTED_SHA256" ]]; then
        log_info "Verifying all blocklists from metadata file"
        if ! verify_from_metadata "$METADATA_FILE"; then
            verification_failed=1
        fi
    fi
    
    # Case 2: Metadata file + specific blocklist - verify that blocklist
    elif [[ -n "$METADATA_FILE" ]] && [[ -n "$BLOCKLIST_FILE" ]] && [[ -z "$EXPECTED_SHA256" ]]; then
        log_info "Verifying blocklist against metadata file"
        if ! verify_from_metadata "$METADATA_FILE" "$(basename "$BLOCKLIST_FILE")"; then
            verification_failed=1
        fi
    fi
    
    # Case 3: Blocklist + explicit SHA256 - direct verification
    elif [[ -n "$BLOCKLIST_FILE" ]] && [[ -n "$EXPECTED_SHA256" ]]; then
        log_info "Verifying blocklist with explicit SHA256"
        if ! verify_single_file "$BLOCKLIST_FILE" "$EXPECTED_SHA256"; then
            verification_failed=1
        fi
    fi
    
    # Case 4: Blocklist file only - compute and display SHA256
    elif [[ -n "$BLOCKLIST_FILE" ]] && [[ -z "$EXPECTED_SHA256" ]] && [[ -z "$METADATA_FILE" ]]; then
        log_info "Computing SHA256 for blocklist"
        local sha256
        if ! sha256=$(compute_sha256 "$BLOCKLIST_FILE"); then
            verification_failed=1
        else
            echo "SHA256: $sha256"
            log_success "File: $BLOCKLIST_FILE"
        fi
    fi
    
    # No valid arguments
    else
        log_error "Invalid argument combination. Use --help for usage information."
        verification_failed=1
    fi
    
    # Report summary
    echo ""
    if [[ $verification_failed -eq 0 ]]; then
        log_success "All integrity checks passed"
        exit 0
    else
        log_error "One or more integrity checks failed"
        if [[ "$ABORT_ON_FAILURE" == true ]]; then
            exit 1
        else
            exit 0  # Exit cleanly even if checks failed (operator can decide action)
        fi
    fi
}

main "$@"
