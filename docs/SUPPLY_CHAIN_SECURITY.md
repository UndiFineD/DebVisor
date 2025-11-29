# Supply Chain Security Guide

**Last Updated**: November 29, 2025

## Overview

DebVisor implements comprehensive software supply chain security following industry best practices including SLSA Build Level 3, dual-format SBOM generation, cryptographic attestations, policy enforcement, and vulnerability exploitability documentation.

---

## 🔒 Security Components

### 1. Artifact Signing (GPG)

**Implementation**: `.github/workflows/release.yml`

All release artifacts are signed with GPG using detached ASCII-armored signatures:

- Release tarball (`debvisor-{version}.tar.gz.asc`)
- CycloneDX SBOM (`sbom-{version}.xml.asc`)
- VEX documents (`debvisor-{version}.vex.json.asc`)

**Configuration**:

```bash
# Store GPG private key as repository secret
gh secret set GPG_PRIVATE_KEY < gpg_priv_key.txt
gh secret set GPG_PASSPHRASE  # Optional passphrase

# Verify signatures locally
gpg --verify debvisor-1.0.0.tar.gz.asc debvisor-1.0.0.tar.gz
```text

**Features**:

- Passphrase support via `--pinentry-mode loopback`
- Automatic public key import for verification
- Smoke test verification post-signing

---

### 2. Cryptographic Checksums

**Implementation**: `.github/workflows/release.yml` (job: `build-artifacts`)

SHA256 checksums generated for all artifacts:

```bash
# Verify checksums
sha256sum -c debvisor-1.0.0.tar.gz.sha256
sha256sum -c sbom-1.0.0.xml.sha256
sha256sum -c sbom-1.0.0.spdx.json.sha256
```text

**Job Outputs**:

- `tarball_sha256`: Tarball digest
- `sbom_sha256`: CycloneDX SBOM digest
- `spdx_sha256`: SPDX SBOM digest

**Verification Flow**:

1. Build-time hash generation
1. Upload to release artifacts
1. Smoke test re-computation and comparison
1. SBOM attestation hash consistency check

---

### 3. SBOM Generation (Dual Format)

**Implementation**: `.github/workflows/release.yml` (job: `build-artifacts`)

#### CycloneDX Format

```bash
cyclonedx-py requirements requirements.txt -o sbom-{version}.xml
```text

**Advantages**:

- Wide ecosystem support
- Rich vulnerability correlation
- Component metadata

#### SPDX Format

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "spdxVersion": "SPDX-2.3",
  "packages": [...]
}
```text

**Advantages**:

- ISO/IEC 5962:2021 standard
- License compliance tooling
- Legal review compatibility

**Minimum Quality Standards**:

- ≥10 components enforced
- Version information required
- License metadata validated (policy)

---

### 4. Cosign Attestations

**Implementation**: `.github/workflows/release.yml` (job: `sbom-attest`)

#### CycloneDX Attestation

```bash
cosign attest --predicate sbom-{version}.xml --type cyclonedx ghcr.io/undefind/debvisor:{version}
```text

#### SPDX Attestation

```bash
cosign attest --predicate sbom-{version}.spdx.json --type spdxjson ghcr.io/undefind/debvisor:{version}
```text

**Verification**:
```bash
cosign verify-attestation --type cyclonedx ghcr.io/undefind/debvisor:1.0.0
cosign verify-attestation --type spdxjson ghcr.io/undefind/debvisor:1.0.0
```text

**Features**:

- Keyless signing (Sigstore)
- OIDC identity binding
- Rekor transparency log

---

### 5. SLSA Provenance

**Implementation**: `.github/workflows/release.yml` (job: `docker-build`)

Generated via GitHub's `attest-build-provenance` action:

```yaml
- uses: actions/attest-build-provenance@v1
  with:
    subject-name: ghcr.io/${{ github.repository }}
    subject-digest: ${{ steps.push.outputs.digest }}
    push-to-registry: true
```text

**SLSA Build Level 3 Requirements**:

- ✅ Build platform generates provenance
- ✅ Build service hardened against tampering
- ✅ Provenance includes all build parameters
- ✅ Two-person reviewed build definition

**Verification**: `.github/workflows/slsa-verify.yml`
```bash
slsa-verifier verify-image ghcr.io/undefind/debvisor:1.0.0 \
  --source-uri github.com/UndiFineD/DebVisor \
  --source-tag v1.0.0
```text

---

### 6. Policy Enforcement (OPA/Conftest)

**Implementation**: `.github/workflows/sbom-policy.yml`

**Policy File**: `.github/policies/sbom.rego`

#### Rules

```rego
# Minimum component count
deny[msg] {
  count(input.components) < 10
  msg := sprintf("SBOM must contain at least 10 components, found %d", [count(input.components)])
}

# Version information required
deny[msg] {
  component := input.components[_]
  not component.version
  msg := sprintf("Component '%s' missing version information", [component.name])
}

# License metadata validation
warn[msg] {
  component := input.components[_]
  not component.licenses
  msg := sprintf("Component '%s' missing license information", [component.name])
}
```text

**Execution**:
```bash
conftest test sbom-1.0.0.xml --policy .github/policies --output json
```text

**Integration**: Called as reusable workflow after SBOM attestation.

---

### 7. VEX (Vulnerability Exploitability eXchange)

**Implementation**: `.github/workflows/vex-generate.yml`

**Format**: OpenVEX (https://openvex.dev)

#### Document Structure

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",
  "author": "DebVisor Security Team",
  "timestamp": "2025-11-29T00:00:00Z",
  "statements": [
    {
      "vulnerability": {"id": "CVE-2024-1234"},
      "products": [{"id": "cryptography", "version": "41.0.0"}],
      "status": "not_affected",
      "justification": "inline_mitigations_already_exist"
    }
  ]
}
```text

**Status Values**:

- `not_affected`: Vulnerability does not apply
- `affected`: Confirmed vulnerable
- `fixed`: Patched in this version
- `under_investigation`: Analysis pending

**Usage**:
```bash
# Download VEX alongside SBOM
gh release download v1.0.0 --pattern "*.vex.json*"

# Verify signature
gpg --verify debvisor-1.0.0.vex.json.asc debvisor-1.0.0.vex.json

# Parse with tooling
vexctl verify debvisor-1.0.0.vex.json
```text

---

### 8. Rekor Transparency Log

**Implementation**: `.github/workflows/release.yml` (job: `provenance-verify`)

**Extraction**:
```bash
cosign verify ghcr.io/undefind/debvisor:1.0.0 | grep "uuid:"
```text

**Artifacts**:

- `rekor_uuid.txt`: Transparency log entry UUID
- `rekor_entries.txt`: SHA256 digests from log
- `rekor_provenance.log`: Full verification output

**Public Verification**:
```bash
# Query Rekor by UUID
rekor-cli get --uuid <uuid-from-artifact>

# Verify inclusion proof
rekor-cli verify --artifact debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc
```text

---

### 9. Scheduled Re-verification

**Implementation**: `.github/workflows/release-reverify.yml`

**Schedule**: Daily at 02:00 UTC

**Checks**:

1. Download latest release assets
1. Verify GPG signatures (tarball, CycloneDX, SPDX)
1. Recompute and compare SHA256 checksums
1. Verify CycloneDX attestation
1. Verify SPDX attestation
1. Create issue on failure via `_notify.yml`

**Failure Scenarios**:

- Registry tampering
- Key rotation issues
- Attestation expiry
- Rekor unavailability

---

## 🔍 Verification Workflows

### Consumer Verification (End Users)

**Step 1: Download Release**
```bash
gh release download v1.0.0
```text

**Step 2: Verify GPG Signature**
```bash
# Import public key
curl -L https://github.com/UndiFineD.gpg | gpg --import

# Verify tarball
gpg --verify debvisor-1.0.0.tar.gz.asc debvisor-1.0.0.tar.gz
```text

**Step 3: Verify Checksums**
```bash
sha256sum -c debvisor-1.0.0.tar.gz.sha256
sha256sum -c sbom-1.0.0.xml.sha256
```text

**Step 4: Inspect SBOM**
```bash
# CycloneDX
cat sbom-1.0.0.xml | grep '<component'

# SPDX
jq '.packages[] | {name, version: .versionInfo}' sbom-1.0.0.spdx.json
```text

**Step 5: Review VEX**
```bash
jq '.statements[] | select(.status == "affected")' debvisor-1.0.0.vex.json
```text

---

### Auditor Verification (Compliance)

**Step 1: Verify Container Provenance**
```bash
slsa-verifier verify-image ghcr.io/undefind/debvisor:1.0.0 \
  --source-uri github.com/UndiFineD/DebVisor \
  --source-tag v1.0.0 \
  --print-provenance | jq
```text

**Step 2: Verify SBOM Attestations**
```bash
cosign verify-attestation --type cyclonedx ghcr.io/undefind/debvisor:1.0.0
cosign verify-attestation --type spdxjson ghcr.io/undefind/debvisor:1.0.0
```text

**Step 3: Policy Compliance Check**
```bash
conftest test sbom-1.0.0.xml --policy compliance-policies/
```text

**Step 4: Rekor Transparency**
```bash
# Extract UUID from artifacts
UUID=$(cat rekor_uuid.txt)

# Query public log
rekor-cli get --uuid $UUID --format json | jq '.Body.HashedRekordObj'
```text

**Step 5: Generate Audit Report**
```bash
# Download all provenance artifacts
gh run download <run-id> --name provenance-logs
gh run download <run-id> --name sbom-attestation-1.0.0

# Compile verification results
echo "Artifact Integrity: $(sha256sum -c *.sha256 && echo PASS)"
echo "GPG Signatures: $(gpg --verify *.asc && echo PASS)"
echo "Rekor Inclusion: $(rekor-cli verify --artifact *.tar.gz && echo PASS)"
```text

---

## 🛡️ Security Properties

### Supply Chain Attack Mitigation

| Attack Vector | Mitigation | Verification |
|--------------|------------|--------------|
| Compromised dependencies | SBOM + VEX | Policy enforcement |
| Build tampering | SLSA provenance | slsa-verifier |
| Artifact substitution | GPG + SHA256 | Signature verification |
| Registry compromise | Cosign attestation | Rekor transparency |
| Malicious commits | Provenance identity | OIDC workflow path |
| Vulnerability injection | VEX statements | Trivy + manual review |

### Compliance Mappings

**NIST SSDF**:

- PO.3.1: SBOM generation ✅
- PO.3.2: Provenance documentation ✅
- PO.5.1: Vulnerability tracking (VEX) ✅
- PS.3.1: Integrity verification ✅

**SLSA**:

- Build L3: GitHub-hosted runner ✅
- Provenance: Generated + verified ✅
- Hermetic: Dependency pinning ✅

**Executive Order 14028**:

- SBOM requirement: CycloneDX + SPDX ✅
- Cryptographic signing: GPG + Cosign ✅
- Vulnerability disclosure: VEX ✅

---

## 📊 Artifact Inventory

### Per Release

| Artifact | Format | Signed | Attested | Policy-Checked |
|----------|--------|--------|----------|----------------|
| `debvisor-{version}.tar.gz` | tar.gz | GPG | - | - |
| `sbom-{version}.xml` | CycloneDX | GPG | Cosign | OPA |
| `sbom-{version}.spdx.json` | SPDX | - | Cosign | OPA |
| `debvisor-{version}.vex.json` | OpenVEX | GPG | - | - |
| `ghcr.io/.../debvisor:{version}` | OCI | Cosign | SLSA | Trivy |
| `*.sha256` | Checksum | - | - | - |

### Workflow Artifacts (Retained 30-90 days)

- `provenance-logs`: Cosign verification, Rekor UUIDs
- `sbom-attestation-{version}`: Predicate digests, component counts
- `sbom-policy-results`: Conftest output
- `vex-document-{version}`: OpenVEX + signature

---

## 🔧 Maintenance

### Key Rotation

**GPG Key Expiry**:
```bash
# Generate new key
gpg --full-generate-key

# Export and update secret
gpg --export-secret-keys --armor NEWKEYID > new_key.txt
gh secret set GPG_PRIVATE_KEY < new_key.txt

# Publish public key
gpg --export --armor NEWKEYID > public.asc
# Add to https://github.com/UndiFineD.gpg
```text

**Cosign Key Rotation**: Keyless signing (no manual rotation required)

### Policy Updates

**Adding New Rules**:
```bash
# Edit .github/policies/sbom.rego
vim .github/policies/sbom.rego

# Test locally
conftest test sbom-test.xml --policy .github/policies

# Commit and push
git add .github/policies/sbom.rego
git commit -m "policy: add license allowlist check"
```text

### Monitoring

**Nightly Re-verification**:

- Check GitHub Issues for `release-integrity` label
- Review workflow run summaries
- Investigate Rekor query failures

**Manual Spot Checks**:
```bash
# Random release verification
VERSION=$(gh release list --limit 1 | awk '{print $1}')
gh release download $VERSION
gpg --verify debvisor-*.tar.gz.asc
sha256sum -c *.sha256
```text

---

## 📚 References

- [SLSA Framework](https://slsa.dev)
- [Sigstore Documentation](https://docs.sigstore.dev)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [SPDX 2.3](https://spdx.github.io/spdx-spec/v2.3/)
- [OpenVEX](https://openvex.dev)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [NIST SSDF](https://csrc.nist.gov/publications/detail/sp/800-218/final)

---

**Questions?** Open an issue with the `supply-chain-security` label.
