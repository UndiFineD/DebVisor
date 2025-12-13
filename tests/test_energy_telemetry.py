"""
Tests for Energy Telemetry.
"""
import pytest
from unittest.mock import patch, mock_open
from opt.services.observability.energy import EnergyMonitor


@pytest.fixture


def monitor() -> EnergyMonitor:
    return EnergyMonitor()


def test_get_metrics_defaults(monitor):
    # Test with no sensors (default mock values)
    metrics = monitor.get_metrics()
    assert metrics.power_watts == 45.0
    assert metrics.temperature_celsius == 35.0
    assert metrics.estimated_carbon_emission_g > 0


@patch("glob.glob")
@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")


def test_read_temperature_success(mock_exists, mock_file, mock_glob, monitor):
    mock_exists.return_value = True
    mock_glob.return_value = ["/sys/class/thermal/thermal_zone0"]

    # Mock file reads: first for 'type', second for 'temp'
    # We need to handle multiple calls to open
    handlers = (
        mock_open(read_data="x86_pkg_temp").return_value,
        mock_open(read_data="45000").return_value,
    )
    mock_file.side_effect = handlers

    temp = monitor._read_temperature()
    assert temp == 45.0


@patch("os.path.exists")


def test_read_temperature_no_path(mock_exists, monitor):
    mock_exists.return_value = False
    temp = monitor._read_temperature()
    assert temp == 35.0    # Default fallback
