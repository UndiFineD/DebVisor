"""Passthrough Inventory UI Routes.

Web panel endpoints for hardware passthrough management:
- List PCI/GPU devices available for passthrough
- Display IOMMU group isolation status
- Bind/unbind devices to VFIO
- Profile-based assignment recommendations

Enterprise Features:
- Rate limiting per endpoint
- Input validation with JSON schema
- Structured error responses
"""
from __future__ import annotations
import logging
import re
from functools import wraps
from typing import Dict, Any, List, Optional, Callable
from flask import Blueprint, render_template, jsonify, request, g
from datetime import datetime, timezone

# Import passthrough manager with proper path handling
import sys
from pathlib import Path
_system_path = str(Path(__file__).parent.parent.parent.parent / "system")
if _system_path not in sys.path:
    sys.path.insert(0, _system_path)

# Rate limiting support
try:
    from flask_limiter import Limiter
    HAS_LIMITER = True
except ImportError:
    HAS_LIMITER = False
    Limiter = None

try:
    from passthrough_manager import PassthroughManager, PCIDevice, IOMMUGroup
    _HAS_PASSTHROUGH = True
except ImportError:
    PassthroughManager = None
    PCIDevice = None
    IOMMUGroup = None
    _HAS_PASSTHROUGH = False

logger = logging.getLogger(__name__)

# =============================================================================
# Input Validation
# =============================================================================

# PCI address pattern: DDDD:BB:DD.F (domain:bus:device.function)
PCI_ADDRESS_PATTERN = re.compile(r'^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7]$')


class ValidationError(Exception):
    """Input validation error."""

    def __init__(self, message: str, field: str = None, code: str = "VALIDATION_ERROR"):
        self.message = message
        self.field = field
        self.code = code
        super().__init__(message)


def validate_pci_address(address: str) -> bool:
    """Validate PCI address format."""
    if not address or not isinstance(address, str):
        return False
    return bool(PCI_ADDRESS_PATTERN.match(address))


def validate_request_json(required_fields: List[str] = None,
                          validators: Dict[str, Callable] = None) -> Callable:
    """
    Decorator for validating JSON request body.

    Args:
        required_fields: List of required field names
        validators: Dict of field_name -> validator_function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)

            if data is None:
                return jsonify({
                    "error": "Invalid JSON body",
                    "code": "INVALID_JSON",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }), 400

            # Check required fields
            if required_fields:
                missing = [f for f in required_fields if f not in data]
                if missing:
                    return jsonify({
                        "error": f"Missing required fields: {', '.join(missing)}",
                        "code": "MISSING_FIELDS",
                        "fields": missing,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }), 400

            # Run validators
            if validators:
                for field_name, validator in validators.items():
                    if field_name in data:
                        try:
                            if not validator(data[field_name]):
                                return jsonify({
                                    "error": f"Invalid value for field: {field_name}",
                                    "code": "INVALID_FIELD",
                                    "field": field_name,
                                    "timestamp": datetime.now(timezone.utc).isoformat()
                                }), 400
                        except Exception as e:
                            return jsonify({
                                "error": f"Validation error for {field_name}: {str(e)}",
                                "code": "VALIDATION_ERROR",
                                "field": field_name,
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }), 400

            # Store validated data in g for handler access
            g.validated_data = data
            return f(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Rate Limiting (in-memory fallback when flask-limiter not available)
# =============================================================================

class SimpleRateLimiter:
    """Simple in-memory rate limiter when flask-limiter is not available."""

    def __init__(self):
        self._requests: Dict[str, List[float]] = {}
        self._lock = None
        try:
            import threading
            self._lock = threading.Lock()
        except ImportError:
            pass

    def is_allowed(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        """Check if request is allowed under rate limit."""
        import time
        now = time.time()
        window_start = now - window_seconds

        if self._lock:
            with self._lock:
                return self._check_limit(key, limit, now, window_start)
        return self._check_limit(key, limit, now, window_start)

    def _check_limit(self, key: str, limit: int, now: float, window_start: float) -> bool:
        if key not in self._requests:
            self._requests[key] = []

        # Clean old requests
        self._requests[key] = [t for t in self._requests[key] if t > window_start]

        if len(self._requests[key]) >= limit:
            return False

        self._requests[key].append(now)
        return True


_rate_limiter = SimpleRateLimiter()


def rate_limit(limit: int = 60, window: int = 60, key_func: Callable = None):
    """
    Rate limiting decorator.

    Args:
        limit: Maximum requests per window
        window: Window size in seconds
        key_func: Function to generate rate limit key (default: client IP)
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Generate key
            if key_func:
                key = key_func()
            else:
                key = request.remote_addr or "unknown"

            rate_key = f"{f.__name__}:{key}"

            if not _rate_limiter.is_allowed(rate_key, limit, window):
                return jsonify({
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "retry_after": window,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }), 429

            return f(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Blueprint and Routes
# =============================================================================

passthrough_bp = Blueprint("passthrough", __name__, url_prefix="/passthrough")

# Global manager instance
_manager: Optional[Any] = None


def get_manager() -> Optional[Any]:
    """Get or create passthrough manager instance."""
    global _manager
    if _manager is None:
        if not _HAS_PASSTHROUGH or PassthroughManager is None:
            logger.error("PassthroughManager not available")
            return None
        _manager = PassthroughManager()
        _manager.scan_devices()
    return _manager


@passthrough_bp.route("/")
def index():
    """Passthrough inventory main page."""
    return render_template("passthrough/index.html")


@passthrough_bp.route("/api/devices")
@rate_limit(limit=30, window=60)
def api_list_devices():
    """API: List all PCI devices with passthrough info."""
    manager = get_manager()
    if manager is None:
        return jsonify({
            "error": "Passthrough manager not available",
            "code": "SERVICE_UNAVAILABLE",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

    # Refresh device list
    devices = manager.scan_devices()

    device_list = []
    for dev in devices:
        group = manager.get_iommu_group(dev.iommu_group)
        device_list.append({
            "address": dev.address,
            "vendor_id": dev.vendor_id,
            "product_id": dev.product_id,
            "device_class": dev.device_class,
            "device_name": dev.device_name,
            "driver": dev.driver_in_use,
            "iommu_group": dev.iommu_group,
            "isolated": group.is_isolated if group else False,
            "group_devices": len(group.devices) if group else 0,
            "is_vfio_bound": dev.driver_in_use == "vfio-pci",
        })

    return jsonify({
        "devices": device_list,
        "summary": manager.get_passthrough_summary(),
    })


@passthrough_bp.route("/api/gpus")
@rate_limit(limit=30, window=60)
def api_list_gpus():
    """API: List GPU devices suitable for passthrough."""
    manager = get_manager()
    if manager is None:
        return jsonify({
            "error": "Passthrough manager not available",
            "code": "SERVICE_UNAVAILABLE",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

    gpus = manager.get_gpus()
    gpu_list = []
    for gpu in gpus:
        group = manager.get_iommu_group(gpu.iommu_group)
        gpu_list.append({
            "address": gpu.address,
            "name": gpu.device_name,
            "vendor_id": gpu.vendor_id,
            "product_id": gpu.product_id,
            "driver": gpu.driver_in_use,
            "iommu_group": gpu.iommu_group,
            "isolated": group.is_isolated if group else False,
            "passthrough_ready": (
                group is not None
                and gpu.driver_in_use != "nouveau"
                and manager.check_iommu_enabled()
            ),
        })

    return jsonify({"gpus": gpu_list})


@passthrough_bp.route("/api/iommu-groups")
def api_list_iommu_groups():
    """API: List all IOMMU groups with their devices."""
    manager = get_manager()
    if manager is None:
        return jsonify({"error": "Passthrough manager not available"}), 500

    # Refresh
    manager.scan_devices()

    groups = []
    for group_id, group in manager._iommu_groups.items():
        groups.append({
            "id": group_id,
            "isolated": group.is_isolated,
            "device_count": len(group.devices),
            "devices": [
                {
                    "address": d.address,
                    "name": d.device_name,
                    "class": d.device_class,
                    "driver": d.driver_in_use,
                }
                for d in group.devices
            ],
        })

    return jsonify({"groups": sorted(groups, key=lambda g: g["id"])})


@passthrough_bp.route("/api/profiles")
def api_list_profiles():
    """API: List available passthrough profiles."""
    manager = get_manager()
    if manager is None:
        return jsonify({"error": "Passthrough manager not available"}), 500

    profiles = []
    for profile_id, profile in manager.PROFILES.items():
        # Find matching devices
        matching = []
        for dev in manager._device_cache:
            if any(dev.device_class.startswith(cls[:2]) for cls in profile.device_classes):
                matching.append({
                    "address": dev.address,
                    "name": dev.device_name,
                })

        profiles.append({
            "id": profile_id,
            "name": profile.name,
            "description": profile.description,
            "device_classes": profile.device_classes,
            "matching_devices": matching,
        })

    return jsonify({"profiles": profiles})


@passthrough_bp.route("/api/bind", methods=["POST"])
@rate_limit(limit=10, window=60)  # More restrictive for mutations
@validate_request_json(
    required_fields=["address"],
    validators={"address": validate_pci_address}
)
def api_bind_device():
    """API: Bind device to VFIO-PCI for passthrough."""
    manager = get_manager()
    if manager is None:
        return jsonify({
            "error": "Passthrough manager not available",
            "code": "SERVICE_UNAVAILABLE",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

    data = g.validated_data
    address = data["address"]

    logger.info(f"Binding device {address} to VFIO-PCI (client: {request.remote_addr})")
    success = manager.bind_to_vfio(address)

    if success:
        return jsonify({"status": "success", "message": f"Bound {address} to vfio-pci"})
    else:
        return jsonify({"error": f"Failed to bind {address}"}), 500


@passthrough_bp.route("/api/release", methods=["POST"])
@rate_limit(limit=10, window=60)  # More restrictive for mutations
@validate_request_json(
    required_fields=["address"],
    validators={"address": validate_pci_address}
)
def api_release_device():
    """API: Release device from VFIO-PCI back to host driver."""
    manager = get_manager()
    if manager is None:
        return jsonify({
            "error": "Passthrough manager not available",
            "code": "SERVICE_UNAVAILABLE",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

    data = g.validated_data
    address = data["address"]

    logger.info(f"Releasing device {address} from VFIO-PCI (client: {request.remote_addr})")
    success = manager.release_device(address)

    if success:
        return jsonify({"status": "success", "message": f"Released {address} from vfio-pci"})
    else:
        return jsonify({"error": f"Failed to release {address}"}), 500


@passthrough_bp.route("/api/status")
def api_status():
    """API: Get overall passthrough system status."""
    manager = get_manager()
    if manager is None:
        return jsonify({"error": "Passthrough manager not available"}), 500

    summary = manager.get_passthrough_summary()

    # Add recommendations
    recommendations = []
    if not summary["iommu_enabled"]:
        recommendations.append({
            "severity": "error",
            "message": "IOMMU is not enabled. Add 'intel_iommu=on' or 'amd_iommu=on' to kernel parameters.",
        })

    if summary["isolated_groups"] < summary["gpus"]:
        recommendations.append({
            "severity": "warning",
            "message": "Some GPUs share IOMMU groups with other devices. ACS override patch may be needed.",
        })

    return jsonify({
        "summary": summary,
        "recommendations": recommendations,
        "status": "ready" if summary["iommu_enabled"] else "not_ready",
    })
