# DebVisor Supply Chain & Signing

This document describes how DebVisor workloads (images and manifests) can be
signed and verified so that only trusted artifacts run in clusters.

## Concepts

- **Signer keys**: one or more keypairs used to sign container images and

  other artifacts, typically stored in CI/CD systems.

- **Trusted signers on DebVisor**: public keys or certificate bundles made

  available on DebVisor nodes, for example under
  `/etc/debvisor/trusted-signers/`.

- **Registry**: a container registry that stores DebVisor images

  (e.g. `registry.example.com/debvisor/*`).

- **Admission policies**: Kubernetes policies that enforce that only signed

  images from approved registries are allowed.

## Keys and Trust Roots

- Generate a signing keypair for DebVisor workloads (example using cosign):

  cosign generate-key-pair

## Produces cosign.key (private) and cosign.pub (public)

- Store the**private key**in CI/CD secrets and do not place it on DebVisor

      nodes.

- Distribute the**public key**to DebVisor nodes, for example:

- `/etc/debvisor/trusted-signers/debvisor-app-signer.pub`

## Signing Container Images

    1. Build and push the image from CI:

       docker build -t registry.example.com/debvisor/app:TAG .
       docker push registry.example.com/debvisor/app:TAG

1. Sign the image with cosign in CI:

       COSIGN_PASSWORD="${COSIGN_PASSWORD}" \
       cosign sign -key cosign.key \
         registry.example.com/debvisor/app:TAG

    1. Verification example (on DebVisor or in a cluster node):

   cosign verify -key /etc/debvisor/trusted-signers/debvisor-app-signer.pub \
     registry.example.com/debvisor/app:TAG

## Manifests and GitOps

- Store Kubernetes manifests and Helm charts for DebVisor in a Git

  repository under your control.

- Optionally:
- Sign Git tags or commits with GPG.
- Use Sigstore/cosign to sign release artifacts.
- Use GitOps tools (such as Argo CD or Flux) so DebVisor-backed clusters

  only sync from that repository.

## Admission Policies Overview

- Admission policies ensure that only images meeting certain criteria are

  allowed to run in the cluster, for example:

- Image registry must match `registry.example.com`.
- Image must be signed by a key present in

    `/etc/debvisor/trusted-signers/`.

- See `docker\addons\k8s\security\require-signed-images.yaml` for an example

  Kyverno policy enforcing signed images.

## Recommended Directory Layout on DebVisor

- `/etc/debvisor/trusted-signers/`
- `debvisor-app-signer.pub` (main public key)
- Additional partner keys as needed
- `/etc/debvisor/` (existing configs)
- Blocklists/whitelists and other DebVisor-specific configuration.

This supply-chain model is intended as a baseline. Operators can extend it
with additional attestations or stricter policies as needed.
