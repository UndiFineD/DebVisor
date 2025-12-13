# DebVisor Quick Reference\n\n## Get Grafana Admin Password (Kubernetes)\n\n kubectl

--namespace

monitoring get secrets prometheus-stack-grafana \\n\n - o
jsonpath="{.data.admin-password}" | base64
-d ; echo\n\n## Common Operations\n\n### Containers-first workload
checklist\n\n-
Prefer**containers**when:\n\n- The workload is a new or refactored application,
microservice, or
web/API service.\n\n- You already build and publish container images via
CI/CD.\n\n-
Horizontal
scaling and rolling updates are desired.\n\n- Prefer**VMs**when:\n\n- You must
run a
legacy OS or
vendor appliance that only ships as a VM image.\n\n- You need strong OS-level
isolation,
custom
kernels/modules, or hardware passthrough.\n\n- The surrounding environment
expects VM
artifacts
(qcow2/raw/vmdk, cloud-init images).\n\n### DNS Management\n\n## Manual DNS
update\n\n
echo "server
10.10.0.1\n zone debvisor.local\n update add myhost.debvisor.local 300 A
10.10.0.50\n
send" |
nsupdate -k /etc/debvisor/nsupdate.key\n\n## Check zone status\n\n rndc status\n
dig
@10.10.0.1
debvisor.local AXFR\n\n## DHCP Leases\n\n## View active leases\n\n cat
/var/lib/dnsmasq/dnsmasq.leases\n\n## Reload dnsmasq\n\n systemctl reload
dnsmasq\n\n##
TSIG Key
Rotation\n\n## Generate new key\n\n /usr/local/bin/tsig-keygen.sh\n\n## Verify
rotation\n\n rndc
tsig-list\n\n## Cluster Operations\n\n## Join new node\n\n
/usr/local/bin/debvisor-join.sh\n\n##
Migrate VM\n\n /usr/local/bin/debvisor-migrate.sh vm-name target-host\n\n##
Check cluster
health\n\n
ceph -s\n kubectl get nodes\n virsh list --all\n\n## Monitoring\n\n## Check
Prometheus
targets\n\n
curl
[http://10.10.0.1:9090/api/v1/targets]([http://10.10.0.1:9090/api/v1/target]([http://10.10.0.1:9090/api/v1/targe]([http://10.10.0.1:9090/api/v1/targ]([http://10.10.0.1:9090/api/v1/tar]([http://10.10.0.1:9090/api/v1/ta]([http://10.10.0.1:9090/api/v1/t]([http://10.10.0.1:9090/api/v1/]([http://10.10.0.1:9090/api/v1]([http://10.10.0.1:9090/api/v]([http://10.10.0.1:9090/api/]([http://10.10.0.1:9090/api]([http://10.10.0.1:9090/ap]([http://10.10.0.1:9090/a]([http://10.10.0.1:9090/]([http://10.10.0.1:9090]([http://10.10.0.1:909]([http://10.10.0.1:90]([http://10.10.0.1:9]([http://10.10.0.1:]([http://10.10.0.1]([http://10.10.0.]([http://10.10.0]([http://10.10.]([http://10.10]([http://10.1]([http://10.]([http://10]([http://1](http://1)0).)1)0).)0).)1):)9)0)9)0)/)a)p)i)/)v)1)/)t)a)r)g)e)t)s)\n\n##
Query metrics\n\n curl
'[http://10.10.0.1:9090/api/v1/query?query=bind_queries_total']([http://10.10.0.1:9090/api/v1/query?query=bind_queries_total]([http://10.10.0.1:9090/api/v1/query?query=bind_queries_tota]([http://10.10.0.1:9090/api/v1/query?query=bind_queries_tot]([http://10.10.0.1:9090/api/v1/query?query=bind_queries_to]([http://10.10.0.1:9090/api/v1/query?query=bind_queries_t]([http://10.10.0.1:9090/api/v1/query?query=bind*queries*]([http://10.10.0.1:9090/api/v1/query?query=bind*queries]([http://10.10.0.1:9090/api/v1/query?query=bind*querie]([http://10.10.0.1:9090/api/v1/query?query=bind*queri]([http://10.10.0.1:9090/api/v1/query?query=bind*quer]([http://10.10.0.1:9090/api/v1/query?query=bind*que]([http://10.10.0.1:9090/api/v1/query?query=bind*qu]([http://10.10.0.1:9090/api/v1/query?query=bind*q]([http://10.10.0.1:9090/api/v1/query?query=bind*]([http://10.10.0.1:9090/api/v1/query?query=bind]([http://10.10.0.1:9090/api/v1/query?query=bin]([http://10.10.0.1:9090/api/v1/query?query=bi]([http://10.10.0.1:9090/api/v1/query?query=b]([http://10.10.0.1:9090/api/v1/query?query=]([http://10.10.0.1:9090/api/v1/query?query]([http://10.10.0.1:9090/api/v1/query?quer]([http://10.10.0.1:9090/api/v1/query?que]([http://10.10.0.1:9090/api/v1/query?qu]([http://10.10.0.1:9090/api/v1/query?q]([http://10.10.0.1:9090/api/v1/query?]([http://10.10.0.1:9090/api/v1/query]([http://10.10.0.1:9090/api/v1/quer]([http://10.10.0.1:9090/api/v1/que]([http://10.10.0.1:9090/api/v1/qu]([http://10.10.0.1:9090/api/v1/q]([http://10.10.0.1:9090/api/v1/]([http://10.10.0.1:9090/api/v1]([http://10.10.0.1:9090/api/v]([http://10.10.0.1:9090/api/]([http://10.10.0.1:9090/api](http://10.10.0.1:9090/api)/)v)1)/)q)u)e)r)y)?)q)u)e)r)y)=)b)i)n)d)*)q)u)e)r)i)e)s)*)t)o)t)a)l)')\n\n##
View logs\n\n kubectl logs -n debvisor-monitoring -l
app=synthetic-workload\n\n##
Security\n\n## Run
MFA enforcement\n\n ansible-playbook -i inventory
ansible/playbooks/enforce-mfa.yml\n\n##
Quarantine
compromised host\n\n ansible-playbook -i inventory -e "target_host=node3" \\n
ansible/playbooks/quarantine-host.yml\n\n## Block IPs\n\n ansible-playbook -i
inventory -e
"blocked_ips=1.2.3.4,5.6.7.8" \\n ansible/playbooks/block-ips.yml\n\n##
Compliance\n\n##
Query audit
logs\n\n journalctl -u auditd | grep -i "config"\n\n## Check immutable log status\n\n aws
s3api
get-object-lock-configuration \\n\n - -bucket debvisor-compliance-archive\n\n##
Search
compliance
events\n\n curl -X GET
"[http://es01:9200/debvisor-compliance-*/_search"]([http://es01:9200/debvisor-compliance-*/_search]([http://es01:9200/debvisor-compliance-*/_searc]([http://es01:9200/debvisor-compliance-*/_sear]([http://es01:9200/debvisor-compliance-*/_sea]([http://es01:9200/debvisor-compliance-*/*se]([http://es01:9200/debvisor-compliance-*/*s]([http://es01:9200/debvisor-compliance-*/*]([http://es01:9200/debvisor-compliance-*/]([http://es01:9200/debvisor-compliance-*]([http://es01:9200/debvisor-compliance-]([http://es01:9200/debvisor-compliance]([http://es01:9200/debvisor-complianc]([http://es01:9200/debvisor-complian]([http://es01:9200/debvisor-complia]([http://es01:9200/debvisor-compli]([http://es01:9200/debvisor-compl]([http://es01:9200/debvisor-comp]([http://es01:9200/debvisor-com]([http://es01:9200/debvisor-co]([http://es01:9200/debvisor-c]([http://es01:9200/debvisor-]([http://es01:9200/debvisor]([http://es01:9200/debviso]([http://es01:9200/debvis]([http://es01:9200/debvi]([http://es01:9200/debv]([http://es01:9200/deb]([http://es01:9200/de]([http://es01:9200/d]([http://es01:9200/]([http://es01:9200]([http://es01:920]([http://es01:92]([http://es01:9]([http://es01:](http://es01:)9)2)0)0)/)d)e)b)v)i)s)o)r)-)c)o)m)p)l)i)a)n)c)e)-)*)/)*)s)e)a)r)c)h)")
\\n\n - H 'Content-Type: application/json' \\n\n - d '{"query": {"term":
{"compliance_tag":
"MFA"}}}'\n\n## File Locations\n\nSee `DebVisor_initial.md` for complete
canonical
location
table.\n\n
