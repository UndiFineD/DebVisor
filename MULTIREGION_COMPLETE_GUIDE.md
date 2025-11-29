# Multi-region Support Complete Guide

## Table of Contents

1. [Overview](#overview)
1. [Architecture](#architecture)
1. [Features](#features)
1. [Quick Start](#quick-start)
1. [Region Management](#region-management)
1. [Replication](#replication)
1. [Failover](#failover)
1. [CLI Reference](#cli-reference)
1. [REST API Reference](#rest-api-reference)
1. [Python API Guide](#python-api-guide)
1. [Configuration](#configuration)
1. [Monitoring](#monitoring)
1. [Troubleshooting](#troubleshooting)
1. [Performance Tuning](#performance-tuning)

---

## Overview

The DebVisor Multi-region Support system enables seamless geo-distributed operations across multiple datacenters with automatic failover, data replication, and comprehensive region management.

### Use Cases

- **Disaster Recovery**: Maintain standby regions for rapid failover
- **Geographic Distribution**: Place workloads closer to users
- **Data Compliance**: Replicate data to compliant regions
- **Load Balancing**: Distribute VMs across regions
- **High Availability**: Eliminate single points of failure

### Key Capabilities

- **Multi-datacenter Replication**: Automatic sync of VMs, storage, and config
- **Automatic Failover**: Detect failures and promote standby regions
- **Health Monitoring**: Real-time region status and latency tracking
- **Dependency Tracking**: Complex replication relationships
- **History & Audit**: Full logging of all operations
- **REST & CLI Access**: Multiple interfaces for integration

---

## Architecture

### Component Model

```python
+---------------------------------------------------------+
|         DebVisor Multi-region System                     |
+---------------------------------------------------------+
|                                                           |
|  +--------------------------------------------------+   |
|  |        MultiRegionManager (Core)                 |   |
|  |  - Region registration & health checks           |   |
|  |  - Replication orchestration                     |   |
|  |  - Failover coordination                         |   |
|  |  - Statistics & monitoring                       |   |
|  +--------------------------------------------------+   |
|         |                    |                    |      |
|         ?                    ?                    ?      |
|    +---------+          +---------+          +----+    |
|    |   CLI   |          |  REST   |          |API |    |
|    | Interface|          |  API    |          |    |    |
|    +---------+          +---------+          +----+    |
|                                                           |
+---------------------------------------------------------+
         |                    |                    |
         +--------------------+--------------------+
                              |
         +--------------------+--------------------+
         |                    |                    |
         ?                    ?                    ?
    +-------------+      +-------------+     +----------+
    |  Region 1   |      |  Region 2   |     | Region N |
    | (Primary)   |      | (Standby)   |     |          |
    +-------------+      +-------------+     +----------+
```python

### Data Model

**Region**: Geographic location with API endpoint and capacity

- `region_id`: Unique identifier (e.g., "us-east-1")
- `name`: Human-readable name
- `location`: Geographic location
- `api_endpoint`: API URL for access
- `is_primary`: Primary or standby designation
- `status`: HEALTHY, DEGRADED, UNREACHABLE, RECOVERING
- `capacity_vms`: Maximum VM capacity
- `current_vms`: Currently hosted VMs
- `latency_ms`: Network latency to region
- `bandwidth_mbps`: Available bandwidth

**ReplicatedResource**: VM or resource tracked for replication

- `resource_id`: Resource identifier
- `resource_type`: VM, STORAGE, NETWORK, CONFIG, STATE
- `primary_region_id`: Primary region
- `replica_regions`: Dict of replica regions and IDs
- `replication_status`: Per-region sync status
- `version`: Resource version number
- `last_sync_time`: Last successful sync

**FailoverEvent**: Historical failover operation record

- `event_id`: Event identifier
- `timestamp`: When failover occurred
- `from_region_id`: Source region
- `to_region_id`: Target region
- `affected_resources`: Count of resources moved
- `success`: True if failover succeeded
- `duration_seconds`: Time taken

---

## Features

### Feature Matrix

| Feature | Capability | Status |
|---------|-----------|--------|
| Region Management | Register, list, monitor regions | ? Complete |
| Health Monitoring | Real-time health checks via ping | ? Complete |
| VM Replication | Multi-region VM replication | ? Complete |
| Config Replication | Application config sync | ? Complete |
| Automatic Failover | Detect failures and promote | ? Complete |
| Manual Failover | Operator-initiated failover | ? Complete |
| Dependency Resolution | Track resource dependencies | ? Complete |
| Statistics | Per-region and global metrics | ? Complete |
| History | Audit trail of all operations | ? Complete |
| REST API | 11 endpoints for HTTP access | ? Complete |
| CLI Interface | 13 commands for operations | ? Complete |
| Python SDK | Direct Python API | ? Complete |

---

## Quick Start

### 1. Initialize Manager (5 seconds)

```python
from opt.services.multiregion import MultiRegionManager

manager = MultiRegionManager()
```python

### 2. Register Regions (30 seconds)

```python

# Register primary region
primary = manager.register_region(
    name="US East 1",
    location="us-east-1",
    api_endpoint="https://api.us-east-1.internal",
    is_primary=True,
    capacity_vms=1000
)

# Register standby regions
west = manager.register_region(
    name="US West 1",
    location="us-west-1",
    api_endpoint="https://api.us-west-1.internal",
    capacity_vms=1000
)

eu = manager.register_region(
    name="EU West 1",
    location="eu-west-1",
    api_endpoint="https://api.eu-west-1.internal",
    capacity_vms=500
)
```python

### 3. Setup Replication (1 minute)

```python
from opt.services.multiregion import ResourceType

# Setup US replication
manager.setup_replication(
    source_region_id="us-east-1",
    target_region_id="us-west-1",
    resource_types=[ResourceType.VM, ResourceType.CONFIG],
    sync_interval_seconds=300,  # 5 minutes
    bidirectional=False
)

# Setup EU replication
manager.setup_replication(
    source_region_id="us-east-1",
    target_region_id="eu-west-1",
    resource_types=[ResourceType.VM, ResourceType.CONFIG, ResourceType.STATE],
    sync_interval_seconds=600  # 10 minutes for longer distance
)
```python

### 4. Register VMs for Replication (2 minutes)

```python

# Register web app VMs
for i in range(1, 6):
    manager.replicate_vm(
        vm_id=f"web-vm-{i}",
        primary_region_id="us-east-1",
        replica_regions=["us-west-1", "eu-west-1"]
    )

# Register database VMs
for i in range(1, 3):
    manager.replicate_vm(
        vm_id=f"db-vm-{i}",
        primary_region_id="us-east-1",
        replica_regions=["us-west-1"]  # Only close region
    )
```python

### 5. Monitor Status (ongoing)

```python
import asyncio

# Check region health
async def monitor():
    status = await manager.check_region_health("us-east-1")
    print(f"Primary region: {status}")

    status = await manager.check_region_health("us-west-1")
    print(f"West region: {status}")

asyncio.run(monitor())
```python

### 6. Perform Failover (if needed)

```python

# Automatic failover if primary fails
async def failover_if_needed():
    primary = manager.get_primary_region()

    # Check if primary is healthy
    status = await manager.check_region_health(primary.region_id)

    if status == RegionStatus.UNREACHABLE:
        # Failover to nearest healthy region
        backup = manager.get_region("us-west-1")
        success, event = await manager.perform_failover(
            from_region_id=primary.region_id,
            to_region_id=backup.region_id,
            reason="Primary region unreachable"
        )
        print(f"Failover: {event.event_id} - {'Success' if success else 'Failed'}")

asyncio.run(failover_if_needed())
```python

---

## Region Management

### Registering a Region

```python
region = manager.register_region(
    name="US Central 2",          # Display name
    location="us-central-2",      # Geographic location
    api_endpoint="https://api.us-central-2.internal",
    is_primary=False,             # Primary or standby
    capacity_vms=2000             # VM capacity
)

print(f"Registered {region.name} ({region.location})")
print(f"  Capacity: {region.capacity_vms} VMs")
print(f"  Primary: {region.is_primary}")
```python

### Listing Regions

```python

# All regions
all_regions = manager.list_regions()
print(f"Total regions: {len(all_regions)}")

# Only healthy regions
from opt.services.multiregion import RegionStatus
healthy = manager.list_regions(status=RegionStatus.HEALTHY)
print(f"Healthy regions: {len(healthy)}")
```python

### Getting Region Details

```python
region = manager.get_region("us-east-1")
print(f"Region: {region.name}")
print(f"  Status: {region.status}")
print(f"  Latency: {region.latency_ms}ms")
print(f"  Utilization: {region.current_vms}/{region.capacity_vms}")
```python

### Checking Region Health

```python

# Async health check
import asyncio

async def check():
    status = await manager.check_region_health("us-east-1")
    return status

status = asyncio.run(check())
print(f"Status: {status}")
```python

---

## Replication

### Setting Up Replication

```python

# Basic replication
config = manager.setup_replication(
    source_region_id="us-east-1",
    target_region_id="us-west-1",
    resource_types=[ResourceType.VM, ResourceType.CONFIG],
    sync_interval_seconds=300
)

# Bidirectional replication for sync pairs
config = manager.setup_replication(
    source_region_id="us-west-1",
    target_region_id="us-central-1",
    resource_types=[ResourceType.VM, ResourceType.STATE],
    sync_interval_seconds=60,
    bidirectional=True
)

# With compression for long distances
config = manager.setup_replication(
    source_region_id="us-east-1",
    target_region_id="ap-south-1",
    resource_types=[ResourceType.VM, ResourceType.STORAGE],
    sync_interval_seconds=600,
    compression=True
)
```python

### Registering VMs for Replication

```python

# Single VM
resource = manager.replicate_vm(
    vm_id="web-server-1",
    primary_region_id="us-east-1",
    replica_regions=["us-west-1", "eu-west-1"]
)

# Multiple VMs
vm_ids = ["web-1", "web-2", "web-3", "db-1", "cache-1"]
for vm_id in vm_ids:
    manager.replicate_vm(
        vm_id=vm_id,
        primary_region_id="us-east-1",
        replica_regions=["us-west-1"]
    )
```python

### Syncing Resources

```python
async def sync_all():
    # Get all resources
    for resource_id, resource in manager.resources.items():
        for target_region in resource.replica_regions:
            success = await manager.sync_resource(
                resource_id=resource_id,
                source_region_id=resource.primary_region_id,
                target_region_id=target_region
            )
            print(f"Sync {resource_id} -> {target_region}: {'?' if success else '?'}")

asyncio.run(sync_all())
```python

### Checking Replication Status

```python

# Get status for specific resource
status = manager.get_replication_status("web-server-1")
print(f"Resource: {status['resource_id']}")
print(f"  Primary: {status['primary_region']}")
print(f"  Version: {status['version']}")
print(f"  Last Sync: {status['last_sync']}")
print(f"  Replicas:")
for region, replica_info in status['replicas'].items():
    print(f"    {region}: {replica_info['status']}")
```python

---

## Failover

### Automatic Failover

```python
async def automatic_failover():
    primary = manager.get_primary_region()

    # Check if primary is healthy
    status = await manager.check_region_health(primary.region_id)

    if status == RegionStatus.UNREACHABLE:
        # Find healthiest backup
        backups = manager.list_regions(status=RegionStatus.HEALTHY)

        if backups:
            backup = backups[0]
            success, event = await manager.perform_failover(
                from_region_id=primary.region_id,
                to_region_id=backup.region_id,
                reason="Automatic failover - primary unavailable"
            )

            if success:
                print(f"? Failover completed: {event.event_id}")
                print(f"  Duration: {event.duration_seconds}s")
                print(f"  Resources: {event.affected_resources}")
            else:
                print(f"? Failover failed: {event.notes}")

asyncio.run(automatic_failover())
```python

### Manual Failover

```python
async def manual_failover():
    success, event = await manager.perform_failover(
        from_region_id="us-east-1",
        to_region_id="us-west-1",
        reason="Scheduled maintenance on primary"
    )

    if success:
        print(f"Failover {event.event_id}: SUCCESS")
    else:
        print(f"Failover {event.event_id}: FAILED - {event.notes}")

asyncio.run(manual_failover())
```python

### Failover History

```python

# Recent failovers
recent = manager.get_failover_history(limit=10)
for event in recent:
    print(f"[{event.timestamp}] {event.event_id}")
    print(f"  {event.from_region_id} -> {event.to_region_id}")
    print(f"  Status: {'? Success' if event.success else '? Failed'}")
    print(f"  Duration: {event.duration_seconds}s")
    print()

# Failovers for specific region
regional = manager.get_failover_history(region_id="us-east-1")
print(f"Failovers involving us-east-1: {len(regional)}")
```python

---

## CLI Reference

### Region Commands

#### Add Region

```bash
debvisor-region region add us-east-1 "US East 1" \
  https://api.us-east-1.internal \
  --primary \
  --capacity 2000
```python

#### List Regions

```bash

# All regions [2]
debvisor-region region list

# Only healthy regions [2]
debvisor-region region list --status healthy

# JSON format
debvisor-region region list --format json
```python

#### Show Region Details

```bash
debvisor-region region show us-east-1
debvisor-region region show us-east-1 --format json
```python

#### Check Region Health [2]

```bash
debvisor-region region health-check us-east-1
```python

#### Get Region Statistics

```bash
debvisor-region region stats us-east-1
```python

### Replication Commands

#### Setup Replication

```bash

# Basic replication [2]
debvisor-region replication setup us-east-1 us-west-1 vm,config

# With custom interval
debvisor-region replication setup us-east-1 eu-west-1 vm,config,state \
  --interval 600

# Bidirectional
debvisor-region replication setup us-west-1 us-central-1 vm \
  --bidirectional
```python

#### Check Replication Status

```bash
debvisor-region replication status vm-12345
```python

#### Sync Resource

```bash
debvisor-region replication sync vm-12345 us-east-1 us-west-1
```python

### VM Replication Commands

#### Register VM for Replication

```bash
debvisor-region vm replicate vm-web-1 us-east-1 us-west-1,eu-west-1
```python

### Failover Commands

#### Execute Failover

```bash

# Automatic failover [2]
debvisor-region failover execute us-east-1 us-west-1

# Manual with confirmation
debvisor-region failover execute us-east-1 us-west-1

# Force without confirmation
debvisor-region failover execute us-east-1 us-west-1 --force

# With reason
debvisor-region failover execute us-east-1 us-west-1 \
  --reason "Scheduled maintenance"
```python

#### View Failover History

```bash

# Recent failovers [2]
debvisor-region failover history

# For specific region
debvisor-region failover history --region us-east-1

# Show more
debvisor-region failover history --limit 50

# JSON format [2]
debvisor-region failover history --format json
```python

### Global Statistics

```bash
debvisor-region global
```python

---

## REST API Reference

### Base URL

```python
http://api.debvisor.local:5000/api/v1
```python

### Region Endpoints

#### Register Region

```python
POST /regions

{
  "name": "US East 1",
  "location": "us-east-1",
  "api_endpoint": "https://api.us-east-1.internal",
  "is_primary": true,
  "capacity_vms": 1000
}

Response: 201 Created
{
  "status": "success",
  "timestamp": "2025-11-27T12:34:56.789Z",
  "data": {
    "region_id": "us-east-1",
    "name": "US East 1",
    ...
  }
}
```python

#### List Regions [2]

```python
GET /regions?status=healthy

Response: 200 OK
{
  "status": "success",
  "timestamp": "2025-11-27T12:34:56.789Z",
  "data": [
    {
      "region_id": "us-east-1",
      "name": "US East 1",
      "status": "healthy",
      ...
    },
    ...
  ]
}
```python

#### Get Region Details

```python
GET /regions/us-east-1

Response: 200 OK
{
  "status": "success",
  "data": {
    "region_id": "us-east-1",
    "name": "US East 1",
    "status": "healthy",
    "latency_ms": 5.2,
    "capacity_vms": 1000,
    "current_vms": 850,
    ...
  }
}
```python

#### Check Region Health [3]

```python
POST /regions/us-east-1/health

Response: 200 OK
{
  "status": "success",
  "data": {
    "region_id": "us-east-1",
    "status": "healthy",
    "latency_ms": 5.2,
    "last_heartbeat": "2025-11-27T12:34:55.123Z"
  }
}
```python

#### Get Region Statistics [2]

```python
GET /regions/us-east-1/stats

Response: 200 OK
{
  "status": "success",
  "data": {
    "region_id": "us-east-1",
    "name": "US East 1",
    "status": "healthy",
    "utilization_percent": 85.0,
    "resources_primary": 45,
    "failover_events": 2,
    ...
  }
}
```python

### Replication Endpoints

#### Setup Replication [2]

```python
POST /replication/setup

{
  "source_region_id": "us-east-1",
  "target_region_id": "us-west-1",
  "resource_types": ["vm", "config"],
  "sync_interval_seconds": 300,
  "bidirectional": false
}

Response: 201 Created
```python

#### Sync Resource [2]

```python
POST /replication/sync

{
  "resource_id": "vm-12345",
  "source_region_id": "us-east-1",
  "target_region_id": "us-west-1"
}

Response: 200 OK
```python

#### Get Replication Status

```python
GET /replication/vm-12345/status

Response: 200 OK
{
  "status": "success",
  "data": {
    "resource_id": "vm-12345",
    "primary_region": "us-east-1",
    "replicas": {
      "us-west-1": {
        "status": "in_sync",
        "replica_id": "vm-12345-replica"
      }
    }
  }
}
```python

### Failover Endpoints

#### Execute Failover [2]

```python
POST /failover/execute

{
  "from_region_id": "us-east-1",
  "to_region_id": "us-west-1",
  "strategy": "automatic",
  "reason": "Primary region failure"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "event_id": "evt-abc123",
    "timestamp": "2025-11-27T12:34:56.789Z",
    "success": true,
    "duration_seconds": 45.3,
    "affected_resources": 125
  }
}
```python

#### Get Failover History

```python
GET /failover/history?region_id=us-east-1&limit=50

Response: 200 OK
{
  "status": "success",
  "data": [
    {
      "event_id": "evt-abc123",
      "timestamp": "2025-11-27T12:34:56.789Z",
      "from_region_id": "us-east-1",
      "to_region_id": "us-west-1",
      "success": true,
      ...
    },
    ...
  ]
}
```python

### VM Endpoints

#### Register VM for Replication [2]

```python
POST /vms/replicate

{
  "vm_id": "web-server-1",
  "primary_region_id": "us-east-1",
  "replica_regions": ["us-west-1", "eu-west-1"]
}

Response: 201 Created
```python

### Global Endpoints

#### Get Global Statistics

```python
GET /stats

Response: 200 OK
{
  "status": "success",
  "data": {
    "total_regions": 3,
    "healthy_regions": 3,
    "total_resources": 125,
    "utilization_percent": 82.5,
    "failover_events_total": 2,
    "failover_events_failed": 0
  }
}
```python

#### Health Check

```python
GET /health

Response: 200 OK
{
  "status": "success",
  "data": {
    "service": "multi-region",
    "status": "operational"
  }
}
```python

---

## Python API Guide

### Initialize Manager

```python
from opt.services.multiregion import MultiRegionManager

manager = MultiRegionManager(config_dir="/etc/debvisor/regions")
```python

### Region Management [2]

```python

# Register primary region [2]
primary = manager.register_region(
    name="US East 1",
    location="us-east-1",
    api_endpoint="https://api.us-east-1.internal",
    is_primary=True,
    capacity_vms=1000
)

# Get region
region = manager.get_region("us-east-1")

# List regions [3]
all_regions = manager.list_regions()
healthy = manager.list_regions(status=RegionStatus.HEALTHY)

# Get primary
primary = manager.get_primary_region()
```python

### Health Checking

```python
import asyncio

async def check_all_regions():
    regions = manager.list_regions()
    for region in regions:
        status = await manager.check_region_health(region.region_id)
        print(f"{region.name}: {status}")

asyncio.run(check_all_regions())
```python

### Replication Setup

```python

# Setup replication config
config = manager.setup_replication(
    source_region_id="us-east-1",
    target_region_id="us-west-1",
    resource_types=[ResourceType.VM, ResourceType.CONFIG],
    sync_interval_seconds=300
)

# Register VM for replication [3]
resource = manager.replicate_vm(
    vm_id="web-1",
    primary_region_id="us-east-1",
    replica_regions=["us-west-1"]
)

# Check replication status [2]
status = manager.get_replication_status("web-1")
```python

### Replication Sync

```python
async def sync_resources():
    for resource_id in manager.resources:
        success = await manager.sync_resource(
            resource_id=resource_id,
            source_region_id="us-east-1",
            target_region_id="us-west-1"
        )
        print(f"{resource_id}: {'?' if success else '?'}")

asyncio.run(sync_resources())
```python

### Failover Operations

```python
async def execute_failover():
    success, event = await manager.perform_failover(
        from_region_id="us-east-1",
        to_region_id="us-west-1",
        reason="Manual failover test"
    )

    if success:
        print(f"Failover completed: {event.event_id}")
    else:
        print(f"Failover failed: {event.notes}")

asyncio.run(execute_failover())
```python

### Monitoring

```python

# Get statistics
region_stats = manager.get_region_statistics("us-east-1")
global_stats = manager.get_global_statistics()

# Get failover history [2]
recent = manager.get_failover_history(limit=10)
for event in recent:
    print(f"Failover {event.event_id}: {event.from_region_id} -> {event.to_region_id}")
```python

---

## Configuration

### Region Configuration

```python
Region(
    region_id="us-east-1",           # Unique identifier
    name="US East 1",                # Display name
    location="us-east-1",            # Geographic location
    api_endpoint="https://...",      # API URL
    is_primary=True,                 # Primary/standby
    capacity_vms=1000,               # VM capacity
    latency_ms=0.0,                  # Network latency (calculated)
    bandwidth_mbps=0.0,              # Available bandwidth
    replication_lag_seconds=0.0      # Replication delay
)
```python

### Replication Configuration

```python
ReplicationConfig(
    source_region_id="us-east-1",
    target_region_id="us-west-1",
    resource_types=[ResourceType.VM],
    sync_interval_seconds=300,        # 5 minutes
    batch_size=100,                   # Items per sync
    priority=1,                       # Lower number = higher priority
    enabled=True,
    bidirectional=False,
    compression=True                  # Compress for bandwidth savings
)
```python

---

## Monitoring [2]

### Key Metrics

- **Replication Lag**: Time between primary update and replica sync
- **Failover Time**: Duration of failover operation
- **Resource Sync Rate**: Resources synced per minute
- **Region Latency**: Network latency to each region
- **VM Utilization**: VMs per region vs capacity
- **Failover Success Rate**: Successful failovers / total attempts

### Health Checks

```python
async def comprehensive_health():
    regions = manager.list_regions()

    for region in regions:
        status = await manager.check_region_health(region.region_id)

        print(f"{region.name}:")
        print(f"  Status: {status}")
        print(f"  Latency: {region.latency_ms}ms")
        print(f"  Utilization: {region.current_vms}/{region.capacity_vms}")
        print(f"  Replication Lag: {region.replication_lag_seconds}s")

asyncio.run(comprehensive_health())
```python

---

## Troubleshooting

### Region Unreachable

**Symptom**: `RegionStatus.UNREACHABLE`

**Diagnosis**:
```python
region = manager.get_region("us-east-1")
print(f"Last heartbeat: {region.last_heartbeat}")
print(f"Latency: {region.latency_ms}ms")
```python

**Solutions**:

1. Check network connectivity to region API
1. Verify API endpoint URL is correct
1. Check firewall rules and security groups
1. Review API server logs for errors

### Replication Sync Failures

**Symptom**: `ReplicationStatus.FAILED`

**Diagnosis**:
```python
status = manager.get_replication_status("vm-123")
print(json.dumps(status, indent=2))
```python

**Solutions**:

1. Verify both regions are healthy
1. Check bandwidth between regions
1. Verify resource still exists in primary
1. Check storage capacity in target region

### Failover Not Triggering

**Symptom**: Failover doesn't occur automatically

**Diagnosis**:
```python

# Check health check interval
primary = manager.get_primary_region()
backup = manager.list_regions()

# Manually check status
for region in [primary] + backup:
    status = await manager.check_region_health(region.region_id)
    print(f"{region.name}: {status}")
```python

**Solutions**:

1. Verify health check is running on schedule
1. Check that backup regions are registered
1. Verify failover strategy is set to AUTOMATIC
1. Review failover event history for errors

---

## Performance Tuning

### Sync Interval Optimization

```python

# Aggressive sync for critical regions (5 minutes)
manager.setup_replication(
    "us-east-1", "us-west-1",
    [ResourceType.VM],
    sync_interval_seconds=300
)

# Standard sync for distance (10 minutes)
manager.setup_replication(
    "us-east-1", "eu-west-1",
    [ResourceType.VM],
    sync_interval_seconds=600
)

# Low-frequency sync for far regions (30 minutes)
manager.setup_replication(
    "us-east-1", "ap-south-1",
    [ResourceType.CONFIG],  # Only config
    sync_interval_seconds=1800,
    compression=True
)
```python

### Batch Size Optimization

```python

# Smaller batches for low bandwidth
config = ReplicationConfig(
    source_region_id="us-east-1",
    target_region_id="ap-south-1",
    resource_types=[ResourceType.VM],
    batch_size=10,  # Small batches
    compression=True
)

# Larger batches for high bandwidth
config = ReplicationConfig(
    source_region_id="us-east-1",
    target_region_id="us-west-1",
    resource_types=[ResourceType.VM],
    batch_size=500,  # Large batches
    compression=False
)
```python

### Compression Strategy

```python

# Enable compression for long-distance
manager.setup_replication(
    "us-east-1", "ap-south-1",
    [ResourceType.VM, ResourceType.STORAGE],
    sync_interval_seconds=600,
    compression=True
)

# Disable for local regions (reduces CPU overhead)
manager.setup_replication(
    "us-east-1", "us-west-1",
    [ResourceType.VM],
    sync_interval_seconds=300,
    compression=False
)
```python

---

## Summary

The DebVisor Multi-region Support system provides enterprise-grade geo-distributed operations with:

- ? Seamless multi-datacenter replication
- ? Automatic failover with health monitoring
- ? Flexible configuration for any topology
- ? Complete audit trail and history
- ? Multiple access interfaces (CLI, API, Python)
- ? Production-ready error handling
- ? Comprehensive monitoring and statistics

For production deployment, ensure proper networking, security group rules, and health check monitoring are in place.
