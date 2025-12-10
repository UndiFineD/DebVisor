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

"""
Role-Based Access Control (RBAC) for DebVisor Web Panel.

Implements fine-grained permission system for operations.

Features:
    - Role-based access control (Admin, Operator, Developer, Viewer)
    - Resource-based permissions (Node, Snapshot, User, AuditLog, System)
    - Action-based permissions (Create, Read, Update, Delete, Execute)
    - Attribute-based access control (ABAC) for fine-grained policies
    - Flask integration via decorators
"""

from enum import Enum
from typing import TypeVar
from typing import Any
from typing import Dict, List, Set, Callable, Tuple, TYPE_CHECKING
from functools import wraps
import logging
from flask import abort

if TYPE_CHECKING:
    from flask import Flask

logger = logging.getLogger(__name__)

# Type variable for decorated functions
F = TypeVar("F", bound=Callable[..., Any])


class Role(Enum):
    """User roles in DebVisor."""

    ADMIN = "admin"    # Full system access
    OPERATOR = "operator"    # Operational tasks
    DEVELOPER = "developer"    # Development/testing
    VIEWER = "viewer"    # Read-only access


class Resource(Enum):
    """System resources."""

    NODE = "node"
    SNAPSHOT = "snapshot"
    USER = "user"
    AUDIT_LOG = "audit_log"
    SYSTEM = "system"


class Action(Enum):
    """Actions on resources."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


# Define role permissions
ROLE_PERMISSIONS: Dict[Role, Set[Tuple[Resource, Action]]] = {
    Role.ADMIN: {
        # Admin has all permissions
        (Resource.NODE, Action.CREATE),
        (Resource.NODE, Action.READ),
        (Resource.NODE, Action.UPDATE),
        (Resource.NODE, Action.DELETE),
        (Resource.NODE, Action.EXECUTE),
        (Resource.SNAPSHOT, Action.CREATE),
        (Resource.SNAPSHOT, Action.READ),
        (Resource.SNAPSHOT, Action.UPDATE),
        (Resource.SNAPSHOT, Action.DELETE),
        (Resource.USER, Action.CREATE),
        (Resource.USER, Action.READ),
        (Resource.USER, Action.UPDATE),
        (Resource.USER, Action.DELETE),
        (Resource.AUDIT_LOG, Action.READ),
        (Resource.SYSTEM, Action.EXECUTE),
        (Resource.SYSTEM, Action.READ),
    },
    Role.OPERATOR: {
        # Operators can manage nodes and snapshots
        (Resource.NODE, Action.READ),
        (Resource.NODE, Action.UPDATE),
        (Resource.NODE, Action.EXECUTE),
        (Resource.SNAPSHOT, Action.CREATE),
        (Resource.SNAPSHOT, Action.READ),
        (Resource.SNAPSHOT, Action.DELETE),
        (Resource.AUDIT_LOG, Action.READ),
    },
    Role.DEVELOPER: {
        # Developers can create and manage snapshots for testing
        (Resource.NODE, Action.READ),
        (Resource.SNAPSHOT, Action.CREATE),
        (Resource.SNAPSHOT, Action.READ),
        (Resource.SNAPSHOT, Action.DELETE),
    },
    Role.VIEWER: {
        # Viewers can only read
        (Resource.NODE, Action.READ),
        (Resource.SNAPSHOT, Action.READ),
        (Resource.AUDIT_LOG, Action.READ),
    },
}


class PermissionChecker:
    """
    Check permissions for user actions.

    Provides methods to verify if a user with a given role
    can perform specific actions on resources.

    Attributes:
        role: The user's role
        permissions: Set of (Resource, Action) tuples allowed for this role
    """

    def __init__(self, role: Role) -> None:
        """
        Initialize permission checker for a role.

        Args:
            role: The user's role
        """
        self.role = role
        self.permissions = ROLE_PERMISSIONS.get(role, set())

    def can(self, resource: Resource, action: Action) -> bool:
        """
        Check if user can perform action on resource.

        Args:
            resource: The resource to check
            action: The action to check

        Returns:
            True if permitted, False otherwise
        """
        return (resource, action) in self.permissions

    def get_allowed_actions(self, resource: Resource) -> List[Action]:
        """
        Get all allowed actions for a resource.

        Args:
            resource: The resource to check

        Returns:
            List of permitted actions
        """
        return [action for res, action in self.permissions if res == resource]


def require_permission(resource: Resource, action: Action) -> Callable[[F], F]:
    """
    Decorator to enforce permission checks on Flask routes.

    Checks if the current user has the required permission.
    Aborts with 401 if not authenticated, 403 if not authorized.

    Args:
        resource: Resource to check permission for
        action: Action to check permission for

    Returns:
        Decorator function

    Example:
        @app.route('/nodes')
        @require_permission(Resource.NODE, Action.READ)
        def list_nodes():
            return jsonify(nodes)
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get current user from Flask-Login
            from flask_login import current_user

            if not current_user.is_authenticated:
                abort(401)

            # Check permission
            checker = PermissionChecker(Role(current_user.role))
            if not checker.can(resource, action):
                logger.warning(
                    f"Permission denied: user {current_user.email} "
                    f"attempted {action.value} on {resource.value}"
                )
                abort(403)

            return func(*args, **kwargs)

        return wrapper    # type: ignore

    return decorator


def require_any_permission(*permissions: Tuple[Resource, Action]) -> Callable[[F], F]:
    """
    Decorator to require any of multiple permissions.

    User must have at least one of the specified permissions.
    Aborts with 401 if not authenticated, 403 if not authorized.

    Args:
        *permissions: Tuples of (Resource, Action)

    Returns:
        Decorator function

    Example:
        @app.route('/audit-log')
        @require_any_permission(
            (Resource.AUDIT_LOG, Action.READ),
            (Resource.SYSTEM, Action.READ)
        )
        def get_audit_log():
            return jsonify(events)
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from flask_login import current_user

            if not current_user.is_authenticated:
                abort(401)

            checker = PermissionChecker(Role(current_user.role))

            has_permission = any(
                checker.can(resource, action) for resource, action in permissions
            )

            if not has_permission:
                abort(403)

            return func(*args, **kwargs)

        return wrapper    # type: ignore

    return decorator


def require_role(*allowed_roles: Role) -> Callable[[F], F]:
    """
    Decorator to require specific roles.

    User must have one of the specified roles.
    Aborts with 401 if not authenticated, 403 if not authorized.

    Args:
        *allowed_roles: Roles that are permitted

    Returns:
        Decorator function

    Example:
        @app.route('/users', methods=['POST'])
        @require_role(Role.ADMIN)
        def create_user():
            return jsonify(user)
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from flask_login import current_user

            if not current_user.is_authenticated:
                abort(401)

            user_role = Role(current_user.role)
            if user_role not in allowed_roles:
                logger.warning(
                    f"Role check failed: user {current_user.email} "
                    f"has role {user_role.value}, requires {[r.value for r in allowed_roles]}"
                )
                abort(403)

            return func(*args, **kwargs)

        return wrapper    # type: ignore

    return decorator


class AttributeBasedAccessControl:
    """
    Attribute-based access control for fine-grained permissions.

    Allows defining policies with custom condition functions
    that evaluate context at runtime.

    Attributes:
        policies: List of policy dictionaries
    """

    def __init__(self) -> None:
        """Initialize ABAC with empty policy list."""
        self.policies: List[Dict[str, Any]] = []

    def add_policy(
        self, resource: Resource, action: Action, condition: Callable[[Dict[str, Any]], bool]
    ) -> None:
        """
        Add a policy with a condition function.

        Args:
            resource: Resource the policy applies to
            action: Action the policy applies to
            condition: Function that evaluates context and returns bool
        """
        self.policies.append(
            {"resource": resource, "action": action, "condition": condition}
        )

    def evaluate(self, resource: Resource, action: Action, context: Dict[str, Any]) -> bool:
        """
        Evaluate if action is allowed given context.

        Args:
            resource: Resource being accessed
            action: Action being performed
            context: Dictionary of contextual information

        Returns:
            True if any matching policy condition passes
        """
        matching_policies = [
            p
            for p in self.policies
            if p["resource"] == resource and p["action"] == action
        ]

        return any(p["condition"](context) for p in matching_policies)


def require_attribute_permission(
    resource: Resource, action: Action, context_key: str = "obj"
) -> Callable[[F], F]:
    """
    Decorator requiring attribute-based permission check.

    Combines RBAC check with optional ABAC policy evaluation.
    Aborts with 400 if context object missing, 401 if not authenticated,
    403 if not authorized.

    Args:
        resource: Resource being accessed
        action: Action being performed
        context_key: Keyword argument name containing the object (default: 'obj')

    Returns:
        Decorator function

    Example:
        @app.route('/nodes/<node_id>')
        @require_attribute_permission(Resource.NODE, Action.UPDATE, 'node')
        def update_node(node_id, node=None):
            return jsonify(node)
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from flask_login import current_user

            if not current_user.is_authenticated:
                abort(401)

            # Get the object being accessed from kwargs
            obj = kwargs.get(context_key)
            if not obj:
                abort(400)

            # Check RBAC first
            role_checker = PermissionChecker(Role(current_user.role))
            if not role_checker.can(resource, action):
                abort(403)

            # Could add ABAC checks here if needed

            return func(*args, **kwargs)

        return wrapper    # type: ignore

    return decorator


# Example usage for routes


def setup_rbac_routes(app: "Flask") -> None:
    """
    Setup example routes with RBAC.

    Demonstrates how to use RBAC decorators with Flask routes.

    Args:
        app: Flask application instance
    """
    from flask import jsonify

    @app.route("/nodes")
    @require_permission(Resource.NODE, Action.READ)
    def list_nodes() -> Any:
        """List nodes - requires node:read permission."""
        return jsonify({"nodes": []})

    @app.route("/nodes/<node_id>", methods=["PUT"])
    @require_permission(Resource.NODE, Action.UPDATE)
    def update_node(node_id: str) -> Any:
        """Update node - requires node:update permission."""
        return jsonify({"success": True})

    @app.route("/snapshots", methods=["POST"])
    @require_permission(Resource.SNAPSHOT, Action.CREATE)
    def create_snapshot() -> Any:
        """Create snapshot - requires snapshot:create permission."""
        return jsonify({"snapshot_id": "123"}), 201

    @app.route("/snapshots/<snapshot_id>", methods=["DELETE"])
    @require_permission(Resource.SNAPSHOT, Action.DELETE)
    def delete_snapshot(snapshot_id: str) -> Any:
        """Delete snapshot - requires snapshot:delete permission."""
        return jsonify({"success": True})

    @app.route("/users", methods=["POST"])
    @require_role(Role.ADMIN)
    def create_user() -> Any:
        """Create user - admin only."""
        return jsonify({"user_id": "456"}), 201

    @app.route("/audit-log")
    @require_any_permission((Resource.AUDIT_LOG, Action.READ))
    def get_audit_log() -> Any:
        """Get audit log - read-only, available to most roles."""
        return jsonify({"events": []})


# Permission summary for documentation
PERMISSION_MATRIX = {
    "Admin": {
        "Nodes": ["Create", "Read", "Update", "Delete", "Execute"],
        "Snapshots": ["Create", "Read", "Update", "Delete"],
        "Users": ["Create", "Read", "Update", "Delete"],
        "Audit Log": ["Read"],
        "System": ["Execute"],
    },
    "Operator": {
        "Nodes": ["Read", "Update", "Execute"],
        "Snapshots": ["Create", "Read", "Delete"],
        "Audit Log": ["Read"],
    },
    "Developer": {"Nodes": ["Read"], "Snapshots": ["Create", "Read", "Delete"]},
    "Viewer": {"Nodes": ["Read"], "Snapshots": ["Read"], "Audit Log": ["Read"]},
}
