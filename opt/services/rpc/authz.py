#!/usr/bin/env python3
"""
RPC Service Authorization Module

Implements RBAC (Role-Based Access Control) with wildcard permission matching.

Permission Format: resource:action[:subresource]
Examples:
  - node:register
  - node:list
  - storage:snapshot:create
  - storage:*  (matches all storage operations)
  - *          (matches all operations)

Permission Matching:
  - Exact match: 'node:register' matches 'node:register'
  - Wildcard match: 'node:*' matches 'node:register', 'node:list', etc.
  - Superuser: '*' matches any permission
"""

import grpc
import logging
from typing import Optional, List, Dict, Any, Callable

from opt.services.rpc.auth import Identity

logger = logging.getLogger(__name__)


class PermissionMatcher:
    """Utility for matching permission specs with wildcards"""

    @staticmethod
    def matches(required_permission: str, caller_permissions: List[str]) -> bool:
        """
        Check if caller has required permission.

        Supports wildcard matching:
        - 'storage:*' matches 'storage:snapshot:create', 'storage:snapshot:list', etc.
        - '*' matches any permission

        Args:
            required_permission: Permission to check (e.g., 'storage:snapshot:create')
            caller_permissions: List of permissions caller has

        Returns:
            True if caller has permission, False otherwise
        """
        # Examples:
        # required: 'storage:snapshot:create'
        # caller has: 'storage:*' -> MATCH
        # caller has: 'storage:snapshot:*' -> MATCH
        # caller has: 'storage:snapshot:create' -> MATCH
        # caller has: 'node:*' -> NO MATCH

        for perm in caller_permissions:
            if PermissionMatcher._perm_matches(required_permission, perm):
                return True
        return False

    @staticmethod
    def _perm_matches(required: str, pattern: str) -> bool:
        """
        Check if required permission matches a wildcard pattern.

        Args:
            required: Specific permission needed (e.g., 'storage:snapshot:create')
            pattern: Pattern with possible wildcards (e.g., 'storage:*')

        Returns:
            True if pattern matches required, False otherwise
        """
        # Special case: * matches everything
        if pattern == "*":
            return True

        required_parts = required.split(":")
        pattern_parts = pattern.split(":")

        # Pattern can't have more parts than required
        if len(pattern_parts) > len(required_parts):
            return False

        # Check each part
        for i, pattern_part in enumerate(pattern_parts):
            if pattern_part == "*":
                # Wildcard matches remaining parts
                return True
            if pattern_part != required_parts[i]:
                # Part mismatch
                return False

        # All parts matched and pattern has same length as required
        return len(pattern_parts) == len(required_parts)


def check_permission(
    identity: Optional[Identity],
    required_permission: str,
    context: grpc.ServicerContext,
) -> bool:
    """
    Check if authenticated identity has required permission.

    Raises PermissionError and calls context.abort() if permission denied.

    Args:
        identity: Authenticated Identity object
        required_permission: Permission required for operation (e.g., 'node:register')
        context: gRPC context for aborting on permission denied

    Returns:
        True if authorized

    Raises:
        PermissionError if not authenticated or lacks permission
    """
    # Not authenticated
    if not identity:
        logger.warning("Permission check failed: not authenticated")
        error_msg = "Not authenticated"
        context.abort(grpc.StatusCode.UNAUTHENTICATED, error_msg)
        raise PermissionError(error_msg)

    # Check permission
    if PermissionMatcher.matches(required_permission, identity.permissions):
        logger.debug(
            f"Permission granted: principal={identity.principal_id}, "
            f"permission={required_permission}"
        )
        return True

    # Permission denied
    logger.warning(
        f"Permission denied: principal={identity.principal_id}, "
        f"permission={required_permission}, "
        f"has_permissions={identity.permissions}"
    )

    error_msg = (
        f"Principal {identity.principal_id} lacks permission: {required_permission}"
    )
    context.abort(grpc.StatusCode.PERMISSION_DENIED, error_msg)
    raise PermissionError(error_msg)


class AuthorizationInterceptor(grpc.ServerInterceptor):
    """
    Authorization interceptor for logging and policy enforcement.

    Note: Actual authorization checks happen in handlers
    using check_permission(). This interceptor provides
    additional logging and policy enforcement points.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize authorization interceptor.

        Args:
            config: Configuration dict
        """
        self.config = config
        logger.info("AuthorizationInterceptor initialized")

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Any],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:
        """
        Intercept RPC call for authorization.

        Args:
            continuation: Handler to call
            handler_call_details: Details about RPC call

        Returns:
            Handler response
        """
        # Authorization is checked per-operation in handlers
        # using check_permission() function
        return continuation(handler_call_details)


# Role Definitions for Documentation
ROLE_DEFINITIONS = {
    "admin": {"description": "Full cluster administration", "permissions": ["*"]},
    "operator": {
        "description": "Cluster operations and management",
        "permissions": [
            "node:*",
            "storage:*",
            "migration:*",
        ],
    },
    "developer": {
        "description": "CI/CD and application deployment",
        "permissions": [
            "node:list",
            "storage:snapshot:create",
            "storage:snapshot:list",
            "storage:clone:*",
        ],
    },
    "monitor": {
        "description": "Monitoring and health checks",
        "permissions": [
            "node:list",
            "node:heartbeat",
        ],
    },
    "viewer": {
        "description": "Read-only access",
        "permissions": [
            "node:list",
            "storage:snapshot:list",
        ],
    },
}

# Resource-specific permissions
RESOURCE_PERMISSIONS = {
    "node": [
        "register",  # Register node with cluster
        "list",  # List all nodes
        "heartbeat",  # Send health/heartbeat
    ],
    "storage": [
        "snapshot:create",  # Create snapshot
        "snapshot:list",  # List snapshots
        "snapshot:delete",  # Delete snapshot
        "clone:create",  # Clone image from template
        "replication:plan",  # Plan replication
        "replication:execute",  # Execute replication
    ],
    "migration": [
        "plan",  # Plan VM migration
        "execute",  # Execute VM migration
        "failover",  # Execute failover
    ],
}


if __name__ == "__main__":
    # Test permission matching
    logging.basicConfig(level=logging.DEBUG)

    # Test cases
    test_cases = [
        # (required, caller_permissions, expected_result)
        ("node:register", ["node:*"], True),
        ("node:register", ["node:register"], True),
        ("storage:snapshot:create", ["storage:*"], True),
        ("storage:snapshot:create", ["storage:snapshot:*"], True),
        ("storage:snapshot:create", ["storage:snapshot:create"], True),
        ("storage:snapshot:create", ["node:*"], False),
        ("any:permission", ["*"], True),
        ("anything:goes:here", ["*"], True),
    ]

    print("Testing permission matching:")
    for required, permissions, expected in test_cases:
        result = PermissionMatcher.matches(required, permissions)
        status = "?" if result == expected else "?"
        print(
            f"{status} matches({required}, {permissions}) = {result} (expected {expected})"
        )
