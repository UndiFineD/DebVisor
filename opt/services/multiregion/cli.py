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


"""
Multi-region Support CLI - Command-line interface for multi-region operations

Provides comprehensive CLI commands for managing regions, replication, and failover.
"""

from typing import List, Optional
import argparse
import asyncio
import json

# Configure logging
try:
    from opt.core.logging import configure_logging
except ImportError:

    def configure_logging(**kwargs):  # type: ignore[misc] -> None:
        """Placeholder docstring."""
        pass

from opt.core.cli_utils import format_table, setup_common_args, handle_cli_error

from opt.services.multiregion.core import (
    MultiRegionManager,
    RegionStatus,
    FailoverStrategy,
    ResourceType,
    get_multi_region_manager,
)


class MultiRegionCLI:
    """CLI interface for multi-region operations."""

    def __init__(self, manager: Optional[MultiRegionManager] = None) -> None:
        """Initialize CLI.

        Args:
            manager: MultiRegionManager instance
        """
        self.manager=manager or get_multi_region_manager()
        self.parser=self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        _parser = argparse.ArgumentParser(
            _description = "DebVisor Multi-region Operations CLI",
            _formatter_class = argparse.RawDescriptionHelpFormatter,
            _epilog = "Examples:\n"
            "  debvisor-region region add us-east-1 'US East 1' https://api.us-east-1.internal --primary\n"
            "  debvisor-region region list\n"
            "  debvisor-region region health-check us-east-1\n"
            "  debvisor-region replication setup us-east-1 us-west-1 vm, config\n"
            "  debvisor-region failover execute us-east-1 us-west-1\n"
            "  debvisor-region failover history\n",
        )

        setup_common_args(parser)

        _subparsers=parser.add_subparsers(dest="command", help="Command")

        # Region commands
        _region_parser=subparsers.add_parser("region", help="Region management")
        _region_subparsers=region_parser.add_subparsers(dest="region_cmd")

        # region add
        _add_parser=region_subparsers.add_parser("add", help="Add a region")
        add_parser.add_argument("region_id", help="Region ID")
        add_parser.add_argument("name", help="Region name")
        add_parser.add_argument("api_endpoint", help="API endpoint URL")
        add_parser.add_argument("--primary", action="store_true", help="Set as primary")
        add_parser.add_argument(
            "--capacity", type=int, default=1000, help="VM capacity"
        )
        add_parser.set_defaults(handler=self._cmd_region_add)

        # region list
        _list_parser=region_subparsers.add_parser("list", help="List regions")
        list_parser.add_argument(
            "--status",
            _choices=["healthy", "degraded", "unreachable", "recovering"],
            _help="Filter by status",
        )
        list_parser.add_argument("--format", choices=["table", "json"], default="table")
        list_parser.set_defaults(handler=self._cmd_region_list)

        # region show
        _show_parser=region_subparsers.add_parser("show", help="Show region details")
        show_parser.add_argument("region_id", help="Region ID")
        show_parser.add_argument("--format", choices=["table", "json"], default="table")
        show_parser.set_defaults(handler=self._cmd_region_show)

        # region health-check
        health_parser = region_subparsers.add_parser(
            "health-check", help="Check region health"
        )
        health_parser.add_argument("region_id", help="Region ID")
        health_parser.set_defaults(handler=self._cmd_region_health_check)

        # region stats
        stats_parser = region_subparsers.add_parser(
            "stats", help="Get region statistics"
        )
        stats_parser.add_argument("region_id", help="Region ID")
        stats_parser.set_defaults(handler=self._cmd_region_stats)

        # Replication commands
        repl_parser = subparsers.add_parser(
            "replication", help="Replication management"
        )
        _repl_subparsers=repl_parser.add_subparsers(dest="repl_cmd")

        # replication setup
        _setup_parser=repl_subparsers.add_parser("setup", help="Setup replication")
        setup_parser.add_argument("source", help="Source region")
        setup_parser.add_argument("target", help="Target region")
        setup_parser.add_argument(
            "resource_types",
            _help="Comma-separated resource types (vm, storage, network, config, state)",
        )
        setup_parser.add_argument(
            "--interval", type=int, default=300, help="Sync interval in seconds"
        )
        setup_parser.add_argument(
            "--bidirectional", action="store_true", help="Enable bidirectional sync"
        )
        setup_parser.set_defaults(handler=self._cmd_replication_setup)

        # replication status
        status_parser = repl_subparsers.add_parser(
            "status", help="Get replication status"
        )
        status_parser.add_argument("resource_id", help="Resource ID")
        status_parser.set_defaults(handler=self._cmd_replication_status)

        # replication sync
        _sync_parser=repl_subparsers.add_parser("sync", help="Sync resource")
        sync_parser.add_argument("resource_id", help="Resource ID")
        sync_parser.add_argument("source", help="Source region")
        sync_parser.add_argument("target", help="Target region")
        sync_parser.set_defaults(handler=self._cmd_replication_sync)

        # Failover commands
        _fail_parser=subparsers.add_parser("failover", help="Failover management")
        _fail_subparsers=fail_parser.add_subparsers(dest="fail_cmd")

        # failover execute
        _exec_parser=fail_subparsers.add_parser("execute", help="Execute failover")
        exec_parser.add_argument("from_region", help="Source region")
        exec_parser.add_argument("to_region", help="Target region")
        exec_parser.add_argument(
            "--strategy",
            _choices = ["automatic", "manual", "graceful", "cascading"],
            _default="automatic",
            _help="Failover strategy",
        )
        exec_parser.add_argument(
            "--reason", default="Manual failover", help="Reason for failover"
        )
        exec_parser.add_argument("--force", action="store_true", help="Force failover")
        exec_parser.set_defaults(handler=self._cmd_failover_execute)

        # failover history
        hist_parser = fail_subparsers.add_parser(
            "history", help="View failover history"
        )
        hist_parser.add_argument("--region", help="Filter by region")
        hist_parser.add_argument("--limit", type=int, default=20, help="Max results")
        hist_parser.add_argument("--format", choices=["table", "json"], default="table")
        hist_parser.set_defaults(handler=self._cmd_failover_history)

        # VM replication commands
        _vm_parser=subparsers.add_parser("vm", help="VM replication management")
        _vm_subparsers=vm_parser.add_subparsers(dest="vm_cmd")

        # vm replicate
        rep_parser = vm_subparsers.add_parser(
            "replicate", help="Register VM for replication"
        )
        rep_parser.add_argument("vm_id", help="VM ID")
        rep_parser.add_argument("primary_region", help="Primary region")
        rep_parser.add_argument(
            "replica_regions", help="Comma-separated replica regions"
        )
        rep_parser.set_defaults(handler=self._cmd_vm_replicate)

        # Global commands
        _global_parser=subparsers.add_parser("global", help="Global statistics")
        global_parser.set_defaults(handler=self._cmd_global_stats)

        return parser

    async def _cmd_region_add(self, args: argparse.Namespace) -> None:
        """Add a region."""
        try:
            region = self.manager.register_region(
                _name=args.name,
                _location=args.region_id,
                _api_endpoint=args.api_endpoint,
                _is_primary=args.primary,
                _capacity_vms=args.capacity,
            )

            print(f"? Region added: {region.region_id}")
            print(f"   Name: {region.name}")
            print(f"   Location: {region.location}")
            print(f"   API: {region.api_endpoint}")
            print(f"   Primary: {region.is_primary}")
            print(f"   Capacity: {region.capacity_vms} VMs")

        except Exception as e:
            print(f"? Error adding region: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_region_list(self, args: argparse.Namespace) -> None:
        """List regions."""
        try:
            status_filter = None
            if args.status:
                _status_filter=RegionStatus(args.status)

            _regions=self.manager.list_regions(status=status_filter)

            if args.format == "json":
                print(json.dumps([r.to_dict() for r in regions], indent=2))
            else:
                _headers = [
                    "Region ID",
                    "Name",
                    "Location",
                    "Status",
                    "Primary",
                    "VMs",
                    "Latency",
                ]
                rows = []
                for r in regions:
                    rows.append(
                        [
                            r.region_id,
                            r.name,
                            r.location,
                            r.status.value,
                            "Yes" if r.is_primary else "No",
                            f"{r.current_vms}/{r.capacity_vms}",
                            f"{r.latency_ms:.0f}ms" if r.latency_ms > 0 else "N/A",
                        ]
                    )
                print(format_table(rows, headers=headers, tablefmt="grid"))

            print(f"\nTotal: {len(regions)} regions")

        except Exception as e:
            print(f"? Error listing regions: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_region_show(self, args: argparse.Namespace) -> None:
        """Show region details."""
        try:
            _region=self.manager.get_region(args.region_id)
            if not region:
                print(f"? Region not found: {args.region_id}", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

            if args.format == "json":
                print(json.dumps(region.to_dict(), indent=2))  # type: ignore[union-attr]
            else:
                print(f"Region: {region.region_id}")  # type: ignore[union-attr]
                print(f"  Name: {region.name}")  # type: ignore[union-attr]
                print(f"  Location: {region.location}")  # type: ignore[union-attr]
                print(f"  API Endpoint: {region.api_endpoint}")  # type: ignore[union-attr]
                print(f"  Primary: {'Yes' if region.is_primary else 'No'}")  # type: ignore[union-attr]
                print(f"  Status: {region.status.value}")  # type: ignore[union-attr]
                print(f"  VM Capacity: {region.capacity_vms}")  # type: ignore[union-attr]
                print(f"  Current VMs: {region.current_vms}")  # type: ignore[union-attr]
                print(
                    f"  Utilization: {(region.current_vms / region.capacity_vms * 100):.1f}%"  # type: ignore[union-attr]
                )
                print(f"  Latency: {region.latency_ms:.1f}ms")  # type: ignore[union-attr]
                print(f"  Bandwidth: {region.bandwidth_mbps:.1f} Mbps")  # type: ignore[union-attr]
                print(f"  Replication Lag: {region.replication_lag_seconds:.1f}s")  # type: ignore[union-attr]
                print(f"  Last Heartbeat: {region.last_heartbeat.isoformat()}")  # type: ignore[union-attr]

        except Exception as e:
            print(f"? Error showing region: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_region_health_check(self, args: argparse.Namespace) -> None:
        """Check region health."""
        try:
            print(f"Checking health of {args.region_id}...")
            _status=await self.manager.check_region_health(args.region_id)

            _region=self.manager.get_region(args.region_id)
            if not region:
                print(f"? Region not found: {args.region_id}", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

            status_emoji = {
                RegionStatus.HEALTHY: "?",
                RegionStatus.DEGRADED: "[warn]?",
                RegionStatus.UNREACHABLE: "?",
                RegionStatus.RECOVERING: "[U+1F504]",
                RegionStatus.UNKNOWN: "?",
            }

            print(f"{status_emoji.get(status, '?')} Status: {status.value}")
            print(f"  Latency: {region.latency_ms:.1f}ms")  # type: ignore[union-attr]
            print(f"  Last Check: {region.last_heartbeat.isoformat()}")  # type: ignore[union-attr]

        except Exception as e:
            print(f"? Error checking health: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_region_stats(self, args: argparse.Namespace) -> None:
        """Get region statistics."""
        try:
            _stats=self.manager.get_region_statistics(args.region_id)
            if not stats:
                print(f"? Region not found: {args.region_id}", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

            print(json.dumps(stats, indent=2))

        except Exception as e:
            print(f"? Error getting statistics: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_replication_setup(self, args: argparse.Namespace) -> None:
        """Setup replication."""
        try:
            resource_types = [
                ResourceType(rt.strip()) for rt in args.resource_types.split(", ")
            ]

            self.manager.setup_replication(
                _source_region_id = args.source,
                _target_region_id = args.target,
                _resource_types=resource_types,
                _sync_interval_seconds = args.interval,
                _bidirectional=args.bidirectional,
            )

            print(f"? Replication configured: {args.source} -> {args.target}")
            print(f"   Resource Types: {', '.join(rt.value for rt in resource_types)}")
            print(f"   Sync Interval: {args.interval}s")
            print(f"   Bidirectional: {'Yes' if args.bidirectional else 'No'}")

        except ValueError as e:
            print(f"? Invalid resource type: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]
        except Exception as e:
            print("? Error setting up replication: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_replication_status(self, args: argparse.Namespace) -> None:
        """Get replication status."""
        try:
            _status=self.manager.get_replication_status(args.resource_id)
            if not status:
                print(f"? Resource not found: {args.resource_id}", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

            print(json.dumps(status, indent=2))

        except Exception as e:
            print(f"? Error getting replication status: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_replication_sync(self, args: argparse.Namespace) -> None:
        """Sync resource."""
        try:
            print(f"Syncing {args.resource_id} from {args.source} to {args.target}...")
            success = await self.manager.sync_resource(
                _resource_id = args.resource_id,
                _source_region_id = args.source,
                _target_region_id = args.target,
            )

            if success:
                print("? Sync completed successfully")
            else:
                print("? Sync failed", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

        except Exception as e:
            print(f"? Error syncing resource: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_failover_execute(self, args: argparse.Namespace) -> None:
        """Execute failover."""
        try:
            _strategy=FailoverStrategy(args.strategy)

            if not args.force:
                response = input(
                    f"[warn]?  Failover {args.from_region} -> {args.to_region}. Continue? (yes/no): "
                )
                if response.lower() != "yes":
                    print("Failover cancelled")
                    return

            print("Executing failover...")
            success, event = await self.manager.perform_failover(
                _from_region_id = args.from_region,
                _to_region_id = args.to_region,
                _strategy = strategy,
                _reason = args.reason,
            )

            if success:
                print("? Failover completed")
                print(f"   Event ID: {event.event_id}")
                print(f"   Duration: {event.duration_seconds:.1f}s")
                print(f"   Resources Affected: {event.affected_resources}")
            else:
                print(f"? Failover failed: {event.notes}", file=sys.stderr)  # type: ignore[name-defined]
                sys.exit(1)  # type: ignore[name-defined]

        except Exception as e:
            print(f"? Error executing failover: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_failover_history(self, args: argparse.Namespace) -> None:
        """View failover history."""
        try:
            events = self.manager.get_failover_history(
                _region_id = args.region, limit=args.limit
            )

            if args.format == "json":
                print(json.dumps([e.to_dict() for e in events], indent=2))
            else:
                if not events:
                    print("No failover events")
                    return

                _headers = [
                    "Event ID",
                    "Timestamp",
                    "From",
                    "To",
                    "Resources",
                    "Success",
                    "Duration",
                ]
                rows = []
                for e in events:
                    rows.append(
                        [
                            e.event_id,
                            e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            e.from_region_id,
                            e.to_region_id,
                            e.affected_resources,
                            "?" if e.success else "?",
                            f"{e.duration_seconds:.1f}s",
                        ]
                    )
                print(format_table(rows, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"? Error getting failover history: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_vm_replicate(self, args: argparse.Namespace) -> None:
        """Register VM for replication."""
        try:
            _replica_regions=[r.strip() for r in args.replica_regions.split(", ")]

            self.manager.replicate_vm(
                _vm_id=args.vm_id,
                _primary_region_id = args.primary_region,
                _replica_regions=replica_regions,
            )

            print(f"? VM registered for replication: {args.vm_id}")
            print(f"   Primary Region: {args.primary_region}")
            print(f"   Replica Regions: {', '.join(replica_regions)}")

        except Exception as e:
            print(f"? Error registering VM: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def _cmd_global_stats(self, args: argparse.Namespace) -> None:
        """Get global statistics."""
        try:
            _stats=self.manager.get_global_statistics()
            print(json.dumps(stats, indent=2))

        except Exception as e:
            print(f"? Error getting global statistics: {e}", file=sys.stderr)  # type: ignore[name-defined]
            sys.exit(1)  # type: ignore[name-defined]

    async def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI with given arguments.

        Args:
            args: Command-line arguments
        """
        _parsed_args=self.parser.parse_args(args)

        if not hasattr(parsed_args, "handler"):
            self.parser.print_help()
            return 0

        await parsed_args.handler(parsed_args)
        return 0

    @handle_cli_error

    def run_sync(self, args: Optional[List[str]] = None) -> int:
        """Run CLI synchronously (wrapper for async).

        Args:
            args: Command-line arguments
        """
        return asyncio.run(self.run(args))


def main() -> None:
    """Main entry point."""
    configure_logging(service_name="multiregion-cli")
    _cli=MultiRegionCLI()
    cli.run_sync()


if __name__ == "__main__":
    main()
