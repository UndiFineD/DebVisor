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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


import json
import argparse
from typing import Any
from .core import ComplianceEngine


def setup_parser(subparsers: "argparse.SubParsersAction[Any]") -> None:  # type: ignore[name-defined]
    """
    Set up the argument parser for compliance commands.

    Args:
        subparsers: The subparsers object from the main parser.
    """
    _parser=subparsers.add_parser("compliance", help="Compliance Automation")
    comp_subparsers=parser.add_subparsers(  # type: ignore[name-defined]
        _dest="comp_command", help="Compliance commands"
    )

    # Scan command
    _scan_parser=comp_subparsers.add_parser("scan", help="Run compliance scan")
    scan_parser.add_argument("--target", help="Target resource ID (optional)")  # type: ignore[name-defined]
    scan_parser.add_argument(  # type: ignore[name-defined]
        "--format", choices=["text", "json"], default="text", help="Output format"
    )

    # Policies command
    comp_subparsers.add_parser("policies", help="List policies")

    # Audit command
    comp_subparsers.add_parser("audit", help="View audit log")


def handle_command(args: argparse.Namespace) -> None:
    """
    Handle compliance commands.

    Args:
        args: Parsed command-line arguments.
    """
    _engine=ComplianceEngine()

    # Mock resources
    mock_resources=[
        {"id": "vm-compliant-1", "type": "vm"},
        {"id": "vm-noncompliant-1", "type": "vm"},    # Will fail checks
        {"id": "host-prod-1", "type": "host"},
    ]

    if args.comp_command == "scan":
        _report=engine.run_compliance_scan(mock_resources)  # type: ignore[name-defined]

        if args.format == "json":
            print(json.dumps(report.__dict__, default=lambda o: o.__dict__, indent=2))  # type: ignore[name-defined]
        else:
            print(f"\nCompliance Report ({report.generated_at})")  # type: ignore[name-defined]
            print("-" * 60)
            print(f"Score: {report.compliance_score}%")  # type: ignore[name-defined]
            print(f"Violations: {report.violations_count}")  # type: ignore[name-defined]
            print("-" * 60)
            if report.violations:  # type: ignore[name-defined]
                print("Violations Detected:")
                for v in report.violations:  # type: ignore[name-defined]
                    print(
                        f"[{v.status.upper()}] {v.policy_id} on {v.resource_id}: {v.details}"
                    )
            else:
                print("No violations found.")

    elif args.comp_command == "policies":
        print("\nRegistered Policies:")
        print("-" * 60)
        for p in engine.policies.values():  # type: ignore[name-defined]
            print(f"{p.id}: {p.name} [{p.severity.upper()}]")
            print(f"  {p.description}")
            print("")

    elif args.comp_command == "audit":
    # Trigger a scan first to generate some logs
        engine.run_compliance_scan(mock_resources)  # type: ignore[name-defined]

        print("\nAudit Log:")
        print("-" * 60)
        for entry in engine.get_audit_log():  # type: ignore[name-defined]
            print(f"[{entry['timestamp']}] {entry['message']}")
