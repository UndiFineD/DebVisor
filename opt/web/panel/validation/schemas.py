#!/usr/bin/env python3
"""
Input Validation Schemas for DebVisor Web Panel.

Provides comprehensive Marshmallow schemas for all API endpoints
to prevent SQL injection, XSS, command injection, and other attacks.

Author: DebVisor Team
Date: November 29, 2025
"""

from flask import request, jsonify
from functools import wraps
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from typing import Any, Dict
import re


# =============================================================================
# Base Schemas & Validators
# =============================================================================

class StrictSchema(Schema):
    """Base schema with strict mode enabled."""

    class Meta:
        strict = True
        unknown = 'RAISE'  # Reject unknown fields


# Custom validators
def validate_hostname(value: str) -> None:
    """Validate hostname format."""
    pattern = (
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    )
    if not re.match(pattern, value):
        raise ValidationError("Invalid hostname format")


def validate_ip_address(value: str) -> None:
    """Validate IP address (IPv4 or IPv6)."""
    import ipaddress
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError("Invalid IP address")


def validate_cidr(value: str) -> None:
    """Validate CIDR notation."""
    import ipaddress
    try:
        ipaddress.ip_network(value, strict=False)
    except ValueError:
        raise ValidationError("Invalid CIDR notation")


def validate_safe_path(value: str) -> None:
    """Validate path doesn't contain directory traversal."""
    if '..' in value or value.startswith('/'):
        raise ValidationError("Path contains invalid characters or directory traversal")


def validate_alphanumeric_dash(value: str) -> None:
    """Validate alphanumeric with dashes and underscores only."""
    if not re.match(r'^[a-zA-Z0-9_\-]+$', value):
        raise ValidationError("Only alphanumeric characters, dashes, and underscores allowed")


# =============================================================================
# Authentication Schemas
# =============================================================================

class LoginSchema(StrictSchema):
    """Login request validation."""

    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate_alphanumeric_dash
        ]
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    remember = fields.Bool(missing=False)


class RegisterSchema(StrictSchema):
    """User registration validation."""

    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate_alphanumeric_dash
        ]
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    password_confirm = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )

    @validates_schema
    def validate_passwords_match(self, data: Dict[str, Any], **kwargs: Any) -> None:
        """Ensure passwords match."""
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError('Passwords must match', field_name='password_confirm')


class ChangePasswordSchema(StrictSchema):
    """Password change validation."""

    current_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    new_password_confirm = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )

    @validates_schema
    def validate_passwords(self, data: Dict[str, Any], **kwargs: Any) -> None:
        """Validate password requirements."""
        if data.get('new_password') != data.get('new_password_confirm'):
            raise ValidationError('New passwords must match', field_name='new_password_confirm')

        if data.get('current_password') == data.get('new_password'):
            raise ValidationError(
                'New password must be different from current',
                field_name='new_password')


# =============================================================================
# Node Management Schemas
# =============================================================================

class NodeCreateSchema(StrictSchema):
    """Node creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    hostname = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=253),
            validate_hostname
        ]
    )
    ip_address = fields.Str(
        required=True,
        validate=validate_ip_address
    )
    port = fields.Int(
        missing=8006,
        validate=validate.Range(min=1, max=65535)
    )
    node_type = fields.Str(
        required=True,
        validate=validate.OneOf(['hypervisor', 'storage', 'compute'])
    )
    region = fields.Str(
        missing='default',
        validate=[
            validate.Length(min=1, max=50),
            validate_alphanumeric_dash
        ]
    )
    tags = fields.List(
        fields.Str(validate=validate.Length(max=50)),
        missing=[]
    )


class NodeUpdateSchema(StrictSchema):
    """Node update validation."""

    name = fields.Str(
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    hostname = fields.Str(
        validate=[
            validate.Length(min=1, max=253),
            validate_hostname
        ]
    )
    ip_address = fields.Str(validate=validate_ip_address)
    port = fields.Int(validate=validate.Range(min=1, max=65535))
    node_type = fields.Str(validate=validate.OneOf(['hypervisor', 'storage', 'compute']))
    region = fields.Str(
        validate=[
            validate.Length(min=1, max=50),
            validate_alphanumeric_dash
        ]
    )
    tags = fields.List(fields.Str(validate=validate.Length(max=50)))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'maintenance']))


# =============================================================================
# Storage Schemas
# =============================================================================

class StoragePoolCreateSchema(StrictSchema):
    """Storage pool creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    pool_type = fields.Str(
        required=True,
        validate=validate.OneOf(['zfs', 'ceph', 'lvm', 'nfs'])
    )
    node_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    size_gb = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=1000000)
    )
    replication = fields.Int(
        missing=1,
        validate=validate.Range(min=1, max=10)
    )
    compression = fields.Bool(missing=True)
    deduplication = fields.Bool(missing=False)


class VolumeCreateSchema(StrictSchema):
    """Volume creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    pool_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    size_gb = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=10000)
    )
    filesystem = fields.Str(
        missing='ext4',
        validate=validate.OneOf(['ext4', 'xfs', 'btrfs', 'zfs'])
    )
    mount_path = fields.Str(
        validate=[
            validate.Length(max=255),
            validate_safe_path
        ]
    )


# =============================================================================
# Network Schemas
# =============================================================================

class NetworkCreateSchema(StrictSchema):
    """Network creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    vlan_id = fields.Int(
        validate=validate.Range(min=1, max=4094)
    )
    cidr = fields.Str(
        required=True,
        validate=validate_cidr
    )
    gateway = fields.Str(validate=validate_ip_address)
    dns_servers = fields.List(
        fields.Str(validate=validate_ip_address),
        missing=[]
    )
    dhcp_enabled = fields.Bool(missing=True)
    dhcp_range_start = fields.Str(validate=validate_ip_address)
    dhcp_range_end = fields.Str(validate=validate_ip_address)


# =============================================================================
# VM/Container Schemas
# =============================================================================

class VMCreateSchema(StrictSchema):
    """Virtual machine creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    node_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    vcpus = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=256)
    )
    memory_mb = fields.Int(
        required=True,
        validate=validate.Range(min=128, max=1048576)  # 128MB to 1TB
    )
    disk_gb = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=10000)
    )
    os_type = fields.Str(
        required=True,
        validate=validate.OneOf(['linux', 'windows', 'bsd', 'other'])
    )
    template_id = fields.Int(validate=validate.Range(min=1))
    network_id = fields.Int(validate=validate.Range(min=1))
    auto_start = fields.Bool(missing=False)


# =============================================================================
# Backup Schemas
# =============================================================================

class BackupCreateSchema(StrictSchema):
    """Backup creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    resource_type = fields.Str(
        required=True,
        validate=validate.OneOf(['vm', 'container', 'volume', 'full'])
    )
    resource_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    compression = fields.Str(
        missing='gzip',
        validate=validate.OneOf(['none', 'gzip', 'lz4', 'zstd'])
    )
    retention_days = fields.Int(
        missing=30,
        validate=validate.Range(min=1, max=3650)
    )


class BackupScheduleSchema(StrictSchema):
    """Backup schedule validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    cron_expression = fields.Str(
        required=True,
        validate=validate.Length(min=9, max=100)
    )
    resource_type = fields.Str(
        required=True,
        validate=validate.OneOf(['vm', 'container', 'volume', 'full'])
    )
    resource_ids = fields.List(
        fields.Int(validate=validate.Range(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )
    retention_days = fields.Int(
        missing=30,
        validate=validate.Range(min=1, max=3650)
    )
    enabled = fields.Bool(missing=True)

    @validates('cron_expression')
    def validate_cron(self, value: str) -> None:
        """Validate cron expression format."""
        parts = value.split()
        if len(parts) != 5:
            raise ValidationError(
                "Cron expression must have 5 parts (minute hour day month weekday)")


# =============================================================================
# Job/Scheduler Schemas
# =============================================================================

class JobCreateSchema(StrictSchema):
    """Job creation validation."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate_alphanumeric_dash
        ]
    )
    job_type = fields.Str(
        required=True,
        validate=validate.OneOf(['backup', 'migration', 'snapshot', 'cleanup', 'custom'])
    )
    schedule = fields.Str(
        validate=validate.Length(min=9, max=100)
    )
    parameters = fields.Dict(missing={})
    enabled = fields.Bool(missing=True)
    max_retries = fields.Int(
        missing=3,
        validate=validate.Range(min=0, max=10)
    )
    timeout_seconds = fields.Int(
        missing=3600,
        validate=validate.Range(min=1, max=86400)
    )


# =============================================================================
# Search/Filter Schemas
# =============================================================================

class PaginationSchema(StrictSchema):
    """Pagination parameters validation."""

    page = fields.Int(
        missing=1,
        validate=validate.Range(min=1, max=10000)
    )
    per_page = fields.Int(
        missing=20,
        validate=validate.Range(min=1, max=100)
    )
    sort_by = fields.Str(
        missing='created_at',
        validate=validate.Length(max=50)
    )
    order = fields.Str(
        missing='desc',
        validate=validate.OneOf(['asc', 'desc'])
    )


class SearchSchema(PaginationSchema):
    """Search parameters validation."""

    query = fields.Str(
        validate=validate.Length(max=255)
    )
    filters = fields.Dict(missing={})
    date_from = fields.DateTime()
    date_to = fields.DateTime()


# =============================================================================
# Helper Functions
# =============================================================================

def validate_request_data(schema_class: type, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate request data against schema.

    Args:
        schema_class: Marshmallow schema class
        data: Request data to validate

    Returns:
        Validated and cleaned data

    Raises:
        ValidationError: If validation fails
    """
    schema = schema_class()
    return schema.load(data)


def get_validation_errors(error: ValidationError) -> Dict[str, list]:
    """
    Extract validation errors in user-friendly format.

    Args:
        error: Marshmallow ValidationError

    Returns:
        Dictionary of field errors
    """
    return error.messages


# =============================================================================
# Flask Decorator for Automatic Validation
# =============================================================================


def validate_json(schema_class: type):
    """
    Decorator to automatically validate JSON request body.

    Usage:
        @app.route('/api/nodes', methods=['POST'])
        @validate_json(NodeCreateSchema)
        def create_node(validated_data):
            # validated_data is already cleaned and validated
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                if not request.is_json:
                    return jsonify({
                        'error': 'Content-Type must be application/json'
                    }), 400

                data = request.get_json()
                validated = validate_request_data(schema_class, data)

                # Pass validated data to the route handler
                return f(validated_data=validated, *args, **kwargs)

            except ValidationError as e:
                return jsonify({
                    'error': 'Validation failed',
                    'details': get_validation_errors(e)
                }), 400

        return wrapper
    return decorator


def validate_query_params(schema_class: type):
    """
    Decorator to automatically validate query parameters.

    Usage:
        @app.route('/api/nodes', methods=['GET'])
        @validate_query_params(PaginationSchema)
        def list_nodes(validated_params):
            # validated_params contains cleaned query params
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                params = request.args.to_dict()
                validated = validate_request_data(schema_class, params)

                return f(validated_params=validated, *args, **kwargs)

            except ValidationError as e:
                return jsonify({
                    'error': 'Invalid query parameters',
                    'details': get_validation_errors(e)
                }), 400

        return wrapper
    return decorator


if __name__ == "__main__":
    # Example usage
    test_data = {
        'username': 'testuser',
        'password': 'securepassword123',
        'remember': True
    }

    try:
        validated = validate_request_data(LoginSchema, test_data)
        print("Valid:", validated)
    except ValidationError as e:
        print("Errors:", get_validation_errors(e))
