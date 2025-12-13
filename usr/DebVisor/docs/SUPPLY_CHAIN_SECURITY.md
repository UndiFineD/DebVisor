# Supply Chain Security Guide\n\n- *Last Updated**: November 29, 2025\n\n##

Overview\n\nDebVisor

implements comprehensive software supply chain security following industry best
practices
including
SLSA Build Level 3, dual-format SBOM generation, cryptographic attestations,
policy
enforcement, and
vulnerability exploitability documentation.\n\n- --\n\n## [U+1F512] Security
Components\n\n### 1.
Artifact Signing (GPG)\n\n- *Implementation**:
`.github/workflows/release.yml`\n\nAll
release
artifacts are signed with GPG using detached ASCII-armored signatures:\n\n-
Release
tarball
(`debvisor-{version}.tar.gz.asc`)\n\n- CycloneDX SBOM
(`sbom-{version}.xml.asc`)\n\n- VEX
documents
(`debvisor-{version}.vex.json.asc`)\n\n- *Configuration**:\n\n```bash\n# Store
GPG private
key as
repository secret\ngh secret set GPG_PRIVATE_KEY \n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n\n "@context":
">\n]([https://openvex.dev/ns/v0.2.0",>>\]([https://openvex.dev/ns/v0.2.0",>>]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)>)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n{\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n\n "@context":
"\n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n{\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n\n "@context":
"\n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"spdxVersion": "SPDX-2.3",\n "packages": [...]\n}\n```text\n "spdxVersion":
"SPDX-2.3",\n
"packages": [...]\n}\n```text\n\n- *Advantages**:\n\n- ISO/IEC 5962:2021
standard\n\n-
License
compliance tooling\n\n- Legal review compatibility\n\n- *Minimum Quality
Standards**:\n\n-
?10
components enforced\n\n- Version information required\n\n- License metadata
validated
(policy)\n\n-
--\n### 4. Cosign Attestations\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n#### CycloneDX
Attestation\n```bash\n\n-
*Advantages**:\n\n- ISO/IEC 5962:2021 standard\n\n- License compliance
tooling\n\n- Legal
review
compatibility\n\n- *Minimum Quality Standards**:\n\n- ?10 components
enforced\n\n- Version
information required\n\n- License metadata validated (policy)\n\n- --\n\n### 4.
Cosign
Attestations
(2)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n####
CycloneDX
Attestation (2)\n\n```bash\n\n- *Advantages**:\n\n- ISO/IEC 5962:2021
standard\n\n-
License
compliance tooling\n\n- Legal review compatibility\n\n- *Minimum Quality
Standards**:\n\n-
?10
components enforced\n\n- Version information required\n\n- License metadata
validated
(policy)\n\n-
--\n\n### 4. Cosign Attestations (3)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n#### CycloneDX Attestation
(3)\n```bash\n\n-
*Advantages**:\n\n- ISO/IEC 5962:2021 standard\n\n- License compliance
tooling\n\n- Legal
review
compatibility\n\n- *Minimum Quality Standards**:\n\n- ?10 components
enforced\n\n- Version
information required\n\n- License metadata validated (policy)\n\n- --\n\n### 4.
Cosign
Attestations
(4)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n####
CycloneDX
Attestation (4)\n\n```bash\n\n- *Advantages**:\n\n- ISO/IEC 5962:2021
standard\n\n-
License
compliance tooling\n\n- Legal review compatibility\n\n- *Minimum Quality
Standards**:\n\n-
?10
components enforced\n\n- Version information required\n\n- License metadata
validated
(policy)\n\n-
--\n### 4. Cosign Attestations (5)\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n#### CycloneDX Attestation
(5)\n```bash\n\n-
*Advantages**:\n\n- ISO/IEC 5962:2021 standard\n\n- License compliance
tooling\n\n- Legal
review
compatibility\n\n- *Minimum Quality Standards**:\n\n- ?10 components
enforced\n\n- Version
information required\n\n- License metadata validated (policy)\n\n- --\n\n### 4.
Cosign
Attestations
(6)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n####
CycloneDX
Attestation (6)\n\n```bash\n\n- *Advantages**:\n\n- ISO/IEC 5962:2021
standard\n\n-
License
compliance tooling\n\n- Legal review compatibility\n\n- *Minimum Quality
Standards**:\n\n-
?10
components enforced\n\n- Version information required\n\n- License metadata
validated
(policy)\n\n-
--\n\n### 4. Cosign Attestations (7)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n#### CycloneDX Attestation
(7)\n```bash\n\n-
*Advantages**:\n\n- ISO/IEC 5962:2021 standard\n\n- License compliance
tooling\n\n- Legal
review
compatibility\n\n- *Minimum Quality Standards**:\n\n- ?10 components
enforced\n\n- Version
information required\n\n- License metadata validated (policy)\n\n- --\n\n### 4.
Cosign
Attestations
(8)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`sbom-attest`)\n\n####
CycloneDX
Attestation (8)\n\n```bash\ncosign attest --predicate sbom-{version}.xml --type
cyclonedx
ghcr.io/undefind/debvisor:{version}\n```text\n```text\ncosign attest --predicate
sbom-{version}.xml
--type cyclonedx ghcr.io/undefind/debvisor:{version}\n```text\n```text\ncosign
attest
--predicate
sbom-{version}.xml --type cyclonedx
ghcr.io/undefind/debvisor:{version}\n```text\n```text\n```text\n```text\n####
SPDX
Attestation\n```bash\n\n```bash\n#### SPDX Attestation
(2)\n```bash\n\n```bash\n#### SPDX
Attestation (3)\n```bash\n\n```bash\n\n```bash\n\n```bash\ncosign attest
--predicate
sbom-{version}.spdx.json --type spdxjson
ghcr.io/undefind/debvisor:{version}\n```text\n```text\ncosign attest --predicate
sbom-{version}.spdx.json --type spdxjson
ghcr.io/undefind/debvisor:{version}\n```text\n```text\ncosign attest --predicate
sbom-{version}.spdx.json --type spdxjson
ghcr.io/undefind/debvisor:{version}\n```text\n```text\n```text\n```text\n\n-
*Verification**:\n\n```bash\n\n- *Verification**:\n\n```bash\n\n-
*Verification**:\n\n```bash\n\n-
*Verification**:\n\n```bash\n\n- *Verification**:\n\n```bash\n\n-
*Verification**:\n\n```bash\n\n-
*Verification**:\n\n```bash\n\n- *Verification**:\n\n```bash\ncosign
verify-attestation
--type
cyclonedx ghcr.io/undefind/debvisor:1.0.0\ncosign verify-attestation --type
spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\n\ncosign verify-attestation --type
spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\ncosign verify-attestation --type
cyclonedx
ghcr.io/undefind/debvisor:1.0.0\ncosign verify-attestation --type spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\n\ncosign verify-attestation --type
spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\ncosign verify-attestation --type
cyclonedx
ghcr.io/undefind/debvisor:1.0.0\ncosign verify-attestation --type spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\n\ncosign verify-attestation --type
spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\ncosign verify-attestation --type
spdxjson
ghcr.io/undefind/debvisor:1.0.0\n```text\n```text\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n- OIDC identity binding\n\n- Rekor transparency log\n\n- --\n###

1. SLSA
Provenance\n-
*Implementation**:
`.github/workflows/release.yml`(job:`docker-build`)\nGenerated via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(2)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\n\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(3)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(4)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\n\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n### 5. SLSA
Provenance (5)\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(6)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\n\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(7)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- *Features**:\n\n- Keyless
signing
(Sigstore)\n\n-
OIDC identity binding\n\n- Rekor transparency log\n\n- --\n\n### 5. SLSA
Provenance
(8)\n\n-
*Implementation**:`.github/workflows/release.yml`(job:`docker-build`)\n\nGenerated
via
GitHub's
`attest-build-provenance`action:\n\n```yaml\n\n- uses:
actions/attest-build-provenance@v1\n with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses:
actions/attest-build-provenance@v1\n\n with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses: actions/attest-build-provenance@v1\n
with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses:
actions/attest-build-provenance@v1\n\n with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses: actions/attest-build-provenance@v1\n
with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses:
actions/attest-build-provenance@v1\n\n with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses: actions/attest-build-provenance@v1\n
with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- uses:
actions/attest-build-provenance@v1\n\n with:\n
subject-name: ghcr.io/${{ github.repository }}\n subject-digest: ${{
steps.push.outputs.digest }}\n
push-to-registry: true\n```text\n\n- *SLSA Build Level 3 Requirements**:\n\n- ?
Build
platform
generates provenance\n\n- ? Build service hardened against tampering\n\n- ?
Provenance
includes all
build parameters\n\n- ? Two-person reviewed build definition\n\n-
*Verification**:`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA Build
Level 3
Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build service
hardened
against
tampering\n\n- ? Provenance includes all build parameters\n\n- ? Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\n\n- *SLSA
Build
Level 3 Requirements**:\n\n- ? Build platform generates provenance\n\n- ? Build
service
hardened
against tampering\n\n- ? Provenance includes all build parameters\n\n- ?
Two-person
reviewed build
definition\n\n- *Verification**:
`.github/workflows/slsa-verify.yml`\n\n```bash\nslsa-verifier
verify-image ghcr.io/undefind/debvisor:1.0.0 \\n\n- -source-uri
github.com/UndiFineD/DebVisor \\n\n-
-source-tag v1.0.0\n```text\n\n- -source-uri github.com/UndiFineD/DebVisor
\\n\n-
-source-tag
v1.0.0\n```text\nslsa-verifier verify-image ghcr.io/undefind/debvisor:1.0.0
\\n\n-
-source-uri
github.com/UndiFineD/DebVisor \\n\n- -source-tag v1.0.0\n```text\n\n-
-source-uri
github.com/UndiFineD/DebVisor \\n\n- -source-tag v1.0.0\n```text\nslsa-verifier
verify-image
ghcr.io/undefind/debvisor:1.0.0 \\n\n- -source-uri github.com/UndiFineD/DebVisor
\\n\n-
-source-tag
v1.0.0\n```text\n\n- -source-uri github.com/UndiFineD/DebVisor \\n\n-
-source-tag
v1.0.0\n```text\n\n- -source-uri github.com/UndiFineD/DebVisor \\n\n-
-source-tag
v1.0.0\n```text\n\n- -source-uri github.com/UndiFineD/DebVisor \\n\n-
-source-tag
v1.0.0\n```text\n\n- --\n### 6. Policy Enforcement (OPA/Conftest)\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n####
Rules\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (2)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(2)\n\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (3)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(3)\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (4)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(4)\n\n```rego\n\n- --\n### 6. Policy Enforcement (OPA/Conftest) (5)\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n#### Rules
(5)\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (6)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(6)\n\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (7)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(7)\n```rego\n\n- --\n\n### 6. Policy Enforcement (OPA/Conftest) (8)\n\n-
*Implementation**:
`.github/workflows/sbom-policy.yml`\n\n- *Policy File**:
`.github/policies/sbom.rego`\n\n#### Rules
(8)\n\n```rego\n# Minimum component count\ndeny[msg] {\n count(input.components) \n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"@id":
"\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De](https://github.com/UndiFineD/De)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)>)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n\n "@context":
">\n]([https://openvex.dev/ns/v0.2.0",>>\]([https://openvex.dev/ns/v0.2.0",>>]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)>)\)n)
"@id":
">\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>>\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb](https://github.com/UndiFineD/Deb)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)>)>)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n{\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"@id":
"[https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De]([https://github.com/UndiFineD/D](https://github.com/UndiFineD/D)e)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n\n "@context":
"\n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"@id":
"\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De](https://github.com/UndiFineD/De)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)>)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n{\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"@id":
"[https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De]([https://github.com/UndiFineD/D](https://github.com/UndiFineD/D)e)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n\n "@context":
"\n]([https://openvex.dev/ns/v0.2.0",>\]([https://openvex.dev/ns/v0.2.0",>]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)>)\)n)
"@id":
"\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De](https://github.com/UndiFineD/De)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)>)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n "@context":
"[https://openvex.dev/ns/v0.2.0",\n]([https://openvex.dev/ns/v0.2.0",\]([https://openvex.dev/ns/v0.2.0",]([https://openvex.dev/ns/v0.2.0"]([https://openvex.dev/ns/v0.2.0]([https://openvex.dev/ns/v0.2.]([https://openvex.dev/ns/v0.2]([https://openvex.dev/ns/v0.]([https://openvex.dev/ns/v0]([https://openvex.dev/ns/v]([https://openvex.dev/ns/]([https://openvex.dev/ns]([https://openvex.dev/n]([https://openvex.dev/]([https://openvex.dev]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)/)n)s)/)v)0).)2).)0)"),)\)n)
"@id":
"[https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De]([https://github.com/UndiFineD/D](https://github.com/UndiFineD/D)e)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n "@id":
"\n]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>\]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",>]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0",]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0"]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.0]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1.]([https://github.com/UndiFineD/DebVisor/vex/debvisor-1]([https://github.com/UndiFineD/DebVisor/vex/debvisor-]([https://github.com/UndiFineD/DebVisor/vex/debvisor]([https://github.com/UndiFineD/DebVisor/vex/debviso]([https://github.com/UndiFineD/DebVisor/vex/debvis]([https://github.com/UndiFineD/DebVisor/vex/debvi]([https://github.com/UndiFineD/DebVisor/vex/debv]([https://github.com/UndiFineD/DebVisor/vex/deb]([https://github.com/UndiFineD/DebVisor/vex/de]([https://github.com/UndiFineD/DebVisor/vex/d]([https://github.com/UndiFineD/DebVisor/vex/]([https://github.com/UndiFineD/DebVisor/vex]([https://github.com/UndiFineD/DebVisor/ve]([https://github.com/UndiFineD/DebVisor/v]([https://github.com/UndiFineD/DebVisor/]([https://github.com/UndiFineD/DebVisor]([https://github.com/UndiFineD/DebViso]([https://github.com/UndiFineD/DebVis]([https://github.com/UndiFineD/DebVi]([https://github.com/UndiFineD/DebV]([https://github.com/UndiFineD/Deb]([https://github.com/UndiFineD/De](https://github.com/UndiFineD/De)b)V)i)s)o)r)/)v)e)x)/)d)e)b)v)i)s)o)r)-)1).)0).)0)"),)>)\)n)
"author": "DebVisor Security Team",\n "timestamp": "2025-11-29T00:00:00Z",\n
"statements":
[\n {\n
"vulnerability": {"id": "CVE-2024-1234"},\n "products": [{"id": "cryptography",
"version":
"41.0.0"}],\n "status": "not_affected",\n "justification":
"inline_mitigations_already_exist"\n }\n
]\n}\n```text\n\n- *Status Values**:\n\n- `not_affected`: Vulnerability does not
apply\n\n-
`affected`: Confirmed vulnerable\n\n- `fixed`: Patched in this version\n\n-
`under_investigation`:
Analysis pending\n\n- *Usage**:\n\n```bash\n\n- *Status Values**:\n\n-
`not_affected`:
Vulnerability
does not apply\n\n- `affected`: Confirmed vulnerable\n\n- `fixed`: Patched in
this
version\n\n-
`under_investigation`: Analysis pending\n\n- *Usage**:\n\n```bash\n\n- *Status
Values**:\n\n-
`not_affected`: Vulnerability does not apply\n\n- `affected`: Confirmed
vulnerable\n\n-
`fixed`:
Patched in this version\n\n- `under_investigation`: Analysis pending\n\n-
*Usage**:\n\n```bash\n\n-
*Status Values**:\n\n- `not_affected`: Vulnerability does not apply\n\n-
`affected`:
Confirmed
vulnerable\n\n- `fixed`: Patched in this version\n\n- `under_investigation`:
Analysis
pending\n\n-
*Usage**:\n\n```bash\n\n- *Status Values**:\n\n- `not_affected`: Vulnerability
does not
apply\n\n-
`affected`: Confirmed vulnerable\n\n- `fixed`: Patched in this version\n\n-
`under_investigation`:
Analysis pending\n\n- *Usage**:\n\n```bash\n\n- *Status Values**:\n\n-
`not_affected`:
Vulnerability
does not apply\n\n- `affected`: Confirmed vulnerable\n\n- `fixed`: Patched in
this
version\n\n-
`under_investigation`: Analysis pending\n\n- *Usage**:\n\n```bash\n\n- *Status
Values**:\n\n-
`not_affected`: Vulnerability does not apply\n\n- `affected`: Confirmed
vulnerable\n\n-
`fixed`:
Patched in this version\n\n- `under_investigation`: Analysis pending\n\n-
*Usage**:\n\n```bash\n\n-
*Status Values**:\n\n- `not_affected`: Vulnerability does not apply\n\n-
`affected`:
Confirmed
vulnerable\n\n- `fixed`: Patched in this version\n\n- `under_investigation`:
Analysis
pending\n\n-
*Usage**:\n\n```bash\n# Download VEX alongside SBOM\ngh release download v1.0.0
--pattern
"*.vex.json*"\n# Verify signature\ngpg --verify debvisor-1.0.0.vex.json.asc
debvisor-1.0.0.vex.json\n# Parse with tooling\nvexctl verify
debvisor-1.0.0.vex.json\n```text\ngh
release download v1.0.0 --pattern "*.vex.json*"\n\n## Verify signature\n\ngpg
--verify
debvisor-1.0.0.vex.json.asc debvisor-1.0.0.vex.json\n\n## Parse with
tooling\n\nvexctl
verify
debvisor-1.0.0.vex.json\n```text\n## Download VEX alongside SBOM\n\ngh release
download
v1.0.0
--pattern "*.vex.json*"\n\n## Verify signature (2)\n\ngpg --verify
debvisor-1.0.0.vex.json.asc
debvisor-1.0.0.vex.json\n\n## Parse with tooling (2)\n\nvexctl verify
debvisor-1.0.0.vex.json\n```text\n\ngh release download v1.0.0 --pattern
"*.vex.json*"\n\n## Verify
signature (3)\n\ngpg --verify debvisor-1.0.0.vex.json.asc
debvisor-1.0.0.vex.json\n\n##
Parse with
tooling (3)\n\nvexctl verify debvisor-1.0.0.vex.json\n```text\n## Download VEX
alongside
SBOM
(2)\ngh release download v1.0.0 --pattern "*.vex.json*"\n## Verify signature
(4)\ngpg
--verify
debvisor-1.0.0.vex.json.asc debvisor-1.0.0.vex.json\n## Parse with tooling
(4)\nvexctl
verify
debvisor-1.0.0.vex.json\n```text\n\ngh release download v1.0.0 --pattern
"*.vex.json*"\n\n## Verify
signature (5)\n\ngpg --verify debvisor-1.0.0.vex.json.asc
debvisor-1.0.0.vex.json\n\n##
Parse with
tooling (5)\n\nvexctl verify debvisor-1.0.0.vex.json\n```text\ngh release
download v1.0.0
--pattern
"*.vex.json*"\n\n## Verify signature (6)\n\ngpg --verify
debvisor-1.0.0.vex.json.asc
debvisor-1.0.0.vex.json\n\n## Parse with tooling (6)\n\nvexctl verify
debvisor-1.0.0.vex.json\n```text\n\n## Verify signature (7)\n\ngpg --verify
debvisor-1.0.0.vex.json.asc debvisor-1.0.0.vex.json\n\n## Parse with tooling
(7)\n\nvexctl
verify
debvisor-1.0.0.vex.json\n```text\n\n- --\n### 8. Rekor Transparency Log\n-
*Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (2)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (3)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (4)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n- --\n###

1. Rekor Transparency Log (5)\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (6)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (7)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\n\n-
--\n\n### 8. Rekor Transparency Log (8)\n\n- *Implementation**:
`.github/workflows/release.yml`(job:`provenance-verify`)\n\n-
*Extraction**:\n\n```bash\ncosign
verify ghcr.io/undefind/debvisor:1.0.0 | grep "uuid:"\n```text\n```text\ncosign verify
ghcr.io/undefind/debvisor:1.0.0 | grep "uuid:"\n```text\n```text\ncosign verify
ghcr.io/undefind/debvisor:1.0.0 | grep "uuid:"\n```text\n```text\n```text\n```text\n\n-
*Artifacts**:\n\n- `rekor_uuid.txt`: Transparency log entry UUID\n\n-
`rekor_entries.txt`:
SHA256
digests from log\n\n- `rekor_provenance.log`: Full verification output\n\n-
*Public
Verification**:\n\n```bash\n\n- *Artifacts**:\n\n- `rekor_uuid.txt`:
Transparency log
entry
UUID\n\n- `rekor_entries.txt`: SHA256 digests from log\n\n-
`rekor_provenance.log`: Full
verification output\n\n- *Public Verification**:\n\n```bash\n\n-
*Artifacts**:\n\n-
`rekor_uuid.txt`: Transparency log entry UUID\n\n- `rekor_entries.txt`: SHA256
digests
from log\n\n-
`rekor_provenance.log`: Full verification output\n\n- *Public
Verification**:\n\n```bash\n\n-
*Artifacts**:\n\n- `rekor_uuid.txt`: Transparency log entry UUID\n\n-
`rekor_entries.txt`:
SHA256
digests from log\n\n- `rekor_provenance.log`: Full verification output\n\n-
*Public
Verification**:\n\n```bash\n\n- *Artifacts**:\n\n- `rekor_uuid.txt`:
Transparency log
entry
UUID\n\n- `rekor_entries.txt`: SHA256 digests from log\n\n-
`rekor_provenance.log`: Full
verification output\n\n- *Public Verification**:\n\n```bash\n\n-
*Artifacts**:\n\n-
`rekor_uuid.txt`: Transparency log entry UUID\n\n- `rekor_entries.txt`: SHA256
digests
from log\n\n-
`rekor_provenance.log`: Full verification output\n\n- *Public
Verification**:\n\n```bash\n\n-
*Artifacts**:\n\n- `rekor_uuid.txt`: Transparency log entry UUID\n\n-
`rekor_entries.txt`:
SHA256
digests from log\n\n- `rekor_provenance.log`: Full verification output\n\n-
*Public
Verification**:\n\n```bash\n\n- *Artifacts**:\n\n- `rekor_uuid.txt`:
Transparency log
entry
UUID\n\n- `rekor_entries.txt`: SHA256 digests from log\n\n-
`rekor_provenance.log`: Full
verification output\n\n- *Public Verification**:\n\n```bash\n# Query Rekor by
UUID\nrekor-cli get
--uuid \n# Verify inclusion proof\nrekor-cli verify --artifact
debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc\n```text\nrekor-cli
get --uuid
\n\n## Verify inclusion proof\n\nrekor-cli verify --artifact
debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc\n```text\n## Query
Rekor by
UUID\n\nrekor-cli get --uuid \n\n## Verify inclusion proof
(2)\n\nrekor-cli
verify --artifact debvisor-1.0.0.tar.gz --signature
debvisor-1.0.0.tar.gz.asc\n```text\n\nrekor-cli
get --uuid \n\n## Verify inclusion proof (3)\n\nrekor-cli verify
--artifact
debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc\n```text\n## Query
Rekor by
UUID
(2)\nrekor-cli get --uuid \n## Verify inclusion proof (4)\nrekor-cli
verify
--artifact debvisor-1.0.0.tar.gz --signature
debvisor-1.0.0.tar.gz.asc\n```text\n\nrekor-cli get
--uuid \n\n## Verify inclusion proof (5)\n\nrekor-cli verify
--artifact
debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc\n```text\nrekor-cli
get --uuid
\n\n## Verify inclusion proof (6)\n\nrekor-cli verify --artifact
debvisor-1.0.0.tar.gz --signature debvisor-1.0.0.tar.gz.asc\n```text\n\n##
Verify
inclusion proof
(7)\n\nrekor-cli verify --artifact debvisor-1.0.0.tar.gz --signature
debvisor-1.0.0.tar.gz.asc\n```text\n\n- --\n### 9. Scheduled Re-verification\n-
*Implementation**:
`.github/workflows/release-reverify.yml`\n\n- *Schedule**: Daily at 02:00
UTC\n\n-
*Checks**:\n\n1.
Download latest release assets\n\n1. Verify GPG signatures (tarball, CycloneDX,
SPDX)\n\n1.
Recompute and compare SHA256 checksums\n\n1. Verify CycloneDX attestation\n\n1.
Verify
SPDX
attestation\n\n1. Create issue on failure via `notifications.yml`\n\n- *Failure
Scenarios**:\n\n-
Registry tampering\n\n- Key rotation issues\n\n- Attestation expiry\n\n- Rekor
unavailability\n\n-
--\n## [U+1F50D] Verification Workflows\n### Consumer Verification (End
Users)\n- *Step 1:
Download
Release**\n\n```bash\n\n- --\n\n### 9. Scheduled Re-verification (2)\n\n-
*Implementation**:
`.github/workflows/release-reverify.yml`\n\n- *Schedule**: Daily at 02:00
UTC\n\n-
*Checks**:\n\n1.
Download latest release assets\n\n1. Verify GPG signatures (tarball, CycloneDX,
SPDX)\n\n1.
Recompute and compare SHA256 checksums\n\n1. Verify CycloneDX attestation\n\n1.
Verify
SPDX
attestation\n\n1. Create issue on failure via `notifications.yml`\n\n- *Failure
Scenarios**:\n\n-
Registry tampering\n\n- Key rotation issues\n\n- Attestation expiry\n\n- Rekor
unavailability\n\n-
--\n\n## [U+1F50D] Verification Workflows (2)\n\n### Consumer Verification (End
Users)
(2)\n\n-
*Step 1: Download Release**\n\n```bash\n\n- --\n\n### 9. Scheduled
Re-verification
(3)\n\n-
*Implementation**: `.github/workflows/release-reverify.yml`\n\n- *Schedule**:
Daily at
02:00
UTC\n\n- *Checks**:\n\n1. Download latest release assets\n\n1. Verify GPG
signatures
(tarball,
CycloneDX, SPDX)\n\n1. Recompute and compare SHA256 checksums\n\n1. Verify
CycloneDX
attestation\n\n1. Verify SPDX attestation\n\n1. Create issue on failure via
`notifications.yml`\n\n-
*Failure Scenarios**:\n\n- Registry tampering\n\n- Key rotation issues\n\n-
Attestation
expiry\n\n-
Rekor unavailability\n\n- --\n\n## [U+1F50D] Verification Workflows (3)\n\n###
Consumer
Verification
(End Users) (3)\n\n- *Step 1: Download Release**\n\n```bash\n\n- --\n\n### 9.
Scheduled
Re-verification (4)\n\n- *Implementation**:
`.github/workflows/release-reverify.yml`\n\n-
*Schedule**: Daily at 02:00 UTC\n\n- *Checks**:\n\n1. Download latest release
assets\n\n1.
Verify
GPG signatures (tarball, CycloneDX, SPDX)\n\n1. Recompute and compare SHA256
checksums\n\n1. Verify
CycloneDX attestation\n\n1. Verify SPDX attestation\n\n1. Create issue on
failure via
`notifications.yml`\n\n- *Failure Scenarios**:\n\n- Registry tampering\n\n- Key
rotation
issues\n\n-
Attestation expiry\n\n- Rekor unavailability\n\n- --\n\n## [U+1F50D]
Verification
Workflows
(4)\n\n### Consumer Verification (End Users) (4)\n\n- *Step 1: Download
Release**\n\n```bash\n\n-
--\n### 9. Scheduled Re-verification (5)\n- *Implementation**:
`.github/workflows/release-reverify.yml`\n\n- *Schedule**: Daily at 02:00
UTC\n\n-
*Checks**:\n\n1.
Download latest release assets\n\n1. Verify GPG signatures (tarball, CycloneDX,
SPDX)\n\n1.
Recompute and compare SHA256 checksums\n\n1. Verify CycloneDX attestation\n\n1.
Verify
SPDX
attestation\n\n1. Create issue on failure via `notifications.yml`\n\n- *Failure
Scenarios**:\n\n-
Registry tampering\n\n- Key rotation issues\n\n- Attestation expiry\n\n- Rekor
unavailability\n\n-
--\n## [U+1F50D] Verification Workflows (5)\n### Consumer Verification (End
Users) (5)\n-
*Step 1:
Download Release**\n\n```bash\n\n- --\n\n### 9. Scheduled Re-verification
(6)\n\n-
*Implementation**: `.github/workflows/release-reverify.yml`\n\n- *Schedule**:
Daily at
02:00
UTC\n\n- *Checks**:\n\n1. Download latest release assets\n\n1. Verify GPG
signatures
(tarball,
CycloneDX, SPDX)\n\n1. Recompute and compare SHA256 checksums\n\n1. Verify
CycloneDX
attestation\n\n1. Verify SPDX attestation\n\n1. Create issue on failure via
`notifications.yml`\n\n-
*Failure Scenarios**:\n\n- Registry tampering\n\n- Key rotation issues\n\n-
Attestation
expiry\n\n-
Rekor unavailability\n\n- --\n\n## [U+1F50D] Verification Workflows (6)\n\n###
Consumer
Verification
(End Users) (6)\n\n- *Step 1: Download Release**\n\n```bash\n\n- --\n\n### 9.
Scheduled
Re-verification (7)\n\n- *Implementation**:
`.github/workflows/release-reverify.yml`\n\n-
*Schedule**: Daily at 02:00 UTC\n\n- *Checks**:\n\n1. Download latest release
assets\n\n1.
Verify
GPG signatures (tarball, CycloneDX, SPDX)\n\n1. Recompute and compare SHA256
checksums\n\n1. Verify
CycloneDX attestation\n\n1. Verify SPDX attestation\n\n1. Create issue on
failure via
`notifications.yml`\n\n- *Failure Scenarios**:\n\n- Registry tampering\n\n- Key
rotation
issues\n\n-
Attestation expiry\n\n- Rekor unavailability\n\n- --\n\n## [U+1F50D]
Verification
Workflows
(7)\n\n### Consumer Verification (End Users) (7)\n\n- *Step 1: Download
Release**\n\n```bash\n\n-
--\n\n### 9. Scheduled Re-verification (8)\n\n- *Implementation**:
`.github/workflows/release-reverify.yml`\n\n- *Schedule**: Daily at 02:00
UTC\n\n-
*Checks**:\n\n1.
Download latest release assets\n\n1. Verify GPG signatures (tarball, CycloneDX,
SPDX)\n\n1.
Recompute and compare SHA256 checksums\n\n1. Verify CycloneDX attestation\n\n1.
Verify
SPDX
attestation\n\n1. Create issue on failure via `notifications.yml`\n\n- *Failure
Scenarios**:\n\n-
Registry tampering\n\n- Key rotation issues\n\n- Attestation expiry\n\n- Rekor
unavailability\n\n-
--\n\n## [U+1F50D] Verification Workflows (8)\n\n### Consumer Verification (End
Users)
(8)\n\n-
*Step 1: Download Release**\n\n```bash\ngh release download
v1.0.0\n```text\n```text\ngh
release
download v1.0.0\n```text\n```text\ngh release download
v1.0.0\n```text\n```text\n```text\n```text\n\n- *Step 2: Verify GPG
Signature**\n\n```bash\n\n-
*Step 2: Verify GPG Signature**\n\n```bash\n\n- *Step 2: Verify GPG
Signature**\n\n```bash\n\n-
*Step 2: Verify GPG Signature**\n\n```bash\n\n- *Step 2: Verify GPG
Signature**\n\n```bash\n\n-
*Step 2: Verify GPG Signature**\n\n```bash\n\n- *Step 2: Verify GPG
Signature**\n\n```bash\n\n-
*Step 2: Verify GPG Signature**\n\n```bash\n# Import public key\ncurl -L
]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)
| gpg --import\n# Verify tarball\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\ncurl -L
]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)
| gpg --import\n\n## Verify tarball\n\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n## Import public key\n\ncurl -L
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
| gpg --import\n\n## Verify tarball (2)\n\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n\ncurl -L
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
| gpg --import\n\n## Verify tarball (3)\n\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n## Import public key (2)\ncurl -L
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
| gpg --import\n## Verify tarball (4)\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n\ncurl -L
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
| gpg --import\n\n## Verify tarball (5)\n\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\ncurl -L
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
| gpg --import\n\n## Verify tarball (6)\n\ngpg --verify debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n\n## Verify tarball (7)\n\ngpg --verify
debvisor-1.0.0.tar.gz.asc
debvisor-1.0.0.tar.gz\n```text\n\n- *Step 3: Verify Checksums**\n\n```bash\n\n-
*Step 3:
Verify
Checksums**\n\n```bash\n\n- *Step 3: Verify Checksums**\n\n```bash\n\n- *Step 3:
Verify
Checksums**\n\n```bash\n\n- *Step 3: Verify Checksums**\n\n```bash\n\n- *Step 3:
Verify
Checksums**\n\n```bash\n\n- *Step 3: Verify Checksums**\n\n```bash\n\n- *Step 3:
Verify
Checksums**\n\n```bash\nsha256sum -c debvisor-1.0.0.tar.gz.sha256\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\n\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\nsha256sum
-c
debvisor-1.0.0.tar.gz.sha256\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\n\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\nsha256sum -c
debvisor-1.0.0.tar.gz.sha256\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\n\nsha256sum -c
sbom-1.0.0.xml.sha256\n```text\nsha256sum
-c
sbom-1.0.0.xml.sha256\n```text\n```text\n\n- *Step 4: Inspect
SBOM**\n\n```bash\n\n- *Step
4:
Inspect SBOM**\n\n```bash\n\n- *Step 4: Inspect SBOM**\n\n```bash\n\n- *Step 4:
Inspect
SBOM**\n\n```bash\n\n- *Step 4: Inspect SBOM**\n\n```bash\n\n- *Step 4: Inspect
SBOM**\n\n```bash\n\n- *Step 4: Inspect SBOM**\n\n```bash\n\n- *Step 4: Inspect
SBOM**\n\n```bash\n#
CycloneDX\ncat sbom-1.0.0.xml | grep ' --name provenance-logs\ngh run download

--name sbom-attestation-1.0.0\n# Compile verification results\necho "Artifact
Integrity:
$(sha256sum
-c *.sha256 && echo PASS)"\necho "GPG Signatures: $(gpg --verify *.asc && echo
PASS)"\necho "Rekor
Inclusion: $(rekor-cli verify --artifact *.tar.gz && echo PASS)"\n```text\ngh
run download

--name provenance-logs\ngh run download  --name sbom-attestation-1.0.0\n\n##
Compile
verification results\n\necho "Artifact Integrity: $(sha256sum -c *.sha256 &&
echo
PASS)"\necho "GPG
Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor Inclusion:
$(rekor-cli verify
--artifact *.tar.gz && echo PASS)"\n```text\n## Download all provenance
artifacts\n\ngh
run download
 --name provenance-logs\ngh run download  --name
sbom-attestation-1.0.0\n\n##
Compile verification results (2)\n\necho "Artifact Integrity: $(sha256sum -c
*.sha256 &&
echo
PASS)"\necho "GPG Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor
Inclusion:
$(rekor-cli verify --artifact *.tar.gz && echo PASS)"\n```text\n\ngh run
download
--name
provenance-logs\ngh run download  --name sbom-attestation-1.0.0\n\n## Compile
verification
results (3)\n\necho "Artifact Integrity: $(sha256sum -c *.sha256 && echo
PASS)"\necho "GPG
Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor Inclusion:
$(rekor-cli verify
--artifact *.tar.gz && echo PASS)"\n```text\n## Download all provenance
artifacts (2)\ngh
run
download  --name provenance-logs\ngh run download  --name
sbom-attestation-1.0.0\n##
Compile verification results (4)\necho "Artifact Integrity: $(sha256sum -c
*.sha256 &&
echo
PASS)"\necho "GPG Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor
Inclusion:
$(rekor-cli verify --artifact *.tar.gz && echo PASS)"\n```text\n\ngh run
download
--name
provenance-logs\ngh run download  --name sbom-attestation-1.0.0\n\n## Compile
verification
results (5)\n\necho "Artifact Integrity: $(sha256sum -c *.sha256 && echo
PASS)"\necho "GPG
Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor Inclusion:
$(rekor-cli verify
--artifact *.tar.gz && echo PASS)"\n```text\ngh run download  --name
provenance-logs\ngh run
download  --name sbom-attestation-1.0.0\n\n## Compile verification results
(6)\n\necho
"Artifact Integrity: $(sha256sum -c *.sha256 && echo PASS)"\necho "GPG
Signatures: $(gpg
--verify
*.asc && echo PASS)"\necho "Rekor Inclusion: $(rekor-cli verify --artifact
*.tar.gz &&
echo
PASS)"\n```text\ngh run download  --name sbom-attestation-1.0.0\n\n## Compile
verification
results (7)\n\necho "Artifact Integrity: $(sha256sum -c *.sha256 && echo
PASS)"\necho "GPG
Signatures: $(gpg --verify *.asc && echo PASS)"\necho "Rekor Inclusion:
$(rekor-cli verify
--artifact *.tar.gz && echo PASS)"\n```text\n\n- --\n## [U+1F6E1]? Security
Properties\n### Supply
Chain Attack Mitigation\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n### Compliance Mappings\n- *NIST SSDF**:\n\n-
PO.3.1: SBOM
generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1: Vulnerability
tracking
(VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n## [U+1F4CA] Artifact Inventory\n###
Per
Release\n|
Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n### Workflow Artifacts (Retained 30-90 days)\n-`provenance-logs`:
Cosign
verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n## [U+1F527] Maintenance\n### Key Rotation\n- *GPG Key
Expiry**:\n\n```bash\n\n-
--\n\n## [U+1F6E1]? Security Properties (2)\n\n### Supply Chain Attack Mitigation (2)\n\n|
Attack
Vector | Mitigation | Verification |\n|--------------|------------|--------------|\n|
Compromised
dependencies | SBOM + VEX | Policy enforcement |\n| Build tampering | SLSA provenance |
slsa-verifier |\n| Artifact substitution | GPG + SHA256 | Signature verification |\n|
Registry
compromise | Cosign attestation | Rekor transparency |\n| Malicious commits | Provenance
identity |
OIDC workflow path |\n| Vulnerability injection | VEX statements | Trivy + manual review
|\n\n###
Compliance Mappings (2)\n\n- *NIST SSDF**:\n\n- PO.3.1: SBOM generation ?\n\n-
PO.3.2:
Provenance
documentation ?\n\n- PO.5.1: Vulnerability tracking (VEX) ?\n\n- PS.3.1:
Integrity
verification
?\n\n- *SLSA**:\n\n- Build L3: GitHub-hosted runner ?\n\n- Provenance: Generated
+
verified ?\n\n-
Hermetic: Dependency pinning ?\n\n- *Executive Order 14028**:\n\n- SBOM
requirement:
CycloneDX +
SPDX ?\n\n- Cryptographic signing: GPG + Cosign ?\n\n- Vulnerability disclosure:
VEX
?\n\n- --\n\n##
[U+1F4CA] Artifact Inventory (2)\n\n### Per Release (2)\n\n| Artifact | Format | Signed |
Attested |
Policy-Checked |\n|----------|--------|--------|----------|----------------|\n|
`debvisor-{version}.tar.gz`| tar.gz | GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX |
GPG | Cosign
| OPA |\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`|
OpenVEX | GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`| Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(2)\n\n-`provenance-logs`: Cosign verification, Rekor UUIDs\n\n-
`sbom-attestation-{version}`:
Predicate digests, component counts\n\n- `sbom-policy-results`: Conftest
output\n\n-
`vex-document-{version}`: OpenVEX + signature\n\n- --\n\n## [U+1F527]
Maintenance
(2)\n\n### Key
Rotation (2)\n\n- *GPG Key Expiry**:\n\n```bash\n\n- --\n\n## [U+1F6E1]?
Security
Properties
(3)\n\n### Supply Chain Attack Mitigation (3)\n\n| Attack Vector | Mitigation |
Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n\n### Compliance Mappings (3)\n\n- *NIST
SSDF**:\n\n- PO.3.1:
SBOM generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1:
Vulnerability
tracking (VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n\n## [U+1F4CA] Artifact Inventory
(3)\n\n### Per
Release
(3)\n\n| Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(3)\n\n-`provenance-logs`:
Cosign verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate
digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n\n## [U+1F527] Maintenance (3)\n\n### Key Rotation (3)\n\n-
*GPG Key
Expiry**:\n\n```bash\n\n- --\n\n## [U+1F6E1]? Security Properties (4)\n\n###
Supply Chain
Attack
Mitigation (4)\n\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n\n### Compliance Mappings (4)\n\n- *NIST
SSDF**:\n\n- PO.3.1:
SBOM generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1:
Vulnerability
tracking (VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n\n## [U+1F4CA] Artifact Inventory
(4)\n\n### Per
Release
(4)\n\n| Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(4)\n\n-`provenance-logs`:
Cosign verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate
digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n\n## [U+1F527] Maintenance (4)\n\n### Key Rotation (4)\n\n-
*GPG Key
Expiry**:\n\n```bash\n\n- --\n## [U+1F6E1]? Security Properties (5)\n### Supply
Chain
Attack
Mitigation (5)\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n### Compliance Mappings (5)\n- *NIST SSDF**:\n\n-
PO.3.1: SBOM
generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1: Vulnerability
tracking
(VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n## [U+1F4CA] Artifact Inventory
(5)\n### Per
Release (5)\n|
Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n### Workflow Artifacts (Retained 30-90 days)
(5)\n-`provenance-logs`: Cosign
verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n## [U+1F527] Maintenance (5)\n### Key Rotation (5)\n- *GPG
Key
Expiry**:\n\n```bash\n\n- --\n\n## [U+1F6E1]? Security Properties (6)\n\n###
Supply Chain
Attack
Mitigation (6)\n\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n\n### Compliance Mappings (6)\n\n- *NIST
SSDF**:\n\n- PO.3.1:
SBOM generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1:
Vulnerability
tracking (VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n\n## [U+1F4CA] Artifact Inventory
(6)\n\n### Per
Release
(6)\n\n| Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(6)\n\n-`provenance-logs`:
Cosign verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate
digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n\n## [U+1F527] Maintenance (6)\n\n### Key Rotation (6)\n\n-
*GPG Key
Expiry**:\n\n```bash\n\n- --\n\n## [U+1F6E1]? Security Properties (7)\n\n###
Supply Chain
Attack
Mitigation (7)\n\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n\n### Compliance Mappings (7)\n\n- *NIST
SSDF**:\n\n- PO.3.1:
SBOM generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1:
Vulnerability
tracking (VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n\n## [U+1F4CA] Artifact Inventory
(7)\n\n### Per
Release
(7)\n\n| Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(7)\n\n-`provenance-logs`:
Cosign verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate
digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n\n## [U+1F527] Maintenance (7)\n\n### Key Rotation (7)\n\n-
*GPG Key
Expiry**:\n\n```bash\n\n- --\n\n## [U+1F6E1]? Security Properties (8)\n\n###
Supply Chain
Attack
Mitigation (8)\n\n| Attack Vector | Mitigation | Verification
|\n|--------------|------------|--------------|\n| Compromised dependencies | SBOM + VEX | Policy
enforcement |\n| Build tampering | SLSA provenance | slsa-verifier |\n| Artifact
substitution | GPG

- SHA256 | Signature verification |\n| Registry compromise | Cosign attestation | Rekor
transparency
|\n| Malicious commits | Provenance identity | OIDC workflow path |\n| Vulnerability injection | VEX
statements | Trivy + manual review |\n\n### Compliance Mappings (8)\n\n- *NIST
SSDF**:\n\n- PO.3.1:
SBOM generation ?\n\n- PO.3.2: Provenance documentation ?\n\n- PO.5.1:
Vulnerability
tracking (VEX)
?\n\n- PS.3.1: Integrity verification ?\n\n- *SLSA**:\n\n- Build L3:
GitHub-hosted runner
?\n\n-
Provenance: Generated + verified ?\n\n- Hermetic: Dependency pinning ?\n\n-
*Executive
Order
14028**:\n\n- SBOM requirement: CycloneDX + SPDX ?\n\n- Cryptographic signing:
GPG +
Cosign ?\n\n-
Vulnerability disclosure: VEX ?\n\n- --\n\n## [U+1F4CA] Artifact Inventory
(8)\n\n### Per
Release
(8)\n\n| Artifact | Format | Signed | Attested | Policy-Checked
|\n|----------|--------|--------|----------|----------------|\n| `debvisor-{version}.tar.gz`| tar.gz
| GPG | - | - |\n|`sbom-{version}.xml`| CycloneDX | GPG | Cosign | OPA
|\n|`sbom-{version}.spdx.json`| SPDX | - | Cosign | OPA |\n|`debvisor-{version}.vex.json`| OpenVEX |
GPG | - | - |\n|`ghcr.io/.../debvisor:{version}`| OCI | Cosign | SLSA | Trivy
|\n|`*.sha256`|
Checksum | - | - | - |\n\n### Workflow Artifacts (Retained 30-90 days)
(8)\n\n-`provenance-logs`:
Cosign verification, Rekor UUIDs\n\n- `sbom-attestation-{version}`: Predicate
digests,
component
counts\n\n- `sbom-policy-results`: Conftest output\n\n-
`vex-document-{version}`: OpenVEX
+
signature\n\n- --\n\n## [U+1F527] Maintenance (8)\n\n### Key Rotation (8)\n\n-
*GPG Key
Expiry**:\n\n```bash\n# Generate new key\ngpg --full-generate-key\n# Export and
update
secret\ngpg
--export-secret-keys --armor NEWKEYID > new_key.txt\ngh secret set
GPG_PRIVATE_KEY public.asc\n# Add to
\n```text\ngpg]([https://github.com/UndiFineD.gpg>\n```text\ngp]([https://github.com/UndiFineD.gpg>\n```text\ng]([https://github.com/UndiFineD.gpg>\n```text\n]([https://github.com/UndiFineD.gpg>\n```text\]([https://github.com/UndiFineD.gpg>\n```text]([https://github.com/UndiFineD.gpg>\n```tex]([https://github.com/UndiFineD.gpg>\n```te]([https://github.com/UndiFineD.gpg>\n```t]([https://github.com/UndiFineD.gpg>\n```]([https://github.com/UndiFineD.gpg>\n``]([https://github.com/UndiFineD.gpg>\n`]([https://github.com/UndiFineD.gpg>\n]([https://github.com/UndiFineD.gpg>\]([https://github.com/UndiFineD.gpg>]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co](https://github.co)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)\)n)`)`)`)t)e)x)t)\)n)g)p)g)
--full-generate-key\n\n## Export and update secret\n\ngpg --export-secret-keys
--armor
NEWKEYID >
new_key.txt\ngh secret set GPG_PRIVATE_KEY  public.asc\n\n## Add to

>\n\n```text\n##]([https://github.com/UndiFineD.gpg>>\n\n```text\n#]([https://github.com/UndiFineD.gpg>>\n\n```text\n]([https://github.com/UndiFineD.gpg>>\n\n```text\]([https://github.com/UndiFineD.gpg>>\n\n```text]([https://github.com/UndiFineD.gpg>>\n\n```tex]([https://github.com/UndiFineD.gpg>>\n\n```te]([https://github.com/UndiFineD.gpg>>\n\n```t]([https://github.com/UndiFineD.gpg>>\n\n```]([https://github.com/UndiFineD.gpg>>\n\n``]([https://github.com/UndiFineD.gpg>>\n\n`]([https://github.com/UndiFineD.gpg>>\n\n]([https://github.com/UndiFineD.gpg>>\n\]([https://github.com/UndiFineD.gpg>>\n]([https://github.com/UndiFineD.gpg>>\]([https://github.com/UndiFineD.gpg>>]([https://github.com/UndiFineD.gpg>]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/](https://github.com/)U)n)d)i)F)i)n)e)D).)g)p)g)>)>)\)n)\)n)`)`)`)t)e)x)t)\)n)#)#)
Generate new key\n\ngpg --full-generate-key\n\n## Export and update secret
(2)\n\ngpg
--export-secret-keys --armor NEWKEYID > new_key.txt\ngh secret set
GPG_PRIVATE_KEY
public.asc\n\n## Add to
[https://github.com/UndiFineD.gpg\n```text\n\ngpg]([https://github.com/UndiFineD.gpg\n```text\n\ngp]([https://github.com/UndiFineD.gpg\n```text\n\ng]([https://github.com/UndiFineD.gpg\n```text\n\n]([https://github.com/UndiFineD.gpg\n```text\n\]([https://github.com/UndiFineD.gpg\n```text\n]([https://github.com/UndiFineD.gpg\n```text\]([https://github.com/UndiFineD.gpg\n```text]([https://github.com/UndiFineD.gpg\n```tex]([https://github.com/UndiFineD.gpg\n```te]([https://github.com/UndiFineD.gpg\n```t]([https://github.com/UndiFineD.gpg\n```]([https://github.com/UndiFineD.gpg\n``]([https://github.com/UndiFineD.gpg\n`]([https://github.com/UndiFineD.gpg\n]([https://github.com/UndiFineD.gpg\]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com](https://github.com)/)U)n)d)i)F)i)n)e)D).)g)p)g)\)n)`)`)`)t)e)x)t)\)n)\)n)g)p)g)
--full-generate-key\n\n## Export and update secret (3)\n\ngpg
--export-secret-keys --armor
NEWKEYID

> new_key.txt\ngh secret set GPG_PRIVATE_KEY  public.asc\n\n## Add to
]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)
(2)\n\n```text\n## Generate new key (2)\ngpg --full-generate-key\n## Export and
update
secret
(4)\ngpg --export-secret-keys --armor NEWKEYID > new_key.txt\ngh secret set
GPG_PRIVATE_KEY  public.asc\n## Add
to
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
(3)\n```text\n\ngpg --full-generate-key\n\n## Export and update secret
(5)\n\ngpg
--export-secret-keys --armor NEWKEYID > new_key.txt\ngh secret set
GPG_PRIVATE_KEY
public.asc\n\n## Add to
]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)
(4)\n\n```text\ngpg --full-generate-key\n\n## Export and update secret
(6)\n\ngpg
--export-secret-keys --armor NEWKEYID > new_key.txt\ngh secret set
GPG_PRIVATE_KEY
public.asc\n\n## Add to
[https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)
(5)\n```text\n\n## Export and update secret (7)\n\ngpg --export-secret-keys
--armor
NEWKEYID >
new_key.txt\ngh secret set GPG_PRIVATE_KEY  public.asc\n\n## Add to
]([https://github.com/UndiFineD.gpg]([https://github.com/UndiFineD.gp]([https://github.com/UndiFineD.g]([https://github.com/UndiFineD.]([https://github.com/UndiFineD]([https://github.com/UndiFine]([https://github.com/UndiFin]([https://github.com/UndiFi]([https://github.com/UndiF]([https://github.com/Undi]([https://github.com/Und]([https://github.com/Un]([https://github.com/U]([https://github.com/]([https://github.com]([https://github.co]([https://github.c]([https://github.]([https://github]([https://githu]([https://gith]([https://git]([https://gi]([https://g](https://g)i)t)h)u)b).)c)o)m)/)U)n)d)i)F)i)n)e)D).)g)p)g)>)
(6)\n\n```text\n\n- *Cosign Key Rotation**: Keyless signing (no manual rotation
required)\n###
Policy Updates\n- *Adding New Rules**:\n\n```bash\n\n- *Cosign Key Rotation**:
Keyless
signing (no
manual rotation required)\n\n### Policy Updates (2)\n\n- *Adding New
Rules**:\n\n```bash\n\n-
*Cosign Key Rotation**: Keyless signing (no manual rotation required)\n\n###
Policy
Updates (3)\n\n-
*Adding New Rules**:\n\n```bash\n\n- *Cosign Key Rotation**: Keyless signing (no
manual
rotation
required)\n\n### Policy Updates (4)\n\n- *Adding New Rules**:\n\n```bash\n\n-
*Cosign Key
Rotation**: Keyless signing (no manual rotation required)\n### Policy Updates
(5)\n-
*Adding New
Rules**:\n\n```bash\n\n- *Cosign Key Rotation**: Keyless signing (no manual
rotation
required)\n\n### Policy Updates (6)\n\n- *Adding New Rules**:\n\n```bash\n\n-
*Cosign Key
Rotation**: Keyless signing (no manual rotation required)\n\n### Policy Updates
(7)\n\n-
*Adding New
Rules**:\n\n```bash\n\n- *Cosign Key Rotation**: Keyless signing (no manual
rotation
required)\n\n### Policy Updates (8)\n\n- *Adding New Rules**:\n\n```bash\n# Edit
.github/policies/sbom.rego\nvim .github/policies/sbom.rego\n# Test
locally\nconftest test
sbom-test.xml --policy .github/policies\n# Commit and push\ngit add
.github/policies/sbom.rego\ngit
commit -m "policy: add license allowlist check"\n```text\nvim
.github/policies/sbom.rego\n\n## Test
locally\n\nconftest test sbom-test.xml --policy .github/policies\n\n## Commit
and
push\n\ngit add
.github/policies/sbom.rego\ngit commit -m "policy: add license allowlist
check"\n```text\n## Edit
.github/policies/sbom.rego\n\nvim .github/policies/sbom.rego\n\n## Test locally
(2)\n\nconftest test
sbom-test.xml --policy .github/policies\n\n## Commit and push (2)\n\ngit add
.github/policies/sbom.rego\ngit commit -m "policy: add license allowlist
check"\n```text\n\nvim
.github/policies/sbom.rego\n\n## Test locally (3)\n\nconftest test sbom-test.xml
--policy
.github/policies\n\n## Commit and push (3)\n\ngit add
.github/policies/sbom.rego\ngit
commit -m
"policy: add license allowlist check"\n```text\n## Edit
.github/policies/sbom.rego
(2)\nvim
.github/policies/sbom.rego\n## Test locally (4)\nconftest test sbom-test.xml
--policy
.github/policies\n## Commit and push (4)\ngit add
.github/policies/sbom.rego\ngit commit
-m "policy:
add license allowlist check"\n```text\n\nvim .github/policies/sbom.rego\n\n##
Test locally
(5)\n\nconftest test sbom-test.xml --policy .github/policies\n\n## Commit and
push
(5)\n\ngit add
.github/policies/sbom.rego\ngit commit -m "policy: add license allowlist
check"\n```text\nvim
.github/policies/sbom.rego\n\n## Test locally (6)\n\nconftest test sbom-test.xml
--policy
.github/policies\n\n## Commit and push (6)\n\ngit add
.github/policies/sbom.rego\ngit
commit -m
"policy: add license allowlist check"\n```text\n\n## Test locally
(7)\n\nconftest test
sbom-test.xml
--policy .github/policies\n\n## Commit and push (7)\n\ngit add
.github/policies/sbom.rego\ngit
commit -m "policy: add license allowlist check"\n```text\n### Monitoring\n-
*Nightly
Re-verification**:\n\n- Check GitHub Issues for `release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n\n- *Nightly
Re-verification**:\n\n- Check GitHub Issues for`release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n###
Monitoring (2)\n\n- *Nightly Re-verification**:\n\n- Check GitHub Issues
for`release-integrity`label\n\n- Review workflow run summaries\n\n- Investigate
Rekor
query
failures\n\n- *Manual Spot Checks**:\n\n```bash\n\n- *Nightly
Re-verification**:\n\n-
Check GitHub
Issues for`release-integrity`label\n\n- Review workflow run summaries\n\n-
Investigate
Rekor query
failures\n\n- *Manual Spot Checks**:\n\n```bash\n### Monitoring (3)\n- *Nightly
Re-verification**:\n\n- Check GitHub Issues for`release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n\n- *Nightly
Re-verification**:\n\n- Check GitHub Issues for`release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n\n- *Nightly
Re-verification**:\n\n- Check GitHub Issues for`release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n\n- *Nightly
Re-verification**:\n\n- Check GitHub Issues for`release-integrity`label\n\n-
Review
workflow run
summaries\n\n- Investigate Rekor query failures\n\n- *Manual Spot
Checks**:\n\n```bash\n#
Random
release verification\nVERSION=$(gh release list --limit 1 | awk '{print $1}')\ngh release
download
$VERSION\ngpg --verify debvisor-*.tar.gz.asc\nsha256sum -c
*.sha256\n```text\nVERSION=$(gh
release
list --limit 1 | awk '{print $1}')\ngh release download $VERSION\ngpg --verify
debvisor-*.tar.gz.asc\nsha256sum -c *.sha256\n```text\n## Random release
verification\n\nVERSION=$(gh release list --limit 1 | awk '{print $1}')\ngh release
download
$VERSION\ngpg --verify debvisor-*.tar.gz.asc\nsha256sum -c
*.sha256\n```text\n\nVERSION=$(gh release
list --limit 1 | awk '{print $1}')\ngh release download $VERSION\ngpg --verify
debvisor-*.tar.gz.asc\nsha256sum -c *.sha256\n```text\n## Random release
verification
(2)\nVERSION=$(gh release list --limit 1 | awk '{print $1}')\ngh release download
$VERSION\ngpg
--verify debvisor-*.tar.gz.asc\nsha256sum -c *.sha256\n```text\n\nVERSION=$(gh
release
list --limit
1 | awk '{print $1}')\ngh release download $VERSION\ngpg --verify
debvisor-*.tar.gz.asc\nsha256sum
-c *.sha256\n```text\nVERSION=$(gh release list --limit 1 | awk '{print $1}')\ngh release
download
$VERSION\ngpg --verify debvisor-*.tar.gz.asc\nsha256sum -c *.sha256\n```text\ngh
release
download
$VERSION\ngpg --verify debvisor-*.tar.gz.asc\nsha256sum -c
*.sha256\n```text\n\n- --\n##
[U+1F4DA]
References\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n- *Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (2)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (3)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (4)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (5)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (6)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (7)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?**Open an issue with the`supply-chain-security`label.\n\n-
--\n##
[U+1F4DA]
References (8)\n- [SLSA
Framework]([https://slsa.de]([https://slsa.d]([https://slsa.]([https://slsa]([https://sls]([https://sl]([https://s](https://s)l)s)a).)d)e)v)\n\n-
[Sigstore
Documentation]([https://docs.sigstore.de]([https://docs.sigstore.d]([https://docs.sigstore.]([https://docs.sigstore]([https://docs.sigstor]([https://docs.sigsto]([https://docs.sigst]([https://docs.sigs]([https://docs.sig]([https://docs.si]([https://docs.s]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)s)i)g)s)t)o)r)e).)d)e)v)\n\n-
[CycloneDX
Specification]([https://cyclonedx.org/specification/overview]([https://cyclonedx.org/specification/overvie]([https://cyclonedx.org/specification/overvi]([https://cyclonedx.org/specification/overv]([https://cyclonedx.org/specification/over]([https://cyclonedx.org/specification/ove]([https://cyclonedx.org/specification/ov]([https://cyclonedx.org/specification/o]([https://cyclonedx.org/specification/]([https://cyclonedx.org/specification]([https://cyclonedx.org/specificatio]([https://cyclonedx.org/specificati]([https://cyclonedx.org/specificat]([https://cyclonedx.org/specifica]([https://cyclonedx.org/specific]([https://cyclonedx.org/specifi]([https://cyclonedx.org/specif]([https://cyclonedx.org/speci]([https://cyclonedx.org/spec]([https://cyclonedx.org/spe]([https://cyclonedx.org/sp]([https://cyclonedx.org/s]([https://cyclonedx.org/]([https://cyclonedx.org]([https://cyclonedx.or]([https://cyclonedx.o]([https://cyclonedx.]([https://cyclonedx]([https://cycloned]([https://cyclone]([https://cyclon](https://cyclon)e)d)x).)o)r)g)/)s)p)e)c)i)f)i)c)a)t)i)o)n)/)o)v)e)r)v)i)e)w)/)\n\n-
[SPDX
2.3]([https://spdx.github.io/spdx-spec/v2.3]([https://spdx.github.io/spdx-spec/v2.]([https://spdx.github.io/spdx-spec/v2]([https://spdx.github.io/spdx-spec/v]([https://spdx.github.io/spdx-spec/]([https://spdx.github.io/spdx-spec]([https://spdx.github.io/spdx-spe]([https://spdx.github.io/spdx-sp]([https://spdx.github.io/spdx-s]([https://spdx.github.io/spdx-]([https://spdx.github.io/spdx]([https://spdx.github.io/spd]([https://spdx.github.io/sp]([https://spdx.github.io/s]([https://spdx.github.io/]([https://spdx.github.io]([https://spdx.github.i]([https://spdx.github.]([https://spdx.github]([https://spdx.githu]([https://spdx.gith]([https://spdx.git]([https://spdx.gi]([https://spdx.g]([https://spdx.]([https://spdx]([https://spd]([https://sp]([https://s](https://s)p)d)x).)g)i)t)h)u)b).)i)o)/)s)p)d)x)-)s)p)e)c)/)v)2).)3)/)\n\n-
[OpenVEX]([https://openvex.de]([https://openvex.d]([https://openvex.]([https://openvex]([https://openve]([https://openv]([https://open]([https://ope]([https://op]([https://o](https://o)p)e)n)v)e)x).)d)e)v)\n\n-
[Open Policy
Agent]([https://www.openpolicyagent.org]([https://www.openpolicyagent.or]([https://www.openpolicyagent.o]([https://www.openpolicyagent.]([https://www.openpolicyagent]([https://www.openpolicyagen]([https://www.openpolicyage]([https://www.openpolicyag]([https://www.openpolicya]([https://www.openpolicy]([https://www.openpolic]([https://www.openpoli]([https://www.openpol]([https://www.openpo]([https://www.openp]([https://www.open]([https://www.ope]([https://www.op]([https://www.o]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)o)p)e)n)p)o)l)i)c)y)a)g)e)n)t).)o)r)g)/)\n\n-
[NIST
SSDF]([https://csrc.nist.gov/publications/detail/sp/800-218/fina]([https://csrc.nist.gov/publications/detail/sp/800-218/fin]([https://csrc.nist.gov/publications/detail/sp/800-218/fi]([https://csrc.nist.gov/publications/detail/sp/800-218/f]([https://csrc.nist.gov/publications/detail/sp/800-218/]([https://csrc.nist.gov/publications/detail/sp/800-218]([https://csrc.nist.gov/publications/detail/sp/800-21]([https://csrc.nist.gov/publications/detail/sp/800-2]([https://csrc.nist.gov/publications/detail/sp/800-]([https://csrc.nist.gov/publications/detail/sp/800]([https://csrc.nist.gov/publications/detail/sp/80]([https://csrc.nist.gov/publications/detail/sp/8]([https://csrc.nist.gov/publications/detail/sp/]([https://csrc.nist.gov/publications/detail/sp]([https://csrc.nist.gov/publications/detail/s]([https://csrc.nist.gov/publications/detail/]([https://csrc.nist.gov/publications/detail]([https://csrc.nist.gov/publications/detai]([https://csrc.nist.gov/publications/deta]([https://csrc.nist.gov/publications/det]([https://csrc.nist.gov/publications/de]([https://csrc.nist.gov/publications/d]([https://csrc.nist.gov/publications/]([https://csrc.nist.gov/publications]([https://csrc.nist.gov/publication]([https://csrc.nist.gov/publicatio]([https://csrc.nist.gov/publicati]([https://csrc.nist.gov/publicat]([https://csrc.nist.gov/publica]([https://csrc.nist.gov/public]([https://csrc.nist.gov/publi](https://csrc.nist.gov/publi)c)a)t)i)o)n)s)/)d)e)t)a)i)l)/)s)p)/)8)0)0)-)2)1)8)/)f)i)n)a)l)\n\n-
--\n\n-*Questions?** Open an issue with the`supply-chain-security` label.\n\n
