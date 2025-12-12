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


"""
AI-Assisted Operational Runbooks for DebVisor.

Provides intelligent remediation suggestions based on:
- System alerts and anomalies
- Log patterns and error messages
- Historical incident data
- Best practices knowledge base

Features:
- LLM-powered root cause analysis
- Step-by-step remediation guidance
- Contextual documentation links
- Command generation with safety checks
- Feedback loop for continuous improvement

Author: DebVisor Team
Date: December 11, 2025
"""

import asyncio
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class AlertSeverity(Enum):
    """Alert severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RemediationStatus(Enum):
    """Status of remediation execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class RunbookCategory(Enum):
    """Categories of operational runbooks."""
    PERFORMANCE = "performance"
    SECURITY = "security"
    AVAILABILITY = "availability"
    CAPACITY = "capacity"
    NETWORK = "network"
    STORAGE = "storage"
    DATABASE = "database"
    APPLICATION = "application"


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class SystemAlert:
    """Represents a system alert requiring attention."""
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    source: str  # e.g., "prometheus", "logs", "health_check"
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    labels: Dict[str, str] = field(default_factory=dict)
    raw_data: Optional[str] = None


@dataclass
class RemediationStep:
    """Single step in a remediation plan."""
    step_number: int
    description: str
    command: Optional[str] = None
    expected_output: Optional[str] = None
    verification: Optional[str] = None
    safety_level: str = "safe"  # safe, caution, dangerous
    estimated_duration: str = "< 1 min"
    rollback_command: Optional[str] = None


@dataclass
class RunbookRecommendation:
    """AI-generated runbook recommendation."""
    runbook_id: str
    title: str
    category: RunbookCategory
    confidence_score: float  # 0.0 to 1.0
    root_cause_analysis: str
    remediation_steps: List[RemediationStep]
    prerequisites: List[str] = field(default_factory=list)
    documentation_links: List[str] = field(default_factory=list)
    estimated_time: str = "5-10 minutes"
    risk_assessment: str = "Low"
    success_rate: Optional[float] = None  # Historical success rate
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RemediationExecution:
    """Tracks execution of a remediation plan."""
    execution_id: str
    runbook_id: str
    alert_id: str
    status: RemediationStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    executed_steps: List[int] = field(default_factory=list)
    step_results: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    error_message: Optional[str] = None
    user_approved: bool = False


# =============================================================================
# Knowledge Base
# =============================================================================


class RunbookKnowledgeBase:
    """
    Knowledge base of operational patterns and remediation strategies.
    In production, this would be populated from:
    - Historical incident data
    - Best practices documentation
    - Team expertise and tribal knowledge
    """

    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        """Initialize common operational patterns."""
        self.patterns = {
            "high_cpu_usage": {
                "indicators": ["cpu", "high", "usage", "overload", "throttle"],
                "category": RunbookCategory.PERFORMANCE,
                "root_causes": [
                    "Resource-intensive process running",
                    "Infinite loop or runaway process",
                    "Insufficient CPU allocation",
                    "DoS attack or traffic spike",
                ],
                "remediation_steps": [
                    "Identify top CPU consumers (top, htop)",
                    "Check for unexpected processes",
                    "Review recent deployments or changes",
                    "Scale resources if needed",
                    "Investigate process logs for errors",
                ],
            },
            "high_memory_usage": {
                "indicators": ["memory", "ram", "oom", "swap", "leak"],
                "category": RunbookCategory.PERFORMANCE,
                "root_causes": [
                    "Memory leak in application",
                    "Insufficient memory allocation",
                    "Large dataset loaded into memory",
                    "Memory-intensive operations",
                ],
                "remediation_steps": [
                    "Identify memory-consuming processes",
                    "Check for memory leaks",
                    "Review application logs",
                    "Restart affected services if safe",
                    "Scale memory resources",
                ],
            },
            "disk_full": {
                "indicators": ["disk", "full", "space", "storage", "no space"],
                "category": RunbookCategory.STORAGE,
                "root_causes": [
                    "Log files growing unbounded",
                    "Temporary files not cleaned up",
                    "Database growth without maintenance",
                    "Backup files accumulating",
                ],
                "remediation_steps": [
                    "Identify largest directories (du -sh)",
                    "Clean up old log files",
                    "Remove temporary files",
                    "Archive or delete old backups",
                    "Extend disk capacity if needed",
                ],
            },
            "service_down": {
                "indicators": ["down", "unavailable", "failed", "stopped", "crash"],
                "category": RunbookCategory.AVAILABILITY,
                "root_causes": [
                    "Service crashed due to error",
                    "Resource exhaustion",
                    "Configuration error",
                    "Dependency failure",
                ],
                "remediation_steps": [
                    "Check service status",
                    "Review service logs for errors",
                    "Verify configuration",
                    "Check dependencies",
                    "Restart service if appropriate",
                ],
            },
            "network_latency": {
                "indicators": ["latency", "slow", "timeout", "network", "connection"],
                "category": RunbookCategory.NETWORK,
                "root_causes": [
                    "Network congestion",
                    "Routing issues",
                    "DNS resolution problems",
                    "Firewall blocking traffic",
                ],
                "remediation_steps": [
                    "Check network connectivity",
                    "Measure latency to endpoints",
                    "Verify DNS resolution",
                    "Review firewall rules",
                    "Check for network congestion",
                ],
            },
            "database_slow": {
                "indicators": ["database", "slow", "query", "timeout", "lock"],
                "category": RunbookCategory.DATABASE,
                "root_causes": [
                    "Slow queries without indexes",
                    "Database locks or deadlocks",
                    "Resource contention",
                    "Large transactions",
                ],
                "remediation_steps": [
                    "Identify slow queries",
                    "Check for missing indexes",
                    "Review active connections",
                    "Check for locks or deadlocks",
                    "Optimize query performance",
                ],
            },
        }

    def match_pattern(self, alert: SystemAlert) -> Optional[Dict[str, Any]]:
        """Match an alert to a known pattern."""
        alert_text = f"{alert.title} {alert.description}".lower()

        best_match = None
        best_score = 0

        for pattern_name, pattern_data in self.patterns.items():
            score = sum(
                1 for indicator in pattern_data["indicators"]
                if indicator in alert_text
            )

            if score > best_score:
                best_score = score
                best_match = (pattern_name, pattern_data)

        if best_match and best_score > 0:
            return best_match[1]

        return None


# =============================================================================
# AI Runbook Generator
# =============================================================================


class AIRunbookGenerator:
    """
    Generates operational runbooks using AI/LLM capabilities.

    In production, this would integrate with:
    - OpenAI GPT-4 / Claude / Gemini
    - Local LLM (llama.cpp, Ollama)
    - Azure OpenAI Service

    For now, uses pattern matching + templates.
    """

    def __init__(self, knowledge_base: RunbookKnowledgeBase):
        self.kb = knowledge_base
        self.historical_success: Dict[str, float] = {}

    async def generate_runbook(
        self,
        alert: SystemAlert,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[RunbookRecommendation]:
        """Generate a runbook recommendation for an alert."""
        logger.info(f"Generating runbook for alert: {alert.alert_id}")

        # Match alert to known patterns
        pattern = self.kb.match_pattern(alert)

        if not pattern:
            logger.warning(f"No pattern match for alert {alert.alert_id}")
            return self._generate_generic_runbook(alert, context)

        # Generate runbook from pattern
        runbook_id = f"rb-{alert.alert_id}"

        steps = self._create_remediation_steps(pattern, alert, context)

        recommendation = RunbookRecommendation(
            runbook_id=runbook_id,
            title=f"Remediation for {alert.title}",
            category=pattern["category"],
            confidence_score=self._calculate_confidence(pattern, alert),
            root_cause_analysis=self._generate_root_cause_analysis(
                pattern, alert, context
            ),
            remediation_steps=steps,
            prerequisites=self._identify_prerequisites(pattern, alert),
            documentation_links=self._get_documentation_links(pattern),
            estimated_time=self._estimate_time(steps),
            risk_assessment=self._assess_risk(steps),
            success_rate=self.historical_success.get(runbook_id),
        )

        logger.info(
            f"Generated runbook {runbook_id} with confidence "
            f"{recommendation.confidence_score:.2f}"
        )

        return recommendation

    def _calculate_confidence(
        self,
        pattern: Dict[str, Any],
        alert: SystemAlert
    ) -> float:
        """Calculate confidence score for the recommendation."""
        # Simple scoring based on pattern match strength
        alert_text = f"{alert.title} {alert.description}".lower()

        matches = sum(
            1 for indicator in pattern["indicators"]
            if indicator in alert_text
        )

        confidence = min(0.5 + (matches * 0.1), 0.95)

        # Boost confidence if we have historical success
        runbook_id = f"rb-{alert.alert_id}"
        if runbook_id in self.historical_success:
            confidence = (confidence + self.historical_success[runbook_id]) / 2

        return confidence

    def _generate_root_cause_analysis(
        self,
        pattern: Dict[str, Any],
        alert: SystemAlert,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate root cause analysis."""
        analysis = f"Alert: {alert.title}\n\n"
        analysis += f"Severity: {alert.severity.value}\n\n"
        analysis += "Possible Root Causes:\n"

        for i, cause in enumerate(pattern.get("root_causes", []), 1):
            analysis += f"{i}. {cause}\n"

        if context:
            analysis += "\nContextual Information:\n"
            for key, value in context.items():
                analysis += f"- {key}: {value}\n"

        return analysis

    def _create_remediation_steps(
        self,
        pattern: Dict[str, Any],
        alert: SystemAlert,
        context: Optional[Dict[str, Any]]
    ) -> List[RemediationStep]:
        """Create detailed remediation steps."""
        steps = []

        for i, step_desc in enumerate(pattern.get("remediation_steps", []), 1):
            step = RemediationStep(
                step_number=i,
                description=step_desc,
                command=self._generate_command(step_desc, alert, context),
                expected_output=self._describe_expected_output(step_desc),
                verification=self._create_verification_check(step_desc),
                safety_level=self._assess_step_safety(step_desc),
                estimated_duration=self._estimate_step_duration(step_desc),
            )
            steps.append(step)

        return steps

    def _generate_command(
        self,
        step_desc: str,
        alert: SystemAlert,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Generate specific command for a remediation step."""
        step_lower = step_desc.lower()

        # Pattern-based command generation
        if "top cpu" in step_lower or "identify" in step_lower:
            return "ps aux --sort=-%cpu | head -10"
        elif "memory" in step_lower and "identify" in step_lower:
            return "ps aux --sort=-%mem | head -10"
        elif "disk" in step_lower and "largest" in step_lower:
            return "du -h / | sort -rh | head -20"
        elif "service status" in step_lower:
            if context and "service_name" in context:
                return f"systemctl status {context['service_name']}"
            return "systemctl status <service-name>"
        elif "restart service" in step_lower:
            if context and "service_name" in context:
                return f"systemctl restart {context['service_name']}"
            return "systemctl restart <service-name>"
        elif "clean" in step_lower and "log" in step_lower:
            return "find /var/log -name '*.log' -mtime +30 -delete"

        return None

    def _describe_expected_output(self, step_desc: str) -> Optional[str]:
        """Describe what to expect from a step."""
        if "identify" in step_desc.lower():
            return "List of processes with resource usage"
        elif "status" in step_desc.lower():
            return "Service status: active (running) or inactive/failed"
        elif "restart" in step_desc.lower():
            return "Service restarted successfully"

        return None

    def _create_verification_check(self, step_desc: str) -> Optional[str]:
        """Create verification check for a step."""
        if "restart" in step_desc.lower():
            return "systemctl is-active <service-name>"
        elif "clean" in step_desc.lower():
            return "df -h (verify space freed)"

        return None

    def _assess_step_safety(self, step_desc: str) -> str:
        """Assess safety level of a remediation step."""
        dangerous_keywords = ["delete", "remove", "kill", "force"]
        caution_keywords = ["restart", "stop", "modify", "change"]

        step_lower = step_desc.lower()

        if any(kw in step_lower for kw in dangerous_keywords):
            return "dangerous"
        elif any(kw in step_lower for kw in caution_keywords):
            return "caution"

        return "safe"

    def _estimate_step_duration(self, step_desc: str) -> str:
        """Estimate duration for a remediation step."""
        if "identify" in step_desc.lower() or "check" in step_desc.lower():
            return "< 1 min"
        elif "restart" in step_desc.lower():
            return "1-2 mins"
        elif "clean" in step_desc.lower() or "remove" in step_desc.lower():
            return "2-5 mins"

        return "1-5 mins"

    def _identify_prerequisites(
        self,
        pattern: Dict[str, Any],
        alert: SystemAlert
    ) -> List[str]:
        """Identify prerequisites for remediation."""
        prereqs = [
            "Root or sudo access to the system",
            "Backup of current configuration",
        ]

        if pattern["category"] == RunbookCategory.DATABASE:
            prereqs.append("Database connection credentials")
        elif pattern["category"] == RunbookCategory.NETWORK:
            prereqs.append("Network access to affected systems")

        return prereqs

    def _get_documentation_links(self, pattern: Dict[str, Any]) -> List[str]:
        """Get relevant documentation links."""
        # In production, this would link to actual documentation
        return [
            f"https://docs.debvisor.com/{pattern['category'].value}/troubleshooting",
            "https://docs.debvisor.com/operations/runbooks",
        ]

    def _estimate_time(self, steps: List[RemediationStep]) -> str:
        """Estimate total time for remediation."""
        # Simple estimation based on number of steps
        if len(steps) <= 3:
            return "5-10 minutes"
        elif len(steps) <= 6:
            return "10-20 minutes"
        else:
            return "20-30 minutes"

    def _assess_risk(self, steps: List[RemediationStep]) -> str:
        """Assess overall risk of remediation."""
        dangerous_count = sum(1 for s in steps if s.safety_level == "dangerous")
        caution_count = sum(1 for s in steps if s.safety_level == "caution")

        if dangerous_count > 0:
            return "High"
        elif caution_count >= 2:
            return "Medium"

        return "Low"

    def _generate_generic_runbook(
        self,
        alert: SystemAlert,
        context: Optional[Dict[str, Any]]
    ) -> RunbookRecommendation:
        """Generate a generic runbook when no pattern matches."""
        steps = [
            RemediationStep(
                step_number=1,
                description="Review alert details and error messages",
                safety_level="safe",
            ),
            RemediationStep(
                step_number=2,
                description="Check system logs for related errors",
                command="journalctl -xe | tail -100",
                safety_level="safe",
            ),
            RemediationStep(
                step_number=3,
                description="Verify system resource availability",
                command="free -h && df -h && uptime",
                safety_level="safe",
            ),
            RemediationStep(
                step_number=4,
                description="Consult documentation or escalate to on-call engineer",
                safety_level="safe",
            ),
        ]

        return RunbookRecommendation(
            runbook_id=f"rb-generic-{alert.alert_id}",
            title=f"Investigation Steps for {alert.title}",
            category=RunbookCategory.APPLICATION,
            confidence_score=0.3,
            root_cause_analysis=(
                f"Alert: {alert.title}\n\n"
                "No specific pattern matched. Follow generic investigation steps."
            ),
            remediation_steps=steps,
            prerequisites=["System access"],
            documentation_links=["https://docs.debvisor.com/operations/troubleshooting"],
            estimated_time="15-30 minutes",
            risk_assessment="Low",
        )


# =============================================================================
# Runbook Manager
# =============================================================================


class OperationalRunbookManager:
    """
    Main manager for AI-assisted operational runbooks.
    """

    def __init__(self):
        self.kb = RunbookKnowledgeBase()
        self.generator = AIRunbookGenerator(self.kb)
        self.active_executions: Dict[str, RemediationExecution] = {}

    async def handle_alert(
        self,
        alert: SystemAlert,
        context: Optional[Dict[str, Any]] = None,
        auto_remediate: bool = False
    ) -> Optional[RunbookRecommendation]:
        """
        Handle a system alert and generate runbook recommendation.

        Args:
            alert: The system alert to handle
            context: Additional context (e.g., service name, host)
            auto_remediate: Whether to automatically execute safe steps

        Returns:
            Generated runbook recommendation
        """
        runbook = await self.generator.generate_runbook(alert, context)

        if not runbook:
            logger.error(f"Failed to generate runbook for alert {alert.alert_id}")
            return None

        logger.info(
            f"Generated runbook {runbook.runbook_id} for alert {alert.alert_id} "
            f"(confidence: {runbook.confidence_score:.2f})"
        )

        if auto_remediate and runbook.confidence_score >= 0.7:
            await self.execute_runbook(runbook, alert, auto_execute_safe=True)

        return runbook

    async def execute_runbook(
        self,
        runbook: RunbookRecommendation,
        alert: SystemAlert,
        auto_execute_safe: bool = False
    ) -> RemediationExecution:
        """Execute a runbook's remediation steps."""
        execution_id = f"exec-{alert.alert_id}-{datetime.now().timestamp()}"

        execution = RemediationExecution(
            execution_id=execution_id,
            runbook_id=runbook.runbook_id,
            alert_id=alert.alert_id,
            status=RemediationStatus.PENDING,
            started_at=datetime.now(timezone.utc),
            user_approved=not auto_execute_safe,
        )

        self.active_executions[execution_id] = execution

        # In production, this would execute steps via automation framework
        # For now, just log the steps
        logger.info(f"Starting execution {execution_id} for runbook {runbook.runbook_id}")

        execution.status = RemediationStatus.IN_PROGRESS

        for step in runbook.remediation_steps:
            if auto_execute_safe and step.safety_level != "safe":
                logger.info(
                    f"Skipping step {step.step_number} (safety: {step.safety_level})"
                )
                continue

            logger.info(f"Executing step {step.step_number}: {step.description}")

            # Simulate execution
            await asyncio.sleep(0.1)

            execution.executed_steps.append(step.step_number)
            execution.step_results[step.step_number] = {
                "status": "completed",
                "output": "Simulated execution output",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        execution.status = RemediationStatus.COMPLETED
        execution.completed_at = datetime.now(timezone.utc)

        logger.info(f"Completed execution {execution_id}")

        return execution

    def get_execution_status(self, execution_id: str) -> Optional[RemediationExecution]:
        """Get status of a remediation execution."""
        return self.active_executions.get(execution_id)


# =============================================================================
# Example Usage
# =============================================================================


async def main():
    """Example usage of AI-assisted operational runbooks."""
    manager = OperationalRunbookManager()

    # Simulate a high CPU alert
    alert = SystemAlert(
        alert_id="alert-12345",
        title="High CPU Usage Detected",
        description="CPU usage has exceeded 90% for the past 5 minutes",
        severity=AlertSeverity.HIGH,
        source="prometheus",
        timestamp=datetime.now(timezone.utc),
        metadata={"cpu_percent": 92.5, "host": "web-server-01"},
        labels={"service": "web", "environment": "production"},
    )

    # Generate runbook
    runbook = await manager.handle_alert(
        alert,
        context={"service_name": "nginx", "host": "web-server-01"},
        auto_remediate=False,
    )

    if runbook:
        print(f"\n{'='*80}")
        print(f"Runbook: {runbook.title}")
        print(f"Confidence: {runbook.confidence_score:.2%}")
        print(f"Risk: {runbook.risk_assessment}")
        print(f"Estimated Time: {runbook.estimated_time}")
        print(f"\n{runbook.root_cause_analysis}")
        print(f"\nRemediation Steps:")
        for step in runbook.remediation_steps:
            print(f"\n{step.step_number}. {step.description}")
            if step.command:
                print(f"   Command: {step.command}")
            print(f"   Safety: {step.safety_level}")
            if step.expected_output:
                print(f"   Expected: {step.expected_output}")
        print(f"\n{'='*80}")


if __name__ == "__main__":
    asyncio.run(main())
