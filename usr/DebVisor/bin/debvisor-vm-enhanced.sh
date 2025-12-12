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

###############################################################################
# debvisor-vm-enhanced.sh
# Enhanced VM management scripts with idempotence, pre-checks, and logging
###############################################################################

set -eEuo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/var/log/debvisor-vm.log"
AUDIT_LOG="/var/log/debvisor-vm-audit.log"
STATE_DIR="/var/lib/debvisor/vm-state"
LOCK_DIR="/var/run/debvisor/vm-locks"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Error handling
trap 'error_handler $? $LINENO' ERR
trap 'cleanup' EXIT

###############################################################################
# Logging Functions
###############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

audit_log_entry() {
    local action="$1"
    local vm_name="$2"
    local status="$3"
    local details="${4:-}"

    local timestamp=$(date -Iseconds)
    local user="${SUDO_USER:-${USER:-unknown}}"

    mkdir -p "$(dirname "$AUDIT_LOG")"
    echo "$timestamp | $user | $action | $vm_name | $status | $details" >> "$AUDIT_LOG"
}

error_handler() {
    local exit_code=$1
    local line_number=$2
    log_error "Script failed at line $line_number with exit code $exit_code"
}

cleanup() {
    debug_log "Cleanup completed"
}

debug_log() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        echo "[DEBUG] $1" >> "$LOG_FILE"
    fi
}

###############################################################################
# Utility Functions
###############################################################################

print_usage() {
    cat << EOF
${BLUE}Usage:${NC} $SCRIPT_NAME COMMAND [OPTIONS]

${BLUE}Commands:${NC}
  register VM_NAME          Register VM for management
  convert VM_NAME           Convert VM disk format
  health-check [VM_NAME]    Check VM/cluster health

${BLUE}Global Options:${NC}
  --dry-run                 Show what would be done
  --verbose                 Detailed output
  --force                   Force operation even if checks fail
  --json                    JSON output format
  --help                    Print this help message
  --version                 Print version

${BLUE}Examples:${NC}
  $SCRIPT_NAME register myvm
  $SCRIPT_NAME convert myvm
  $SCRIPT_NAME health-check
EOF
}

print_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

acquire_lock() {
    local lock_name="$1"
    local lock_file="$LOCK_DIR/$lock_name.lock"

    mkdir -p "$LOCK_DIR"

    # Try to acquire lock
    if ! mkdir "$lock_file" 2>/dev/null; then
        log_error "Could not acquire lock: $lock_name (already in progress)"
        return 1
    fi

    # Create lock cleanup
    # Expand lock_file now but follow ShellCheck SC2064 recommendation
    trap 'rmdir "'"$lock_file"'" 2>/dev/null || true' EXIT

    debug_log "Lock acquired: $lock_name"
    return 0
}

is_idempotent() {
    local operation="$1"
    local vm_name="$2"

    local state_file="$STATE_DIR/${vm_name}.${operation}.state"

    if [[ -f "$state_file" ]]; then
        local last_run=$(stat -c %Y "$state_file" 2>/dev/null || stat -f %m "$state_file" 2>/dev/null)
        local now=$(date +%s)
        local elapsed=$((now - last_run))

        # Consider successful if run within last 24 hours
        if ((elapsed < 86400)); then
            log_info "Operation already completed (cached): $operation for $vm_name"
            return 0
        fi
    fi

    return 1
}

save_state() {
    local operation="$1"
    local vm_name="$2"
    local status="$3"

    mkdir -p "$STATE_DIR"
    local state_file="$STATE_DIR/${vm_name}.${operation}.state"

    cat > "$state_file" << EOF
{
  "operation": "$operation",
  "vm_name": "$vm_name",
  "status": "$status",
  "timestamp": "$(date -Iseconds)",
  "user": "${SUDO_USER:-${USER:-unknown}}"
}
EOF

    debug_log "State saved: $state_file"
}

###############################################################################
# Pre-check Functions
###############################################################################

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check required commands
    local required_commands=("virsh" "qemu-img" "ssh")

    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            log_warn "Optional command not found: $cmd"
        fi
    done

    # Check disk space
    local available_space=$(df /var/lib/libvirt | awk 'NR==2 {print $4}')
    if ((available_space < 10485760)); then  # 10 GB
        log_warn "Low disk space: $(numfmt --to=iec-i --suffix=B "$available_space" 2>/dev/null || echo "$available_space KB")"
    fi

    log_success "Prerequisites check completed"
}

check_vm_exists() {
    local vm_name="$1"

    if ! virsh list --all | grep -qw "$vm_name"; then
        log_error "VM not found: $vm_name"
        return 1
    fi

    debug_log "VM exists: $vm_name"
    return 0
}

check_vm_running() {
    local vm_name="$1"

    if virsh list | grep -q "$vm_name.*running"; then
        return 0
    fi

    return 1
}

###############################################################################
# VM Registration
###############################################################################

register_vm() {
    local vm_name="$1"

    log_info "Registering VM: $vm_name"

    # Check idempotence
    if [[ "${FORCE:-false}" != "true" ]] && is_idempotent "register" "$vm_name"; then
        log_success "VM already registered: $vm_name"
        audit_log_entry "register" "$vm_name" "skipped" "already_registered"
        return 0
    fi

    # Acquire lock
    acquire_lock "register-$vm_name" || return 1

    # Pre-flight checks
    check_prerequisites || return 1

    if ! check_vm_exists "$vm_name"; then
        log_error "Cannot register non-existent VM: $vm_name"
        audit_log_entry "register" "$vm_name" "failed" "vm_not_found"
        return 1
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would register VM: $vm_name"
        return 0
    fi

    # Create registration metadata
    mkdir -p "$STATE_DIR"
    local reg_file="$STATE_DIR/${vm_name}.registration"

    cat > "$reg_file" << EOF
{
  "vm_name": "$vm_name",
  "registered_at": "$(date -Iseconds)",
  "registered_by": "${SUDO_USER:-${USER:-unknown}}",
  "uuid": "$(virsh dominfo "$vm_name" | grep UUID | awk '{print $2}')",
  "state": "registered",
  "management_enabled": true
}
EOF

    chmod 600 "$reg_file"

    log_success "VM registered: $vm_name"
    save_state "register" "$vm_name" "success"
    audit_log_entry "register" "$vm_name" "success"

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        cat "$reg_file"
    fi
}

###############################################################################
# VM Disk Conversion
###############################################################################

convert_vm_disk() {
    local vm_name="$1"
    local target_format="${2:-qcow2}"

    log_info "Converting VM disk: $vm_name to $target_format"

    # Acquire lock
    acquire_lock "convert-$vm_name" || return 1

    # Pre-flight checks
    if ! check_vm_exists "$vm_name"; then
        log_error "VM not found: $vm_name"
        audit_log_entry "convert" "$vm_name" "failed" "vm_not_found"
        return 1
    fi

    if check_vm_running "$vm_name"; then
        if [[ "${FORCE:-false}" != "true" ]]; then
            log_error "VM is running, must shut down first"
            audit_log_entry "convert" "$vm_name" "failed" "vm_running"
            return 1
        fi
        log_warn "Force flag set, shutting down VM"
        virsh shutdown "$vm_name" --mode acpi
        sleep 10
    fi

    # Get disk path - robustly parse virsh domblklist output
    local disk_path
    disk_path=$(virsh domblklist "$vm_name" | awk 'NR>1 && NF>1 {print $2; exit}')

    # Validate the extracted path
    if [[ -z "$disk_path" ]]; then
        log_error "Could not determine disk path for VM: $vm_name"
        audit_log_entry "convert" "$vm_name" "failed" "disk_not_found"
        return 1
    fi

    # Check that the path exists and is a valid disk/block file
    if [[ ! -e "$disk_path" ]]; then
        log_error "Disk path does not exist: $disk_path"
        audit_log_entry "convert" "$vm_name" "failed" "disk_path_invalid"
        return 1
    fi

    if [[ ! -f "$disk_path" && ! -b "$disk_path" ]]; then
        log_error "Disk path is not a regular file or block device: $disk_path"
        audit_log_entry "convert" "$vm_name" "failed" "disk_path_invalid"
        return 1
    fi

    log_info "Disk path: $disk_path"

    # Check current format
    local current_format
    current_format=$(qemu-img info "$disk_path" | grep "file format" | awk '{print $3}')
    log_info "Current format: $current_format"

    if [[ "$current_format" == "$target_format" ]]; then
        log_success "Disk already in target format: $target_format"
        audit_log_entry "convert" "$vm_name" "skipped" "already_target_format"
        return 0
    fi

    # Create backup
    local backup_path="${disk_path}.backup-$(date +%Y%m%d-%H%M%S)"
    log_info "Creating backup: $backup_path"

    if [[ "$DRY_RUN" != "true" ]]; then
        cp "$disk_path" "$backup_path"
        log_success "Backup created: $backup_path"
    fi

    # Perform conversion
    log_info "Converting disk format..."

    if [[ "$DRY_RUN" != "true" ]]; then
        if ! qemu-img convert -f "$current_format" -O "$target_format" "$disk_path" "${disk_path}.new"; then
            log_error "Conversion failed"
            audit_log_entry "convert" "$vm_name" "failed" "conversion_error"
            return 1
        fi

        # Replace original with converted
        mv "${disk_path}.new" "$disk_path"
    else
        log_info "[DRY-RUN] Would convert $disk_path from $current_format to $target_format"
    fi

    log_success "Disk conversion completed: $vm_name"
    save_state "convert" "$vm_name" "success"
    audit_log_entry "convert" "$vm_name" "success"

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        cat << EOF
{
  "vm_name": "$vm_name",
  "original_format": "$current_format",
  "target_format": "$target_format",
  "disk_path": "$disk_path",
  "backup_path": "$backup_path",
  "status": "success"
}
EOF
    fi
}

###############################################################################
# Health Check
###############################################################################

health_check() {
    local vm_name="${1:-all}"

    log_info "Performing health check..."

    if [[ "$vm_name" == "all" ]]; then
        log_info "Checking all VMs..."
        local vm_list
        vm_list=$(virsh list --all | tail -n +3 | awk '{print $2}' | grep -v "^$")

        for vm in $vm_list; do
            check_single_vm "$vm" || true
        done
    else
        check_single_vm "$vm_name"
    fi

    log_success "Health check completed"
}

check_single_vm() {
    local vm_name="$1"

    log_info "Checking VM: $vm_name"

    # Check if running
    local vm_state
    vm_state=$(virsh domstate "$vm_name")
    log_info "  State: $vm_state"

    # Check disk usage
    local disk_path
    disk_path=$(virsh domblklist "$vm_name" 2>/dev/null | tail -1 | awk '{print $2}')

    if [[ -n "$disk_path" ]]; then
        local disk_size
        disk_size=$(qemu-img info "$disk_path" 2>/dev/null | grep "virtual size" | awk '{print $3}')
        log_info "  Disk: $disk_size"
    fi

    # Check memory
    local memory
    memory=$(virsh dominfo "$vm_name" | grep "Max memory" | awk '{print $3}')
    log_info "  Memory: $memory"
}

###############################################################################
# Main Function
###############################################################################

main() {
    # Create log directory with restrictive permissions
    local log_dir
    log_dir="$(dirname "$LOG_FILE")"
    if [[ ! -d "$log_dir" ]]; then
        mkdir -p "$log_dir"
        chmod 0700 "$log_dir"
    fi

    # Create LOG_FILE with secure permissions
    if [[ ! -f "$LOG_FILE" ]]; then
        touch "$LOG_FILE"
        chmod 0600 "$LOG_FILE"
    fi

    # Create AUDIT_LOG with secure permissions
    if [[ ! -f "$AUDIT_LOG" ]]; then
        touch "$AUDIT_LOG"
        chmod 0600 "$AUDIT_LOG"
    fi

    if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
    fi

    local command="$1"
    shift

    case "$command" in
        register)
            if [[ $# -lt 1 ]]; then
                log_error "VM name required"
                exit 1
            fi
            register_vm "$@"
            ;;
        convert)
            if [[ $# -lt 1 ]]; then
                log_error "VM name required"
                exit 1
            fi
            convert_vm_disk "$@"
            ;;
        health-check)
            health_check "$@"
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        --version)
            print_version
            exit 0
            ;;
        *)
            log_error "Unknown command: $command"
            print_usage
            exit 1
            ;;
    esac
}

# Parse global options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --verbose)
            VERBOSE="true"
            shift
            ;;
        --force)
            FORCE="true"
            shift
            ;;
        --json)
            JSON_OUTPUT="true"
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
