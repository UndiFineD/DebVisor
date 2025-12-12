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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
ML Anomaly Detection Package

Statistical and ML-based anomaly detection for VM and system metrics.

Features:
- Multiple detection methods (Z-Score, IQR, EWMA)
- Baseline establishment from historical data
- Trend analysis with forecasting
- Confidence scoring for alerts
- Multi-interface access (Python, CLI, REST API)
- Comprehensive alert management and history
- JSON-based persistence

Author: DebVisor Development Team
Version: 1.0.0

Example Usage:

from opt.services.anomaly import get_anomaly_engine, MetricType

# Get engine instance
engine = get_anomaly_engine()

# Add metrics
engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.5)
engine.add_metric("vm-001", MetricType.MEMORY_USAGE, 82.3)

# Establish baselines
baseline = engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

# Detect anomalies
alerts = engine.detect_anomalies("vm-001", MetricType.CPU_USAGE, 95.0)

# Analyze trends
trend = engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=24)

# Manage alerts
active = engine.get_active_alerts()
history = engine.get_alert_history(resource_id="vm-001")
engine.acknowledge_alert(alert_id, acknowledged_by="admin")
"""

from opt.services.anomaly.core import (
    AnomalyDetectionEngine,
    AnomalyType,
    AnomalyAlert,
    Baseline,
    DetectionMethod,
    MetricType,
    MetricPoint,
    SeverityLevel,
    TrendAnalysis,
    get_anomaly_engine,
)

from opt.services.anomaly.cli import AnomalyCLI, main

from opt.services.anomaly.api import AnomalyAPI, create_flask_app

__version__ = "1.0.0"
__author__ = "DebVisor Development Team"

__all__ = [
    # Core engine
    "get_anomaly_engine",
    "AnomalyDetectionEngine",
    # Data models
    "MetricPoint",
    "Baseline",
    "AnomalyAlert",
    "TrendAnalysis",
    # Enumerations
    "MetricType",
    "AnomalyType",
    "SeverityLevel",
    "DetectionMethod",
    # CLI
    "AnomalyCLI",
    "main",
    # API
    "AnomalyAPI",
    "create_flask_app",
]
