# DebVisor Addons Architecture

This directory contains optional addon components that extend DebVisor cluster functionality. Addons are organized by deployment mechanism: Docker Compose for standalone services and Kubernetes manifests for cluster-wide deployments.

## Addon Architecture Overview

### What is an addon

An addon is a self-contained, optional component that:

- Provides specialized functionality (monitoring, ingress, storage, security)
- Can be independently enabled or disabled
- Declares dependencies on other addons or core DebVisor services
- Includes deployment manifests and configuration templates
- Is documented with usage and troubleshooting guidance

### Addon Discovery

Addons are discovered at build time and install time:

1.__Build Time__: `sync-addons-playbook.sh` scans this directory for addon manifests
1.__Install Time__: `debvisor-firstboot.sh` evaluates profile selections
1.__Runtime__: Operators enable addons via CLI or web panel

Each addon is uniquely identified by its directory name (e.g., `prometheus-monitoring`,`traefik`,`ceph-csi-rbd`).

### Addon Types

| Type | Location | Mechanism | Use Case |
|------|----------|-----------|----------|
|__Docker Compose__| `compose/` | Docker daemon | Standalone container stacks on DebVisor nodes |
|__Kubernetes__| `k8s/` | kubectl apply | Cluster-wide services and controllers |

### Addon Lifecycle

    Discovery (build/firstboot)
        v
    Dependency Check (validate prerequisites)
        v
    Metadata Validation (addon.yaml schema)
        v
    User Selection (profile, CLI, or web panel)
        v
    Deployment (docker-compose or kubectl apply)
        v
    Verification (health checks, readiness probes)
        v
    Rollback (if deployment fails, revert to previous state)

## Directory Structure

    addons/
    +-- README.md                 # This file
    +-- compose/                  # Docker Compose addons
    |   +-- README.md
    |   +-- traefik/
    |   |   +-- addon.yaml       # Metadata (name, dependencies, resources)
    |   |   +-- traefik-compose.yml
    |   +-- gitlab-runner/
    |       +-- addon.yaml
    |       +-- gitlab-runner-compose.yml
    +-- k8s/                      # Kubernetes addons
        +-- README.md
        +-- monitoring/
        |   +-- addon.yaml
        |   +-- prometheus.yaml
        |   +-- grafana.yaml
        |   +-- ...
        +-- ingress/
        |   +-- addon.yaml
        |   +-- nginx-ingress.yaml
        +-- storage/
        |   +-- addon.yaml
        |   +-- ceph-csi-rbd.yaml
        |   +-- ceph-csi-cephfs.yaml
        |   +-- zfs-localpv.yaml
        +-- csi/
        +-- security/
        +-- ...

## Addon Metadata Format (`addon.yaml`)

Each addon includes an `addon.yaml` manifest describing its properties:

    apiVersion: debvisor.io/v1alpha1
    kind: Addon
    metadata:
      name: prometheus-monitoring
      description: Prometheus + Grafana monitoring stack for Kubernetes
      category: monitoring
      version: "1.0.0"

    spec:

## Deployment mechanism

      type: kubernetes  # or "compose"

## Resource requirements

      resources:
        cpu: "500m"
        memory: "1Gi"
        disk: "10Gi"  # Persistent volume size

## Platform/architecture support

      supported_architectures:

- amd64
- arm64

## Dependencies on other addons

      dependencies:

- addon: kubernetes-core  # Required addon

          version: ">=1.25.0"

- addon: networking       # Required addon

## Conflicting addons (cannot be enabled together)

      conflicts:

- addon: other-monitoring-stack

## Lifecycle hooks

      hooks:
        pre_deploy:  # Run before deployment

- script: validate-prereqs.sh

        post_deploy:  # Run after deployment

- script: configure-monitoring.sh

        pre_remove:  # Run before removal

- script: backup-data.sh

## Health checks

      healthcheck:
        type: http
        endpoint: "[http://localhost:9090/-/healthy"](http://localhost:9090/-/healthy")
        interval: 30s
        timeout: 5s

## Configuration schema (for validation)

      config:
        properties:
          prometheus_retention_days:
            type: integer
            default: 30
            description: "Prometheus data retention period (days)"
          grafana_admin_password:
            type: string
            description: "Initial Grafana admin password"
          enable_alerting:
            type: boolean
            default: true

## Installation instructions

      install:
        instructions: |

          1. Ensure Kubernetes cluster is ready: `kubectl get nodes`
          1. Create monitoring namespace: `kubectl create namespace monitoring`
          1. Deploy addon: `kubectl apply -f monitoring/`
          1. Verify: `kubectl get pods -n monitoring`

## Removal instructions

      remove:
        instructions: |

          1. Backup Prometheus data: `kubectl exec -it prometheus-0 -- tar czf /tmp/backup.tgz /prometheus`
          1. Remove addon: `kubectl delete -f monitoring/`
          1. Clean up volumes: `kubectl delete pvc --all -n monitoring`

## Post-install validation

      validation:
        checks:

- name: "Prometheus running"

            command: "kubectl get deployment prometheus -n monitoring"

- name: "Grafana accessible"

            command: "curl -f [http://localhost:3000](http://localhost:3000) || exit 1"

### Addon Metadata Schema Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `metadata.name` | Yes | string | Unique addon identifier (alphanumeric + dash) |
| `metadata.description` | Yes | string | Human-readable description |
| `metadata.category` | Yes | string | Category: monitoring, ingress, storage, security, networking, other |
| `metadata.version` | Yes | string | Addon version (semver) |
| `spec.type`| Yes | enum | Deployment type:`kubernetes`or`compose` |
| `spec.resources.cpu` | Yes | string | CPU reservation (k8s format, e.g., "500m", "1") |
| `spec.resources.memory` | Yes | string | Memory reservation (k8s format, e.g., "512Mi", "1Gi") |
| `spec.resources.disk` | No | string | Persistent storage requirement |
| `spec.supported_architectures` | Yes | list | Architectures: amd64, arm64, ppc64le, s390x |
| `spec.dependencies` | No | list | Required addons (name + optional version) |
| `spec.conflicts` | No | list | Conflicting addons (cannot be enabled together) |
| `spec.hooks.pre_deploy` | No | list | Scripts to run before deployment |
| `spec.hooks.post_deploy` | No | list | Scripts to run after deployment |
| `spec.healthcheck.type` | No | enum | Health check type: http, tcp, exec, kubernetes |
| `spec.install.instructions` | Yes | string | Installation instructions |
| `spec.remove.instructions` | Yes | string | Removal instructions |

## Addon Validation

Addons are validated at multiple stages:

### Build-Time Validation

## Check all addon.yaml files for schema compliance

    debvisor validate-addons

## Output

## ? compose/traefik: Valid

## ? k8s/monitoring: Valid

## ? k8s/ingress: Valid

## ? k8s/custom-addon: Missing required field 'metadata.description'

## Install-Time Validation

## Validate that selected addons don't conflict

    debvisor validate-selection [addon1] [addon2] [addon3]

## Output [2]

## ? All addons compatible

## OR

## ? Conflict detected: prometheus-monitoring and datadog-monitoring

## Deployment-Time Validation

## Verify prerequisites before deploying

    debvisor deploy-addon [addon-name] --dry-run

## Output [3]

## Checking prerequisites for [addon-name]

## ? Required addon 'kubernetes-core' is enabled

## ? Required addon 'networking' is enabled

## ? Insufficient disk space: required 10Gi, available 5Gi

## Common Addon Patterns

### Docker Compose Addon Pattern

    compose/my-service/
    +-- addon.yaml
    +-- my-service-compose.yml
    +-- config/
    |   +-- app.conf
    |   +-- secrets.env
    +-- README.md

### Deployment

    docker compose -f compose/my-service/my-service-compose.yml up -d

### Kubernetes Addon Pattern

    k8s/my-addon/
    +-- addon.yaml
    +-- namespace.yaml          # Create namespace
    +-- deployment.yaml         # Deployment manifest
    +-- service.yaml           # Service manifest
    +-- configmap.yaml         # Configuration
    +-- secret.yaml            # Secrets (template)
    +-- pvc.yaml               # PersistentVolumeClaim (if needed)
    +-- README.md

### Deployment [2]

    kubectl apply -f k8s/my-addon/

## Selective Addon Deployment

Build images with specific addon subsets:

## Build with only monitoring addons

    debvisor build --addons k8s/monitoring,k8s/logging

## Build with Kubernetes addons only

    debvisor build --addon-filter k8s

## Build with all addons

    debvisor build --addons all

## Managing Addon Configuration

### Configuration Files

Each addon may include configuration:

    compose/traefik/
    +-- addon.yaml
    +-- traefik-compose.yml
    +-- config/
        +-- traefik.toml         # Main config
        +-- dynamic.toml         # Dynamic routing
        +-- secrets.env.example  # Template for secrets

### Customization

1. Copy example config files
1. Edit for your environment
1. Mount or inject into deployed containers/pods
1. Document any non-standard settings in comments

Example:

    cp compose/traefik/config/secrets.env.example compose/traefik/config/secrets.env

## Edit secrets.env with your values

    docker compose -f compose/traefik/traefik-compose.yml --env-file compose/traefik/config/secrets.env up -d

## Addon Dependencies and Ordering

### Dependency Resolution

When deploying multiple addons, dependencies are resolved in order:

    prometheus-monitoring
    +-- depends on -> kubernetes-core
    +-- depends on -> networking
    +-- depends on -> node-exporter

    node-exporter
    +-- depends on -> kubernetes-core
    +-- depends on -> networking

    kubernetes-core (no dependencies)

    networking (no dependencies)

__Deployment order:__kubernetes-core -> networking -> node-exporter -> prometheus-monitoring

### Circular Dependency Detection

Validation fails if circular dependencies are detected:

    addon-a depends on addon-b
    addon-b depends on addon-a
    v
    ERROR: Circular dependency detected

## Addon Integration with DebVisor Components

### Monitoring Integration

- Addons in `k8s/monitoring/` inherit DebVisor Prometheus label conventions
- Export metrics following `debvisor_*` namespace
- Register with existing Grafana dashboards via label matching

### Networking Integration

- Addons requiring network access should use DebVisor bridge or Calico networks
- DNS integration: register addon services in DebVisor DNS
- Load balancing: use existing HAProxy or Kubernetes ingress

### Storage Integration

- Addons requiring persistent storage use DebVisor storage backends:
- Ceph RBD for block storage
- CephFS for shared filesystems
- ZFS LocalPV for node-local storage
- StorageClass examples: `ceph-rbd`,`ceph-cephfs`,`zfs-local`

## Troubleshooting Addons

### Addon Deployment Failed

1. Check prerequisite addons are enabled
1. Verify resource availability
1. Review addon healthcheck logs
1. Check for conflicting addons

### Addon Cannot Be Removed

1. Identify dependent services/pods
1. Migrate workloads to alternative addon or backend
1. Remove dependent addons first
1. Then remove the addon

### Addon Conflicts with Core Services

- Check `spec.conflicts` field in addon.yaml
- Consider alternative addon or run on dedicated nodes
- File issue if conflict is unresolvable

## Best Practices

1.__Always validate__: Run dry-run before deploying to production
1.__Test dependencies__: Verify addon works with your core version
1.__Monitor resources__: Watch CPU, memory, disk usage after deployment
1.__Document customizations__: Keep notes of configuration changes
1.__Plan removal__: Know how to cleanly remove addons before deploying
1.__Version tracking__: Maintain addon versions and upgrade procedures
1.__Backup data__: Backup persistent data before addon upgrades or removals

## Contributing New Addons

To contribute a new addon:

1. Create addon directory under `compose/`or`k8s/`
1. Create `addon.yaml` with complete metadata
1. Add deployment manifests (compose YAML or Kubernetes manifests)
1. Create `README.md` with usage instructions
1. Include validation and health check scripts
1. Add configuration examples and templates
1. Test deployment and removal procedures
1. Submit pull request with documentation

## Support

-__Documentation__: See individual addon `README.md` files
-__Troubleshooting__: Check `opt/docs/troubleshooting.md`
-__Issue Tracking__: File issues in the main DebVisor repository
-__Contributing__: See `CONTRIBUTING.md` for guidelines

---

__Last Updated__: 2025-11-26

__Addon Format Version__: v1alpha1
