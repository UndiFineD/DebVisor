# etc/ Directory - DebVisor Configuration & Services\n\n## Overview\n\n## RPC Server

Configuration

(gRPC)\n\nPath: `etc/debvisor/rpc/config.json`\n\n- `host`, `port`: Bind address
and
port\n\n-
`require_client_auth`: Enable mTLS client cert validation\n\n- `tls_cert_file`,
`tls_key_file`,
`tls_ca_file`: TLS materials\n\n- `connection_pool`: gRPC server
threading/keepalive
tuning\n\n-
`compression`: Enable and choose algorithm (`gzip`or`deflate`)\n\n-
`rate_limit`:\n\n-
`window_seconds`: Sliding window duration in seconds\n\n- `max_calls`: Default
max calls
per
principal per method in the window\n\n- `method_limits`: Per-method overrides
(exact
match)\n\n-
`method_limits_prefix`: Prefix-based defaults for groups of methods\n\n-
`method_limits_patterns`:
Regex-based matching for automatic stricter limits\n\nImplemented by
`RateLimitingInterceptor`in`opt/services/rpc/server.py`.\n\n## Web Panel
Configuration
(Flask)\n\n-
Set a global default rate limit via `RATELIMIT_DEFAULT`(e.g.,`"100 per
minute"`).\n\n- Use
`@limiter.limit(" per ")`on routes for granular control.\n\n- Authentication
routes
implement per-IP and per-user limits with lightweight
backoff.\n\nThe`etc/`directory
contains
systemd service and timer units, configuration templates, and blocklist
management tools
for
DebVisor system operations. This directory is installed as`/etc/`on target
systems.\n\n###
Key
Responsibilities\n\n- Automated maintenance scheduling (Ceph health checks, ZFS
scrubbing)\n\n-
Blocklist and network filtering configuration\n\n- Default environment variables
for
system
services\n\n- Systemd service lifecycle management\n\n## Directory Structure\n\n
etc/\n
+--
README.md # This file\n +-- debvisor/ # Blocklist and validation tools\n | +--
blocklist-example.txt

## Sample network blocklist\n | +-- blocklist-whitelist-example.txt # Whitelist

overrides\n

| +--

blocklist-metadata.json # Blocklist metadata and provenance\n | +--
validate-blocklists.sh

## 

Validation script (CIDR syntax, overlaps)\n | +-- verify-blocklist-integrity.sh

## 

Integrity checks
(checksums, format)\n |\n +-- default/ # Environment variables for services\n |
+--
debvisor-zfs-scrub # ZFS scrub configuration (pools, timeout, options)\n |\n +--
systemd/system/ #
Systemd service and timer units\n +-- ceph-health.service # Ceph cluster health
check
(oneshot
service)\n +-- ceph-health.timer # Ceph health check scheduler (hourly,
default)\n +--
zfs-scrub-weekly.service # ZFS pool scrub (oneshot service)\n +--
zfs-scrub-weekly.timer #
ZFS scrub
scheduler (weekly, default)\n\n## Component Descriptions\n\n### etc/debvisor/ -
Blocklist
Management\n\n- *Purpose:**Network blocklist configuration and validation for
traffic
filtering,
DDoS mitigation, or policy enforcement.\n\n### Files\n\n-
**blocklist-example.txt**:
Sample
blocklist with IPv4 and IPv6 CIDR ranges\n\n- Format: One CIDR per line,`#`for
comments\n\n- Example
entries:`10.0.0.0/8`,`2001:db8::/32`,`192.168.1.1/32`\n\n-
**blocklist-whitelist-example.txt**:
Trusted networks to exclude from blocklist\n\n- Used to override blocklist
entries for
specific
trusted sources\n\n- Example: Allow Google DNS even if broader range is
blocked\n\n-
**blocklist-metadata.json**: Metadata about blocklist\n\n- Source, version,
creation
timestamp,
purpose\n\n- Checksums for integrity verification\n\n- Tags for categorization
(malware,
spam,
private, etc.)\n\n- **validate-blocklists.sh**: Validation script\n\n- Checks
CIDR syntax
validity\n\n- Detects overlapping ranges with warnings\n\n- Handles comments and
blank
lines
correctly\n\n- Exit code 0 (valid), non-zero (invalid)\n\n-
**verify-blocklist-integrity.sh**:
Integrity verification\n\n- Validates file checksums match metadata\n\n- Checks
format
compliance
(no stray data)\n\n- Ensures file hasn't been tampered with\n\n### Usage\n\n##
Validate
blocklist
syntax\n\n ./etc/debvisor/validate-blocklists.sh --blocklist
etc/debvisor/blocklist-example.txt\n\n## Verify integrity\n\n
./etc/debvisor/verify-blocklist-integrity.sh
etc/debvisor/blocklist-example.txt\n\n## Both
combined\n\n ./etc/debvisor/validate-blocklists.sh \\n\n - -blocklist
etc/debvisor/blocklist-example.txt \\n\n - -whitelist
etc/debvisor/blocklist-whitelist-example.txt
\\n\n - -verbose\n\n## CI Integration\n\n- GitHub Actions:
`.github/workflows/validate-blocklists.yml`\n\n- Validates all blocklists on
each
commit\n\n-
Integration tests: `.github/workflows/blocklist-integration-tests.yml`\n\n###
etc/default/
-
Environment Variables\n\n- *Purpose:**Default configuration values for system
services,
loaded at
runtime via `EnvironmentFile=`in systemd units.\n\n### Files [2]\n\n-
**debvisor-zfs-scrub**:
Configuration for ZFS scrubbing service\n\n-`ZFS_POOL`: Primary pool name
(default:
tank)\n\n-
`ZFS_POOL_LIST`: Multiple pools to scrub sequentially\n\n- `ZFS_SCRUB_TIMEOUT`:
Maximum
scrub
duration (default: 7200 seconds)\n\n- `ZFS_SCRUB_OPTIONS`: Additional zpool
scrub flags
(pause/resume)\n\n- `ZFS_SCRUB_LOG_LEVEL`: Journal logging level (default:
info)\n\n-
`ZFS_POOL_VALIDATION_ENABLED`: Pre-scrub pool checks (default: true)\n\n-
`ZFS_SCRUB_EMAIL_ON_ERROR`: Optional email alerts for failures\n\n-
`ZFS_SCRUB_PARALLEL_JOBS`:
Parallel job tuning (ZFS 2.0+)\n\n### Usage [2]\n\n## View current
configuration\n\n cat
/etc/default/debvisor-zfs-scrub\n\n## Edit configuration\n\n sudo nano
/etc/default/debvisor-zfs-scrub\n\n## Reload service to pick up changes\n\n sudo
systemctl
restart
zfs-scrub-weekly.timer\nSee `debvisor-zfs-scrub`file for 1700+ lines of
comprehensive
documentation.\n\n## etc/systemd/system/ - Services & Timers\n\n-
*Purpose:**Systemd
service and
timer units for automated maintenance tasks.\n\n### Ceph Health Checking\n\n####
ceph-health.service\n\n- **Type:**Oneshot service (runs once, completes)\n\n-
**Function:**Checks
Ceph cluster health status\n\n- **Exit codes:**\n\n- 0: Cluster is
HEALTH_OK\n\n- 1:
Cluster is
HEALTH_WARN or HEALTH_ERR\n\n- **Logging:**Systemd journal with syslog
levels\n\n-
**Timeout:**30
seconds (prevents hangs)\n\n- **Reliability:**Retries up to 3 times in 60 second
window\n\n-
**Security:**Strict filesystem sandboxing, no privilege escalation\n\n###
Improvements\n\n- Full
Ceph status output captured in logs (was: minimal error info)\n\n- Syslog levels
(info,
warning,
error) for better filtering\n\n- Timeout protection (was: no timeout)\n\n-
Resource limits
(memory,
CPU)\n\n- Post-execution hook for email alerts (optional)\n\n####
ceph-health.timer\n\n-
**Schedule:**Every hour at the top of the hour\n\n- **Timezone:**UTC (or system
timezone)\n\n-
**Persistent:**Missed checks are caught up on boot\n\n- **Accuracy:**?1 minute
(allows
systemd
flexibility)\n\n### Customization\n\n## Change to every 15 minutes\n\n sudo
systemctl edit
ceph-health.timer\n\n## [Timer]\n\n## OnCalendar=*:0/15:00\n\n## Change to once
daily at 2
AM\n\n##
OnCalendar=*-*-*02:00:00\n\n## Reload\n\n sudo systemctl daemon-reload\n sudo
systemctl
restart
ceph-health.timer\n\n## Monitoring\n\n## View next scheduled run\n\n systemctl
list-timers
ceph-health.timer\n\n## View past runs\n\n journalctl -u ceph-health.service
--since
today\n\n##
Manually trigger check now\n\n systemctl start ceph-health.service\n\n## Follow
logs in
real-time\n\n journalctl -u ceph-health.service -f\n\n## ZFS Pool
Scrubbing\n\n###
zfs-scrub-weekly.service\n\n-**Type:**Oneshot service\n\n-
**Function:**Initiates ZFS pool
scrub
(data integrity check)\n\n- **Configuration:**Loaded
from`/etc/default/debvisor-zfs-scrub`\n\n-
**Pre-flight checks:**Validates pool exists before scrubbing\n\n-
**Timeout:**Configurable, default
7200 seconds (2 hours)\n\n- **Logging:**Systemd journal with syslog levels\n\n-
**Reliability:**Retries up to 2 times in 300 second window\n\n-
**Security:**Filesystem
sandboxing,
restricted device access\n\n### Improvements [2]\n\n- Pre-scrub pool validation
(fails
fast if pool
offline)\n\n- Configurable timeout for different pool sizes\n\n- Support for
multiple
pools via
`ZFS_POOL_LIST`\n\n- Custom scrub options (pause/resume)\n\n- Dependencies on
`zfs-mount.service`(ensures ZFS ready)\n\n#### zfs-scrub-weekly.timer\n\n-
**Schedule:**Every Sunday
at 02:00 UTC (off-peak)\n\n- **Timezone:**UTC (or system timezone)\n\n-
**Persistent:**Missed scrubs
are caught up on boot\n\n- **Accuracy:**?1 minute\n\n### Pool Size & Timeout
Reference\n\n| Pool
Size | Typical Time | Recommended Timeout
|\n|-----------|--------------|---------------------|\n|  100 TB | > 6 hours | 86400s+
(24+ hours) |\n\n### Customization [2]\n\n## Edit default configuration\n\n sudo
nano
/etc/default/debvisor-zfs-scrub\n\n## Change: ZFS_SCRUB_TIMEOUT=21600 (for large
pool)\n\n## Or
override timer schedule (e.g., daily instead of weekly)\n\n sudo systemctl edit
zfs-scrub-weekly.timer\n\n## [Timer] [2]\n\n## OnCalendar=*-*-*02:00:00
[2]\n\n## Reload
[2]\n\n
sudo systemctl daemon-reload\n sudo systemctl restart
zfs-scrub-weekly.timer\n\n##
Monitoring Scrub
Progress\n\n## Check pool status and scrub progress\n\n zpool status tank\n\n##
Monitor in
real-time\n\n watch -n 5 'zpool status tank | grep -i scrub'\n\n## View scrub
statistics\n\n zpool
status -v tank\n\n## Stop in-progress scrub\n\n sudo zpool scrub -s tank\n\n##
Resume
paused scrub
(ZFS 2.1.0+)\n\n sudo zpool scrub -r tank\n\n## Troubleshooting Scrubs\n\n##
View service
logs\n\n
journalctl -u zfs-scrub-weekly.service --since today\n\n## Check if timer is
enabled\n\n
systemctl
status zfs-scrub-weekly.timer\n\n## Manually trigger scrub immediately\n\n sudo
systemctl
start
zfs-scrub-weekly.service\n\n## Check when next scrub is scheduled\n\n systemctl
list-timers
zfs-scrub-weekly.timer\n\n## View scrub completion times over time\n\n
journalctl -u
zfs-scrub-weekly.service --all | grep -i 'initiated\|completed'\n\n## Management
Commands\n\n###
Viewing Service Status\n\n## List all timers and their next run times\n\n sudo
systemctl
list-timers\n\n## Specific timer\n\n sudo systemctl list-timers
ceph-health.timer\n sudo
systemctl
list-timers zfs-scrub-weekly.timer\n\n## Service status\n\n sudo systemctl
status
ceph-health.service\n sudo systemctl status zfs-scrub-weekly.service\n\n##
Enabling /
Disabling
Services\n\n## Enable on boot (start automatically)\n\n sudo systemctl enable
ceph-health.timer\n
sudo systemctl enable zfs-scrub-weekly.timer\n\n## Disable (don't start on
boot)\n\n sudo
systemctl
disable ceph-health.timer\n sudo systemctl disable zfs-scrub-weekly.timer\n\n##
Check if
enabled\n\n
sudo systemctl is-enabled ceph-health.timer\n\n## Starting / Stopping
Services\n\n## Start
timer
now\n\n sudo systemctl start ceph-health.timer\n sudo systemctl start
zfs-scrub-weekly.timer\n\n##
Stop timer (prevents future runs)\n\n sudo systemctl stop ceph-health.timer\n
sudo
systemctl stop
zfs-scrub-weekly.timer\n\n## Restart (reload configuration)\n\n sudo systemctl
restart
ceph-health.timer\n sudo systemctl daemon-reload # After editing .service/.timer
files\n\n## Viewing
Logs\n\n## Follow real-time logs\n\n sudo journalctl -u ceph-health.service -f\n
sudo
journalctl -u
zfs-scrub-weekly.service -f\n\n## Last 100 lines\n\n sudo journalctl -u
ceph-health.service -n
100\n\n## Since specific time\n\n sudo journalctl -u ceph-health.service --since
today\n
sudo
journalctl -u ceph-health.service --since "2 hours ago"\n\n## Only errors\n\n
sudo
journalctl -u
ceph-health.service -p err\n\n## All Ceph-related logs\n\n sudo journalctl |
grep
ceph-health\n\n##
Manual Execution\n\n## Trigger check/scrub immediately\n\n sudo systemctl start
ceph-health.service\n sudo systemctl start zfs-scrub-weekly.service\n\n## Check
status
during
execution\n\n sudo systemctl status ceph-health.service\n sudo watch -n 1 'sudo
systemctl
status
ceph-health.service'\n\n## Customization Guide\n\n### Adding New
Services\n\n1.**Create
service
file:**`/etc/systemd/system/my-service.service`\n [Unit]\n Description=My
Service\n
After=network.target\n [Service]\n Type=oneshot\n
ExecStart=/usr/bin/my-command\n
StandardOutput=journal\n StandardError=journal\n [Install]\n
WantedBy=timers.target\n
1.**Create
timer file (optional):**`/etc/systemd/system/my-service.timer`\n [Unit]\n
Description=My
Service
Timer\n [Timer]\n OnCalendar=daily\n Persistent=true\n [Install]\n
WantedBy=timers.target\n
1.**Reload and enable:**\n sudo systemctl daemon-reload\n sudo systemctl enable
my-service.timer\n
sudo systemctl start my-service.timer\n\n### Modifying Existing
Services\n\n-*Option 1:
Drop-in
override directory**(recommended for package compatibility)\n\n## Create drop-in
directory\n\n sudo
mkdir -p /etc/systemd/system/ceph-health.service.d/\n\n## Create override
file\n\n sudo
nano
/etc/systemd/system/ceph-health.service.d/custom.conf\n\n## [Service]\n\n##
OnFailure=notify-admin@%n.service\n\n## Reload [3]\n\n sudo systemctl
daemon-reload\n\n-
*Option 2:
Edit command**(interactive, creates drop-in automatically)\n\n sudo systemctl
edit
ceph-health.service\n\n## Edit the [Service] section\n\n## Reload happens
automatically\n\n- *Option
3: Direct edit**(not recommended, overwritten on package update)\n\n sudo nano
/etc/systemd/system/ceph-health.service\n sudo systemctl daemon-reload\n\n##
Production
Deployment
Checklist\n\n- [] Enable both timers on first boot:`systemctl enable
ceph-health.timer
zfs-scrub-weekly.timer`\n\n- [] Verify configuration values in
`/etc/default/debvisor-zfs-scrub`for
your environment\n\n- [] Adjust`ZFS_SCRUB_TIMEOUT` if pool size differs
significantly from
defaults\n\n- [] Configure email alerts if monitoring system requires
notification\n\n- []
Set up
log aggregation to collect service logs from journal\n\n- [] Configure alerting
for
service failures
(especially zfs-scrub-weekly)\n\n- [] For multi-node clusters, stagger scrub
schedules to
prevent
simultaneous I/O\n\n- [] Document custom timer schedules for your
environment\n\n- [] Test
service
execution manually before relying on automated schedules\n\n- [] Monitor disk
space for
systemd
journal to prevent log loss\n\n- [ ] Set up metrics collection for scrub
duration and
timing\n\n##
Troubleshooting\n\n### Service Won't Start\n\n## Check service status and
error\n\n sudo
systemctl
status ceph-health.service\n\n## View detailed logs\n\n sudo journalctl -u
ceph-health.service
--no-pager\n\n## Verify unit file syntax\n\n sudo systemd-analyze verify
/etc/systemd/system/ceph-health.service\n\n## Timer Not Running Scheduled
Tasks\n\n##
Verify timer
is enabled and active\n\n sudo systemctl status ceph-health.timer\n\n## Check
next
scheduled run\n\n
sudo systemctl list-timers ceph-health.timer\n\n## If next run is far in future,
restart
timer\n\n
sudo systemctl restart ceph-health.timer\n\n## If timer never ran, check system
time\n\n
date\n
timedatectl\n\n## High Memory/CPU Usage\n\n## Check resource limits\n\n sudo
systemctl
show -p
MemoryLimit ceph-health.service\n\n## Monitor during execution\n\n sudo watch -n
1 'ps aux
| grep
ceph'\n\n## Adjust limits in service file or drop-in override\n\n## Logs Not
Appearing\n\n## Verify
journal is working\n\n sudo systemctl status systemd-journald\n\n## Check
journal disk
usage\n\n
sudo journalctl --disk-usage\n\n## View journal info\n\n sudo journalctl
--unit=ceph-health.service
--follow --all\n\n## References\n\n-
[systemd.service(5)]([https://www.freedesktop.org/software/systemd/man/systemd.service.htm]([https://www.freedesktop.org/software/systemd/man/systemd.service.ht]([https://www.freedesktop.org/software/systemd/man/systemd.service.h]([https://www.freedesktop.org/software/systemd/man/systemd.service.]([https://www.freedesktop.org/software/systemd/man/systemd.service]([https://www.freedesktop.org/software/systemd/man/systemd.servic]([https://www.freedesktop.org/software/systemd/man/systemd.servi]([https://www.freedesktop.org/software/systemd/man/systemd.serv]([https://www.freedesktop.org/software/systemd/man/systemd.ser]([https://www.freedesktop.org/software/systemd/man/systemd.se]([https://www.freedesktop.org/software/systemd/man/systemd.s]([https://www.freedesktop.org/software/systemd/man/systemd.]([https://www.freedesktop.org/software/systemd/man/systemd]([https://www.freedesktop.org/software/systemd/man/system]([https://www.freedesktop.org/software/systemd/man/syste]([https://www.freedesktop.org/software/systemd/man/syst]([https://www.freedesktop.org/software/systemd/man/sys]([https://www.freedesktop.org/software/systemd/man/sy]([https://www.freedesktop.org/software/systemd/man/s]([https://www.freedesktop.org/software/systemd/man/]([https://www.freedesktop.org/software/systemd/man]([https://www.freedesktop.org/software/systemd/ma]([https://www.freedesktop.org/software/systemd/m]([https://www.freedesktop.org/software/systemd/]([https://www.freedesktop.org/software/systemd]([https://www.freedesktop.org/software/system]([https://www.freedesktop.org/software/syste]([https://www.freedesktop.org/software/syst]([https://www.freedesktop.org/software/sys]([https://www.freedesktop.org/software/sy]([https://www.freedesktop.org/software/s]([https://www.freedesktop.org/software/]([https://www.freedesktop.org/software]([https://www.freedesktop.org/softwar]([https://www.freedesktop.org/softwa]([https://www.freedesktop.org/softw]([https://www.freedesktop.org/soft]([https://www.freedesktop.org/sof]([https://www.freedesktop.org/so]([https://www.freedesktop.org/s]([https://www.freedesktop.org/]([https://www.freedesktop.org](https://www.freedesktop.org)/)s)o)f)t)w)a)r)e)/)s)y)s)t)e)m)d)/)m)a)n)/)s)y)s)t)e)m)d).)s)e)r)v)i)c)e).)h)t)m)l)

- Service unit documentation\n\n-
[systemd.timer(5)]([https://www.freedesktop.org/software/systemd/man/systemd.timer.htm]([https://www.freedesktop.org/software/systemd/man/systemd.timer.ht]([https://www.freedesktop.org/software/systemd/man/systemd.timer.h]([https://www.freedesktop.org/software/systemd/man/systemd.timer.]([https://www.freedesktop.org/software/systemd/man/systemd.timer]([https://www.freedesktop.org/software/systemd/man/systemd.time]([https://www.freedesktop.org/software/systemd/man/systemd.tim]([https://www.freedesktop.org/software/systemd/man/systemd.ti]([https://www.freedesktop.org/software/systemd/man/systemd.t]([https://www.freedesktop.org/software/systemd/man/systemd.]([https://www.freedesktop.org/software/systemd/man/systemd]([https://www.freedesktop.org/software/systemd/man/system]([https://www.freedesktop.org/software/systemd/man/syste]([https://www.freedesktop.org/software/systemd/man/syst]([https://www.freedesktop.org/software/systemd/man/sys]([https://www.freedesktop.org/software/systemd/man/sy]([https://www.freedesktop.org/software/systemd/man/s]([https://www.freedesktop.org/software/systemd/man/]([https://www.freedesktop.org/software/systemd/man]([https://www.freedesktop.org/software/systemd/ma]([https://www.freedesktop.org/software/systemd/m]([https://www.freedesktop.org/software/systemd/]([https://www.freedesktop.org/software/systemd]([https://www.freedesktop.org/software/system]([https://www.freedesktop.org/software/syste]([https://www.freedesktop.org/software/syst]([https://www.freedesktop.org/software/sys]([https://www.freedesktop.org/software/sy]([https://www.freedesktop.org/software/s]([https://www.freedesktop.org/software/]([https://www.freedesktop.org/software]([https://www.freedesktop.org/softwar]([https://www.freedesktop.org/softwa]([https://www.freedesktop.org/softw]([https://www.freedesktop.org/soft]([https://www.freedesktop.org/sof]([https://www.freedesktop.org/so]([https://www.freedesktop.org/s]([https://www.freedesktop.org/]([https://www.freedesktop.org]([https://www.freedesktop.or]([https://www.freedesktop.o](https://www.freedesktop.o)r)g)/)s)o)f)t)w)a)r)e)/)s)y)s)t)e)m)d)/)m)a)n)/)s)y)s)t)e)m)d).)t)i)m)e)r).)h)t)m)l)

- Timer unit documentation\n\n-
[ceph(1)]([https://docs.ceph.com/en/latest/man/8/ceph]([https://docs.ceph.com/en/latest/man/8/cep]([https://docs.ceph.com/en/latest/man/8/ce]([https://docs.ceph.com/en/latest/man/8/c]([https://docs.ceph.com/en/latest/man/8/]([https://docs.ceph.com/en/latest/man/8]([https://docs.ceph.com/en/latest/man/]([https://docs.ceph.com/en/latest/man]([https://docs.ceph.com/en/latest/ma]([https://docs.ceph.com/en/latest/m]([https://docs.ceph.com/en/latest/]([https://docs.ceph.com/en/latest]([https://docs.ceph.com/en/lates]([https://docs.ceph.com/en/late]([https://docs.ceph.com/en/lat]([https://docs.ceph.com/en/la]([https://docs.ceph.com/en/l]([https://docs.ceph.com/en/]([https://docs.ceph.com/en]([https://docs.ceph.com/e]([https://docs.ceph.com/]([https://docs.ceph.com]([https://docs.ceph.co]([https://docs.ceph.c]([https://docs.ceph.]([https://docs.ceph]([https://docs.cep]([https://docs.ce]([https://docs.c]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)c)e)p)h).)c)o)m)/)e)n)/)l)a)t)e)s)t)/)m)a)n)/)8)/)c)e)p)h)/)

- Ceph cluster command reference\n\n-
[zpool-scrub(8)]([https://linux.die.net/man/8/zpoo]([https://linux.die.net/man/8/zpo]([https://linux.die.net/man/8/zp]([https://linux.die.net/man/8/z]([https://linux.die.net/man/8/]([https://linux.die.net/man/8]([https://linux.die.net/man/]([https://linux.die.net/man]([https://linux.die.net/ma]([https://linux.die.net/m]([https://linux.die.net/]([https://linux.die.net]([https://linux.die.ne]([https://linux.die.n]([https://linux.die.]([https://linux.die]([https://linux.di]([https://linux.d]([https://linux.]([https://linux]([https://linu]([https://lin]([https://li]([https://l](https://l)i)n)u)x).)d)i)e).)n)e)t)/)m)a)n)/)8)/)z)p)o)o)l)

- ZFS pool scrub documentation\n\n-
[systemd.time(7)]([https://www.freedesktop.org/software/systemd/man/systemd.time.htm]([https://www.freedesktop.org/software/systemd/man/systemd.time.ht]([https://www.freedesktop.org/software/systemd/man/systemd.time.h]([https://www.freedesktop.org/software/systemd/man/systemd.time.]([https://www.freedesktop.org/software/systemd/man/systemd.time]([https://www.freedesktop.org/software/systemd/man/systemd.tim]([https://www.freedesktop.org/software/systemd/man/systemd.ti]([https://www.freedesktop.org/software/systemd/man/systemd.t]([https://www.freedesktop.org/software/systemd/man/systemd.]([https://www.freedesktop.org/software/systemd/man/systemd]([https://www.freedesktop.org/software/systemd/man/system]([https://www.freedesktop.org/software/systemd/man/syste]([https://www.freedesktop.org/software/systemd/man/syst]([https://www.freedesktop.org/software/systemd/man/sys]([https://www.freedesktop.org/software/systemd/man/sy]([https://www.freedesktop.org/software/systemd/man/s]([https://www.freedesktop.org/software/systemd/man/]([https://www.freedesktop.org/software/systemd/man]([https://www.freedesktop.org/software/systemd/ma]([https://www.freedesktop.org/software/systemd/m]([https://www.freedesktop.org/software/systemd/]([https://www.freedesktop.org/software/systemd]([https://www.freedesktop.org/software/system]([https://www.freedesktop.org/software/syste]([https://www.freedesktop.org/software/syst]([https://www.freedesktop.org/software/sys]([https://www.freedesktop.org/software/sy]([https://www.freedesktop.org/software/s]([https://www.freedesktop.org/software/]([https://www.freedesktop.org/software]([https://www.freedesktop.org/softwar]([https://www.freedesktop.org/softwa]([https://www.freedesktop.org/softw]([https://www.freedesktop.org/soft]([https://www.freedesktop.org/sof]([https://www.freedesktop.org/so]([https://www.freedesktop.org/s]([https://www.freedesktop.org/]([https://www.freedesktop.org]([https://www.freedesktop.or]([https://www.freedesktop.o]([https://www.freedesktop.](https://www.freedesktop.)o)r)g)/)s)o)f)t)w)a)r)e)/)s)y)s)t)e)m)d)/)m)a)n)/)s)y)s)t)e)m)d).)t)i)m)e).)h)t)m)l)

- Time specification format\n\n## See Also\n\n- [../opt/README.md](../opt/README.md) -
Operational
scripts and tools\n\n- [../usr/README.md](../usr/README.md) - Runtime services and
CLIs\n\n-
[DebVisor Main README](../README.md) - Project overview\n\n
