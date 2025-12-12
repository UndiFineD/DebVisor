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

#!/usr/bin/env bash
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

set -euo pipefail

log(){ echo "[debvisor-firstboot] $*"; }

MODE="lab"
PROFILE="ceph"
OS_DISK=""
STORAGE_DISKS=()
USB_DISKS=()
DRY_RUN="false"

parse_args(){
  while [[ ${1-} ]]; do
    case "$1" in
      --dry-run)
        DRY_RUN="true"
        ;;
    esac
    shift || break
  done
  if [[ "$DRY_RUN" == "true" ]]; then
    log "Running in DRY-RUN mode: no destructive actions will be taken"
  fi
}

load_profile_and_mode(){
  if [[ -f /etc/debvisor-profile ]]; then
    # shellcheck disable=SC1091
    source /etc/debvisor-profile || true
  fi
  PROFILE=${PROFILE:-ceph}

  if [[ -f /etc/debvisor-mode ]]; then
    MODE=$(tr '[:upper:]' '[:lower:]' </etc/debvisor-mode | awk 'NF{print $1; exit}')
  fi
  MODE=${MODE:-lab}
  case "$MODE" in
    prod|production) MODE="prod" ;;
    lab|dev|development) MODE="lab" ;;
    *) MODE="lab" ;;
  esac

  log "Using profile: $PROFILE"
  log "Using mode: $MODE"
}

init_logging(){
  mkdir -p /var/log/debvisor
}

mark_step(){
  # mark_step <name> <status>
  local name="$1" status="$2"
  echo "${status}" >"/var/log/debvisor/${name}.status" || true
}

ensure_base_services(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would ensure base services (cockpit, libvirtd, KVM modules)"
    return 0
  fi
  systemctl enable --now cockpit.socket || true
  modprobe kvm || true
  modprobe kvm_intel || modprobe kvm_amd || true
  systemctl enable --now libvirtd || true
}

ensure_webpanel_user(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would ensure webpanel system user and ownership of /opt/debvisor/panel"
    return 0
  fi

  if command -v debvisor-setup-webpanel-user.sh &>/dev/null; then
    debvisor-setup-webpanel-user.sh || true
  elif [[ -x /usr/local/sbin/debvisor-setup-webpanel-user.sh ]]; then
    /usr/local/sbin/debvisor-setup-webpanel-user.sh || true
  else
    log "webpanel setup helper not found; ensure user/group 'webpanel' exist if panel is enabled"
  fi
}

ensure_rpc_user(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would ensure debvisor-rpc system user and ownership of /opt/debvisor/rpc"
    return 0
  fi

  if command -v debvisor-setup-rpc-user.sh &>/dev/null; then
    debvisor-setup-rpc-user.sh || true
  elif [[ -x /usr/local/sbin/debvisor-setup-rpc-user.sh ]]; then
    /usr/local/sbin/debvisor-setup-rpc-user.sh || true
  else
    log "RPC setup helper not found; ensure user/group 'debvisor-rpc' exist if rpcd is enabled"
  fi
}

ensure_tsig_rotator_user(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would ensure tsig-rotator system user for TSIG rotation"
    return 0
  fi

  if id tsig-rotator &>/dev/null; then
    log "tsig-rotator user already exists"
    return 0
  fi

  log "Creating tsig-rotator system user"
  adduser --system --group --no-create-home tsig-rotator || true
}

generate_keys(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would generate SSH keys, Internal CA, and Service Secrets"
    return 0
  fi

  log "Generating cryptographic keys and secrets..."
  if [[ -f /opt/tools/first_boot_keygen.py ]]; then
    python3 /opt/tools/first_boot_keygen.py || log "Key generation failed (non-fatal)"
  else
    log "Key generation script not found at /opt/tools/first_boot_keygen.py"
  fi
  mark_step keys success
}

configure_ups(){
  # Enable NUT services only if a UPS configuration exists.
  if [[ "$DRY_RUN" == "true" ]]; then
    if [[ -s /etc/nut/ups.conf ]]; then
      log "[dry-run] Would enable and start NUT UPS services (nut-server, nut-monitor)"
    else
      log "[dry-run] No UPS configuration found; NUT services remain disabled"
    fi
    return 0
  fi

  if [[ -s /etc/nut/ups.conf ]]; then
    log "UPS configuration detected; enabling NUT services"
    systemctl enable --now nut-server.service || true
    systemctl enable --now nut-monitor.service || true
    mark_step ups enabled
  else
    log "No UPS configuration detected in /etc/nut/ups.conf; leaving NUT services disabled"
    mark_step ups skipped
  fi
}

configure_locale_time(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would configure locale and timezone"
    return 0
  fi
  localectl set-locale LANG=en_US.UTF-8 || true
  timedatectl set-timezone UTC || true
}

configure_accounts(){
  # In prod mode, do not auto-create node/monitor; only ensure root exists.
  local users=(root)
  if [[ "$MODE" == "lab" ]]; then
    users=(root node monitor)
  fi

  for u in "${users[@]}"; do
    if ! id "$u" &>/dev/null; then
      if [[ "$DRY_RUN" == "true" ]]; then
        log "[dry-run] Would create missing user: $u"
      else
        log "Creating missing user: $u"
        adduser --disabled-password --gecos "" "$u"
      fi
    fi
    if [[ "$u" != "root" ]]; then
      if [[ "$DRY_RUN" == "true" ]]; then
        log "[dry-run] Would lock user: $u"
      else
        usermod -L "$u" || true
      fi
    fi
  done

  if [[ "$MODE" == "lab" ]]; then
    log "Lab mode: node/monitor created and locked; set passwords as needed."
  else
    log "Prod mode: only root ensured; create additional accounts via your workflow."
  fi
}

configure_networking(){
  local PRIMARY_DEV
  PRIMARY_DEV=$(ip -o link show | awk -F': ' '/state UP/ && $2 !~ /^lo$/ {print $2; exit}')
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would configure bridge br0 on primary device: ${PRIMARY_DEV:-<none>} with STP disabled"
    return 0
  fi
  if ! ip link show br0 &>/dev/null; then
    ip link add name br0 type bridge || true
    # Disable STP to prevent topology change notifications and singing
    ip link set br0 type bridge stp_state 0 || true
    # Set ageing time and forward delay for stability
    ip link set br0 type bridge ageing_time 30000 || true
    ip link set br0 type bridge forward_delay 0 || true
  fi
  if [[ -n "${PRIMARY_DEV:-}" ]]; then
    ip link set "$PRIMARY_DEV" master br0 || true
  fi
  ip link set br0 up || true
  log "Bridge br0 configured (primary=$PRIMARY_DEV, STP disabled)"
}

detect_disks(){
  # Prefer stable by-id names where available
  local root_dev byid_root
  root_dev=$(findmnt -no SOURCE / || true)
  if [[ -n "$root_dev" ]]; then
    root_dev=${root_dev#/dev/}
    root_dev=${root_dev%%[0-9]*}
  fi
  if [[ -n "$root_dev" && -e "/dev/$root_dev" ]]; then
    # shellcheck disable=SC2010
    byid_root=$(ls -1 /dev/disk/by-id 2>/dev/null | grep -m1 "$root_dev" || true)
  fi
  if [[ -n "$byid_root" ]]; then
    OS_DISK="/dev/disk/by-id/$byid_root"
  else
    OS_DISK="/dev/${root_dev:-}"
  fi
  mapfile -t STORAGE_DISKS < <(lsblk -ndo NAME,TYPE | awk '$2=="disk"{print $1}')
  if [[ -n "$root_dev" ]]; then
    mapfile -t STORAGE_DISKS < <(printf '%s\n' "${STORAGE_DISKS[@]}" | grep -v "^${root_dev}$" || true)
  fi
  log "OS disk: ${OS_DISK:-<unknown>}"
  log "Storage disks (by kernel name, will map to by-id for provisioning): ${STORAGE_DISKS[*]:-<none>}"
}

detect_usb_disks(){
  USB_DISKS=()
  # A disk is considered USB/removable if /sys/block/<dev>/removable == 1
  for dev in $(lsblk -ndo NAME,TYPE | awk '$2=="disk"{print $1}'); do
    if [[ -f "/sys/block/${dev}/removable" ]] && [[ "$(<"/sys/block/${dev}/removable")" == "1" ]]; then
      # Skip the OS disk if it happens to be removable
      if [[ -n "$OS_DISK" && "$dev" == "$OS_DISK" ]]; then
        continue
      fi
      USB_DISKS+=("$dev")
    fi
  done
  log "USB disks: ${USB_DISKS[*]:-<none>}"
}

ceph_provision(){
  if [[ "$PROFILE" != "ceph" && "$PROFILE" != "mixed" ]]; then
    return 0
  fi

  if command -v ceph &>/dev/null && ceph status &>/dev/null; then
    log "Ceph already appears configured; skipping provisioning."
    mark_step ceph success
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would provision Ceph single-node using storage disks: ${STORAGE_DISKS[*]:-<none>}"
    mark_step ceph skipped
    return 0
  fi

  log "Provisioning Ceph single-node"
  mkdir -p /var/lib/ceph
  FSID=$(uuidgen)
  cat >/etc/ceph/ceph.conf <<EOF
[global]
fsid = $FSID
mon_allow_pool_delete = true
osd_pool_default_size = 1
osd_pool_default_min_size = 1
public_network = 0.0.0.0/0
cluster_network = 0.0.0.0/0
EOF
  HOSTNAME=$(hostnamectl --static)
  ceph-authtool --create-keyring /etc/ceph/ceph.mon.keyring --gen-key -n mon. --cap mon 'allow *' || true
  mkdir -p "/var/lib/ceph/mon/ceph-$HOSTNAME"
  ceph-mon --mkfs -i "$HOSTNAME" --keyring /etc/ceph/ceph.mon.keyring || true
  systemctl enable --now ceph-mon@"$HOSTNAME" || true
  systemctl enable --now ceph-mgr@"$HOSTNAME" || true

  for dev in "${STORAGE_DISKS[@]}"; do
    # Skip disks that already have a filesystem or partition table
    if blkid "/dev/$dev" &>/dev/null; then
      log "Skipping /dev/$dev (appears to contain data)"
      continue
    fi
    wipefs -a "/dev/$dev" || true
    ceph-volume lvm create --data "/dev/$dev" || true
  done

  systemctl enable --now ceph-mds@"$HOSTNAME" || true
  ceph osd pool create rbd 64 || true
  rbd pool init rbd || true
  ceph osd pool create cephfs.data 64 || true
  ceph osd pool create cephfs.meta 32 || true
  ceph fs new cephfs cephfs.meta cephfs.data || true
  mkdir -p /srv/cephfs
  ceph auth get-or-create client.admin mon 'allow *' osd 'allow *' mds 'allow *' || true
  echo "cephfs /srv/cephfs fuse.ceph ceph.id=admin,_netdev 0 2" >> /etc/fstab
  mount -a || true
  log "CephFS mounted at /srv/cephfs"
  mark_step ceph success
}

zfs_provision(){
  if [[ "$PROFILE" != "zfs" && "$PROFILE" != "mixed" ]]; then
    return 0
  fi

  if command -v zpool &>/dev/null && zpool list tank &>/dev/null; then
    log "ZFS pool 'tank' already exists; skipping provisioning."
    mark_step zfs success
    return 0
  fi

  if [[ ${#STORAGE_DISKS[@]} -eq 0 ]]; then
    log "No extra disks for ZFS"
    mark_step zfs skipped
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would provision ZFS pool 'tank' using storage disks: ${STORAGE_DISKS[*]:-<none>}"
    mark_step zfs skipped
    return 0
  fi

  log "Provisioning ZFS pool"
  modprobe zfs || true
  local WIPED=()
  for d in "${STORAGE_DISKS[@]}"; do
    if blkid "/dev/$d" &>/dev/null; then
      log "Skipping /dev/$d for ZFS (appears to contain data)"
      continue
    fi
    wipefs -a "/dev/$d" || true
    WIPED+=("/dev/$d")
  done

  if [[ ${#WIPED[@]} -eq 0 ]]; then
    log "No suitable empty disks for ZFS; skipping pool creation."
    mark_step zfs skipped
    return 0
  fi

  zpool create -f tank "${WIPED[@]}" || true
  zfs set compression=lz4 tank || true
  for ds in vm docker k8s; do
    zfs create -o mountpoint=/srv/$ds tank/$ds || true
  done
  log "ZFS pool tank ready"
  mark_step zfs success
}

zfs_provision_usb_pool(){
  # usb-zfs profile: build a ZFS pool across removable USB disks only.
  if [[ "$PROFILE" != "usb-zfs" ]]; then
    return 0
  fi

  if command -v zpool &>/dev/null && zpool list tank &>/dev/null; then
    log "ZFS pool 'tank' already exists; skipping USB provisioning."
    mark_step zfs success
    return 0
  fi

  if [[ ${#USB_DISKS[@]} -lt 3 ]]; then
    log "Not enough USB disks for usb-zfs profile (need at least 3), found: ${USB_DISKS[*]:-<none>}"
    mark_step zfs skipped
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would create ZFS pool 'tank' (raidz1) on USB disks: ${USB_DISKS[*]}"
    mark_step zfs skipped
    return 0
  fi

  log "Provisioning ZFS usb-zfs pool (raidz1) on USB disks: ${USB_DISKS[*]}"
  modprobe zfs || true

  local CANDIDATES=()
  for d in "${USB_DISKS[@]}"; do
    if blkid "/dev/$d" &>/dev/null; then
      log "Skipping /dev/$d for usb-zfs (appears to contain data)"
      continue
    fi
    wipefs -a "/dev/$d" || true
    CANDIDATES+=("/dev/$d")
  done

  if [[ ${#CANDIDATES[@]} -lt 3 ]]; then
    log "After filtering, not enough empty USB disks for usb-zfs; skipping pool creation. Candidates: ${CANDIDATES[*]:-<none>}"
    mark_step zfs skipped
    return 0
  fi

  # Use raidz1 across all candidate USB sticks
  zpool create -f -o ashift=12 tank raidz1 "${CANDIDATES[@]}" || true
  zfs set compression=lz4 tank || true
  for ds in vm docker k8s; do
    zfs create -o mountpoint=/srv/$ds tank/$ds || true
  done
  log "ZFS usb-zfs pool 'tank' ready on USB sticks"
  mark_step zfs success
}

configure_docker(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would write /etc/docker/daemon.json and enable docker service"
    return 0
  fi
  mkdir -p /etc/docker /srv/docker
  cat >/etc/docker/daemon.json <<'JSON'
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "100m", "max-file": "3" },
  "storage-driver": "overlay2"
}
JSON
  systemctl enable --now docker || true
  log "Docker configured"
}

kubernetes_init(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would initialize Kubernetes (kubeadm) and apply Calico"
    mark_step kubernetes skipped
    return 0
  fi

  swapoff -a || true
  systemctl enable --now containerd || true

  if [[ -f /etc/kubernetes/admin.conf ]]; then
    log "Kubernetes admin.conf already present; skipping kubeadm init."
    mark_step kubernetes success
  else
    if [[ -f /etc/kubernetes/kubeadm-config.yaml ]]; then
      kubeadm init --config /etc/kubernetes/kubeadm-config.yaml || true
    else
      kubeadm init --pod-network-cidr=192.168.0.0/16 || true
    fi
  fi

  mkdir -p /root/.kube
  cp -f /etc/kubernetes/admin.conf /root/.kube/config || true

  if curl -fsSL https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml >/tmp/calico.yaml 2>/dev/null; then
    kubectl apply -f /tmp/calico.yaml || true
  else
    log "Calico manifest fetch failed (offline or GitHub unavailable); skipping network plugin apply"
  fi

  kubectl taint nodes --all node-role.kubernetes.io/control-plane- || true
  log "Kubernetes initialized"
  mark_step kubernetes success
}

configure_firewall(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would configure ufw firewall for mode: $MODE (22, 9090, 6443)"
    return 0
  fi
  ufw default deny incoming || true
  ufw default allow outgoing || true
  ufw allow 22/tcp || true
  ufw allow 9090/tcp || true
  ufw allow 6443/tcp || true

  # In prod mode you might want to tighten further later; for now
  # we just log the mode so behavior is visible.
  log "Firewall configured for mode: $MODE"

  ufw --force enable || true
  log "Firewall rules applied"
}

configure_libvirt_storage(){
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would configure libvirt default storage pool at /var/lib/libvirt/images"
    return 0
  fi
  virsh pool-define-as default dir - - - - /var/lib/libvirt/images || true
  virsh pool-start default || true
  virsh pool-autostart default || true
  log "Libvirt default pool configured"
}

run_addons(){
  if command -v ansible-playbook &>/dev/null; then
    if [[ ! -f /etc/debvisor-addons.conf ]]; then
      # If no explicit addons config, try a profile-based default.
      if [[ -f "/etc/debvisor-addons.d/${PROFILE}.conf" ]]; then
        cp "/etc/debvisor-addons.d/${PROFILE}.conf" /etc/debvisor-addons.conf || true
        log "No addons config found; applied profile default: ${PROFILE}"
      fi
    fi

    if [[ -f /etc/debvisor-addons.conf && -f /usr/local/share/debvisor/ansible/bootstrap-addons.yml ]]; then
      if [[ "$DRY_RUN" == "true" ]]; then
        log "[dry-run] Would run addons bootstrap via Ansible with /etc/debvisor-addons.conf"
        mark_step addons skipped
      else
        log "Running DebVisor addons bootstrap via Ansible (flags from /etc/debvisor-addons.conf; defaults are all 'no' for a minimal core)"
        if ansible-playbook /usr/local/share/debvisor/ansible/bootstrap-addons.yml; then
          mark_step addons success
        else
          log "Addons bootstrap failed (non-fatal)"
          mark_step addons failed
        fi
      fi
    else
      log "Addons config or playbook missing; skipping addons bootstrap"
      mark_step addons skipped
    fi
  else
    log "ansible-playbook not found; skipping addons bootstrap"
    mark_step addons skipped
  fi
}

main(){
  init_logging
  parse_args "$@"
  load_profile_and_mode
  ensure_base_services
  ensure_webpanel_user
  ensure_rpc_user
  ensure_tsig_rotator_user
  generate_keys
  configure_ups
  configure_locale_time
  configure_accounts
  configure_networking
  detect_disks
  detect_usb_disks
  ceph_provision || mark_step ceph failed
  zfs_provision || mark_step zfs failed
  zfs_provision_usb_pool || mark_step zfs failed
  configure_docker
  kubernetes_init || mark_step kubernetes failed
  configure_firewall
  configure_libvirt_storage
  run_addons

  log "DebVisor first boot complete"
  # Generate profile observability summary if helper is available
  if command -v debvisor-profile-summary.sh >/dev/null 2>&1; then
    debvisor-profile-summary.sh || true
  fi
  # Disable service so it does not re-run
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[dry-run] Would disable debvisor-firstboot.service to avoid re-running"
  else
    systemctl disable debvisor-firstboot.service || true
  fi
}

main "$@"
