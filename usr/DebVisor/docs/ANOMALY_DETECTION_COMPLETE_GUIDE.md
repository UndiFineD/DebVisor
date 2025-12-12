# Anomaly Detection System - Complete Guide

## Overview

The DebVisor Anomaly Detection System is a comprehensive monitoring and alerting framework designed to identify irregularities in system performance and resource usage. It utilizes a multi-layered approach combining statistical methods and machine learning to provide accurate, actionable insights with minimal false positives.

## Core Features

- **Multi-Method Detection**: Combines Z-Score, IQR, EWMA, and LSTM neural networks.
- **Automatic Baselines**: Self-learning baselines that adapt to system behavior over time.
- **Trend Analysis**: Linear regression for forecasting and trend direction identification.
- **Confidence Scoring**: Every alert includes a confidence score (0-100%) to help prioritize responses.
- **Severity Classification**: INFO, WARNING, and CRITICAL levels based on deviation magnitude and confidence.

## Detection Methods

### 1. Z-Score (Standard Deviation)

- **Best for**: Normally distributed data (e.g., steady memory usage).
- **Mechanism**: Measures how many standard deviations a data point is from the mean.
- **Threshold**: Default > 3.0 sigma.

### 2. Interquartile Range (IQR)

- **Best for**: Non-normal distributions and filtering outliers.
- **Mechanism**: Uses the 25th and 75th percentiles to define a "normal" range.
- **Robustness**: Highly resistant to extreme outliers affecting the baseline.

### 3. Exponential Weighted Moving Average (EWMA)

- **Best for**: Detecting sudden shifts in trends or noisy data.
- **Mechanism**: Gives more weight to recent data points, allowing it to react faster to changes than simple averages.

### 4. LSTM Neural Networks (New in Phase 12)

- **Best for**: Complex, non-linear patterns and time-series prediction.
- **Mechanism**: A Recurrent Neural Network (RNN) that learns temporal dependencies.
- **Usage**: Predicts the *next* expected value based on a sequence of previous values. If the actual value deviates significantly from the prediction, an anomaly is flagged.
- **Training**: Models are trained online using historical metric data.

## Supported Metrics

The system monitors the following metric types:

- `cpu_usage`: CPU utilization percentage.
- `memory_usage`: RAM usage percentage.
- `disk_io`: Disk read/write operations.
- `network_io`: Network throughput.
- `disk_usage`: Storage capacity usage.
- `temperature`: System temperature sensors.
- `latency`: Service response times.
- `error_rate`: Application or system error counts.

## Configuration

Configuration is managed via `/etc/debvisor/anomaly/`.

### Key Parameters

- `baseline_window`: 7 days (default).
- `z_score_threshold`: 3.0.
- `confidence_threshold`: 0.65.
- `max_history`: 10,000 data points per metric.

## Alerting

Alerts are generated with the following structure:

- **ID**: Unique UUID.
- **Severity**: INFO, WARNING, CRITICAL.
- **Type**: SPIKE, DIP, TREND, SEASONAL, OUTLIER.
- **Message**: Human-readable description.
- **Details**: Technical context (e.g., Z-score value, expected range).

## Integration

The anomaly detection engine is integrated into the DebVisor RPC service and Web Panel.

- **RPC**: `GetAnomalies` endpoint.
- **Web Panel**: "Analytics" dashboard widget.

## Troubleshooting

- *Logs**: `/var/log/DebVisor/anomaly.log` (or configured path).

- *Common Issues**:

- *Insufficient Data*: Baselines require at least 10 data points. LSTM requires 50+.
- *False Positives*: Adjust `z_score_threshold` or `confidence_threshold` in config.
