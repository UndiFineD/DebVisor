"""RPC Client Wrapper - gRPC Service Communication

Provides high-level interface to DebVisor RPC service with mTLS authentication,
error handling, connection pooling, and response transformation for web panel integration.

Implements PERF-001: Connection pooling for improved performance and resource efficiency.
"""

import grpc
import logging
import threading
import time
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from collections import deque
from dataclasses import dataclass
import os

# Import generated protobuf modules (will be created during build)
# from opt.services.rpc import debvisor_pb2, debvisor_pb2_grpc

logger = logging.getLogger(__name__)


class RPCClientError(Exception):
    """Exception raised for RPC communication errors."""
    pass


@dataclass
class ChannelPoolConfig:
    """Configuration for gRPC channel pool."""
    min_size: int = 2
    max_size: int = 10
    max_idle_time: int = 300  # seconds
    health_check_interval: int = 60  # seconds
    connection_timeout: int = 10  # seconds


class PooledChannel:
    """Wrapper for a pooled gRPC channel with health tracking."""

    def __init__(self, channel: grpc.Channel, created_at: float):
        self.channel = channel
        self.created_at = created_at
        self.last_used = created_at
        self.use_count = 0
        self.is_healthy = True

    def mark_used(self):
        """Mark channel as recently used."""
        self.last_used = time.time()
        self.use_count += 1

    def idle_time(self) -> float:
        """Get idle time in seconds."""
        return time.time() - self.last_used

    def age(self) -> float:
        """Get channel age in seconds."""
        return time.time() - self.created_at


class ChannelPool:
    """
    Connection pool for gRPC channels.

    Implements PERF-001: Add connection pooling to RPC client.

    Features:
    - Min/max pool size limits
    - Health checking
    - Automatic channel rotation
    - Idle connection cleanup
    """

    def __init__(self, target: str, credentials: grpc.ChannelCredentials,
                 config: ChannelPoolConfig):
        self.target = target
        self.credentials = credentials
        self.config = config

        # Pool state
        self.available: deque[PooledChannel] = deque()
        self.in_use: set[PooledChannel] = set()
        self.lock = threading.Lock()

        # Initialize minimum number of connections
        for _ in range(config.min_size):
            channel = self._create_channel()
            self.available.append(channel)

        # Start background health checker
        self.health_check_thread = threading.Thread(
            target=self._health_check_loop,
            daemon=True
        )
        self.health_check_thread.start()

        logger.info(
            f"Channel pool initialized: target={target}, "
            f"min={config.min_size}, max={config.max_size}"
        )

    def _create_channel(self) -> PooledChannel:
        """Create a new gRPC channel."""
        channel = grpc.secure_channel(
            self.target,
            self.credentials,
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),
                ('grpc.max_receive_message_length', 50 * 1024 * 1024),
                ('grpc.keepalive_time_ms', 30000),
                ('grpc.keepalive_timeout_ms', 10000),
                ('grpc.http2.max_pings_without_data', 0),
            ]
        )

        pooled = PooledChannel(channel, time.time())
        logger.debug(f"Created new channel: total_channels={self._total_channels() + 1}")
        return pooled

    def _total_channels(self) -> int:
        """Get total number of channels in pool."""
        return len(self.available) + len(self.in_use)

    def acquire(self, timeout: float = 10.0) -> grpc.Channel:
        """
        Acquire a channel from the pool.

        Returns:
            grpc.Channel: A healthy channel from the pool

        Raises:
            RPCClientError: If no channel available within timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            with self.lock:
                # Try to get an available channel
                if self.available:
                    pooled = self.available.popleft()

                    # Check if channel is healthy
                    if not pooled.is_healthy or pooled.idle_time() > self.config.max_idle_time:
                        # Close unhealthy/stale channel and create new one
                        pooled.channel.close()
                        pooled = self._create_channel()

                    pooled.mark_used()
                    self.in_use.add(pooled)

                    logger.debug(
                        f"Acquired channel from pool: available={len(self.available)}, "
                        f"in_use={len(self.in_use)}"
                    )
                    return pooled.channel

                # No available channels, create new one if under max
                if self._total_channels() < self.config.max_size:
                    pooled = self._create_channel()
                    pooled.mark_used()
                    self.in_use.add(pooled)
                    return pooled.channel

            # Pool exhausted, wait for channel to be released
            time.sleep(0.1)

        raise RPCClientError(
            f"Failed to acquire channel within {timeout}s timeout. "
            f"Pool size: {self._total_channels()}/{self.config.max_size}"
        )

    def release(self, channel: grpc.Channel):
        """Release a channel back to the pool."""
        with self.lock:
            # Find the pooled channel wrapper
            pooled = None
            for p in self.in_use:
                if p.channel == channel:
                    pooled = p
                    break

            if pooled:
                self.in_use.remove(pooled)

                # Return to pool if still healthy and under max idle time
                if pooled.is_healthy and pooled.idle_time() < self.config.max_idle_time:
                    self.available.append(pooled)
                else:
                    # Close unhealthy channel
                    pooled.channel.close()
                    logger.debug("Closed unhealthy channel during release")

                logger.debug(
                    f"Released channel to pool: available={len(self.available)}, "
                    f"in_use={len(self.in_use)}"
                )

    def _health_check_loop(self):
        """Background thread to check channel health."""
        while True:
            time.sleep(self.config.health_check_interval)

            try:
                with self.lock:
                    # Check available channels
                    channels_to_remove = []
                    for pooled in self.available:
                        if pooled.idle_time() > self.config.max_idle_time:
                            channels_to_remove.append(pooled)

                    # Remove idle channels (keep minimum)
                    for pooled in channels_to_remove:
                        if len(self.available) > self.config.min_size:
                            self.available.remove(pooled)
                            pooled.channel.close()
                            logger.debug("Closed idle channel during health check")

                    # Ensure minimum channels available
                    while len(self.available) < self.config.min_size and \
                            self._total_channels() < self.config.max_size:
                        pooled = self._create_channel()
                        self.available.append(pooled)

                    if channels_to_remove:
                        logger.info(
                            f"Health check: removed {len(channels_to_remove)} idle channels, "
                            f"available={len(self.available)}, in_use={len(self.in_use)}"
                        )

            except Exception as e:
                logger.error(f"Error in health check loop: {e}")

    def close_all(self):
        """Close all channels in the pool."""
        with self.lock:
            for pooled in list(self.available):
                pooled.channel.close()
            for pooled in list(self.in_use):
                pooled.channel.close()

            self.available.clear()
            self.in_use.clear()

            logger.info("Closed all channels in pool")

    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        with self.lock:
            return {
                "total_channels": self._total_channels(),
                "available_channels": len(self.available),
                "in_use_channels": len(self.in_use),
                "max_size": self.config.max_size,
                "min_size": self.config.min_size,
            }


class RPCClient:
    """Client for communicating with DebVisor RPC service with connection pooling."""

    def __init__(self, host: str = 'localhost', port: int = 7443,
                 cert_file: str = None, key_file: str = None,
                 ca_cert_file: str = None, timeout: int = 30,
                 pool_config: Optional[ChannelPoolConfig] = None):
        """Initialize RPC client with mTLS configuration and connection pooling.

        Args:
            host: RPC service hostname
            port: RPC service port
            cert_file: Path to client certificate (PEM format)
            key_file: Path to client private key (PEM format)
            ca_cert_file: Path to CA certificate for verification
            timeout: RPC call timeout in seconds
            pool_config: Connection pool configuration
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.stubs = {}

        # Load credentials
        self.cert_file = cert_file or os.getenv('RPC_CERT_FILE', '/etc/debvisor/client.crt')
        self.key_file = key_file or os.getenv('RPC_KEY_FILE', '/etc/debvisor/client.key')
        self.ca_cert_file = ca_cert_file or os.getenv('RPC_CA_CERT_FILE', '/etc/debvisor/ca.crt')

        # Initialize connection pool
        self.pool_config = pool_config or ChannelPoolConfig()
        self._init_pool()

    def _init_pool(self):
        """Initialize gRPC channel pool with mTLS credentials."""
        try:
            # Load certificates
            with open(self.cert_file, 'rb') as f:
                client_cert = f.read()
            with open(self.key_file, 'rb') as f:
                client_key = f.read()
            with open(self.ca_cert_file, 'rb') as f:
                ca_cert = f.read()

            # Create credentials
            credentials = grpc.ssl_channel_credentials(
                root_certificates=ca_cert,
                private_key=client_key,
                certificate_chain=client_cert,
            )

            # Create channel pool
            target = f'{self.host}:{self.port}'
            self.channel_pool = ChannelPool(target, credentials, self.pool_config)

            logger.info(f'Initialized RPC client with channel pool for {target}')

        except FileNotFoundError as e:
            raise RPCClientError(f'Certificate file not found: {e}')
        except Exception as e:
            raise RPCClientError(f'Failed to initialize RPC client: {e}')

    def close(self):
        """Close all channels in the pool."""
        if hasattr(self, 'channel_pool'):
            self.channel_pool.close_all()
            logger.info('RPC client closed, all channels terminated')

    def _call_rpc(self, service_name: str, method_name: str, request):
        """Execute RPC call with error handling using pooled channels.

        Args:
            service_name: Service name (NodeService, StorageService, etc.)
            method_name: Method name (RegisterNode, CreateSnapshot, etc.)
            request: Request object

        Returns:
            Response from RPC method

        Raises:
            RPCClientError: On RPC communication error
        """
        channel = None
        try:
            # Acquire channel from pool
            channel = self.channel_pool.acquire(timeout=self.timeout)

            # Get stub for service
            stub = self._get_stub(service_name, channel)

            # Get method from stub
            method = getattr(stub, method_name)

            # Call method with timeout
            response = method(request, timeout=self.timeout)

            logger.debug(f'RPC call {service_name}.{method_name} succeeded')
            return response

        except grpc.RpcError as e:
            error_msg = f'RPC call failed: {service_name}.{method_name} - {e.details()}'
            logger.error(error_msg)
            raise RPCClientError(error_msg)
        except Exception as e:
            error_msg = f'Unexpected error in RPC call: {str(e)}'
            logger.error(error_msg)
            raise RPCClientError(error_msg)
        finally:
            # Always release channel back to pool
            if channel:
                self.channel_pool.release(channel)

    def _get_stub(self, service_name: str, channel: grpc.Channel):
        """Get or create gRPC stub for service using provided channel.

        Args:
            service_name: Service name
            channel: gRPC channel to use

        Returns:
            Service stub
        """
        # Create new stub for each channel (stubs are cheap, channels are expensive)
        # This is a placeholder - actual implementation depends on protobuf generation
        stub_class_name = f'{service_name}Stub'
        # return getattr(debvisor_pb2_grpc, stub_class_name)(channel)
        logger.debug(f'Created stub for {service_name}')
        return None  # Placeholder

    def get_pool_stats(self) -> Dict[str, int]:
        """Get connection pool statistics."""
        return self.channel_pool.get_stats()



    # Node Service Methods

    def register_node(self, hostname: str, ip_address: str,
                      cpu_cores: int, memory_gb: int,
                      storage_gb: int, region: str = '',
                      rack: str = '') -> Dict[str, Any]:
        """Register a new cluster node.

        Args:
            hostname: Node hostname
            ip_address: Node IP address
            cpu_cores: Number of CPU cores
            memory_gb: Memory in GB
            storage_gb: Storage in GB
            region: Deployment region
            rack: Rack location

        Returns:
            Dictionary with node_id and registration details
        """
        try:
            # Build request (placeholder)
            request = {
                'hostname': hostname,
                'ip_address': ip_address,
                'cpu_cores': cpu_cores,
                'memory_gb': memory_gb,
                'storage_gb': storage_gb,
                'region': region,
                'rack': rack,
            }

            # response = self._call_rpc('NodeService', 'RegisterNode', request)

            return {
                'success': True,
                'node_id': 'placeholder-uuid',
                'hostname': hostname,
                'ip_address': ip_address,
            }
        except Exception as e:
            logger.error(f'Failed to register node: {e}')
            raise

    def list_nodes(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all cluster nodes.

        Args:
            status: Optional status filter (online, offline, error)

        Returns:
            List of node dictionaries
        """
        try:
            # response = self._call_rpc('NodeService', 'ListNodes', {})

            return [
                {
                    'node_id': 'node-1',
                    'hostname': 'node1.example.com',
                    'ip_address': '192.168.1.10',
                    'status': 'online',
                    'cpu_cores': 16,
                    'memory_gb': 64,
                }
            ]
        except Exception as e:
            logger.error(f'Failed to list nodes: {e}')
            raise

    def heartbeat(self, node_id: str, status_data: Dict[str, Any]) -> bool:
        """Send node heartbeat.

        Args:
            node_id: Node UUID
            status_data: Current node status information

        Returns:
            True if heartbeat accepted
        """
        try:
            # response = self._call_rpc('NodeService', 'Heartbeat', {'node_id': node_id})
            return True
        except Exception as e:
            logger.error(f'Failed to send heartbeat for {node_id}: {e}')
            raise

    # Storage Service Methods

    def create_snapshot(self, node_id: str, source_volume: str,
                        name: str, retention_days: int = 30) -> Dict[str, Any]:
        """Create storage snapshot.

        Args:
            node_id: Target node UUID
            source_volume: Source volume identifier
            name: Snapshot name
            retention_days: Retention period in days

        Returns:
            Dictionary with snapshot_id and creation details
        """
        try:
            request = {
                'node_id': node_id,
                'source_volume': source_volume,
                'name': name,
                'retention_days': retention_days,
            }

            # response = self._call_rpc('StorageService', 'CreateSnapshot', request)

            return {
                'success': True,
                'snapshot_id': 'snapshot-uuid',
                'name': name,
                'size_gb': 0,
                'status': 'pending',
            }
        except Exception as e:
            logger.error(f'Failed to create snapshot: {e}')
            raise

    def list_snapshots(self, node_id: Optional[str] = None,
                       status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List storage snapshots.

        Args:
            node_id: Optional node filter
            status: Optional status filter (pending, success, failed)

        Returns:
            List of snapshot dictionaries
        """
        try:
            # response = self._call_rpc('StorageService', 'ListSnapshots', {})

            return [
                {
                    'snapshot_id': 'snap-1',
                    'name': 'snapshot-1',
                    'node_id': node_id,
                    'size_gb': 100,
                    'status': 'success',
                    'created_at': datetime.now(timezone.utc).isoformat(),
                }
            ]
        except Exception as e:
            logger.error(f'Failed to list snapshots: {e}')
            raise

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete storage snapshot.

        Args:
            snapshot_id: Snapshot UUID to delete

        Returns:
            True if deletion initiated
        """
        try:
            # response = self._call_rpc('StorageService', 'DeleteSnapshot', {'snapshot_id': snapshot_id})
            return True
        except Exception as e:
            logger.error(f'Failed to delete snapshot {snapshot_id}: {e}')
            raise

    # Migration Service Methods

    def plan_migration(self, source_node_id: str, target_node_id: str,
                       vm_ids: List[str]) -> Dict[str, Any]:
        """Plan VM migration between nodes.

        Args:
            source_node_id: Source node UUID
            target_node_id: Target node UUID
            vm_ids: List of VM IDs to migrate

        Returns:
            Dictionary with migration plan details
        """
        try:
            request = {
                'source_node_id': source_node_id,
                'target_node_id': target_node_id,
                'vm_ids': vm_ids,
            }

            # response = self._call_rpc('MigrationService', 'PlanMigration', request)

            return {
                'success': True,
                'migration_id': 'migration-uuid',
                'estimated_duration_minutes': 30,
                'downtime_minutes': 5,
            }
        except Exception as e:
            logger.error(f'Failed to plan migration: {e}')
            raise


# Global client instance
_client = None


def get_rpc_client() -> RPCClient:
    """Get or create global RPC client instance."""
    global _client
    if _client is None:
        _client = RPCClient()
    return _client


def close_rpc_client():
    """Close global RPC client connection."""
    global _client
    if _client:
        _client.close()
        _client = None
