#!/bin/bash
################################################################################
# debvisor-lib.sh - Shared bash library for DebVisor operational scripts
#
# This library provides common functions for error handling, logging, retries,
# validation, and safe operation patterns. All DebVisor scripts should source
# this library for consistent behavior and error handling.
#
# Usage in scripts:
#   source /usr/local/bin/debvisor-lib.sh
#   log_info "Starting operation..."
#   require_bin "ceph" "kubectl" "zpool"
#   retry 3 30 "ceph health" || die "Ceph health check failed"
#
# Exit Codes:
#   0 - Success
#   1 - General error
#   2 - Usage/argument error
#   3 - Prerequisite missing (binary, service, etc.)
#   4 - Configuration error
#   5 - Validation failed
#   10+ - Command-specific errors
#
################################################################################

set -eEuo pipefail

# Library identification
readonly DEBVISOR_LIB_VERSION="1.0.0"
readonly DEBVISOR_LIB_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Global state
DEBVISOR_VERBOSE=${DEBVISOR_VERBOSE:-false}
DEBVISOR_DRY_RUN=${DEBVISOR_DRY_RUN:-false}
DEBVISOR_LOG_FILE=${DEBVISOR_LOG_FILE:-}
DEBVISOR_AUDIT_LOG=${DEBVISOR_AUDIT_LOG:-/var/log/debvisor/audit.log}
DEBVISOR_SCRIPT_NAME="${0##*/}"

# Color codes for terminal output
readonly COLOR_RED='\033[0;31m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_RESET='\033[0m'

################################################################################
# Logging Functions
################################################################################

# log_info: Log informational message
# Usage: log_info "Operation started"
log_info() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="$*"
    echo -e "${COLOR_BLUE}[${timestamp}]${COLOR_RESET} ${COLOR_GREEN}[INFO]${COLOR_RESET} ${message}" >&2
    [ -n "$DEBVISOR_LOG_FILE" ] && echo "[${timestamp}] [INFO] ${message}" >> "$DEBVISOR_LOG_FILE"
}

# log_warn: Log warning message
# Usage: log_warn "Potential issue detected"
log_warn() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="$*"
    echo -e "${COLOR_BLUE}[${timestamp}]${COLOR_RESET} ${COLOR_YELLOW}[WARN]${COLOR_RESET} ${message}" >&2
    [ -n "$DEBVISOR_LOG_FILE" ] && echo "[${timestamp}] [WARN] ${message}" >> "$DEBVISOR_LOG_FILE"
}

# log_error: Log error message
# Usage: log_error "Something went wrong"
log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="$*"
    echo -e "${COLOR_BLUE}[${timestamp}]${COLOR_RESET} ${COLOR_RED}[ERROR]${COLOR_RESET} ${message}" >&2
    [ -n "$DEBVISOR_LOG_FILE" ] && echo "[${timestamp}] [ERROR] ${message}" >> "$DEBVISOR_LOG_FILE"
}

# log_debug: Log debug message (only if --verbose flag used)
# Usage: log_debug "Detailed diagnostic info"
log_debug() {
    if [ "$DEBVISOR_VERBOSE" = true ]; then
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        local message="$*"
        echo -e "${COLOR_BLUE}[${timestamp}]${COLOR_RESET} ${COLOR_YELLOW}[DEBUG]${COLOR_RESET} ${message}" >&2
        [ -n "$DEBVISOR_LOG_FILE" ] && echo "[${timestamp}] [DEBUG] ${message}" >> "$DEBVISOR_LOG_FILE"
    fi
}

# audit_log: Log to audit trail (for compliance and troubleshooting)
# Usage: audit_log "Operation" "Description" "Result"
audit_log() {
    local operation="$1"
    local description="$2"
    local result="${3:-success}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local user="${SUDO_USER:-$(whoami)}"
    
    mkdir -p "$(dirname "$DEBVISOR_AUDIT_LOG")"
    
    echo "[${timestamp}] User=${user} Script=${DEBVISOR_SCRIPT_NAME} Operation=${operation} Description=${description} Result=${result}" \
        >> "$DEBVISOR_AUDIT_LOG"
    
    log_debug "Audit logged: ${operation} - ${description} - ${result}"
}

################################################################################
# Error Handling & Exit Functions
################################################################################

# die: Print error message and exit with code
# Usage: die "Fatal error occurred" 1
die() {
    local message="$1"
    local exit_code="${2:-1}"
    
    log_error "$message"
    exit "$exit_code"
}

# cleanup_trap: Called on EXIT, handling cleanup tasks
# Usage: trap cleanup_trap EXIT
cleanup_trap() {
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_debug "Script completed successfully"
    else
        log_error "Script exited with code $exit_code"
    fi
    
    # Override exit code if needed
    return $exit_code
}

# error_trap: Called on ERR, provides error context
# Usage: trap error_trap ERR
error_trap() {
    local line_no=$1
    log_error "Error on line $line_no (exit code: $?)"
}

# Ensure traps are installed
trap cleanup_trap EXIT
trap error_trap ERR

################################################################################
# Validation Functions
################################################################################

# require_bin: Check that required binaries exist, exit if missing
# Usage: require_bin "ceph" "kubectl" "zpool"
require_bin() {
    local missing=()
    
    for bin in "$@"; do
        if ! command -v "$bin" &>/dev/null; then
            missing+=("$bin")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required binaries: ${missing[*]}"
        die "Required tools not installed: ${missing[*]}" 3
    fi
    
    log_debug "All required binaries found: $*"
}

# require_env: Check that required environment variables are set
# Usage: require_env "HOME" "USER" "DEBVISOR_CLUSTER"
require_env() {
    local missing=()
    
    for var in "$@"; do
        if [ -z "${!var:-}" ]; then
            missing+=("$var")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required environment variables: ${missing[*]}"
        die "Required environment variables not set: ${missing[*]}" 4
    fi
    
    log_debug "All required environment variables set: $*"
}

# require_root: Check that script is running as root
# Usage: require_root
require_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        die "Root privileges required" 3
    fi
    log_debug "Running as root"
}

# require_file: Check that required files exist
# Usage: require_file "/etc/ceph/ceph.conf" "/etc/kubernetes/admin.conf"
require_file() {
    local missing=()
    
    for file in "$@"; do
        if [ ! -f "$file" ]; then
            missing+=("$file")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required files: ${missing[*]}"
        die "Required files not found: ${missing[*]}" 5
    fi
    
    log_debug "All required files found: $*"
}

# validate_cidr: Validate CIDR notation (e.g., "192.168.1.0/24")
# Usage: validate_cidr "10.0.0.0/8" || die "Invalid CIDR"
validate_cidr() {
    local cidr="$1"
    
    if ! [[ "$cidr" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        log_error "Invalid CIDR format: $cidr"
        return 1
    fi
    
    local ip="${cidr%/*}"
    local prefix="${cidr#*/}"
    
    # Validate IP octets
    local IFS='.'
    read -ra octets <<< "$ip"
    for octet in "${octets[@]}"; do
        if [ "$octet" -gt 255 ]; then
            log_error "Invalid IP address in CIDR: $ip"
            return 1
        fi
    done
    
    # Validate prefix length
    if [ "$prefix" -lt 0 ] || [ "$prefix" -gt 32 ]; then
        log_error "Invalid prefix length in CIDR: $prefix"
        return 1
    fi
    
    return 0
}

# validate_pool_name: Validate ZFS pool name
# Usage: validate_pool_name "tank" || die "Invalid pool name"
validate_pool_name() {
    local pool="$1"
    
    if ! [[ "$pool" =~ ^[a-zA-Z][a-zA-Z0-9_:-]*$ ]]; then
        log_error "Invalid pool name: $pool"
        return 1
    fi
    
    return 0
}

################################################################################
# Retry & Transient Failure Handling
################################################################################

# retry: Retry command with exponential backoff
# Usage: retry 3 30 "ceph health" || die "Command failed"
# Args: max_attempts initial_delay_seconds command [args...]
retry() {
    local max_attempts="$1"
    local initial_delay="$2"
    shift 2
    local command=("$@")
    
    local attempt=1
    local delay="$initial_delay"
    
    while [ $attempt -le "$max_attempts" ]; do
        log_debug "Attempt $attempt/$max_attempts: ${command[*]}"
        
        if "${command[@]}"; then
            log_debug "Command succeeded on attempt $attempt"
            return 0
        fi
        
        if [ $attempt -lt "$max_attempts" ]; then
            log_warn "Command failed (attempt $attempt/$max_attempts), retrying in ${delay}s..."
            sleep "$delay"
            # Exponential backoff: double delay, cap at 5 minutes
            delay=$((delay * 2))
            delay=$((delay > 300 ? 300 : delay))
        fi
        
        ((attempt++))
    done
    
    log_error "Command failed after $max_attempts attempts: ${command[*]}"
    return 1
}

# wait_for_condition: Wait for a condition to become true with timeout
# Usage: wait_for_condition 60 "ceph health | grep -q HEALTH_OK" || die "Ceph unhealthy"
wait_for_condition() {
    local timeout_seconds="$1"
    local condition="$2"
    local check_interval="${3:-5}"
    
    local start_time=$(date +%s)
    
    while true; do
        if eval "$condition"; then
            log_debug "Condition satisfied"
            return 0
        fi
        
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -ge "$timeout_seconds" ]; then
            log_error "Condition not satisfied within ${timeout_seconds}s: $condition"
            return 1
        fi
        
        local remaining=$((timeout_seconds - elapsed))
        log_debug "Condition not yet satisfied, checking again in ${check_interval}s (${remaining}s remaining)..."
        sleep "$check_interval"
    done
}

################################################################################
# Dry-Run & Safe Operation Functions
################################################################################

# execute: Execute command, respecting dry-run mode
# Usage: execute "rm -rf /tmp/old" "Remove old files"
execute() {
    # Use distinct variable name to avoid array/string cross warnings (SC2178/SC2128)
    local cmd_str="$1"
    local description="${2:-Executing command}"

    log_info "$description"
    log_debug "Command: $cmd_str"

    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "[DRY-RUN] Would execute: $cmd_str"
        return 0
    fi

    if eval "$cmd_str"; then
        log_debug "Command succeeded"
        return 0
    else
        log_error "Command failed: $cmd_str"
        return 1
    fi
}

# show_dry_run_plan: Display what would be done in dry-run mode
# Usage: show_dry_run_plan "- Remove old backups" "- Update DNS records" "- Restart services"
show_dry_run_plan() {
    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "===== DRY-RUN MODE: The following would be executed ====="
        while [ $# -gt 0 ]; do
            log_info "  $1"
            shift
        done
        log_info "===== END DRY-RUN PLAN ====="
    fi
}

# confirm_operation: Prompt user to confirm an operation
# Usage: confirm_operation "This will upgrade all nodes" || return 1
confirm_operation() {
    local message="$1"
    
    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "[DRY-RUN] Would ask for confirmation: $message"
        return 0
    fi
    
    log_warn "$message"
    read -p "Continue? (yes/no): " -r response
    
    if [[ "$response" =~ ^[Yy][Ee][Ss]$ ]]; then
        return 0
    else
        log_info "Operation cancelled by user"
        return 1
    fi
}

################################################################################
# Ceph Operations
################################################################################

# ceph_health_check: Check Ceph cluster health, return status
# Usage: ceph_health_check || die "Cluster unhealthy"
ceph_health_check() {
    require_bin "ceph"
    
    log_debug "Checking Ceph health..."
    local health_status
    
    if ! health_status=$(ceph health); then
        log_error "Failed to query Ceph health"
        return 1
    fi
    
    log_debug "Ceph health output: $health_status"
    
    if [[ "$health_status" =~ HEALTH_OK ]]; then
        log_debug "Ceph cluster healthy"
        return 0
    else
        log_error "Ceph cluster unhealthy: $health_status"
        return 1
    fi
}

# ceph_osds_ready: Check that all OSDs are up and in
# Usage: ceph_osds_ready || die "Not all OSDs ready"
ceph_osds_ready() {
    require_bin "ceph"
    
    log_debug "Checking Ceph OSD status..."
    
    local down_osds
    if ! down_osds=$(ceph osd stat | grep -oP '(?<=down )[^ ]*'); then
        down_osds=0
    fi
    
    if [ "$down_osds" -eq 0 ]; then
        log_debug "All OSDs are up and in"
        return 0
    else
        log_error "Some OSDs are down: $down_osds down"
        return 1
    fi
}

# ceph_set_noout: Set noout flag on cluster (prevents rebalance during maintenance)
# Usage: ceph_set_noout || die "Failed to set noout"
ceph_set_noout() {
    require_bin "ceph"
    require_root
    
    log_info "Setting Ceph noout flag..."
    
    if ceph osd set noout; then
        log_debug "Noout flag set"
        audit_log "ceph_set_noout" "Set noout flag for maintenance"
        return 0
    else
        log_error "Failed to set noout flag"
        return 1
    fi
}

# ceph_unset_noout: Remove noout flag
# Usage: ceph_unset_noout || die "Failed to unset noout"
ceph_unset_noout() {
    require_bin "ceph"
    require_root
    
    log_info "Removing Ceph noout flag..."
    
    if ceph osd unset noout; then
        log_debug "Noout flag removed"
        audit_log "ceph_unset_noout" "Removed noout flag after maintenance"
        return 0
    else
        log_error "Failed to unset noout flag"
        return 1
    fi
}

################################################################################
# ZFS Operations
################################################################################

# zpool_exists: Check if ZFS pool exists
# Usage: zpool_exists "tank" || die "Pool not found"
zpool_exists() {
    local pool="$1"
    
    require_bin "zpool"
    validate_pool_name "$pool" || return 1
    
    if zpool list "$pool" &>/dev/null; then
        log_debug "ZFS pool exists: $pool"
        return 0
    else
        log_error "ZFS pool not found: $pool"
        return 1
    fi
}

# zpool_health: Get ZFS pool health status
# Usage: health=$(zpool_health "tank") && log_info "Pool health: $health"
zpool_health() {
    local pool="$1"
    
    require_bin "zpool"
    validate_pool_name "$pool" || return 1
    
    zpool list -H -o health "$pool" || return 1
}

# zpool_scrub_schedule: Get next scheduled scrub time
# Usage: next_scrub=$(zpool_scrub_schedule "tank")
zpool_scrub_schedule() {
    local pool="$1"
    
    require_bin "zpool"
    validate_pool_name "$pool" || return 1
    
    # Get last scrub time and estimate next
    local last_scrub
    last_scrub=$(zpool status "$pool" | grep "scan:" | grep -oP '\d{4}-\d{2}-\d{2}')
    
    if [ -z "$last_scrub" ]; then
        echo "Never"
        return 0
    fi
    
    echo "$last_scrub"
}

################################################################################
# Kubernetes Operations
################################################################################

# kubectl_available: Check if kubectl is available and configured
# Usage: kubectl_available || log_warn "Kubernetes not configured"
kubectl_available() {
    require_bin "kubectl"
    
    if kubectl cluster-info &>/dev/null; then
        log_debug "Kubernetes cluster accessible"
        return 0
    else
        log_error "Kubernetes cluster not accessible"
        return 1
    fi
}

# k8s_nodes_ready: Check that all K8s nodes are ready
# Usage: k8s_nodes_ready || die "Kubernetes nodes not ready"
k8s_nodes_ready() {
    require_bin "kubectl"
    
    log_debug "Checking Kubernetes node status..."
    
    local ready_count notready_count
    ready_count=$(kubectl get nodes --no-headers 2>/dev/null | grep -c " Ready " || echo 0)
    notready_count=$(kubectl get nodes --no-headers 2>/dev/null | grep -cv " Ready " || echo 0)
    
    if [ "$notready_count" -eq 0 ]; then
        log_debug "All Kubernetes nodes ready"
        return 0
    else
        log_error "Some Kubernetes nodes not ready: $notready_count/$((ready_count + notready_count))"
        return 1
    fi
}

################################################################################
# Output Formatting
################################################################################

# output_json: Convert key=value pairs to JSON
# Usage: output_json status=success node=node1 pool=tank
output_json() {
    local json="{"
    local first=true
    
    while [ $# -gt 0 ]; do
        local pair="$1"
        local key="${pair%=*}"
        local value="${pair#*=}"
        
        if [ "$first" = true ]; then
            first=false
        else
            json+=","
        fi
        
        json+="\"$key\":\"$value\""
        shift
    done
    
    json+="}"
    echo "$json"
}

# tabulate: Format output as table
# Usage: tabulate "Name" "Status" "Pod" "node1" "ready" "pod-123"
tabulate() {
    local col_width=20
    while [ $# -gt 0 ]; do
        printf "%-${col_width}s" "$1"
        shift
    done
    echo
}

################################################################################
# Library Initialization
################################################################################

# Ensure library is properly loaded
log_debug "DebVisor library loaded (version $DEBVISOR_LIB_VERSION)"

# Handle common flags in parent script context (these should be parsed by parent)
# This function can be called to set up common flag handling
parse_common_flags() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --verbose)
                DEBVISOR_VERBOSE=true
                log_debug "Verbose mode enabled"
                shift
                ;;
            --dry-run)
                DEBVISOR_DRY_RUN=true
                log_info "Dry-run mode enabled"
                shift
                ;;
            --log-file)
                DEBVISOR_LOG_FILE="$2"
                mkdir -p "$(dirname "$DEBVISOR_LOG_FILE")"
                log_info "Logging to: $DEBVISOR_LOG_FILE"
                shift 2
                ;;
            --help|-h)
                echo "Common flags:"
                echo "  --verbose           Enable verbose output"
                echo "  --dry-run           Show what would be done without making changes"
                echo "  --log-file FILE     Write logs to file"
                echo "  --help              Show this help"
                shift
                ;;
            *)
                # Unknown flag, let parent handle it
                return 0
                ;;
        esac
    done
}

# Export for use in subshells
export DEBVISOR_VERBOSE DEBVISOR_DRY_RUN DEBVISOR_LOG_FILE DEBVISOR_AUDIT_LOG DEBVISOR_SCRIPT_NAME

################################################################################
# End of debvisor-lib.sh
################################################################################
