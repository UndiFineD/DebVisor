# etc/ Directory - Advanced Configuration Topics\n\n## Version Control & Package

Distribution\n\n###

Systemd .service.d/ Override Patterns\n\nDeployment-specific customizations
should use
systemd
drop-in directories rather than modifying original service files:\n\n##
Directory
structure for
overrides\n\n /etc/systemd/system/debvisor-rpcd.service.d/\n +-- override.conf #
Deployment-specific
overrides\n +-- proxy.conf # HTTP proxy settings\n +-- resource-limits.conf #
Custom
resource
constraints\n\n## Override Examples\n\n- *10-deployment.conf**-
Environment-specific
settings\n\n
[Unit]\n\n## Add deployment-specific requirements\n\n
After=network-online.target
custom-setup.service\n [Service]\n\n## Override or add environment variables\n\n
Environment="DEBVISOR_ENVIRONMENT=production"\n
Environment="DEBVISOR_CLUSTER=primary"\n\n## Custom
restart behavior per environment\n\n Restart=on-failure\n RestartSec=5s\n\n-
*20-resources.conf**-
Resource limits per deployment\n\n [Service]\n\n## Production resource
limits\n\n
MemoryMax=2G\n
CPUQuota=100%\n TasksMax=2000\n\n## Logging configuration\n\n
StandardOutput=journal\n
StandardError=journal\n SyslogIdentifier=debvisor-rpcd-prod\n\n## Versioning
Strategy\n\n### Service
Versioning\n\n debvisor-rpcd.service # Current (symlink or alias)\n
debvisor-rpcd.service.1.0 #
Version 1.0 (stable)\n debvisor-rpcd.service.1.1 # Version 1.1 (with features)\n
debvisor-rpcd.service.2.0.beta # Version 2.0 beta (testing)\n\n### Configuration
Versioning\n\n
/etc/debvisor/rpcd.conf # Current\n /etc/debvisor/rpcd.conf.1.0 # Version 1.0\n
/etc/debvisor/rpcd.conf.1.0.bak # Backup before upgrade\n\n### Deployment
Templates\n\n-
*Lab
Environment**(`deployment-lab.d/override.conf`)\n\n [Service]\n MemoryMax=512M\n
CPUQuota=50%\n
Environment="DEBVISOR_LOG_LEVEL=debug"\n\n- *Staging
Environment**(`deployment-staging.d/override.conf`)\n\n [Service]\n
MemoryMax=1G\n
CPUQuota=75%\n
Environment="DEBVISOR_LOG_LEVEL=info"\n\n- *Production
Environment**(`deployment-prod.d/override.conf`)\n\n [Service]\n MemoryMax=2G\n
CPUQuota=100%\n
Environment="DEBVISOR_LOG_LEVEL=warn"\n Restart=always\n RestartSec=10s\n\n##
Security\n\n### File
Permissions & Ownership\n\n### Standard Service File Permissions\n\n## Service
files
should be
readable but not writable by regular users\n\n chmod 644
/etc/systemd/system/debvisor-*.service\n
chmod 644 /etc/systemd/system/debvisor-*.timer\n chmod 755
/etc/systemd/system/debvisor-*.service.d/\n\n## Configuration files should be
readable but
not
writable\n\n chmod 640 /etc/debvisor/*.conf\n chmod 640
/etc/debvisor/debvisor-secrets.conf #
Secrets file\n\n## Ownership (root:root for system-wide services)\n\n chown
root:root
/etc/systemd/system/debvisor-*.service\n chown root:root
/etc/debvisor/*.conf\n\n##
Secrets file
should have restrictive permissions\n\n chown root:debvisor
/etc/debvisor/debvisor-secrets.conf\n
chmod 640 /etc/debvisor/debvisor-secrets.conf\n\n## Permission Verification
Script\n\n

## !/bin/bash\n\n## Verify systemd service file permissions\n\n echo "Checking systemd

service file

permissions..."\n\n## Service files should be 0644\n\n find /etc/systemd/system
-name
"debvisor-*.service" -type f ! -perm 644 \\n && echo "[warn]? Service files with
incorrect
permissions:" && \\n find /etc/systemd/system -name "debvisor-*.service" -type f
! -perm
644
-ls\n\n## Timer files should be 0644\n\n find /etc/systemd/system -name
"debvisor-*.timer"
-type f !
-perm 644 \\n && echo "[warn]? Timer files with incorrect permissions:" && \\n
find
/etc/systemd/system -name "debvisor-*.timer" -type f ! -perm 644 -ls\n\n##
Config files
should be
0640\n\n find /etc/debvisor -name "*.conf" -type f ! -perm 640 \\n && echo
"[warn]? Config
files
with incorrect permissions:" && \\n find /etc/debvisor -name "*.conf" -type f !
-perm 640
-ls\n echo
"Permission check complete."\n\n## Privilege & Capability Analysis\n\n###
debvisor-rpcd.service\n\nRequired Privileges:\n [Service]\n\n## Must bind to
port 5000
(requires
CAP_NET_BIND_SERVICE or run as root)\n\n## Solution: Run as root or use socket
activation
with lower
port\n\n## Must access Ceph cluster sockets (typically in /var/run/ceph/)\n\n##
Solution:
Add user
to ceph group or use appropriate mount\n\n## Must create logs in
/var/log/debvisor/\n\n##
Solution:
Pre-create directory with appropriate permissions\n\n## Recommended: Run as
debvisor user
with
necessary capabilities\n\n User=debvisor\n Group=debvisor\n
CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_SETUID CAP_SETGID\n
AmbientCapabilities=CAP_NET_BIND_SERVICE\n\n## debvisor-panel.service\n\n
[Service]\n\n##
Requires:
Port binding, configuration file access\n\n User=debvisor\n Group=debvisor\n
CapabilityBoundingSet=CAP_NET_BIND_SERVICE\n
AmbientCapabilities=CAP_NET_BIND_SERVICE\n\n## User &
Group Policies\n\n### Recommended Setup\n\n## Create debvisor system user\n\n
useradd
--system
--shell /usr/sbin/nologin --home /var/lib/debvisor debvisor\n\n## Create
debvisor
group\n\n groupadd
--system debvisor\n\n## Add necessary groups for cluster access\n\n usermod -a
-G ceph
debvisor #
For Ceph cluster access\n usermod -a -G libvirt debvisor # For libvirt access
(if
needed)\n usermod
-a -G docker debvisor # For Docker access (if needed)\n\n## Create necessary
directories
with
correct permissions\n\n mkdir -p /var/log/debvisor\n chown debvisor:debvisor
/var/log/debvisor\n
chmod 750 /var/log/debvisor\n mkdir -p /var/lib/debvisor\n chown
debvisor:debvisor
/var/lib/debvisor\n chmod 750 /var/lib/debvisor\n mkdir -p /var/run/debvisor\n
chown
debvisor:debvisor /var/run/debvisor\n chmod 750 /var/run/debvisor\n\n## Security
Hardening
Checklist\n\n## Recommended systemd security directives for all debvisor
services\n\n
[Service]\n\n## Filesystem isolation\n\n PrivateTmp=yes\n ProtectSystem=strict\n
ProtectHome=yes\n
ReadWritePaths=/var/log/debvisor /var/lib/debvisor /var/run/debvisor\n\n##
Process
isolation\n\n
NoNewPrivileges=yes\n PrivateDevices=yes\n ProtectKernelLogs=yes\n
ProtectKernelModules=yes\n
ProtectKernelTunables=yes\n ProtectControlGroups=yes\n ProtectClock=yes\n\n##
Capabilities
restriction\n\n CapabilityBoundingSet=~CAP_SYS_ADMIN CAP_SYS_BOOT CAP_NET_ADMIN
CAP_SYS_NICE\n
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6\n\n## Privilege escalation
prevention\n\n
LockPersonality=yes\n RestrictNamespaces=yes\n RestrictRealtime=yes\n
RemoveIPC=yes\n\n##
System
call filtering (optional, requires libseccomp)\n\n
SystemCallFilter=@system-service
@basic-io
@io-event @ipc @network-io\n SystemCallErrorNumber=EPERM\n\n## Robustness Across
Reboots\n\n###
Persistence Configuration\n\n### Timer Persistence\n\n## Timers should be
configured to
survive
reboots\n\n [Timer]\n\n## Run timer on boot if it was missed\n\n
OnBootSec=5min\n\n##
Persist timer
state across reboots\n\n Persistent=true\n\n## Accuracy settings (balance
between timing
and system
load)\n\n AccuracySec=1min\n RandomizedDelaySec=0\n [Install]\n
WantedBy=timers.target\n\n## Service
Persistence\n\n [Unit]\n\n## Ensure service starts early in boot\n\n
After=network-online.target\n
Wants=network-online.target\n [Service]\n\n## Auto-restart on failure\n\n
Restart=on-failure\n
RestartSec=10s\n\n## Timeout for long-running initialization\n\n
TimeoutStartSec=300\n
TimeoutStopSec=30\n [Install]\n\n## Enable on system boot\n\n
WantedBy=multi-user.target\n\n##
Recovery Procedures\n\n### If Service Fails on Startup\n\n## 1. Check service
status\n\n
systemctl
status debvisor-rpcd.service\n\n## 2. View recent logs\n\n journalctl -u
debvisor-rpcd.service -n 50
--no-pager\n\n## 3. Test configuration\n\n /opt/services/rpc/bin/rpcd
--validate-config\n\n## 4.
Start with verbose logging\n\n systemctl start debvisor-rpcd.service\n systemctl
status
debvisor-rpcd.service -l --no-pager\n\n## 5. If still failing, disable
auto-start for
debugging\n\n
systemctl disable debvisor-rpcd.service\n\n## ... debug and fix\n\n systemctl
enable
debvisor-rpcd.service\n\n## If Timer Doesn't Run After Reboot\n\n## 1. Verify
timer is
enabled and
started\n\n systemctl is-enabled debvisor-health-check.timer\n systemctl
is-active
debvisor-health-check.timer\n\n## 2. Check timer schedule and next run time\n\n
systemctl
list-timers debvisor-health-check.timer\n\n## 3. View timer logs\n\n journalctl
-u
debvisor-health-check.timer -n 20 --no-pager\n\n## 4. Manually trigger the
associated
service for
testing\n\n systemctl start debvisor-health-check.service\n\n## 5. Reload and
restart
timer if
needed\n\n systemctl daemon-reload\n systemctl restart
debvisor-health-check.timer\n\n##
Boot-Time
Testing & Validation\n\n### Test Boot-Time Service Startup\n\n #!/bin/bash\n\n##
test-boot-startup.sh - Verify services start correctly after reboot\n\n echo
"Testing
boot-time
service startup..."\n\n## Give systemd time to start services\n\n sleep 10\n\n##
Check
critical
services are running\n\n services=("debvisor-rpcd" "debvisor-panel"
"debvisor-health-check.timer")\n
for service in "${services[@]}"; do\n if systemctl is-active --quiet "$service.service" ||
\\n
systemctl is-active --quiet "$service"; then\n echo "? $service is running"\n
else\n echo
"?
$service failed to start"\n systemctl status "$service" -l\n journalctl -u
"$service" -n
20
--no-pager\n fi\n done\n\n## Verify RPC service responds to requests\n\n if curl
-s
[http://localhost:5000/api/health]([http://localhost:5000/api/healt]([http://localhost:5000/api/heal]([http://localhost:5000/api/hea]([http://localhost:5000/api/he]([http://localhost:5000/api/h]([http://localhost:5000/api/]([http://localhost:5000/api]([http://localhost:5000/ap]([http://localhost:5000/a]([http://localhost:5000/]([http://localhost:5000]([http://localhost:500]([http://localhost:50]([http://localhost:5]([http://localhost:]([http://localhost]([http://localhos]([http://localho]([http://localh]([http://local]([http://loca]([http://loc]([http://lo]([http://l](http://l)o)c)a)l)h)o)s)t):)5)0)0)0)/)a)p)i)/)h)e)a)l)t)h)

>/dev/null; then\n echo "? RPC service responding to requests"\n else\n echo "?
RPC
service not
responding"\n fi\n\n## Check for startup errors in journal\n\n if journalctl
--since "10
seconds
ago" | grep -i error | grep -i debvisor; then\n echo "[warn]? Found startup errors in
journal"\n
journalctl --since "10 seconds ago" | grep -i debvisor\n fi\n\n## Pre-Reboot
Validation\n\n

## !/bin/bash\n\n## pre-reboot-check.sh - Verify system is ready for safe reboot\n\n echo

"Running

pre-reboot checks..."\n\n## 1. Verify all service files are valid\n\n
systemd-analyze
verify
/etc/systemd/system/debvisor-*.service 2>&1\n if [$? -ne 0]; then\n echo "?
Service file
validation
failed"\n exit 1\n fi\n\n## 2. Check for services in failed state\n\n if
systemctl
list-units
--failed | grep debvisor; then\n echo "[warn]? Found debvisor services in failed state"\n
fi\n\n##

1. Verify timer schedules are correct\n\n systemctl list-timers
debvisor-*.timer\n\n## 4.
Confirm
configuration files are accessible\n\n for conf in /etc/debvisor/*.conf; do\n if
[-r
"$conf"];
then\n echo "? $conf is readable"\n else\n echo "? $conf is not readable"\n fi\n
done\n
echo
"Pre-reboot checks complete. Safe to reboot."\n\n## Post-Reboot Validation\n\n

## !/bin/bash\n\n##

post-reboot-check.sh - Verify system recovered correctly after reboot\n\n echo
"Running
post-reboot
checks (run 2-3 minutes after boot)..."\n\n## 1. Verify all services started\n\n
systemctl
status
debvisor-*.service debvisor-*.timer\n\n## 2. Check service response times
(should be
fast)\n\n curl
-w "@curl-format.txt" -o /dev/null -s
[http://localhost:5000/api/health]([http://localhost:5000/api/healt]([http://localhost:5000/api/heal]([http://localhost:5000/api/hea]([http://localhost:5000/api/he]([http://localhost:5000/api/h]([http://localhost:5000/api/]([http://localhost:5000/api]([http://localhost:5000/ap]([http://localhost:5000/a]([http://localhost:5000/]([http://localhost:5000]([http://localhost:500]([http://localhost:50]([http://localhost:5]([http://localhost:]([http://localhost]([http://localhos]([http://localho]([http://localh]([http://local]([http://loca]([http://loc]([http://lo]([http://l](http://l)o)c)a)l)h)o)s)t):)5)0)0)0)/)a)p)i)/)h)e)a)l)t)h)\n\n##

1. Verify no error floods in logs\n\n error_count=$(journalctl --since "5
minutes ago" \\n
| grep -i
"debvisor\|rpcd\|panel" \\n | grep -i "error\|fail" \\n | wc -l)\n echo "Errors in last 5
minutes:
$error_count"\n\n## 4. Check persistent state was preserved\n\n if [-f
/var/lib/debvisor/state.json]; then\n echo "? Persistent state file present"\n
jq .
/var/lib/debvisor/state.json 2>/dev/null | head -20\n fi\n echo "Post-reboot checks
complete."\n\n##
References\n\n- Systemd documentation:
[https://www.freedesktop.org/software/systemd/man/]([https://www.freedesktop.org/software/systemd/man]([https://www.freedesktop.org/software/systemd/ma]([https://www.freedesktop.org/software/systemd/m]([https://www.freedesktop.org/software/systemd/]([https://www.freedesktop.org/software/systemd]([https://www.freedesktop.org/software/system]([https://www.freedesktop.org/software/syste]([https://www.freedesktop.org/software/syst]([https://www.freedesktop.org/software/sys]([https://www.freedesktop.org/software/sy]([https://www.freedesktop.org/software/s]([https://www.freedesktop.org/software/]([https://www.freedesktop.org/software]([https://www.freedesktop.org/softwar]([https://www.freedesktop.org/softwa]([https://www.freedesktop.org/softw]([https://www.freedesktop.org/soft]([https://www.freedesktop.org/sof]([https://www.freedesktop.org/so]([https://www.freedesktop.org/s]([https://www.freedesktop.org/]([https://www.freedesktop.org]([https://www.freedesktop.or]([https://www.freedesktop.o]([https://www.freedesktop.]([https://www.freedesktop]([https://www.freedeskto]([https://www.freedeskt]([https://www.freedesk]([https://www.freedes]([https://www.freede]([https://www.freed]([https://www.free]([https://www.fre]([https://www.fr]([https://www.f]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)f)r)e)e)d)e)s)k)t)o)p).)o)r)g)/)s)o)f)t)w)a)r)e)/)s)y)s)t)e)m)d)/)m)a)n)/)\n\n-
Service file format: `man 5 systemd.service`\n\n- Timer format: `man 5
systemd.timer`\n\n-
Drop-in
files: `man 5 systemd.unit`\n\n- Security directives:
[https://www.freedesktop.org/software/systemd/man/systemd.exec.html]([https://www.freedesktop.org/software/systemd/man/systemd.exec.htm]([https://www.freedesktop.org/software/systemd/man/systemd.exec.ht]([https://www.freedesktop.org/software/systemd/man/systemd.exec.h]([https://www.freedesktop.org/software/systemd/man/systemd.exec.]([https://www.freedesktop.org/software/systemd/man/systemd.exec]([https://www.freedesktop.org/software/systemd/man/systemd.exe]([https://www.freedesktop.org/software/systemd/man/systemd.ex]([https://www.freedesktop.org/software/systemd/man/systemd.e]([https://www.freedesktop.org/software/systemd/man/systemd.]([https://www.freedesktop.org/software/systemd/man/systemd]([https://www.freedesktop.org/software/systemd/man/system]([https://www.freedesktop.org/software/systemd/man/syste]([https://www.freedesktop.org/software/systemd/man/syst]([https://www.freedesktop.org/software/systemd/man/sys]([https://www.freedesktop.org/software/systemd/man/sy]([https://www.freedesktop.org/software/systemd/man/s]([https://www.freedesktop.org/software/systemd/man/]([https://www.freedesktop.org/software/systemd/man]([https://www.freedesktop.org/software/systemd/ma]([https://www.freedesktop.org/software/systemd/m]([https://www.freedesktop.org/software/systemd/]([https://www.freedesktop.org/software/systemd]([https://www.freedesktop.org/software/system]([https://www.freedesktop.org/software/syste]([https://www.freedesktop.org/software/syst]([https://www.freedesktop.org/software/sys]([https://www.freedesktop.org/software/sy]([https://www.freedesktop.org/software/s]([https://www.freedesktop.org/software/]([https://www.freedesktop.org/software]([https://www.freedesktop.org/softwar]([https://www.freedesktop.org/softwa]([https://www.freedesktop.org/softw]([https://www.freedesktop.org/soft]([https://www.freedesktop.org/sof]([https://www.freedesktop.org/so]([https://www.freedesktop.org/s]([https://www.freedesktop.org/]([https://www.freedesktop.org]([https://www.freedesktop.or]([https://www.freedesktop.o]([https://www.freedesktop.]([https://www.freedesktop]([https://www.freedeskto]([https://www.freedeskt]([https://www.freedesk]([https://www.freedes]([https://www.freede]([https://www.freed]([https://www.free]([https://www.fre](https://www.fre)e)d)e)s)k)t)o)p).)o)r)g)/)s)o)f)t)w)a)r)e)/)s)y)s)t)e)m)d)/)m)a)n)/)s)y)s)t)e)m)d).)e)x)e)c).)h)t)m)l)\n\n
