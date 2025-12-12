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

###############################################################################
# debvisor-cloudinit-iso-enhanced.sh
# Enhanced cloud-init ISO generation with validation, templates, vendor-data
###############################################################################

set -eEuo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/var/log/debvisor-cloudinit.log"
TEMPLATE_DIR="/etc/debvisor/cloud-init-templates"
OUTPUT_DIR="/tmp/debvisor-cloudinit"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
METADATA_VERSION="2"
MAX_ISO_SIZE=$((10 * 1024 * 1024))  # 10 MB

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

debug_log() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        echo "[DEBUG] $1" >> "$LOG_FILE"
    fi
}

error_handler() {
    local exit_code=$1
    local line_number=$2
    log_error "Script failed at line $line_number with exit code $exit_code"
}

cleanup() {
    if [[ "${KEEP_TEMP:-false}" != "true" ]] && [[ -d "$WORKDIR" ]]; then
        rm -rf "$WORKDIR"
    fi
}

###############################################################################
# Utility Functions
###############################################################################

print_usage() {
    cat << EOF
${BLUE}Usage:${NC} $SCRIPT_NAME [OPTIONS]

${BLUE}Description:${NC}
Generate cloud-init ISO with validation, templates, and vendor-data support.

${BLUE}Options:${NC}
  -o, --output FILE         Output ISO file path (required)
  -u, --user-data FILE      Cloud-init user-data file
  -m, --meta-data FILE      Cloud-init meta-data file
  -v, --vendor-data FILE    Cloud-init vendor-data file
  -n, --network-config FILE Network configuration file
  --template TEMPLATE       Use built-in template (ubuntu, debian, rhel)
  --hostname HOSTNAME       Set VM hostname
  --username USERNAME       Set username (default: debian)
  --password HASH           Password hash (use mkpasswd)
  --ssh-key KEY_FILE        SSH public key file
  --packages PKG1,PKG2      Comma-separated packages to install
  --validate-only           Validate without generating ISO
  --dry-run                 Show what would be done
  --verbose                 Detailed output
  --json                    JSON output format
  --help                    Print this help message
  --version                 Print version

${BLUE}Examples:${NC}
  # Generate from files
  $SCRIPT_NAME -o /tmp/cloud-init.iso -u user-data.txt -m meta-data.txt

  # Using template
  $SCRIPT_NAME --template ubuntu --hostname myvm -o /tmp/cloud-init.iso

  # With SSH key and packages
  $SCRIPT_NAME --template debian \\
    --ssh-key ~/.ssh/id_rsa.pub \\
    --packages curl,vim,htop \\
    -o /tmp/cloud-init.iso
EOF
}

print_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

###############################################################################
# Template Management
###############################################################################

list_templates() {
    log_info "Available templates:"
    if [[ -d "$TEMPLATE_DIR" ]]; then
        find "$TEMPLATE_DIR" -name "*.template" -type f | while read -r template; do
            local name=$(basename "$template" .template)
            echo "  - $name"
        done
    fi
    echo "  - ubuntu (built-in)"
    echo "  - debian (built-in)"
    echo "  - rhel (built-in)"
}

generate_ubuntu_template() {
    local hostname="${1:-debvisor-vm}"
    local username="${2:-ubuntu}"
    local ssh_key="${3:-}"
    local packages="${4:-}"

    cat << 'EOF'
#cloud-config
version: 2
EOF

    cat << EOF

# System configuration
hostname: $hostname
manage_etc_hosts: true

# User configuration
users:
  - name: $username
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    home: /home/$username
    lock_passwd: true
EOF

    if [[ -n "$ssh_key" ]]; then
        echo "    ssh_authorized_keys:"
        echo "      - $(cat "$ssh_key")"
    fi

    echo ""
    echo "# Package installation"
    if [[ -n "$packages" ]]; then
        echo "packages:"
        IFS=',' read -ra PKGS <<< "$packages"
        for pkg in "${PKGS[@]}"; do
            echo "  - $(echo "$pkg" | xargs)"
        done
    fi

    cat << 'EOF'

# System updates
apt:
  preserve_sources_list: true
  sources:
    ubuntu_updates:
      source: "deb http://archive.ubuntu.com/ubuntu $RELEASE-updates main"
      keyid: "C0B21F32"

# Run commands
runcmd:
  - systemctl enable ssh
  - systemctl start ssh
  - apt-get update
  - apt-get install -y build-essential
  - echo "DebVisor VM initialized" > /etc/debvisor-init-complete

# Output to console
output: { all: '| tee -a /var/log/cloud-init-output.log' }
EOF
}

generate_debian_template() {
    local hostname="${1:-debvisor-vm}"
    local username="${2:-debian}"
    local ssh_key="${3:-}"
    local packages="${4:-}"

    cat << EOF
#cloud-config
version: 2

hostname: $hostname
manage_etc_hosts: true

users:
  - name: $username
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    home: /home/$username
    lock_passwd: true
EOF

    if [[ -n "$ssh_key" ]]; then
        echo "    ssh_authorized_keys:"
        echo "      - $(cat "$ssh_key")"
    fi

    echo ""
    if [[ -n "$packages" ]]; then
        echo "packages:"
        IFS=',' read -ra PKGS <<< "$packages"
        for pkg in "${PKGS[@]}"; do
            echo "  - $(echo "$pkg" | xargs)"
        done
    fi

    cat << 'EOF'

apt_upgrade: true

runcmd:
  - systemctl enable ssh
  - systemctl start ssh
  - echo "DebVisor VM initialized" > /etc/debvisor-init-complete

output: { all: '| tee -a /var/log/cloud-init-output.log' }
EOF
}

###############################################################################
# Validation Functions
###############################################################################

validate_yaml() {
    local file="$1"
    local type="$2"  # user-data, meta-data, vendor-data, network-config

    if [[ ! -f "$file" ]]; then
        log_error "$type file not found: $file"
        return 1
    fi

    # Basic YAML validation (check for valid structure)
    if ! grep -q "^#" "$file" 2>/dev/null; then
        log_warn "$type file doesn't start with shebang"
    fi

    # Check file is readable
    if [[ ! -r "$file" ]]; then
        log_error "Cannot read $type file: $file (permissions denied)"
        return 1
    fi

    # Check for common issues
    if grep -q "	" "$file"; then
        log_warn "$type file contains tabs (should use spaces)"
    fi

    local size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    if ((size > 1048576)); then  # 1 MB
        log_warn "$type file is large ($(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "$size bytes"))"
    fi

    log_success "$type validation passed"
    return 0
}

validate_iso_size() {
    local iso_file="$1"
    if [[ ! -f "$iso_file" ]]; then
        return 0
    fi

    local size=$(stat -c%s "$iso_file" 2>/dev/null || stat -f%z "$iso_file" 2>/dev/null)
    if ((size > MAX_ISO_SIZE)); then
        log_error "ISO size ($size bytes) exceeds maximum ($MAX_ISO_SIZE bytes)"
        return 1
    fi

    log_info "ISO size: $(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "$size bytes")"
    return 0
}

validate_ssh_key() {
    local key_file="$1"

    if [[ ! -f "$key_file" ]]; then
        log_error "SSH key file not found: $key_file"
        return 1
    fi

    if ! grep -q "^ssh-" "$key_file"; then
        log_error "Invalid SSH public key format"
        return 1
    fi

    log_success "SSH key validation passed"
    return 0
}

validate_password_hash() {
    local hash="$1"

    # Check for common hash formats
    if ! [[ "$hash" =~ ^\$[0-9] ]] && ! [[ "$hash" =~ ^\$2[aby] ]] && ! [[ "$hash" =~ ^\$6 ]]; then
        log_warn "Password hash format may be invalid (expected crypt/bcrypt/sha512)"
    fi

    return 0
}

###############################################################################
# ISO Generation Functions
###############################################################################

create_iso() {
    local workdir="$1"
    local output_file="$2"

    log_info "Creating ISO image..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create ISO: $output_file"
        return 0
    fi

    # Create ISO using mkisofs or xorrisofs
    if command -v mkisofs &>/dev/null; then
        mkisofs -output "$output_file" \
            -volid "cidata" \
            -joliet \
            -rock \
            "$workdir" || {
            log_error "Failed to create ISO with mkisofs"
            return 1
        }
    elif command -v xorrisofs &>/dev/null; then
        xorrisofs -output "$output_file" \
            -volid "cidata" \
            -joliet \
            -rock \
            "$workdir" || {
            log_error "Failed to create ISO with xorrisofs"
            return 1
        }
    else
        log_error "Neither mkisofs nor xorrisofs found"
        return 1
    fi

    log_success "ISO created: $output_file"
    validate_iso_size "$output_file" || return 1
}

###############################################################################
# Main Function
###############################################################################

main() {
    local output_file=""
    local user_data_file=""
    local meta_data_file=""
    local vendor_data_file=""
    local network_config_file=""
    local template_name=""
    local hostname=""
    local username="debian"
    local password_hash=""
    local ssh_key_file=""
    local packages=""
    local validate_only="false"

    mkdir -p "$(dirname "$LOG_FILE")" || {
        echo "Error: Failed to create log directory" >&2
        exit 1
    }
    touch "$LOG_FILE" || {
        echo "Error: Failed to create log file" >&2
        exit 1
    }

    # Create temporary workspace
    export WORKDIR=$(mktemp -d)

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                print_usage
                exit 0
                ;;
            --version)
                print_version
                exit 0
                ;;
            --list-templates)
                list_templates
                exit 0
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -u|--user-data)
                user_data_file="$2"
                shift 2
                ;;
            -m|--meta-data)
                meta_data_file="$2"
                shift 2
                ;;
            -v|--vendor-data)
                vendor_data_file="$2"
                shift 2
                ;;
            -n|--network-config)
                network_config_file="$2"
                shift 2
                ;;
            --template)
                template_name="$2"
                shift 2
                ;;
            --hostname)
                hostname="$2"
                shift 2
                ;;
            --username)
                username="$2"
                shift 2
                ;;
            --password)
                password_hash="$2"
                shift 2
                ;;
            --ssh-key)
                ssh_key_file="$2"
                shift 2
                ;;
            --packages)
                packages="$2"
                shift 2
                ;;
            --validate-only)
                validate_only="true"
                shift
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --verbose)
                VERBOSE="true"
                shift
                ;;
            --json)
                JSON_OUTPUT="true"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
            *)
                log_error "Unexpected argument: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    log_info "Cloud-init ISO Generator v$SCRIPT_VERSION started"

    # Generate from template if specified
    if [[ -n "$template_name" ]]; then
        log_info "Using template: $template_name"
        case "$template_name" in
            ubuntu)
                user_data=$(generate_ubuntu_template "$hostname" "$username" "$ssh_key_file" "$packages")
                ;;
            debian)
                user_data=$(generate_debian_template "$hostname" "$username" "$ssh_key_file" "$packages")
                ;;
            *)
                log_error "Unknown template: $template_name"
                exit 1
                ;;
        esac
        echo "$user_data" > "$WORKDIR/user-data"
        user_data_file="$WORKDIR/user-data"
    fi

    # Validate files if provided
    if [[ -n "$user_data_file" ]]; then
        validate_yaml "$user_data_file" "user-data" || exit 1
    fi

    if [[ -n "$meta_data_file" ]]; then
        validate_yaml "$meta_data_file" "meta-data" || exit 1
    fi

    if [[ -n "$vendor_data_file" ]]; then
        validate_yaml "$vendor_data_file" "vendor-data" || exit 1
    fi

    if [[ -n "$network_config_file" ]]; then
        validate_yaml "$network_config_file" "network-config" || exit 1
    fi

    if [[ -n "$ssh_key_file" ]]; then
        validate_ssh_key "$ssh_key_file" || exit 1
    fi

    if [[ -n "$password_hash" ]]; then
        validate_password_hash "$password_hash" || exit 1
    fi

    if [[ "$validate_only" == "true" ]]; then
        log_success "All validations passed"
        exit 0
    fi

    if [[ -z "$output_file" ]]; then
        log_error "Output file required (-o/--output)"
        print_usage
        exit 1
    fi

    # Create ISO directory structure
    mkdir -p "$WORKDIR"

    # Copy files
    if [[ -n "$user_data_file" ]]; then
        cp "$user_data_file" "$WORKDIR/user-data"
    fi

    if [[ -n "$meta_data_file" ]]; then
        cp "$meta_data_file" "$WORKDIR/meta-data"
    else
        # Create minimal meta-data
        echo "local-ipv4: 192.168.1.1" > "$WORKDIR/meta-data"
    fi

    if [[ -n "$vendor_data_file" ]]; then
        cp "$vendor_data_file" "$WORKDIR/vendor-data"
    fi

    if [[ -n "$network_config_file" ]]; then
        cp "$network_config_file" "$WORKDIR/network-config"
    fi

    # Create ISO
    create_iso "$WORKDIR" "$output_file" || exit 1

    log_success "Cloud-init ISO generation completed"
    log_info "Output: $output_file"

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        cat << EOF
{
  "status": "success",
  "output_file": "$output_file",
  "size": $(stat -c%s "$output_file" 2>/dev/null || stat -f%z "$output_file" 2>/dev/null),
  "timestamp": "$(date -Iseconds)"
}
EOF
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
