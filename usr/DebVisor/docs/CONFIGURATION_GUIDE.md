# etc/ Configuration Directory - Improvements

## Overview

The `etc/` directory contains service configurations, timers, and operational documentation.

## Directory Structure

    etc/
    +-- blocklist.d/               # Blocklist definitions
    +-- debvisor/                  # Main configuration
    +-- systemd/
    |   +-- system/
    |   |   +-- debvisor-*.service
    |   |   +-- debvisor-*.timer
    |   |   +-- system.conf.d/
    |   +-- user/
    +-- README.md                  # Configuration documentation
    +-- VALIDATION_GUIDE.md        # Validation procedures

## Blocklist Management

### Blocklist Files

### etc/blocklist.d/nodes.blocklist

## Format: one node per line

## Lines starting with # are comments

    node-123
    node-456

## Reason: Hardware failure

    node-789

## etc/blocklist.d/networks.blocklist

## CIDR format for network ranges

    192.168.1.0/24
    10.0.0.0/8

## IPv6 support

    fc00::/7

## etc/blocklist.d/storage.blocklist

## Storage devices or pools to exclude

    /dev/sdb
    ceph-pool-backup
    zfs-tank-old

## Blocklist Validation

## Validate all blocklist files

    python3 opt/config/validate-blocklist.py --dir etc/blocklist.d/

## Check specific file

    python3 opt/config/validate-blocklist.py --file etc/blocklist.d/nodes.blocklist

## Apply blocklist

    debvisor-blocklist-apply etc/blocklist.d/

## Service Configuration

### Service Files

- *debvisor-rpcd.service**- RPC daemon

    [Unit]
    Description=DebVisor RPC Service
    After=network-online.target
    Requires=network-online.target

    [Service]
    Type=simple
    User=debvisor
    ExecStart=/opt/services/rpc/bin/rpcd --config /etc/debvisor/rpcd.conf
    Restart=always
    RestartSec=10s

    [Install]
    WantedBy=multi-user.target

- *debvisor-panel.service**- Web panel

    [Unit]
    Description=DebVisor Web Panel
    After=network.target debvisor-rpcd.service
    Requires=debvisor-rpcd.service

    [Service]
    Type=simple
    User=debvisor
    ExecStart=/opt/web/panel/bin/panel --config /etc/debvisor/panel.conf
    Restart=always

    [Install]
    WantedBy=multi-user.target

### Timer Units

- *debvisor-health-check.timer**- Regular health checks

    [Unit]
    Description=DebVisor Health Check Timer

    [Timer]
    OnBootSec=5min
    OnUnitActiveSec=5min
    AccuracySec=1min

    [Install]
    WantedBy=timers.target

- *debvisor-cleanup.timer**- Periodic cleanup

    [Unit]
    Description=DebVisor Cleanup Timer

    [Timer]
    OnCalendar=daily
    OnCalendar=*-*-* 02:00:00
    AccuracySec=5min

    [Install]
    WantedBy=timers.target

## Configuration Best Practices

### Service Requirements

1.**Security Hardening**

       PrivateTmp=yes
       ProtectSystem=strict
       ProtectHome=yes
       NoNewPrivileges=yes

    1.**Resource Limits**

   MemoryMax=2G
   CPUQuota=50%
   TasksMax=1000

    1.**Restart Policy**

       Restart=on-failure
       RestartSec=10s
       StartLimitInterval=60s
       StartLimitBurst=3

### Timer Best Practices

1. Use `OnBootSec` for startup delays
1. Use `OnUnitActiveSec` for regular intervals
1. Set `AccuracySec` to balance timing and system load
1. Document purpose in `[Unit] Description`

## Validation

### Configuration Validation

## Validate all service files

    systemd-analyze verify etc/systemd/system/*.service

## Check timer definitions

    systemd-analyze verify-times etc/systemd/system/*.timer

## Pre-flight checks

    debvisor-validate-config etc/

## Service Testing

## Test service startup (no actual start)

    systemd-analyze --scope user verify etc/systemd/user/*.service

## Check dependencies

    systemctl list-dependencies debvisor-rpcd.service

## Troubleshooting

### Common Issues

### Service fails to start

## Check service logs

    journalctl -u debvisor-rpcd.service -n 50

## Verify configuration syntax

    systemd-analyze verify etc/systemd/system/debvisor-rpcd.service

## Check dependencies [2]

    systemctl list-dependencies --all debvisor-rpcd.service

## Timer doesn't run

## Check timer status

    systemctl list-timers debvisor-health-check.timer

## View last run

    journalctl -u debvisor-health-check.timer

## Manual trigger for testing

    systemctl start debvisor-health-check.timer

## Configuration changed but not applied

## Reload systemd manager

    systemctl daemon-reload

## Verify changes

    systemd-analyze diff before after

## Security Hardening

### Service Security

1.**User privileges**: Run as non-root
1.**File permissions**: Restrict config file access (600 or 640)
1.**Secrets management**: Use systemd credentials or external vault
1.**Network**: Use specific ports and protocols
1.**Resource limits**: Prevent DoS and resource exhaustion

### Configuration Security

## Check file permissions

    find etc/ -type f ! -perm 644 -print
    find etc/ -type d ! -perm 755 -print

## Validate no secrets in plain text

    grep -r "password\|secret\|token" etc/ || echo "OK"

## Check ownership

    stat -c '%A %u:%g %n' etc/debvisor/*

## Integration Points

- **Logging**: All services integrate with systemd journal
- **Monitoring**: Prometheus metrics from service status
- **Health**: debvisor-health-check validates services
- **Audit**: All configuration changes logged
- **Dependencies**: Clear service dependency graph

## References

- systemd documentation: [https://systemd.io/](https://systemd.io/)
- Service file format: `man 5 systemd.service`
- Timer format: `man 5 systemd.timer`
- Best practices: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)
