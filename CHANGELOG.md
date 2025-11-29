# Changelog

## [0.1.1](https://github.com/UndiFineD/DebVisor/compare/v0.1.0...v0.1.1) (2025-11-29)


### Features

* **ci-tool:** add --debug flag for token and endpoint diagnostics to actions_inspector ([f4f9015](https://github.com/UndiFineD/DebVisor/commit/f4f9015daa15165c560b54e81c52d048568ec34c))
* **ci-tool:** add requests fallback + clearer 401/403 diagnostics in actions_inspector ([45544cb](https://github.com/UndiFineD/DebVisor/commit/45544cba8bda5c9c4a39af58a8bdb37a58e017ba))
* **ci-tool:** support external GH_TOKEN file loader (github-vscode.txt) and add .gitignore entry ([6625a49](https://github.com/UndiFineD/DebVisor/commit/6625a492eda8d96930b8675e4cbb676c7bb9bdde))
* **ci:** add CodeQL and secret scanning workflows (session 11) ([e5469c9](https://github.com/UndiFineD/DebVisor/commit/e5469c9da09ddb60403a13aded624c2cb59f6384))
* **ci:** complete Session 11 - all 16 advanced CI/security items ([42071e2](https://github.com/UndiFineD/DebVisor/commit/42071e2a1974d4400d85ce5e0149fe355eef8006))
* **ci:** complete Session 11 advanced CI/security enhancements ([2a2bd34](https://github.com/UndiFineD/DebVisor/commit/2a2bd3462b0c595bc858f89f9bda760b783968ea))
* **enterprise:** implement SEC-001, PERF-004, API-001, HEALTH-001 critical fixes ([086f7ad](https://github.com/UndiFineD/DebVisor/commit/086f7ad9f26030026b9ed994331c1ddd28c644e7))
* **enterprise:** Priority improvements - Vault, RBAC, DB optimization, integration tests ([664ed30](https://github.com/UndiFineD/DebVisor/commit/664ed300e9314505aa9cb54370c540ccb2f65d1e))
* **enterprise:** Session 12 - Enterprise readiness improvements ([c66002d](https://github.com/UndiFineD/DebVisor/commit/c66002d14aa7bf2e2442e751e501e8574759b5c8))


### Bug Fixes

* **ci:** correct SBOM generation command (use cyclonedx-py instead of missing cyclonedx-bom) in security workflow ([6f3381c](https://github.com/UndiFineD/DebVisor/commit/6f3381c08403f9303da53c0320f0643afb111c10))
* **ci:** pin trivy-action to v0.28.0 (audit finding) ([7d570dd](https://github.com/UndiFineD/DebVisor/commit/7d570dd484eab68c35143e23f0b212ef2a6c8f35))
* replace invalid man page reference with URL in systemd service ([dfa0857](https://github.com/UndiFineD/DebVisor/commit/dfa08578c66defe02226a3b124f3a630de65c485))
* resolve critical shellcheck errors and add configuration ([22b1ee0](https://github.com/UndiFineD/DebVisor/commit/22b1ee0b02e20e83d047e49306788e9cd451e92b))
* resolve SC2178 eval array issue and enforce shellcheck in CI ([b6378b7](https://github.com/UndiFineD/DebVisor/commit/b6378b72c7761efff6129fa4fdbcf2c48c15705f))
* **shell:** resolve SC2178/SC2128 execute() variable, quote opts, robust IP octet parsing, correct trap quoting ([b94c48c](https://github.com/UndiFineD/DebVisor/commit/b94c48cd302288fa7921f6eb78155d288d4cf537))
* standardize GitHub Actions to stable tags and configure workspace Python venv ([0bca453](https://github.com/UndiFineD/DebVisor/commit/0bca453083f42c278cf9accbb2de80dd20917107))
* **testing:** correct escaped docstring causing flake8 E999 in mock_mode ([622596b](https://github.com/UndiFineD/DebVisor/commit/622596b10667ce3b8c2d4de2cdfb22d786722e9e))
* upgrade cryptography to 44.0.1 to resolve CVE (Dependabot alert [#6](https://github.com/UndiFineD/DebVisor/issues/6)) ([f1d7b3c](https://github.com/UndiFineD/DebVisor/commit/f1d7b3cf3edcf4aab167102f4b2ef85862e28e2f))
