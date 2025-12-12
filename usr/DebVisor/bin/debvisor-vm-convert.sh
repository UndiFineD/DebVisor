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
# debvisor-vm-convert.sh - Enterprise VM Disk Converter
#
# This script converts VM disk images between formats (qcow2, raw, vmdk)
# with support for compression, progress monitoring, and integrity validation.
#
# Usage:
#   debvisor-vm-convert.sh [OPTIONS] --in SRC --out DEST
#
# Options:
#   --in FILE         Source disk image
#   --out FILE        Destination disk image
#   --from FORMAT     Source format (optional, auto-detected)
#   --to FORMAT       Destination format (default: qcow2)
#   --compress        Enable compression (qcow2 only)
#   --force           Overwrite destination if exists
#   --threads N       Number of coroutines (default: 8)
#   --dry-run         Show what would be done without making changes
#   --help            Show this help message
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

readonly SCRIPT_VERSION="2.0.0"
SRC_FILE=""
DEST_FILE=""
FROM_FMT=""
TO_FMT="qcow2"
COMPRESS=false
FORCE=false
THREADS=8

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -30
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --in)
                SRC_FILE="$2"
                shift 2
                ;;
            --out)
                DEST_FILE="$2"
                shift 2
                ;;
            --from)
                FROM_FMT="$2"
                shift 2
                ;;
            --to)
                TO_FMT="$2"
                shift 2
                ;;
            --compress)
                COMPRESS=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --threads)
                THREADS="$2"
                shift 2
                ;;
            --dry-run)
                DEBVISOR_DRY_RUN=true
                log_info "Dry-run mode enabled"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

validate_arguments() {
    if [ -z "$SRC_FILE" ] || [ -z "$DEST_FILE" ]; then
        log_error "--in and --out are required."
        show_help
        exit 1
    fi

    if [ ! -f "$SRC_FILE" ]; then
        log_error "Source file not found: $SRC_FILE"
        exit 1
    fi

    if [ -e "$DEST_FILE" ] && [ "$FORCE" = false ]; then
        log_error "Destination exists: $DEST_FILE (use --force to overwrite)"
        exit 1
    fi
}

detect_format() {
    if [ -z "$FROM_FMT" ]; then
        log_info "Auto-detecting source format..."
        FROM_FMT=$(qemu-img info --output=json "$SRC_FILE" | grep '"format":' | head -1 | awk -F'"' '{print $4}')
        if [ -z "$FROM_FMT" ]; then
            log_error "Could not detect format of $SRC_FILE"
            exit 1
        fi
        log_info "Detected source format: $FROM_FMT"
    fi
}

convert_image() {
    log_info "===== Starting conversion ====="
    log_info "Source: $SRC_FILE ($FROM_FMT)"
    log_info "Target: $DEST_FILE ($TO_FMT)"

    local -a opts
    opts=("-p" "-m" "$THREADS")

    if [ "$COMPRESS" = true ]; then
        if [ "$TO_FMT" == "qcow2" ]; then
            opts+=("-c")
            log_info "Compression enabled"
        else
            log_warn "Compression requested but not supported for format $TO_FMT (ignored)"
        fi
    fi

    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "Dry-run: qemu-img convert -f $FROM_FMT -O $TO_FMT ${opts[*]} $SRC_FILE $DEST_FILE"
        return 0
    fi

    mkdir -p "$(dirname "$DEST_FILE")"

    log_info "Converting..."
    if qemu-img convert -f "$FROM_FMT" -O "$TO_FMT" "${opts[@]}" "$SRC_FILE" "$DEST_FILE"; then
        log_info "? Conversion successful"
    else
        log_error "Conversion failed"
        # Cleanup partial file
        if [ -f "$DEST_FILE" ]; then
            rm -f "$DEST_FILE"
        fi
        return 1
    fi
}

verify_image() {
    if [ "$DEBVISOR_DRY_RUN" = true ]; then return 0; fi

    log_info "===== Verifying image ====="

    if ! qemu-img info "$DEST_FILE" &>/dev/null; then
        log_error "Generated image is invalid or corrupt"
        return 1
    fi

    local size
    size=$(du -h "$DEST_FILE" | cut -f1)
    log_info "Output size: $size"

    if [ "$TO_FMT" == "qcow2" ]; then
        log_info "Checking qcow2 consistency..."
        if qemu-img check "$DEST_FILE" &>/dev/null; then
            log_info "? Consistency check passed"
        else
            log_warn "Consistency check reported issues (run 'qemu-img check' manually for details)"
        fi
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor VM Converter v${SCRIPT_VERSION}"

    require_bin "qemu-img"

    parse_arguments "$@"
    validate_arguments
    detect_format
    convert_image
    verify_image

    audit_log "vm_convert" "Converted $SRC_FILE to $DEST_FILE ($TO_FMT)" "success"
}

# Run main
main "$@"
