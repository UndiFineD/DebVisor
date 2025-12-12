# etc/ Directory - Advanced Configuration Topics

## Version Control & Package Distribution
### Systemd .service.d/ Override Patterns
Deployment-specific customizations should use systemd drop-in directories rather than modifying original service files:
## Directory structure for overrides
    /etc/systemd/system/debvisor-rpcd.service.d/
    +-- override.conf              # Deployment-specific overrides
    +-- proxy.conf                 # HTTP proxy settings
    +-- resource-limits.conf       # Custom resource constraints
## Override Examples
- *10-deployment.conf**- Environment-specific settings
    [Unit]
## Add deployment-specific requirements
    After=network-online.target custom-setup.service
    [Service]
## Override or add environment variables
    Environment="DEBVISOR_ENVIRONMENT=production"
    Environment="DEBVISOR_CLUSTER=primary"
## Custom restart behavior per environment
    Restart=on-failure
    RestartSec=5s

- *20-resources.conf**- Resource limits per deployment
    [Service]
## Production resource limits
    MemoryMax=2G
    CPUQuota=100%
    TasksMax=2000
## Logging configuration
    StandardOutput=journal
    StandardError=journal
    SyslogIdentifier=debvisor-rpcd-prod
## Versioning Strategy
### Service Versioning
    debvisor-rpcd.service            # Current (symlink or alias)
    debvisor-rpcd.service.1.0        # Version 1.0 (stable)
    debvisor-rpcd.service.1.1        # Version 1.1 (with features)
    debvisor-rpcd.service.2.0.beta   # Version 2.0 beta (testing)
### Configuration Versioning
    /etc/debvisor/rpcd.conf           # Current
    /etc/debvisor/rpcd.conf.1.0       # Version 1.0
    /etc/debvisor/rpcd.conf.1.0.bak   # Backup before upgrade
### Deployment Templates
- *Lab Environment**(`deployment-lab.d/override.conf`)
    [Service]
    MemoryMax=512M
    CPUQuota=50%
    Environment="DEBVISOR_LOG_LEVEL=debug"

- *Staging Environment**(`deployment-staging.d/override.conf`)
    [Service]
    MemoryMax=1G
    CPUQuota=75%
    Environment="DEBVISOR_LOG_LEVEL=info"

- *Production Environment**(`deployment-prod.d/override.conf`)
    [Service]
    MemoryMax=2G
    CPUQuota=100%
    Environment="DEBVISOR_LOG_LEVEL=warn"
    Restart=always
    RestartSec=10s
## Security
### File Permissions & Ownership
### Standard Service File Permissions
## Service files should be readable but not writable by regular users
    chmod 644 /etc/systemd/system/debvisor-*.service
    chmod 644 /etc/systemd/system/debvisor-*.timer
    chmod 755 /etc/systemd/system/debvisor-*.service.d/
## Configuration files should be readable but not writable
    chmod 640 /etc/debvisor/*.conf
    chmod 640 /etc/debvisor/debvisor-secrets.conf    # Secrets file
## Ownership (root:root for system-wide services)
    chown root:root /etc/systemd/system/debvisor-*.service
    chown root:root /etc/debvisor/*.conf
## Secrets file should have restrictive permissions
    chown root:debvisor /etc/debvisor/debvisor-secrets.conf
    chmod 640 /etc/debvisor/debvisor-secrets.conf
## Permission Verification Script
    #!/bin/bash
## Verify systemd service file permissions
    echo "Checking systemd service file permissions..."
## Service files should be 0644
    find /etc/systemd/system -name "debvisor-*.service" -type f ! -perm 644 \
        && echo "[warn]?  Service files with incorrect permissions:" && \
        find /etc/systemd/system -name "debvisor-*.service" -type f ! -perm 644 -ls
## Timer files should be 0644
    find /etc/systemd/system -name "debvisor-*.timer" -type f ! -perm 644 \
        && echo "[warn]?  Timer files with incorrect permissions:" && \
        find /etc/systemd/system -name "debvisor-*.timer" -type f ! -perm 644 -ls
## Config files should be 0640
    find /etc/debvisor -name "*.conf" -type f ! -perm 640 \
        && echo "[warn]?  Config files with incorrect permissions:" && \
        find /etc/debvisor -name "*.conf" -type f ! -perm 640 -ls
    echo "Permission check complete."
## Privilege & Capability Analysis
### debvisor-rpcd.service
Required Privileges:
    [Service]
## Must bind to port 5000 (requires CAP_NET_BIND_SERVICE or run as root)
## Solution: Run as root or use socket activation with lower port
## Must access Ceph cluster sockets (typically in /var/run/ceph/)
## Solution: Add user to ceph group or use appropriate mount
## Must create logs in /var/log/debvisor/
## Solution: Pre-create directory with appropriate permissions
## Recommended: Run as debvisor user with necessary capabilities
    User=debvisor
    Group=debvisor
    CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_SETUID CAP_SETGID
    AmbientCapabilities=CAP_NET_BIND_SERVICE
## debvisor-panel.service
    [Service]
## Requires: Port binding, configuration file access
    User=debvisor
    Group=debvisor
    CapabilityBoundingSet=CAP_NET_BIND_SERVICE
    AmbientCapabilities=CAP_NET_BIND_SERVICE
## User & Group Policies
### Recommended Setup
## Create debvisor system user
    useradd --system --shell /usr/sbin/nologin --home /var/lib/debvisor debvisor
## Create debvisor group
    groupadd --system debvisor
## Add necessary groups for cluster access
    usermod -a -G ceph debvisor      # For Ceph cluster access
    usermod -a -G libvirt debvisor   # For libvirt access (if needed)
    usermod -a -G docker debvisor    # For Docker access (if needed)
## Create necessary directories with correct permissions
    mkdir -p /var/log/debvisor
    chown debvisor:debvisor /var/log/debvisor
    chmod 750 /var/log/debvisor
    mkdir -p /var/lib/debvisor
    chown debvisor:debvisor /var/lib/debvisor
    chmod 750 /var/lib/debvisor
    mkdir -p /var/run/debvisor
    chown debvisor:debvisor /var/run/debvisor
    chmod 750 /var/run/debvisor
## Security Hardening Checklist
## Recommended systemd security directives for all debvisor services
    [Service]
## Filesystem isolation
    PrivateTmp=yes
    ProtectSystem=strict
    ProtectHome=yes
    ReadWritePaths=/var/log/debvisor /var/lib/debvisor /var/run/debvisor
## Process isolation
    NoNewPrivileges=yes
    PrivateDevices=yes
    ProtectKernelLogs=yes
    ProtectKernelModules=yes
    ProtectKernelTunables=yes
    ProtectControlGroups=yes
    ProtectClock=yes
## Capabilities restriction
    CapabilityBoundingSet=~CAP_SYS_ADMIN CAP_SYS_BOOT CAP_NET_ADMIN CAP_SYS_NICE
    RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
## Privilege escalation prevention
    LockPersonality=yes
    RestrictNamespaces=yes
    RestrictRealtime=yes
    RemoveIPC=yes
## System call filtering (optional, requires libseccomp)
    SystemCallFilter=@system-service @basic-io @io-event @ipc @network-io
    SystemCallErrorNumber=EPERM
## Robustness Across Reboots
### Persistence Configuration
### Timer Persistence
## Timers should be configured to survive reboots
    [Timer]
## Run timer on boot if it was missed
    OnBootSec=5min
## Persist timer state across reboots
    Persistent=true
## Accuracy settings (balance between timing and system load)
    AccuracySec=1min
    RandomizedDelaySec=0
    [Install]
    WantedBy=timers.target
## Service Persistence
    [Unit]
## Ensure service starts early in boot
    After=network-online.target
    Wants=network-online.target
    [Service]
## Auto-restart on failure
    Restart=on-failure
    RestartSec=10s
## Timeout for long-running initialization
    TimeoutStartSec=300
    TimeoutStopSec=30
    [Install]
## Enable on system boot
    WantedBy=multi-user.target
## Recovery Procedures
### If Service Fails on Startup
## 1. Check service status
    systemctl status debvisor-rpcd.service
## 2. View recent logs
    journalctl -u debvisor-rpcd.service -n 50 --no-pager
## 3. Test configuration
    /opt/services/rpc/bin/rpcd --validate-config
## 4. Start with verbose logging
    systemctl start debvisor-rpcd.service
    systemctl status debvisor-rpcd.service -l --no-pager
## 5. If still failing, disable auto-start for debugging
    systemctl disable debvisor-rpcd.service
## ... debug and fix
    systemctl enable debvisor-rpcd.service
## If Timer Doesn't Run After Reboot
## 1. Verify timer is enabled and started
    systemctl is-enabled debvisor-health-check.timer
    systemctl is-active debvisor-health-check.timer
## 2. Check timer schedule and next run time
    systemctl list-timers debvisor-health-check.timer
## 3. View timer logs
    journalctl -u debvisor-health-check.timer -n 20 --no-pager
## 4. Manually trigger the associated service for testing
    systemctl start debvisor-health-check.service
## 5. Reload and restart timer if needed
    systemctl daemon-reload
    systemctl restart debvisor-health-check.timer
## Boot-Time Testing & Validation
### Test Boot-Time Service Startup
    #!/bin/bash
## test-boot-startup.sh - Verify services start correctly after reboot
    echo "Testing boot-time service startup..."
## Give systemd time to start services
    sleep 10
## Check critical services are running
    services=("debvisor-rpcd" "debvisor-panel" "debvisor-health-check.timer")
    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service.service" || \
           systemctl is-active --quiet "$service"; then
            echo "? $service is running"
        else
            echo "? $service failed to start"
            systemctl status "$service" -l
            journalctl -u "$service" -n 20 --no-pager
        fi
    done
## Verify RPC service responds to requests
    if curl -s [http://localhost:5000/api/health](http://localhost:5000/api/health) >/dev/null; then
        echo "? RPC service responding to requests"
    else
        echo "? RPC service not responding"
    fi
## Check for startup errors in journal
    if journalctl --since "10 seconds ago" | grep -i error | grep -i debvisor; then
        echo "[warn]?  Found startup errors in journal"
        journalctl --since "10 seconds ago" | grep -i debvisor
    fi
## Pre-Reboot Validation
    #!/bin/bash
## pre-reboot-check.sh - Verify system is ready for safe reboot
    echo "Running pre-reboot checks..."
## 1. Verify all service files are valid
    systemd-analyze verify /etc/systemd/system/debvisor-*.service 2>&1
    if [ $? -ne 0 ]; then
        echo "? Service file validation failed"
        exit 1
    fi
## 2. Check for services in failed state
    if systemctl list-units --failed | grep debvisor; then
        echo "[warn]?  Found debvisor services in failed state"
    fi
## 3. Verify timer schedules are correct
    systemctl list-timers debvisor-*.timer
## 4. Confirm configuration files are accessible
    for conf in /etc/debvisor/*.conf; do
        if [ -r "$conf" ]; then
            echo "? $conf is readable"
        else
            echo "? $conf is not readable"
        fi
    done
    echo "Pre-reboot checks complete. Safe to reboot."
## Post-Reboot Validation
    #!/bin/bash
## post-reboot-check.sh - Verify system recovered correctly after reboot
    echo "Running post-reboot checks (run 2-3 minutes after boot)..."
## 1. Verify all services started
    systemctl status debvisor-*.service debvisor-*.timer
## 2. Check service response times (should be fast)
    curl -w "@curl-format.txt" -o /dev/null -s [http://localhost:5000/api/health](http://localhost:5000/api/health)
## 3. Verify no error floods in logs
    error_count=$(journalctl --since "5 minutes ago" \
        | grep -i "debvisor\|rpcd\|panel" \
        | grep -i "error\|fail" \
        | wc -l)
    echo "Errors in last 5 minutes: $error_count"
## 4. Check persistent state was preserved
    if [ -f /var/lib/debvisor/state.json ]; then
        echo "? Persistent state file present"
        jq . /var/lib/debvisor/state.json 2>/dev/null | head -20
    fi
    echo "Post-reboot checks complete."
## References
- Systemd documentation: [https://www.freedesktop.org/software/systemd/man/](https://www.freedesktop.org/software/systemd/man/)

- Service file format: `man 5 systemd.service`

- Timer format: `man 5 systemd.timer`

- Drop-in files: `man 5 systemd.unit`

- Security directives: [https://www.freedesktop.org/software/systemd/man/systemd.exec.html](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)
