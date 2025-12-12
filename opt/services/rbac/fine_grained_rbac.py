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

"""Fine-Grained RBAC System for DebVisor

Implements RBAC-001: Resource-level permissions with conditional access control.

Features:
- Resource-level permissions (beyond CRUD)
- Conditional permissions (time-based, IP-based, attribute-based)
- Permission inheritance and role hierarchies
- Dynamic permission evaluation
- Audit logging for authorization decisions
- Integration with existing authentication system
"""

from datetime import datetime, timezone, time as dt_time
# import logging
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set
from enum import Enum
from ipaddress import ip_address, ip_network

logger = logging.getLogger(__name__)  # type: ignore[name-defined]


class Action(Enum):
    """Supported actions for resources."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"
    LIST = "list"
    EXPORT = "export"
    IMPORT = "import"
    MIGRATE = "migrate"
    BACKUP = "backup"
    RESTORE = "restore"
    SNAPSHOT = "snapshot"


class ResourceType(Enum):
    """Resource types in the system."""

    VM = "vm"
    HOST = "host"
    STORAGE = "storage"
    NETWORK = "network"
    USER = "user"
    ROLE = "role"
    POLICY = "policy"
    BACKUP = "backup"
    SNAPSHOT = "snapshot"
    CLUSTER = "cluster"
    REGION = "region"
    SECRET = "secret"    # nosec B105
    CERTIFICATE = "certificate"


class ConditionType(Enum):
    """Types of conditional permissions."""

    TIME_RANGE = "time_range"
    IP_ADDRESS = "ip_address"
    IP_NETWORK = "ip_network"
    ATTRIBUTE = "attribute"
    TAG = "tag"
    CUSTOM = "custom"


@dataclass
class Condition:
    """Permission condition that must be satisfied."""

    type: ConditionType
    parameters: Dict[str, Any]
    negate: bool = False    # If True, condition must NOT be satisfied

    def evaluate(self, context: "AuthorizationContext") -> bool:
        """
        Evaluate if condition is satisfied.

        Args:
            context: Authorization context with request info

        Returns:
            True if condition is satisfied
        """
        result = False

        if self.type == ConditionType.TIME_RANGE:
            result = self._evaluate_time_range(context)
        elif self.type == ConditionType.IP_ADDRESS:
            result = self._evaluate_ip_address(context)
        elif self.type == ConditionType.IP_NETWORK:
            result = self._evaluate_ip_network(context)
        elif self.type == ConditionType.ATTRIBUTE:
            result = self._evaluate_attribute(context)
        elif self.type == ConditionType.TAG:
            result = self._evaluate_tag(context)
        elif self.type == ConditionType.CUSTOM:
            result = self._evaluate_custom(context)

        return not result if self.negate else result

    def _evaluate_time_range(self, context: "AuthorizationContext") -> bool:
        """Check if current time is within allowed range."""
        start_time = dt_time.fromisoformat(self.parameters["start_time"])
        end_time = dt_time.fromisoformat(self.parameters["end_time"])
        current_time = datetime.now(timezone.utc).time()

        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            # Handles ranges that cross midnight
            return current_time >= start_time or current_time <= end_time

    def _evaluate_ip_address(self, context: "AuthorizationContext") -> bool:
        """Check if request IP matches allowed IPs."""
        allowed_ips = self.parameters["allowed_ips"]
        client_ip = context.client_ip

        if not client_ip:
            return False

        try:
            client = ip_address(client_ip)
            return any(client == ip_address(allowed_ip) for allowed_ip in allowed_ips)
        except ValueError:
            return False

    def _evaluate_ip_network(self, context: "AuthorizationContext") -> bool:
        """Check if request IP is in allowed networks."""
        allowed_networks = self.parameters["allowed_networks"]
        client_ip = context.client_ip

        if not client_ip:
            return False

        try:
            client = ip_address(client_ip)
            return any(client in ip_network(network) for network in allowed_networks)
        except ValueError:
            return False

    def _evaluate_attribute(self, context: "AuthorizationContext") -> bool:
        """Check if resource/principal attributes match requirements."""
        required_attrs = self.parameters["attributes"]

        # Check principal attributes
        principal_attrs = context.principal_attributes
        resource_attrs = context.resource_attributes

        for key, value in required_attrs.items():
            # Check both principal and resource attributes
            if principal_attrs.get(key) != value and resource_attrs.get(key) != value:
                return False

        return True

    def _evaluate_tag(self, context: "AuthorizationContext") -> bool:
        """Check if resource has required tags."""
        required_tags = self.parameters["tags"]
        resource_tags = context.resource_attributes.get("tags", {})

        for key, value in required_tags.items():
            if resource_tags.get(key) != value:
                return False

        return True

    def _evaluate_custom(self, context: "AuthorizationContext") -> bool:
        """Evaluate custom condition using callable."""
        evaluator = self.parameters.get("evaluator")
        if callable(evaluator):
            return evaluator(context)
        return False


@dataclass
class Permission:
    """
    Fine-grained permission with resource-level and conditional access control.

    Implements RBAC-001: Resource-level permissions.
    """

    resource_type: ResourceType
    resource_id: Optional[str]    # None = all resources of type
    actions: List[Action]
    conditions: List[Condition] = field(default_factory=list)
    description: str = ""

    def matches_resource(self, resource_type: ResourceType, resource_id: str) -> bool:
        """Check if permission applies to given resource."""
        if self.resource_type != resource_type:
            return False

        # Wildcard permission applies to all resources of type
        if self.resource_id is None or self.resource_id == "*":
            return True

        # Pattern matching for resource IDs (supports wildcards)
        pattern = self.resource_id.replace("*", ".*")
        return bool(re.match(f"^{pattern}$", resource_id))

    def allows_action(self, action: Action) -> bool:
        """Check if permission allows given action."""
        # MANAGE action allows all other actions
        if Action.MANAGE in self.actions:
            return True

        return action in self.actions

    def evaluate_conditions(self, context: "AuthorizationContext") -> bool:
        """Evaluate all conditions for this permission."""
        if not self.conditions:
            return True    # No conditions = always allowed

        return all(condition.evaluate(context) for condition in self.conditions)


@dataclass
class Role:
    """
    Role with permissions and optional parent roles for inheritance.

    Implements RBAC-001: Permission inheritance.
    """

    name: str
    description: str
    permissions: List[Permission]
    parent_roles: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_all_permissions(self, role_manager: "RoleManager") -> List[Permission]:
        """
        Get all permissions including inherited from parent roles.

        Args:
            role_manager: Role manager to resolve parent roles

        Returns:
            List of all permissions (own + inherited)
        """
        all_permissions = list(self.permissions)

        # Recursively gather permissions from parent roles
        for parent_name in self.parent_roles:
            parent = role_manager.get_role(parent_name)
            if parent:
                all_permissions.extend(parent.get_all_permissions(role_manager))

        return all_permissions


@dataclass
class AuthorizationContext:
    """Context for authorization decision."""

    principal_id: str
    principal_attributes: Dict[str, Any]
    resource_type: ResourceType
    resource_id: str
    resource_attributes: Dict[str, Any]
    action: Action
    client_ip: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    additional_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthorizationDecision:
    """Result of authorization decision."""

    allowed: bool
    principal_id: str
    resource_type: ResourceType
    resource_id: str
    action: Action
    matched_permissions: List[Permission]
    failed_conditions: List[Condition]
    reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RoleManager:
    """
    Manages roles and permissions.

    Implements RBAC-001: Fine-grained permission system.
    """

    def __init__(self) -> None:
        self.roles: Dict[str, Role] = {}
        self.principal_roles: Dict[str, Set[str]] = {}    # principal_id -> role names

        # Initialize built-in roles
        self._initialize_builtin_roles()

        logger.info("RoleManager initialized")

    def _initialize_builtin_roles(self) -> None:
        """Create built-in system roles."""
        # Super Admin: Full access
        self.create_role(
            Role(
                name="superadmin",
                description="Full system access",
                permissions=[
                    Permission(
                        resource_type=rt,
                        resource_id=None,
                        actions=list(Action),
                        description=f"Full access to all {rt.value} resources",
                    )
                    for rt in ResourceType
                ],
            )
        )

        # Admin: Manage most resources except users/roles
        admin_permissions = []
        for rt in ResourceType:
            if rt not in [ResourceType.USER, ResourceType.ROLE, ResourceType.POLICY]:
                admin_permissions.append(
                    Permission(
                        resource_type=rt,
                        resource_id=None,
                        actions=[
                            Action.CREATE,
                            Action.READ,
                            Action.UPDATE,
                            Action.DELETE,
                            Action.LIST,
                        ],
                    )
                )

        self.create_role(
            Role(
                name="admin",
                description="Administrative access",
                permissions=admin_permissions,
            )
        )

        # Operator: Manage VMs and resources, read-only for configuration
        self.create_role(
            Role(
                name="operator",
                description="Operations access",
                permissions=[
                    Permission(
                        ResourceType.VM,
                        None,
                        [
                            Action.CREATE,
                            Action.READ,
                            Action.UPDATE,
                            Action.DELETE,
                            Action.EXECUTE,
                            Action.MIGRATE,
                        ],
                    ),
                    Permission(
                        ResourceType.SNAPSHOT,
                        None,
                        [Action.CREATE, Action.READ, Action.DELETE],
                    ),
                    Permission(
                        ResourceType.BACKUP,
                        None,
                        [Action.CREATE, Action.READ, Action.RESTORE],
                    ),
                    Permission(ResourceType.HOST, None, [Action.READ, Action.LIST]),
                    Permission(ResourceType.NETWORK, None, [Action.READ, Action.LIST]),
                    Permission(ResourceType.STORAGE, None, [Action.READ, Action.LIST]),
                ],
            )
        )

        # Viewer: Read-only access
        self.create_role(
            Role(
                name="viewer",
                description="Read-only access",
                permissions=[
                    Permission(
                        resource_type=rt,
                        resource_id=None,
                        actions=[Action.READ, Action.LIST],
                    )
                    for rt in ResourceType
                ],
            )
        )

        logger.info("Built-in roles initialized")

    def create_role(self, role: Role) -> None:
        """Create a new role."""
        if role.name in self.roles:
            raise ValueError(f"Role already exists: {role.name}")

        self.roles[role.name] = role
        logger.info(f"Created role: {role.name}")

    def get_role(self, name: str) -> Optional[Role]:
        """Get role by name."""
        return self.roles.get(name)

    def delete_role(self, name: str) -> None:
        """Delete a role."""
        if name in ["superadmin", "admin", "operator", "viewer"]:
            raise ValueError(f"Cannot delete built-in role: {name}")

        if name in self.roles:
            del self.roles[name]
            logger.info(f"Deleted role: {name}")

    def assign_role(self, principal_id: str, role_name: str) -> None:
        """Assign role to principal."""
        if role_name not in self.roles:
            raise ValueError(f"Role not found: {role_name}")

        if principal_id not in self.principal_roles:
            self.principal_roles[principal_id] = set()

        self.principal_roles[principal_id].add(role_name)
        logger.info(f"Assigned role {role_name} to principal {principal_id}")

    def revoke_role(self, principal_id: str, role_name: str) -> None:
        """Revoke role from principal."""
        if principal_id in self.principal_roles:
            self.principal_roles[principal_id].discard(role_name)
            logger.info(f"Revoked role {role_name} from principal {principal_id}")

    def get_principal_roles(self, principal_id: str) -> List[Role]:
        """Get all roles assigned to principal."""
        role_names = self.principal_roles.get(principal_id, set())
        return [self.roles[name] for name in role_names if name in self.roles]

    def get_principal_permissions(self, principal_id: str) -> List[Permission]:
        """Get all permissions for principal (including inherited)."""
        roles = self.get_principal_roles(principal_id)

        all_permissions = []
        for role in roles:
            all_permissions.extend(role.get_all_permissions(self))

        return all_permissions

    def authorize(self, context: AuthorizationContext) -> AuthorizationDecision:
        """
        Make authorization decision for a request.

        Implements RBAC-001: Dynamic permission evaluation with conditions.

        Args:
            context: Authorization context

        Returns:
            AuthorizationDecision with allow/deny and reasoning
        """
        permissions = self.get_principal_permissions(context.principal_id)

        matched_permissions = []
        failed_conditions = []

        # Check each permission
        for permission in permissions:
            # Check if permission applies to this resource
            if not permission.matches_resource(
                context.resource_type, context.resource_id
            ):
                continue

            # Check if permission allows this action
            if not permission.allows_action(context.action):
                continue

            # Check conditions
            if not permission.evaluate_conditions(context):
                failed_conditions.extend(permission.conditions)
                continue

            # Permission matches!
            matched_permissions.append(permission)

        # Authorization decision
        allowed = len(matched_permissions) > 0

        if allowed:
            reason = f"Allowed by {len(matched_permissions)} permission(s)"
        elif failed_conditions:
            reason = f"Denied: {len(failed_conditions)} condition(s) not satisfied"
        else:
            reason = "Denied: No matching permissions"

        decision = AuthorizationDecision(
            allowed=allowed,
            principal_id=context.principal_id,
            resource_type=context.resource_type,
            resource_id=context.resource_id,
            action=context.action,
            matched_permissions=matched_permissions,
            failed_conditions=failed_conditions,
            reason=reason,
        )

        # Audit log
        logger.info(
            f"Authorization: principal={context.principal_id}, "
            f"resource={context.resource_type.value}/{context.resource_id}, "
            f"action={context.action.value}, allowed={allowed}, reason={reason}"
        )

        return decision


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # type: ignore[name-defined]

    rm = RoleManager()

    # Create custom role with conditional permissions
    business_hours_condition = Condition(
        type=ConditionType.TIME_RANGE,
        parameters={
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        },
    )

    office_network_condition = Condition(
        type=ConditionType.IP_NETWORK,
        parameters={
            "allowed_networks": ["10.0.0.0/8", "192.168.0.0/16"],
        },
    )

    business_role = Role(
        name="business_user",
        description="Business hours access from office network",
        permissions=[
            Permission(
                resource_type=ResourceType.VM,
                resource_id="vm-prod-*",    # Only production VMs
                actions=[Action.READ, Action.EXECUTE],
                conditions=[business_hours_condition, office_network_condition],
                description="Read/execute production VMs during business hours from office",
            ),
        ],
    )

    rm.create_role(business_role)
    rm.assign_role("user@example.com", "business_user")

    # Test authorization
    context = AuthorizationContext(
        principal_id="user@example.com",
        principal_attributes={"department": "engineering"},
        resource_type=ResourceType.VM,
        resource_id="vm-prod-001",
        resource_attributes={"tags": {"env": "production"}},
        action=Action.READ,
        client_ip="192.168.1.100",
    )

    decision = rm.authorize(context)
    print(f"Decision: {decision.allowed}, Reason: {decision.reason}")
