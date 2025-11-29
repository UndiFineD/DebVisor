# DebVisor Phase 5 Week 3-4 API Documentation

Comprehensive API reference for newly implemented enterprise features.

---

## Table of Contents

1. [Advanced Analytics Dashboard API](#advanced-analytics-dashboard-api)
1. [Custom Report Scheduling API](#custom-report-scheduling-api)
1. [Advanced Diagnostics API](#advanced-diagnostics-api)
1. [Network Configuration TUI API](#network-configuration-tui-api)
1. [Multi-Cluster Management API](#multi-cluster-management-api)

---

## Advanced Analytics Dashboard API

### Module: `opt/web/panel/analytics.py`

Provides real-time metrics aggregation, trend analysis, anomaly detection, and forecasting.

### Classes

#### `AnalyticsEngine`

Main class for metrics collection and analysis.

**Methods:**

##### `record_metric(metric_type, value, resource_id, tags=None, timestamp=None) -> bool`

Record a single metric data point.

**Parameters:**

- `metric_type: MetricType` - Type of metric (CPU_USAGE, MEMORY_USAGE, etc.)
- `value: float` - Metric value
- `resource_id: str` - Resource identifier
- `tags: Dict[str, str]` (optional) - Additional tags for filtering
- `timestamp: datetime` (optional) - Data point timestamp (defaults to now)

**Returns:** `bool` - True if recorded successfully

**Example:**

```python
engine = AnalyticsEngine()
engine.record_metric(
    metric_type=MetricType.CPU_USAGE,
    value=45.5,
    resource_id="node-1",
    tags={'host': 'server1'}
)
```python

---

##### `aggregate_metrics(metric_type, start_time, end_time, granularity, resource_id=None) -> List[AggregatedMetrics]`

Aggregate metrics over time buckets.

**Parameters:**

- `metric_type: MetricType` - Metric type to aggregate
- `start_time: datetime` - Start of time range
- `end_time: datetime` - End of time range
- `granularity: TimeGranularity` - Bucketing granularity (MINUTE, HOUR, DAY, etc.)
- `resource_id: str` (optional) - Filter by resource

**Returns:** `List[AggregatedMetrics]` - Aggregated data points

**Example:**
```python
from datetime import datetime, timedelta
from opt.web.panel.analytics import TimeGranularity

result = engine.aggregate_metrics(
    metric_type=MetricType.CPU_USAGE,
    start_time=datetime.utcnow() - timedelta(days=7),
    end_time=datetime.utcnow(),
    granularity=TimeGranularity.HOUR,
    resource_id='node-1'
)
```python

---

##### `detect_anomalies(metric_type, threshold_stddevs=2.5, resource_id=None) -> List[Dict]`

Detect anomalous values using statistical analysis.

**Parameters:**

- `metric_type: MetricType` - Metric type to analyze
- `threshold_stddevs: float` - Deviation threshold (default: 2.5 standard deviations)
- `resource_id: str` (optional) - Filter by resource

**Returns:** `List[Dict]` - Anomalies with metadata

**Example:**
```python
anomalies = engine.detect_anomalies(
    metric_type=MetricType.MEMORY_USAGE,
    threshold_stddevs=3.0,
    resource_id='node-1'
)

# Returns: [{'value': 98.5, 'timestamp': '...', 'zscore': 3.2, ...}]
```python

---

##### `calculate_trend(metric_type, time_window=86400, resource_id=None) -> Dict[str, Any]`

Calculate trend using linear regression.

**Parameters:**

- `metric_type: MetricType` - Metric to analyze
- `time_window: int` - Time window in seconds (default: 24 hours)
- `resource_id: str` (optional) - Filter by resource

**Returns:** `Dict` with keys:

- `slope: float` - Trend slope (positive = increasing)
- `direction: str` - "INCREASING", "DECREASING", or "STABLE"
- `magnitude: float` - Absolute change over period

**Example:**
```python
trend = engine.calculate_trend(
    metric_type=MetricType.DISK_IO,
    time_window=3600,  # Last hour
    resource_id='node-1'
)
print(f"Trend: {trend['direction']} at {trend['slope']:.2f} units/minute")
```python

---

##### `forecast_metric(metric_type, periods_ahead=10, resource_id=None) -> List[float]`

Forecast metric values using exponential smoothing.

**Parameters:**

- `metric_type: MetricType` - Metric to forecast
- `periods_ahead: int` - Number of periods to forecast
- `resource_id: str` (optional) - Filter by resource

**Returns:** `List[float]` - Forecasted values

**Example:**
```python
forecast = engine.forecast_metric(
    metric_type=MetricType.CPU_USAGE,
    periods_ahead=5,
    resource_id='node-1'
)

# Returns: [45.2, 45.8, 46.1, 46.5, 47.0]
```python

---

##### `get_dashboard_summary(time_window=3600) -> Dict[str, Any]`

Generate comprehensive dashboard summary.

**Parameters:**

- `time_window: int` - Time window in seconds

**Returns:** `Dict` containing:

- `summary: str` - Text summary
- `metrics: List[Dict]` - Metric summaries
- `health_score: float` - Overall health (0-100)
- `anomalies: List[Dict]` - Recent anomalies
- `trends: Dict` - Trend analysis

**Example:**
```python
dashboard = engine.get_dashboard_summary(time_window=3600)
```python

---

#### Enumerations

##### `TimeGranularity` Enum

Time bucketing granularities:

- `MINUTE` - 1 minute buckets
- `HOUR` - 1 hour buckets
- `DAY` - 24 hour buckets
- `WEEK` - 7 day buckets
- `MONTH` - ~30 day buckets

##### `MetricType` Enum

Supported metric types:

- `CPU_USAGE` - CPU percentage
- `MEMORY_USAGE` - Memory percentage
- `DISK_IO` - Disk I/O operations/sec
- `NETWORK_IO` - Network throughput bytes/sec
- `QUERY_LATENCY` - Query response time (ms)
- `RPC_CALLS` - RPC invocation count
- `ERRORS` - Error count
- `ALERTS` - Alert count
- `CONNECTIONS` - Active connections
- `THROUGHPUT` - Request throughput

---

## Custom Report Scheduling API

### Module: `opt/web/panel/reporting.py`

Manages scheduled report generation and email delivery.

### Classes [2]

#### `ReportScheduler`

Orchestrates report generation and distribution.

**Methods:**

##### `register_template(template: ReportTemplate) -> bool`

Register a report template.

**Parameters:**

- `template: ReportTemplate` - Template definition

**Returns:** `bool` - Success status

**Example:**
```python
from opt.services.reporting_scheduler import ReportTemplate, ReportScheduler

template = ReportTemplate(
    template_id="daily_metrics",
    name="Daily Metrics Report",
    description="Daily system metrics summary",
    sections=[
        "system_health",
        "performance_analysis",
        "alerts_summary"
    ]
)

scheduler = ReportScheduler()
scheduler.register_template(template)
```python

---

##### `schedule_report(report_id, name, template_id, frequency, recipients, parameters={}) -> bool`

Schedule a new report.

**Parameters:**

- `report_id: str` - Unique report identifier
- `name: str` - Report name
- `template_id: str` - Template to use
- `frequency: ReportFrequency` - Execution frequency
- `recipients: List[str]` - Email recipients
- `parameters: Dict` (optional) - Template parameters

**Returns:** `bool` - Success status

**Example:**
```python
from opt.services.reporting_scheduler import ReportFrequency

scheduler.schedule_report(
    report_id="daily_ops",
    name="Daily Operations Report",
    template_id="daily_metrics",
    frequency=ReportFrequency.DAILY,
    recipients=["ops@example.com", "mgmt@example.com"],
    parameters={
        "time_window": 86400,
        "include_forecasts": True
    }
)
```python

---

##### `register_generation_callback(template_id, callback) -> bool`

Register callback for report generation.

**Parameters:**

- `template_id: str` - Template ID
- `callback: Callable` - Async callback function

**Callback Signature:**
```python
async def generate_report(scheduled_report: ScheduledReport) -> str:
    # Generate report content
    # Return: Report content as string
    return report_content
```python

**Returns:** `bool` - Success status

---

##### `generate_report(scheduled_report: ScheduledReport) -> GeneratedReport`

Generate a single report.

**Parameters:**

- `scheduled_report: ScheduledReport` - Report configuration

**Returns:** `GeneratedReport` - Generated report with status

---

##### `deliver_report(generated_report, scheduled_report) -> bool`

Deliver report via email.

**Parameters:**

- `generated_report: GeneratedReport` - Report to deliver
- `scheduled_report: ScheduledReport` - Delivery configuration

**Returns:** `bool` - Success status

**Features:**

- Automatic retry (3 attempts)
- SMTP delivery with TLS support
- Delivery tracking

---

##### `execute_scheduled_reports() -> Dict[str, Any]`

Execute all pending scheduled reports.

**Returns:** `Dict` containing:

- `total_executed: int` - Reports executed
- `succeeded: int` - Successful reports
- `failed: int` - Failed reports
- `pending: int` - Still pending

---

##### `get_report_history(scheduled_report_id, limit=100) -> List[GeneratedReport]`

Retrieve report history.

**Parameters:**

- `scheduled_report_id: str` - Scheduled report ID
- `limit: int` - Maximum results

**Returns:** `List[GeneratedReport]` - Historical reports

---

#### `EmailNotifier` Class

Handles SMTP email delivery.

**Configuration (Environment Variables):**
```bash
SMTP_HOST=mail.example.com
SMTP_PORT=587
SMTP_USER=reports@example.com
SMTP_PASSWORD=password
SMTP_TLS=true
REPORT_FROM_EMAIL=reports@example.com
```python

---

#### Enumerations [2]

##### `ReportFrequency`

- `DAILY` - Daily execution
- `WEEKLY` - Weekly execution (Mondays)
- `MONTHLY` - Monthly execution (1st of month)
- `QUARTERLY` - Quarterly execution
- `ON_DEMAND` - Manual execution only

##### `ReportStatus`

- `PENDING` - Scheduled but not yet generated
- `GENERATING` - Currently generating
- `COMPLETED` - Successfully generated
- `FAILED` - Generation failed
- `DELIVERED` - Successfully delivered

---

## Advanced Diagnostics API

### Module: `opt/tools/diagnostics.py`

Provides comprehensive system health diagnostics and performance analysis.

### Classes [3]

#### `DiagnosticsFramework`

Main diagnostics orchestration class.

**Methods:**

##### `run_diagnostics() -> DiagnosticReport`

Execute all registered diagnostic checks.

**Returns:** `DiagnosticReport` with:

- `checks: List[CheckResult]` - Individual check results
- `overall_health_score: float` - 0-100 health percentage
- `issues_found: int` - Total issues detected
- `critical_issues: int` - Critical issue count
- `summary: str` - Human-readable summary

**Example:**
```python
from opt.services.diagnostics import DiagnosticsFramework

framework = DiagnosticsFramework()
report = framework.run_diagnostics()

print(f"Health Score: {report.overall_health_score}%")
print(f"Summary: {report.summary}")
print(f"Critical Issues: {report.critical_issues}")
```python

---

##### `get_remediation_suggestions(report) -> List[str]`

Get actionable remediation suggestions.

**Parameters:**

- `report: DiagnosticReport` - Report to analyze

**Returns:** `List[str]` - Remediation suggestions

**Example:**
```python
suggestions = framework.get_remediation_suggestions(report)
for suggestion in suggestions:
    print(f"  - {suggestion}")
```python

---

##### `get_health_trend(hours=24) -> List[Dict]`

Get health score trend over time.

**Parameters:**

- `hours: int` - Historical period in hours

**Returns:** `List[Dict]` - Health scores with timestamps

**Example:**
```python
trend = framework.get_health_trend(hours=24)

# Returns: [
#     {'timestamp': '2025-01-15T10:00:00', 'health_score': 92.5, 'issues': 1, 'critical': 0},
#     {'timestamp': '2025-01-15T11:00:00', 'health_score': 88.0, 'issues': 3, 'critical': 0},
# ]
```python

---

##### `get_diagnostics_summary() -> Dict[str, Any]`

Get comprehensive diagnostics summary.

**Returns:** `Dict` with:

- `last_run: str` - Last execution timestamp
- `overall_health: float` - Current health score
- `checks_registered: int` - Number of checks
- `reports_generated: int` - Historical report count
- `check_details: List[Dict]` - Per-check summaries

---

#### Diagnostic Check Classes

##### `CPUDiagnostics`

Analyzes CPU usage and performance.

**Alerts:**

- WARNING: CPU > 80%
- Provides: CPU %, frequency, load average

---

##### `MemoryDiagnostics`

Analyzes memory and swap usage.

**Alerts:**

- WARNING: Memory > 85%
- WARNING: Swap > 50%
- Provides: Memory %, swap %, available space

---

##### `DiskDiagnostics`

Analyzes disk space and I/O performance.

**Alerts:**

- WARNING: Disk > 80%
- CRITICAL: Disk > 95%
- Provides: Disk usage %, I/O metrics

---

##### `NetworkDiagnostics`

Analyzes network connectivity and latency.

**Alerts:**

- WARNING: Connectivity failed
- Provides: Interface status, latency, traffic

---

## Network Configuration TUI API

### Module: `opt/netcfg-tui/netcfg_tui_full.py`

Interactive terminal UI for network configuration management.

### Classes [4]

#### `NetworkConfig`

Core network configuration management.

**Methods:**

##### `save_config(filepath: str) -> bool`

Save current configuration to JSON file.

**Parameters:**

- `filepath: str` - Destination file path

**Returns:** `bool` - Success status

**Example:**
```python
from opt.netcfg_tui.main import NetworkConfig

config = NetworkConfig()
config.save_config('/etc/debvisor/network_config.json')
```python

---

##### `load_config(filepath: str) -> bool`

Load configuration from JSON file.

**Parameters:**

- `filepath: str` - Source file path

**Returns:** `bool` - Success status

---

##### `add_change(change_type, target, details={}, description="") -> None`

Queue a configuration change.

**Parameters:**

- `change_type: ConfigChangeType` - Type of change
- `target: str` - Target interface/route name
- `details: Dict` - Additional parameters
- `description: str` - Human-readable description

**ConfigChangeType Options:**

- `INTERFACE_UP` - Bring interface up
- `INTERFACE_DOWN` - Bring interface down
- `INTERFACE_ADDRESS` - Configure IP address
- `ROUTE_ADD` - Add route
- `ROUTE_DELETE` - Delete route
- `HOSTNAME_SET` - Set system hostname

---

##### `apply_changes(dry_run=False) -> Tuple[bool, List[str]]`

Apply all queued changes.

**Parameters:**

- `dry_run: bool` - Preview without applying (default: False)

**Returns:** `Tuple` with:

- `bool` - Success status
- `List[str]` - Commands executed/proposed

**Example:**
```python
config = NetworkConfig()
config.add_change(
    change_type=ConfigChangeType.INTERFACE_UP,
    target="eth0"
)
success, commands = config.apply_changes(dry_run=True)
for cmd in commands:
    print(f"Would execute: {cmd}")
```python

---

### Command-Line Interface

#### Usage

```bash

# Interactive mode
python opt/netcfg-tui/main.py

# Apply configuration file
python opt/netcfg-tui/main.py --apply /path/to/config.json

# Dry-run (preview changes)
python opt/netcfg-tui/main.py --apply /path/to/config.json --dry-run

# Save current configuration
python opt/netcfg-tui/main.py --save /path/to/config.json

# Load configuration
python opt/netcfg-tui/main.py --load /path/to/config.json
```python

---

## Multi-Cluster Management API

### Module: `opt/services/multi_cluster.py`

Manages multi-cluster deployments with federation, service discovery, and load balancing.

### Classes [5]

#### `MultiClusterManager`

High-level multi-cluster orchestration.

**Methods:**

##### `add_cluster(name, endpoint, region, version) -> str`

Add a new cluster to the federation.

**Parameters:**

- `name: str` - Cluster name
- `endpoint: str` - Kubernetes API endpoint URL
- `region: str` - Geographic region
- `version: str` - Cluster version

**Returns:** `str` - Cluster ID

**Example:**
```python
from opt.services.multi_cluster import MultiClusterManager

manager = MultiClusterManager()

cluster_id = manager.add_cluster(
    name="prod-west",
    endpoint="https://k8s-west.example.com:6443",
    region="us-west-2",
    version="1.28.0"
)
```python

---

##### `get_federation_status() -> Dict[str, Any]`

Get overall federation status.

**Returns:** `Dict` with:

- `total_clusters: int` - Number of clusters
- `healthy_clusters: int` - Responsive clusters
- `total_nodes: int` - Aggregate node count
- `total_jobs: int` - Active jobs
- `total_services: int` - Services running
- `clusters: List[Dict]` - Per-cluster details

**Example:**
```python
status = manager.get_federation_status()
print(f"Health: {status['healthy_clusters']}/{status['total_clusters']}")
```python

---

##### `create_federation_policy(name, description, clusters, replication_strategy, failover_enabled) -> str`

Create federation policy.

**Parameters:**

- `name: str` - Policy name
- `description: str` - Policy description
- `clusters: List[str]` - Cluster IDs
- `replication_strategy: ReplicationStrategy` - Sync strategy
- `failover_enabled: bool` - Enable automatic failover

**Returns:** `str` - Policy ID

**Example:**
```python
from opt.services.multi_cluster import ReplicationStrategy

policy_id = manager.create_federation_policy(
    name="ha-policy",
    description="High availability policy",
    clusters=[cluster_id_1, cluster_id_2],
    replication_strategy=ReplicationStrategy.SYNCHRONOUS,
    failover_enabled=True
)
```python

---

#### `ClusterRegistry`

Central cluster registry.

**Methods:**

##### `list_clusters(region=None) -> List[ClusterNode]`

List all clusters.

**Parameters:**

- `region: str` (optional) - Filter by region

**Returns:** `List[ClusterNode]` - Cluster list

---

##### `get_healthy_clusters(region=None) -> List[ClusterNode]`

Get responsive healthy clusters.

---

#### `ServiceDiscovery`

Cross-cluster service discovery.

**Methods:**

##### `discover_service(service_name, region=None) -> CrossClusterService`

Discover service by name.

**Parameters:**

- `service_name: str` - Service name
- `region: str` (optional) - Region filter

**Returns:** `CrossClusterService` or None

---

##### `get_service_endpoints(service_id, region=None) -> List[str]`

Get all service endpoints.

**Returns:** `List[str]` - API endpoints

---

#### `LoadBalancer`

Cross-cluster work distribution.

**Methods:**

##### `get_next_cluster(policy="round_robin", region=None) -> ClusterNode`

Select next cluster for work.

**Parameters:**

- `policy: str` - Load balancing policy
- `region: str` (optional) - Region constraint

**Policies:**

- `"round_robin"` - Sequential selection
- `"least_loaded"` - Lowest CPU usage
- `"nearest"` - Lowest latency

**Returns:** `ClusterNode` - Selected cluster

---

##### `distribute_work(work_items, region=None) -> Dict[str, int]`

Distribute work across clusters.

**Parameters:**

- `work_items: int` - Items to distribute
- `region: str` (optional) - Region constraint

**Returns:** `Dict` - Cluster ID -> work count mapping

---

### Enumerations [3]

#### `ClusterStatus`

- `HEALTHY` - All systems normal
- `DEGRADED` - Partial functionality
- `UNHEALTHY` - Significant issues
- `OFFLINE` - Not responding
- `UNKNOWN` - Status unknown

#### `ReplicationStrategy`

- `NONE` - No replication
- `SYNCHRONOUS` - Sync across all clusters
- `ASYNCHRONOUS` - Async replication
- `MULTI_MASTER` - Multi-master federation

#### `ResourceType`

- `NODE` - Cluster node
- `JOB` - Workload/job
- `SERVICE` - Service
- `VOLUME` - Storage volume
- `NETWORK` - Network resource

---

## Error Handling

All APIs use consistent error handling:

```python
try:
    result = api_call()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    # Handle error appropriately
```python

---

## Performance Considerations

### Analytics Engine

- **Data Retention:** 35 days (configurable)
- **Aggregation:** O(n) for n data points
- **Anomaly Detection:** O(n log n) with statistical analysis

### Report Scheduler

- **Max Retries:** 3 attempts with exponential backoff
- **Concurrent Reports:** Limited by system resources
- **Email Delivery:** Async with tracking

### Diagnostics Framework

- **Check Timeout:** 30 seconds per check
- **Cache TTL:** Metrics cached for 5 minutes
- **History Retention:** Last 1,000 reports

### Multi-Cluster

- **Cluster Discovery:** 60-second heartbeat timeout
- **Load Balancing:** O(n) complexity for distribution
- **Service Endpoints:** DNS cached for 300 seconds

---

## Integration Examples

### Complete Analytics Workflow

```python
from opt.web.panel.analytics import AnalyticsEngine, MetricType, TimeGranularity
from datetime import datetime, timedelta

engine = AnalyticsEngine()

# Collect metrics
for i in range(100):
    engine.record_metric(
        metric_type=MetricType.CPU_USAGE,
        value=40 + (i % 20),
        resource_id="node-1"
    )

# Analyze
anomalies = engine.detect_anomalies(MetricType.CPU_USAGE)
trend = engine.calculate_trend(MetricType.CPU_USAGE)
forecast = engine.forecast_metric(MetricType.CPU_USAGE, periods_ahead=10)

# Dashboard
summary = engine.get_dashboard_summary(time_window=3600)
```python

### Complete Diagnostics Workflow

```python
from opt.services.diagnostics import DiagnosticsFramework

framework = DiagnosticsFramework()

# Run diagnostics
report = framework.run_diagnostics()

# Get insights
print(f"Health: {report.overall_health_score}%")
print(f"Issues: {report.issues_found}")
print(f"Critical: {report.critical_issues}")

# Get remediation
suggestions = framework.get_remediation_suggestions(report)
for sug in suggestions:
    print(f"  → {sug}")

# Monitor trend
trend = framework.get_health_trend(hours=24)
```python

---

## Version Information

- **Phase:** 5 Week 3-4
- **Release Date:** January 2025
- **Python:** 3.8+
- **Status:** Production Ready
