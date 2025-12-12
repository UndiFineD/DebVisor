# Docker / Compose addons

This directory contains optional Docker Compose stacks that can be enabled on DebVisor nodes.
## Included stacks
- **Traefik reverse proxy**(`traefik/traefik-compose.yml`):

- Fronts HTTP/S services and can terminate TLS for containers
    running on the local Docker daemon.

- **GitLab Runner**(`gitlab-runner/gitlab-runner-compose.yml`):

- Provides CI/CD runner capacity using the Docker executor.

- **Other examples**: Additional small services intended as reference
  deployments.
## Enabling a stack
From a DebVisor node with Docker installed:
    cd docker\addons\compose
    docker compose -f traefik/traefik-compose.yml up -d
    docker compose -f gitlab-runner/gitlab-runner-compose.yml up -d
Stacks that mount `/var/run/docker.sock` grant broad control over the
Docker daemon. Treat hosts running these stacks as privileged control
nodes and restrict shell access accordingly.
## Disabling / rolling back
- Stop and remove a stack with:
  docker compose -f traefik/traefik-compose.yml down
  docker compose -f gitlab-runner/gitlab-runner-compose.yml down

- Review any named volumes or bind mounts (for example the
  `gitlab_runner_config` volume) that should be cleaned up or
  preserved.
## Interaction with DebVisor networking, DNS, and monitoring
- Exposed ports should be integrated with the existing bridge network
  and, where appropriate, registered in DNS so other nodes can reach
  them.

- For production use, consider fronting services with Kubernetes
  ingress or Traefik running on dedicated nodes, and wire logs/metrics
  into the existing monitoring stack.
