# SBOM Policy Rules for DebVisor
# Enforces minimum security and quality standards for SBOMs

package main

# Deny if SBOM has fewer than minimum components
deny[msg] {
  count(input.components) < 10
  msg := sprintf("SBOM must contain at least 10 components, found %d", [count(input.components)])
}

# Deny if any component lacks version information
deny[msg] {
  component := input.components[_]
  not component.version
  msg := sprintf("Component '%s' missing version information", [component.name])
}

# Deny if critical dependencies have known vulnerabilities (example check)
deny[msg] {
  component := input.components[_]
  component.name == "cryptography"
  not component.version
  msg := "Critical package 'cryptography' must specify version"
}

# Warn if license information is missing (non-blocking)
warn[msg] {
  component := input.components[_]
  not component.licenses
  msg := sprintf("Component '%s' missing license information", [component.name])
}

# Deny if SBOM format version is too old
deny[msg] {
  input.specVersion
  not startswith(input.specVersion, "1.")
  msg := sprintf("SBOM spec version '%s' is deprecated, use 1.x", [input.specVersion])
}

# Ensure SBOM contains serialNumber for tracking
deny[msg] {
  not input.serialNumber
  msg := "SBOM must include serialNumber for tracking"
}

# Deny if bomFormat is not CycloneDX
deny[msg] {
  not input.bomFormat == "CycloneDX"
  msg := "SBOM format must be CycloneDX"
}
