# DebVisor Addons Architecture\n\nThis directory contains optional addon components that

extend

DebVisor cluster functionality. Addons are organized by deployment mechanism: Docker
Compose for
standalone services and Kubernetes manifests for cluster-wide deployments.\n\n## Addon
Architecture
Overview\n\n### What is an addon\n\nAn addon is a self-contained, optional component
that:\n\n-
Provides specialized functionality (monitoring, ingress, storage, security)\n\n- Can be
independently enabled or disabled\n\n- Declares dependencies on other addons or core
DebVisor
services\n\n- Includes deployment manifests and configuration templates\n\n- Is documented
with
usage and troubleshooting guidance\n\n### Addon Discovery\n\nAddons are discovered at
build time and
install time:\n1.**Build Time**: `sync-addons-playbook.sh`scans this directory for addon
manifests\n1.**Install Time**:`debvisor-firstboot.sh`evaluates profile
selections\n1.**Runtime**:
Operators enable addons via CLI or web panel\nEach addon is uniquely identified by its
directory
name (e.g.,`prometheus-monitoring`,`traefik`,`ceph-csi-rbd`).\n\n### Addon Types\n\n| Type
|
Location | Mechanism | Use Case |\n|------|----------|-----------|----------|\n|**Docker
Compose**|
`compose/`| Docker daemon | Standalone container stacks on DebVisor nodes
|\n|**Kubernetes**|`k8s/`|
kubectl apply | Cluster-wide services and controllers |\n\n### Addon Lifecycle\n\n
Discovery
(build/firstboot)\n v\n Dependency Check (validate prerequisites)\n v\n Metadata
Validation
(addon.yaml schema)\n v\n User Selection (profile, CLI, or web panel)\n v\n Deployment
(docker-compose or kubectl apply)\n v\n Verification (health checks, readiness probes)\n
v\n
Rollback (if deployment fails, revert to previous state)\n\n## Directory Structure\n\n
addons/\n +--
README.md # This file\n +-- compose/ # Docker Compose addons\n | +-- README.md\n | +--
traefik/\n |
| +-- addon.yaml # Metadata (name, dependencies, resources)\n | | +-- traefik-compose.yml\n | +--
gitlab-runner/\n | +-- addon.yaml\n | +-- gitlab-runner-compose.yml\n +-- k8s/ #
Kubernetes addons\n
+-- README.md\n +-- monitoring/\n | +-- addon.yaml\n | +-- prometheus.yaml\n | +--
grafana.yaml\n |
+-- ...\n +-- ingress/\n | +-- addon.yaml\n | +-- nginx-ingress.yaml\n +-- storage/\n |
+--
addon.yaml\n | +-- ceph-csi-rbd.yaml\n | +-- ceph-csi-cephfs.yaml\n | +--
zfs-localpv.yaml\n +--
csi/\n +-- security/\n +-- ...\n\n## Addon Metadata Format (`addon.yaml`)\n\nEach addon
includes
an`addon.yaml`manifest describing its properties:\n apiVersion: debvisor.io/v1alpha1\n
kind: Addon\n
metadata:\n name: prometheus-monitoring\n description: Prometheus + Grafana monitoring
stack for
Kubernetes\n category: monitoring\n version: "1.0.0"\n spec:\n\n## Deployment
mechanism\n\n type:
kubernetes # or "compose"\n\n## Resource requirements\n\n resources:\n cpu: "500m"\n
memory: "1Gi"\n
disk: "10Gi" # Persistent volume size\n\n## Platform/architecture support\n\n
supported_architectures:\n\n- amd64\n\n- arm64\n\n## Dependencies on other addons\n\n
dependencies:\n\n- addon: kubernetes-core # Required addon\n\n version: ">=1.25.0"\n\n-
addon:
networking # Required addon\n\n## Conflicting addons (cannot be enabled together)\n\n
conflicts:\n\n- addon: other-monitoring-stack\n\n## Lifecycle hooks\n\n hooks:\n
pre_deploy: # Run
before deployment\n\n- script: validate-prereqs.sh\n\n post_deploy: # Run after
deployment\n\n-
script: configure-monitoring.sh\n\n pre_remove: # Run before removal\n\n- script:
backup-data.sh\n\n## Health checks\n\n healthcheck:\n type: http\n endpoint:
"[http://localhost:9090/-/healthy"]([http://localhost:9090/-/healthy]([http://localhost:9090/-/health]([http://localhost:9090/-/healt]([http://localhost:9090/-/heal]([http://localhost:9090/-/hea]([http://localhost:9090/-/he]([http://localhost:9090/-/h](http://localhost:9090/-/h)e)a)l)t)h)y)")\n
interval: 30s\n timeout: 5s\n\n## Configuration schema (for validation)\n\n config:\n
properties:\n
prometheus_retention_days:\n type: integer\n default: 30\n description: "Prometheus data
retention
period (days)"\n grafana_admin_password:\n type: string\n description: "Initial Grafana
admin
password"\n enable_alerting:\n type: boolean\n default: true\n\n## Installation
instructions\n\n
install:\n instructions: |\n\n 1. Ensure Kubernetes cluster is ready:`kubectl get
nodes`\n\n 1.
Create monitoring namespace: `kubectl create namespace monitoring`\n\n 1. Deploy addon:
`kubectl
apply -f monitoring/`\n\n 1. Verify: `kubectl get pods -n monitoring`\n\n## Removal
instructions\n\n
remove:\n instructions: |\n\n 1. Backup Prometheus data: `kubectl exec -it prometheus-0 --
tar czf
/tmp/backup.tgz /prometheus`\n\n 1. Remove addon: `kubectl delete -f monitoring/`\n\n 1.
Clean up
volumes: `kubectl delete pvc --all -n monitoring`\n\n## Post-install validation\n\n
validation:\n
checks:\n\n- name: "Prometheus running"\n\n command: "kubectl get deployment prometheus -n
monitoring"\n\n- name: "Grafana accessible"\n\n command: "curl -f
[http://localhost:3000]([http://localhost:300]([http://localhost:30]([http://localhost:3]([http://localhost:]([http://localhost]([http://localhos]([http://localho](http://localho)s)t):)3)0)0)0)
|| exit 1"\n\n### Addon Metadata Schema Fields\n\n| Field | Required | Type | Description
|\n|-------|----------|------|-------------|\n| `metadata.name`| Yes | string | Unique addon
identifier (alphanumeric + dash) |\n|`metadata.description`| Yes | string | Human-readable
description |\n|`metadata.category`| Yes | string | Category: monitoring, ingress,
storage,
security, networking, other |\n|`metadata.version`| Yes | string | Addon version (semver)
|\n|`spec.type`| Yes | enum | Deployment type:`kubernetes`or`compose`|\n|`spec.resources.cpu`| Yes |
string | CPU reservation (k8s format, e.g., "500m", "1") |\n|`spec.resources.memory`| Yes
| string |
Memory reservation (k8s format, e.g., "512Mi", "1Gi") |\n|`spec.resources.disk`| No |
string |
Persistent storage requirement |\n|`spec.supported_architectures`| Yes | list |
Architectures:
amd64, arm64, ppc64le, s390x |\n|`spec.dependencies`| No | list | Required addons (name +
optional
version) |\n|`spec.conflicts`| No | list | Conflicting addons (cannot be enabled together)
|\n|`spec.hooks.pre_deploy`| No | list | Scripts to run before deployment
|\n|`spec.hooks.post*deploy`| No | list | Scripts to run after deployment
|\n|`spec.healthcheck.type`| No | enum | Health check type: http, tcp, exec, kubernetes
|\n|`spec.install.instructions`| Yes | string | Installation instructions
|\n|`spec.remove.instructions`| Yes | string | Removal instructions |\n\n## Addon
Validation\n\nAddons are validated at multiple stages:\n\n### Build-Time Validation\n\n##
Check all
addon.yaml files for schema compliance\n\n debvisor validate-addons\n\n## Output\n\n## ?
compose/traefik: Valid\n\n## ? k8s/monitoring: Valid\n\n## ? k8s/ingress: Valid\n\n## ?
k8s/custom-addon: Missing required field 'metadata.description'\n\n## Install-Time
Validation\n\n##
Validate that selected addons don't conflict\n\n debvisor validate-selection [addon1]
[addon2]
[addon3]\n\n## Output [2]\n\n## ? All addons compatible\n\n## OR\n\n## ? Conflict
detected:
prometheus-monitoring and datadog-monitoring\n\n## Deployment-Time Validation\n\n## Verify
prerequisites before deploying\n\n debvisor deploy-addon [addon-name] --dry-run\n\n##
Output
[3]\n\n## Checking prerequisites for [addon-name]\n\n## ? Required addon 'kubernetes-core'
is
enabled\n\n## ? Required addon 'networking' is enabled\n\n## ? Insufficient disk space:
required
10Gi, available 5Gi\n\n## Common Addon Patterns\n\n### Docker Compose Addon Pattern\n\n
compose/my-service/\n +-- addon.yaml\n +-- my-service-compose.yml\n +-- config/\n | +--
app.conf\n |
+-- secrets.env\n +-- README.md\n\n### Deployment\n\n docker compose -f
compose/my-service/my-service-compose.yml up -d\n\n### Kubernetes Addon Pattern\n\n
k8s/my-addon/\n
+-- addon.yaml\n +-- namespace.yaml # Create namespace\n +-- deployment.yaml # Deployment
manifest\n
+-- service.yaml # Service manifest\n +-- configmap.yaml # Configuration\n +-- secret.yaml

## Secrets

(template)\n +-- pvc.yaml # PersistentVolumeClaim (if needed)\n +-- README.md\n\n###
Deployment
[2]\n\n kubectl apply -f k8s/my-addon/\n\n## Selective Addon Deployment\n\nBuild images
with
specific addon subsets:\n\n## Build with only monitoring addons\n\n debvisor build
--addons
k8s/monitoring,k8s/logging\n\n## Build with Kubernetes addons only\n\n debvisor build
--addon-filter
k8s\n\n## Build with all addons\n\n debvisor build --addons all\n\n## Managing Addon
Configuration\n\n### Configuration Files\n\nEach addon may include configuration:\n
compose/traefik/\n +-- addon.yaml\n +-- traefik-compose.yml\n +-- config/\n +--
traefik.toml # Main
config\n +-- dynamic.toml # Dynamic routing\n +-- secrets.env.example # Template for
secrets\n\n###
Customization\n\n1. Copy example config files\n\n1. Edit for your environment\n\n1. Mount
or inject
into deployed containers/pods\n\n1. Document any non-standard settings in
comments\n\nExample:\n cp
compose/traefik/config/secrets.env.example compose/traefik/config/secrets.env\n\n## Edit
secrets.env
with your values\n\n docker compose -f compose/traefik/traefik-compose.yml --env-file
compose/traefik/config/secrets.env up -d\n\n## Addon Dependencies and Ordering\n\n###
Dependency
Resolution\n\nWhen deploying multiple addons, dependencies are resolved in order:\n
prometheus-monitoring\n +-- depends on -> kubernetes-core\n +-- depends on -> networking\n
+--
depends on -> node-exporter\n node-exporter\n +-- depends on -> kubernetes-core\n +--
depends on ->
networking\n kubernetes-core (no dependencies)\n networking (no dependencies)\n\n-
*Deployment
order:**kubernetes-core -> networking -> node-exporter -> prometheus-monitoring\n\n###
Circular
Dependency Detection\n\nValidation fails if circular dependencies are detected:\n addon-a
depends on
addon-b\n addon-b depends on addon-a\n v\n ERROR: Circular dependency detected\n\n## Addon
Integration with DebVisor Components\n\n### Monitoring Integration\n\n- Addons
in`k8s/monitoring/`inherit DebVisor Prometheus label conventions\n\n- Export metrics
following`debvisor**`namespace\n\n- Register with existing Grafana dashboards via label
matching\n\n### Networking Integration\n\n- Addons requiring network access should use
DebVisor
bridge or Calico networks\n\n- DNS integration: register addon services in DebVisor
DNS\n\n- Load
balancing: use existing HAProxy or Kubernetes ingress\n\n### Storage Integration\n\n-
Addons
requiring persistent storage use DebVisor storage backends:\n\n- Ceph RBD for block
storage\n\n-
CephFS for shared filesystems\n\n- ZFS LocalPV for node-local storage\n\n- StorageClass
examples:`ceph-rbd`,`ceph-cephfs`,`zfs-local`\n\n## Troubleshooting Addons\n\n### Addon
Deployment
Failed\n\n1. Check prerequisite addons are enabled\n\n1. Verify resource
availability\n\n1. Review
addon healthcheck logs\n\n1. Check for conflicting addons\n\n### Addon Cannot Be
Removed\n\n1.
Identify dependent services/pods\n\n1. Migrate workloads to alternative addon or
backend\n\n1.
Remove dependent addons first\n\n1. Then remove the addon\n\n### Addon Conflicts with Core
Services\n\n- Check `spec.conflicts`field in addon.yaml\n\n- Consider alternative addon or
run on
dedicated nodes\n\n- File issue if conflict is unresolvable\n\n## Best
Practices\n\n1.**Always
validate**: Run dry-run before deploying to production\n1.**Test dependencies**: Verify
addon works
with your core version\n1.**Monitor resources**: Watch CPU, memory, disk usage after
deployment\n1.**Document customizations**: Keep notes of configuration changes\n1.**Plan
removal**:
Know how to cleanly remove addons before deploying\n1.**Version tracking**: Maintain addon
versions
and upgrade procedures\n1.**Backup data**: Backup persistent data before addon upgrades or
removals\n\n## Contributing New Addons\n\nTo contribute a new addon:\n\n1. Create addon
directory
under`compose/`or`k8s/`\n\n1. Create `addon.yaml`with complete metadata\n\n1. Add
deployment
manifests (compose YAML or Kubernetes manifests)\n\n1. Create`README.md`with usage
instructions\n\n1. Include validation and health check scripts\n\n1. Add configuration
examples and
templates\n\n1. Test deployment and removal procedures\n\n1. Submit pull request with
documentation\n\n## Support\n\n- **Documentation**: See individual
addon`README.md`files\n\n-
**Troubleshooting**: Check`opt/docs/troubleshooting.md`\n\n- **Issue Tracking**: File
issues in the
main DebVisor repository\n\n- **Contributing**: See `CONTRIBUTING.md` for guidelines\n\n-
--\n\n-
*Last Updated**: 2025-11-26\n\n- *Addon Format Version**: v1alpha1\n\n
