#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
ML Anomaly Detection - Command Line Interface

CLI for managing anomaly detection, baselines, and alert handling.

Author: DebVisor Development Team
Version: 1.0.0
"""

import argparse
import json
import sys
from typing import Optional, Any, List

from opt.core.cli_utils import (
    format_table,
    setup_common_args,
    handle_cli_error,
    print_error,
)

from opt.services.anomaly.core import (
    get_anomaly_engine,
    AnomalyDetectionEngine,
    MetricType,
    SeverityLevel,
    DetectionMethod,
)


class AnomalyCLI:
    """Command-line interface for anomaly detection."""

    def __init__(self, engine: AnomalyDetectionEngine) -> None:
        """Initialize CLI.

        Args:
            engine: AnomalyDetectionEngine instance
        """
        self.engine = engine
        self.parser=self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser."""
        parser = argparse.ArgumentParser(
            _prog = "debvisor-anomaly", description="ML Anomaly Detection System"
        )

        setup_common_args(parser)

        _subparsers=parser.add_subparsers(dest="command", help="Commands")

        # Metric commands
        self._add_metric_commands(subparsers)

        # Baseline commands
        self._add_baseline_commands(subparsers)

        # Detection commands
        self._add_detection_commands(subparsers)

        # Alert commands
        self._add_alert_commands(subparsers)

        # Trend commands
        self._add_trend_commands(subparsers)

        # System commands
        self._add_system_commands(subparsers)

        return parser

    def _add_metric_commands(self, subparsers: Any) -> None:
        """Add metric management commands."""
        _metric=subparsers.add_parser("metric", help="Metric management")
        _metric_sub=metric.add_subparsers(dest="metric_cmd", help="Metric commands")

        # metric add
        _add=metric_sub.add_parser("add", help="Add metric data point")
        add.add_argument("resource_id", help="Resource identifier")
        add.add_argument(
            "metric_type", help="Metric type (cpu_usage, memory_usage, disk_io, etc.)"
        )
        add.add_argument("value", type=float, help="Metric value")

        # metric list
        _list_cmd=metric_sub.add_parser("list", help="List monitored metrics")
        list_cmd.add_argument("--resource", help="Filter by resource ID")
        list_cmd.add_argument("--metric", help="Filter by metric type")

        # metric history
        _hist=metric_sub.add_parser("history", help="View metric history")
        hist.add_argument("resource_id", help="Resource identifier")
        hist.add_argument("metric_type", help="Metric type")
        hist.add_argument(
            "--limit", type=int, default=50, help="Number of records (default: 50)"
        )

    def _add_baseline_commands(self, subparsers: Any) -> None:
        """Add baseline management commands."""
        _baseline=subparsers.add_parser("baseline", help="Baseline management")
        baseline_sub = baseline.add_subparsers(
            _dest = "baseline_cmd", help="Baseline commands"
        )

        # baseline establish
        establish = baseline_sub.add_parser(
            "establish", help="Establish baseline from data"
        )
        establish.add_argument("resource_id", help="Resource identifier")
        establish.add_argument("metric_type", help="Metric type")
        establish.add_argument(
            "--percentile", action="store_true", help="Use percentile-based baseline"
        )

        # baseline list
        _list_cmd=baseline_sub.add_parser("list", help="List baselines")
        list_cmd.add_argument("--resource", help="Filter by resource ID")

        # baseline show
        _show=baseline_sub.add_parser("show", help="Show baseline details")
        show.add_argument("resource_id", help="Resource identifier")
        show.add_argument("metric_type", help="Metric type")

    def _add_detection_commands(self, subparsers: Any) -> None:
        """Add anomaly detection commands."""
        _detect=subparsers.add_parser("detect", help="Anomaly detection")
        _detect_sub=detect.add_subparsers(dest="detect_cmd", help="Detection commands")

        # detect check
        _check=detect_sub.add_parser("check", help="Check for anomalies")
        check.add_argument("resource_id", help="Resource identifier")
        check.add_argument("metric_type", help="Metric type")
        check.add_argument("value", type=float, help="Current metric value")
        check.add_argument(
            "--methods", nargs="+", help="Detection methods (z_score, iqr, ewma)"
        )

        # detect recent
        _recent=detect_sub.add_parser("recent", help="Get recent detections")
        recent.add_argument("--resource", help="Filter by resource ID")
        recent.add_argument(
            "--hours", type=int, default=24, help="Look back hours (default: 24)"
        )
        recent.add_argument(
            "--limit", type=int, default=50, help="Limit results (default: 50)"
        )

    def _add_alert_commands(self, subparsers: Any) -> None:
        """Add alert management commands."""
        _alert=subparsers.add_parser("alert", help="Alert management")
        _alert_sub=alert.add_subparsers(dest="alert_cmd", help="Alert commands")

        # alert list
        _list_cmd=alert_sub.add_parser("list", help="List active alerts")
        list_cmd.add_argument("--resource", help="Filter by resource ID")
        list_cmd.add_argument(
            "--severity", help="Filter by severity (info, warning, critical)"
        )

        # alert history
        _hist=alert_sub.add_parser("history", help="Alert history")
        hist.add_argument("--resource", help="Filter by resource ID")
        hist.add_argument(
            "--hours", type=int, default=24, help="Look back hours (default: 24)"
        )
        hist.add_argument(
            "--limit", type=int, default=100, help="Limit results (default: 100)"
        )

        # alert acknowledge
        _ack=alert_sub.add_parser("acknowledge", help="Acknowledge alert")
        ack.add_argument("alert_id", help="Alert ID")
        ack.add_argument("--by", required=True, help="User acknowledging")
        ack.add_argument("--notes", default="", help="Acknowledgment notes")

        # alert show
        _show=alert_sub.add_parser("show", help="Show alert details")
        show.add_argument("alert_id", help="Alert ID")

    def _add_trend_commands(self, subparsers: Any) -> None:
        """Add trend analysis commands."""
        _trend=subparsers.add_parser("trend", help="Trend analysis")
        _trend_sub=trend.add_subparsers(dest="trend_cmd", help="Trend commands")

        # trend analyze
        _analyze=trend_sub.add_parser("analyze", help="Analyze metric trend")
        analyze.add_argument("resource_id", help="Resource identifier")
        analyze.add_argument("metric_type", help="Metric type")
        analyze.add_argument(
            "--hours", type=int, default=24, help="Analysis window hours (default: 24)"
        )

        # trend list
        _list_cmd=trend_sub.add_parser("list", help="List trend analyses")
        list_cmd.add_argument("--resource", help="Filter by resource ID")

    def _add_system_commands(self, subparsers: Any) -> None:
        """Add system commands."""
        _system=subparsers.add_parser("system", help="System commands")
        _system_sub=system.add_subparsers(dest="system_cmd", help="System commands")

        # system stats
        system_sub.add_parser("stats", help="System statistics")

        # system config
        _config=system_sub.add_parser("config", help="Show configuration")
        config.add_argument("--param", help="Show specific parameter")

        # system export
        _export=system_sub.add_parser("export", help="Export data")
        export.add_argument(
            "--type", choices=["alerts", "baselines", "metrics"], required=True
        )
        export.add_argument("--resource", help="Filter by resource ID")
        export.add_argument("--output", required=True, help="Output file")

    @handle_cli_error

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI.

        Args:
            args: Command line arguments (default: sys.argv[1:])

        Returns:
            Exit code
        """
        _parsed=self.parser.parse_args(args)

        if not parsed.command:
            self.parser.print_help()
            return 0

        # Route to handler
        try:
            if parsed.command == "metric":
                return self._handle_metric(parsed)
            elif parsed.command == "baseline":
                return self._handle_baseline(parsed)
            elif parsed.command == "detect":
                return self._handle_detect(parsed)
            elif parsed.command == "alert":
                return self._handle_alert(parsed)
            elif parsed.command == "trend":
                return self._handle_trend(parsed)
            elif parsed.command == "system":
                return self._handle_system(parsed)
            else:
                print_error(f"Unknown command: {parsed.command}")
                return 1

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def _handle_metric(self, args: argparse.Namespace) -> int:
        """Handle metric commands."""
        if args.metric_cmd == "add":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]
                self.engine.add_metric(args.resource_id, metric_type, args.value)
                print(
                    f"? Metric added: {args.resource_id}/{args.metric_type} = {args.value}"
                )
                return 0
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        elif args.metric_cmd == "list":
            metrics_data = []
            for (resource_id, metric_type), history in self.engine.metrics.items():
                if args.resource and resource_id != args.resource:
                    continue
                if args.metric and metric_type.value != args.metric:
                    continue

                metrics_data.append(
                    [
                        resource_id,
                        metric_type.value,
                        len(history),
                        f"{history[-1].value:.2f}" if history else "N/A",
                        history[-1].timestamp.isoformat() if history else "N/A",
                    ]
                )

            if metrics_data:
                print(
                    format_table(
                        metrics_data,
                        _headers = [
                            "Resource",
                            "Metric Type",
                            "Points",
                            "Latest Value",
                            "Last Update",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No metrics found")
            return 0

        elif args.metric_cmd == "history":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]
                _key=(args.resource_id, metric_type)

                if key not in self.engine.metrics:
                    print(f"No data for {key}")
                    return 1

                metric_history: List[Any] = list(self.engine.metrics[key])[-args.limit :]
                history_data = [
                    [p.timestamp.isoformat(), f"{p.value:.2f}"] for p in metric_history
                ]

                print(
                    format_table(
                        history_data, headers=["Timestamp", "Value"], tablefmt="grid"
                    )
                )
                return 0
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        return 1

    def _handle_baseline(self, args: argparse.Namespace) -> int:
        """Handle baseline commands."""
        if args.baseline_cmd == "establish":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]
                baseline = self.engine.establish_baseline(
                    args.resource_id, metric_type, percentile_based=args.percentile
                )

                if baseline:
                    print(
                        f"? Baseline established: {args.resource_id}/{args.metric_type}"
                    )
                    print(f"  Mean: {baseline.mean:.2f}")
                    print(f"  StdDev: {baseline.stddev:.2f}")
                    print(
                        f"  Range: {baseline.min_value:.2f} - {baseline.max_value:.2f}"
                    )
                    print(f"  Samples: {baseline.sample_count}")
                    return 0
                else:
                    print("Failed to establish baseline (insufficient data)")
                    return 1
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        elif args.baseline_cmd == "list":
            baseline_data = []
            for (resource_id, metric_type), baseline in self.engine.baselines.items():
                if args.resource and resource_id != args.resource:
                    continue

                baseline_data.append(
                    [
                        resource_id,
                        metric_type.value,
                        f"{baseline.mean:.2f}",
                        f"{baseline.stddev:.2f}",
                        baseline.sample_count,
                        baseline.created_at.isoformat()[:10],
                    ]
                )

            if baseline_data:
                print(
                    format_table(
                        baseline_data,
                        _headers = [
                            "Resource",
                            "Metric",
                            "Mean",
                            "StdDev",
                            "Samples",
                            "Created",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No baselines found")
            return 0

        elif args.baseline_cmd == "show":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]
                _key=(args.resource_id, metric_type)

                if key not in self.engine.baselines:
                    print(f"Baseline not found: {key}")
                    return 1

                baseline = self.engine.baselines[key]
                print(f"\nBaseline: {key}")
                print(f"  Mean: {baseline.mean:.2f}")
                print(f"  StdDev: {baseline.stddev:.2f}")
                print(f"  Min: {baseline.min_value:.2f}")
                print(f"  Max: {baseline.max_value:.2f}")
                print(f"  P25: {baseline.p25:.2f}")
                print(f"  P50: {baseline.p50:.2f}")
                print(f"  P75: {baseline.p75:.2f}")
                print(f"  P95: {baseline.p95:.2f}")
                print(f"  Samples: {baseline.sample_count}")
                print(f"  Created: {baseline.created_at.isoformat()}")
                return 0
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        return 1

    def _handle_detect(self, args: argparse.Namespace) -> int:
        """Handle detection commands."""
        if args.detect_cmd == "check":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]

                # Parse methods
                methods = []
                if args.methods:
                    for method in args.methods:
                        try:
                            methods.append(DetectionMethod[method.upper()])
                        except KeyError:
                            print(f"Unknown method: {method}", file=sys.stderr)
                            return 1
                else:
                    methods = [
                        DetectionMethod.Z_SCORE,
                        DetectionMethod.IQR,
                        DetectionMethod.EWMA,
                    ]

                alerts = self.engine.detect_anomalies(
                    args.resource_id, metric_type, args.value, methods
                )

                self.engine.add_metric(args.resource_id, metric_type, args.value)

                if alerts:
                    print(f"[warn] Anomalies detected: {len(alerts)}")
                    for alert in alerts:
                        print(
                            f"  [{alert.severity.value}] {alert.anomaly_type.value}: "
                            f"{alert.message}"
                        )
                        print(f"    Confidence: {alert.confidence:.1%}")
                        print(f"    Expected range: {alert.expected_range}")
                    return 0
                else:
                    print("? No anomalies detected")
                    return 0
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        elif args.detect_cmd == "recent":
            alerts = self.engine.get_alert_history(
                _resource_id=args.resource, hours=args.hours, limit=args.limit
            )

            if alerts:
                _alert_data = [
                    [
                        a.timestamp.isoformat()[:16],
                        a.resource_id,
                        a.metric_type.value,
                        a.anomaly_type.value,
                        a.severity.value,
                        f"{a.confidence:.0%}",
                    ]
                    for a in alerts
                ]

                print(
                    format_table(
                        alert_data,
                        _headers = [
                            "Timestamp",
                            "Resource",
                            "Metric",
                            "Type",
                            "Severity",
                            "Confidence",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No recent detections")
            return 0

        return 1

    def _handle_alert(self, args: argparse.Namespace) -> int:
        """Handle alert commands."""
        if args.alert_cmd == "list":
            _alerts=self.engine.get_active_alerts(resource_id=args.resource)

            # Filter by severity if requested
            if args.severity:
                try:
                    _severity=SeverityLevel[args.severity.upper()]
                    alerts = [a for a in alerts if a.severity == severity]
                except KeyError:
                    print(f"Unknown severity: {args.severity}", file=sys.stderr)
                    return 1

            if alerts:
                _alert_data = [
                    [
                        a.alert_id,
                        a.resource_id,
                        a.metric_type.value,
                        a.anomaly_type.value,
                        a.severity.value,
                        f"{a.confidence:.0%}",
                        f"{a.detected_value:.2f}",
                    ]
                    for a in alerts
                ]

                print(
                    format_table(
                        alert_data,
                        _headers = [
                            "Alert ID",
                            "Resource",
                            "Metric",
                            "Type",
                            "Severity",
                            "Confidence",
                            "Value",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No active alerts")
            return 0

        elif args.alert_cmd == "history":
            alerts = self.engine.get_alert_history(
                _resource_id=args.resource, hours=args.hours, limit=args.limit
            )

            if alerts:
                _alert_data = [
                    [
                        a.timestamp.isoformat()[:16],
                        a.alert_id,
                        a.resource_id,
                        a.metric_type.value,
                        a.severity.value,
                        "?" if a.acknowledged else "",
                    ]
                    for a in alerts
                ]

                print(
                    format_table(
                        alert_data,
                        _headers = [
                            "Timestamp",
                            "Alert ID",
                            "Resource",
                            "Metric",
                            "Severity",
                            "Ack",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No alert history")
            return 0

        elif args.alert_cmd == "acknowledge":
            if self.engine.acknowledge_alert(args.alert_id, args.by, args.notes):
                print(f"? Alert acknowledged: {args.alert_id}")
                return 0
            else:
                print(f"Alert not found: {args.alert_id}", file=sys.stderr)
                return 1

        elif args.alert_cmd == "show":
            for alert in self.engine.alerts:
                if alert.alert_id == args.alert_id:
                    print(f"\nAlert: {alert.alert_id}")
                    print(f"  Timestamp: {alert.timestamp.isoformat()}")
                    print(f"  Resource: {alert.resource_id}")
                    print(f"  Metric: {alert.metric_type.value}")
                    print(f"  Type: {alert.anomaly_type.value}")
                    print(f"  Severity: {alert.severity.value}")
                    print(f"  Confidence: {alert.confidence:.1%}")
                    print(f"  Value: {alert.detected_value:.2f}")
                    print(f"  Expected Range: {alert.expected_range}")
                    print(f"  Method: {alert.detection_method.value}")
                    print(f"  Message: {alert.message}")
                    print(f"  Acknowledged: {'Yes' if alert.acknowledged else 'No'}")
                    if alert.acknowledged:
                        print(f"  Acknowledged by: {alert.acknowledged_by}")
                        _ack_at=alert.acknowledged_at.isoformat() if alert.acknowledged_at else "N/A"
                        print(f"  Acknowledged at: {ack_at}")
                    return 0

            print(f"Alert not found: {args.alert_id}", file=sys.stderr)
            return 1

        return 1

    def _handle_trend(self, args: argparse.Namespace) -> int:
        """Handle trend commands."""
        if args.trend_cmd == "analyze":
            try:
                _metric_type=MetricType[args.metric_type.upper().replace("-", "_")]
                trend = self.engine.analyze_trend(
                    args.resource_id, metric_type, hours=args.hours
                )

                if trend:
                    print(f"\nTrend Analysis: {args.resource_id}/{args.metric_type}")
                    print(f"  Period: {args.hours} hours")
                    print(f"  Direction: {trend.trend_direction}")
                    print(f"  Strength: {trend.trend_strength:.2f}")
                    print(f"  Avg Change/Hour: {trend.average_change_per_hour:.2f}")
                    print(f"  24h Forecast: {trend.forecast_value_24h:.2f}")
                    print(f"  Confidence: {trend.confidence:.1%}")
                    return 0
                else:
                    print("Insufficient data for trend analysis")
                    return 1
            except KeyError:
                print(f"Unknown metric type: {args.metric_type}", file=sys.stderr)
                return 1

        elif args.trend_cmd == "list":
            trend_data = []
            for (resource_id, metric_type), trend in self.engine.trends.items():
                if args.resource and resource_id != args.resource:
                    continue

                trend_data.append(
                    [
                        resource_id,
                        metric_type.value,
                        trend.trend_direction,
                        f"{trend.trend_strength:.2f}",
                        f"{trend.average_change_per_hour:.2f}",
                        f"{trend.confidence:.0%}",
                    ]
                )

            if trend_data:
                print(
                    format_table(
                        trend_data,
                        _headers = [
                            "Resource",
                            "Metric",
                            "Direction",
                            "Strength",
                            "Change/Hour",
                            "Confidence",
                        ],
                        _tablefmt = "grid",
                    )
                )
            else:
                print("No trends found")
            return 0

        return 1

    def _handle_system(self, args: argparse.Namespace) -> int:
        """Handle system commands."""
        if args.system_cmd == "stats":
            _stats=self.engine.get_statistics()
            print("\nAnomaly Detection System Statistics")
            print(f"  Total Metrics: {stats['total_metrics']}")
            print(f"  Total Baselines: {stats['total_baselines']}")
            print(f"  Total Alerts: {stats['total_alerts']}")
            print(f"  Active Alerts: {stats['active_alerts']}")
            print(f"    Critical: {stats['critical_alerts']}")
            print(f"    Warning: {stats['warning_alerts']}")
            print(f"  Trends Analyzed: {stats['trends_analyzed']}")
            print(f"  Alert Ack Rate: {stats['alert_ack_rate']:.1%}")
            return 0

        elif args.system_cmd == "config":
            print("\nAnomaly Detection Configuration")
            print(f"  Config Dir: {self.engine.config.config_dir}")
            print(f"  Baseline Window: {self.engine.baseline_window} seconds")
            print(f"  Z-Score Threshold: {self.engine.z_score_threshold}")
            print(f"  Confidence Threshold: {self.engine.confidence_threshold:.1%}")
            print(f"  Max History: {self.engine.max_history} points/metric")
            return 0

        elif args.system_cmd == "export":
            if args.type == "alerts":
                alerts = self.engine.alerts
                if args.resource:
                    alerts = [a for a in alerts if a.resource_id == args.resource]

                _data=[a.to_dict() for a in alerts]
            elif args.type == "baselines":
                baselines = self.engine.baselines
                if args.resource:
                    baselines = {
                        k: v for k, v in baselines.items() if k[0] == args.resource
                    }

                _data=[b.to_dict() for b in baselines.values()]
            else:
                print(f"Unknown export type: {args.type}", file=sys.stderr)
                return 1

            try:
                with open(args.output, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"? Exported {len(data)} items to {args.output}")
                return 0
            except Exception as e:
                print(f"Export failed: {e}", file=sys.stderr)
                return 1

        return 1


def main() -> int:
    """Main entry point."""
    _engine=get_anomaly_engine()
    _cli=AnomalyCLI(engine)
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
