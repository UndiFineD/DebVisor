#!/usr/bin/env bash
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

# setup-runner-tools.sh
# Cross-platform portable tool installation for self-hosted runners
# Installs: jq, cosign, gpg (Windows only - Linux assumed to have it)

set -e

TOOLS_DIR="${TOOLS_DIR:-$(pwd)/tools}"
mkdir -p "$TOOLS_DIR"

# Detect OS
if [ -n "$RUNNER_OS" ]; then
  OS="$RUNNER_OS"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
  OS="Windows"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macOS"
else
  OS="Linux"
fi

echo "Detected OS: $OS"
echo "Tools directory: $TOOLS_DIR"

# Install jq
install_jq() {
  if command -v jq &>/dev/null; then
    echo "jq already available: $(command -v jq)"
    jq --version
    return 0
  fi

  echo "Installing jq..."
  JQ_VERSION="1.7.1"
  
  case "$OS" in
    Windows)
      curl -sSL -o "$TOOLS_DIR/jq.exe" \
        "https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-windows-amd64.exe"
      echo "jq installed to $TOOLS_DIR/jq.exe"
      ;;
    Linux)
      curl -sSL -o "$TOOLS_DIR/jq" \
        "https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-linux-amd64"
      chmod +x "$TOOLS_DIR/jq"
      echo "jq installed to $TOOLS_DIR/jq"
      ;;
    macOS)
      curl -sSL -o "$TOOLS_DIR/jq" \
        "https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-macos-amd64"
      chmod +x "$TOOLS_DIR/jq"
      echo "jq installed to $TOOLS_DIR/jq"
      ;;
  esac
}

# Install cosign
install_cosign() {
  if command -v cosign &>/dev/null; then
    echo "cosign already available: $(command -v cosign)"
    cosign version || true
    return 0
  fi

  echo "Installing cosign..."
  COSIGN_VERSION="2.2.2"
  
  case "$OS" in
    Windows)
      curl -sSL -o "$TOOLS_DIR/cosign.exe" \
        "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-windows-amd64.exe"
      echo "cosign installed to $TOOLS_DIR/cosign.exe"
      ;;
    Linux)
      curl -sSL -o "$TOOLS_DIR/cosign" \
        "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-linux-amd64"
      chmod +x "$TOOLS_DIR/cosign"
      echo "cosign installed to $TOOLS_DIR/cosign"
      ;;
    macOS)
      curl -sSL -o "$TOOLS_DIR/cosign" \
        "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-darwin-amd64"
      chmod +x "$TOOLS_DIR/cosign"
      echo "cosign installed to $TOOLS_DIR/cosign"
      ;;
  esac
}

# Check/install GPG (Windows only - Linux/macOS typically have it)
check_gpg() {
  if command -v gpg &>/dev/null; then
    echo "gpg already available: $(command -v gpg)"
    gpg --version | head -n1
    return 0
  fi

  case "$OS" in
    Windows)
      # Check common Git for Windows location
      if [ -f "/c/Program Files/Git/usr/bin/gpg.exe" ]; then
        echo "gpg found in Git for Windows: /c/Program Files/Git/usr/bin/gpg.exe"
        echo "Ensure C:\\Program Files\\Git\\usr\\bin is in PATH"
      else
        echo "WARNING: gpg not found. Install Git for Windows or Gpg4win."
        echo "Git for Windows: https://git-scm.com/download/win"
        echo "Gpg4win: https://www.gpg4win.org/download.html"
        return 1
      fi
      ;;
    *)
      echo "WARNING: gpg not found. Install via package manager:"
      echo "  Linux: apt-get install gnupg / yum install gnupg"
      echo "  macOS: brew install gnupg"
      return 1
      ;;
  esac
}

# Main execution
main() {
  install_jq
  install_cosign
  check_gpg || echo "GPG check returned warning (non-fatal)"

  # Add tools to PATH for GitHub Actions
  if [ -n "$GITHUB_PATH" ]; then
    echo "$TOOLS_DIR" >> "$GITHUB_PATH"
    echo "Added $TOOLS_DIR to GITHUB_PATH"
  fi

  echo ""
  echo "Tool setup complete. Available tools:"
  echo "  jq: $(command -v jq || echo 'not in PATH yet')"
  echo "  cosign: $(command -v cosign || echo 'not in PATH yet')"
  echo "  gpg: $(command -v gpg || echo 'not found')"
  echo ""
  echo "To use in current shell, run: export PATH=\"$TOOLS_DIR:\$PATH\""
}

main "$@"
