"""Storage Management Routes - Snapshot Operations

Provides endpoints for snapshot creation, monitoring, and deletion.
Integrates with RPC service for backend storage operations.
"""

from typing import Any, Union, Tuple
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required, current_user
from datetime import datetime, timedelta, timezone
from opt.web.panel.core.rpc_client import get_rpc_client, RPCClientError
from opt.web.panel.models.snapshot import Snapshot
from opt.web.panel.models.node import Node
from opt.web.panel.models.audit_log import AuditLog
from opt.web.panel.extensions import db, limiter
from opt.web.panel.rbac import require_permission, Resource, Action

# Create blueprint
storage_bp = Blueprint("storage", __name__, url_prefix="/storage")


@storage_bp.route("/snapshots", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.READ)
@limiter.limit("100 per minute")  # type: ignore
def list_snapshots() -> Any:
    """List all storage snapshots.

    GET: Display paginated snapshot list
    """
    page = request.args.get("page", 1, type=int)
    per_page = 20
    node_id = request.args.get("node_id", None, type=int)
    status_filter = request.args.get("status", None)

    query = Snapshot.query
    if node_id:
        query = query.filter_by(node_id=node_id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(Snapshot.created_at.desc()).paginate(
        page=page, per_page=per_page
    )
    snapshots = pagination.items

    # Log view
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="read",
        resource_type="snapshot",
        action="Viewed snapshot list",
        status="success",
        ip_address=request.remote_addr,
    )

    return render_template(
        "storage/list.html", snapshots=snapshots, pagination=pagination
    )


@storage_bp.route("/snapshots/<int:snapshot_id>", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.READ)
@limiter.limit("100 per minute")  # type: ignore
def view_snapshot(snapshot_id: int) -> Any:
    """View snapshot details.

    GET: Display snapshot information and status
    """
    snapshot = Snapshot.query.get(snapshot_id)
    if not snapshot:
        flash("Snapshot not found", "error")
        return redirect(url_for("storage.list_snapshots"))

    # Log view
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="read",
        resource_type="snapshot",
        action=f"Viewed snapshot: {snapshot.name}",
        status="success",
        resource_id=str(snapshot_id),
        ip_address=request.remote_addr,
    )

    return render_template("storage/view.html", snapshot=snapshot)


@storage_bp.route("/snapshots/create", methods=["GET", "POST"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.CREATE)
@limiter.limit("10 per minute")  # type: ignore
def create_snapshot() -> Any:
    """Create new storage snapshot.

    GET: Display creation form
    POST: Create snapshot via RPC service
    """
    # Get list of nodes for selection
    nodes = Node.get_healthy_nodes()

    if request.method == "POST":
        node_id = request.form.get("node_id", type=int)
        source_volume = request.form.get("source_volume", "").strip()
        name = request.form.get("name", "").strip()
        retention_days = request.form.get("retention_days", 30, type=int)
        description = request.form.get("description", "").strip()

        # Validate input
        errors = []
        if not node_id:
            errors.append("Node selection required")
        if not source_volume:
            errors.append("Source volume required")
        if not name:
            errors.append("Snapshot name required")
        if retention_days < 1 or retention_days > 3650:
            errors.append("Retention days must be 1-3650")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("storage.create_snapshot"))

        # Verify node exists
        node = Node.query.get(node_id)
        if not node:
            flash("Selected node not found", "error")
            return redirect(url_for("storage.create_snapshot"))

        try:
            # Create snapshot via RPC service
            rpc_client = get_rpc_client()
            rpc_response = rpc_client.create_snapshot(
                node_id=node.node_id,
                source_volume=source_volume,
                name=name,
                retention_days=retention_days,
            )

            # Save snapshot to database
            expires_at = datetime.now(timezone.utc) + timedelta(days=retention_days)
            snapshot = Snapshot(
                snapshot_id=rpc_response.get("snapshot_id"),
                name=name,
                node_id=node_id,
                source_volume=source_volume,
                description=description,
                size_gb=rpc_response.get("size_gb", 0),
                status=rpc_response.get("status", "pending"),
                retention_days=retention_days,
                expires_at=expires_at,
            )
            db.session.add(snapshot)
            db.session.commit()

            # Log creation
            AuditLog.log_operation(
                user_id=current_user.id,
                operation="create",
                resource_type="snapshot",
                action=f"Created snapshot: {name} on {node.hostname}",
                status="success",
                resource_id=str(snapshot.id),
                request_data={"node": node.hostname, "volume": source_volume},
                rpc_method="CreateSnapshot",
                ip_address=request.remote_addr,
            )

            flash(f"Snapshot {name} created successfully", "success")
            return redirect(url_for("storage.view_snapshot", snapshot_id=snapshot.id))

        except RPCClientError as e:
            flash(f"Failed to create snapshot: {str(e)}", "error")
            AuditLog.log_operation(
                user_id=current_user.id,
                operation="create",
                resource_type="snapshot",
                action=f"Failed to create snapshot: {name}",
                status="failure",
                error_message=str(e),
                rpc_method="CreateSnapshot",
                ip_address=request.remote_addr,
            )

    return render_template("storage/create.html", nodes=nodes)


@storage_bp.route("/snapshots/<int:snapshot_id>/delete", methods=["POST"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.DELETE)
@limiter.limit("10 per minute")  # type: ignore
def delete_snapshot(snapshot_id: int) -> Any:
    """Delete storage snapshot.

    POST: Delete snapshot via RPC service
    """
    snapshot = Snapshot.query.get(snapshot_id)
    if not snapshot:
        flash("Snapshot not found", "error")
        return redirect(url_for("storage.list_snapshots"))

    try:
        # Delete snapshot via RPC service
        rpc_client = get_rpc_client()
        rpc_client.delete_snapshot(snapshot.snapshot_id)

        # Update status to deleting
        snapshot.status = "deleting"
        db.session.commit()

        # Log deletion
        AuditLog.log_operation(
            user_id=current_user.id,
            operation="delete",
            resource_type="snapshot",
            action=f"Deleted snapshot: {snapshot.name}",
            status="success",
            resource_id=str(snapshot_id),
            rpc_method="DeleteSnapshot",
            ip_address=request.remote_addr,
        )

        flash(f"Snapshot {snapshot.name} has been deleted", "success")
        return redirect(url_for("storage.list_snapshots"))

    except RPCClientError as e:
        flash(f"Failed to delete snapshot: {str(e)}", "error")
        AuditLog.log_operation(
            user_id=current_user.id,
            operation="delete",
            resource_type="snapshot",
            action=f"Failed to delete snapshot: {snapshot.name}",
            status="failure",
            error_message=str(e),
            rpc_method="DeleteSnapshot",
            ip_address=request.remote_addr,
        )
        return redirect(url_for("storage.list_snapshots"))


@storage_bp.route("/api/snapshots", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.READ)
@limiter.limit("60 per minute")  # type: ignore
def api_snapshots() -> Any:
    """API endpoint to get snapshot list.

    GET: Return JSON array of snapshots
    """
    node_id = request.args.get("node_id", None, type=int)

    query = Snapshot.query
    if node_id:
        query = query.filter_by(node_id=node_id)

    snapshots = query.order_by(Snapshot.created_at.desc()).limit(100).all()
    return jsonify([s.to_dict(include_node=True) for s in snapshots])


@storage_bp.route("/api/snapshots/<int:snapshot_id>/progress", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.READ)
def api_snapshot_progress(snapshot_id: int) -> Any:
    """API endpoint to get snapshot creation progress.

    GET: Return snapshot progress and status
    """
    snapshot = Snapshot.query.get(snapshot_id)
    if not snapshot:
        return jsonify({"error": "Snapshot not found"}), 404

    return jsonify(
        {
            "snapshot_id": snapshot.snapshot_id,
            "status": snapshot.status,
            "progress_percent": snapshot.progress_percent,
            "size_gb": snapshot.size_gb,
        }
    )


@storage_bp.route("/cleanup/expired", methods=["POST"])
@login_required  # type: ignore
@require_permission(Resource.SNAPSHOT, Action.DELETE)
def cleanup_expired() -> Any:
    """Clean up expired snapshots.

    POST: Delete all snapshots past retention date
    """
    expired = Snapshot.get_expired_snapshots()

    if not expired:
        flash("No expired snapshots to clean up", "info")
        return redirect(url_for("storage.list_snapshots"))

    deleted_count = 0
    for snapshot in expired:
        try:
            rpc_client = get_rpc_client()
            rpc_client.delete_snapshot(snapshot.snapshot_id)
            snapshot.status = "deleting"
            deleted_count += 1
        except RPCClientError as e:
            flash(
                f"Failed to delete expired snapshot {snapshot.name}: {str(e)}",
                "warning",
            )

    db.session.commit()

    # Log cleanup
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="execute",
        resource_type="snapshot",
        action=f"Cleaned up {deleted_count} expired snapshots",
        status="success",
        ip_address=request.remote_addr,
    )

    flash(f"Cleanup initiated for {deleted_count} expired snapshots", "success")
    return redirect(url_for("storage.list_snapshots"))
