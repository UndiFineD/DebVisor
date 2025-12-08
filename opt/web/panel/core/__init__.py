"""Core Package - Shared Utilities

Provides RPC client, validators, and other shared functionality.
"""

from .rpc_client import get_rpc_client, close_rpc_client, RPCClientError

__all__ = ["get_rpc_client", "close_rpc_client", "RPCClientError"]
