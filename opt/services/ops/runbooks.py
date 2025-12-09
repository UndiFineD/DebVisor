"""
AI-Assisted Operational Runbooks.

Generates dynamic runbooks based on system alerts and context.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import logging
# import json
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class RunbookStep:
    order: int
    description: str
    command: Optional[str] = None
    verification: Optional[str] = None
    estimated_time_minutes: int = 5

@dataclass
class Runbook:
    id: str
    title: str
    description: str
    steps: List[RunbookStep]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence_score: float = 1.0
    tags: List[str] = field(default_factory=list)

class RunbookGenerator:
    """Generates runbooks based on alert context."""

    def __init__(self) -> None:
        self._templates: Dict[str, Any] = {
            "high_cpu": {
                "title": "High CPU Usage Investigation",
                "description": "Steps to diagnose and resolve high CPU usage on {hostname}.",
                "steps": [
                    {
                        "description": "Check top consuming processes",
                        "command": "top -b -n 1 | head -n 20",
                        "verification": "Identify process with >80% CPU"
                    },
                    {
                        "description": "Check system logs for errors",
                        "command": "journalctl -xe | grep error | tail -n 50",
                        "verification": "Look for repeated error messages"
                    },
                    {
                        "description": "Restart impacted service (if identified)",
                        "command": "systemctl restart <service_name>",
                        "verification": "systemctl status <service_name>"
                    }
                ],
                "tags": ["cpu", "performance"]
            },
            "disk_space": {
                "title": "Low Disk Space Resolution",
                "description": "Free up space on {hostname} partition {partition}.",
                "steps": [
                    {
                        "description": "Identify large files",
                        "command": "find {partition} -type f -size +100M -exec ls -lh {{}} \\; | sort -k 5 -rh | head -n 10",
                        "verification": "List of large files"
                    },
                    {
                        "description": "Clean package cache",
                        "command": "apt-get clean",
                        "verification": "df -h {partition}"
                    },
                    {
                        "description": "Remove old logs",
                        "command": "journalctl --vacuum-time=7d",
                        "verification": "df -h {partition}"
                    }
                ],
                "tags": ["disk", "storage"]
            },
            "service_down": {
                "title": "Service {service_name} Down",
                "description": "Restore service {service_name} on {hostname}.",
                "steps": [
                    {
                        "description": "Check service status",
                        "command": "systemctl status {service_name}",
                        "verification": "Service should be active (running)"
                    },
                    {
                        "description": "Check service logs",
                        "command": "journalctl -u {service_name} --no-pager | tail -n 50",
                        "verification": "Identify crash reason"
                    },
                    {
                        "description": "Attempt restart",
                        "command": "systemctl restart {service_name}",
                        "verification": "systemctl is-active {service_name}"
                    }
                ],
                "tags": ["service", "availability"]
            }
        }

    def generate_runbook(self, alert_type: str, context: Dict[str, Any]) -> Optional[Runbook]:
        """
        Generate a runbook for a specific alert.
        
        Args:
            alert_type: Type of alert (e.g., 'high_cpu', 'disk_space')
            context: Dictionary containing variables for the template (e.g., hostname, service_name)
        """
        template = self._templates.get(alert_type)
        if not template:
            logger.warning(f"No runbook template found for alert type: {alert_type}")
            return None

        try:
            title = template["title"].format(**context)
            description = template["description"].format(**context)
            
            steps = []
            for i, step_data in enumerate(template["steps"], 1):
                cmd = step_data.get("command", "").format(**context) if step_data.get("command") else None
                ver = step_data.get("verification", "").format(**context) if step_data.get("verification") else None
                
                steps.append(RunbookStep(
                    order=i,
                    description=step_data["description"],
                    command=cmd,
                    verification=ver
                ))

            return Runbook(
                id=f"rb-{int(datetime.now().timestamp())}",
                title=title,
                description=description,
                steps=steps,
                tags=template.get("tags", [])
            )
        except KeyError as e:
            logger.error(f"Missing context variable for runbook generation: {e}")
            return None

    def suggest_runbooks(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Suggest runbooks based on keywords (simulating AI search)."""
        suggestions = []
        for key, tmpl in self._templates.items():
            score = 0
            text = (tmpl["title"] + " " + tmpl["description"] + " " + " ".join(tmpl.get("tags", []))).lower()
            
            for kw in keywords:
                if kw.lower() in text:
                    score += 1
            
            if score > 0:
                suggestions.append({
                    "type": key,
                    "title": tmpl["title"],
                    "relevance": score
                })
        
        return sorted(suggestions, key=lambda x: x["relevance"], reverse=True)
