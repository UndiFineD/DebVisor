"""RPC Client Wrapper - gRPC Service Communication

Provides high-level interface to DebVisor RPC service with mTLS authentication,
error handling, and response transformation for web panel integration.
"""

import grpc
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import os

# Import generated protobuf modules (will be created during build)
# from opt.services.rpc import debvisor_pb2, debvisor_pb2_grpc

logger = logging.getLogger(__name__)


class RPCClientError(Exception):
    """Exception raised for RPC communication errors."""
    pass


class RPCClient:
    """Client for communicating with DebVisor RPC service."""
    
    def __init__(self, host: str = 'localhost', port: int = 7443,
                 cert_file: str = None, key_file: str = None,
                 ca_cert_file: str = None, timeout: int = 30):
        """Initialize RPC client with mTLS configuration.
        
        Args:
            host: RPC service hostname
            port: RPC service port
            cert_file: Path to client certificate (PEM format)
            key_file: Path to client private key (PEM format)
            ca_cert_file: Path to CA certificate for verification
            timeout: RPC call timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.channel = None
        self.stubs = {}
        
        # Load credentials
        self.cert_file = cert_file or os.getenv('RPC_CERT_FILE', '/etc/debvisor/client.crt')
        self.key_file = key_file or os.getenv('RPC_KEY_FILE', '/etc/debvisor/client.key')
        self.ca_cert_file = ca_cert_file or os.getenv('RPC_CA_CERT_FILE', '/etc/debvisor/ca.crt')
        
        self._connect()
    
    def _connect(self):
        """Establish gRPC channel with mTLS credentials."""
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
            
            # Create channel with SSL
            target = f'{self.host}:{self.port}'
            self.channel = grpc.secure_channel(target, credentials)
            
            logger.info(f'Connected to RPC service at {target}')
        
        except FileNotFoundError as e:
            raise RPCClientError(f'Certificate file not found: {e}')
        except grpc.RpcError as e:
            raise RPCClientError(f'Failed to connect to RPC service: {e}')
    
    def close(self):
        """Close gRPC channel."""
        if self.channel:
            self.channel.close()
            logger.info('RPC channel closed')
    
    def _call_rpc(self, service_name: str, method_name: str, request):
        """Execute RPC call with error handling.
        
        Args:
            service_name: Service name (NodeService, StorageService, etc.)
            method_name: Method name (RegisterNode, CreateSnapshot, etc.)
            request: Request object
            
        Returns:
            Response from RPC method
            
        Raises:
            RPCClientError: On RPC communication error
        """
        try:
            # Get stub for service
            stub = self._get_stub(service_name)
            
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
    
    def _get_stub(self, service_name: str):
        """Get or create gRPC stub for service.
        
        Args:
            service_name: Service name
            
        Returns:
            Service stub
        """
        if service_name not in self.stubs:
            # Import stub class based on service name
            # This is a placeholder - actual implementation depends on protobuf generation
            stub_class_name = f'{service_name}Stub'
            # self.stubs[service_name] = getattr(debvisor_pb2_grpc, stub_class_name)(self.channel)
            logger.debug(f'Created stub for {service_name}')
        
        return self.stubs.get(service_name)
    
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
