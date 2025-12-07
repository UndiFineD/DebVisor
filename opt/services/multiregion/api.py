"""
Multi-region Support REST API - HTTP interface for multi-region operations

Provides RESTful API endpoints for managing regions, replication, and failover.
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from opt.services.multiregion.core import (
    MultiRegionManager,
    RegionStatus,
    FailoverStrategy,
    ResourceType,
    get_multi_region_manager,
)


class MultiRegionAPI:
    """REST API interface for multi-region operations."""

    def __init__(self, manager: Optional[MultiRegionManager] = None):
        """Initialize API.

        Args:
            manager: MultiRegionManager instance
        """
        self.manager = manager or get_multi_region_manager()
        self.logger = logging.getLogger("DebVisor.MultiRegionAPI")

    def _json_response(
        self,
        status: str = "success",
        data: Optional[Any] = None,
        message: str = "",
        status_code: int = 200
    ) -> Tuple[Dict[str, Any], int]:
        """Create JSON response.

        Args:
            status: Response status
            data: Response data
            message: Response message
            status_code: HTTP status code

        Returns:
            (response_dict, status_code)
        """
        response = {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message
        }

        if data is not None:
            response["data"] = data

        return response, status_code

    def _error_response(
        self,
        message: str,
        error: str = "error",
        status_code: int = 400
    ) -> Tuple[Dict[str, Any], int]:
        """Create error response.

        Args:
            message: Error message
            error: Error type
            status_code: HTTP status code

        Returns:
            (response_dict, status_code)
        """
        return self._json_response(
            status="error",
            message=message,
            data={"error": error},
            status_code=status_code
        )

    # ========================================================================
    # Region Endpoints
    # ========================================================================

    def register_region(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/regions - Register a new region.

        Args:
            request_data: Request JSON data

        Returns:
            (response, status_code)
        """
        try:
            required_fields = ["name", "location", "api_endpoint"]
            if not all(field in request_data for field in required_fields):
                return self._error_response("Missing required fields", "validation_error", 400)

            region = self.manager.register_region(
                name=request_data["name"],
                location=request_data["location"],
                api_endpoint=request_data["api_endpoint"],
                is_primary=request_data.get("is_primary", False),
                capacity_vms=request_data.get("capacity_vms", 1000)
            )

            self.logger.info(f"Region registered: {region.region_id}")
            return self._json_response(
                data=region.to_dict(),
                message=f"Region {region.region_id} registered",
                status_code=201
            )

        except Exception as e:
            self.logger.error(f"Error registering region: {e}")
            return self._error_response(str(e), "registration_error", 500)

    def list_regions(self, status: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/regions - List regions.

        Args:
            status: Optional status filter

        Returns:
            (response, status_code)
        """
        try:
            status_filter = None
            if status:
                try:
                    status_filter = RegionStatus(status)
                except ValueError:
                    return self._error_response(
                        f"Invalid status: {status}", "validation_error", 400)

            regions = self.manager.list_regions(status=status_filter)
            return self._json_response(
                data=[r.to_dict() for r in regions],
                message=f"Retrieved {len(regions)} regions"
            )

        except Exception as e:
            self.logger.error(f"Error listing regions: {e}")
            return self._error_response(str(e), "list_error", 500)

    def get_region(self, region_id: str) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/regions/:region_id - Get region details.

        Args:
            region_id: Region ID

        Returns:
            (response, status_code)
        """
        try:
            region = self.manager.get_region(region_id)
            if not region:
                return self._error_response(f"Region not found: {region_id}", "not_found", 404)

            return self._json_response(data=region.to_dict())

        except Exception as e:
            self.logger.error(f"Error getting region: {e}")
            return self._error_response(str(e), "get_error", 500)

    def check_region_health(self, region_id: str) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/regions/:region_id/health - Check region health.

        Args:
            region_id: Region ID

        Returns:
            (response, status_code)
        """
        try:
            import asyncio

            # Run async health check
            loop = asyncio.new_event_loop()
            try:
                status = loop.run_until_complete(
                    self.manager.check_region_health(region_id)
                )
            finally:
                loop.close()

            region = self.manager.get_region(region_id)
            if not region:
                return self._error_response(f"Region not found: {region_id}", "not_found", 404)

            return self._json_response(
                data={
                    "region_id": region_id,
                    "status": status.value,
                    "latency_ms": region.latency_ms,
                    "last_heartbeat": region.last_heartbeat.isoformat()
                }
            )

        except Exception as e:
            self.logger.error(f"Error checking health: {e}")
            return self._error_response(str(e), "health_check_error", 500)

    def get_region_stats(self, region_id: str) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/regions/:region_id/stats - Get region statistics.

        Args:
            region_id: Region ID

        Returns:
            (response, status_code)
        """
        try:
            stats = self.manager.get_region_statistics(region_id)
            if not stats:
                return self._error_response(f"Region not found: {region_id}", "not_found", 404)

            return self._json_response(data=stats)

        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return self._error_response(str(e), "stats_error", 500)

    # ========================================================================
    # Replication Endpoints
    # ========================================================================

    def setup_replication(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/replication/setup - Setup replication.

        Args:
            request_data: Request JSON data

        Returns:
            (response, status_code)
        """
        try:
            required_fields = ["source_region_id", "target_region_id", "resource_types"]
            if not all(field in request_data for field in required_fields):
                return self._error_response("Missing required fields", "validation_error", 400)

            resource_types = []
            for rt in request_data["resource_types"]:
                try:
                    resource_types.append(ResourceType(rt))
                except ValueError:
                    return self._error_response(
                        f"Invalid resource type: {rt}", "validation_error", 400)

            config = self.manager.setup_replication(
                source_region_id=request_data["source_region_id"],
                target_region_id=request_data["target_region_id"],
                resource_types=resource_types,
                sync_interval_seconds=request_data.get("sync_interval_seconds", 300),
                bidirectional=request_data.get("bidirectional", False)
            )

            self.logger.info(
                f"Replication setup: {config.source_region_id} -> {config.target_region_id}")
            return self._json_response(
                data=config.to_dict(),
                message="Replication configured",
                status_code=201
            )

        except Exception as e:
            self.logger.error(f"Error setting up replication: {e}")
            return self._error_response(str(e), "setup_error", 500)

    def sync_resource(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/replication/sync - Sync a resource.

        Args:
            request_data: Request JSON data

        Returns:
            (response, status_code)
        """
        try:
            required_fields = ["resource_id", "source_region_id", "target_region_id"]
            if not all(field in request_data for field in required_fields):
                return self._error_response("Missing required fields", "validation_error", 400)

            import asyncio

            loop = asyncio.new_event_loop()
            try:
                success = loop.run_until_complete(
                    self.manager.sync_resource(
                        resource_id=request_data["resource_id"],
                        source_region_id=request_data["source_region_id"],
                        target_region_id=request_data["target_region_id"]
                    )
                )
            finally:
                loop.close()

            if success:
                self.logger.info(f"Resource synced: {request_data['resource_id']}")
                return self._json_response(
                    data={"resource_id": request_data["resource_id"], "success": True},
                    message="Resource synced"
                )
            else:
                return self._error_response("Sync failed", "sync_error", 500)

        except Exception as e:
            self.logger.error(f"Error syncing resource: {e}")
            return self._error_response(str(e), "sync_error", 500)

    def get_replication_status(self, resource_id: str) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/replication/:resource_id/status - Get replication status.

        Args:
            resource_id: Resource ID

        Returns:
            (response, status_code)
        """
        try:
            status = self.manager.get_replication_status(resource_id)
            if not status:
                return self._error_response(f"Resource not found: {resource_id}", "not_found", 404)

            return self._json_response(data=status)

        except Exception as e:
            self.logger.error(f"Error getting replication status: {e}")
            return self._error_response(str(e), "status_error", 500)

    # ========================================================================
    # Failover Endpoints
    # ========================================================================

    def execute_failover(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/failover/execute - Execute failover.

        Args:
            request_data: Request JSON data

        Returns:
            (response, status_code)
        """
        try:
            required_fields = ["from_region_id", "to_region_id"]
            if not all(field in request_data for field in required_fields):
                return self._error_response("Missing required fields", "validation_error", 400)

            import asyncio

            loop = asyncio.new_event_loop()
            try:
                success, event = loop.run_until_complete(
                    self.manager.perform_failover(
                        from_region_id=request_data["from_region_id"],
                        to_region_id=request_data["to_region_id"],
                        strategy=FailoverStrategy(request_data.get("strategy", "automatic")),
                        reason=request_data.get("reason", "API-initiated failover")
                    )
                )
            finally:
                loop.close()

            if success:
                self.logger.info(f"Failover executed: {event.event_id}")
                return self._json_response(
                    data=event.to_dict(),
                    message="Failover completed",
                    status_code=201
                )
            else:
                self.logger.error(f"Failover failed: {event.notes}")
                return self._error_response(
                    f"Failover failed: {event.notes}",
                    "failover_error",
                    500
                )

        except Exception as e:
            self.logger.error(f"Error executing failover: {e}")
            return self._error_response(str(e), "failover_error", 500)

    def get_failover_history(
        self,
        region_id: Optional[str] = None,
        limit: int = 50
    ) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/failover/history - Get failover history.

        Args:
            region_id: Optional region filter
            limit: Maximum results

        Returns:
            (response, status_code)
        """
        try:
            events = self.manager.get_failover_history(
                region_id=region_id,
                limit=limit
            )

            return self._json_response(
                data=[e.to_dict() for e in events],
                message=f"Retrieved {len(events)} failover events"
            )

        except Exception as e:
            self.logger.error(f"Error getting failover history: {e}")
            return self._error_response(str(e), "history_error", 500)

    # ========================================================================
    # VM Replication Endpoints
    # ========================================================================

    def replicate_vm(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """POST /api/v1/vms/replicate - Register VM for replication.

        Args:
            request_data: Request JSON data

        Returns:
            (response, status_code)
        """
        try:
            required_fields = ["vm_id", "primary_region_id", "replica_regions"]
            if not all(field in request_data for field in required_fields):
                return self._error_response("Missing required fields", "validation_error", 400)

            resource = self.manager.replicate_vm(
                vm_id=request_data["vm_id"],
                primary_region_id=request_data["primary_region_id"],
                replica_regions=request_data["replica_regions"]
            )

            self.logger.info(f"VM registered for replication: {request_data['vm_id']}")
            return self._json_response(
                data=resource.to_dict(),
                message="VM registered for replication",
                status_code=201
            )

        except Exception as e:
            self.logger.error(f"Error registering VM: {e}")
            return self._error_response(str(e), "registration_error", 500)

    # ========================================================================
    # Global Endpoints
    # ========================================================================

    def get_global_stats(self) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/stats - Get global statistics.

        Returns:
            (response, status_code)
        """
        try:
            stats = self.manager.get_global_statistics()
            return self._json_response(data=stats)

        except Exception as e:
            self.logger.error(f"Error getting global stats: {e}")
            return self._error_response(str(e), "stats_error", 500)

    def get_health(self) -> Tuple[Dict[str, Any], int]:
        """GET /api/v1/health - Health check endpoint.

        Returns:
            (response, status_code)
        """
        return self._json_response(
            data={"service": "multi-region", "status": "operational"},
            message="Service is operational"
        )


def create_flask_app(manager: Optional[MultiRegionManager] = None):
    """Create Flask application with multi-region API.

    Args:
        manager: MultiRegionManager instance

    Returns:
        Flask app instance
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        raise ImportError("Flask is required for API. Install with: pip install flask")

    app = Flask(__name__)
    api = MultiRegionAPI(manager)

    # Region endpoints
    @app.route("/api/v1/regions", methods=["POST"])
    def regions_register():
        response, status = api.register_region(request.get_json() or {})
        return jsonify(response), status

    @app.route("/api/v1/regions", methods=["GET"])
    def regions_list():
        response, status = api.list_regions(request.args.get("status"))
        return jsonify(response), status

    @app.route("/api/v1/regions/<region_id>", methods=["GET"])
    def regions_get(region_id):
        response, status = api.get_region(region_id)
        return jsonify(response), status

    @app.route("/api/v1/regions/<region_id>/health", methods=["POST"])
    def regions_health(region_id):
        response, status = api.check_region_health(region_id)
        return jsonify(response), status

    @app.route("/api/v1/regions/<region_id>/stats", methods=["GET"])
    def regions_stats(region_id):
        response, status = api.get_region_stats(region_id)
        return jsonify(response), status

    # Replication endpoints
    @app.route("/api/v1/replication/setup", methods=["POST"])
    def replication_setup():
        response, status = api.setup_replication(request.get_json() or {})
        return jsonify(response), status

    @app.route("/api/v1/replication/sync", methods=["POST"])
    def replication_sync():
        response, status = api.sync_resource(request.get_json() or {})
        return jsonify(response), status

    @app.route("/api/v1/replication/<resource_id>/status", methods=["GET"])
    def replication_status(resource_id):
        response, status = api.get_replication_status(resource_id)
        return jsonify(response), status

    # Failover endpoints
    @app.route("/api/v1/failover/execute", methods=["POST"])
    def failover_execute():
        response, status = api.execute_failover(request.get_json() or {})
        return jsonify(response), status

    @app.route("/api/v1/failover/history", methods=["GET"])
    def failover_history():
        region_id = request.args.get("region_id")
        limit = request.args.get("limit", 50, type=int)
        response, status = api.get_failover_history(region_id, limit)
        return jsonify(response), status

    # VM endpoints
    @app.route("/api/v1/vms/replicate", methods=["POST"])
    def vms_replicate():
        response, status = api.replicate_vm(request.get_json() or {})
        return jsonify(response), status

    # Global endpoints
    @app.route("/api/v1/stats", methods=["GET"])
    def global_stats():
        response, status = api.get_global_stats()
        return jsonify(response), status

    @app.route("/api/v1/health", methods=["GET"])
    def health():
        response, status = api.get_health()
        return jsonify(response), status

    return app


if __name__ == "__main__":
    app = create_flask_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
