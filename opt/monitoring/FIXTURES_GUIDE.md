# DebVisor Monitoring Fixtures - Comprehensive Guide

This directory contains optional synthetic metrics fixtures for testing DebVisor monitoring, dashboards, and alerting in non-production or demo environments.

## What Are Fixtures

Fixtures are synthetic (generated) metrics data that simulate realistic workload patterns without requiring actual workloads. They're useful for:

-__Dashboard Development__: Test dashboard panels without live clusters
-__Alert Tuning__: Validate alert thresholds and notification channels
-__Training__: Demonstrate monitoring capabilities to operators
-__CI/CD Testing__: Validate monitoring pipelines in test environments
-__Demo/PoC Environments__: Create convincing demos without real infrastructure

## Important Caveat

⚠️__Production Warning:__Synthetic fixtures are NEVER appropriate for production environments. They mask real signals and can hide actual problems. Use only in:

- Lab environments
- Testing/QA clusters
- Development setups
- Demos and POCs
- Training environments

## Fixture Types

### Type 1: ConfigMap-Based Fixtures

Simple Kubernetes ConfigMaps containing metric definitions.

__Files:__`edge-lab.yaml`, etc.

### Characteristics

- No deployment; passive data
- Can be consumed by Prometheus `static_configs`
- Good for small test scenarios
- Minimal resource overhead

### Usage

    kubectl apply -f monitoring/fixtures/edge-lab.yaml

### Type 2: Generator-Based Fixtures

Active generator Deployments that produce synthetic metrics.

__Files:__`edge-lab-deployment.yaml`, etc.

### Characteristics [2]

- Active Pods generating metrics
- Exposed via Service with `/metrics` endpoint
- Prometheus can scrape directly
- Configurable via environment variables
- More realistic time-series generation

### Usage [2]

    kubectl apply -f monitoring/fixtures/edge-lab-deployment.yaml

## Prometheus scrapes: [http://synthetic-metrics:8080/metrics](http://synthetic-metrics:8080/metrics)

## Environment Classifications

### Lab Environment

__When:__Local development, learning, small test clusters

### Characteristics [3]

- Single-node or 2-3 node clusters
- Minimal real workloads
- Fast iteration and testing
- No SLA requirements

__Fixture:__`edge-lab.yaml`,`edge-lab-deployment.yaml`

### Metrics Included

- Node CPU/memory/disk (realistic single-node profile)
- Network I/O (low traffic patterns)
- Container metrics (few running containers)
- Ceph metrics (if enabled, minimal pool)
- Kubernetes API latency

### Testing/QA Environment

__When:__CI/CD pipelines, automated testing, staging

### Characteristics [4]

- 3-5 node test clusters
- Mixed workloads (some containers, some VMs)
- Realistic but compressed time scales
- Alert testing and validation

__Fixture:__Create custom fixture or use parametrized generator

### Typical Metrics

- Multi-node host metrics with variance
- Various pod states (running, pending, failed)
- Storage pool operations (snapshots, writes)
- API request patterns

### Demo/PoC Environment

__When:__Customer demos, sales POCs, training

### Characteristics [5]

- Simulated production-like cluster
- Realistic metric shapes and thresholds
- Time-shifted data (compress hours into minutes)
- Convincing visualizations

__Fixture:__Deploy dedicated generator with realistic patterns

### Key Metrics

- Multi-hour dashboard history (compressed to 10-15 min demo)
- Alert firing and resolution patterns
- Anomalies and incident scenarios
- Remediation impact visualization

## Generator Implementation

### Location

`monitoring/fixtures/generator/` - Python Prometheus client-based generator

### Components

    generator/
    ├── Dockerfile                  # Build synthetic metrics image
    ├── requirements.txt           # Python dependencies
    ├── app.py                     # Generator application
    └── metrics/
        ├──__init__.py
        ├── node_metrics.py        # Host-level metrics
        ├── container_metrics.py   # Pod/container metrics
        ├── storage_metrics.py     # Ceph/ZFS metrics
        ├── network_metrics.py     # Network I/O metrics
        └── patterns.py            # Realistic time-series patterns

### Building

### Local Build

    cd monitoring/fixtures/generator
    docker build -t debvisor/synthetic-metrics:local .

### With Custom Repository

    docker build -t your-registry/synthetic-metrics:v1.0 .
    docker push your-registry/synthetic-metrics:v1.0

### Multi-Architecture Build (with buildx)

    docker buildx build --platform linux/amd64,linux/arm64 \
      -t your-registry/synthetic-metrics:latest \
      --push monitoring/fixtures/generator

### Environment Variables

Configure generator behavior via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `METRICS_PORT`|`8080`| Port to expose`/metrics` on |
| `UPDATE_INTERVAL`|`5` | Seconds between metric updates |
| `SCENARIO`|`lab` | Scenario: lab, testing, demo |
| `COMPRESSION_FACTOR`|`1` | Time compression (>1 for compressed time) |
| `NODE_COUNT`|`3` | Number of simulated nodes |
| `POD_COUNT`|`50` | Number of simulated pods |
| `POOL_COUNT`|`2` | Number of simulated storage pools |
| `ERROR_RATE`|`0.01` | Synthetic error rate (0.0-1.0) |
| `ALERT_SCENARIO`|`none` | Trigger alert: none, high_cpu, disk_full, mem_pressure |

### Example with Parameters

    docker run -e SCENARIO=demo -e COMPRESSION_FACTOR=10 \
      -e ALERT_SCENARIO=high_cpu -p 8080:8080 \
      debvisor/synthetic-metrics:local

## Metric Categories

### 1. Node/Host Metrics

### Metrics

- `node_cpu_seconds_total` - CPU time per CPU
- `node_memory_MemTotal_bytes` - Total memory
- `node_memory_MemAvailable_bytes` - Available memory
- `node_disk_read_bytes_total` - Disk read I/O
- `node_disk_write_bytes_total` - Disk write I/O
- `node_network_receive_bytes_total` - Network received
- `node_network_transmit_bytes_total` - Network transmitted
- `node_filesystem_avail_bytes` - Filesystem space available

### Generated Patterns

- CPU: Realistic multi-core utilization with periodic spikes
- Memory: Gradual increase with periodic drops (GC events)
- Disk: Steady writes with occasional bursts
- Network: Bursty traffic patterns

### 2. Container/Pod Metrics (cAdvisor)

### Metrics [2]

- `container_cpu_usage_seconds_total` - CPU per container
- `container_memory_usage_bytes` - Memory per container
- `container_network_receive_bytes_total` - Per-container network in
- `container_network_transmit_bytes_total` - Per-container network out
- `container_last_seen` - Container alive/dead indicator

### Pod Distribution

- Running: 70-80% of pods
- Pending: 5-10% of pods
- Failed/CrashLoop: 1-5% of pods (variable based on scenario)

### 3. Storage Metrics (Ceph)

### Metrics [3]

- `ceph_cluster_used_bytes` - Used storage
- `ceph_cluster_capacity_bytes` - Total capacity
- `ceph_osd_up` - OSD online/offline
- `ceph_pg_active` - Placement group status
- `ceph_pool_objects_total` - Objects in pool
- `ceph_pool_used_bytes` - Pool usage

### Scenarios

- Lab: 1-2 objects, minimal usage
- Testing: 100-1000 objects, realistic usage
- Demo: Complex pool dynamics, rebalancing events

### 4. Kubernetes Metrics

### Metrics [4]

- `kube_node_status_condition` - Node ready/not ready
- `kube_pod_status_phase` - Pod phase (Running, Pending, Failed)
- `kube_pod_container_status_restarts_total` - Pod restarts
- `kube_deployment_status_replicas` - Deployment replicas
- `apiserver_request_duration_seconds` - API latency

### Patterns

- Node status: Occasional "NotReady" events (auto-recovery)
- Pod restarts: Realistic restart patterns
- API latency: Variable with occasional spikes

### 5. Custom DebVisor Metrics

### Metrics [5]

- `debvisor_cluster_health` - Cluster health score (0-100)
- `debvisor_remediation_total` - Security remediations performed
- `debvisor_vm_migrations_total` - VM migrations
- `debvisor_alert_firing_total` - Active alerts

## Usage Scenarios

### Scenario 1: Dashboard Testing (Lab)

## Apply lab fixture

    kubectl apply -f monitoring/fixtures/edge-lab.yaml

## Prometheus scrapes ConfigMap data

## Grafana renders dashboards with synthetic data

## Remove when done

    kubectl delete -f monitoring/fixtures/edge-lab.yaml

__Duration:__Few minutes of testing
__Cleanup:__Manual removal

## Scenario 2: Alert Validation (Testing)

## Deploy parametrized generator

    kubectl apply -f monitoring/fixtures/edge-lab-deployment.yaml

## Manually trigger alert scenario

    kubectl set env deployment/synthetic-metrics \
      ALERT_SCENARIO=high_cpu -n monitoring

## Monitor alert firing via Prometheus/Grafana

## Alert should fire within 1-2 minutes

## Verify notification channels receive alert

## Cleanup

    kubectl delete -f monitoring/fixtures/edge-lab-deployment.yaml

__Duration:__5-15 minutes
__Metrics:__Realistic patterns with configurable anomalies

## Scenario 3: Time-Compressed Demo (POC)

## Deploy demo generator with 10x time compression

    kubectl apply -f monitoring/fixtures/edge-lab-deployment.yaml
    kubectl set env deployment/synthetic-metrics \
      SCENARIO=demo COMPRESSION_FACTOR=10 -n monitoring

## Demo shows 10 hours of metrics in ~1 hour

## Dashboards show full day cycle, anomalies, recovery

## Perfect for 1-hour sales demos

## Cleanup after demo

    kubectl delete -f monitoring/fixtures/edge-lab-deployment.yaml

__Duration:__45-60 minutes demo
__Metrics:__Compressed time-series with realistic patterns

## Best Practices

### ✅ DO

- Use fixtures in__non-production environments only__

-__Label fixtures clearly__(e.g., `fixture: "true"`,`scenario: lab`)
-__Auto-cleanup__: Use Kubernetes Job or timer to remove fixtures
-__Document intent__: Comment why fixtures are applied, when to remove them
-__Compress time__for demos: Use `COMPRESSION_FACTOR` > 1 for speed
-__Test alert thresholds__before moving to production
-__Preserve fixture definitions__: Keep generator code in version control

### ❌ DON'T

-__Never apply to production__- Synthetic data masks real problems
-__Don't rely on fixture data__for capacity planning or billing
-__Don't forget cleanup__- Fixtures left running waste resources
-__Don't modify thresholds__based solely on fixture behavior
-__Don't publish fixture images__without version tags
-__Don't hardcode fixture data__in dashboards or alerts

## Cleanup [2]

### Manual Cleanup

## Remove generator deployment

    kubectl delete -f monitoring/fixtures/edge-lab-deployment.yaml

## Remove ConfigMap fixture

    kubectl delete -f monitoring/fixtures/edge-lab.yaml

## Automated Cleanup

Create a timer or CronJob for automatic fixture cleanup:

    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: fixture-cleanup
      namespace: monitoring
    spec:
      schedule: "0 22 * * *"  # 10 PM daily
      jobTemplate:
        spec:
          template:
            spec:
              serviceAccountName: fixture-cleanup
              containers:

- name: cleanup

                image: bitnami/kubectl:latest
                command:

- /bin/sh
- -c
- |

                  kubectl delete deployment -l fixture=true -n monitoring
                  kubectl delete configmap -l fixture=true -n monitoring
              restartPolicy: OnFailure

### Time-Based Cleanup

Use labels with expiry logic:

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: edge-lab-fixture
      namespace: monitoring
      labels:
        fixture: "true"
        fixture-expiry: "2025-11-27T22:00:00Z"  # Expires tomorrow 10 PM
    data:
      cleanup-instructions: |
        This fixture expires at 2025-11-27T22:00:00Z
        Check back daily for auto-cleanup

## Troubleshooting

### Generator Not Producing Metrics

1. Check pod status: `kubectl get pods -n monitoring -l app=synthetic-metrics`
1. Check logs: `kubectl logs -f deployment/synthetic-metrics -n monitoring`
1. Verify endpoint: `kubectl port-forward svc/synthetic-metrics 8080:8080`
1. Test endpoint: `curl [http://localhost:8080/metrics](http://localhost:8080/metrics)

### Prometheus Not Scraping

1. Verify ServiceMonitor or scrape config exists
1. Check Prometheus targets: [http://prometheus:9090/targets](http://prometheus:9090/targets)
1. Look for scrape errors in Prometheus logs

### Dashboards Showing No Data

1. Confirm metrics are arriving: [http://prometheus:9090/graph](http://prometheus:9090/graph)
1. Check query syntax in dashboard JSON
1. Verify metric names match generator output

### Alert Not Triggering

1. Confirm metric value exceeds threshold
1. Check Prometheus rule evaluation: [http://prometheus:9090/rules](http://prometheus:9090/rules)
1. Verify Alertmanager is running: `kubectl get pods -n monitoring`
1. Check notification channel configuration

## Reference

### Files in this directory

- `README.md` - Quick start guide
- `FIXTURES_GUIDE.md` - This detailed guide
- `edge-lab.yaml` - Lab environment fixture (ConfigMap)
- `edge-lab-deployment.yaml` - Lab environment generator (Deployment)
- `generator/` - Source code for synthetic metrics generator
- `kustomize/` - Kustomize overlays for environment-specific customization

## Contributing

To add new fixtures or scenarios:

1. Create new fixture YAML in this directory
1. Document intended use and metric types
1. Add scenario to `generator/metrics/patterns.py`
1. Test locally before committing
1. Update this guide with scenario description

---

__Last Updated:__2025-11-26

__Classification:__Development/Testing/Demo Only - NOT FOR PRODUCTION
