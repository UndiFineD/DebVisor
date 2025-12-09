import json
import argparse
from typing import Any
from .core import ComplianceEngine


def setup_parser(subparsers: "argparse._SubParsersAction[Any]") -> None:
    """
    Set up the argument parser for compliance commands.

    Args:
        subparsers: The subparsers object from the main parser.
    """
    parser = subparsers.add_parser("compliance", help="Compliance Automation")
    comp_subparsers = parser.add_subparsers(
        dest="comp_command", help="Compliance commands"
    )

    # Scan command
    scan_parser = comp_subparsers.add_parser("scan", help="Run compliance scan")
    scan_parser.add_argument("--target", help="Target resource ID (optional)")
    scan_parser.add_argument(
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
    engine = ComplianceEngine()

    # Mock resources
    mock_resources = [
        {"id": "vm-compliant-1", "type": "vm"},
        {"id": "vm-noncompliant-1", "type": "vm"},  # Will fail checks
        {"id": "host-prod-1", "type": "host"},
    ]

    if args.comp_command == "scan":
        report = engine.run_compliance_scan(mock_resources)

        if args.format == "json":
            print(json.dumps(report.__dict__, default=lambda o: o.__dict__, indent=2))
        else:
            print(f"\nCompliance Report ({report.generated_at})")
            print("-" * 60)
            print(f"Score: {report.compliance_score}%")
            print(f"Violations: {report.violations_count}")
            print("-" * 60)
            if report.violations:
                print("Violations Detected:")
                for v in report.violations:
                    print(
                        f"[{v.status.upper()}] {v.policy_id} on {v.resource_id}: {v.details}"
                    )
            else:
                print("No violations found.")

    elif args.comp_command == "policies":
        print("\nRegistered Policies:")
        print("-" * 60)
        for p in engine.policies.values():
            print(f"{p.id}: {p.name} [{p.severity.upper()}]")
            print(f"  {p.description}")
            print("")

    elif args.comp_command == "audit":
        # Trigger a scan first to generate some logs
        engine.run_compliance_scan(mock_resources)

        print("\nAudit Log:")
        print("-" * 60)
        for entry in engine.get_audit_log():
            print(f"[{entry['timestamp']}] {entry['message']}")
