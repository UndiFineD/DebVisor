# DebVisor Quick Reference

## Get Grafana Admin Password (Kubernetes)

    kubectl --namespace monitoring get secrets prometheus-stack-grafana \
      -o jsonpath="{.data.admin-password}" | base64 -d ; echo

## Common Operations

### Containers-first workload checklist

- Prefer**containers**when:
- The workload is a new or refactored application, microservice, or web/API service.
- You already build and publish container images via CI/CD.
- Horizontal scaling and rolling updates are desired.
- Prefer**VMs**when:
- You must run a legacy OS or vendor appliance that only ships as a VM image.
- You need strong OS-level isolation, custom kernels/modules, or hardware passthrough.
- The surrounding environment expects VM artifacts (qcow2/raw/vmdk, cloud-init images).

### DNS Management

## Manual DNS update

    echo "server 10.10.0.1
    zone debvisor.local
    update add myhost.debvisor.local 300 A 10.10.0.50
    send" | nsupdate -k /etc/debvisor/nsupdate.key

## Check zone status

    rndc status
    dig @10.10.0.1 debvisor.local AXFR

## DHCP Leases

## View active leases

    cat /var/lib/dnsmasq/dnsmasq.leases

## Reload dnsmasq

    systemctl reload dnsmasq

## TSIG Key Rotation

## Generate new key

    /usr/local/bin/tsig-keygen.sh

## Verify rotation

    rndc tsig-list

## Cluster Operations

## Join new node

    /usr/local/bin/debvisor-join.sh

## Migrate VM

    /usr/local/bin/debvisor-migrate.sh vm-name target-host

## Check cluster health

    ceph -s
    kubectl get nodes
    virsh list --all

## Monitoring

## Check Prometheus targets

    curl [http://10.10.0.1:9090/api/v1/targets](http://10.10.0.1:9090/api/v1/targets)

## Query metrics

    curl '[http://10.10.0.1:9090/api/v1/query?query=bind_queries_total'](http://10.10.0.1:9090/api/v1/query?query=bind_queries_total')

## View logs

    kubectl logs -n debvisor-monitoring -l app=synthetic-workload

## Security

## Run MFA enforcement

    ansible-playbook -i inventory ansible/playbooks/enforce-mfa.yml

## Quarantine compromised host

    ansible-playbook -i inventory -e "target_host=node3" \
      ansible/playbooks/quarantine-host.yml

## Block IPs

    ansible-playbook -i inventory -e "blocked_ips=1.2.3.4,5.6.7.8" \
      ansible/playbooks/block-ips.yml

## Compliance

## Query audit logs

    journalctl -u auditd | grep -i "config"

## Check immutable log status

    aws s3api get-object-lock-configuration \
      --bucket debvisor-compliance-archive

## Search compliance events

    curl -X GET "[http://es01:9200/debvisor-compliance-*/_search"](http://es01:9200/debvisor-compliance-*/_search") \
      -H 'Content-Type: application/json' \
      -d '{"query": {"term": {"compliance_tag": "MFA"}}}'

## File Locations

See `DebVisor_initial.md` for complete canonical location table.
