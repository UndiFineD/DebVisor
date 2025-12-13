# DebVisor Supply Chain & Signing\n\nThis document describes how DebVisor workloads (images and

manifests) can be\nsigned and verified so that only trusted artifacts run in clusters.\n\n##
Concepts\n\n- **Signer keys**: one or more keypairs used to sign container images and\n\n other
artifacts, typically stored in CI/CD systems.\n\n- **Trusted signers on DebVisor**: public keys or
certificate bundles made\n\n available on DebVisor nodes, for example under\n
`/etc/debvisor/trusted-signers/`.\n\n- **Registry**: a container registry that stores DebVisor
images\n\n (e.g. `registry.example.com/debvisor/*`).\n\n- **Admission policies**: Kubernetes
policies that enforce that only signed\n\n images from approved registries are allowed.\n\n## Keys
and Trust Roots\n\n- Generate a signing keypair for DebVisor workloads (example using cosign):\n\n
cosign generate-key-pair\n\n## Produces cosign.key (private) and cosign.pub (public)\n\n- Store
the**private key**in CI/CD secrets and do not place it on DebVisor\n\n nodes.\n\n- Distribute
the**public key**to DebVisor nodes, for example:\n\n-
`/etc/debvisor/trusted-signers/debvisor-app-signer.pub`\n\n## Signing Container Images\n\n 1. Build
and push the image from CI:\n\n docker build -t registry.example.com/debvisor/app:TAG .\n docker
push registry.example.com/debvisor/app:TAG\n\n1. Sign the image with cosign in CI:\n\n
COSIGN_PASSWORD="${COSIGN_PASSWORD}" \\n cosign sign -key cosign.key \\n
registry.example.com/debvisor/app:TAG\n\n 1. Verification example (on DebVisor or in a cluster
node):\n\n cosign verify -key /etc/debvisor/trusted-signers/debvisor-app-signer.pub \\n
registry.example.com/debvisor/app:TAG\n\n## Manifests and GitOps\n\n- Store Kubernetes manifests and
Helm charts for DebVisor in a Git\n\n repository under your control.\n\n- Optionally:\n\n- Sign Git
tags or commits with GPG.\n\n- Use Sigstore/cosign to sign release artifacts.\n\n- Use GitOps tools
(such as Argo CD or Flux) so DebVisor-backed clusters\n\n only sync from that repository.\n\n##
Admission Policies Overview\n\n- Admission policies ensure that only images meeting certain criteria
are\n\n allowed to run in the cluster, for example:\n\n- Image registry must match
`registry.example.com`.\n\n- Image must be signed by a key present in\n\n
`/etc/debvisor/trusted-signers/`.\n\n- See
`docker\addons\k8s\security\require-signed-images.yaml`for an example\n\n Kyverno policy enforcing
signed images.\n\n## Recommended Directory Layout on
DebVisor\n\n-`/etc/debvisor/trusted-signers/`\n\n- `debvisor-app-signer.pub`(main public key)\n\n-
Additional partner keys as needed\n\n-`/etc/debvisor/` (existing configs)\n\n- Blocklists/whitelists
and other DebVisor-specific configuration.\n\nThis supply-chain model is intended as a baseline.
Operators can extend it\nwith additional attestations or stricter policies as needed.\n\n
