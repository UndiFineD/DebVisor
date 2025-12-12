# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Enhanced Monitoring & Metrics Configuration
============================================

Provides configuration management for Prometheus metrics collection,
alerting rules, and observability enhancements.
"""

import logging
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import timedelta

logger = logging.getLogger(__name__)


###############################################################################
# Enumerations
###############################################################################


class AlertSeverity(Enum):
    """Alert severity levels"""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class MetricType(Enum):
    """Prometheus metric types"""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


###############################################################################
# Data Classes
###############################################################################


@dataclass
class MetricLabel:
    """Prometheus metric label"""

    name: str
    value: str


@dataclass
class MetricDefinition:
    """Prometheus metric definition"""

    name: str
    type: MetricType
    help_text: str
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None    # For histograms
    quantiles: Optional[List[float]] = None    # For summaries

    def to_yaml(self) -> str:
        """Convert to YAML representation"""
        yaml_str = """    # {self.help_text}
- metric_name: {self.name}
metric_type: {self.type.value}
help: {self.help_text}
"""
        if self.labels:
            yaml_str += "  labels:\n"
            for label in self.labels:
                yaml_str += f"    - {label}\n"

        if self.buckets:
            yaml_str += f"  buckets: {self.buckets}\n"

        if self.quantiles:
            yaml_str += f"  quantiles: {self.quantiles}\n"

        return yaml_str


@dataclass
class AlertRule:
    """Prometheus alert rule"""

    name: str
    expr: str
    for_duration: timedelta = field(default_factory=lambda: timedelta(minutes=5))
    severity: AlertSeverity = AlertSeverity.WARNING
    description: str = ""
    runbook_url: Optional[str] = None

    def to_yaml(self) -> str:
        """Convert to YAML representation"""
        return """- alert: {self.name}
expr: {self.expr}
for: {int(self.for_duration.total_seconds())}s
labels:
    severity: {self.severity.value}
annotations:
    summary: {self.description}
    runbook_url: {self.runbook_url or 'N/A'}
"""


@dataclass
class RecordingRule:
    """Prometheus recording rule"""

    name: str
    expr: str
    interval: timedelta = field(default_factory=lambda: timedelta(minutes=1))
    description: str = ""

    def to_yaml(self) -> str:
        """Convert to YAML representation"""
        return """- record: {self.name}
expr: {self.expr}
interval: {int(self.interval.total_seconds())}s
description: {self.description}
"""


@dataclass
class ScrapeConfig:
    """Prometheus scrape configuration"""

    job_name: str
    metrics_path: str = "/metrics"
    scheme: str = "http"
    scrape_interval: timedelta = field(default_factory=lambda: timedelta(minutes=1))
    scrape_timeout: timedelta = field(default_factory=lambda: timedelta(seconds=10))
    static_configs: List[Dict[str, Any]] = field(default_factory=list)
    relabel_configs: List[Dict[str, Any]] = field(default_factory=list)

    def to_yaml(self) -> str:
        """Convert to YAML representation"""
        yaml_str = """- job_name: {self.job_name}
metrics_path: {self.metrics_path}
scheme: {self.scheme}
scrape_interval: {int(self.scrape_interval.total_seconds())}s
scrape_timeout: {int(self.scrape_timeout.total_seconds())}s
"""

        if self.static_configs:
            yaml_str += "  static_configs:\n"
            for config in self.static_configs:
                yaml_str += f"    - targets: {config.get('targets', [])}\n"
                if "labels" in config:
                    yaml_str += "      labels:\n"
                    for label, value in config["labels"].items():
                        yaml_str += f"        {label}: {value}\n"

        if self.relabel_configs:
            yaml_str += "  relabel_configs:\n"
            for relabel in self.relabel_configs:
                yaml_str += f"    - source_labels: {relabel.get('source_labels', [])}\n"
                yaml_str += f"      regex: {relabel.get('regex', '.*')}\n"
                yaml_str += f"      target_label: {relabel.get('target_label', '')}\n"

        return yaml_str


###############################################################################
# Configuration Manager
###############################################################################


class MonitoringConfigManager:
    """Manages monitoring and metrics configuration"""

    def __init__(self) -> None:
        """Initialize monitoring config manager"""
        self.metrics: Dict[str, MetricDefinition] = {}
        self.alert_rules: Dict[str, AlertRule] = {}
        self.recording_rules: Dict[str, RecordingRule] = {}
        self.scrape_configs: Dict[str, ScrapeConfig] = {}
        self._initialize_default_metrics()
        self._initialize_default_alerts()
        logger.info("MonitoringConfigManager initialized")

    def _initialize_default_metrics(self) -> None:
        """Initialize default metrics"""
        default_metrics = [
            MetricDefinition(
                name="debvisor_cluster_nodes_total",
                type=MetricType.GAUGE,
                help_text="Total number of nodes in cluster",
                labels=["cluster"],
            ),
            MetricDefinition(
                name="debvisor_cluster_pods_total",
                type=MetricType.GAUGE,
                help_text="Total number of pods in cluster",
                labels=["cluster", "namespace"],
            ),
            MetricDefinition(
                name="debvisor_node_cpu_usage_percent",
                type=MetricType.GAUGE,
                help_text="CPU usage percentage per node",
                labels=["node"],
            ),
            MetricDefinition(
                name="debvisor_node_memory_usage_bytes",
                type=MetricType.GAUGE,
                help_text="Memory usage in bytes per node",
                labels=["node"],
            ),
            MetricDefinition(
                name="debvisor_disk_used_bytes",
                type=MetricType.GAUGE,
                help_text="Disk usage in bytes",
                labels=["node", "mount_point"],
            ),
            MetricDefinition(
                name="debvisor_network_bytes_in_total",
                type=MetricType.COUNTER,
                help_text="Total bytes received",
                labels=["interface"],
            ),
            MetricDefinition(
                name="debvisor_network_bytes_out_total",
                type=MetricType.COUNTER,
                help_text="Total bytes transmitted",
                labels=["interface"],
            ),
            MetricDefinition(
                name="debvisor_rpc_requests_total",
                type=MetricType.COUNTER,
                help_text="Total RPC requests",
                labels=["method", "status"],
            ),
            MetricDefinition(
                name="debvisor_rpc_request_duration_seconds",
                type=MetricType.HISTOGRAM,
                help_text="RPC request duration in seconds",
                labels=["method"],
                buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
            ),
        ]

        for metric in default_metrics:
            self.register_metric(metric)

    def _initialize_default_alerts(self) -> None:
        """Initialize default alert rules"""
        default_alerts = [
            AlertRule(
                name="HighCPUUsage",
                expr="debvisor_node_cpu_usage_percent > 80",
                severity=AlertSeverity.WARNING,
                description="Node CPU usage is above 80%",
                runbook_url="/docs/runbooks/high-cpu",
            ),
            AlertRule(
                name="HighMemoryUsage",
                expr=(
                    "(debvisor_node_memory_usage_bytes / "
                    "debvisor_node_memory_available_bytes) > 0.9"
                ),
                severity=AlertSeverity.WARNING,
                description="Node memory usage is above 90%",
                runbook_url="/docs/runbooks/high-memory",
            ),
            AlertRule(
                name="DiskSpaceCritical",
                expr="(debvisor_disk_used_bytes / debvisor_disk_total_bytes) > 0.95",
                severity=AlertSeverity.CRITICAL,
                description="Disk usage is above 95%",
                runbook_url="/docs/runbooks/disk-space",
            ),
            AlertRule(
                name="NodeNotReady",
                expr="debvisor_node_status == 0",
                for_duration=timedelta(minutes=5),
                severity=AlertSeverity.CRITICAL,
                description="Node is not ready",
                runbook_url="/docs/runbooks/node-not-ready",
            ),
            AlertRule(
                name="HighRPCErrorRate",
                expr=(
                    "(debvisor_rpc_requests_total{status='error'} / "
                    "debvisor_rpc_requests_total) > 0.05"
                ),
                severity=AlertSeverity.WARNING,
                description="RPC error rate is above 5%",
                runbook_url="/docs/runbooks/rpc-errors",
            ),
        ]

        for alert in default_alerts:
            self.register_alert_rule(alert)

    def register_metric(self, metric: MetricDefinition) -> None:
        """Register a metric definition"""
        self.metrics[metric.name] = metric
        logger.info(f"Metric registered: {metric.name}")

    def register_alert_rule(self, rule: AlertRule) -> None:
        """Register an alert rule"""
        self.alert_rules[rule.name] = rule
        logger.info(f"Alert rule registered: {rule.name}")

    def register_recording_rule(self, rule: RecordingRule) -> None:
        """Register a recording rule"""
        self.recording_rules[rule.name] = rule
        logger.info(f"Recording rule registered: {rule.name}")

    def register_scrape_config(self, config: ScrapeConfig) -> None:
        """Register a scrape configuration"""
        self.scrape_configs[config.job_name] = config
        logger.info(f"Scrape config registered: {config.job_name}")

    def get_metrics_yaml(self) -> str:
        """Get all metrics as YAML"""
        yaml_output = "    # Prometheus Metric Definitions\n"
        yaml_output += f"    # Total metrics: {len(self.metrics)}\n\n"

        for metric in self.metrics.values():
            yaml_output += metric.to_yaml()
            yaml_output += "\n"

        return yaml_output

    def get_alerts_yaml(self) -> str:
        """Get all alert rules as YAML"""
        yaml_output = "    # Prometheus Alert Rules\n"
        yaml_output += f"    # Total alerts: {len(self.alert_rules)}\n"
        yaml_output += "groups:\n"
        yaml_output += "  - name: debvisor_alerts\n"
        yaml_output += "    interval: 30s\n"
        yaml_output += "    rules:\n"

        for alert in self.alert_rules.values():
            # Indent for group structure
            for line in alert.to_yaml().split("\n"):
                if line:
                    yaml_output += f"      {line}\n"

        return yaml_output

    def get_scrape_config_yaml(self) -> str:
        """Get all scrape configurations as YAML"""
        yaml_output = "    # Prometheus Scrape Configurations\n"
        yaml_output += "scrape_configs:\n"

        for config in self.scrape_configs.values():
            for line in config.to_yaml().split("\n"):
                if line:
                    yaml_output += f"  {line}\n"

        return yaml_output

    def export_configuration(self) -> Dict[str, Any]:
        """Export entire configuration as dictionary"""
        return {
            "metrics": {name: asdict(metric) for name, metric in self.metrics.items()},
            "alert_rules": {
                name: asdict(rule) for name, rule in self.alert_rules.items()
            },
            "recording_rules": {
                name: asdict(rule) for name, rule in self.recording_rules.items()
            },
            "scrape_configs": {
                name: asdict(config) for name, config in self.scrape_configs.items()
            },
        }


###############################################################################
# Pre-built Monitoring Templates
###############################################################################


class MonitoringTemplates:
    """Pre-built monitoring templates"""

    @staticmethod
    def get_kubernetes_monitoring() -> MonitoringConfigManager:
        """Get Kubernetes monitoring template"""
        mgr = MonitoringConfigManager()

        # Add K8s-specific scrape config
        k8s_config = ScrapeConfig(
            job_name="kubernetes-apiserver",
            metrics_path="/metrics",
            scheme="https",
            static_configs=[
                {
                    "targets": ["kubernetes.default.svc.cluster.local:443"],
                }
            ],
        )
        mgr.register_scrape_config(k8s_config)

        # Add K8s-specific recording rule
        k8s_recording = RecordingRule(
            name="kubernetes:pod_memory_usage_mb",
            expr="kubernetes_pod_memory_rss_bytes / 1024 / 1024",
            description="Pod memory usage in MB",
        )
        mgr.register_recording_rule(k8s_recording)

        return mgr

    @staticmethod
    def get_infra_monitoring() -> MonitoringConfigManager:
        """Get infrastructure monitoring template"""
        mgr = MonitoringConfigManager()

        # Add node scrape config
        node_config = ScrapeConfig(
            job_name="node-exporter",
            static_configs=[
                {"targets": ["localhost:9100"], "labels": {"instance": "infra-node"}}
            ],
        )
        mgr.register_scrape_config(node_config)

        # Add node recording rules
        node_recording = RecordingRule(
            name="node:cpu_usage_percent",
            expr="100 - (avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
            description="CPU usage percentage",
        )
        mgr.register_recording_rule(node_recording)

        return mgr

    @staticmethod
    def get_storage_monitoring() -> MonitoringConfigManager:
        """Get storage monitoring template"""
        mgr = MonitoringConfigManager()

        # Add storage scrape config
        storage_config = ScrapeConfig(
            job_name="ceph-exporter",
            static_configs=[
                {
                    "targets": ["localhost:9283"],
                }
            ],
        )
        mgr.register_scrape_config(storage_config)

        return mgr


###############################################################################
# Example Usage
###############################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create manager
    mgr = MonitoringConfigManager()

    # Add custom metric
    custom_metric = MetricDefinition(
        name="debvisor_custom_metric",
        type=MetricType.GAUGE,
        help_text="Custom application metric",
        labels=["app", "instance"],
    )
    mgr.register_metric(custom_metric)

    # Add custom alert
    custom_alert = AlertRule(
        name="CustomAlertExample",
        expr="debvisor_custom_metric > 100",
        severity=AlertSeverity.WARNING,
        description="Custom metric exceeded threshold",
    )
    mgr.register_alert_rule(custom_alert)

    # Export configuration
    config = mgr.export_configuration()
    print(f"Total metrics: {len(config['metrics'])}")
    print(f"Total alerts: {len(config['alert_rules'])}")

    # Get Kubernetes template
    k8s_mgr = MonitoringTemplates.get_kubernetes_monitoring()
    print(f"K8s template scrape configs: {len(k8s_mgr.scrape_configs)}")
