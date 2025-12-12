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


"""
Deployment Configuration for DebVisor Phase 4

Provides deployment manifests and configuration for:
- Docker containerization
- Kubernetes orchestration
- Environment-specific configs
- Health checks and readiness probes
- Service definitions and networking
- Resource specifications
- Scaling policies

Author: DebVisor Team
Date: 2025-11-26
"""

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, Optional
import yaml


class Environment(Enum):
    """Deployment environments"""

    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "prod"


class ResourceLevel(Enum):
    """Resource allocation levels"""

    MINIMAL = "minimal"    # Development
    SMALL = "small"    # Testing
    MEDIUM = "medium"    # Staging
    LARGE = "large"    # Production


@dataclass
class ResourceRequests:
    """Kubernetes resource requests"""

    cpu_cores: str    # e.g., "100m", "500m", "1"
    memory_mb: str    # e.g., "128Mi", "512Mi", "1Gi"


@dataclass
class ResourceLimits:
    """Kubernetes resource limits"""

    cpu_cores: str
    memory_mb: str


@dataclass
class HealthCheck:
    """Health check configuration"""

    enabled: bool = True
    path: str = "/health"
    port: int = 8080
    initial_delay_seconds: int = 10
    timeout_seconds: int = 5
    period_seconds: int = 10
    success_threshold: int = 1
    failure_threshold: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ServiceConfig:
    """Service configuration"""

    name: str
    port: int
    target_port: int
    protocol: str = "TCP"
    node_port: Optional[int] = None    # For NodePort services


@dataclass
class DeploymentConfig:
    """Kubernetes Deployment configuration"""

    name: str
    image: str
    replicas: int = 1
    port: int = 8080
    environment: Environment = Environment.DEV
    resource_level: ResourceLevel = ResourceLevel.MINIMAL
    health_check: Optional[HealthCheck] = None
    service: Optional[ServiceConfig] = None
    env_vars: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.health_check is None:
            self.health_check = HealthCheck()

    def get_resources(self) -> tuple[Any, ...]:
        """Get resource requests and limits based on level"""
        if self.resource_level == ResourceLevel.MINIMAL:
            requests = ResourceRequests(cpu_cores="50m", memory_mb="64Mi")
            limits = ResourceLimits(cpu_cores="200m", memory_mb="256Mi")
        elif self.resource_level == ResourceLevel.SMALL:
            requests = ResourceRequests(cpu_cores="100m", memory_mb="128Mi")
            limits = ResourceLimits(cpu_cores="500m", memory_mb="512Mi")
        elif self.resource_level == ResourceLevel.MEDIUM:
            requests = ResourceRequests(cpu_cores="250m", memory_mb="256Mi")
            limits = ResourceLimits(cpu_cores="1000m", memory_mb="1Gi")
        else:    # LARGE
            requests = ResourceRequests(cpu_cores="500m", memory_mb="512Mi")
            limits = ResourceLimits(cpu_cores="2000m", memory_mb="2Gi")

        return requests, limits

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class DockerfileGenerator:
    """Generate Dockerfile for DebVisor services"""

    @staticmethod
    def generate_python_dockerfile(
        base_image: str = "python:3.9-slim",
        app_path: str = "/app",
        requirements_file: str = "requirements.txt",
        port: int = 8080,
    ) -> str:
        """Generate Dockerfile for Python service"""
        return """FROM {base_image}

WORKDIR {app_path}

# Install dependencies
COPY {requirements_file} .
RUN pip install --no-cache-dir -r {requirements_file}

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 debvisor && chown -R debvisor:debvisor {app_path}
USER debvisor

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:{port}/health')"

EXPOSE {port}

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
"""


class KubernetesManifestGenerator:
    """Generate Kubernetes manifests"""

    @staticmethod
    def generate_deployment(config: DeploymentConfig) -> str:
        """Generate Kubernetes Deployment manifest"""
        requests, limits = config.get_resources()

        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": config.name,
                "labels": {"app": config.name, "environment": config.environment.value},
            },
            "spec": {
                "replicas": config.replicas,
                "selector": {"matchLabels": {"app": config.name}},
                "template": {
                    "metadata": {"labels": {"app": config.name, "version": "1.0"}},
                    "spec": {
                        "containers": [
                            {
                                "name": config.name,
                                "image": config.image,
                                "imagePullPolicy": "IfNotPresent",
                                "ports": [
                                    {
                                        "name": "http",
                                        "containerPort": config.port,
                                        "protocol": "TCP",
                                    }
                                ],
                                "env": [
                                    {"name": k, "value": v}
                                    for k, v in config.env_vars.items()
                                ],
                                "resources": {
                                    "requests": {
                                        "cpu": requests.cpu_cores,
                                        "memory": requests.memory_mb,
                                    },
                                    "limits": {
                                        "cpu": limits.cpu_cores,
                                        "memory": limits.memory_mb,
                                    },
                                },
                            }
                        ]
                    },
                },
            },
        }

        # Add health check if enabled
        if config.health_check and config.health_check.enabled:
            hc = config.health_check
            deployment["spec"]["template"]["spec"]["containers"][0]["livenessProbe"] = {  # type: ignore[index]
                "httpGet": {"path": hc.path, "port": hc.port},
                "initialDelaySeconds": hc.initial_delay_seconds,
                "timeoutSeconds": hc.timeout_seconds,
                "periodSeconds": hc.period_seconds,
                "successThreshold": hc.success_threshold,
                "failureThreshold": hc.failure_threshold,
            }

            deployment["spec"]["template"]["spec"]["containers"][0][  # type: ignore[index]
                "readinessProbe"
            ] = {
                "httpGet": {"path": hc.path, "port": hc.port},
                "initialDelaySeconds": 5,
                "timeoutSeconds": hc.timeout_seconds,
                "periodSeconds": hc.period_seconds,
            }

        return yaml.dump(deployment, default_flow_style=False)

    @staticmethod
    def generate_service(config: DeploymentConfig) -> str:
        """Generate Kubernetes Service manifest"""
        if not config.service:
            return ""

        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": config.service.name, "labels": {"app": config.name}},
            "spec": {
                "type": "ClusterIP" if not config.service.node_port else "NodePort",
                "selector": {"app": config.name},
                "ports": [
                    {
                        "name": "http",
                        "protocol": config.service.protocol,
                        "port": config.service.port,
                        "targetPort": config.service.target_port,
                    }
                ],
            },
        }

        # Add NodePort if specified
        if config.service.node_port:
            service["spec"]["ports"][0]["nodePort"] = config.service.node_port  # type: ignore[index]

        return yaml.dump(service, default_flow_style=False)

    @staticmethod
    def generate_configmap(name: str, data: Dict[str, str]) -> str:
        """Generate ConfigMap manifest"""
        configmap = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": name},
            "data": data,
        }

        return yaml.dump(configmap, default_flow_style=False)

    @staticmethod
    def generate_secret(name: str, data: Dict[str, str]) -> str:
        """Generate Secret manifest"""
        secret = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {"name": name},
            "type": "Opaque",
            "stringData": data,
        }

        return yaml.dump(secret, default_flow_style=False)

    @staticmethod
    def generate_hpa(
        name: str,
        deployment_name: str,
        min_replicas: int = 2,
        max_replicas: int = 10,
        cpu_threshold: int = 80,
    ) -> str:
        """Generate HorizontalPodAutoscaler manifest"""
        hpa = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": name},
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": deployment_name,
                },
                "minReplicas": min_replicas,
                "maxReplicas": max_replicas,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": cpu_threshold,
                            },
                        },
                    }
                ],
            },
        }

        return yaml.dump(hpa, default_flow_style=False)


class EnvironmentConfig:
    """Environment-specific configuration"""

    CONFIGURATIONS = {
        Environment.DEV: {
            "replicas": 1,
            "resource_level": ResourceLevel.MINIMAL,
            "image_pull_policy": "Always",
            "log_level": "DEBUG",
        },
        Environment.TEST: {
            "replicas": 1,
            "resource_level": ResourceLevel.SMALL,
            "image_pull_policy": "IfNotPresent",
            "log_level": "INFO",
        },
        Environment.STAGING: {
            "replicas": 2,
            "resource_level": ResourceLevel.MEDIUM,
            "image_pull_policy": "IfNotPresent",
            "log_level": "INFO",
        },
        Environment.PRODUCTION: {
            "replicas": 3,
            "resource_level": ResourceLevel.LARGE,
            "image_pull_policy": "IfNotPresent",
            "log_level": "WARNING",
        },
    }

    @staticmethod
    def get_config(env: Environment) -> Dict[str, Any]:
        """Get configuration for environment"""
        return EnvironmentConfig.CONFIGURATIONS.get(
            env, EnvironmentConfig.CONFIGURATIONS[Environment.DEV]
        )


class DeploymentValidator:
    """Validate deployment configurations"""

    @staticmethod
    def validate_deployment(config: DeploymentConfig) -> tuple[Any, ...]:
        """Validate deployment configuration"""
        errors = []
        warnings = []

        # Check required fields
        if not config.name:
            errors.append("Deployment name is required")

        if not config.image:
            errors.append("Container image is required")

        # Check replicas for production
        if config.environment == Environment.PRODUCTION and config.replicas < 3:
            warnings.append(
                "Production deployment should have at least 3 replicas, "
                f"found {config.replicas}"
            )

        # Check resource limits
        requests, limits = config.get_resources()
        if requests.cpu_cores > limits.cpu_cores:
            errors.append("CPU requests cannot exceed limits")

        # Check port
        if config.port < 1024 or config.port > 65535:
            errors.append(f"Invalid port: {config.port}")

        return len(errors) == 0, errors, warnings


class DeploymentPlan:
    """Complete deployment plan"""

    def __init__(self, environment: Environment):
        self.environment = environment
        self.components = {}  # type: ignore[var-annotated]

    def add_deployment(self, config: DeploymentConfig) -> None:
        """Add deployment to plan"""
        # Validate
        valid, errors, warnings = DeploymentValidator.validate_deployment(config)
        if not valid:
            raise ValueError(f"Invalid deployment config: {errors}")

        self.components[config.name] = config

    def generate_manifests(self) -> Dict[str, str]:
        """Generate all manifests"""
        manifests = {}

        for name, config in self.components.items():
        # Generate deployment
            manifest_name = f"{name}-deployment.yaml"
            manifests[manifest_name] = KubernetesManifestGenerator.generate_deployment(
                config
            )

            # Generate service if configured
            if config.service:
                service_name = f"{name}-service.yaml"
                manifests[service_name] = KubernetesManifestGenerator.generate_service(
                    config
                )

            # Generate HPA for production
            if self.environment == Environment.PRODUCTION:
                hpa_name = f"{name}-hpa.yaml"
                manifests[hpa_name] = KubernetesManifestGenerator.generate_hpa(
                    f"{name}-hpa", config.name
                )

        return manifests

    def get_summary(self) -> Dict[str, Any]:
        """Get deployment plan summary"""
        return {
            "environment": self.environment.value,
            "components": [
                {
                    "name": name,
                    "replicas": config.replicas,
                    "image": config.image,
                    "resource_level": config.resource_level.value,
                }
                for name, config in self.components.items()
            ],
            "total_replicas": sum(c.replicas for c in self.components.values()),
        }


# Pre-configured deployment plans


def create_development_plan() -> DeploymentPlan:
    """Create development deployment plan"""
    plan = DeploymentPlan(Environment.DEV)

    # RPC Service
    plan.add_deployment(
        DeploymentConfig(
            name="debvisor-rpc",
            image="debvisor/rpc:latest",
            replicas=1,
            port=50051,
            environment=Environment.DEV,
            resource_level=ResourceLevel.MINIMAL,
            service=ServiceConfig(
                name="debvisor-rpc", port=50051, target_port=50051, protocol="TCP"
            ),
            env_vars={"LOG_LEVEL": "DEBUG", "REDIS_URL": "redis://redis:6379"},
        )
    )

    # Web Panel
    plan.add_deployment(
        DeploymentConfig(
            name="debvisor-panel",
            image="debvisor/panel:latest",
            replicas=1,
            port=8080,
            environment=Environment.DEV,
            resource_level=ResourceLevel.MINIMAL,
            service=ServiceConfig(name="debvisor-panel", port=8080, target_port=8080),
            env_vars={
                "LOG_LEVEL": "DEBUG",
                "FLASK_ENV": "development",
                "REDIS_URL": "redis://redis:6379",
            },
        )
    )

    return plan


def create_production_plan() -> DeploymentPlan:
    """Create production deployment plan"""
    plan = DeploymentPlan(Environment.PRODUCTION)

    # RPC Service (HA)
    plan.add_deployment(
        DeploymentConfig(
            name="debvisor-rpc",
            image="debvisor/rpc:v1.0",
            replicas=3,
            port=50051,
            environment=Environment.PRODUCTION,
            resource_level=ResourceLevel.LARGE,
            health_check=HealthCheck(
                enabled=True, path="/healthz", port=50051, failure_threshold=2
            ),
            service=ServiceConfig(name="debvisor-rpc", port=50051, target_port=50051),
            env_vars={
                "LOG_LEVEL": "WARNING",
                "REDIS_URL": "redis-cluster:6379",
                "POOL_SIZE": "50",
            },
        )
    )

    # Web Panel (HA)
    plan.add_deployment(
        DeploymentConfig(
            name="debvisor-panel",
            image="debvisor/panel:v1.0",
            replicas=3,
            port=8080,
            environment=Environment.PRODUCTION,
            resource_level=ResourceLevel.LARGE,
            health_check=HealthCheck(
                enabled=True, path="/health", port=8080, failure_threshold=2
            ),
            service=ServiceConfig(name="debvisor-panel", port=8080, target_port=8080),
            env_vars={
                "LOG_LEVEL": "WARNING",
                "FLASK_ENV": "production",
                "REDIS_URL": "redis-cluster:6379",
                "CACHE_SIZE": "1000",
            },
        )
    )

    return plan
