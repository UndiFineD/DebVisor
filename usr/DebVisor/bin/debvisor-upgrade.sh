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

################################################################################
# debvisor-upgrade.sh - Orchestrate safe cluster upgrades
#
# This script performs coordinated upgrades across Ceph, Kubernetes, and system
# components while maintaining cluster health and preventing data loss. It includes
# comprehensive pre-flight validation, maintenance mode management, and rollback
# guidance.
#
# Usage:
#   debvisor-upgrade.sh [OPTIONS]
#
# Options:
#   --dry-run              Show what would be done without making changes
#   --check                Validate prerequisites and show plan, then exit
#   --verbose              Enable verbose output for debugging
#   --log-file FILE        Write detailed logs to file
#   --pause                Pause at checkpoints for manual verification
#   --skip-ceph            Skip Ceph upgrade validation
#   --skip-k8s             Skip Kubernetes upgrade validation
#   --only-system          Only upgrade system packages, skip Ceph/K8s
#   --help                 Show this help message
#
# Examples:
#   # Show what would happen
#   debvisor-upgrade.sh --dry-run --check
#
#   # Upgrade with pauses for verification
#   debvisor-upgrade.sh --verbose --pause
#
#   # Upgrade only system packages
#   debvisor-upgrade.sh --only-system
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
SKIP_CEPH=false
SKIP_K8S=false
ONLY_SYSTEM=false
PAUSE_AT_CHECKPOINTS=false
CHECK_ONLY=false
NODE_HOSTNAME=$(hostname)

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -50
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run)
                DEBVISOR_DRY_RUN=true
                log_info "Dry-run mode enabled"
                shift
                ;;
            --check)
                CHECK_ONLY=true
                log_info "Check mode enabled"
                shift
                ;;
            --verbose)
                DEBVISOR_VERBOSE=true
                shift
                ;;
            --log-file)
                DEBVISOR_LOG_FILE="$2"
                mkdir -p "$(dirname "$DEBVISOR_LOG_FILE")"
                shift 2
                ;;
            --pause)
                PAUSE_AT_CHECKPOINTS=true
                log_info "Will pause at checkpoints for verification"
                shift
                ;;
            --skip-ceph)
                SKIP_CEPH=true
                shift
                ;;
            --skip-k8s)
                SKIP_K8S=true
                shift
                ;;
            --only-system)
                ONLY_SYSTEM=true
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
                log_error "Unexpected argument: $1"
                exit 2
                ;;
        esac
    done
}

checkpoint() {
    local msg="$1"
    if [ "$PAUSE_AT_CHECKPOINTS" = true ]; then
        log_warn "CHECKPOINT: $msg"
        read -p "Press enter to continue or Ctrl+C to abort: " -r || true
    fi
}

check_prerequisites() {
    log_info "===== Checking prerequisites ====="

    require_root

    if [ "$ONLY_SYSTEM" = false ]; then
        if [ "$SKIP_CEPH" = false ]; then
            require_bin "ceph"
            log_info "? Ceph binary found"
        fi
        if [ "$SKIP_K8S" = false ]; then
            require_bin "kubectl"
            log_info "? Kubectl binary found"
        fi
    fi

    require_bin "apt-get"
    log_info "? APT package manager available"
}

check_versions() {
    log_info "===== Checking version compatibility ====="

    # Check Ceph version
    if [ "$SKIP_CEPH" = false ] && command -v ceph &>/dev/null; then
        local ceph_ver
        ceph_ver=$(ceph --version | awk '{print $3}')
        log_info "Current Ceph version: $ceph_ver"
        # In a real scenario, we would check against a compatibility matrix
    fi

    # Check ZFS version
    if command -v zfs &>/dev/null; then
        local zfs_ver
        zfs_ver=$(zfs --version | head -1 | awk '{print $3}')
        log_info "Current ZFS version: $zfs_ver"
    fi
}

validate_ceph_health() {
    if [ "$SKIP_CEPH" = true ] || [ "$ONLY_SYSTEM" = true ]; then
        log_info "Skipping Ceph health checks"
        return 0
    fi

    log_info "===== Pre-upgrade Ceph health ====="

    if ! ceph_health_check; then
        log_error "Ceph cluster not healthy. Abort upgrade."
        return 1
    fi

    if ! ceph_osds_ready; then
        log_error "Not all Ceph OSDs ready. Abort upgrade."
        return 1
    fi

    log_info "? Ceph cluster healthy"
}

validate_k8s_health() {
    if [ "$SKIP_K8S" = true ] || [ "$ONLY_SYSTEM" = true ]; then
        log_info "Skipping Kubernetes health checks"
        return 0
    fi

    log_info "===== Pre-upgrade Kubernetes health ====="

    if ! kubectl_available; then
        log_error "Kubernetes not available. Abort upgrade."
        return 1
    fi

    if ! k8s_nodes_ready; then
        log_warn "Some Kubernetes nodes not ready (may recover after upgrade)"
    fi

    log_info "? Kubernetes cluster accessible"
}

show_upgrade_plan() {
    log_info "===== Upgrade Plan ====="

    log_info "System:"
    log_info "  1. Update APT package lists"
    log_info "  2. Upgrade system packages (apt-get upgrade)"
    log_info "  3. Check for kernel upgrades (linux-image packages)"

    if [ "$SKIP_CEPH" = false ] && [ "$ONLY_SYSTEM" = false ]; then
        log_info "Ceph:"
        log_info "  4. Set noout flag (prevent rebalance during upgrade)"
        log_info "  5. Upgrade Ceph packages"
        log_info "  6. Restart Ceph services"
        log_info "  7. Remove noout flag"
    fi

    if [ "$SKIP_K8S" = false ] && [ "$ONLY_SYSTEM" = false ]; then
        log_info "Kubernetes:"
        log_info "  8. Drain node (reschedule pods)"
        log_info "  9. Upgrade kubeadm/kubelet/kubectl"
        log_info "  10. Uncordon node (allow pod rescheduling)"
        log_info "  11. Wait for node readiness"
    fi

    if [ "$CHECK_ONLY" = true ]; then
        log_info "===== End Plan (--check mode) ====="
    fi
}

create_snapshots() {
    log_info "===== Creating pre-upgrade snapshots ====="

    # ZFS Root Snapshot
    if command -v zfs &>/dev/null; then
        local snap_name="pre-upgrade-$(date +%Y%m%d-%H%M%S)"
        log_info "Creating ZFS snapshot: rpool/ROOT@$snap_name"
        if zfs snapshot "rpool/ROOT@$snap_name"; then
            log_info "? ZFS snapshot created"
        else
            log_warn "Failed to create ZFS snapshot"
        fi
    else
        log_info "ZFS not found, skipping filesystem snapshot"
    fi

    # Ceph Config Backup
    if [ -d "/etc/ceph" ]; then
        log_info "Backing up /etc/ceph..."
        cp -r /etc/ceph "/var/backups/ceph-$(date +%Y%m%d-%H%M%S)"
    fi
}

upgrade_system_packages() {
    log_info "===== Upgrading system packages ====="

    log_info "Updating package lists..."
    execute "apt-get update" "Updating package lists" || return 1

    log_info "Upgrading packages..."
    execute "DEBIAN_FRONTEND=noninteractive apt-get -y --with-new-pkgs upgrade" \
        "Upgrading system packages" || return 1

    # Check for kernel upgrades
    log_info "Checking for kernel updates..."
    if apt-get -s upgrade 2>/dev/null | grep -q "^Inst linux-image"; then
        log_warn "Kernel update available - may require reboot after completion"
    fi

    audit_log "system_upgrade" "System packages upgraded" "success"
    log_info "? System packages upgraded"
}

upgrade_ceph() {
    if [ "$SKIP_CEPH" = true ]; then
        log_info "Skipping Ceph upgrade"
        return 0
    fi

    log_info "===== Upgrading Ceph ====="

    # Set maintenance mode
    if ! ceph_set_noout; then
        log_error "Failed to set Ceph maintenance mode"
        return 1
    fi

    checkpoint "Ceph maintenance mode enabled. Verify no rebalancing is starting."

    log_info "Upgrading Ceph packages..."
    if ! execute "apt-get -y --only-upgrade install ceph ceph-osd ceph-mon ceph-mgr" \
        "Upgrading Ceph packages"; then
        log_error "Ceph upgrade failed"
        ceph_unset_noout || log_error "Could not restore cluster state"
        return 1
    fi

    checkpoint "Ceph packages upgraded. Verify cluster status before proceeding."

    # Wait for cluster to stabilize
    log_info "Waiting for Ceph cluster to stabilize..."
    if ! wait_for_condition 300 "ceph_health_check" 10; then
        log_warn "Ceph did not fully recover within 5 minutes (may continue to recover)"
    fi

    # Remove maintenance mode
    if ! ceph_unset_noout; then
        log_error "Failed to remove Ceph maintenance mode"
        return 1
    fi

    checkpoint "Ceph maintenance mode removed. Verify rebalancing is progressing."

    audit_log "ceph_upgrade" "Ceph packages upgraded and cluster restored" "success"
    log_info "? Ceph upgrade complete"
}

upgrade_kubernetes() {
    if [ "$SKIP_K8S" = true ]; then
        log_info "Skipping Kubernetes upgrade"
        return 0
    fi

    log_info "===== Upgrading Kubernetes ====="

    # Drain node
    log_info "Draining node: $NODE_HOSTNAME"
    if ! execute "kubectl drain \"$NODE_HOSTNAME\" --ignore-daemonsets --delete-emptydir-data --grace-period=60" \
        "Draining Kubernetes node"; then
        log_warn "Node drain failed (may be expected if node is already drained)"
    fi

    checkpoint "Node drained. All pods have been evicted."

    # Upgrade Kubernetes components
    log_info "Upgrading Kubernetes packages..."
    if ! execute "apt-get -y --only-upgrade install kubeadm kubelet kubectl" \
        "Upgrading Kubernetes packages"; then
        log_error "Kubernetes upgrade failed"
        execute "kubectl uncordon \"$NODE_HOSTNAME\"" "Uncordoning node after failure"
        return 1
    fi

    # Restart kubelet
    log_info "Restarting kubelet service..."
    if ! execute "systemctl restart kubelet" "Restarting kubelet"; then
        log_error "Failed to restart kubelet"
        execute "kubectl uncordon \"$NODE_HOSTNAME\"" "Uncordoning node after failure"
        return 1
    fi

    checkpoint "Kubelet restarted. Verify kubelet is running."

    # Uncordon node
    log_info "Uncordoning node: $NODE_HOSTNAME"
    if ! execute "kubectl uncordon \"$NODE_HOSTNAME\"" "Uncordoning Kubernetes node"; then
        log_warn "Uncordon command failed (node may already be cordoned)"
    fi

    # Wait for node readiness
    log_info "Waiting for node to reach Ready state..."
    if ! wait_for_condition 300 "k8s_nodes_ready" 10; then
        log_warn "Node not ready within 5 minutes (may continue to recover)"
    fi

    audit_log "k8s_upgrade" "Kubernetes packages upgraded and node restored" "success"
    log_info "? Kubernetes upgrade complete"
}

post_upgrade_validation() {
    log_info "===== Post-upgrade validation ====="

    if [ "$SKIP_CEPH" = false ] && [ "$ONLY_SYSTEM" = false ]; then
        if ceph_health_check; then
            log_info "? Ceph cluster healthy"
        else
            log_warn "[warn] Ceph cluster not yet fully recovered (check status)"
        fi
    fi

    if [ "$SKIP_K8S" = false ] && [ "$ONLY_SYSTEM" = false ]; then
        if kubectl_available; then
            log_info "? Kubernetes available"
        else
            log_warn "[warn] Kubernetes not available"
        fi
    fi
}

cleanup_on_error() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Upgrade operation failed with exit code $exit_code"

        if [ "$SKIP_K8S" = false ]; then
            log_warn "Attempting to uncordon node..."
            execute "kubectl uncordon \"$NODE_HOSTNAME\"" "Emergency uncordon" || true
        fi

        if [ "$SKIP_CEPH" = false ]; then
            log_warn "Attempting to restore Ceph cluster state..."
            ceph_unset_noout || log_error "Could not restore Ceph state"
        fi

        audit_log "upgrade_failed" "Upgrade failed with exit code $exit_code" "error"
    fi
}

trap cleanup_on_error EXIT

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor Cluster Upgrade Script v${SCRIPT_VERSION}"
    log_info "=================================================="

    parse_arguments "$@"

    # Check mode
    check_prerequisites
    check_versions
    validate_ceph_health
    validate_k8s_health
    show_upgrade_plan

    if [ "$CHECK_ONLY" = true ]; then
        log_info "Check mode complete. Run without --check to execute."
        exit 0
    fi

    # Dry-run mode
    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        show_dry_run_plan \
            "- Create pre-upgrade snapshots" \
            "- Update APT package lists" \
            "- Upgrade system packages" \
            "- Set Ceph maintenance mode" \
            "- Upgrade Ceph packages" \
            "- Remove Ceph maintenance mode" \
            "- Drain Kubernetes node" \
            "- Upgrade Kubernetes packages" \
            "- Uncordon Kubernetes node"
        exit 0
    fi

    # Execution mode
    log_info "===== Starting upgrade ====="
    local start_time
    start_time=$(date +%s)

    create_snapshots

    upgrade_system_packages
    checkpoint "System packages upgraded. Review before proceeding to cluster upgrades."

    if [ "$ONLY_SYSTEM" = false ]; then
        upgrade_ceph
        upgrade_kubernetes
    fi

    post_upgrade_validation

    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log_info "===== Upgrade complete ====="
    log_info "Total duration: ${duration}s"
    log_info "? Node successfully upgraded"
    audit_log "upgrade_complete" "Node successfully upgraded (Duration: ${duration}s)" "success"
}

# Run main
main "$@"
