"""Node Management Routes - Infrastructure Node Operations

Provides endpoints for node registration, monitoring, and management.
Integrates with RPC service for backend operations.
"""

from typing import Any
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
# from flask_login import login_required, current_user
from opt.web.panel.core.rpc_client import get_rpc_client, RPCClientError
from opt.web.panel.models.node import Node
from opt.web.panel.models.audit_log import AuditLog
from opt.web.panel.extensions import db, limiter
from opt.web.panel.rbac import require_permission, Resource, Action

# Create blueprint
nodes_bp = Blueprint("nodes", __name__, url_prefix="/nodes")


@nodes_bp.route("/", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("100 per minute")  # type: ignore
def list_nodes() -> Any:
    """List all cluster nodes.

    GET: Display paginated node list
    """
    page = request.args.get("page", 1, type=int)
    per_page = 20
    status_filter = request.args.get("status", None)

    query = Node.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(Node.updated_at.desc()).paginate(
        page=page, per_page=per_page
    )
    nodes = pagination.items

    # Log view
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="read",
        resource_type="node",
        action="Viewed node list",
        status="success",
        ip_address=request.remote_addr,
    )

    return render_template(
        "nodes/list.html",
        nodes=nodes,
        pagination=pagination,
        status_filter=status_filter,
    )


@nodes_bp.route("/<int:node_id>", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("100 per minute")  # type: ignore
def view_node(node_id: int) -> Any:
    """View node details.

    GET: Display node information and status
    """
    node = Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    # Get snapshots for this node
    snapshots = node.snapshots

    # Log view
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="read",
        resource_type="node",
        action=f"Viewed node details: {node.hostname}",
        status="success",
        resource_id=str(node_id),
        ip_address=request.remote_addr,
    )

    return render_template("nodes/view.html", node=node, snapshots=snapshots)


@nodes_bp.route("/register", methods=["GET", "POST"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.CREATE)
@limiter.limit("20 per minute")  # type: ignore
def register_node() -> Any:
    """Register new cluster node.

    GET: Display registration form
    POST: Register node with RPC service
    """
    if request.method == "POST":
        hostname = request.form.get("hostname", "").strip().lower()
        ip_address = request.form.get("ip_address", "").strip()
        cpu_cores = request.form.get("cpu_cores", type=int, default=0)
        memory_gb = request.form.get("memory_gb", type=int, default=0)
        storage_gb = request.form.get("storage_gb", type=int, default=0)
        region = request.form.get("region", "").strip()
        rack = request.form.get("rack", "").strip()

        # Validate input
        errors = []
        if not hostname:
            errors.append("Hostname required")
        if not ip_address:
            errors.append("IP address required")
        if not cpu_cores or cpu_cores < 1:
            errors.append("CPU cores must be at least 1")
        if not memory_gb or memory_gb < 1:
            errors.append("Memory must be at least 1 GB")
        if not storage_gb or storage_gb < 1:
            errors.append("Storage must be at least 1 GB")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("nodes.register_node"))

        # Check if node already exists
        if Node.get_by_hostname(hostname):
            flash("Node with this hostname already exists", "error")
            return redirect(url_for("nodes.register_node"))

        try:
            # Register with RPC service
            rpc_client = get_rpc_client()
            rpc_response = rpc_client.register_node(
                hostname=hostname,
                ip_address=ip_address,
                cpu_cores=cpu_cores,
                memory_gb=memory_gb,
                storage_gb=storage_gb,
                region=region,
                rack=rack,
            )

            # Save node to database
            node = Node(
                node_id=rpc_response.get("node_id"),
                hostname=hostname,
                ip_address=ip_address,
                cpu_cores=cpu_cores,
                memory_gb=memory_gb,
                storage_gb=storage_gb,
                region=region,
                rack=rack,
                status="online",
            )
            db.session.add(node)
            db.session.commit()

            # Log registration
            AuditLog.log_operation(
                user_id=current_user.id,
                operation="create",
                resource_type="node",
                action=f"Registered node: {hostname}",
                status="success",
                resource_id=str(node.id),
                rpc_method="RegisterNode",
                ip_address=request.remote_addr,
            )

            flash(f"Node {hostname} registered successfully", "success")
            return redirect(url_for("nodes.view_node", node_id=node.id))

        except RPCClientError as e:
            flash(f"Failed to register node with RPC service: {str(e)}", "error")
            AuditLog.log_operation(
                user_id=current_user.id,
                operation="create",
                resource_type="node",
                action=f"Failed to register node: {hostname}",
                status="failure",
                error_message=str(e),
                rpc_method="RegisterNode",
                ip_address=request.remote_addr,
            )

    return render_template("nodes/register.html")


@nodes_bp.route("/<int:node_id>/heartbeat", methods=["POST"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.UPDATE)
@limiter.limit("60 per minute")  # type: ignore
def send_heartbeat(node_id: int) -> Any:
    """Send node heartbeat to keep it online.

    POST: Update node status
    """
    node = Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    try:
        # Send heartbeat to RPC service
        rpc_client = get_rpc_client()
        rpc_client.heartbeat(node.node_id, {})

        # Update node status
        node.update_heartbeat()

        # Log heartbeat
        AuditLog.log_operation(
            user_id=current_user.id,
            operation="execute",
            resource_type="node",
            action=f"Sent heartbeat to node: {node.hostname}",
            status="success",
            resource_id=str(node_id),
            rpc_method="Heartbeat",
            ip_address=request.remote_addr,
        )

        return jsonify({"success": True, "status": node.status})

    except RPCClientError as e:
        flash("Failed to send heartbeat", "error")
        AuditLog.log_operation(
            user_id=current_user.id,
            operation="execute",
            resource_type="node",
            action=f"Failed to send heartbeat to node: {node.hostname}",
            status="failure",
            error_message=str(e),
            rpc_method="Heartbeat",
            ip_address=request.remote_addr,
        )
        # Return generic error message to prevent information exposure
        return jsonify({"error": "Failed to send heartbeat. Please check logs for details."}), 500


@nodes_bp.route("/<int:node_id>/disable", methods=["POST"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.UPDATE)
@limiter.limit("20 per minute")  # type: ignore
def disable_node(node_id: int) -> Any:
    """Disable node in cluster.

    POST: Mark node as offline
    """
    node = Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    node.status = "offline"
    db.session.commit()

    # Log disable
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="update",
        resource_type="node",
        action=f"Disabled node: {node.hostname}",
        status="success",
        resource_id=str(node_id),
        ip_address=request.remote_addr,
    )

    flash(f"Node {node.hostname} has been disabled", "success")
    return redirect(url_for("nodes.view_node", node_id=node_id))


@nodes_bp.route("/<int:node_id>/delete", methods=["POST"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.DELETE)
@limiter.limit("10 per minute")  # type: ignore
def delete_node(node_id: int) -> Any:
    """Delete node from cluster.

    POST: Remove node and associated data
    """
    node = Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    hostname = node.hostname
    db.session.delete(node)
    db.session.commit()

    # Log deletion
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="delete",
        resource_type="node",
        action=f"Deleted node: {hostname}",
        status="success",
        resource_id=str(node_id),
        ip_address=request.remote_addr,
    )

    flash(f"Node {hostname} has been deleted", "success")
    return redirect(url_for("nodes.list_nodes"))


@nodes_bp.route("/api/status", methods=["GET"])
@login_required  # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("60 per minute")  # type: ignore
def api_nodes_status() -> Any:
    """API endpoint to get all nodes status.

    GET: Return JSON array of node statuses
    """
    nodes = Node.query.all()
    return jsonify([node.to_dict() for node in nodes])
