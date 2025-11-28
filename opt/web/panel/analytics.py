"""
Advanced Analytics Engine for DebVisor Web Panel

Provides:
- Real-time metrics aggregation
- Custom analytics queries
- Forecasting and trend analysis
- Performance dashboards
- Historical data analysis
- Alert-driven analytics

Features:
- Multi-dimensional data aggregation
- Time-series data analysis
- Anomaly detection
- Performance trending
- Predictive analytics
- Custom report generation
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)


class TimeGranularity(Enum):
    """Time series data granularity."""
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class MetricType(Enum):
    """Types of metrics available for analytics."""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    QUERY_LATENCY = "query_latency"
    RPC_CALLS = "rpc_calls"
    ERRORS = "errors"
    ALERTS = "alerts"
    CONNECTIONS = "connections"
    THROUGHPUT = "throughput"


@dataclass
class DataPoint:
    """Single metric data point."""
    timestamp: datetime
    value: float
    metric_type: str
    resource_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AggregatedMetrics:
    """Aggregated metrics over time period."""
    metric_type: str
    start_time: datetime
    end_time: datetime
    granularity: TimeGranularity
    values: List[Tuple[datetime, float]]
    
    @property
    def min_value(self) -> float:
        """Get minimum value."""
        return min((v[1] for v in self.values), default=0.0)
    
    @property
    def max_value(self) -> float:
        """Get maximum value."""
        return max((v[1] for v in self.values), default=0.0)
    
    @property
    def avg_value(self) -> float:
        """Get average value."""
        if not self.values:
            return 0.0
        return statistics.mean([v[1] for v in self.values])
    
    @property
    def median_value(self) -> float:
        """Get median value."""
        if not self.values:
            return 0.0
        sorted_vals = sorted([v[1] for v in self.values])
        return statistics.median(sorted_vals)
    
    @property
    def stddev(self) -> float:
        """Get standard deviation."""
        if len(self.values) < 2:
            return 0.0
        vals = [v[1] for v in self.values]
        return statistics.stdev(vals)


class AnalyticsEngine:
    """
    Advanced analytics engine for metric analysis and reporting.
    
    Capabilities:
    - Real-time metric aggregation
    - Historical data analysis
    - Trend detection
    - Anomaly detection
    - Performance forecasting
    """
    
    def __init__(self, retention_days: int = 90):
        """
        Initialize analytics engine.
        
        Args:
            retention_days: How long to retain historical data
        """
        self.retention_days = retention_days
        self.data_points: Dict[str, List[DataPoint]] = defaultdict(list)
        self.aggregated_cache: Dict[str, AggregatedMetrics] = {}
        self.anomalies: List[Dict[str, Any]] = []

    def record_metric(
        self,
        metric_type: str,
        value: float,
        resource_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record a metric data point.
        
        Args:
            metric_type: Type of metric (CPU_USAGE, etc.)
            value: Metric value
            resource_id: Optional resource identifier
            tags: Optional metadata tags
            timestamp: Data point timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        key = f"{metric_type}:{resource_id or 'global'}"
        data_point = DataPoint(
            timestamp=timestamp,
            value=value,
            metric_type=metric_type,
            resource_id=resource_id,
            tags=tags or {}
        )
        
        self.data_points[key].append(data_point)
        
        # Clean up old data
        self._cleanup_old_data(key)

    def aggregate_metrics(
        self,
        metric_type: str,
        start_time: datetime,
        end_time: datetime,
        granularity: TimeGranularity = TimeGranularity.HOUR,
        resource_id: Optional[str] = None
    ) -> AggregatedMetrics:
        """
        Aggregate metrics over time period.
        
        Args:
            metric_type: Type of metric
            start_time: Start of time range
            end_time: End of time range
            granularity: Time granularity for aggregation
            resource_id: Optional resource filter
            
        Returns:
            AggregatedMetrics object
        """
        key = f"{metric_type}:{resource_id or 'global'}"
        
        # Get relevant data points
        points = [
            p for p in self.data_points[key]
            if start_time <= p.timestamp <= end_time
        ]
        
        if not points:
            return AggregatedMetrics(
                metric_type=metric_type,
                start_time=start_time,
                end_time=end_time,
                granularity=granularity,
                values=[]
            )
        
        # Bucket data by granularity
        buckets = self._bucket_by_granularity(points, granularity)
        
        # Average values in each bucket
        aggregated_values = [
            (timestamp, statistics.mean([p.value for p in bucket_points]))
            for timestamp, bucket_points in sorted(buckets.items())
        ]
        
        return AggregatedMetrics(
            metric_type=metric_type,
            start_time=start_time,
            end_time=end_time,
            granularity=granularity,
            values=aggregated_values
        )

    def detect_anomalies(
        self,
        metric_type: str,
        threshold_stddevs: float = 2.0,
        resource_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in metric data.
        
        Uses statistical analysis to find outliers.
        
        Args:
            metric_type: Type of metric
            threshold_stddevs: Number of standard deviations for anomaly
            resource_id: Optional resource filter
            
        Returns:
            List of detected anomalies
        """
        key = f"{metric_type}:{resource_id or 'global'}"
        points = self.data_points[key]
        
        if len(points) < 3:
            return []
        
        values = [p.value for p in points]
        mean = statistics.mean(values)
        stddev = statistics.stdev(values)
        
        anomalies = []
        for point in points:
            z_score = abs((point.value - mean) / stddev) if stddev > 0 else 0
            
            if z_score > threshold_stddevs:
                anomalies.append({
                    'timestamp': point.timestamp.isoformat(),
                    'value': point.value,
                    'z_score': z_score,
                    'severity': 'high' if z_score > 3 else 'medium',
                    'metric_type': metric_type,
                    'resource_id': resource_id,
                })
        
        return anomalies

    def calculate_trend(
        self,
        metric_type: str,
        time_window: timedelta = timedelta(days=7),
        resource_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate trend for metric over time window.
        
        Args:
            metric_type: Type of metric
            time_window: Time window for trend calculation
            resource_id: Optional resource filter
            
        Returns:
            Trend analysis results
        """
        now = datetime.now(timezone.utc)
        start_time = now - time_window
        
        metrics = self.aggregate_metrics(
            metric_type,
            start_time,
            now,
            TimeGranularity.DAY,
            resource_id
        )
        
        if len(metrics.values) < 2:
            return {
                'trend': 'insufficient_data',
                'direction': None,
                'slope': 0.0,
            }
        
        # Linear regression for trend
        x = list(range(len(metrics.values)))
        y = [v[1] for v in metrics.values]
        
        slope = self._calculate_slope(x, y)
        
        return {
            'trend': 'up' if slope > 0 else 'down' if slope < 0 else 'stable',
            'direction': slope,
            'slope': slope,
            'current_value': metrics.values[-1][1],
            'previous_value': metrics.values[0][1],
            'change_percent': (
                ((metrics.values[-1][1] - metrics.values[0][1]) / metrics.values[0][1] * 100)
                if metrics.values[0][1] != 0 else 0
            ),
        }

    def forecast_metric(
        self,
        metric_type: str,
        periods_ahead: int = 7,
        resource_id: Optional[str] = None
    ) -> List[Tuple[datetime, float]]:
        """
        Forecast metric values using simple exponential smoothing.
        
        Args:
            metric_type: Type of metric
            periods_ahead: Number of periods to forecast
            resource_id: Optional resource filter
            
        Returns:
            List of (timestamp, predicted_value) tuples
        """
        key = f"{metric_type}:{resource_id or 'global'}"
        points = sorted(self.data_points[key], key=lambda p: p.timestamp)
        
        if len(points) < 2:
            return []
        
        # Simple exponential smoothing with alpha=0.3
        alpha = 0.3
        values = [p.value for p in points]
        
        # Initialize smoothing
        smoothed = values[0]
        smoothed_values = [smoothed]
        
        for value in values[1:]:
            smoothed = alpha * value + (1 - alpha) * smoothed
            smoothed_values.append(smoothed)
        
        # Forecast
        last_timestamp = points[-1].timestamp
        last_value = smoothed_values[-1]
        forecast = []
        
        for i in range(1, periods_ahead + 1):
            timestamp = last_timestamp + timedelta(days=i)
            # Simple linear extrapolation
            predicted_value = last_value
            forecast.append((timestamp, predicted_value))
        
        return forecast

    def get_dashboard_summary(
        self,
        time_window: timedelta = timedelta(hours=24)
    ) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            Dashboard summary with all key metrics
        """
        now = datetime.now(timezone.utc)
        start_time = now - time_window
        
        summary = {
            'timestamp': now.isoformat(),
            'time_window_hours': time_window.total_seconds() / 3600,
            'metrics': {},
            'anomalies': [],
            'trends': {},
        }
        
        # Analyze each metric type
        for metric_type in [m.value for m in MetricType]:
            # Get aggregated metrics
            metrics = self.aggregate_metrics(
                metric_type, start_time, now
            )
            
            summary['metrics'][metric_type] = {
                'current': metrics.values[-1][1] if metrics.values else 0,
                'min': metrics.min_value,
                'max': metrics.max_value,
                'avg': metrics.avg_value,
                'median': metrics.median_value,
                'stddev': metrics.stddev,
            }
            
            # Detect anomalies
            anomalies = self.detect_anomalies(metric_type)
            if anomalies:
                summary['anomalies'].extend(anomalies)
            
            # Calculate trend
            summary['trends'][metric_type] = self.calculate_trend(metric_type)
        
        return summary

    def _bucket_by_granularity(
        self,
        points: List[DataPoint],
        granularity: TimeGranularity
    ) -> Dict[datetime, List[DataPoint]]:
        """Bucket data points by time granularity."""
        buckets = defaultdict(list)
        
        for point in points:
            if granularity == TimeGranularity.MINUTE:
                bucket_time = point.timestamp.replace(second=0, microsecond=0)
            elif granularity == TimeGranularity.HOUR:
                bucket_time = point.timestamp.replace(minute=0, second=0, microsecond=0)
            elif granularity == TimeGranularity.DAY:
                bucket_time = point.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                bucket_time = point.timestamp
            
            buckets[bucket_time].append(point)
        
        return buckets

    def _calculate_slope(self, x: List[int], y: List[float]) -> float:
        """Calculate linear regression slope."""
        if len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def _cleanup_old_data(self, key: str) -> None:
        """Remove data older than retention period."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        self.data_points[key] = [
            p for p in self.data_points[key]
            if p.timestamp > cutoff_time
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        total_points = sum(len(points) for points in self.data_points.values())
        metric_types = len(set(p.metric_type for points in self.data_points.values() for p in points))
        
        return {
            'total_data_points': total_points,
            'metric_types': metric_types,
            'datasets': len(self.data_points),
            'anomalies_detected': len(self.anomalies),
            'retention_days': self.retention_days,
        }

