"""Routes Package - Blueprint Organization

Provides centralized routing for authentication, node management, and storage operations.
"""

from .auth import auth_bp
from .nodes import nodes_bp
from .storage import storage_bp

__all__ = ['auth_bp', 'nodes_bp', 'storage_bp']
