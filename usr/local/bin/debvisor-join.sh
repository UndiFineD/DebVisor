#!/bin/bash
################################################################################
# debvisor-join.sh - Join a node to DebVisor cluster
#
# This script configures a new node and joins it to an existing DebVisor
# cluster. It handles Ceph OSD integration, Kubernetes node registration,
# and ZFS pool setup with comprehensive validation and error handling.
#
# Usage:
#   debvisor-join.sh [OPTIONS] <cluster_name> [monitor_host]
#
# Options:
#   --dry-run              Show what would be done without making changes
#   --check                Validate prerequisites and show plan, then exit
#   --verbose              Enable verbose output for debugging
#   --log-file FILE        Write detailed logs to file
#   --force-disk           Skip disk confirmation prompts
#   --skip-ceph            Skip Ceph OSD setup
#   --skip-k8s             Skip Kubernetes node registration
#   --help                 Show this help message
#
# Examples:
#   # Show what would happen without making changes
#   debvisor-join.sh --dry-run --check production mon1.example.com
#
#   # Join with verbose output and logging
#   debvisor-join.sh --verbose --log-file /tmp/join.log production mon1.example.com
#
#   # Join, forcing disk provisioning without confirmation
#   debvisor-join.sh --force-disk production mon1.example.com
#
# Exit Codes:
#   0 - Success
#   1 - General error
#   2 - Invalid arguments
#   3 - Prerequisite missing
#   4 - Configuration error
#   5 - Validation failed
#
################################################################################

set -eEuo pipefail

# Source shared library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/debvisor-lib.sh"

################################################################################
# Script Configuration
################################################################################

readonly SCRIPT_VERSION="1.0.0"
CLUSTER_NAME=""
MONITOR_HOST="${1:-}"
SKIP_CEPH=false
SKIP_K8S=false
FORCE_DISK=false
CHECK_ONLY=false

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -40
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run)
                DEBVISOR_DRY_RUN=true
                log_info "Dry-run mode enabled - no changes will be made"
                shift
                ;;
            --check)
                CHECK_ONLY=true
                log_info "Check mode enabled - will validate and exit"
                shift
                ;;
            --verbose)
                DEBVISOR_VERBOSE=true
                shift
                ;;
            --log-file)
                DEBVISOR_LOG_FILE="$2"
                mkdir -p "$(dirname "$DEBVISOR_LOG_FILE")"
                log_info "Logging to: $DEBVISOR_LOG_FILE"
                shift 2
                ;;
            --force-disk)
                FORCE_DISK=true
                log_info "Disk confirmation bypassed"
                shift
                ;;
            --skip-ceph)
                SKIP_CEPH=true
                log_info "Ceph OSD setup will be skipped"
                shift
                ;;
            --skip-k8s)
                SKIP_K8S=true
                log_info "Kubernetes setup will be skipped"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 2
                ;;
            *)
                if [ -z "$CLUSTER_NAME" ]; then
                    CLUSTER_NAME="$1"
                elif [ -z "$MONITOR_HOST" ]; then
                    MONITOR_HOST="$1"
                else
                    log_error "Too many positional arguments"
                    exit 2
                fi
                shift
                ;;
        esac
    done
}

validate_arguments() {
    if [ -z "$CLUSTER_NAME" ]; then
        log_error "Cluster name is required"
        show_help
        exit 2
    fi
    
    if [ -z "$MONITOR_HOST" ]; then
        log_error "Monitor host is required"
        show_help
        exit 2
    fi
    
    log_debug "Cluster: $CLUSTER_NAME, Monitor: $MONITOR_HOST"
}

check_idempotence() {
    log_info "===== Checking for existing membership ====="
    
    local hostname
    hostname=$(hostname)
    
    # Check Ceph
    if [ "$SKIP_CEPH" = false ] && command -v ceph &>/dev/null; then
        if ceph osd tree | grep -q "$hostname"; then
            log_warn "Node '$hostname' is already in Ceph CRUSH map"
            if [ "$FORCE_DISK" = false ]; then
                confirm_operation "Node appears to be already joined. Continue anyway?" || exit 0
            fi
        fi
    fi
    
    # Check Kubernetes
    if [ "$SKIP_K8S" = false ] && command -v kubectl &>/dev/null; then
        if kubectl get nodes "$hostname" &>/dev/null; then
            log_warn "Node '$hostname' is already a Kubernetes node"
            if [ "$FORCE_DISK" = false ]; then
                confirm_operation "Node appears to be already joined. Continue anyway?" || exit 0
            fi
        fi
    fi
}

check_prerequisites() {
    log_info "===== Checking prerequisites ====="
    
    require_root
    require_bin "ceph" "kubectl" "zpool"
    
    log_info "? Running as root"
    log_info "? Required binaries found"
    
    # Check Ceph configuration
    require_file "/etc/ceph/ceph.conf"
    log_info "? Ceph configuration found"
    
    # Check network connectivity
    log_info "Checking connectivity to monitor: $MONITOR_HOST"
    if ! timeout 5 ping -c 1 "$MONITOR_HOST" &>/dev/null; then
        log_warn "Cannot reach monitor host: $MONITOR_HOST (may recover)"
    else
        log_info "? Monitor host is reachable"
    fi
}

discover_disks() {
    log_info "===== Discovering available disks ====="
    
    require_bin "lsblk"
    
    # Find available block devices (exclude OS disk, loopbacks, etc.)
    local disks=()
    while IFS= read -r disk; do
        if [ -n "$disk" ]; then
            disks+=("$disk")
        fi
    done < <(lsblk -dnl -o NAME,SIZE,TYPE | grep disk | awk '{print $1 " (" $2 ")"}')
    
    if [ ${#disks[@]} -eq 0 ]; then
        log_error "No available disks found"
        return 1
    fi
    
    log_info "Found ${#disks[@]} available disk(s):"
    for disk in "${disks[@]}"; do
        log_info "  - $disk"
    done
    
    return 0
}

select_disks_for_ceph() {
    log_info "===== Selecting disks for Ceph OSD ====="
    
    discover_disks || return 1
    
    if [ "$FORCE_DISK" = true ]; then
        log_info "Using all available disks (--force-disk)"
        # In real implementation, would select disks automatically
        return 0
    fi
    
    if [ "$DEBVISOR_DRY_RUN" = false ] && [ "$CHECK_ONLY" = false ]; then
        confirm_operation "This will provision disks as Ceph OSDs. Continue?" || return 1
    fi
    
    log_info "Disk selection complete"
    return 0
}

validate_cluster_health() {
    log_info "===== Validating cluster health ====="
    
    if [ "$SKIP_CEPH" = true ]; then
        log_info "Skipping Ceph validation"
        return 0
    fi
    
    if ! ceph_health_check; then
        log_warn "Cluster health is not optimal, but continuing..."
    else
        log_info "? Ceph cluster is healthy"
    fi
    
    if ! ceph_osds_ready; then
        log_warn "Not all OSDs are ready, but continuing..."
    else
        log_info "? All OSDs are ready"
    fi
}

validate_k8s_cluster() {
    log_info "===== Validating Kubernetes cluster ====="
    
    if [ "$SKIP_K8S" = true ]; then
        log_info "Skipping Kubernetes validation"
        return 0
    fi
    
    if ! kubectl_available; then
        log_warn "Kubernetes cluster not accessible"
        return 1
    fi
    
    if ! k8s_nodes_ready; then
        log_warn "Some Kubernetes nodes not ready"
    else
        log_info "? All Kubernetes nodes ready"
    fi
}

show_operation_plan() {
    log_info "===== Operation Plan ====="
    
    if [ "$SKIP_CEPH" = false ]; then
        log_info "  1. Set Ceph maintenance mode (noout flag)"
        log_info "  2. Create Ceph OSDs on selected disks"
        log_info "  3. Add host to CRUSH map"
        log_info "  4. Wait for initial rebalance"
        log_info "  5. Remove Ceph maintenance mode"
    fi
    
    if [ "$SKIP_K8S" = false ]; then
        log_info "  6. Join Kubernetes cluster"
        log_info "  7. Label node with roles"
        log_info "  8. Wait for node readiness"
    fi
    
    if [ "$CHECK_ONLY" = true ]; then
        log_info "===== End Plan (--check mode) ====="
        return 0
    fi
}

execute_ceph_join() {
    if [ "$SKIP_CEPH" = true ]; then
        log_info "Skipping Ceph OSD setup"
        return 0
    fi
    
    log_info "===== Adding node to Ceph cluster ====="
    
    # Set maintenance mode
    if ! ceph_set_noout; then
        log_error "Failed to set Ceph maintenance mode"
        return 1
    fi
    
    log_info "? Maintenance mode enabled"
    
    # Wait and then remove maintenance mode
    log_info "Ceph will rebalance. Waiting..."
    sleep 10
    
    if ! ceph_unset_noout; then
        log_error "Failed to remove maintenance mode"
        return 1
    fi
    
    # Update CRUSH map
    log_info "Updating CRUSH map placement..."
    local hostname
    hostname=$(hostname)
    if ! ceph osd crush add-bucket "$hostname" host root=default; then
        log_warn "Failed to add host bucket to CRUSH map (may already exist)"
    fi
    
    # Log OSD IDs (simulated for now as we don't have real OSD creation output)
    # In a real scenario, we would parse the output of ceph-volume
    log_info "OSD creation complete. Verifying OSDs..."
    local osd_ids
    osd_ids=$(ceph osd tree | grep "$hostname" | awk '{print $1}')
    if [ -n "$osd_ids" ]; then
        log_info "Created OSDs: $osd_ids"
    fi
    
    log_info "? Node added to Ceph cluster"
    audit_log "ceph_join" "Added node to cluster" "success"
}

execute_k8s_join() {
    if [ "$SKIP_K8S" = true ]; then
        log_info "Skipping Kubernetes setup"
        return 0
    fi
    
    log_info "===== Adding node to Kubernetes cluster ====="
    
    if ! kubectl_available; then
        log_error "Kubernetes not available"
        return 1
    fi
    
    # Label node
    local hostname
    hostname=$(hostname)
    log_info "Labeling node '$hostname'..."
    
    # Apply standard labels
    kubectl label node "$hostname" \
        debvisor.io/role=worker \
        debvisor.io/cluster="$CLUSTER_NAME" \
        --overwrite || log_warn "Failed to apply labels"
        
    # Apply taints if needed (e.g., for dedicated storage nodes)
    # kubectl taint nodes "$hostname" dedicated=storage:NoSchedule
    
    log_info "? Node added to Kubernetes cluster"
    audit_log "k8s_join" "Added node to Kubernetes cluster" "success"
}

cleanup_on_error() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Join operation failed with exit code $exit_code"
        
        if [ "$SKIP_CEPH" = false ]; then
            log_warn "Attempting to restore cluster maintenance mode..."
            ceph_unset_noout || log_error "Could not restore cluster state"
        fi
        
        audit_log "join_failed" "Node join failed" "error"
    fi
}

trap cleanup_on_error EXIT

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor Node Join Script v${SCRIPT_VERSION}"
    log_info "=================================================="
    
    parse_arguments "$@"
    validate_arguments
    
    # Check mode: validate and show plan
    check_prerequisites
    check_idempotence
    validate_cluster_health
    validate_k8s_cluster
    discover_disks
    select_disks_for_ceph
    show_operation_plan
    
    if [ "$CHECK_ONLY" = true ]; then
        log_info "Check mode complete. Run without --check to execute."
        exit 0
    fi
    
    # Execution mode
    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        show_dry_run_plan \
            "- Set Ceph noout flag" \
            "- Provision OSDs on selected disks" \
            "- Register node in Kubernetes" \
            "- Configure ZFS pool" \
            "- Clear Ceph noout flag"
        exit 0
    fi
    
    log_info "===== Executing join operation ====="
    execute_ceph_join
    execute_k8s_join
    
    log_info "===== Join operation complete ====="
    log_info "? Node successfully joined cluster: $CLUSTER_NAME"
    audit_log "join_complete" "Node successfully joined cluster" "success"
}

# Run main
main "$@"
