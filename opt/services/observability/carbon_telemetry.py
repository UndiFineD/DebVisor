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

# !/usr/bin/env python3


"""
Carbon & Energy Telemetry for DebVisor.

Provides comprehensive energy and carbon footprint monitoring:
- Power consumption tracking (CPU, RAM, disk, network, GPU)
- Thermal metrics collection
- Carbon intensity calculations
- Energy efficiency recommendations
- Green computing metrics and reporting
- Integration with energy grid carbon intensity APIs

Author: DebVisor Team
Date: December 11, 2025
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json

_logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================
class PowerSource(Enum):
    """Power source types."""
    AC_GRID = "ac_grid"
    BATTERY = "battery"
    SOLAR = "solar"
    WIND = "wind"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class ComponentType(Enum):
    """Hardware component types for power tracking."""
    CPU = "cpu"
    RAM = "ram"
    DISK = "disk"
    GPU = "gpu"
    NETWORK = "network"
    COOLING = "cooling"
    MOTHERBOARD = "motherboard"
    PSU = "psu"


class EnergyEfficiencyRating(Enum):
    """Energy efficiency ratings."""
    EXCELLENT = "excellent"  # < 50W avg
    GOOD = "good"  # 50-100W
    MODERATE = "moderate"  # 100-200W
    POOR = "poor"  # 200-300W
    CRITICAL = "critical"  # > 300W


# =============================================================================
# Data Models
# =============================================================================


@dataclass


class PowerMetrics:
    """Power consumption metrics for a component or system."""
    component_type: ComponentType
    component_id: str
    timestamp: datetime
    power_watts: float
    voltage_volts: Optional[float] = None
    current_amperes: Optional[float] = None
    temperature_celsius: Optional[float] = None
    utilization_percent: Optional[float] = None
    power_source: PowerSource = PowerSource.AC_GRID


@dataclass


class ThermalMetrics:
    """Thermal metrics for system components."""
    sensor_id: str
    sensor_location: str  # e.g., "CPU Package", "GPU Core", "System"
    timestamp: datetime
    temperature_celsius: float
    critical_temp: float = 100.0
    warning_temp: float = 80.0
    fan_rpm: Optional[int] = None
    fan_duty_percent: Optional[int] = None


@dataclass


class CarbonIntensity:
    """Carbon intensity data for energy grid."""
    region: str  # e.g., "US-CA", "EU-DE", "GB"
    timestamp: datetime
    grams_co2_per_kwh: float
    source: str  # e.g., "electricitymap", "carbonintensity.org.uk"
    forecast_available: bool = False


@dataclass


class EnergyConsumption:
    """Aggregated energy consumption over a time period."""
    start_time: datetime
    end_time: datetime
    duration_hours: float
    total_energy_kwh: float
    average_power_watts: float
    peak_power_watts: float
    component_breakdown: Dict[ComponentType, float] = field(default_factory=dict)


@dataclass


class CarbonFootprint:
    """Carbon footprint calculation results."""
    start_time: datetime
    end_time: datetime
    energy_kwh: float
    carbon_intensity_avg: float  # grams CO2/kWh
    total_carbon_kg: float
    equivalent_km_driven: float  # Car equivalent
    equivalent_trees: float  # Trees needed to offset
    component_breakdown: Dict[ComponentType, float] = field(default_factory=dict)


@dataclass


class EnergyRecommendation:
    """Energy efficiency recommendation."""
    recommendation_id: str
    category: str  # "cpu", "cooling", "scheduling", "hardware"
    title: str
    description: str
    estimated_savings_watts: float
    estimated_savings_percent: float
    implementation_effort: str  # "low", "medium", "high"
    priority: str  # "low", "medium", "high", "critical"


# =============================================================================
# Power Monitoring
# =============================================================================
class PowerMonitor:
    """
    Monitors power consumption from various sources.

    Integrates with:
    - IPMI (for server power metrics)
    - sysfs (/sys/class/power_supply, /sys/class/hwmon)
    - Intel RAPL (Running Average Power Limit)
    - NVIDIA SMI (for GPU power)
    - BMC/iDRAC/iLO (for comprehensive datacenter power)
    """

    def __init__(self):
        self.metrics_history: List[PowerMetrics] = []
        self.thermal_history: List[ThermalMetrics] = []
        self.collection_interval: int = 60  #
        self.max_history_hours: int = 24  # retain 24 hours of history

    def _prune_history(self) -> None:
        """Remove metrics older than max_history_hours."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.max_history_hours)
        self.metrics_history = [m for m in self.metrics_history if m.timestamp > cutoff]
        self.thermal_history = [m for m in self.thermal_history if m.timestamp > cutoff]

    async def collect_power_metrics(self) -> List[PowerMetrics]:
        """Collect current power metrics from all components."""
        metrics = []
        timestamp = datetime.now(timezone.utc)

        # CPU power
        cpu_power = await self._read_cpu_power()
        if cpu_power:
            metrics.append(PowerMetrics(
                _component_type = ComponentType.CPU,
                _component_id = "cpu0",
                _timestamp = timestamp,
                _power_watts = cpu_power["power"],
                _temperature_celsius = cpu_power.get("temperature"),
                _utilization_percent = cpu_power.get("utilization"),
            ))

        # RAM power (estimated)
        ram_power = await self._estimate_ram_power()
        if ram_power:
            metrics.append(PowerMetrics(
                _component_type = ComponentType.RAM,
                _component_id = "ram0",
                _timestamp = timestamp,
                _power_watts = ram_power,
            ))

        # Disk power
        disk_metrics = await self._read_disk_power()
        for disk_id, disk_power in disk_metrics.items():
            metrics.append(PowerMetrics(
                _component_type = ComponentType.DISK,
                _component_id = disk_id,
                _timestamp = timestamp,
                _power_watts = disk_power,
            ))

        # GPU power
        gpu_metrics = await self._read_gpu_power()
        for gpu_id, gpu_data in gpu_metrics.items():
            metrics.append(PowerMetrics(
                _component_type = ComponentType.GPU,
                _component_id = gpu_id,
                _timestamp = timestamp,
                _power_watts = gpu_data["power"],
                _temperature_celsius = gpu_data.get("temperature"),
                _utilization_percent = gpu_data.get("utilization"),
            ))

        self.metrics_history.extend(metrics)
        return metrics

    async def _read_cpu_power(self) -> Optional[Dict[str, Any]]:
        """Read CPU power using Intel RAPL or similar."""
        try:
        # Try Intel RAPL first
            rapl_path = Path("/sys/class/powercap/intel-rapl/intel-rapl:0")
            if rapl_path.exists():
                energy_uj_file = rapl_path / "energy_uj"
                if energy_uj_file.exists():
                # Read energy in microjoules and compute delta
                    if not hasattr(self, '_last_rapl_reading'):
                        self._last_rapl_reading = None
                        self._last_rapl_time = None

                    energy_uj = int(energy_uj_file.read_text().strip())
                    current_time = datetime.now(timezone.utc)

                    if self._last_rapl_reading is not None and self._last_rapl_time is not None:
                        delta_energy_uj = energy_uj - self._last_rapl_reading
                        delta_time_s = (current_time - self._last_rapl_time).total_seconds()
                        if delta_time_s > 0:
                            power_watts = (delta_energy_uj / 1_000_000) / delta_time_s
                        else:
                            power_watts = 45.0  # fallback
                    else:
                        power_watts = 45.0  # first reading, use fallback

                    self._last_rapl_reading = energy_uj
                    self._last_rapl_time = current_time

                    return {
                        "power": power_watts,
                        "temperature": await self._read_cpu_temp(),
                        "utilization": await self._read_cpu_utilization(),
                    }

            # Fallback to estimation based on utilization
            utilization = await self._read_cpu_utilization()
            if utilization is not None:
            # Estimate: 65W TDP * utilization
                estimated_power = 65.0 * (utilization / 100.0)
                return {
                    "power": estimated_power,
                    "temperature": await self._read_cpu_temp(),
                    "utilization": utilization,
                }

        except Exception as e:
            logger.debug(f"Error reading CPU power: {e}")

        return None
    async def _read_cpu_temp(self) -> Optional[float]:
        """Read CPU temperature."""
        try:
        # Try common temperature sensors
            temp_paths = [
                "/sys/class/thermal/thermal_zone0/temp",
                "/sys/class/hwmon/hwmon0/temp1_input",
            ]

            for temp_path in temp_paths:
                if Path(temp_path).exists():
                    temp_millicelsius = int(Path(temp_path).read_text().strip())
                    return temp_millicelsius / 1000.0
        except Exception as e:
            logger.debug(f"Error reading CPU temperature: {e}")

        return None

    async def _read_cpu_utilization(self) -> Optional[float]:
        """Read CPU utilization percentage."""
        try:
        # Use psutil if available
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
        # Fallback to /proc/stat parsing
            pass
        except Exception as e:
            logger.debug(f"Error reading CPU utilization: {e}")

        return None

    async def _estimate_ram_power(self) -> Optional[float]:
        """Estimate RAM power consumption."""
        try:
            import psutil
            mem = psutil.virtual_memory()
            # Typical DDR4: ~3W per 8GB stick
            total_gb = mem.total / (1024 ** 3)
            estimated_power = (total_gb / 8.0) * 3.0
            return estimated_power
        except Exception as e:
            logger.debug(f"Error estimating RAM power: {e}")

        return None

    async def _read_disk_power(self) -> Dict[str, float]:
        """Read disk power consumption."""
        # Typical values:
            # SSD: 2-5W active, 0.5W idle
        # HDD: 6-10W active, 2W idle

        try:
            import psutil
            disk_metrics = {}

            for disk in psutil.disk_partitions():
            # Estimate based on disk type (simplified)
                if "ssd" in disk.device.lower() or "nvme" in disk.device.lower():
                    disk_metrics[disk.device] = 3.5  # SSD average
                else:
                    disk_metrics[disk.device] = 8.0  # HDD average

            return disk_metrics
        except Exception as e:
            logger.debug(f"Error reading disk power: {e}")

        return {}

    async def _read_gpu_power(self) -> Dict[str, Dict[str, Any]]:
        """Read GPU power using nvidia-smi or similar."""
        _gpu_metrics = {}

        try:
        # Try nvidia-smi
            import subprocess
            _result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=index,power.draw,temperature.gpu,utilization.gpu",
                    "--format=csv,noheader,nounits"
                ],
                _capture_output = True,
                _text = True,
                _timeout = 5,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        parts = [p.strip() for p in line.split(",")]
                        if len(parts) >= 4:
                            gpu_id = f"gpu{parts[0]}"
                            gpu_metrics[gpu_id] = {
                                "power": float(parts[1]),
                                "temperature": float(parts[2]),
                                "utilization": float(parts[3]),
                            }
        except Exception as e:
            logger.debug(f"Error reading GPU power: {e}")

        return gpu_metrics

    async def collect_thermal_metrics(self) -> List[ThermalMetrics]:
        """Collect thermal metrics from system sensors."""
        _metrics = []
        _timestamp = datetime.now(timezone.utc)

        try:
        # Read from hwmon
            hwmon_path = Path("/sys/class/hwmon")
            if hwmon_path.exists():
                for hwmon_dir in hwmon_path.iterdir():
                    name_file = hwmon_dir / "name"
                    if name_file.exists():
                        sensor_name = name_file.read_text().strip()

                        # Find temperature inputs
                        for temp_file in hwmon_dir.glob("temp*_input"):
                            try:
                                temp_millicelsius = int(temp_file.read_text().strip())
                                temp_celsius = temp_millicelsius / 1000.0

                                metric = ThermalMetrics(
                                    _sensor_id = f"{sensor_name}_{temp_file.stem}",
                                    _sensor_location = sensor_name,
                                    _timestamp = timestamp,
                                    _temperature_celsius = temp_celsius,
                                )

                                metrics.append(metric)
                            except Exception:
                                pass
        except Exception as e:
            logger.debug(f"Error collecting thermal metrics: {e}")

        self.thermal_history.extend(metrics)
        return metrics

    def get_total_power(self, metrics: List[PowerMetrics]) -> float:
        """Calculate total power consumption from metrics."""
        return sum(m.power_watts for m in metrics)

    def get_component_power(
        self,
        metrics: List[PowerMetrics],
        component_type: ComponentType
    ) -> float:
        """Get total power for a specific component type."""
        return sum(
            m.power_watts for m in metrics
            if m.component_type == component_type
        )


# =============================================================================
# Carbon Intensity Service
# =============================================================================
class CarbonIntensityService:
    """
    Fetches carbon intensity data from various sources.

    Supports:
    - ElectricityMap API (global coverage)
    - UK Carbon Intensity API
    - US EIA data
    - Custom regional data
    """

    def __init__(self, region: str = "US-CA"):
        self.region = region
        self.cache: Optional[CarbonIntensity] = None
        self.cache_duration = timedelta(hours=1)

    async def get_carbon_intensity(self) -> CarbonIntensity:
        """Get current carbon intensity for the region."""
        # Check cache
        if self.cache and datetime.now(timezone.utc) - self.cache.timestamp < self.cache_duration:
            return self.cache

        # Try to fetch from API
        intensity = await self._fetch_from_api()

        if intensity:
            self.cache = intensity
            return intensity

        # Fallback to regional averages
        return self._get_regional_average()

    async def _fetch_from_api(self) -> Optional[CarbonIntensity]:
        """Fetch carbon intensity from external API."""
        # In production, this would make HTTP requests to carbon intensity APIs
        # For now, return None to use regional averages
        return None

    def _get_regional_average(self) -> CarbonIntensity:
        """Get regional average carbon intensity."""
        # Regional averages in grams CO2/kWh
        _regional_data = {
            "US-CA": 200,  # California (lots of renewables)
            "US-TX": 450,  # Texas (gas/coal heavy)
            "US-NY": 250,  # New York
            "EU-DE": 350,  # Germany
            "EU-FR": 50,   # France (nuclear)
            "GB": 250,     # United Kingdom
            "CN": 600,     # China (coal heavy)
            "IN": 650,     # India
            "AU": 550,     # Australia
            "GLOBAL": 475, # Global average
        }

        intensity = regional_data.get(self.region, regional_data["GLOBAL"])

        return CarbonIntensity(
            region=self.region,
            _timestamp = datetime.now(timezone.utc),
            _grams_co2_per_kwh = intensity,
            _source = "regional_average",
        )


# =============================================================================
# Carbon Footprint Calculator
# =============================================================================
class CarbonFootprintCalculator:
    """
    Calculates carbon footprint from energy consumption.
    """

    def __init__(self, carbon_service: CarbonIntensityService):
        self.carbon_service = carbon_service

    async def calculate_footprint(
        self,
        energy: EnergyConsumption
    ) -> CarbonFootprint:
        """Calculate carbon footprint for energy consumption."""
        # Get carbon intensity
        intensity = await self.carbon_service.get_carbon_intensity()

        # Calculate total carbon
        total_carbon_grams = energy.total_energy_kwh * intensity.grams_co2_per_kwh
        total_carbon_kg = total_carbon_grams / 1000.0

        # Average car emits ~120g CO2/km
        _equivalent_km_driven = total_carbon_grams / 120.0

        # Average tree absorbs ~21kg CO2/year
        equivalent_trees = total_carbon_kg / 21.0

        return CarbonFootprint(
            _start_time = energy.start_time,
            _end_time = energy.end_time,
            energy_kwh=energy.total_energy_kwh,
            _carbon_intensity_avg = intensity.grams_co2_per_kwh,
            _total_carbon_kg = total_carbon_kg,
            _equivalent_km_driven = equivalent_km_driven,
            _equivalent_trees = equivalent_trees,
            component_breakdown={
                comp_type: (energy_kwh / 1000.0) * intensity.grams_co2_per_kwh
                for comp_type, energy_kwh in energy.component_breakdown.items()
            },
        )

    def calculate_energy_consumption(
        self,
        metrics: List[PowerMetrics],
        start_time: datetime,
        end_time: datetime
    ) -> EnergyConsumption:
        """Calculate energy consumption from power metrics."""
        if not metrics:
            return EnergyConsumption(
                _start_time = start_time,
                _end_time = end_time,
                _duration_hours = 0,
                _total_energy_kwh = 0,
                _average_power_watts = 0,
                _peak_power_watts = 0,
            )

        # Filter metrics by time range
        metrics_in_range = [
            m for m in metrics
            if start_time <= m.timestamp <= end_time
        ]

        if not metrics_in_range:
            return EnergyConsumption(
                start_time=start_time,
                end_time=end_time,
                duration_hours=0,
                _total_energy_kwh = 0,
                _average_power_watts = 0,
                _peak_power_watts = 0,
            )

        # Calculate duration
        duration = end_time - start_time
        _duration_hours = duration.total_seconds() / 3600.0

        # Group metrics by timestamp and sum component power per timestamp
        timestamp_power: Dict[datetime, float] = {}
        for m in metrics_in_range:
            if m.timestamp not in timestamp_power:
                timestamp_power[m.timestamp] = 0.0
            timestamp_power[m.timestamp] += m.power_watts

        # Get per-timestamp system power values
        system_power_samples = list(timestamp_power.values())

        if not system_power_samples:
            return EnergyConsumption(
                _start_time = start_time,
                _end_time = end_time,
                _duration_hours = 0,
                _total_energy_kwh = 0,
                _average_power_watts = 0,
                _peak_power_watts = 0,
            )

        # Calculate average power from per-timestamp system power
        average_power = sum(system_power_samples) / len(system_power_samples)

        # Calculate peak power from per-timestamp system power
        _peak_power = max(system_power_samples)

        # Calculate total energy (kWh)
        _total_energy_kwh = (average_power * duration_hours) / 1000.0

        # Component breakdown
        component_breakdown = {}
        for comp_type in ComponentType:
            comp_metrics = [m for m in metrics_in_range if m.component_type == comp_type]
            if comp_metrics:
                comp_avg_power = sum(m.power_watts for m in comp_metrics) / len(comp_metrics)
                comp_energy_kwh = (comp_avg_power * duration_hours) / 1000.0
                component_breakdown[comp_type] = comp_energy_kwh

        return EnergyConsumption(
            _start_time = start_time,
            _end_time = end_time,
            _duration_hours = duration_hours,
            _total_energy_kwh = total_energy_kwh,
            _average_power_watts = average_power,
            _peak_power_watts = peak_power,
            _component_breakdown = component_breakdown,
        )


# =============================================================================
# Energy Efficiency Analyzer
# =============================================================================
class EnergyEfficiencyAnalyzer:
    """
    Analyzes energy efficiency and provides recommendations.
    """

    def __init__(self):
        self.recommendations: List[EnergyRecommendation] = []

    def analyze_efficiency(
        self,
        metrics: List[PowerMetrics],
        thermal_metrics: List[ThermalMetrics]
    ) -> Tuple[EnergyEfficiencyRating, List[EnergyRecommendation]]:
        """Analyze system energy efficiency."""
        if not metrics:
            return EnergyEfficiencyRating.MODERATE, []

        # Calculate average power
        avg_power = sum(m.power_watts for m in metrics) / len(metrics)

        # Determine rating
        if avg_power < 50:
            rating = EnergyEfficiencyRating.EXCELLENT
        elif avg_power < 100:
            rating = EnergyEfficiencyRating.GOOD
        elif avg_power < 200:
            rating = EnergyEfficiencyRating.MODERATE
        elif avg_power < 300:
            rating = EnergyEfficiencyRating.POOR
        else:
            _rating = EnergyEfficiencyRating.CRITICAL

        # Generate recommendations
        _recommendations = []

        # Check CPU power
        cpu_metrics = [m for m in metrics if m.component_type == ComponentType.CPU]
        if cpu_metrics:
            avg_cpu_power = sum(m.power_watts for m in cpu_metrics) / len(cpu_metrics)
            avg_cpu_util = sum(
                m.utilization_percent for m in cpu_metrics if m.utilization_percent
            ) / max(len([m for m in cpu_metrics if m.utilization_percent]), 1)

            if avg_cpu_power > 50 and avg_cpu_util < 30:
                recommendations.append(EnergyRecommendation(
                    _recommendation_id = "rec-cpu-idle",
                    _category = "cpu",
                    _title = "High CPU power with low utilization",
                    _description = (
                        f"CPU consuming {avg_cpu_power:.1f}W but only "
                        f"{avg_cpu_util:.1f}% utilized. Consider enabling "
                        "power-saving features or consolidating workloads."
                    ),
                    _estimated_savings_watts = avg_cpu_power * 0.3,
                    _estimated_savings_percent = 30,
                    _implementation_effort = "low",
                    _priority = "medium",
                ))

        # Check thermal efficiency
        if thermal_metrics:
            avg_temp = sum(m.temperature_celsius for m in thermal_metrics) / len(thermal_metrics)

            if avg_temp > 70:
                recommendations.append(EnergyRecommendation(
                    _recommendation_id = "rec-cooling",
                    _category = "cooling",
                    _title = "High operating temperatures",
                    _description = (
                        f"Average temperature {avg_temp:.1f}°C. "
                        "Improve cooling to reduce power consumption."
                    ),
                    _estimated_savings_watts = 20,
                    _estimated_savings_percent = 10,
                    _implementation_effort = "medium",
                    _priority = "high",
                ))

        return rating, recommendations


# =============================================================================
# Main Telemetry Service
# =============================================================================
class CarbonTelemetryService:
    """
    Main service for carbon and energy telemetry.
    """

    def __init__(self, region: str = "US-CA"):
        self.power_monitor = PowerMonitor()
        self.carbon_service = CarbonIntensityService(region)
        self.footprint_calculator = CarbonFootprintCalculator(self.carbon_service)
        self.efficiency_analyzer = EnergyEfficiencyAnalyzer()
        self._running = False

    async def collect_metrics(self) -> Tuple[List[PowerMetrics], List[ThermalMetrics]]:
        """Collect all metrics."""
        power_metrics = await self.power_monitor.collect_power_metrics()
        thermal_metrics = await self.power_monitor.collect_thermal_metrics()
        return power_metrics, thermal_metrics

    async def get_current_footprint(self, duration_minutes: int = 60) -> CarbonFootprint:
        """Get carbon footprint for the specified duration."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=duration_minutes)

        # Get metrics from history
        recent_metrics = [
            m for m in self.power_monitor.metrics_history
            if start_time <= m.timestamp <= end_time
        ]

        # Calculate energy consumption
        energy = self.footprint_calculator.calculate_energy_consumption(
            recent_metrics,
            start_time,
            end_time
        )

        # Calculate footprint
        return await self.footprint_calculator.calculate_footprint(energy)

    async def get_efficiency_report(self) -> Dict[str, Any]:
        """Get comprehensive efficiency report."""
        # Collect current metrics
        power_metrics, thermal_metrics = await self.collect_metrics()

        # Analyze efficiency
        rating, recommendations = self.efficiency_analyzer.analyze_efficiency(
            power_metrics,
            thermal_metrics
        )

        # Get footprint
        footprint = await self.get_current_footprint(60)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "efficiency_rating": rating.value,
            "current_power_watts": self.power_monitor.get_total_power(power_metrics),
            "carbon_footprint_kg": footprint.total_carbon_kg,
            "recommendations": [
                {
                    "id": r.recommendation_id,
                    "category": r.category,
                    "title": r.title,
                    "description": r.description,
                    "savings_watts": r.estimated_savings_watts,
                    "priority": r.priority,
                }
                for r in recommendations
            ],
        }

    async def start_monitoring(self) -> None:
        """Start continuous monitoring."""
        self._running = True
        logger.info("Starting carbon telemetry monitoring...")

        while self._running:
            try:
                await self.collect_metrics()
                await asyncio.sleep(self.power_monitor.collection_interval)
            except Exception as e:
                logger.error(f"Error in telemetry monitoring: {e}")
                await asyncio.sleep(60)

    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        self._running = False
        logger.info("Stopped carbon telemetry monitoring")


# =============================================================================
# Example Usage
# =============================================================================


async def main():
    """Example usage of carbon telemetry."""
    service = CarbonTelemetryService(region="US-CA")

    # Collect metrics
    print("Collecting power and thermal metrics...")
    power_metrics, thermal_metrics = await service.collect_metrics()

    print(f"\nPower Metrics ({len(power_metrics)} components):")
    for metric in power_metrics:
        print(f"  {metric.component_type.value}: {metric.power_watts:.2f}W")
        if metric.temperature_celsius:
            print(f"    Temperature: {metric.temperature_celsius:.1f}°C")

    total_power = service.power_monitor.get_total_power(power_metrics)
    print(f"\nTotal Power Consumption: {total_power:.2f}W")

    # Get footprint
    print("\nCalculating carbon footprint...")
    footprint = await service.get_current_footprint(60)

    print("\nCarbon Footprint (last hour):")
    print(f"  Energy: {footprint.energy_kwh:.4f} kWh")
    print(f"  Carbon: {footprint.total_carbon_kg:.4f} kg CO2")
    print(f"  Equivalent to driving: {footprint.equivalent_km_driven:.2f} km")
    print(f"  Trees needed to offset: {footprint.equivalent_trees:.4f}")

    # Get efficiency report
    report = await service.get_efficiency_report()

    print(f"\nEfficiency Rating: {report['efficiency_rating'].upper()}")
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  [{rec['priority'].upper()}] {rec['title']}")
            print(f"    {rec['description']}")
            print(f"    Potential savings: {rec['savings_watts']:.1f}W")


if __name__ == "__main__":
    asyncio.run(main())
