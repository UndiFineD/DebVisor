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


"""Node Management Routes - Infrastructure Node Operations

Provides endpoints for node registration, monitoring, and management.
Integrates with RPC service for backend operations.
"""

from typing import Any
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from opt.web.panel.core.rpc_client import get_rpc_client, RPCClientError
from opt.web.panel.models.node import Node
from opt.web.panel.models.audit_log import AuditLog
from opt.web.panel.extensions import db, limiter
from opt.web.panel.rbac import require_permission, Resource, Action

# Create blueprint
_nodes_bp=Blueprint("nodes", __name__, url_prefix="/nodes")


@nodes_bp.route("/", methods=["GET"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("100 per minute")    # type: ignore
def list_nodes() -> Any:
    """List all cluster nodes.

    GET: Display paginated node list
    """
    _page=request.args.get("page", 1, type=int)
    per_page=20
    _status_filter=request.args.get("status", None)

    query=Node.query
    if status_filter:
        _query=query.filter_by(status=status_filter)

    _pagination=query.order_by(Node.updated_at.desc()).paginate(
        _page=page, per_page=per_page
    )
    _nodes=pagination.items

    # Log view
    AuditLog.log_operation(
        _user_id=current_user.id,
        _operation="read",
        _resource_type="node",
        _action="Viewed node list",
        _status="success",
        _ip_address=request.remote_addr,
    )

    return render_template(
        "nodes/list.html",
        _nodes=nodes,
        _pagination=pagination,
        _status_filter=status_filter,
    )


@nodes_bp.route("/<int:node_id>", methods=["GET"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("100 per minute")    # type: ignore
def view_node(nodeid: int) -> Any:
    """View node details.

    GET: Display node information and status
    """
    _node=Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    # Get snapshots for this node
    _snapshots=node.snapshots

    # Log view
    AuditLog.log_operation(
        _user_id=current_user.id,
        _operation="read",
        _resource_type="node",
        _action=f"Viewed node details: {node.hostname}",
        _status="success",
        _resource_id=str(node_id),
        _ip_address=request.remote_addr,
    )

    return render_template("nodes/view.html", node=node, snapshots=snapshots)


@nodes_bp.route("/register", methods=["GET", "POST"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.CREATE)
@limiter.limit("20 per minute")    # type: ignore
def register_node() -> Any:
    """Register new cluster node.

    GET: Display registration form
    POST: Register node with RPC service
    """
    if request.method == "POST":
        _hostname=request.form.get("hostname", "").strip().lower()
        _ip_address=request.form.get("ip_address", "").strip()
        _cpu_cores=request.form.get("cpu_cores", type=int, default=0)
        _memory_gb=request.form.get("memory_gb", type=int, default=0)
        _storage_gb=request.form.get("storage_gb", type=int, default=0)
        _region=request.form.get("region", "").strip()
        _rack=request.form.get("rack", "").strip()

        # Validate input
        errors=[]
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
            _rpc_client=get_rpc_client()
            _rpc_response=rpc_client.register_node(
                _hostname=hostname,
                _ip_address=ip_address,
                _cpu_cores=cpu_cores,
                _memory_gb=memory_gb,
                _storage_gb=storage_gb,
                _region=region,
                _rack=rack,
            )

            # Save node to database
            node=Node(
                _node_id=rpc_response.get("node_id"),
                _hostname=hostname,
                _ip_address=ip_address,
                _cpu_cores=cpu_cores,
                _memory_gb=memory_gb,
                _storage_gb=storage_gb,
                _region=region,
                _rack=rack,
                _status="online",
            )
            db.session.add(node)
            db.session.commit()

            # Log registration
            AuditLog.log_operation(
                _user_id=current_user.id,
                _operation="create",
                _resource_type="node",
                _action=f"Registered node: {hostname}",
                _status="success",
                _resource_id=str(node.id),
                _rpc_method="RegisterNode",
                _ip_address=request.remote_addr,
            )

            flash(f"Node {hostname} registered successfully", "success")
            return redirect(url_for("nodes.view_node", node_id=node.id))

        except RPCClientError as e:
                current_app.logger.error(f"Failed to send heartbeat to node {node.hostname}: {e}", exc_info=True)
            current_app.logger.error(f"Failed to register node with RPC service: {e}", exc_info=True)
            flash("Failed to register node with RPC service", "error")
            AuditLog.log_operation(
                _user_id=current_user.id,
                _operation="create",
                _resource_type="node",
                _action=f"Failed to register node: {hostname}",
                _status="failure",
                _error_message="RPC registration failed",
                _rpc_method="RegisterNode",
                _ip_address=request.remote_addr,
            )

    return render_template("nodes/register.html")


@nodes_bp.route("/<int:node_id>/heartbeat", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.UPDATE)
@limiter.limit("60 per minute")    # type: ignore
def send_heartbeat(nodeid: int) -> Any:
    """Send node heartbeat to keep it online.

    POST: Update node status
    """
    _node=Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    try:
    # Send heartbeat to RPC service
        _rpc_client=get_rpc_client()
        rpc_client.heartbeat(node.node_id, {})

        # Update node status
        node.update_heartbeat()

        # Log heartbeat
        AuditLog.log_operation(
            _user_id=current_user.id,
            _operation="execute",
            _resource_type="node",
            _action=f"Sent heartbeat to node: {node.hostname}",
            _status="success",
            _resource_id=str(node_id),
            _rpc_method="Heartbeat",
            _ip_address=request.remote_addr,
        )

        return jsonify({"success": True, "status": node.status})

    except RPCClientError as e:
        flash("Failed to send heartbeat", "error")
        AuditLog.log_operation(
            _user_id=current_user.id,
            _operation="execute",
            _resource_type="node",
            _action=f"Failed to send heartbeat to node: {node.hostname}",
            _status="failure",
            _error_message="Heartbeat RPC failed",
            _rpc_method="Heartbeat",
            _ip_address=request.remote_addr,
        )
        # Return generic error message to prevent information exposure
        return jsonify({"error": "Failed to send heartbeat. Please check logs for details."}), 500


@nodes_bp.route("/<int:node_id>/disable", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.UPDATE)
@limiter.limit("20 per minute")    # type: ignore
def disable_node(nodeid: int) -> Any:
    """Disable node in cluster.

    POST: Mark node as offline
    """
    _node=Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    node.status="offline"
    db.session.commit()

    # Log disable
    AuditLog.log_operation(
        _user_id=current_user.id,
        _operation="update",
        _resource_type="node",
        _action=f"Disabled node: {node.hostname}",
        _status="success",
        _resource_id=str(node_id),
        _ip_address=request.remote_addr,
    )

    flash(f"Node {node.hostname} has been disabled", "success")
    return redirect(url_for("nodes.view_node", node_id=node_id))


@nodes_bp.route("/<int:node_id>/delete", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.DELETE)
@limiter.limit("10 per minute")    # type: ignore
def delete_node(nodeid: int) -> Any:
    """Delete node from cluster.

    POST: Remove node and associated data
    """
    _node=Node.query.get(node_id)
    if not node:
        flash("Node not found", "error")
        return redirect(url_for("nodes.list_nodes"))

    hostname=node.hostname
    db.session.delete(node)
    db.session.commit()

    # Log deletion
    AuditLog.log_operation(
        _user_id=current_user.id,
        _operation="delete",
        _resource_type="node",
        _action=f"Deleted node: {hostname}",
        _status="success",
        _resource_id=str(node_id),
        _ip_address=request.remote_addr,
    )

    flash(f"Node {hostname} has been deleted", "success")
    return redirect(url_for("nodes.list_nodes"))


@nodes_bp.route("/api/status", methods=["GET"])
@login_required    # type: ignore
@require_permission(Resource.NODE, Action.READ)
@limiter.limit("60 per minute")    # type: ignore
def api_nodes_status() -> Any:
    """API endpoint to get all nodes status.

    GET: Return JSON array of node statuses
    """
    _nodes=Node.query.all()
    return jsonify([node.to_dict() for node in nodes])
