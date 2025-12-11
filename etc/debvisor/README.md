# etc/ Directory - DebVisor Configuration & Services

## Overview

## RPC Server Configuration (gRPC)

Path: `etc/debvisor/rpc/config.json`

- `host`, `port`: Bind address and port
- `require_client_auth`: Enable mTLS client cert validation
- `tls_cert_file`, `tls_key_file`, `tls_ca_file`: TLS materials
- `connection_pool`: gRPC server threading/keepalive tuning
- `compression`: Enable and choose algorithm (`gzip` or `deflate`)
- `rate_limit`:
- `window_seconds`: Sliding window duration in seconds
- `max_calls`: Default max calls per principal per method in the window
- `method_limits`: Per-method overrides (exact match)
- `method_limits_prefix`: Prefix-based defaults for groups of methods
- `method_limits_patterns`: Regex-based matching for automatic stricter limits

Implemented by `RateLimitingInterceptor` in `opt/services/rpc/server.py`.

## Web Panel Configuration (Flask)

- Set a global default rate limit via `RATELIMIT_DEFAULT` (e.g., `"100 per minute"`).
- Use `@limiter.limit("<N> per <period>")` on routes for granular control.
- Authentication routes implement per-IP and per-user limits with lightweight backoff.

The `etc/`directory contains systemd service and timer units, configuration templates, and blocklist management tools for DebVisor system operations. This directory is installed as`/etc/` on target systems.

### Key Responsibilities

- Automated maintenance scheduling (Ceph health checks, ZFS scrubbing)
- Blocklist and network filtering configuration
- Default environment variables for system services
- Systemd service lifecycle management

## Directory Structure

    etc/
    +-- README.md                          # This file
    +-- debvisor/                          # Blocklist and validation tools
    |   +-- blocklist-example.txt          # Sample network blocklist
    |   +-- blocklist-whitelist-example.txt # Whitelist overrides
    |   +-- blocklist-metadata.json        # Blocklist metadata and provenance
    |   +-- validate-blocklists.sh         # Validation script (CIDR syntax, overlaps)
    |   +-- verify-blocklist-integrity.sh  # Integrity checks (checksums, format)
    |
    +-- default/                           # Environment variables for services
    |   +-- debvisor-zfs-scrub             # ZFS scrub configuration (pools, timeout, options)
    |
    +-- systemd/system/                    # Systemd service and timer units
        +-- ceph-health.service            # Ceph cluster health check (oneshot service)
        +-- ceph-health.timer              # Ceph health check scheduler (hourly, default)
        +-- zfs-scrub-weekly.service       # ZFS pool scrub (oneshot service)
        +-- zfs-scrub-weekly.timer         # ZFS scrub scheduler (weekly, default)

## Component Descriptions

### etc/debvisor/ - Blocklist Management

**Purpose:**Network blocklist configuration and validation for traffic filtering, DDoS mitigation, or policy enforcement.

### Files

-**blocklist-example.txt**: Sample blocklist with IPv4 and IPv6 CIDR ranges

- Format: One CIDR per line, `#` for comments
- Example entries: `10.0.0.0/8`,`2001:db8::/32`,`192.168.1.1/32`

-**blocklist-whitelist-example.txt**: Trusted networks to exclude from blocklist

- Used to override blocklist entries for specific trusted sources
- Example: Allow Google DNS even if broader range is blocked

-**blocklist-metadata.json**: Metadata about blocklist

- Source, version, creation timestamp, purpose
- Checksums for integrity verification
- Tags for categorization (malware, spam, private, etc.)

-**validate-blocklists.sh**: Validation script

- Checks CIDR syntax validity
- Detects overlapping ranges with warnings
- Handles comments and blank lines correctly
- Exit code 0 (valid), non-zero (invalid)

-**verify-blocklist-integrity.sh**: Integrity verification

- Validates file checksums match metadata
- Checks format compliance (no stray data)
- Ensures file hasn't been tampered with

### Usage

## Validate blocklist syntax

    ./etc/debvisor/validate-blocklists.sh --blocklist etc/debvisor/blocklist-example.txt

## Verify integrity

    ./etc/debvisor/verify-blocklist-integrity.sh etc/debvisor/blocklist-example.txt

## Both combined

    ./etc/debvisor/validate-blocklists.sh \
      --blocklist etc/debvisor/blocklist-example.txt \
      --whitelist etc/debvisor/blocklist-whitelist-example.txt \
      --verbose

## CI Integration

- GitHub Actions: `.github/workflows/validate-blocklists.yml`
- Validates all blocklists on each commit
- Integration tests: `.github/workflows/blocklist-integration-tests.yml`

### etc/default/ - Environment Variables

**Purpose:**Default configuration values for system services, loaded at runtime via `EnvironmentFile=` in systemd units.

### Files [2]

-**debvisor-zfs-scrub**: Configuration for ZFS scrubbing service

- `ZFS_POOL`: Primary pool name (default: tank)
- `ZFS_POOL_LIST`: Multiple pools to scrub sequentially
- `ZFS_SCRUB_TIMEOUT`: Maximum scrub duration (default: 7200 seconds)
- `ZFS_SCRUB_OPTIONS`: Additional zpool scrub flags (pause/resume)
- `ZFS_SCRUB_LOG_LEVEL`: Journal logging level (default: info)
- `ZFS_POOL_VALIDATION_ENABLED`: Pre-scrub pool checks (default: true)
- `ZFS_SCRUB_EMAIL_ON_ERROR`: Optional email alerts for failures
- `ZFS_SCRUB_PARALLEL_JOBS`: Parallel job tuning (ZFS 2.0+)

### Usage [2]

## View current configuration

    cat /etc/default/debvisor-zfs-scrub

## Edit configuration

    sudo nano /etc/default/debvisor-zfs-scrub

## Reload service to pick up changes

    sudo systemctl restart zfs-scrub-weekly.timer

See `debvisor-zfs-scrub` file for 1700+ lines of comprehensive documentation.

## etc/systemd/system/ - Services & Timers

**Purpose:**Systemd service and timer units for automated maintenance tasks.

### Ceph Health Checking

#### ceph-health.service

-**Type:**Oneshot service (runs once, completes)
-**Function:**Checks Ceph cluster health status
-**Exit codes:**

- 0: Cluster is HEALTH_OK
- 1: Cluster is HEALTH_WARN or HEALTH_ERR

-**Logging:**Systemd journal with syslog levels
-**Timeout:**30 seconds (prevents hangs)
-**Reliability:**Retries up to 3 times in 60 second window
-**Security:**Strict filesystem sandboxing, no privilege escalation

### Improvements

- Full Ceph status output captured in logs (was: minimal error info)
- Syslog levels (info, warning, error) for better filtering
- Timeout protection (was: no timeout)
- Resource limits (memory, CPU)
- Post-execution hook for email alerts (optional)

#### ceph-health.timer

-**Schedule:**Every hour at the top of the hour
-**Timezone:**UTC (or system timezone)
-**Persistent:**Missed checks are caught up on boot
-**Accuracy:**?1 minute (allows systemd flexibility)

### Customization

## Change to every 15 minutes

    sudo systemctl edit ceph-health.timer

## [Timer]

## OnCalendar=*:0/15:00

## Change to once daily at 2 AM

## OnCalendar=*-*-* 02:00:00

## Reload

    sudo systemctl daemon-reload
    sudo systemctl restart ceph-health.timer

## Monitoring

## View next scheduled run

    systemctl list-timers ceph-health.timer

## View past runs

    journalctl -u ceph-health.service --since today

## Manually trigger check now

    systemctl start ceph-health.service

## Follow logs in real-time

    journalctl -u ceph-health.service -f

## ZFS Pool Scrubbing

### zfs-scrub-weekly.service

-**Type:**Oneshot service
-**Function:**Initiates ZFS pool scrub (data integrity check)
-**Configuration:**Loaded from `/etc/default/debvisor-zfs-scrub`
-**Pre-flight checks:**Validates pool exists before scrubbing
-**Timeout:**Configurable, default 7200 seconds (2 hours)
-**Logging:**Systemd journal with syslog levels
-**Reliability:**Retries up to 2 times in 300 second window
-**Security:**Filesystem sandboxing, restricted device access

### Improvements [2]

- Pre-scrub pool validation (fails fast if pool offline)
- Configurable timeout for different pool sizes
- Support for multiple pools via `ZFS_POOL_LIST`
- Custom scrub options (pause/resume)
- Dependencies on `zfs-mount.service` (ensures ZFS ready)

#### zfs-scrub-weekly.timer

-**Schedule:**Every Sunday at 02:00 UTC (off-peak)
-**Timezone:**UTC (or system timezone)
-**Persistent:**Missed scrubs are caught up on boot
-**Accuracy:**?1 minute

### Pool Size & Timeout Reference

| Pool Size | Typical Time | Recommended Timeout |
|-----------|--------------|---------------------|
| < 1 TB    | < 30 min     | 3600s (1 hour)      |
| 1-10 TB   | 30m-1h       | 5400s (1.5 hours)   |
| 10-50 TB  | 1-3 hours    | 10800s (3 hours)    |
| 50-100 TB | 3-6 hours    | 21600s (6 hours)    |
| > 100 TB  | > 6 hours    | 86400s+ (24+ hours) |

### Customization [2]

## Edit default configuration

    sudo nano /etc/default/debvisor-zfs-scrub

## Change: ZFS_SCRUB_TIMEOUT=21600  (for large pool)

## Or override timer schedule (e.g., daily instead of weekly)

    sudo systemctl edit zfs-scrub-weekly.timer

## [Timer] [2]

## OnCalendar=*-*-* 02:00:00 [2]

## Reload [2]

    sudo systemctl daemon-reload
    sudo systemctl restart zfs-scrub-weekly.timer

## Monitoring Scrub Progress

## Check pool status and scrub progress

    zpool status tank

## Monitor in real-time

    watch -n 5 'zpool status tank | grep -i scrub'

## View scrub statistics

    zpool status -v tank

## Stop in-progress scrub

    sudo zpool scrub -s tank

## Resume paused scrub (ZFS 2.1.0+)

    sudo zpool scrub -r tank

## Troubleshooting Scrubs

## View service logs

    journalctl -u zfs-scrub-weekly.service --since today

## Check if timer is enabled

    systemctl status zfs-scrub-weekly.timer

## Manually trigger scrub immediately

    sudo systemctl start zfs-scrub-weekly.service

## Check when next scrub is scheduled

    systemctl list-timers zfs-scrub-weekly.timer

## View scrub completion times over time

    journalctl -u zfs-scrub-weekly.service --all | grep -i 'initiated\|completed'

## Management Commands

### Viewing Service Status

## List all timers and their next run times

    sudo systemctl list-timers

## Specific timer

    sudo systemctl list-timers ceph-health.timer
    sudo systemctl list-timers zfs-scrub-weekly.timer

## Service status

    sudo systemctl status ceph-health.service
    sudo systemctl status zfs-scrub-weekly.service

## Enabling / Disabling Services

## Enable on boot (start automatically)

    sudo systemctl enable ceph-health.timer
    sudo systemctl enable zfs-scrub-weekly.timer

## Disable (don't start on boot)

    sudo systemctl disable ceph-health.timer
    sudo systemctl disable zfs-scrub-weekly.timer

## Check if enabled

    sudo systemctl is-enabled ceph-health.timer

## Starting / Stopping Services

## Start timer now

    sudo systemctl start ceph-health.timer
    sudo systemctl start zfs-scrub-weekly.timer

## Stop timer (prevents future runs)

    sudo systemctl stop ceph-health.timer
    sudo systemctl stop zfs-scrub-weekly.timer

## Restart (reload configuration)

    sudo systemctl restart ceph-health.timer
    sudo systemctl daemon-reload  # After editing .service/.timer files

## Viewing Logs

## Follow real-time logs

    sudo journalctl -u ceph-health.service -f
    sudo journalctl -u zfs-scrub-weekly.service -f

## Last 100 lines

    sudo journalctl -u ceph-health.service -n 100

## Since specific time

    sudo journalctl -u ceph-health.service --since today
    sudo journalctl -u ceph-health.service --since "2 hours ago"

## Only errors

    sudo journalctl -u ceph-health.service -p err

## All Ceph-related logs

    sudo journalctl | grep ceph-health

## Manual Execution

## Trigger check/scrub immediately

    sudo systemctl start ceph-health.service
    sudo systemctl start zfs-scrub-weekly.service

## Check status during execution

    sudo systemctl status ceph-health.service
    sudo watch -n 1 'sudo systemctl status ceph-health.service'

## Customization Guide

### Adding New Services

1.**Create service file:**`/etc/systemd/system/my-service.service`

       [Unit]
       Description=My Service
       After=network.target

       [Service]
       Type=oneshot
       ExecStart=/usr/bin/my-command
       StandardOutput=journal
       StandardError=journal

       [Install]
       WantedBy=timers.target

    1.**Create timer file (optional):**`/etc/systemd/system/my-service.timer`

   [Unit]
   Description=My Service Timer

   [Timer]
   OnCalendar=daily
   Persistent=true

   [Install]
   WantedBy=timers.target

    1.**Reload and enable:**

       sudo systemctl daemon-reload
       sudo systemctl enable my-service.timer
       sudo systemctl start my-service.timer

### Modifying Existing Services

**Option 1: Drop-in override directory**(recommended for package compatibility)

## Create drop-in directory

    sudo mkdir -p /etc/systemd/system/ceph-health.service.d/

## Create override file

    sudo nano /etc/systemd/system/ceph-health.service.d/custom.conf

## [Service]

## OnFailure=notify-admin@%n.service

## Reload [3]

    sudo systemctl daemon-reload

**Option 2: Edit command**(interactive, creates drop-in automatically)

    sudo systemctl edit ceph-health.service

## Edit the [Service] section

## Reload happens automatically

**Option 3: Direct edit**(not recommended, overwritten on package update)

    sudo nano /etc/systemd/system/ceph-health.service
    sudo systemctl daemon-reload

## Production Deployment Checklist

- [ ] Enable both timers on first boot: `systemctl enable ceph-health.timer zfs-scrub-weekly.timer`
- [ ] Verify configuration values in `/etc/default/debvisor-zfs-scrub` for your environment
- [ ] Adjust `ZFS_SCRUB_TIMEOUT` if pool size differs significantly from defaults
- [ ] Configure email alerts if monitoring system requires notification
- [ ] Set up log aggregation to collect service logs from journal
- [ ] Configure alerting for service failures (especially zfs-scrub-weekly)
- [ ] For multi-node clusters, stagger scrub schedules to prevent simultaneous I/O
- [ ] Document custom timer schedules for your environment
- [ ] Test service execution manually before relying on automated schedules
- [ ] Monitor disk space for systemd journal to prevent log loss
- [ ] Set up metrics collection for scrub duration and timing

## Troubleshooting

### Service Won't Start

## Check service status and error

    sudo systemctl status ceph-health.service

## View detailed logs

    sudo journalctl -u ceph-health.service --no-pager

## Verify unit file syntax

    sudo systemd-analyze verify /etc/systemd/system/ceph-health.service

## Timer Not Running Scheduled Tasks

## Verify timer is enabled and active

    sudo systemctl status ceph-health.timer

## Check next scheduled run

    sudo systemctl list-timers ceph-health.timer

## If next run is far in future, restart timer

    sudo systemctl restart ceph-health.timer

## If timer never ran, check system time

    date
    timedatectl

## High Memory/CPU Usage

## Check resource limits

    sudo systemctl show -p MemoryLimit ceph-health.service

## Monitor during execution

    sudo watch -n 1 'ps aux | grep ceph'

## Adjust limits in service file or drop-in override

## Logs Not Appearing

## Verify journal is working

    sudo systemctl status systemd-journald

## Check journal disk usage

    sudo journalctl --disk-usage

## View journal info

    sudo journalctl --unit=ceph-health.service --follow --all

## References

- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/systemd.service.html) - Service unit documentation
- [systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) - Timer unit documentation
- [ceph(1)](https://docs.ceph.com/en/latest/man/8/ceph/) - Ceph cluster command reference
- [zpool-scrub(8)](https://linux.die.net/man/8/zpool) - ZFS pool scrub documentation
- [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) - Time specification format

## See Also

- [../opt/README.md](../opt/README.md) - Operational scripts and tools
- [../usr/README.md](../usr/README.md) - Runtime services and CLIs
- [DebVisor Main README](../README.md) - Project overview
