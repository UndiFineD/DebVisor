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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Continuous Compliance Auto-Remediation for DebVisor.

Provides automatic detection and remediation of configuration drift
that violates compliance policies.

Features:
- Continuous monitoring for compliance violations
- Automatic remediation of approved policies
- Drift detection and alerting
- Rollback capabilities
- Audit trail of all remediation actions
- Policy-based auto-remediation rules

Author: DebVisor Team
Date: December 11, 2025
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from pathlib import Path
import hashlib

_logger=logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================
class RemediationAction(Enum):
    """Types of remediation actions."""
    REVERT_CONFIG = "revert_config"
    APPLY_TEMPLATE = "apply_template"
    RESTART_SERVICE = "restart_service"
    UPDATE_SETTING = "update_setting"
    DISABLE_FEATURE = "disable_feature"
    ENABLE_FEATURE = "enable_feature"
    APPLY_PATCH = "apply_patch"


class RemediationMode(Enum):
    """Modes for auto-remediation."""
    MANUAL = "manual"  # Require approval
    SEMI_AUTO = "semi_auto"  # Auto for low-risk, manual for high-risk
    FULLY_AUTO = "fully_auto"  # Auto for all approved policies


class DriftSeverity(Enum):
    """Severity of configuration drift."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# =============================================================================
# Data Models
# =============================================================================


@dataclass


class ConfigurationBaseline:
    """Represents a known-good configuration baseline."""
    baseline_id: str
    resource_type: str  # e.g., "ssh_config", "firewall_rules", "user_settings"
    resource_id: str
    configuration: Dict[str, Any]
    checksum: str
    created_at: datetime
    approved_by: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass


class ConfigurationDrift:
    """Represents detected configuration drift."""
    drift_id: str
    baseline_id: str
    resource_type: str
    resource_id: str
    detected_at: datetime
    severity: DriftSeverity
    changes: Dict[str, Any]  # {field: {expected: x, actual: y}}
    compliance_policies_violated: List[str] = field(default_factory=list)
    remediation_action: Optional[RemediationAction] = None
    auto_remediate: bool = False


@dataclass


class RemediationRule:
    """Rule for automatic remediation."""
    rule_id: str
    name: str
    description: str
    resource_type: str
    compliance_policy_ids: List[str]
    action: RemediationAction
    mode: RemediationMode
    risk_level: str  # "low", "medium", "high"
    enabled: bool = True
    max_auto_remediations_per_hour: int = 10
    require_approval_threshold: Optional[DriftSeverity] = None


@dataclass


class RemediationRecord:
    """Record of a remediation action."""
    record_id: str
    drift_id: str
    rule_id: str
    action: RemediationAction
    executed_at: datetime
    executed_by: str  # "system" or user ID
    success: bool
    changes_made: Dict[str, Any]
    rollback_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


# =============================================================================
# Configuration Monitor
# =============================================================================
class ConfigurationMonitor:
    """
    Monitors system configuration for drift from baselines.
    """

    def __init__(self) -> None:
        self.baselines: Dict[str, ConfigurationBaseline] = {}
        self.scan_interval: int = 300  # 5 minutes
        self._running: bool = False

    def register_baseline(self, baseline: ConfigurationBaseline) -> None:
        """Register a configuration baseline for monitoring."""
        logger.info(
            f"Registering baseline {baseline.baseline_id} for "
            f"{baseline.resource_type}/{baseline.resource_id}"
        )
        self.baselines[baseline.baseline_id] = baseline

    async def scan_for_drift(self) -> List[ConfigurationDrift]:
        """Scan all registered baselines for configuration drift."""
        drifts: List[ConfigurationDrift] = []

        for baseline in self.baselines.values():
            _drift=await self._check_single_resource(baseline)
            if drift:
                drifts.append(drift)

        return drifts

    async def _check_single_resource(
        self,
        baseline: ConfigurationBaseline
    ) -> Optional[ConfigurationDrift]:
        """Check a single resource for drift."""
        try:
        # Get current configuration
            current_config = await self._get_current_config(
                baseline.resource_type,
                baseline.resource_id
            )

            # Calculate checksum
            _current_checksum=self._calculate_checksum(current_config)

            # Compare with baseline
            if current_checksum == baseline.checksum:
                return None

            # Detect specific changes
            _changes=self._detect_changes(baseline.configuration, current_config)

            if not changes:
                return None

            # Determine severity
            _severity=self._assess_drift_severity(changes, baseline)

            drift = ConfigurationDrift(
                _drift_id=f"drift-{baseline.baseline_id}-{datetime.now().timestamp()}",
                _baseline_id = baseline.baseline_id,
                _resource_type = baseline.resource_type,
                _resource_id = baseline.resource_id,
                _detected_at=datetime.now(timezone.utc),
                _severity=severity,
                _changes = changes,
            )

            logger.warning(
                f"Configuration drift detected: {drift.drift_id} "
                f"(severity: {severity.value})"
            )

            return drift

        except Exception as e:
            logger.error(
                f"Error checking resource {baseline.resource_id}: {e}"
            )
            return None

    async def _get_current_config(
        self,
        resource_type: str,
        resource_id: str
    ) -> Dict[str, Any]:
        """Get current configuration for a resource."""
        # In production, this would query actual system configuration
        # For now, simulate by returning example configs

        if resource_type == "ssh_config":
            return {
                "PermitRootLogin": "yes",  # Drift detected!
                "PasswordAuthentication": "no",
                "PermitEmptyPasswords": "no",
                "PubkeyAuthentication": "yes",
            }
        elif resource_type == "firewall_rules":
            return {
                "allow_ssh": True,
                "allow_http": True,
                "allow_https": True,
                "default_policy": "deny",
            }

        return {}

    def _calculate_checksum(self, config: Dict[str, Any]) -> str:
        """Calculate checksum of configuration."""
        _config_json=json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_json.encode()).hexdigest()

    def _detect_changes(
        self,
        baseline_config: Dict[str, Any],
        current_config: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Detect specific configuration changes."""
        changes = {}

        _all_keys=set(baseline_config.keys()) | set(current_config.keys())

        for key in all_keys:
            _baseline_value=baseline_config.get(key)
            _current_value=current_config.get(key)

            if baseline_value != current_value:
                changes[key] = {
                    "expected": baseline_value,
                    "actual": current_value,
                }

        return changes

    def _assess_drift_severity(
        self,
        changes: Dict[str, Any],
        baseline: ConfigurationBaseline
    ) -> DriftSeverity:
        """Assess severity of configuration drift."""
        # Critical security settings
        critical_settings = {
            "PermitRootLogin",
            "PasswordAuthentication",
            "default_firewall_policy",
        }

        for change_key in changes.keys():
            if change_key in critical_settings:
                return DriftSeverity.CRITICAL

        if len(changes) >= 5:
            return DriftSeverity.HIGH
        elif len(changes) >= 3:
            return DriftSeverity.MEDIUM

        return DriftSeverity.LOW

    async def start_monitoring(self) -> None:
        """Start continuous monitoring loop."""
        self._running = True
        logger.info("Starting configuration monitoring...")

        while self._running:
            try:
                _drifts=await self.scan_for_drift()

                if drifts:
                    logger.warning(f"Detected {len(drifts)} configuration drifts")

                await asyncio.sleep(self.scan_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self._running = False
        logger.info("Stopping configuration monitoring...")


# =============================================================================
# Auto-Remediation Engine
# =============================================================================
class AutoRemediationEngine:
    """
    Automatically remediates configuration drift based on rules.
    """

    def __init__(self, monitor: ConfigurationMonitor) -> None:
        self.monitor = monitor
        self.rules: Dict[str, RemediationRule] = {}
        self.remediation_history: List[RemediationRecord] = []
        self.remediation_counts: Dict[str, List[datetime]] = {}
        self._initialize_default_rules()

    def _initialize_default_rules(self) -> None:
        """Initialize default remediation rules."""
        self.rules = {
            "ssh-root-login": RemediationRule(
                _rule_id = "ssh-root-login",
                _name = "SSH Root Login Disabled",
                _description = "Automatically disable SSH root login if enabled",
                _resource_type = "ssh_config",
                _compliance_policy_ids = ["SEC-001"],
                _action = RemediationAction.UPDATE_SETTING,
                _mode = RemediationMode.FULLY_AUTO,
                _risk_level = "low",
                _max_auto_remediations_per_hour = 5,
            ),
            "firewall-default-deny": RemediationRule(
                _rule_id = "firewall-default-deny",
                _name = "Firewall Default Deny",
                _description = "Ensure firewall default policy is deny",
                _resource_type = "firewall_rules",
                _compliance_policy_ids = ["NET-001"],
                _action = RemediationAction.UPDATE_SETTING,
                _mode = RemediationMode.SEMI_AUTO,
                _risk_level = "medium",
                _require_approval_threshold = DriftSeverity.HIGH,
            ),
        }

    def register_rule(self, rule: RemediationRule) -> None:
        """Register a remediation rule."""
        self.rules[rule.rule_id] = rule
        logger.info(f"Registered remediation rule: {rule.rule_id}")

    async def process_drift(
        self,
        drift: ConfigurationDrift
    ) -> Optional[RemediationRecord]:
        """Process a detected drift and remediate if appropriate."""
        # Find matching rule
        _rule=self._find_matching_rule(drift)

        if not rule:
            logger.info(f"No remediation rule for drift {drift.drift_id}")
            return None

        if not rule.enabled:
            logger.info(f"Rule {rule.rule_id} is disabled")
            return None

        # Check rate limits
        if not self._check_rate_limit(rule):
            logger.warning(
                f"Rate limit exceeded for rule {rule.rule_id}, skipping remediation"
            )
            return None

        # Determine if auto-remediation is allowed
        if not self._should_auto_remediate(drift, rule):
            logger.info(
                f"Drift {drift.drift_id} requires manual approval "
                f"(severity: {drift.severity.value}, mode: {rule.mode.value})"
            )
            # In production, this would trigger an approval workflow
            return None

        # Execute remediation
        return await self._execute_remediation(drift, rule)

    def _find_matching_rule(
        self,
        drift: ConfigurationDrift
    ) -> Optional[RemediationRule]:
        """Find a remediation rule matching the drift."""
        for rule in self.rules.values():
            if rule.resource_type == drift.resource_type:
            # Check if any violated policies match rule
                if any(
                    policy_id in rule.compliance_policy_ids
                    for policy_id in drift.compliance_policies_violated
                ):
                    return rule

                # Also match if no specific policies violated but resource type matches
                if not drift.compliance_policies_violated:
                    return rule

        return None

    def _check_rate_limit(self, rule: RemediationRule) -> bool:
        """Check if rate limit allows remediation."""
        _now=datetime.now(timezone.utc)
        _one_hour_ago=now - timedelta(hours=1)

        if rule.rule_id not in self.remediation_counts:
            self.remediation_counts[rule.rule_id] = []

        # Clean up old entries
        self.remediation_counts[rule.rule_id] = [
            ts for ts in self.remediation_counts[rule.rule_id]
            if ts > one_hour_ago
        ]

        # Check limit
        _count=len(self.remediation_counts[rule.rule_id])
        if count >= rule.max_auto_remediations_per_hour:
            return False

        return True

    def _should_auto_remediate(
        self,
        drift: ConfigurationDrift,
        rule: RemediationRule
    ) -> bool:
        """Determine if drift should be auto-remediated."""
        if rule.mode == RemediationMode.MANUAL:
            return False

        if rule.mode == RemediationMode.FULLY_AUTO:
            return True

        # Semi-auto mode
        if rule.require_approval_threshold:
        # Require approval for high severity
            severity_values = {
                DriftSeverity.LOW: 1,
                DriftSeverity.MEDIUM: 2,
                DriftSeverity.HIGH: 3,
                DriftSeverity.CRITICAL: 4,
            }

            _drift_level=severity_values.get(drift.severity, 0)
            _threshold_level=severity_values.get(rule.require_approval_threshold, 0)

            if drift_level >= threshold_level:
                return False

        return True

    async def _execute_remediation(
        self,
        drift: ConfigurationDrift,
        rule: RemediationRule
    ) -> RemediationRecord:
        """Execute a remediation action."""
        record_id = f"rem-{drift.drift_id}"

        logger.info(
            f"Executing remediation {record_id} for drift {drift.drift_id} "
            f"using rule {rule.rule_id}"
        )

        # Get baseline configuration
        _baseline=self.monitor.baselines.get(drift.baseline_id)
        if not baseline:
            raise ValueError(f"Baseline {drift.baseline_id} not found")

        # Store rollback data
        _current_config = await self.monitor._get_current_config(
            drift.resource_type,
            drift.resource_id
        )

        try:
        # Execute remediation based on action type
            if rule.action == RemediationAction.REVERT_CONFIG:
                success = await self._revert_configuration(
                    drift,
                    baseline.configuration
                )
            elif rule.action == RemediationAction.UPDATE_SETTING:
                _success=await self._update_settings(drift, baseline.configuration)
            else:
                logger.warning(f"Unsupported action: {rule.action}")
                _success = False

            # Record remediation
            record = RemediationRecord(
                _record_id = record_id,
                _drift_id = drift.drift_id,
                _rule_id = rule.rule_id,
                _action = rule.action,
                _executed_at=datetime.now(timezone.utc),
                _executed_by = "system",
                _success=success,
                _changes_made = drift.changes if success else {},
                _rollback_data = current_config,
            )

            self.remediation_history.append(record)

            # Update rate limit tracker
            if rule.rule_id not in self.remediation_counts:
                self.remediation_counts[rule.rule_id] = []
            self.remediation_counts[rule.rule_id].append(
                datetime.now(timezone.utc)
            )

            if success:
                logger.info(f"Remediation {record_id} completed successfully")
            else:
                logger.error(f"Remediation {record_id} failed")

            return record

        except Exception as e:
            logger.error(f"Error executing remediation {record_id}: {e}")

            record = RemediationRecord(
                _record_id = record_id,
                _drift_id = drift.drift_id,
                _rule_id = rule.rule_id,
                _action = rule.action,
                _executed_at=datetime.now(timezone.utc),
                _executed_by = "system",
                _success = False,
                _changes_made = {},
                _rollback_data = current_config,
                _error_message=str(e),
            )

            self.remediation_history.append(record)
            return record

    async def _revert_configuration(
        self,
        drift: ConfigurationDrift,
        baseline_config: Dict[str, Any]
    ) -> bool:
        """Revert configuration to baseline."""
        logger.info(
            f"Reverting {drift.resource_type}/{drift.resource_id} to baseline"
        )

        # In production, this would apply the baseline configuration
        # For now, simulate success
        await asyncio.sleep(0.1)

        return True

    async def _update_settings(
        self,
        drift: ConfigurationDrift,
        baseline_config: Dict[str, Any]
    ) -> bool:
        """Update specific settings that drifted."""
        logger.info(
            f"Updating settings for {drift.resource_type}/{drift.resource_id}"
        )

        # Update only the changed settings
        for setting, change_info in drift.changes.items():
            expected_value = change_info["expected"]
            logger.info(f"Setting {setting} = {expected_value}")

        # In production, this would apply changes via SSH/API
        await asyncio.sleep(0.1)

        return True

    async def rollback_remediation(
        self,
        record: RemediationRecord
    ) -> bool:
        """Rollback a previous remediation."""
        if not record.rollback_data:
            logger.error(f"No rollback data for remediation {record.record_id}")
            return False

        logger.info(f"Rolling back remediation {record.record_id}")

        # Find the drift
        drift = next(
            (d for d in self.monitor.baselines.values()
             if f"drift-{d.baseline_id}" in record.drift_id),
            None
        )

        if not drift:
            logger.error(f"Cannot find drift for rollback: {record.drift_id}")
            return False

        # Apply rollback data
        # In production, this would restore the previous configuration
        await asyncio.sleep(0.1)

        logger.info(f"Rollback completed for {record.record_id}")
        return True


# =============================================================================
# Main Service
# =============================================================================
class ContinuousComplianceService:
    """
    Main service for continuous compliance monitoring and auto-remediation.
    """

    def __init__(self) -> None:
        self.monitor=ConfigurationMonitor()
        self.engine=AutoRemediationEngine(self.monitor)
        self._running = False

    def register_baseline(
        self,
        resource_type: str,
        resource_id: str,
        configuration: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> ConfigurationBaseline:
        """Register a configuration baseline."""
        baseline = ConfigurationBaseline(
            _baseline_id = f"baseline-{resource_type}-{resource_id}",
            _resource_type = resource_type,
            _resource_id = resource_id,
            _configuration=configuration,
            _checksum=self.monitor._calculate_checksum(configuration),
            _created_at=datetime.now(timezone.utc),
            _tags = tags or [],
        )

        self.monitor.register_baseline(baseline)
        return baseline

    async def start(self) -> None:
        """Start continuous compliance service."""
        self._running = True
        logger.info("Starting Continuous Compliance Service...")

        while self._running:
            try:
            # Scan for drift
                _drifts=await self.monitor.scan_for_drift()

                # Process each drift
                for drift in drifts:
                    await self.engine.process_drift(drift)

                # Wait before next scan
                await asyncio.sleep(self.monitor.scan_interval)

            except Exception as e:
                logger.error(f"Error in compliance service: {e}")
                await asyncio.sleep(60)

    def stop(self) -> None:
        """Stop continuous compliance service."""
        self._running = False
        self.monitor.stop_monitoring()
        logger.info("Stopped Continuous Compliance Service")


# =============================================================================
# Example Usage
# =============================================================================


async def main():
    """Example usage of continuous compliance auto-remediation."""
    _service=ContinuousComplianceService()

    # Register SSH configuration baseline
    _ssh_baseline_config = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",
        "PermitEmptyPasswords": "no",
        "PubkeyAuthentication": "yes",
    }

    service.register_baseline(
        _resource_type = "ssh_config",
        _resource_id = "/etc/ssh/sshd_config",
        _configuration=ssh_baseline_config,
        _tags = ["security", "cis-benchmark"],
    )

    # Scan for drift once
    print("\nScanning for configuration drift...")
    _drifts=await service.monitor.scan_for_drift()

    if drifts:
        print(f"\nFound {len(drifts)} configuration drift(s):")
        for drift in drifts:
            print(f"\n  Drift ID: {drift.drift_id}")
            print(f"  Resource: {drift.resource_type}/{drift.resource_id}")
            print(f"  Severity: {drift.severity.value}")
            print("  Changes:")
            for key, change in drift.changes.items():
                print(f"    - {key}: {change['actual']} (expected: {change['expected']})")

            # Process drift
            print("\n  Processing remediation...")
            _record=await service.engine.process_drift(drift)

            if record:
                print(f"  Remediation {'succeeded' if record.success else 'failed'}")
            else:
                print("  Remediation skipped (requires approval or no rule)")
    else:
        print("\nNo configuration drift detected. All systems compliant!")


if __name__ == "__main__":
    asyncio.run(main())
