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


"""
Scheduled Report Generation Service for DebVisor

Provides:
- Scheduled report generation
- Email delivery automation
- Report templates
- Background job scheduling
- Report history and archival
- Delivery confirmation tracking

Features:
- Cron-based scheduling
- Multiple report types
- Email notifications
- Report templates
- Delivery retries
- Audit trail
"""

import logging
import smtplib
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class ReportFrequency(Enum):
    """Report generation frequency."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ON_DEMAND = "on_demand"


class ReportStatus(Enum):
    """Report generation status."""

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    DELIVERED = "delivered"


@dataclass
class ReportTemplate:
    """Report template definition."""

    template_id: str
    name: str
    description: str
    sections: List[str]    # e.g., ["summary", "metrics", "trends", "recommendations"]
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScheduledReport:
    """Scheduled report configuration."""

    report_id: str
    name: str
    template_id: str
    frequency: ReportFrequency
    recipients: List[str]
    enabled: bool = True
    next_run: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_run: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedReport:
    """Generated report instance."""

    report_instance_id: str
    scheduled_report_id: str
    template_id: str
    status: ReportStatus
    content: Optional[str] = None
    file_path: Optional[str] = None
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    delivered_at: Optional[datetime] = None
    delivery_attempts: int = 0
    error_message: Optional[str] = None


class EmailNotifier:
    """
    Handles email delivery for reports.

    Configuration via environment variables:
    - SMTP_HOST: SMTP server address
    - SMTP_PORT: SMTP server port
    - SMTP_USER: SMTP authentication user
    - SMTP_PASSWORD: SMTP authentication password
    - REPORT_FROM_ADDRESS: From address for emails
    """

    def __init__(
        self,
        smtp_host: str = "localhost",
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        from_address: str = "reports@debvisor.local",
    ):
        """
        Initialize email notifier.

        Args:
            smtp_host: SMTP server address
            smtp_port: SMTP server port
            username: SMTP authentication username
            password: SMTP authentication password
            from_address: From address for emails
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address

    def send_report(
        self,
        recipients: List[str],
        subject: str,
        report_name: str,
        report_content: str,
        file_path: Optional[str] = None,
    ) -> bool:
        """
        Send report via email.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            report_name: Report name for body
            report_content: Report content/summary
            file_path: Optional report file attachment

        Returns:
            True if successful, False otherwise
        """
        try:
        # Create email
            msg = MIMEMultipart()
            msg["From"] = self.from_address
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg["Date"] = datetime.now(timezone.utc).isoformat()

            # Email body
            body = """
            <html>
            <body>
                <h2>{report_name}</h2>
                <p>Your scheduled report has been generated and is attached.</p>
                <pre>{report_content}</pre>
                <hr/>
                <p><em>Generated: {datetime.now(timezone.utc).isoformat()}</em></p>
            </body>
            </html>
            """

            msg.attach(MIMEText(body, "html"))

            # Attach file if provided
            if file_path:
                try:
                    with open(file_path, "r") as attachment:
                        msg.attach(MIMEText(attachment.read(), "plain"))
                except Exception as e:
                    logger.warning(f"Failed to attach file {file_path}: {e}")

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.username and self.password:
                    server.starttls()
                    server.login(self.username, self.password)

                server.send_message(msg)

            logger.info(f"Report sent to {len(recipients)} recipients")
            return True

        except Exception as e:
            logger.error(f"Failed to send report email: {e}")
            return False


class ReportScheduler:
    """
    Manages scheduled report generation and delivery.

    Responsibilities:
    - Schedule report generation
    - Execute scheduled reports
    - Deliver reports via email
    - Track report history
    - Retry failed deliveries
    """

    # Maximum retry attempts for failed deliveries
    MAX_DELIVERY_RETRIES = 3

    def __init__(
        self,
        email_notifier: Optional[EmailNotifier] = None,
    ):
        """
        Initialize report scheduler.

        Args:
            email_notifier: EmailNotifier instance for sending reports
        """
        self.email_notifier = email_notifier or EmailNotifier()
        self.scheduled_reports: Dict[str, ScheduledReport] = {}
        self.generated_reports: List[GeneratedReport] = []
        self.report_templates: Dict[str, ReportTemplate] = {}
        self.generation_callbacks: Dict[str, Callable[..., Any]] = {}

    def register_template(self, template: ReportTemplate) -> None:
        """
        Register a report template.

        Args:
            template: ReportTemplate instance
        """
        self.report_templates[template.template_id] = template
        logger.info(f"Registered template: {template.name}")

    def register_generation_callback(
        self, template_id: str, callback: Callable[[ScheduledReport], str]
    ) -> None:
        """
        Register callback for report generation.

        Callback should accept ScheduledReport and return report content string.

        Args:
            template_id: Template ID
            callback: Generation callback function
        """
        self.generation_callbacks[template_id] = callback
        logger.info(f"Registered generation callback for template {template_id}")

    def schedule_report(
        self,
        report_id: str,
        name: str,
        template_id: str,
        frequency: ReportFrequency,
        recipients: List[str],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> ScheduledReport:
        """
        Schedule a new report.

        Args:
            report_id: Unique report identifier
            name: Report name
            template_id: Template to use
            frequency: Report frequency
            recipients: Email recipients
            parameters: Optional report parameters

        Returns:
            ScheduledReport instance
        """
        if template_id not in self.report_templates:
            raise ValueError(f"Unknown template: {template_id}")

        scheduled_report = ScheduledReport(
            report_id=report_id,
            name=name,
            template_id=template_id,
            frequency=frequency,
            recipients=recipients,
            parameters=parameters or {},
        )

        self.scheduled_reports[report_id] = scheduled_report
        logger.info(f"Scheduled report: {name} ({frequency.value})")
        return scheduled_report

    def generate_report(
        self,
        scheduled_report: ScheduledReport,
    ) -> GeneratedReport:
        """
        Generate report from scheduled configuration.

        Args:
            scheduled_report: ScheduledReport to generate

        Returns:
            GeneratedReport instance
        """
        import uuid

        report_instance = GeneratedReport(
            report_instance_id=str(uuid.uuid4()),
            scheduled_report_id=scheduled_report.report_id,
            template_id=scheduled_report.template_id,
            status=ReportStatus.GENERATING,
        )

        try:
        # Get generation callback
            callback = self.generation_callbacks.get(scheduled_report.template_id)
            if not callback:
                raise ValueError(
                    f"No generation callback for template {scheduled_report.template_id}"
                )

            # Generate content
            content = callback(scheduled_report)

            report_instance.content = content
            report_instance.status = ReportStatus.COMPLETED

            logger.info(f"Generated report: {scheduled_report.name}")

        except Exception as e:
            report_instance.status = ReportStatus.FAILED
            report_instance.error_message = str(e)
            logger.error(f"Failed to generate report {scheduled_report.name}: {e}")

        self.generated_reports.append(report_instance)
        return report_instance

    def deliver_report(
        self,
        generated_report: GeneratedReport,
        scheduled_report: ScheduledReport,
    ) -> bool:
        """
        Deliver generated report to recipients.

        Args:
            generated_report: Report to deliver
            scheduled_report: Original scheduled report

        Returns:
            True if delivery successful
        """
        if generated_report.status != ReportStatus.COMPLETED:
            logger.warning(
                f"Cannot deliver report {generated_report.report_instance_id}: not in COMPLETED status"
            )
            return False

        success = self.email_notifier.send_report(
            recipients=scheduled_report.recipients,
            subject=f"DebVisor Report: {scheduled_report.name}",
            report_name=scheduled_report.name,
            report_content=generated_report.content or "",
            file_path=generated_report.file_path,
        )

        if success:
            generated_report.delivered_at = datetime.now(timezone.utc)
            generated_report.status = ReportStatus.DELIVERED
            logger.info(f"Delivered report {generated_report.report_instance_id}")
        else:
            generated_report.delivery_attempts += 1
            if generated_report.delivery_attempts < self.MAX_DELIVERY_RETRIES:
                logger.warning(
                    "Report delivery failed, will retry "
                    f"({generated_report.delivery_attempts}/{self.MAX_DELIVERY_RETRIES})"
                )
            else:
                logger.error(
                    f"Report delivery failed after {self.MAX_DELIVERY_RETRIES} attempts"
                )

        return success

    def execute_scheduled_reports(self) -> Dict[str, Any]:
        """
        Execute all due scheduled reports.

        Should be called by scheduler (e.g., APScheduler, Celery).

        Returns:
            Execution summary
        """
        now = datetime.now(timezone.utc)
        executed = []
        failed = []

        for report_id, scheduled_report in self.scheduled_reports.items():
            if not scheduled_report.enabled:
                continue

            if scheduled_report.next_run > now:
                continue    # Not due yet

            try:
            # Generate report
                generated_report = self.generate_report(scheduled_report)

                # Deliver report
                if generated_report.status == ReportStatus.COMPLETED:
                    self.deliver_report(generated_report, scheduled_report)

                # Update next run time
                scheduled_report.last_run = now
                scheduled_report.next_run = self._calculate_next_run(
                    scheduled_report.frequency, now
                )

                executed.append(
                    {
                        "report_id": report_id,
                        "name": scheduled_report.name,
                        "status": generated_report.status.value,
                    }
                )

            except Exception as e:
                failed.append(
                    {
                        "report_id": report_id,
                        "name": scheduled_report.name,
                        "error": str(e),
                    }
                )
                logger.error(f"Failed to execute scheduled report {report_id}: {e}")

        return {
            "timestamp": now.isoformat(),
            "executed": len(executed),
            "failed": len(failed),
            "executed_reports": executed,
            "failed_reports": failed,
        }

    def _calculate_next_run(
        self, frequency: ReportFrequency, current_time: datetime
    ) -> datetime:
        """Calculate next run time based on frequency."""
        if frequency == ReportFrequency.DAILY:
            return current_time + timedelta(days=1)
        elif frequency == ReportFrequency.WEEKLY:
            return current_time + timedelta(weeks=1)
        elif frequency == ReportFrequency.MONTHLY:
        # Simple: add ~30 days
            return current_time + timedelta(days=30)
        elif frequency == ReportFrequency.QUARTERLY:
            return current_time + timedelta(days=90)
        else:
            return current_time

    def get_report_history(
        self,
        scheduled_report_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[GeneratedReport]:
        """
        Get report generation history.

        Args:
            scheduled_report_id: Optional filter by scheduled report
            limit: Maximum results to return

        Returns:
            List of GeneratedReport instances
        """
        reports = self.generated_reports

        if scheduled_report_id:
            reports = [
                r for r in reports if r.scheduled_report_id == scheduled_report_id
            ]

        # Sort by most recent first
        reports.sort(key=lambda r: r.generated_at, reverse=True)

        return reports[:limit]

    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status and statistics."""
        total_reports = len(self.generated_reports)
        delivered = len(
            [r for r in self.generated_reports if r.status == ReportStatus.DELIVERED]
        )
        failed = len(
            [r for r in self.generated_reports if r.status == ReportStatus.FAILED]
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scheduled_reports": len(self.scheduled_reports),
            "generated_reports": total_reports,
            "delivered": delivered,
            "failed": failed,
            "templates": len(self.report_templates),
            "scheduled_report_details": [
                {
                    "report_id": r.report_id,
                    "name": r.name,
                    "frequency": r.frequency.value,
                    "enabled": r.enabled,
                    "next_run": r.next_run.isoformat(),
                    "last_run": r.last_run.isoformat() if r.last_run else None,
                }
                for r in self.scheduled_reports.values()
            ],
        }
