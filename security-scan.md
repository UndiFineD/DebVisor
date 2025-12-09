# Security Scan Report

**Total Alerts:** 6981

Generated via GitHub CLI.

## Security Vulnerabilities (High Priority)

| ID | Rule | Severity | File | Line | Message |
|----|------|----------|------|------|---------|
| 6950 | PinnedDependenciesID | error | `.github/workflows/fuzzing.yml` | 26 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6949 | PinnedDependenciesID | error | `.github/workflows/fuzzing.yml` | 25 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6948 | PinnedDependenciesID | error | `.github/workflows/fuzzing.yml` | 24 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6947 | PinnedDependenciesID | error | `.github/workflows/fuzzing.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzzing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6946 | PinnedDependenciesID | error | `.github/workflows/fuzzing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzzing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6945 | TokenPermissionsID | error | `.github/workflows/fuzzing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzzing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6926 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_rotation.py` | 243 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 6925 | py/url-redirection | error | `opt/web/panel/routes/auth.py` | 115 | Untrusted URL redirection depends on a user-provided value. |
| 6924 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets/vault_manager.py` | 635 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 6923 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets/vault_manager.py` | 631 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 6922 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets_management.py` | 665 | This expression logs sensitive data (secret) as clear text. |
| 6921 | BinaryArtifactsID | error | `opt/web/panel/**pycache**/analytics.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6920 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/app.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6919 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/app.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6918 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6917 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6916 | BinaryArtifactsID | error | `opt/testing/**pycache**/mock_mode.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6915 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6914 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6913 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6912 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/k8s_integration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6911 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6910 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6909 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6908 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6907 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6906 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6905 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6904 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6903 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6902 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6901 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6900 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6899 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6898 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6897 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6896 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6895 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6894 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6893 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6892 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6891 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6890 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6889 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6888 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6887 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6886 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6885 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6884 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6883 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6882 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6881 | BinaryArtifactsID | error | `opt/services/**pycache**/multi_cluster.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6880 | BinaryArtifactsID | error | `opt/services/**pycache**/diagnostics.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6879 | BinaryArtifactsID | error | `opt/netcfg-tui/**pycache**/mock_mode.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6878 | BinaryArtifactsID | error | `opt/**pycache**/webhook_system.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6877 | BinaryArtifactsID | error | `opt/**pycache**/security_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6876 | BinaryArtifactsID | error | `opt/**pycache**/plugin_architecture.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6875 | BinaryArtifactsID | error | `opt/**pycache**/performance_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6874 | BinaryArtifactsID | error | `opt/**pycache**/oidc_oauth2.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6873 | BinaryArtifactsID | error | `opt/**pycache**/netcfg_tui_full.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6872 | BinaryArtifactsID | error | `opt/**pycache**/k8sctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6871 | BinaryArtifactsID | error | `opt/**pycache**/hvctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6870 | BinaryArtifactsID | error | `opt/**pycache**/graphql_integration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6869 | BinaryArtifactsID | error | `opt/**pycache**/graphql_api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6868 | BinaryArtifactsID | error | `opt/**pycache**/e2e_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6867 | BinaryArtifactsID | error | `opt/**pycache**/distributed_tracing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6866 | BinaryArtifactsID | error | `opt/**pycache**/cephctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6865 | BinaryArtifactsID | error | `opt/**pycache**/advanced_features.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6864 | BinaryArtifactsID | error | `opt/**pycache**/advanced_documentation.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6863 | py/stack-trace-exposure | error | `opt/web/panel/routes/passthrough.py` | 144 | Stack trace information flows to this location and may be exposed to an external user. |
| 6862 | py/stack-trace-exposure | error | `opt/web/panel/routes/nodes.py` | 238 | Stack trace information flows to this location and may be exposed to an external user. |
| 6861 | py/stack-trace-exposure | error | `opt/web/panel/routes/health.py` | 144 | Stack trace information flows to this location and may be exposed to an external user. |
| 6860 | py/stack-trace-exposure | error | `opt/web/panel/routes/health.py` | 41 | Stack trace information flows to this location and may be exposed to an external user. |
| 6859 | py/url-redirection | error | `opt/web/panel/routes/auth.py` | 112 | Untrusted URL redirection depends on a user-provided value. |
| 6858 | py/url-redirection | error | `opt/web/panel/app.py` | 473 | Untrusted URL redirection depends on a user-provided value. |
| 6857 | py/clear-text-logging-sensitive-data | error | `opt/services/api_key_rotation.py` | 770 | This expression logs sensitive data (password) as clear text. |
| 6856 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/app.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6855 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6854 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6853 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6852 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6851 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6850 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6849 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6848 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6847 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6846 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6845 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6844 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6843 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6842 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6841 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6840 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6839 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6838 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6837 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6836 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6835 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6834 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6833 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6832 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6831 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6830 | BinaryArtifactsID | error | `opt/**pycache**/webhook_system.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6829 | BinaryArtifactsID | error | `opt/**pycache**/distributed_tracing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6815 | F401 | warning | `tests/test_licensing.py` | 20 | 'opt.services.licensing.licensing_server.TIER_FEATURES' imported but unused |
| 6814 | F401 | warning | `tests/test_licensing.py` | 20 | 'opt.services.licensing.licensing_server.LicenseValidationError' imported but unused |
| 6813 | F401 | warning | `tests/test_licensing.py` | 16 | 'time' imported but unused |
| 6812 | F401 | warning | `tests/test_licensing.py` | 15 | 'base64' imported but unused |
| 6811 | F401 | warning | `tests/test_licensing.py` | 14 | 'json' imported but unused |
| 6797 | F401 | warning | `tests/test_backup_manager_encryption.py` | 6 | 'unittest.mock.MagicMock' imported but unused |
| 6796 | F401 | warning | `tests/test_backup_manager_encryption.py` | 6 | 'unittest.mock.patch' imported but unused |
| 6795 | F401 | warning | `tests/test_backup_manager_encryption.py` | 5 | 'asyncio' imported but unused |
| 6780 | F401 | warning | `tests/test_audit_encryption.py` | 18 | 'opt.services.audit_encryption.EncryptionKey' imported but unused |
| 6779 | F401 | warning | `tests/test_audit_encryption.py` | 18 | 'opt.services.audit_encryption.EncryptionAlgorithm' imported but unused |
| 6778 | F401 | warning | `tests/test_audit_encryption.py` | 15 | 'datetime.timezone' imported but unused |
| 6777 | F401 | warning | `tests/test_audit_encryption.py` | 15 | 'datetime.datetime' imported but unused |
| 6776 | F401 | warning | `tests/test_audit_encryption.py` | 13 | 'base64' imported but unused |
| 6770 | F401 | warning | `tests/test_api_key_rotation.py` | 14 | 'opt.services.api_key_rotation.RotationTrigger' imported but unused |
| 6769 | F401 | warning | `tests/test_api_key_rotation.py` | 13 | 'datetime.timedelta' imported but unused |
| 6768 | F401 | warning | `opt/web/panel/routes/storage.py` | 16 | 'opt.web.panel.rbac.Role' imported but unused |
| 6767 | F401 | warning | `opt/web/panel/routes/storage.py` | 16 | 'opt.web.panel.rbac.require_role' imported but unused |
| 6766 | F401 | warning | `opt/web/panel/routes/storage.py` | 9 | 'functools.wraps' imported but unused |
| 6765 | F401 | warning | `opt/web/panel/routes/nodes.py` | 9 | 'functools.wraps' imported but unused |
| 6764 | F401 | warning | `opt/web/panel/routes/auth.py` | 9 | 'functools.wraps' imported but unused |
| 6763 | F821 | warning | `opt/web/panel/app.py` | 447 | undefined name 'CORSConfig' |
| 6762 | F821 | warning | `opt/web/panel/app.py` | 445 | undefined name 'CORSConfig' |
| 6741 | F401 | warning | `opt/services/rpc/audit.py` | 14 | 'typing.Optional' imported but unused |
| 6660 | F401 | warning | `opt/core/config.py` | 10 | 'pydantic.AnyHttpUrl' imported but unused |
| 6659 | F401 | warning | `opt/core/config.py` | 10 | 'pydantic.RedisDsn' imported but unused |
| 6658 | F401 | warning | `opt/core/config.py` | 10 | 'pydantic.PostgresDsn' imported but unused |
| 6657 | F401 | warning | `opt/core/config.py` | 9 | 'typing.Any' imported but unused |
| 6656 | F401 | warning | `opt/core/config.py` | 9 | 'typing.Dict' imported but unused |
| 6655 | F401 | warning | `opt/core/config.py` | 9 | 'typing.Union' imported but unused |
| 6645 | F401 | warning | `opt/web/panel/routes/storage.py` | 16 | 'rbac.Role' imported but unused |
| 6644 | F401 | warning | `opt/web/panel/routes/storage.py` | 16 | 'rbac.require_role' imported but unused |
| 6643 | F401 | warning | `opt/web/panel/routes/storage.py` | 9 | 'functools.wraps' imported but unused |
| 6637 | F401 | warning | `opt/web/panel/routes/nodes.py` | 9 | 'functools.wraps' imported but unused |
| 6635 | F401 | warning | `opt/web/panel/routes/auth.py` | 9 | 'functools.wraps' imported but unused |
| 6632 | F841 | warning | `opt/testing/test_phase4_week4.py` | 605 | local variable 'logins' is assigned to but never used |
| 6630 | F841 | warning | `opt/testing/test_phase4_week4.py` | 597 | local variable 'queries' is assigned to but never used |
| 6549 | F401 | warning | `opt/testing/test_phase4_week4.py` | 16 | 'unittest.mock.patch' imported but unused |
| 6497 | F401 | warning | `opt/plugin_architecture.py` | 23 | 'os' imported but unused |
| 6486 | F401 | warning | `opt/dvctl.py` | 22 | 'opt.hvctl_enhanced as hv' imported but unused |
| 6468 | F401 | warning | `opt/core/logging.py` | 13 | 'typing.Dict' imported but unused |
| 6467 | F401 | warning | `opt/core/logging.py` | 13 | 'typing.Any' imported but unused |
| 6464 | F401 | warning | `opt/core/cli_utils.py` | 7 | 'typing.Union' imported but unused |
| 6458 | BinaryArtifactsID | error | `opt/**pycache**/plugin_architecture.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 6457 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 37 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6456 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 210 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6455 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 187 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6454 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 138 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6453 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 81 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6452 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 22 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6451 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 286 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6450 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 247 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6449 | PinnedDependenciesID | error | `.github/workflows/validate-dashboards.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6448 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 40 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6447 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 34 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6446 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 237 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6445 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 190 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6444 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 117 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6443 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 93 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6442 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6441 | PinnedDependenciesID | error | `.github/workflows/test-profile-summary.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6440 | PinnedDependenciesID | error | `.github/workflows/test-grafana.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6439 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 186 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6438 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 153 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6437 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 112 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6436 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 63 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6435 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6434 | PinnedDependenciesID | error | `.github/workflows/secret-scan.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6433 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 28 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6432 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 17 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6431 | PinnedDependenciesID | error | `.github/workflows/sbom-policy.yml` | 29 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6430 | PinnedDependenciesID | error | `.github/workflows/runner-smoke-test.yml` | 33 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/runner-smoke-test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6429 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 248 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6428 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 177 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6427 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 27 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6426 | PinnedDependenciesID | error | `.github/workflows/release-reverify.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release-reverify.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6425 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 36 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6424 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6423 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6422 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 29 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6421 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6420 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 307 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6419 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 257 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6418 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 178 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6417 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 100 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6416 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 50 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6415 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 406 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6414 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 359 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6413 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 120 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6412 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 107 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6411 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 77 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6410 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6409 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6408 | PinnedDependenciesID | error | `.github/workflows/firstboot-smoke-test.yml` | 22 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6407 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6406 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 14 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6405 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 99 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6404 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 73 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6403 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6402 | PinnedDependenciesID | error | `.github/workflows/dependency-review.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/dependency-review.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6401 | PinnedDependenciesID | error | `.github/workflows/container-scan.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/container-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6400 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 32 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6399 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6398 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 19 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6397 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6396 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6395 | PinnedDependenciesID | error | `.github/workflows/build-generator.yml` | 36 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/build-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6394 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 49 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6393 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 20 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6392 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 144 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6391 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 51 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6390 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 501 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6389 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 459 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6388 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 411 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6387 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 307 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6386 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 247 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6385 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 94 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6384 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 366 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6383 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 187 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6382 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/architecture.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6381 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6380 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 489 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6379 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 410 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6378 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6377 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/_common.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6376 | TokenPermissionsID | error | `.github/workflows/validate-blocklists.yml` | 31 | score is 0: jobLevel 'checks' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6362 | F841 | warning | `opt/netcfg_tui_app.py` | 59 | local variable 'state_color' is assigned to but never used |
| 6355 | F401 | warning | `opt/distributed_tracing.py` | 21 | 'typing.Dict' imported but unused |
| 6354 | F401 | warning | `opt/distributed_tracing.py` | 19 | 'uuid' imported but unused |
| 6353 | F401 | warning | `opt/distributed_tracing.py` | 18 | 'time' imported but unused |
| 6352 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 29 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6351 | CITestsID | error | `no file associated with this alert` | 1 | score is 9: 9 out of 10 merged PRs checked by a CI test -- score normalized to 9 Click Remediation section below to solve this issue |
| 6350 | SASTID | error | `no file associated with this alert` | 1 | score is 9: SAST tool detected but not run on all commits: Warn: 16 commits out of 19 are checked with a SAST tool Click Remediation section below to solve this issue |
| 6349 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6348 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6347 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6346 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 63 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6345 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 74 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6344 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 73 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6343 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 312 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6342 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 307 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6341 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 44 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6340 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 37 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6339 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6338 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 120 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6337 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 117 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6336 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 96 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6335 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 93 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6334 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 24 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6333 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6332 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6331 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 158 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6330 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 68 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6329 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6328 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 17 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6327 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6326 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6325 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6324 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6323 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 39 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6322 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6321 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6320 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6319 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 123 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6318 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 120 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6317 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6316 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6315 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6314 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6313 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6312 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6311 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 40 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6310 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6309 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6308 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 52 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6307 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 49 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6306 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 55 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6305 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/architecture.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6304 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/architecture.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6303 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 24 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6302 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6301 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 492 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6300 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 489 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6299 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 413 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6298 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 410 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6297 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 33 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6296 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6295 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 34 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/_common.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6294 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 50 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6293 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 157 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6292 | PinnedDependenciesID | error | `.github/workflows/sbom-policy.yml` | 39 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6291 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 452 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6290 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 449 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6289 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 251 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6288 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 248 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6287 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 102 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6286 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 99 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6285 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 76 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6284 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 73 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6283 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 17 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6282 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 14 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6281 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 33 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6274 | F541 | warning | `opt/system/upgrade_manager.py` | 53 | f-string is missing placeholders |
| 6269 | F401 | warning | `opt/system/upgrade_manager.py` | 12 | 'sys' imported but unused |
| 6268 | F401 | warning | `opt/system/upgrade_manager.py` | 11 | 'shutil' imported but unused |
| 6267 | F401 | warning | `opt/system/upgrade_manager.py` | 10 | 'subprocess' imported but unused |
| 6243 | F401 | warning | `opt/dvctl.py` | 22 | 'opt.hvctl_enhanced as hv' imported but unused |
| 6242 | F401 | warning | `opt/dvctl.py` | 21 | 'opt.cephctl_enhanced as ceph' imported but unused |
| 6241 | F401 | warning | `opt/dvctl.py` | 16 | 'typing.List' imported but unused |
| 6240 | F401 | warning | `opt/dvctl.py` | 16 | 'typing.Optional' imported but unused |
| 6231 | F841 | warning | `opt/discovery/zerotouch.py` | 90 | local variable 'browser' is assigned to but never used |
| 6222 | F401 | warning | `opt/discovery/zerotouch.py` | 16 | 'zeroconf.ServiceStateChange' imported but unused |
| 6204 | F401 | warning | `opt/dvctl.py` | 21 | 'opt.hvctl_enhanced as hv' imported but unused |
| 6203 | F401 | warning | `opt/dvctl.py` | 20 | 'opt.cephctl_enhanced as ceph' imported but unused |
| 6202 | F401 | warning | `opt/dvctl.py` | 20 | 'opt.k8sctl_enhanced as k8s' imported but unused |
| 6201 | F401 | warning | `opt/dvctl.py` | 14 | 'typing.Optional' imported but unused |
| 6200 | F401 | warning | `opt/dvctl.py` | 12 | 'subprocess' imported but unused |
| 6199 | VulnerabilitiesID | error | `no file associated with this alert` | 1 | score is 0: 25 existing vulnerabilities detected: Warn: Project is vulnerable to: GHSA-79v4-65xg-pq4g Warn: Project is vulnerable to: GHSA-h4gh-qq45-vh27 Warn: Project is vulnerable to: GHSA-8qvm-5x2c-j2w7 Warn: Project is vulnerable to: GHSA-9hjg-9r4m-mvj7 Warn: Project is vulnerable to: GHSA-f9vj-2wh5-fj8j Warn: Project is vulnerable to: GHSA-hgf8-39gv-g3f2 Warn: Project is vulnerable to: GHSA-q34m-jh98-gwm2 Warn: Project is vulnerable to: PYSEC-2024-48 / GHSA-fj7x-q9j7-g6q6 Warn: Project is vulnerable to: GHSA-3ww4-gg4f-jr7f Warn: Project is vulnerable to: PYSEC-2024-225 / GHSA-6vqw-3v5j-54x4 Warn: Project is vulnerable to: GHSA-9v9h-cgj8-h64p Warn: Project is vulnerable to: PYSEC-2023-112 / GHSA-cf7p-gm2m-833m Warn: Project is vulnerable to: PYSEC-2023-254 / GHSA-jfhm-5ghh-2f97 Warn: Project is vulnerable to: GHSA-jm77-qphf-c4w8 Warn: Project is vulnerable to: GHSA-v8gr-m533-ghj9 Warn: Project is vulnerable to: GHSA-mr82-8j83-vxmv Warn: Project is vulnerable to: GHSA-9wx4-h78v-vm56 Warn: Project is vulnerable to: GHSA-4grg-w6v8-c28g Warn: Project is vulnerable to: GHSA-43qf-4rqw-9q2g Warn: Project is vulnerable to: GHSA-7rxf-gvfg-47g4 Warn: Project is vulnerable to: GHSA-84pr-m4jr-85g5 Warn: Project is vulnerable to: GHSA-8vgw-p6qm-5gr7 Warn: Project is vulnerable to: PYSEC-2024-71 / GHSA-hxwh-jpp2-84pm Warn: Project is vulnerable to: GHSA-hc5x-x2vx-497g Warn: Project is vulnerable to: GHSA-w3h3-4rj7-4ph4 Click Remediation section below to solve this issue |
| 6198 | MaintainedID | error | `no file associated with this alert` | 1 | score is 0: project was created within the last 90 days. Please review its contents carefully: Warn: Repository was created within the last 90 days. Click Remediation section below to solve this issue |
| 6197 | FuzzingID | error | `no file associated with this alert` | 1 | score is 0: project is not fuzzed: Warn: no fuzzer integrations found Click Remediation section below to solve this issue |
| 6196 | CodeReviewID | error | `no file associated with this alert` | 1 | score is 0: Found 0/12 approved changesets -- score normalized to 0 Click Remediation section below to solve this issue |
| 6195 | CIIBestPracticesID | error | `no file associated with this alert` | 1 | score is 0: no effort to earn an OpenSSF best practices badge detected Click Remediation section below to solve this issue |
| 6194 | TokenPermissionsID | error | `.github/workflows/vex-generate.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6193 | TokenPermissionsID | error | `.github/workflows/validate-syntax.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6192 | TokenPermissionsID | error | `.github/workflows/validate-kustomize.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6191 | TokenPermissionsID | error | `.github/workflows/validate-grafana.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6190 | TokenPermissionsID | error | `.github/workflows/validate-fixtures.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6189 | TokenPermissionsID | error | `.github/workflows/validate-dashboards.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6188 | TokenPermissionsID | error | `.github/workflows/validate-configs.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6187 | TokenPermissionsID | error | `.github/workflows/validate-blocklists.yml` | 264 | score is 0: jobLevel 'checks' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6186 | TokenPermissionsID | error | `.github/workflows/validate-blocklists.yml` | 31 | score is 0: jobLevel 'checks' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6185 | TokenPermissionsID | error | `.github/workflows/validate-blocklists.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6184 | TokenPermissionsID | error | `.github/workflows/test.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6183 | TokenPermissionsID | error | `.github/workflows/test-profile-summary.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6182 | TokenPermissionsID | error | `.github/workflows/test-grafana.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6181 | TokenPermissionsID | error | `.github/workflows/slsa-verify.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6180 | TokenPermissionsID | error | `.github/workflows/security.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6179 | TokenPermissionsID | error | `.github/workflows/secret-scan.yml` | 17 | score is 0: topLevel 'security-events' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6178 | TokenPermissionsID | error | `.github/workflows/sbom.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6177 | TokenPermissionsID | error | `.github/workflows/sbom-policy.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6176 | TokenPermissionsID | error | `.github/workflows/runner-smoke.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6175 | TokenPermissionsID | error | `.github/workflows/release.yml` | 14 | score is 0: topLevel 'packages' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6174 | TokenPermissionsID | error | `.github/workflows/release.yml` | 13 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6173 | TokenPermissionsID | error | `.github/workflows/release-please.yml` | 15 | score is 0: topLevel 'actions' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6172 | TokenPermissionsID | error | `.github/workflows/release-please.yml` | 13 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6171 | TokenPermissionsID | error | `.github/workflows/push-generator.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6170 | TokenPermissionsID | error | `.github/workflows/notifications.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6169 | TokenPermissionsID | error | `.github/workflows/mutation-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6168 | TokenPermissionsID | error | `.github/workflows/merge-guard.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6167 | TokenPermissionsID | error | `.github/workflows/markdownlint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6166 | TokenPermissionsID | error | `.github/workflows/markdown-lint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6165 | TokenPermissionsID | error | `.github/workflows/manifest-validation.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6164 | TokenPermissionsID | error | `.github/workflows/lint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6163 | TokenPermissionsID | error | `.github/workflows/labeler.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6162 | TokenPermissionsID | error | `.github/workflows/fuzz-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6161 | TokenPermissionsID | error | `.github/workflows/firstboot-smoke-test.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6160 | TokenPermissionsID | error | `.github/workflows/doc-integrity.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6159 | TokenPermissionsID | error | `.github/workflows/deploy.yml` | 14 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6158 | TokenPermissionsID | error | `.github/workflows/conventional-commits.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6157 | TokenPermissionsID | error | `.github/workflows/container-scan.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6156 | TokenPermissionsID | error | `.github/workflows/compliance.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6155 | TokenPermissionsID | error | `.github/workflows/codeql.yml` | 19 | score is 0: topLevel 'security-events' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6154 | TokenPermissionsID | error | `.github/workflows/chaos-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6153 | TokenPermissionsID | error | `.github/workflows/build-generator.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6152 | TokenPermissionsID | error | `.github/workflows/blocklist-validate.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6151 | TokenPermissionsID | error | `.github/workflows/blocklist-integration-tests.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6150 | TokenPermissionsID | error | `.github/workflows/architecture.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6149 | TokenPermissionsID | error | `.github/workflows/ansible-syntax-check.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6148 | TokenPermissionsID | error | `.github/workflows/ansible-inventory-validation.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6147 | TokenPermissionsID | error | `.github/workflows/_common.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 6146 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 194 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6145 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 192 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6144 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 37 | score is 0: npmCommand not pinned by hash Click Remediation section below to solve this issue |
| 6143 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 51 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6142 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 103 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6141 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 102 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6140 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 44 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6139 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 36 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6138 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 32 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6137 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 31 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6136 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 30 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6135 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 128 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6134 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 127 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6133 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 126 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6132 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 192 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6131 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 192 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6130 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 165 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6129 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 75 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6128 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 42 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6127 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 26 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6126 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 23 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6125 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 23 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6124 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 36 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6123 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 35 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6122 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 32 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6121 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 23 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6120 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 22 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6119 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 21 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6118 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 38 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6117 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 37 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6116 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 54 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6115 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 363 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6114 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 129 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6113 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 111 | score is 0: npmCommand not pinned by hash Click Remediation section below to solve this issue |
| 6112 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 29 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6111 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 28 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6110 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 27 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6109 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 22 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6108 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 21 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6107 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 33 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6106 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 32 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6105 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 23 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6104 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 22 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6103 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 48 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6102 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 47 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6101 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 22 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6100 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 21 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6099 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 64 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6098 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 63 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6097 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 313 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6096 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 312 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6095 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 24 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6094 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 24 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6093 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 22 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6092 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 39 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6091 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 38 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6090 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 37 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6089 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 500 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6088 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 499 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6087 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 421 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6086 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 420 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6085 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 41 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6084 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 40 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6083 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 41 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6082 | PinnedDependenciesID | error | `opt/monitoring/fixtures/generator/Dockerfile` | 12 | score is 0: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6081 | PinnedDependenciesID | error | `opt/monitoring/fixtures/generator/Dockerfile` | 2 | score is 0: containerImage not pinned by hash Remediation tip: pin your Docker image by updating python:3.11-slim to python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d Click Remediation section below for further remediation help |
| 6080 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 118 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6079 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 56 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6078 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 50 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6077 | PinnedDependenciesID | error | `.github/workflows/vex-generate.yml` | 37 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/vex-generate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6076 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 71 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6075 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 22 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6074 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 286 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6073 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 247 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6072 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 210 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6071 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 187 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6070 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 138 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6069 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 114 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6068 | PinnedDependenciesID | error | `.github/workflows/validate-syntax.yml` | 81 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6067 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 64 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6066 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 58 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6065 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6064 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6063 | PinnedDependenciesID | error | `.github/workflows/validate-grafana.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6062 | PinnedDependenciesID | error | `.github/workflows/validate-dashboards.yml` | 39 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6061 | PinnedDependenciesID | error | `.github/workflows/validate-dashboards.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6060 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 147 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6059 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 93 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6058 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 54 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6057 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 44 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6056 | PinnedDependenciesID | error | `.github/workflows/validate-configs.yml` | 40 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-configs.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6055 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 238 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6054 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 191 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6053 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 156 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6052 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 148 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6051 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 38 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6050 | PinnedDependenciesID | error | `.github/workflows/validate-blocklists.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6049 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 163 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6048 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 157 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6047 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 143 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6046 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 120 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6045 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 117 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6044 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 96 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6043 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 93 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6042 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 83 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6041 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 74 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6040 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 24 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6039 | PinnedDependenciesID | error | `.github/workflows/test.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6038 | PinnedDependenciesID | error | `.github/workflows/test-profile-summary.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6037 | PinnedDependenciesID | error | `.github/workflows/test-grafana.yml` | 45 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6036 | PinnedDependenciesID | error | `.github/workflows/test-grafana.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/test-grafana.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6035 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 206 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6034 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 186 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6033 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 158 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6032 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 153 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6031 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 112 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6030 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 91 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6029 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 68 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6028 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 63 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6027 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6026 | PinnedDependenciesID | error | `.github/workflows/security.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/security.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6025 | PinnedDependenciesID | error | `.github/workflows/secret-scan.yml` | 63 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6024 | PinnedDependenciesID | error | `.github/workflows/secret-scan.yml` | 38 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6023 | PinnedDependenciesID | error | `.github/workflows/secret-scan.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6022 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 63 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6021 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 55 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6020 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 33 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6019 | PinnedDependenciesID | error | `.github/workflows/scorecard.yml` | 28 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/scorecard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6018 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 32 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6017 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6016 | PinnedDependenciesID | error | `.github/workflows/sbom.yml` | 17 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6015 | PinnedDependenciesID | error | `.github/workflows/sbom-policy.yml` | 64 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6014 | PinnedDependenciesID | error | `.github/workflows/sbom-policy.yml` | 39 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6013 | PinnedDependenciesID | error | `.github/workflows/sbom-policy.yml` | 29 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6012 | PinnedDependenciesID | error | `.github/workflows/runner-smoke-test.yml` | 33 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/runner-smoke-test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6011 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 422 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6010 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 384 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6009 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 256 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6008 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 251 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6007 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 248 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6006 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 148 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6005 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 27 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6004 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 539 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6003 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 452 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6002 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 449 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6001 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 237 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 6000 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 230 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5999 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 220 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5998 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 207 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5997 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 195 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5996 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 186 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5995 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 182 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5994 | PinnedDependenciesID | error | `.github/workflows/release.yml` | 177 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5993 | PinnedDependenciesID | error | `.github/workflows/release-reverify.yml` | 35 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release-reverify.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5992 | PinnedDependenciesID | error | `.github/workflows/release-please.yml` | 25 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/release-please.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5991 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 54 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5990 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 47 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5989 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 42 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5988 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 39 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5987 | PinnedDependenciesID | error | `.github/workflows/push-generator.yml` | 36 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/push-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5986 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 82 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5985 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 61 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5984 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 49 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5983 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5982 | PinnedDependenciesID | error | `.github/workflows/performance.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/performance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5981 | PinnedDependenciesID | error | `.github/workflows/notifications.yml` | 36 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/notifications.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5980 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 38 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5979 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5978 | PinnedDependenciesID | error | `.github/workflows/mutation-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5977 | PinnedDependenciesID | error | `.github/workflows/merge-guard.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/merge-guard.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5976 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 50 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5975 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 39 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5974 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 32 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5973 | PinnedDependenciesID | error | `.github/workflows/markdownlint.yml` | 29 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdownlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5972 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 48 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5971 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5970 | PinnedDependenciesID | error | `.github/workflows/markdown-lint.yml` | 25 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5969 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 359 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5968 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 312 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5967 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 307 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5966 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 257 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5965 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 242 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5964 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 178 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5963 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 100 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5962 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 50 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5961 | PinnedDependenciesID | error | `.github/workflows/manifest-validation.yml` | 406 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5960 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 67 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5959 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 59 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5958 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5957 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5956 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 123 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5955 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 120 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5954 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 107 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5953 | PinnedDependenciesID | error | `.github/workflows/lint.yml` | 77 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/lint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5952 | PinnedDependenciesID | error | `.github/workflows/labeler.yml` | 44 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/labeler.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5951 | PinnedDependenciesID | error | `.github/workflows/labeler.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/labeler.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5950 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5949 | PinnedDependenciesID | error | `.github/workflows/fuzz-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5948 | PinnedDependenciesID | error | `.github/workflows/firstboot-smoke-test.yml` | 28 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5947 | PinnedDependenciesID | error | `.github/workflows/firstboot-smoke-test.yml` | 22 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5946 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 29 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5945 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5944 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 17 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5943 | PinnedDependenciesID | error | `.github/workflows/doc-integrity.yml` | 14 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5942 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 107 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5941 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 102 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5940 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 99 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5939 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 76 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5938 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 73 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5937 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 62 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5936 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 26 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5935 | PinnedDependenciesID | error | `.github/workflows/deploy.yml` | 23 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/deploy.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5934 | PinnedDependenciesID | error | `.github/workflows/dependency-review.yml` | 20 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/dependency-review.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5933 | PinnedDependenciesID | error | `.github/workflows/dependency-review.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/dependency-review.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5932 | PinnedDependenciesID | error | `.github/workflows/conventional-commits.yml` | 15 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/conventional-commits.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5931 | PinnedDependenciesID | error | `.github/workflows/container-scan.yml` | 27 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/container-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5930 | PinnedDependenciesID | error | `.github/workflows/container-scan.yml` | 18 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/container-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5929 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 32 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5928 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5927 | PinnedDependenciesID | error | `.github/workflows/compliance.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/compliance.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5926 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 29 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5925 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5924 | PinnedDependenciesID | error | `.github/workflows/commitlint.yml` | 19 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/commitlint.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5923 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 54 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5922 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 51 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5921 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 40 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5920 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 34 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5919 | PinnedDependenciesID | error | `.github/workflows/codeql.yml` | 31 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/codeql.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5918 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 15 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5917 | PinnedDependenciesID | error | `.github/workflows/chaos-testing.yml` | 12 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5916 | PinnedDependenciesID | error | `.github/workflows/build-generator.yml` | 47 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/build-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5915 | PinnedDependenciesID | error | `.github/workflows/build-generator.yml` | 42 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/build-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5914 | PinnedDependenciesID | error | `.github/workflows/build-generator.yml` | 39 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/build-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5913 | PinnedDependenciesID | error | `.github/workflows/build-generator.yml` | 36 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/build-generator.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5912 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 65 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5911 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 52 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5910 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 49 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5909 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 38 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5908 | PinnedDependenciesID | error | `.github/workflows/blocklist-validate.yml` | 20 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5907 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 366 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5906 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 144 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5905 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 73 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5904 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 55 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5903 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 51 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5902 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 459 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5901 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 411 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5900 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 307 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5899 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 247 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5898 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 187 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5897 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 94 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5896 | PinnedDependenciesID | error | `.github/workflows/blocklist-integration-tests.yml` | 501 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5895 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 16 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/architecture.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5894 | PinnedDependenciesID | error | `.github/workflows/architecture.yml` | 13 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/architecture.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5893 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 28 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5892 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 24 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5891 | PinnedDependenciesID | error | `.github/workflows/ansible-syntax-check.yml` | 21 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5890 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 492 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5889 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 489 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5888 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 413 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5887 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 410 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5886 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 33 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5885 | PinnedDependenciesID | error | `.github/workflows/ansible-inventory-validation.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5884 | PinnedDependenciesID | error | `.github/workflows/actions-diagnostics.yml` | 103 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/actions-diagnostics.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5883 | PinnedDependenciesID | error | `.github/workflows/actions-diagnostics.yml` | 27 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/actions-diagnostics.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5882 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 44 | score is 0: third-party GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/_common.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5881 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 34 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/_common.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5880 | PinnedDependenciesID | error | `.github/workflows/_common.yml` | 30 | score is 0: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/_common.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 5879 | LicenseID | error | `license.md` | 1 | score is 9: Any licence detected not an FSF or OSI recognized license Click Remediation section below to solve this issue |
| 5878 | BinaryArtifactsID | error | `tests/benchmarks/**pycache**/test_performance.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5877 | BinaryArtifactsID | error | `tests/**pycache**/test_webhook_system.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5876 | BinaryArtifactsID | error | `tests/**pycache**/test_security_testing.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5875 | BinaryArtifactsID | error | `tests/**pycache**/test_scheduler.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5874 | BinaryArtifactsID | error | `tests/**pycache**/test_rpc_security.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5873 | BinaryArtifactsID | error | `tests/**pycache**/test_plugin_architecture.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5872 | BinaryArtifactsID | error | `tests/**pycache**/test_phase6_vnc.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5871 | BinaryArtifactsID | error | `tests/**pycache**/test_phase6_vm.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5870 | BinaryArtifactsID | error | `tests/**pycache**/test_phase6_dns.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5869 | BinaryArtifactsID | error | `tests/**pycache**/test_phase6_cloudinit.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5868 | BinaryArtifactsID | error | `tests/**pycache**/test_performance_testing.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5867 | BinaryArtifactsID | error | `tests/**pycache**/test_oidc_oauth2.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5866 | BinaryArtifactsID | error | `tests/**pycache**/test_network_backends.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5865 | BinaryArtifactsID | error | `tests/**pycache**/test_netcfg_tui_full.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5864 | BinaryArtifactsID | error | `tests/**pycache**/test_netcfg_mock.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5863 | BinaryArtifactsID | error | `tests/**pycache**/test_multiregion.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5862 | BinaryArtifactsID | error | `tests/**pycache**/test_multiregion.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5861 | BinaryArtifactsID | error | `tests/**pycache**/test_multi_cluster.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5860 | BinaryArtifactsID | error | `tests/**pycache**/test_monitoring.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5859 | BinaryArtifactsID | error | `tests/**pycache**/test_mock_mode.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5858 | BinaryArtifactsID | error | `tests/**pycache**/test_live_migration.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5857 | BinaryArtifactsID | error | `tests/**pycache**/test_graphql_api.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5856 | BinaryArtifactsID | error | `tests/**pycache**/test_e2e_testing.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5855 | BinaryArtifactsID | error | `tests/**pycache**/test_distributed_tracing.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5854 | BinaryArtifactsID | error | `tests/**pycache**/test_diagnostics.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5853 | BinaryArtifactsID | error | `tests/**pycache**/test_dashboard.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5852 | BinaryArtifactsID | error | `tests/**pycache**/test_dashboard.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5851 | BinaryArtifactsID | error | `tests/**pycache**/test_cost_optimization.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5850 | BinaryArtifactsID | error | `tests/**pycache**/test_cost_optimization.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5849 | BinaryArtifactsID | error | `tests/**pycache**/test_compliance.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5848 | BinaryArtifactsID | error | `tests/**pycache**/test_compliance.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5847 | BinaryArtifactsID | error | `tests/**pycache**/test_cli_wrappers.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5846 | BinaryArtifactsID | error | `tests/**pycache**/test_anomaly.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5845 | BinaryArtifactsID | error | `tests/**pycache**/test_anomaly.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5844 | BinaryArtifactsID | error | `tests/**pycache**/test_analytics.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5843 | BinaryArtifactsID | error | `tests/**pycache**/test_advanced_features.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5842 | BinaryArtifactsID | error | `tests/**pycache**/test_advanced_documentation.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5841 | BinaryArtifactsID | error | `tests/**pycache**/conftest.cpython-314-pytest-8.4.2.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5840 | BinaryArtifactsID | error | `tests/**pycache**/conftest.cpython-311-pytest-9.0.1.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5839 | BinaryArtifactsID | error | `opt/web/panel/**pycache**/analytics.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5838 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/app.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5837 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/app.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5836 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5835 | BinaryArtifactsID | error | `opt/web/dashboard/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5834 | BinaryArtifactsID | error | `opt/testing/**pycache**/mock_mode.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5833 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5832 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5831 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5830 | BinaryArtifactsID | error | `opt/services/scheduler/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5829 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/k8s_integration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5828 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5827 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5826 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5825 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5824 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5823 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5822 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5821 | BinaryArtifactsID | error | `opt/services/multiregion/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5820 | BinaryArtifactsID | error | `opt/services/migration/**pycache**/advanced_migration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5819 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5818 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5817 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5816 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5815 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5814 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5813 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5812 | BinaryArtifactsID | error | `opt/services/cost_optimization/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5811 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5810 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5809 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5808 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5807 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5806 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5805 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5804 | BinaryArtifactsID | error | `opt/services/compliance/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5803 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5802 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/core.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5801 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5800 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/cli.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5799 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5798 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/api.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5797 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5796 | BinaryArtifactsID | error | `opt/services/anomaly/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5795 | BinaryArtifactsID | error | `opt/services/**pycache**/multi_cluster.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5794 | BinaryArtifactsID | error | `opt/services/**pycache**/message_queue.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5793 | BinaryArtifactsID | error | `opt/services/**pycache**/diagnostics.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5792 | BinaryArtifactsID | error | `opt/services/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5791 | BinaryArtifactsID | error | `opt/services/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5790 | BinaryArtifactsID | error | `opt/netcfg-tui/**pycache**/netcfg_tui.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5789 | BinaryArtifactsID | error | `opt/netcfg-tui/**pycache**/mock_mode.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5788 | BinaryArtifactsID | error | `opt/**pycache**/webhook_system.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5787 | BinaryArtifactsID | error | `opt/**pycache**/tracing_integration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5786 | BinaryArtifactsID | error | `opt/**pycache**/security_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5785 | BinaryArtifactsID | error | `opt/**pycache**/plugin_architecture.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5784 | BinaryArtifactsID | error | `opt/**pycache**/performance_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5783 | BinaryArtifactsID | error | `opt/**pycache**/oidc_oauth2.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5782 | BinaryArtifactsID | error | `opt/**pycache**/netcfg_tui_full.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5781 | BinaryArtifactsID | error | `opt/**pycache**/k8sctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5780 | BinaryArtifactsID | error | `opt/**pycache**/hvctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5779 | BinaryArtifactsID | error | `opt/**pycache**/graphql_integration.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5778 | BinaryArtifactsID | error | `opt/**pycache**/graphql_api.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5777 | BinaryArtifactsID | error | `opt/**pycache**/e2e_testing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5776 | BinaryArtifactsID | error | `opt/**pycache**/distributed_tracing.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5775 | BinaryArtifactsID | error | `opt/**pycache**/cephctl_enhanced.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5774 | BinaryArtifactsID | error | `opt/**pycache**/advanced_features.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5773 | BinaryArtifactsID | error | `opt/**pycache**/advanced_documentation.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5772 | BinaryArtifactsID | error | `opt/**pycache**/**init**.cpython-314.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5771 | BinaryArtifactsID | error | `opt/**pycache**/**init**.cpython-311.pyc` | 1 | score is 0: binary detected Click Remediation section below to solve this issue |
| 5770 | BranchProtectionID | error | `no file associated with this alert` | 1 | score is 3: branch protection is not maximal on development and all release branches: Warn: could not determine whether codeowners review is allowed Warn: no status checks found to merge onto branch 'main' Warn: PRs are not required to make changes on branch 'main'; or we don't have data to detect it.If you think it might be the latter, make sure to run Scorecard with a PAT or use Repo Rules (that are always public) instead of Branch Protection settings Click Remediation section below to solve this issue |
| 5769 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_rotation.py` | 243 | Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 5768 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_rotation.py` | 238 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 5767 | py/flask-debug | error | `opt/services/multiregion/api.py` | 593 | A Flask app appears to be run in debug mode. This may allow an attacker to run arbitrary code through the debugger. |
| 5766 | F841 | warning | `scripts/fix_markdown_lint.py` | 413 | local variable 'is_blank' is assigned to but never used |
| 5765 | F841 | warning | `scripts/fix_markdown_lint.py` | 412 | local variable 'is_table' is assigned to but never used |
| 5764 | F841 | warning | `scripts/fix_markdown_lint.py` | 221 | local variable 'in_ordered_list' is assigned to but never used |
| 5763 | F841 | warning | `opt/web/panel/socketio_server.py` | 299 | local variable 'permissions' is assigned to but never used |
| 5762 | F811 | warning | `opt/web/panel/graceful_shutdown.py` | 698 | redefinition of unused 'sys' from line 15 |
| 5761 | F841 | warning | `opt/web/panel/core/rpc_client.py` | 575 | local variable 'request' is assigned to but never used |
| 5760 | F841 | warning | `opt/web/panel/core/rpc_client.py` | 496 | local variable 'request' is assigned to but never used |
| 5759 | F841 | warning | `opt/web/panel/core/rpc_client.py` | 415 | local variable 'request' is assigned to but never used |
| 5756 | F841 | warning | `opt/web/panel/core/rpc_client.py` | 384 | local variable 'stub_class_name' is assigned to but never used |
| 5755 | F841 | warning | `opt/web/panel/batch_operations.py` | 538 | local variable 'rollback_duration' is assigned to but never used |
| 5754 | F841 | warning | `opt/web/panel/auth_2fa.py` | 800 | local variable 'e' is assigned to but never used |
| 5751 | F841 | warning | `opt/web/panel/analytics.py` | 328 | local variable 'last_timestamp' is assigned to but never used |
| 5750 | F841 | warning | `opt/tools/first_boot_keygen.py` | 120 | local variable 'args' is assigned to but never used |
| 5749 | F841 | warning | `opt/testing/test_phase4_integration.py` | 326 | local variable 'operation' is assigned to but never used |
| 5748 | F841 | warning | `opt/testing/test_phase4_integration.py` | 45 | local variable 'user_id' is assigned to but never used |
| 5747 | F811 | warning | `opt/services/tracing.py` | 892 | redefinition of unused 'asyncio' from line 16 |
| 5746 | F841 | warning | `opt/services/storage/multiregion_storage.py` | 245 | local variable 'config' is assigned to but never used |
| 5745 | F841 | warning | `opt/services/secrets_management.py` | 489 | local variable 'path' is assigned to but never used |
| 5744 | F841 | warning | `opt/services/secrets_management.py` | 434 | local variable 'path' is assigned to but never used |
| 5743 | F841 | warning | `opt/services/scheduler/api.py` | 144 | local variable 'cron' is assigned to but never used |
| 5742 | F841 | warning | `opt/services/rpc/tests/test_rpc_features.py` | 300 | local variable 'warnings' is assigned to but never used |
| 5741 | F841 | warning | `opt/services/rpc/tests/test_rpc_features.py` | 111 | local variable 'conn' is assigned to but never used |
| 5740 | F841 | warning | `opt/services/rpc/server.py` | 473 | local variable 'options' is assigned to but never used |
| 5739 | F841 | warning | `opt/services/rpc/rate_limiter.py` | 216 | local variable 'configs' is assigned to but never used |
| 5736 | F402 | warning | `opt/services/query_optimization_enhanced.py` | 276 | import 'field' from line 20 shadowed by loop variable |
| 5735 | F402 | warning | `opt/services/query_optimization_enhanced.py` | 261 | import 'field' from line 20 shadowed by loop variable |
| 5734 | F841 | warning | `opt/services/profiling.py` | 222 | local variable 'memory_percent' is assigned to but never used |
| 5733 | F841 | warning | `opt/services/compliance/cli.py` | 24 | local variable 'audit_parser' is assigned to but never used |
| 5731 | F401 | warning | `opt/installer/install_profile_logger.py` | 21 | 'typing.List' imported but unused |
| 5730 | F401 | warning | `opt/installer/install_profile_logger.py` | 21 | 'typing.Dict' imported but unused |
| 5729 | F401 | warning | `opt/installer/install_profile_logger.py` | 21 | 'typing.Any' imported but unused |
| 5728 | F841 | warning | `opt/hvctl_enhanced.py` | 642 | local variable 'total_mem_capacity' is assigned to but never used |
| 5725 | F401 | warning | `opt/services/network/multitenant_network.py` | 28 | 'typing.Union' imported but unused |
| 5724 | F401 | warning | `opt/services/network/multitenant_network.py` | 28 | 'typing.Callable' imported but unused |
| 5723 | F401 | warning | `opt/services/network/multitenant_network.py` | 22 | 'time' imported but unused |
| 5722 | F401 | warning | `opt/services/network/multitenant_network.py` | 21 | 'subprocess' imported but unused |
| 5721 | F401 | warning | `opt/services/network/multitenant_network.py` | 20 | 'random' imported but unused |
| 5720 | F401 | warning | `opt/services/network/multitenant_network.py` | 18 | 'json' imported but unused |
| 5719 | F401 | warning | `opt/services/network/multitenant_network.py` | 15 | 'asyncio' imported but unused |
| 5551 | F401 | warning | `opt/services/multiregion/replication_scheduler.py` | 31 | 'typing.Set' imported but unused |
| 5550 | F401 | warning | `opt/services/multiregion/replication_scheduler.py` | 29 | 'datetime.timedelta' imported but unused |
| 5531 | F401 | warning | `opt/services/multiregion/failover.py` | 17 | 'typing.Optional' imported but unused |
| 5456 | F841 | warning | `opt/services/multiregion/core.py` | 405 | local variable 'e' is assigned to but never used |
| 5449 | F401 | warning | `opt/services/multiregion/core.py` | 28 | '.k8s_integration.K8sClusterStatus' imported but unused |
| 5448 | F401 | warning | `opt/services/multiregion/core.py` | 25 | 'hashlib' imported but unused |
| 5447 | F401 | warning | `opt/services/multiregion/core.py` | 23 | 'typing.Callable' imported but unused |
| 5446 | F401 | warning | `opt/services/multiregion/core.py` | 21 | 'datetime.timedelta' imported but unused |
| 5445 | F401 | warning | `opt/services/multiregion/core.py` | 20 | 'dataclasses.asdict' imported but unused |
| 5437 | F841 | warning | `opt/services/multiregion/cli.py` | 454 | local variable 'resource' is assigned to but never used |
| 5431 | F541 | warning | `opt/services/multiregion/cli.py` | 378 | f-string is missing placeholders |
| 5429 | F541 | warning | `opt/services/multiregion/cli.py` | 369 | f-string is missing placeholders |
| 5425 | F541 | warning | `opt/services/multiregion/cli.py` | 349 | f-string is missing placeholders |
| 5424 | F541 | warning | `opt/services/multiregion/cli.py` | 347 | f-string is missing placeholders |
| 5418 | F841 | warning | `opt/services/multiregion/cli.py` | 321 | local variable 'config' is assigned to but never used |
| 5382 | F401 | warning | `opt/services/multiregion/cli.py` | 33 | 'opt.services.multiregion.core.ReplicationStatus' imported but unused |
| 5378 | F401 | warning | `opt/services/multiregion/cli.py` | 12 | 'datetime.datetime' imported but unused |
| 5377 | F401 | warning | `opt/services/multiregion/cli.py` | 11 | 'typing.Any' imported but unused |
| 5376 | F401 | warning | `opt/services/multiregion/cli.py` | 11 | 'typing.Dict' imported but unused |
| 5375 | F401 | warning | `opt/services/multiregion/cli.py` | 11 | 'typing.List' imported but unused |
| 5293 | F401 | warning | `opt/services/multiregion/api.py` | 13 | 'opt.services.multiregion.core.ReplicationStatus' imported but unused |
| 5292 | F401 | warning | `opt/services/multiregion/api.py` | 11 | 'functools.wraps' imported but unused |
| 5291 | F401 | warning | `opt/services/multiregion/api.py` | 7 | 'json' imported but unused |
| 5208 | F401 | warning | `opt/services/multi_cluster.py` | 29 | 'abc.abstractmethod' imported but unused |
| 5207 | F401 | warning | `opt/services/multi_cluster.py` | 29 | 'abc.ABC' imported but unused |
| 5206 | F401 | warning | `opt/services/multi_cluster.py` | 28 | 'asyncio' imported but unused |
| 5205 | F401 | warning | `opt/services/multi_cluster.py` | 24 | 'datetime.timedelta' imported but unused |
| 5204 | F401 | warning | `opt/services/multi_cluster.py` | 22 | 'json' imported but unused |
| 5189 | F401 | warning | `opt/services/cache/core.py` | 18 | 'datetime.timedelta' imported but unused |
| 5188 | F401 | warning | `opt/services/cache/core.py` | 17 | 'typing.List' imported but unused |
| 5187 | F401 | warning | `opt/services/cache/core.py` | 17 | 'typing.Union' imported but unused |
| 5186 | F401 | warning | `opt/services/cache/core.py` | 17 | 'typing.Optional' imported but unused |
| 5185 | F401 | warning | `opt/services/cache/core.py` | 13 | 'json' imported but unused |
| 5161 | F841 | warning | `opt/services/backup_manager.py` | 109 | local variable 'recv_proc' is assigned to but never used |
| 5151 | F841 | warning | `fix_code_scanning.py` | 73 | local variable 'parts' is assigned to but never used |
| 5145 | F401 | warning | `fix_code_scanning.py` | 3 | 'os' imported but unused |
| 5143 | F401 | warning | `cleanup_implemented.py` | 2 | 'os' imported but unused |
| 5119 | F401 | warning | `opt/netcfg_tui_app.py` | 15 | 'netcfg_tui_full.ConnectionState' imported but unused |
| 5118 | F401 | warning | `opt/netcfg_tui_app.py` | 15 | 'netcfg_tui_full.InterfaceStatus' imported but unused |
| 5117 | F401 | warning | `opt/netcfg_tui_app.py` | 15 | 'netcfg_tui_full.InterfaceType' imported but unused |
| 5058 | F541 | warning | `opt/services/migration/import_wizard.py` | 653 | f-string is missing placeholders |
| 5055 | F841 | warning | `opt/services/migration/import_wizard.py` | 636 | local variable 'pct' is assigned to but never used |
| 5000 | F401 | warning | `opt/services/migration/import_wizard.py` | 204 | 'pyVmomi.vim' imported but unused |
| 4999 | F401 | warning | `opt/services/migration/import_wizard.py` | 203 | 'pyVim.connect.Disconnect' imported but unused |
| 4991 | F401 | warning | `opt/services/migration/import_wizard.py` | 21 | 'threading' imported but unused |
| 4990 | F401 | warning | `opt/services/migration/import_wizard.py` | 14 | 'enum.auto' imported but unused |
| 4984 | F541 | warning | `opt/services/migration/advanced_migration.py` | 1187 | f-string is missing placeholders |
| 4815 | F401 | warning | `opt/services/migration/advanced_migration.py` | 28 | 'pathlib.Path' imported but unused |
| 4814 | F401 | warning | `opt/services/migration/advanced_migration.py` | 26 | 'datetime.timedelta' imported but unused |
| 4813 | F401 | warning | `opt/services/migration/advanced_migration.py` | 20 | 'math' imported but unused |
| 4812 | F401 | warning | `opt/services/migration/advanced_migration.py` | 18 | 'json' imported but unused |
| 4811 | F401 | warning | `opt/services/migration/advanced_migration.py` | 17 | 'hashlib' imported but unused |
| 4772 | F811 | warning | `opt/services/marketplace/marketplace_service.py` | 1155 | redefinition of unused 'tempfile' from line 28 |
| 4629 | F401 | warning | `opt/services/marketplace/marketplace_service.py` | 33 | 'urllib.parse.urlparse' imported but unused |
| 4628 | F401 | warning | `opt/services/marketplace/marketplace_service.py` | 32 | 'concurrent.futures.Future' imported but unused |
| 4627 | F401 | warning | `opt/services/marketplace/marketplace_service.py` | 26 | 'time' imported but unused |
| 4626 | F401 | warning | `opt/services/marketplace/marketplace_service.py` | 19 | 'enum.auto' imported but unused |
| 4625 | F401 | warning | `opt/services/marketplace/marketplace_service.py` | 18 | 'typing.Set' imported but unused |
| 4536 | F401 | warning | `opt/services/licensing/licensing_server.py` | 36 | 'cryptography.fernet.Fernet' imported but unused |
| 4535 | F401 | warning | `opt/services/licensing/licensing_server.py` | 33 | 'cryptography.hazmat.primitives.asymmetric.padding' imported but unused |
| 4534 | F401 | warning | `opt/services/licensing/licensing_server.py` | 33 | 'cryptography.hazmat.primitives.asymmetric.rsa' imported but unused |
| 4524 | F541 | warning | `opt/services/health_check.py` | 430 | f-string is missing placeholders |
| 4521 | F541 | warning | `opt/services/health_check.py` | 419 | f-string is missing placeholders |
| 4520 | F541 | warning | `opt/services/health_check.py` | 415 | f-string is missing placeholders |
| 4481 | F401 | warning | `opt/services/health_check.py` | 25 | 'dataclasses.asdict' imported but unused |
| 4480 | F401 | warning | `opt/services/health_check.py` | 24 | 'typing.Tuple' imported but unused |
| 4448 | F541 | warning | `opt/services/ha/fencing_agent.py` | 455 | f-string is missing placeholders |
| 4447 | F541 | warning | `opt/services/ha/fencing_agent.py` | 452 | f-string is missing placeholders |
| 4432 | F541 | warning | `opt/services/ha/fencing_agent.py` | 356 | f-string is missing placeholders |
| 4421 | F841 | warning | `opt/services/ha/fencing_agent.py` | 302 | local variable 'wd' is assigned to but never used |
| 4388 | F541 | warning | `opt/services/fleet/federation_manager.py` | 1016 | f-string is missing placeholders |
| 4267 | F401 | warning | `opt/services/fleet/federation_manager.py` | 26 | 'abc.abstractmethod' imported but unused |
| 4266 | F401 | warning | `opt/services/fleet/federation_manager.py` | 26 | 'abc.ABC' imported but unused |
| 4265 | F401 | warning | `opt/services/fleet/federation_manager.py` | 25 | 'concurrent.futures.Future' imported but unused |
| 4264 | F401 | warning | `opt/services/fleet/federation_manager.py` | 25 | 'concurrent.futures.ThreadPoolExecutor' imported but unused |
| 4263 | F401 | warning | `opt/services/fleet/federation_manager.py` | 18 | 'time' imported but unused |
| 4262 | F401 | warning | `opt/services/fleet/federation_manager.py` | 14 | 'enum.auto' imported but unused |
| 4207 | F401 | warning | `opt/services/diagnostics.py` | 29 | 'json' imported but unused |
| 4206 | F401 | warning | `opt/services/diagnostics.py` | 27 | 'typing.Callable' imported but unused |
| 4108 | F401 | warning | `opt/services/database/query_optimizer.py` | 23 | 'typing.Callable' imported but unused |
| 4107 | F401 | warning | `opt/services/database/query_optimizer.py` | 21 | 'datetime.timedelta' imported but unused |
| 4099 | F401 | warning | `opt/services/cost_optimization/core.py` | 3 | 'time' imported but unused |
| 4098 | F401 | warning | `opt/services/cost_optimization/core.py` | 2 | 'json' imported but unused |
| 4094 | F401 | warning | `opt/services/cost_optimization/cli.py` | 4 | 'typing.List' imported but unused |
| 4093 | F401 | warning | `opt/services/cost_optimization/cli.py` | 3 | 'sys' imported but unused |
| 4092 | F401 | warning | `opt/services/cost_optimization/cli.py` | 1 | 'argparse' imported but unused |
| 4056 | F841 | warning | `opt/services/cost/cost_engine.py` | 557 | local variable 'mem_max' is assigned to but never used |
| 4054 | F841 | warning | `opt/services/cost/cost_engine.py` | 551 | local variable 'cpu_max' is assigned to but never used |
| 3927 | F841 | warning | `opt/services/containers/container_integration.py` | 721 | local variable 'result' is assigned to but never used |
| 3924 | F841 | warning | `opt/services/containers/container_integration.py` | 709 | local variable 'result' is assigned to but never used |
| 3909 | F541 | warning | `opt/services/containers/container_integration.py` | 525 | f-string is missing placeholders |
| 3908 | F541 | warning | `opt/services/containers/container_integration.py` | 524 | f-string is missing placeholders |
| 3884 | F541 | warning | `opt/services/containers/container_integration.py` | 289 | f-string is missing placeholders |
| 3875 | F401 | warning | `opt/services/containers/container_integration.py` | 25 | 'struct' imported but unused |
| 3874 | F401 | warning | `opt/services/containers/container_integration.py` | 24 | 'socket' imported but unused |
| 3873 | F401 | warning | `opt/services/containers/container_integration.py` | 21 | 'hashlib' imported but unused |
| 3872 | F401 | warning | `opt/services/containers/container_integration.py` | 14 | 'typing.Set' imported but unused |
| 3865 | F811 | warning | `opt/services/connection_pool.py` | 773 | redefinition of unused 'asyncio' from line 20 |
| 3751 | F401 | warning | `opt/services/connection_pool.py` | 29 | 'typing.Union' imported but unused |
| 3750 | F401 | warning | `opt/services/connection_pool.py` | 29 | 'typing.Callable' imported but unused |
| 3749 | F401 | warning | `opt/services/connection_pool.py` | 25 | 'contextlib.contextmanager' imported but unused |
| 3748 | F401 | warning | `opt/services/connection_pool.py` | 23 | 'threading' imported but unused |
| 3744 | F401 | warning | `opt/services/compliance/core.py` | 5 | 'typing.Callable' imported but unused |
| 3743 | F401 | warning | `opt/services/compliance/core.py` | 4 | 'dataclasses.asdict' imported but unused |
| 3742 | F401 | warning | `opt/services/compliance/core.py` | 3 | 'time' imported but unused |
| 3741 | F401 | warning | `opt/services/compliance/core.py` | 2 | 'json' imported but unused |
| 3737 | F841 | warning | `opt/services/compliance/cli.py` | 20 | local variable 'audit_parser' is assigned to but never used |
| 3736 | F841 | warning | `opt/services/compliance/cli.py` | 21 | local variable 'policy_parser' is assigned to but never used |
| 3735 | F401 | warning | `opt/services/compliance/cli.py` | 5 | '.core.CompliancePolicy' imported but unused |
| 3734 | F401 | warning | `opt/services/compliance/cli.py` | 4 | 'typing.List' imported but unused |
| 3733 | F401 | warning | `opt/services/compliance/cli.py` | 3 | 'sys' imported but unused |
| 3732 | F401 | warning | `opt/services/compliance/cli.py` | 1 | 'argparse' imported but unused |
| 3731 | F401 | warning | `opt/services/compliance/api.py` | 1 | 'flask.request' imported but unused |
| 3723 | F541 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 1209 | f-string is missing placeholders |
| 3582 | F841 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 272 | local variable 'old_version' is assigned to but never used |
| 3567 | F401 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 26 | 'concurrent.futures.as_completed' imported but unused |
| 3566 | F401 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 25 | 'struct' imported but unused |
| 3565 | F401 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 23 | 'heapq' imported but unused |
| 3564 | F401 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 20 | 'json' imported but unused |
| 3563 | F401 | warning | `opt/services/cluster/large_cluster_optimizer.py` | 17 | 'pathlib.Path' imported but unused |
| 3496 | F401 | warning | `opt/services/cache.py` | 36 | 'redis' imported but unused |
| 3495 | F401 | warning | `opt/services/cache.py` | 27 | 'datetime.timedelta' imported but unused |
| 3494 | F401 | warning | `opt/services/cache.py` | 24 | 'typing.List' imported but unused |
| 3395 | F401 | warning | `opt/services/business_metrics.py` | 27 | 'typing.Union' imported but unused |
| 3394 | F401 | warning | `opt/services/business_metrics.py` | 25 | 'datetime.timedelta' imported but unused |
| 3264 | F401 | warning | `opt/services/billing/billing_integration.py` | 32 | 'typing.Union' imported but unused |
| 3263 | F401 | warning | `opt/services/billing/billing_integration.py` | 32 | 'typing.TypeVar' imported but unused |
| 3262 | F401 | warning | `opt/services/billing/billing_integration.py` | 32 | 'typing.Protocol' imported but unused |
| 3261 | F401 | warning | `opt/services/billing/billing_integration.py` | 24 | 'secrets' imported but unused |
| 3260 | F401 | warning | `opt/services/billing/billing_integration.py` | 19 | 'asyncio' imported but unused |
| 3208 | F401 | warning | `opt/services/backup_manager.py` | 22 | 'typing.Dict' imported but unused |
| 3207 | F401 | warning | `opt/services/backup_manager.py` | 21 | 'dataclasses.field' imported but unused |
| 3206 | F401 | warning | `opt/services/backup_manager.py` | 16 | 'asyncio' imported but unused |
| 3103 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 29 | 'abc.abstractmethod' imported but unused |
| 3102 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 29 | 'abc.ABC' imported but unused |
| 3101 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 27 | 'concurrent.futures.Future' imported but unused |
| 3100 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 23 | 'struct' imported but unused |
| 3099 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 17 | 'typing.Set' imported but unused |
| 3098 | F401 | warning | `opt/services/backup/dedup_backup_service.py` | 17 | 'typing.Callable' imported but unused |
| 2898 | F401 | warning | `opt/services/backup/backup_intelligence.py` | 19 | 'math' imported but unused |
| 2897 | F401 | warning | `opt/services/backup/backup_intelligence.py` | 17 | 'json' imported but unused |
| 2896 | F401 | warning | `opt/services/backup/backup_intelligence.py` | 16 | 'hashlib' imported but unused |
| 2876 | F841 | warning | `opt/services/auth/ldap_backend.py` | 411 | local variable 'user' is assigned to but never used |
| 2812 | F401 | warning | `opt/services/auth/ldap_backend.py` | 21 | 'datetime.timedelta' imported but unused |
| 2697 | F401 | warning | `opt/services/audit_encryption.py` | 24 | 'typing.Tuple' imported but unused |
| 2696 | F401 | warning | `opt/services/audit_encryption.py` | 19 | 'os' imported but unused |
| 2686 | F811 | warning | `opt/services/api_key_rotation.py` | 740 | redefinition of unused 'asyncio' from line 16 |
| 2573 | F401 | warning | `opt/services/api_key_rotation.py` | 26 | 'json' imported but unused |
| 2572 | F401 | warning | `opt/services/api_key_rotation.py` | 18 | 'hmac' imported but unused |
| 2495 | F401 | warning | `opt/services/anomaly/test_lstm.py` | 4 | 'core.LSTMModel' imported but unused |
| 2384 | F841 | warning | `opt/services/anomaly/core.py` | 283 | local variable 'total_loss' is assigned to but never used |
| 2382 | F841 | warning | `opt/services/anomaly/core.py` | 280 | local variable 'Wy_mut' is assigned to but never used |
| 2381 | F841 | warning | `opt/services/anomaly/core.py` | 279 | local variable 'Wf_mut' is assigned to but never used |
| 2379 | F841 | warning | `opt/services/anomaly/core.py` | 275 | local variable 'best_loss' is assigned to but never used |
| 2365 | F401 | warning | `opt/services/anomaly/core.py` | 21 | 'typing.Callable' imported but unused |
| 2364 | F401 | warning | `opt/services/anomaly/core.py` | 18 | 'dataclasses.asdict' imported but unused |
| 2363 | F401 | warning | `opt/services/anomaly/core.py` | 16 | 'time' imported but unused |
| 2362 | F401 | warning | `opt/services/anomaly/core.py` | 13 | 'json' imported but unused |
| 2330 | F541 | warning | `opt/services/anomaly/cli.py` | 330 | f-string is missing placeholders |
| 2286 | F401 | warning | `opt/services/anomaly/cli.py` | 13 | 'datetime.timedelta' imported but unused |
| 2285 | F401 | warning | `opt/services/anomaly/cli.py` | 13 | 'datetime.datetime' imported but unused |
| 2160 | F401 | warning | `opt/services/anomaly/api.py` | 18 | 'flask.jsonify' imported but unused |
| 2159 | F401 | warning | `opt/services/anomaly/api.py` | 10 | 'asyncio' imported but unused |
| 2145 | F541 | warning | `opt/security/hardening_scanner.py` | 221 | f-string is missing placeholders |
| 2128 | F401 | warning | `opt/security/hardening_scanner.py` | 14 | 'typing.Dict' imported but unused |
| 2127 | F841 | warning | `opt/plugin_architecture.py` | 261 | local variable 'new_config' is assigned to but never used |
| 2126 | F401 | warning | `opt/plugin_architecture.py` | 16 | 'typing.Type' imported but unused |
| 2125 | F841 | warning | `opt/performance_testing.py` | 259 | local variable 'result' is assigned to but never used |
| 2124 | F401 | warning | `opt/performance_testing.py` | 23 | 'threading' imported but unused |
| 2123 | F401 | warning | `opt/oidc_oauth2.py` | 24 | 'urllib.parse.quote' imported but unused |
| 2122 | F401 | warning | `opt/oidc_oauth2.py` | 20 | 'dataclasses.asdict' imported but unused |
| 2121 | F401 | warning | `opt/oidc_oauth2.py` | 17 | 'json' imported but unused |
| 2120 | F401 | warning | `opt/oidc_oauth2.py` | 16 | 'hmac' imported but unused |
| 2119 | F401 | warning | `opt/oidc_oauth2.py` | 15 | 'hashlib' imported but unused |
| 2118 | F401 | warning | `opt/netcfg_tui_full.py` | 19 | 'json' imported but unused |
| 2108 | F401 | warning | `opt/netcfg-tui/tests/test_netcfg.py` | 12 | 'netcfg_tui.BondConfig' imported but unused |
| 2083 | F841 | warning | `opt/netcfg-tui/netcfg_tui.py` | 1023 | local variable 'e' is assigned to but never used |
| 2073 | F541 | warning | `opt/netcfg-tui/netcfg_tui.py` | 760 | f-string is missing placeholders |
| 2071 | F841 | warning | `opt/netcfg-tui/netcfg_tui.py` | 769 | local variable 'bond_name' is assigned to but never used |
| 2058 | F401 | warning | `opt/netcfg-tui/netcfg_tui.py` | 6 | 're' imported but unused |
| 2056 | F541 | warning | `opt/netcfg-tui/mock_mode.py` | 633 | f-string is missing placeholders |
| 1975 | F401 | warning | `opt/netcfg-tui/mock_mode.py` | 22 | 'typing.Tuple' imported but unused |
| 1912 | F401 | warning | `opt/netcfg-tui/main.py` | 24 | 'dataclasses.asdict' imported but unused |
| 1911 | F401 | warning | `opt/netcfg-tui/backends.py` | 17 | 'typing.Any' imported but unused |
| 1910 | F541 | warning | `opt/monitoring/enhanced.py` | 144 | f-string is missing placeholders |
| 1909 | F541 | warning | `opt/monitoring/enhanced.py` | 66 | f-string is missing placeholders |
| 1831 | F401 | warning | `opt/models/phase4_models.py` | 13 | 'sqlalchemy.Table' imported but unused |
| 1827 | F541 | warning | `opt/models/migrations.py` | 333 | f-string is missing placeholders |
| 1790 | F541 | warning | `opt/k8sctl_enhanced.py` | 603 | f-string is missing placeholders |
| 1789 | F541 | warning | `opt/k8sctl_enhanced.py` | 600 | f-string is missing placeholders |
| 1788 | F541 | warning | `opt/k8sctl_enhanced.py` | 596 | f-string is missing placeholders |
| 1787 | F541 | warning | `opt/k8sctl_enhanced.py` | 571 | f-string is missing placeholders |
| 1786 | F541 | warning | `opt/k8sctl_enhanced.py` | 542 | f-string is missing placeholders |
| 1785 | F541 | warning | `opt/k8sctl_enhanced.py` | 539 | f-string is missing placeholders |
| 1784 | F541 | warning | `opt/k8sctl_enhanced.py` | 536 | f-string is missing placeholders |
| 1783 | F541 | warning | `opt/k8sctl_enhanced.py` | 530 | f-string is missing placeholders |
| 1782 | F541 | warning | `opt/k8sctl_enhanced.py` | 524 | f-string is missing placeholders |
| 1781 | F541 | warning | `opt/k8sctl_enhanced.py` | 511 | f-string is missing placeholders |
| 1780 | F541 | warning | `opt/k8sctl_enhanced.py` | 496 | f-string is missing placeholders |
| 1779 | F541 | warning | `opt/k8sctl_enhanced.py` | 331 | f-string is missing placeholders |
| 1778 | F541 | warning | `opt/k8sctl_enhanced.py` | 330 | f-string is missing placeholders |
| 1777 | F541 | warning | `opt/k8sctl_enhanced.py` | 325 | f-string is missing placeholders |
| 1776 | F541 | warning | `opt/k8sctl_enhanced.py` | 324 | f-string is missing placeholders |
| 1775 | F541 | warning | `opt/k8sctl_enhanced.py` | 317 | f-string is missing placeholders |
| 1774 | F401 | warning | `opt/k8sctl_enhanced.py` | 22 | 'typing.Dict' imported but unused |
| 1682 | F401 | warning | `opt/installer/install_profile_logger.py` | 22 | 'typing.Any' imported but unused |
| 1681 | F401 | warning | `opt/installer/install_profile_logger.py` | 18 | 'sys' imported but unused |
| 1680 | F541 | warning | `opt/hvctl_enhanced.py` | 878 | f-string is missing placeholders |
| 1679 | F541 | warning | `opt/hvctl_enhanced.py` | 858 | f-string is missing placeholders |
| 1678 | F541 | warning | `opt/hvctl_enhanced.py` | 833 | f-string is missing placeholders |
| 1677 | F541 | warning | `opt/hvctl_enhanced.py` | 818 | f-string is missing placeholders |
| 1676 | F541 | warning | `opt/hvctl_enhanced.py` | 796 | f-string is missing placeholders |
| 1675 | F541 | warning | `opt/hvctl_enhanced.py` | 783 | f-string is missing placeholders |
| 1674 | F541 | warning | `opt/hvctl_enhanced.py` | 780 | f-string is missing placeholders |
| 1673 | F541 | warning | `opt/hvctl_enhanced.py` | 777 | f-string is missing placeholders |
| 1663 | F841 | warning | `opt/hvctl_enhanced.py` | 639 | local variable 'total_mem_capacity' is assigned to but never used |
| 1661 | F541 | warning | `opt/hvctl_enhanced.py` | 547 | f-string is missing placeholders |
| 1660 | F541 | warning | `opt/hvctl_enhanced.py` | 545 | f-string is missing placeholders |
| 1658 | F541 | warning | `opt/hvctl_enhanced.py` | 392 | f-string is missing placeholders |
| 1656 | F541 | warning | `opt/hvctl_enhanced.py` | 356 | f-string is missing placeholders |
| 1655 | F541 | warning | `opt/hvctl_enhanced.py` | 355 | f-string is missing placeholders |
| 1553 | F401 | warning | `opt/helpers/standardization.py` | 25 | 'sys' imported but unused |
| 1552 | F401 | warning | `opt/helpers/standardization.py` | 24 | 'hashlib' imported but unused |
| 1551 | F401 | warning | `opt/helpers/standardization.py` | 23 | 'typing.TypeVar' imported but unused |
| 1550 | F401 | warning | `opt/helpers/standardization.py` | 20 | 'datetime.timedelta' imported but unused |
| 1549 | F401 | warning | `opt/helpers/standardization.py` | 17 | 'inspect' imported but unused |
| 1548 | F401 | warning | `opt/graphql_integration.py` | 15 | 'json' imported but unused |
| 1488 | F541 | warning | `opt/distributed_tracing.py` | 554 | f-string is missing placeholders |
| 1487 | F401 | warning | `opt/distributed_tracing.py` | 20 | 'datetime.datetime' imported but unused |
| 1427 | F401 | warning | `opt/deployment/migrations.py` | 23 | 'json' imported but unused |
| 1426 | F401 | warning | `opt/deployment/migrations.py` | 19 | 'typing.Callable' imported but unused |
| 1380 | F401 | warning | `opt/deployment/configuration.py` | 20 | 'json' imported but unused |
| 1379 | F401 | warning | `opt/deployment/configuration.py` | 17 | 'typing.List' imported but unused |
| 1278 | F401 | warning | `opt/core/unified_backend.py` | 23 | 'datetime.timedelta' imported but unused |
| 1277 | F401 | warning | `opt/core/unified_backend.py` | 22 | 'typing.Union' imported but unused |
| 1276 | F401 | warning | `opt/core/unified_backend.py` | 22 | 'typing.Awaitable' imported but unused |
| 1275 | F401 | warning | `opt/core/unified_backend.py` | 17 | 'asyncio' imported but unused |
| 1166 | F401 | warning | `opt/core/request_context.py` | 19 | 'typing.Union' imported but unused |
| 1165 | F401 | warning | `opt/core/request_context.py` | 19 | 'typing.List' imported but unused |
| 1152 | F841 | warning | `opt/config_distributor.py` | 167 | local variable 'list_parser' is assigned to but never used |
| 1138 | F401 | warning | `opt/config_distributor.py` | 22 | 'dataclasses.field' imported but unused |
| 1114 | F401 | warning | `opt/cert_manager.py` | 18 | 'os' imported but unused |
| 1113 | F541 | warning | `opt/cephctl_enhanced.py` | 591 | f-string is missing placeholders |
| 1112 | F541 | warning | `opt/cephctl_enhanced.py` | 585 | f-string is missing placeholders |
| 1111 | F541 | warning | `opt/cephctl_enhanced.py` | 566 | f-string is missing placeholders |
| 1110 | F541 | warning | `opt/cephctl_enhanced.py` | 544 | f-string is missing placeholders |
| 1109 | F541 | warning | `opt/cephctl_enhanced.py` | 541 | f-string is missing placeholders |
| 1108 | F541 | warning | `opt/cephctl_enhanced.py` | 538 | f-string is missing placeholders |
| 1107 | F541 | warning | `opt/cephctl_enhanced.py` | 516 | f-string is missing placeholders |
| 1106 | F541 | warning | `opt/cephctl_enhanced.py` | 513 | f-string is missing placeholders |
| 1105 | F541 | warning | `opt/cephctl_enhanced.py` | 335 | f-string is missing placeholders |
| 1104 | F541 | warning | `opt/cephctl_enhanced.py` | 334 | f-string is missing placeholders |
| 1103 | F541 | warning | `opt/cephctl_enhanced.py` | 333 | f-string is missing placeholders |
| 1102 | F541 | warning | `opt/cephctl_enhanced.py` | 332 | f-string is missing placeholders |
| 1101 | F541 | warning | `opt/cephctl_enhanced.py` | 331 | f-string is missing placeholders |
| 1100 | F541 | warning | `opt/cephctl_enhanced.py` | 326 | f-string is missing placeholders |
| 1099 | F541 | warning | `opt/cephctl_enhanced.py` | 325 | f-string is missing placeholders |
| 1098 | F541 | warning | `opt/cephctl_enhanced.py` | 319 | f-string is missing placeholders |
| 1097 | F541 | warning | `opt/cephctl_enhanced.py` | 314 | f-string is missing placeholders |
| 1096 | F541 | warning | `opt/cephctl_enhanced.py` | 313 | f-string is missing placeholders |
| 1095 | F541 | warning | `opt/cephctl_enhanced.py` | 312 | f-string is missing placeholders |
| 1035 | F401 | warning | `opt/build/validate-iso.py` | 22 | 'typing.Tuple' imported but unused |
| 1034 | F401 | warning | `opt/build/validate-iso.py` | 17 | 're' imported but unused |
| 1033 | F401 | warning | `opt/build/validate-iso.py` | 15 | 'json' imported but unused |
| 979 | F401 | warning | `opt/ansible/validate-inventory.py` | 25 | 'typing.Any' imported but unused |
| 978 | F401 | warning | `opt/ansible/validate-inventory.py` | 25 | 'typing.Tuple' imported but unused |
| 977 | F401 | warning | `opt/ansible/validate-inventory.py` | 25 | 'typing.Set' imported but unused |
| 976 | F401 | warning | `opt/ansible/validate-inventory.py` | 19 | 'os' imported but unused |
| 975 | F401 | warning | `opt/ansible/validate-inventory.py` | 18 | 'json' imported but unused |
| 974 | F401 | warning | `opt/advanced_documentation.py` | 18 | 'json' imported but unused |
| 972 | F401 | warning | `mock_mode.py` | 2 | 'opt.testing.mock_mode.*' imported but unused |
| 971 | F403 | warning | `mock_mode.py` | 2 | 'from opt.testing.mock_mode import *' used; unable to detect undefined names |
| 965 | F401 | warning | `etc/debvisor/test_validate_blocklists.py` | 477 | 'ipaddress.ip_network' imported but unused |
| 919 | F401 | warning | `etc/debvisor/test_validate_blocklists.py` | 18 | 'pathlib.Path' imported but unused |
| 918 | F401 | warning | `etc/debvisor/test_validate_blocklists.py` | 17 | 'sys' imported but unused |
| 94 | py/stack-trace-exposure | error | `opt/web/panel/routes/passthrough.py` | 118 | Stack trace information flows to this location and may be exposed to an external user. |
| 93 | py/stack-trace-exposure | error | `opt/web/panel/routes/nodes.py` | 234 | Stack trace information flows to this location and may be exposed to an external user. |
| 92 | py/stack-trace-exposure | error | `opt/web/panel/routes/health.py` | 144 | Stack trace information flows to this location and may be exposed to an external user. |
| 91 | py/stack-trace-exposure | error | `opt/web/panel/routes/health.py` | 68 | Stack trace information flows to this location and may be exposed to an external user. Stack trace information flows to this location and may be exposed to an external user. |
| 90 | py/stack-trace-exposure | error | `opt/web/panel/routes/health.py` | 36 | Stack trace information flows to this location and may be exposed to an external user. |
| 89 | py/stack-trace-exposure | error | `opt/graphql_integration.py` | 312 | Stack trace information flows to this location and may be exposed to an external user. |
| 88 | py/stack-trace-exposure | error | `opt/graphql_integration.py` | 289 | Stack trace information flows to this location and may be exposed to an external user. |
| 87 | py/stack-trace-exposure | error | `opt/graphql_integration.py` | 272 | Stack trace information flows to this location and may be exposed to an external user. |
| 86 | py/stack-trace-exposure | error | `opt/graphql_integration.py` | 237 | Stack trace information flows to this location and may be exposed to an external user. |
| 85 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 591 | Stack trace information flows to this location and may be exposed to an external user. |
| 84 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 591 | Stack trace information flows to this location and may be exposed to an external user. |
| 83 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 585 | Stack trace information flows to this location and may be exposed to an external user. |
| 82 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 585 | Stack trace information flows to this location and may be exposed to an external user. |
| 81 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 579 | Stack trace information flows to this location and may be exposed to an external user. |
| 80 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 579 | Stack trace information flows to this location and may be exposed to an external user. |
| 79 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 572 | Stack trace information flows to this location and may be exposed to an external user. |
| 78 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 572 | Stack trace information flows to this location and may be exposed to an external user. |
| 77 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 566 | Stack trace information flows to this location and may be exposed to an external user. |
| 76 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 566 | Stack trace information flows to this location and may be exposed to an external user. |
| 75 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 561 | Stack trace information flows to this location and may be exposed to an external user. |
| 74 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 561 | Stack trace information flows to this location and may be exposed to an external user. |
| 73 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 556 | Stack trace information flows to this location and may be exposed to an external user. |
| 72 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 556 | Stack trace information flows to this location and may be exposed to an external user. |
| 71 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 550 | Stack trace information flows to this location and may be exposed to an external user. |
| 70 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 550 | Stack trace information flows to this location and may be exposed to an external user. |
| 69 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 545 | Stack trace information flows to this location and may be exposed to an external user. |
| 68 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 545 | Stack trace information flows to this location and may be exposed to an external user. |
| 67 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 540 | Stack trace information flows to this location and may be exposed to an external user. |
| 66 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 540 | Stack trace information flows to this location and may be exposed to an external user. |
| 65 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 535 | Stack trace information flows to this location and may be exposed to an external user. |
| 64 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 535 | Stack trace information flows to this location and may be exposed to an external user. |
| 63 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 530 | Stack trace information flows to this location and may be exposed to an external user. |
| 62 | py/stack-trace-exposure | error | `opt/services/multiregion/api.py` | 530 | Stack trace information flows to this location and may be exposed to an external user. |
| 61 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 803 | Stack trace information flows to this location and may be exposed to an external user. |
| 60 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 795 | Stack trace information flows to this location and may be exposed to an external user. |
| 59 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 791 | Stack trace information flows to this location and may be exposed to an external user. |
| 58 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 783 | Stack trace information flows to this location and may be exposed to an external user. |
| 57 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 778 | Stack trace information flows to this location and may be exposed to an external user. |
| 56 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 774 | Stack trace information flows to this location and may be exposed to an external user. |
| 55 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 770 | Stack trace information flows to this location and may be exposed to an external user. |
| 54 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 762 | Stack trace information flows to this location and may be exposed to an external user. |
| 53 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 758 | Stack trace information flows to this location and may be exposed to an external user. |
| 52 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 750 | Stack trace information flows to this location and may be exposed to an external user. |
| 51 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 746 | Stack trace information flows to this location and may be exposed to an external user. |
| 50 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 742 | Stack trace information flows to this location and may be exposed to an external user. |
| 49 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 734 | Stack trace information flows to this location and may be exposed to an external user. |
| 48 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 730 | Stack trace information flows to this location and may be exposed to an external user. |
| 47 | py/stack-trace-exposure | error | `opt/services/anomaly/api.py` | 726 | Stack trace information flows to this location and may be exposed to an external user. |
| 46 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 559 | Stack trace information flows to this location and may be exposed to an external user. |
| 45 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 554 | Stack trace information flows to this location and may be exposed to an external user. |
| 44 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 549 | Stack trace information flows to this location and may be exposed to an external user. |
| 43 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 542 | Stack trace information flows to this location and may be exposed to an external user. |
| 42 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 537 | Stack trace information flows to this location and may be exposed to an external user. |
| 41 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 532 | Stack trace information flows to this location and may be exposed to an external user. Stack trace information flows to this location and may be exposed to an external user. |
| 40 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 527 | Stack trace information flows to this location and may be exposed to an external user. |
| 39 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 522 | Stack trace information flows to this location and may be exposed to an external user. |
| 38 | py/stack-trace-exposure | error | `opt/services/scheduler/api.py` | 515 | Stack trace information flows to this location and may be exposed to an external user. Stack trace information flows to this location and may be exposed to an external user. |
| 37 | py/weak-sensitive-data-hashing | warning | `opt/services/rpc/auth.py` | 577 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 36 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_rotation.py` | 232 | Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (MD5) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 35 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_rotation.py` | 238 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 34 | py/weak-sensitive-data-hashing | warning | `opt/services/api_key_manager.py` | 157 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 33 | py/flask-debug | error | `opt/services/multiregion/api.py` | 573 | A Flask app appears to be run in debug mode. This may allow an attacker to run arbitrary code through the debugger. |
| 32 | py/reflective-xss | error | `opt/services/multiregion/api.py` | 566 | Cross-site scripting vulnerability due to a user-provided value. |
| 31 | py/reflective-xss | error | `opt/services/multiregion/api.py` | 550 | Cross-site scripting vulnerability due to a user-provided value. |
| 30 | py/reflective-xss | error | `opt/services/multiregion/api.py` | 545 | Cross-site scripting vulnerability due to a user-provided value. |
| 29 | py/reflective-xss | error | `opt/services/multiregion/api.py` | 540 | Cross-site scripting vulnerability due to a user-provided value. |
| 28 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 791 | Cross-site scripting vulnerability due to a user-provided value. |
| 27 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 783 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 26 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 778 | Cross-site scripting vulnerability due to a user-provided value. |
| 25 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 770 | Cross-site scripting vulnerability due to a user-provided value. |
| 24 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 758 | Cross-site scripting vulnerability due to a user-provided value. |
| 23 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 750 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 22 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 742 | Cross-site scripting vulnerability due to a user-provided value. |
| 21 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 734 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 20 | py/reflective-xss | error | `opt/services/anomaly/api.py` | 726 | Cross-site scripting vulnerability due to a user-provided value. |
| 19 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 554 | Cross-site scripting vulnerability due to a user-provided value. |
| 18 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 549 | Cross-site scripting vulnerability due to a user-provided value. |
| 17 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 542 | Cross-site scripting vulnerability due to a user-provided value. |
| 16 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 537 | Cross-site scripting vulnerability due to a user-provided value. |
| 15 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 532 | Cross-site scripting vulnerability due to a user-provided value. |
| 14 | py/reflective-xss | error | `opt/services/scheduler/api.py` | 527 | Cross-site scripting vulnerability due to a user-provided value. |
| 13 | py/url-redirection | error | `opt/web/panel/routes/auth.py` | 104 | Untrusted URL redirection depends on a user-provided value. |
| 12 | py/url-redirection | error | `opt/web/panel/app.py` | 456 | Untrusted URL redirection depends on a user-provided value. |
| 11 | py/clear-text-storage-sensitive-data | error | `opt/tools/first_boot_keygen.py` | 111 | This expression stores sensitive data (secret) as clear text. |
| 10 | py/clear-text-logging-sensitive-data | error | `opt/system/hypervisor/xen_driver.py` | 982 | This expression logs sensitive data (password) as clear text. |
| 9 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets/vault_manager.py` | 635 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 8 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets/vault_manager.py` | 631 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 7 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets_management.py` | 665 | This expression logs sensitive data (secret) as clear text. |
| 6 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets_management.py` | 653 | This expression logs sensitive data (password) as clear text. |
| 5 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets_management.py` | 649 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 4 | py/clear-text-logging-sensitive-data | error | `opt/services/secrets_management.py` | 614 | This expression logs sensitive data (password) as clear text. |
| 3 | py/clear-text-logging-sensitive-data | error | `opt/services/api_key_rotation.py` | 767 | This expression logs sensitive data (password) as clear text. |
| 2 | py/clear-text-logging-sensitive-data | error | `opt/services/api_key_rotation.py` | 758 | This expression logs sensitive data (password) as clear text. |
| 1 | py/clear-text-logging-sensitive-data | error | `opt/services/api_key_manager.py` | 454 | This expression logs sensitive data (password) as clear text. This expression logs sensitive data (password) as clear text. |

## Code Quality & Style Issues

| ID | Rule | File | Line | Message |
|----|------|------|------|---------|
| 6981 | E305 | `tests/test_health_blueprint.py` | 64 | expected 2 blank lines after class or function definition, found 1 |
| 6980 | W293 | `tests/test_health_blueprint.py` | 56 | blank line contains whitespace |
| 6979 | W293 | `tests/test_health_blueprint.py` | 53 | blank line contains whitespace |
| 6978 | W293 | `tests/test_health_blueprint.py` | 43 | blank line contains whitespace |
| 6977 | W293 | `tests/test_health_blueprint.py` | 40 | blank line contains whitespace |
| 6976 | W293 | `tests/test_health_blueprint.py` | 30 | blank line contains whitespace |
| 6975 | W293 | `tests/test_health_blueprint.py` | 27 | blank line contains whitespace |
| 6974 | W293 | `tests/test_health_blueprint.py` | 17 | blank line contains whitespace |
| 6973 | E302 | `tests/test_health_blueprint.py` | 9 | expected 2 blank lines, found 1 |
| 6972 | E305 | `tests/test_feature_flags.py` | 97 | expected 2 blank lines after class or function definition, found 1 |
| 6971 | W293 | `tests/test_feature_flags.py` | 91 | blank line contains whitespace |
| 6970 | W293 | `tests/test_feature_flags.py` | 89 | blank line contains whitespace |
| 6969 | W293 | `tests/test_feature_flags.py` | 82 | blank line contains whitespace |
| 6968 | W293 | `tests/test_feature_flags.py` | 66 | blank line contains whitespace |
| 6967 | W293 | `tests/test_feature_flags.py` | 61 | blank line contains whitespace |
| 6966 | W293 | `tests/test_feature_flags.py` | 55 | blank line contains whitespace |
| 6965 | W293 | `tests/test_feature_flags.py` | 46 | blank line contains whitespace |
| 6964 | W293 | `tests/test_feature_flags.py` | 40 | blank line contains whitespace |
| 6963 | W293 | `tests/test_feature_flags.py` | 33 | blank line contains whitespace |
| 6962 | W293 | `tests/test_feature_flags.py` | 18 | blank line contains whitespace |
| 6961 | W293 | `opt/web/panel/config.py` | 126 | blank line contains whitespace |
| 6960 | W293 | `opt/web/panel/app.py` | 357 | blank line contains whitespace |
| 6959 | W293 | `opt/web/panel/app.py` | 354 | blank line contains whitespace |
| 6958 | W391 | `opt/tracing_integration.py` | 717 | blank line at end of file |
| 6957 | W293 | `opt/services/feature_flags.py` | 73 | blank line contains whitespace |
| 6956 | E305 | `opt/distributed_tracing.py` | 39 | expected 2 blank lines after class or function definition, found 1 |
| 6955 | E302 | `opt/distributed_tracing.py` | 36 | expected 2 blank lines, found 1 |
| 6954 | W293 | `opt/core/config.py` | 60 | blank line contains whitespace |
| 6953 | W293 | `opt/core/config.py` | 56 | blank line contains whitespace |
| 6952 | W293 | `opt/core/config.py` | 53 | blank line contains whitespace |
| 6951 | W293 | `opt/core/config.py` | 24 | blank line contains whitespace |
| 6944 | E305 | `tests/fuzzing/fuzz_validator.py` | 36 | expected 2 blank lines after class or function definition, found 1 |
| 6943 | W293 | `tests/fuzzing/fuzz_validator.py` | 28 | blank line contains whitespace |
| 6942 | W293 | `tests/fuzzing/fuzz_validator.py` | 12 | blank line contains whitespace |
| 6941 | E302 | `tests/fuzzing/fuzz_validator.py` | 10 | expected 2 blank lines, found 1 |
| 6940 | E402 | `tests/fuzzing/fuzz_validator.py` | 8 | module level import not at top of file |
| 6939 | W292 | `opt/web/**init**.py` | 1 | no newline at end of file |
| 6938 | W292 | `opt/tools/**init**.py` | 1 | no newline at end of file |
| 6937 | W292 | `opt/testing/**init**.py` | 1 | no newline at end of file |
| 6936 | W292 | `opt/system/**init**.py` | 1 | no newline at end of file |
| 6935 | W292 | `opt/security/**init**.py` | 1 | no newline at end of file |
| 6934 | W292 | `opt/monitoring/**init**.py` | 1 | no newline at end of file |
| 6933 | W292 | `opt/migrations/**init**.py` | 1 | no newline at end of file |
| 6932 | W292 | `opt/installer/**init**.py` | 1 | no newline at end of file |
| 6931 | W292 | `opt/helpers/**init**.py` | 1 | no newline at end of file |
| 6930 | W292 | `opt/discovery/**init**.py` | 1 | no newline at end of file |
| 6929 | W292 | `opt/deployment/**init**.py` | 1 | no newline at end of file |
| 6928 | W292 | `opt/config/**init**.py` | 1 | no newline at end of file |
| 6927 | W292 | `opt/ansible/**init**.py` | 1 | no newline at end of file |
| 6828 | E305 | `tests/test_licensing.py` | 161 | expected 2 blank lines after class or function definition, found 1 |
| 6827 | W293 | `tests/test_licensing.py` | 157 | blank line contains whitespace |
| 6826 | W293 | `tests/test_licensing.py` | 148 | blank line contains whitespace |
| 6825 | E302 | `tests/test_licensing.py` | 135 | expected 2 blank lines, found 1 |
| 6824 | W293 | `tests/test_licensing.py` | 130 | blank line contains whitespace |
| 6823 | W293 | `tests/test_licensing.py` | 114 | blank line contains whitespace |
| 6822 | E302 | `tests/test_licensing.py` | 107 | expected 2 blank lines, found 1 |
| 6821 | W293 | `tests/test_licensing.py` | 101 | blank line contains whitespace |
| 6820 | E302 | `tests/test_licensing.py` | 76 | expected 2 blank lines, found 1 |
| 6819 | W293 | `tests/test_licensing.py` | 71 | blank line contains whitespace |
| 6818 | W293 | `tests/test_licensing.py` | 55 | blank line contains whitespace |
| 6817 | W293 | `tests/test_licensing.py` | 37 | blank line contains whitespace |
| 6816 | E302 | `tests/test_licensing.py` | 26 | expected 2 blank lines, found 1 |
| 6810 | W293 | `tests/test_backup_manager_encryption.py` | 97 | blank line contains whitespace |
| 6809 | W293 | `tests/test_backup_manager_encryption.py` | 82 | blank line contains whitespace |
| 6808 | E302 | `tests/test_backup_manager_encryption.py` | 77 | expected 2 blank lines, found 1 |
| 6807 | W293 | `tests/test_backup_manager_encryption.py` | 74 | blank line contains whitespace |
| 6806 | W293 | `tests/test_backup_manager_encryption.py` | 57 | blank line contains whitespace |
| 6805 | E302 | `tests/test_backup_manager_encryption.py` | 43 | expected 2 blank lines, found 1 |
| 6804 | W293 | `tests/test_backup_manager_encryption.py` | 39 | blank line contains whitespace |
| 6803 | E302 | `tests/test_backup_manager_encryption.py` | 33 | expected 2 blank lines, found 1 |
| 6802 | E302 | `tests/test_backup_manager_encryption.py` | 25 | expected 2 blank lines, found 1 |
| 6801 | E302 | `tests/test_backup_manager_encryption.py` | 20 | expected 2 blank lines, found 1 |
| 6800 | E302 | `tests/test_backup_manager_encryption.py` | 15 | expected 2 blank lines, found 1 |
| 6799 | W291 | `tests/test_backup_manager_encryption.py` | 11 | trailing whitespace |
| 6798 | W291 | `tests/test_backup_manager_encryption.py` | 10 | trailing whitespace |
| 6794 | E305 | `tests/test_audit_encryption.py` | 115 | expected 2 blank lines after class or function definition, found 1 |
| 6793 | W293 | `tests/test_audit_encryption.py` | 111 | blank line contains whitespace |
| 6792 | W293 | `tests/test_audit_encryption.py` | 102 | blank line contains whitespace |
| 6791 | W293 | `tests/test_audit_encryption.py` | 88 | blank line contains whitespace |
| 6790 | W293 | `tests/test_audit_encryption.py` | 85 | blank line contains whitespace |
| 6789 | W293 | `tests/test_audit_encryption.py` | 81 | blank line contains whitespace |
| 6788 | E261 | `tests/test_audit_encryption.py` | 78 | at least two spaces before inline comment |
| 6787 | W293 | `tests/test_audit_encryption.py` | 68 | blank line contains whitespace |
| 6786 | W293 | `tests/test_audit_encryption.py` | 65 | blank line contains whitespace |
| 6785 | W293 | `tests/test_audit_encryption.py` | 56 | blank line contains whitespace |
| 6784 | E302 | `tests/test_audit_encryption.py` | 45 | expected 2 blank lines, found 1 |
| 6783 | W293 | `tests/test_audit_encryption.py` | 39 | blank line contains whitespace |
| 6782 | W293 | `tests/test_audit_encryption.py` | 36 | blank line contains whitespace |
| 6781 | E302 | `tests/test_audit_encryption.py` | 23 | expected 2 blank lines, found 1 |
| 6775 | E305 | `tests/test_api_key_rotation.py` | 73 | expected 2 blank lines after class or function definition, found 1 |
| 6774 | W293 | `tests/test_api_key_rotation.py` | 69 | blank line contains whitespace |
| 6773 | W293 | `tests/test_api_key_rotation.py` | 60 | blank line contains whitespace |
| 6772 | E302 | `tests/test_api_key_rotation.py` | 39 | expected 2 blank lines, found 1 |
| 6771 | E302 | `tests/test_api_key_rotation.py` | 18 | expected 2 blank lines, found 1 |
| 6761 | E501 | `opt/web/panel/app.py` | 342 | line too long (122 > 120 characters) |
| 6760 | W293 | `opt/web/panel/app.py` | 337 | blank line contains whitespace |
| 6759 | W293 | `opt/web/panel/app.py` | 328 | blank line contains whitespace |
| 6758 | W293 | `opt/web/panel/app.py` | 324 | blank line contains whitespace |
| 6757 | W293 | `opt/services/rpc/server.py` | 475 | blank line contains whitespace |
| 6756 | W293 | `opt/services/rpc/server.py` | 472 | blank line contains whitespace |
| 6755 | W293 | `opt/services/rpc/server.py` | 457 | blank line contains whitespace |
| 6754 | W293 | `opt/services/rpc/audit.py` | 109 | blank line contains whitespace |
| 6753 | W293 | `opt/services/rpc/audit.py` | 91 | blank line contains whitespace |
| 6752 | W291 | `opt/services/rpc/audit.py` | 88 | trailing whitespace |
| 6751 | W291 | `opt/services/rpc/audit.py` | 87 | trailing whitespace |
| 6750 | W293 | `opt/services/rpc/audit.py` | 85 | blank line contains whitespace |
| 6749 | E302 | `opt/services/rpc/audit.py` | 70 | expected 2 blank lines, found 1 |
| 6748 | W293 | `opt/services/rpc/audit.py` | 66 | blank line contains whitespace |
| 6747 | W293 | `opt/services/rpc/audit.py` | 42 | blank line contains whitespace |
| 6746 | W293 | `opt/services/rpc/audit.py` | 37 | blank line contains whitespace |
| 6745 | E302 | `opt/services/rpc/audit.py` | 35 | expected 2 blank lines, found 1 |
| 6744 | W293 | `opt/services/rpc/audit.py` | 26 | blank line contains whitespace |
| 6743 | W293 | `opt/services/rpc/audit.py` | 22 | blank line contains whitespace |
| 6742 | E302 | `opt/services/rpc/audit.py` | 20 | expected 2 blank lines, found 1 |
| 6740 | E302 | `opt/services/anomaly/core.py` | 324 | expected 2 blank lines, found 1 |
| 6739 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 122 | continuation line missing indentation or outdented |
| 6738 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 121 | continuation line missing indentation or outdented |
| 6737 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 120 | continuation line missing indentation or outdented |
| 6736 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 119 | continuation line missing indentation or outdented |
| 6735 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 118 | continuation line missing indentation or outdented |
| 6734 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 117 | continuation line missing indentation or outdented |
| 6733 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 116 | continuation line missing indentation or outdented |
| 6732 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 115 | continuation line missing indentation or outdented |
| 6731 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 114 | continuation line missing indentation or outdented |
| 6730 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 113 | continuation line missing indentation or outdented |
| 6729 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 112 | continuation line missing indentation or outdented |
| 6728 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 111 | continuation line missing indentation or outdented |
| 6727 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 110 | continuation line missing indentation or outdented |
| 6726 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 109 | continuation line missing indentation or outdented |
| 6725 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 108 | continuation line missing indentation or outdented |
| 6724 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 107 | continuation line missing indentation or outdented |
| 6723 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 106 | continuation line missing indentation or outdented |
| 6722 | E128 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 105 | continuation line under-indented for visual indent |
| 6721 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 94 | continuation line missing indentation or outdented |
| 6720 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 93 | continuation line missing indentation or outdented |
| 6719 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 92 | continuation line missing indentation or outdented |
| 6718 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 91 | continuation line missing indentation or outdented |
| 6717 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 90 | continuation line missing indentation or outdented |
| 6716 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 89 | continuation line missing indentation or outdented |
| 6715 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 88 | continuation line missing indentation or outdented |
| 6714 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 87 | continuation line missing indentation or outdented |
| 6713 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 86 | continuation line missing indentation or outdented |
| 6712 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 85 | continuation line missing indentation or outdented |
| 6711 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 84 | continuation line missing indentation or outdented |
| 6710 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 83 | continuation line missing indentation or outdented |
| 6709 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 82 | continuation line missing indentation or outdented |
| 6708 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 81 | continuation line missing indentation or outdented |
| 6707 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 80 | continuation line missing indentation or outdented |
| 6706 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 79 | continuation line missing indentation or outdented |
| 6705 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 78 | continuation line missing indentation or outdented |
| 6704 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 77 | continuation line missing indentation or outdented |
| 6703 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 76 | continuation line missing indentation or outdented |
| 6702 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 75 | continuation line missing indentation or outdented |
| 6701 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 74 | continuation line missing indentation or outdented |
| 6700 | E128 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 73 | continuation line under-indented for visual indent |
| 6699 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 63 | continuation line missing indentation or outdented |
| 6698 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 62 | continuation line missing indentation or outdented |
| 6697 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 61 | continuation line missing indentation or outdented |
| 6696 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 60 | continuation line missing indentation or outdented |
| 6695 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 59 | continuation line missing indentation or outdented |
| 6694 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 58 | continuation line missing indentation or outdented |
| 6693 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 57 | continuation line missing indentation or outdented |
| 6692 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 56 | continuation line missing indentation or outdented |
| 6691 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 55 | continuation line missing indentation or outdented |
| 6690 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 54 | continuation line missing indentation or outdented |
| 6689 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 53 | continuation line missing indentation or outdented |
| 6688 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 52 | continuation line missing indentation or outdented |
| 6687 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 51 | continuation line missing indentation or outdented |
| 6686 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 50 | continuation line missing indentation or outdented |
| 6685 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 49 | continuation line missing indentation or outdented |
| 6684 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 48 | continuation line missing indentation or outdented |
| 6683 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 47 | continuation line missing indentation or outdented |
| 6682 | E128 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 46 | continuation line under-indented for visual indent |
| 6681 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 37 | continuation line missing indentation or outdented |
| 6680 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 36 | continuation line missing indentation or outdented |
| 6679 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 35 | continuation line missing indentation or outdented |
| 6678 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 34 | continuation line missing indentation or outdented |
| 6677 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 33 | continuation line missing indentation or outdented |
| 6676 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 32 | continuation line missing indentation or outdented |
| 6675 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 31 | continuation line missing indentation or outdented |
| 6674 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 30 | continuation line missing indentation or outdented |
| 6673 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 29 | continuation line missing indentation or outdented |
| 6672 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 28 | continuation line missing indentation or outdented |
| 6671 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 27 | continuation line missing indentation or outdented |
| 6670 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 26 | continuation line missing indentation or outdented |
| 6669 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 25 | continuation line missing indentation or outdented |
| 6668 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 24 | continuation line missing indentation or outdented |
| 6667 | E122 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 23 | continuation line missing indentation or outdented |
| 6666 | E128 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 22 | continuation line under-indented for visual indent |
| 6665 | W291 | `opt/migrations/versions/4dd17a47cb28_initial_migration.py` | 4 | trailing whitespace |
| 6664 | E301 | `opt/core/config.py` | 99 | expected 1 blank line, found 0 |
| 6663 | E305 | `opt/core/config.py` | 89 | expected 2 blank lines after class or function definition, found 1 |
| 6662 | W293 | `opt/core/config.py` | 41 | blank line contains whitespace |
| 6661 | W293 | `opt/core/config.py` | 37 | blank line contains whitespace |
| 6654 | W293 | `tests/test_api_versioning.py` | 558 | blank line contains whitespace |
| 6653 | E305 | `tests/manual_test_logging.py` | 30 | expected 2 blank lines after class or function definition, found 1 |
| 6652 | W293 | `tests/manual_test_logging.py` | 23 | blank line contains whitespace |
| 6651 | W293 | `tests/manual_test_logging.py` | 19 | blank line contains whitespace |
| 6650 | W293 | `tests/manual_test_logging.py` | 16 | blank line contains whitespace |
| 6649 | W293 | `tests/manual_test_logging.py` | 14 | blank line contains whitespace |
| 6648 | E302 | `tests/manual_test_logging.py` | 12 | expected 2 blank lines, found 1 |
| 6647 | E402 | `tests/manual_test_logging.py` | 10 | module level import not at top of file |
| 6646 | E303 | `opt/web/panel/routes/storage.py` | 23 | too many blank lines (3) |
| 6642 | W293 | `opt/web/panel/routes/passthrough.py` | 470 | blank line contains whitespace |
| 6641 | W293 | `opt/web/panel/routes/passthrough.py` | 459 | blank line contains whitespace |
| 6640 | W293 | `opt/web/panel/routes/passthrough.py` | 410 | blank line contains whitespace |
| 6639 | W293 | `opt/web/panel/routes/passthrough.py` | 399 | blank line contains whitespace |
| 6638 | E303 | `opt/web/panel/routes/nodes.py` | 21 | too many blank lines (3) |
| 6636 | E303 | `opt/web/panel/routes/auth.py` | 25 | too many blank lines (3) |
| 6634 | W293 | `opt/web/panel/graceful_shutdown.py` | 515 | blank line contains whitespace |
| 6633 | W293 | `opt/testing/test_phase4_week4.py` | 607 | blank line contains whitespace |
| 6631 | W293 | `opt/testing/test_phase4_week4.py` | 599 | blank line contains whitespace |
| 6629 | W293 | `opt/testing/test_phase4_week4.py` | 591 | blank line contains whitespace |
| 6628 | W293 | `opt/testing/test_phase4_week4.py` | 579 | blank line contains whitespace |
| 6627 | W293 | `opt/testing/test_phase4_week4.py` | 567 | blank line contains whitespace |
| 6626 | W293 | `opt/testing/test_phase4_week4.py` | 564 | blank line contains whitespace |
| 6625 | W293 | `opt/testing/test_phase4_week4.py` | 553 | blank line contains whitespace |
| 6624 | W293 | `opt/testing/test_phase4_week4.py` | 545 | blank line contains whitespace |
| 6623 | W293 | `opt/testing/test_phase4_week4.py` | 540 | blank line contains whitespace |
| 6622 | W293 | `opt/testing/test_phase4_week4.py` | 528 | blank line contains whitespace |
| 6621 | W293 | `opt/testing/test_phase4_week4.py` | 520 | blank line contains whitespace |
| 6620 | W293 | `opt/testing/test_phase4_week4.py` | 516 | blank line contains whitespace |
| 6619 | W293 | `opt/testing/test_phase4_week4.py` | 492 | blank line contains whitespace |
| 6618 | W293 | `opt/testing/test_phase4_week4.py` | 485 | blank line contains whitespace |
| 6617 | W293 | `opt/testing/test_phase4_week4.py` | 477 | blank line contains whitespace |
| 6616 | W293 | `opt/testing/test_phase4_week4.py` | 468 | blank line contains whitespace |
| 6615 | W293 | `opt/testing/test_phase4_week4.py` | 454 | blank line contains whitespace |
| 6614 | W293 | `opt/testing/test_phase4_week4.py` | 451 | blank line contains whitespace |
| 6613 | W293 | `opt/testing/test_phase4_week4.py` | 443 | blank line contains whitespace |
| 6612 | W293 | `opt/testing/test_phase4_week4.py` | 439 | blank line contains whitespace |
| 6611 | W293 | `opt/testing/test_phase4_week4.py` | 432 | blank line contains whitespace |
| 6610 | W293 | `opt/testing/test_phase4_week4.py` | 424 | blank line contains whitespace |
| 6609 | W293 | `opt/testing/test_phase4_week4.py` | 419 | blank line contains whitespace |
| 6608 | W293 | `opt/testing/test_phase4_week4.py` | 405 | blank line contains whitespace |
| 6607 | W293 | `opt/testing/test_phase4_week4.py` | 398 | blank line contains whitespace |
| 6606 | W293 | `opt/testing/test_phase4_week4.py` | 389 | blank line contains whitespace |
| 6605 | W293 | `opt/testing/test_phase4_week4.py` | 386 | blank line contains whitespace |
| 6604 | W293 | `opt/testing/test_phase4_week4.py` | 377 | blank line contains whitespace |
| 6603 | W293 | `opt/testing/test_phase4_week4.py` | 373 | blank line contains whitespace |
| 6602 | W293 | `opt/testing/test_phase4_week4.py` | 364 | blank line contains whitespace |
| 6601 | W293 | `opt/testing/test_phase4_week4.py` | 361 | blank line contains whitespace |
| 6600 | W293 | `opt/testing/test_phase4_week4.py` | 353 | blank line contains whitespace |
| 6599 | W293 | `opt/testing/test_phase4_week4.py` | 350 | blank line contains whitespace |
| 6598 | W293 | `opt/testing/test_phase4_week4.py` | 340 | blank line contains whitespace |
| 6597 | W293 | `opt/testing/test_phase4_week4.py` | 337 | blank line contains whitespace |
| 6596 | W293 | `opt/testing/test_phase4_week4.py` | 329 | blank line contains whitespace |
| 6595 | W293 | `opt/testing/test_phase4_week4.py` | 326 | blank line contains whitespace |
| 6594 | W293 | `opt/testing/test_phase4_week4.py` | 318 | blank line contains whitespace |
| 6593 | W293 | `opt/testing/test_phase4_week4.py` | 315 | blank line contains whitespace |
| 6592 | W293 | `opt/testing/test_phase4_week4.py` | 303 | blank line contains whitespace |
| 6591 | W293 | `opt/testing/test_phase4_week4.py` | 300 | blank line contains whitespace |
| 6590 | W293 | `opt/testing/test_phase4_week4.py` | 292 | blank line contains whitespace |
| 6589 | W293 | `opt/testing/test_phase4_week4.py` | 284 | blank line contains whitespace |
| 6588 | W293 | `opt/testing/test_phase4_week4.py` | 282 | blank line contains whitespace |
| 6587 | W293 | `opt/testing/test_phase4_week4.py` | 272 | blank line contains whitespace |
| 6586 | W293 | `opt/testing/test_phase4_week4.py` | 270 | blank line contains whitespace |
| 6585 | W293 | `opt/testing/test_phase4_week4.py` | 260 | blank line contains whitespace |
| 6584 | W293 | `opt/testing/test_phase4_week4.py` | 248 | blank line contains whitespace |
| 6583 | W293 | `opt/testing/test_phase4_week4.py` | 245 | blank line contains whitespace |
| 6582 | E306 | `opt/testing/test_phase4_week4.py` | 242 | expected 1 blank line before a nested definition, found 0 |
| 6581 | W293 | `opt/testing/test_phase4_week4.py` | 237 | blank line contains whitespace |
| 6580 | W293 | `opt/testing/test_phase4_week4.py` | 230 | blank line contains whitespace |
| 6579 | W293 | `opt/testing/test_phase4_week4.py` | 226 | blank line contains whitespace |
| 6578 | W293 | `opt/testing/test_phase4_week4.py` | 217 | blank line contains whitespace |
| 6577 | W293 | `opt/testing/test_phase4_week4.py` | 213 | blank line contains whitespace |
| 6576 | W293 | `opt/testing/test_phase4_week4.py` | 199 | blank line contains whitespace |
| 6575 | W293 | `opt/testing/test_phase4_week4.py` | 188 | blank line contains whitespace |
| 6574 | W293 | `opt/testing/test_phase4_week4.py` | 185 | blank line contains whitespace |
| 6573 | W293 | `opt/testing/test_phase4_week4.py` | 178 | blank line contains whitespace |
| 6572 | W293 | `opt/testing/test_phase4_week4.py` | 168 | blank line contains whitespace |
| 6571 | W293 | `opt/testing/test_phase4_week4.py` | 165 | blank line contains whitespace |
| 6570 | W293 | `opt/testing/test_phase4_week4.py` | 157 | blank line contains whitespace |
| 6569 | W293 | `opt/testing/test_phase4_week4.py` | 154 | blank line contains whitespace |
| 6568 | W293 | `opt/testing/test_phase4_week4.py` | 146 | blank line contains whitespace |
| 6567 | W293 | `opt/testing/test_phase4_week4.py` | 142 | blank line contains whitespace |
| 6566 | W293 | `opt/testing/test_phase4_week4.py` | 135 | blank line contains whitespace |
| 6565 | W293 | `opt/testing/test_phase4_week4.py` | 131 | blank line contains whitespace |
| 6564 | W293 | `opt/testing/test_phase4_week4.py` | 119 | blank line contains whitespace |
| 6563 | W293 | `opt/testing/test_phase4_week4.py` | 113 | blank line contains whitespace |
| 6562 | W293 | `opt/testing/test_phase4_week4.py` | 105 | blank line contains whitespace |
| 6561 | W293 | `opt/testing/test_phase4_week4.py` | 100 | blank line contains whitespace |
| 6560 | W293 | `opt/testing/test_phase4_week4.py` | 92 | blank line contains whitespace |
| 6559 | W293 | `opt/testing/test_phase4_week4.py` | 87 | blank line contains whitespace |
| 6558 | W293 | `opt/testing/test_phase4_week4.py` | 83 | blank line contains whitespace |
| 6557 | W293 | `opt/testing/test_phase4_week4.py` | 80 | blank line contains whitespace |
| 6556 | W293 | `opt/testing/test_phase4_week4.py` | 70 | blank line contains whitespace |
| 6555 | W293 | `opt/testing/test_phase4_week4.py` | 66 | blank line contains whitespace |
| 6554 | W293 | `opt/testing/test_phase4_week4.py` | 62 | blank line contains whitespace |
| 6553 | W293 | `opt/testing/test_phase4_week4.py` | 52 | blank line contains whitespace |
| 6552 | W293 | `opt/testing/test_phase4_week4.py` | 49 | blank line contains whitespace |
| 6551 | W293 | `opt/testing/test_phase4_week4.py` | 38 | blank line contains whitespace |
| 6550 | W293 | `opt/testing/test_phase4_week4.py` | 34 | blank line contains whitespace |
| 6548 | W293 | `opt/services/tracing.py` | 632 | blank line contains whitespace |
| 6547 | W293 | `opt/services/tracing.py` | 629 | blank line contains whitespace |
| 6546 | W293 | `opt/services/tracing.py` | 626 | blank line contains whitespace |
| 6545 | W293 | `opt/services/tracing.py` | 622 | blank line contains whitespace |
| 6544 | W293 | `opt/services/tracing.py` | 619 | blank line contains whitespace |
| 6543 | W293 | `opt/services/tracing.py` | 613 | blank line contains whitespace |
| 6542 | W293 | `opt/services/tracing.py` | 609 | blank line contains whitespace |
| 6541 | E501 | `opt/services/tracing.py` | 607 | line too long (148 > 120 characters) |
| 6540 | W293 | `opt/services/tracing.py` | 605 | blank line contains whitespace |
| 6539 | W293 | `opt/services/tracing.py` | 601 | blank line contains whitespace |
| 6538 | W293 | `opt/services/tracing.py` | 598 | blank line contains whitespace |
| 6537 | W293 | `opt/services/tracing.py` | 595 | blank line contains whitespace |
| 6536 | W293 | `opt/services/tracing.py` | 590 | blank line contains whitespace |
| 6535 | W293 | `opt/services/tracing.py` | 579 | blank line contains whitespace |
| 6534 | W291 | `opt/services/tracing.py` | 566 | trailing whitespace |
| 6533 | W291 | `opt/services/tracing.py` | 565 | trailing whitespace |
| 6532 | W293 | `opt/services/tracing.py` | 557 | blank line contains whitespace |
| 6531 | W293 | `opt/services/tracing.py` | 383 | blank line contains whitespace |
| 6530 | E712 | `opt/services/tracing.py` | 381 | comparison to True should be 'if cond is True:' or 'if cond:' |
| 6529 | W293 | `opt/services/tracing.py` | 365 | blank line contains whitespace |
| 6528 | E501 | `opt/services/security/firewall_manager.py` | 650 | line too long (126 > 120 characters) |
| 6527 | W293 | `opt/services/scheduler/core.py` | 316 | blank line contains whitespace |
| 6526 | W293 | `opt/services/scheduler/core.py` | 313 | blank line contains whitespace |
| 6525 | W293 | `opt/services/scheduler/api.py` | 503 | blank line contains whitespace |
| 6524 | W293 | `opt/services/scheduler/api.py` | 500 | blank line contains whitespace |
| 6523 | W293 | `opt/services/compliance/core.py` | 197 | blank line contains whitespace |
| 6522 | W293 | `opt/services/compliance/core.py` | 146 | blank line contains whitespace |
| 6521 | W293 | `opt/services/compliance/core.py` | 113 | blank line contains whitespace |
| 6520 | W293 | `opt/services/compliance/core.py` | 102 | blank line contains whitespace |
| 6519 | W293 | `opt/services/backup_manager.py` | 414 | blank line contains whitespace |
| 6518 | W293 | `opt/services/backup_manager.py` | 410 | blank line contains whitespace |
| 6517 | W293 | `opt/services/backup_manager.py` | 187 | blank line contains whitespace |
| 6516 | W293 | `opt/services/backup_manager.py` | 184 | blank line contains whitespace |
| 6515 | W293 | `opt/services/backup_manager.py` | 176 | blank line contains whitespace |
| 6514 | W293 | `opt/services/backup_manager.py` | 174 | blank line contains whitespace |
| 6513 | W293 | `opt/services/backup_manager.py` | 168 | blank line contains whitespace |
| 6512 | W293 | `opt/services/backup_manager.py` | 165 | blank line contains whitespace |
| 6511 | W293 | `opt/services/backup_manager.py` | 148 | blank line contains whitespace |
| 6510 | W293 | `opt/services/backup_manager.py` | 146 | blank line contains whitespace |
| 6509 | W293 | `opt/services/backup_manager.py` | 139 | blank line contains whitespace |
| 6508 | W293 | `opt/services/backup_manager.py` | 135 | blank line contains whitespace |
| 6507 | W293 | `opt/services/backup_manager.py` | 130 | blank line contains whitespace |
| 6506 | W293 | `opt/services/backup_manager.py` | 125 | blank line contains whitespace |
| 6505 | W293 | `opt/services/backup_manager.py` | 123 | blank line contains whitespace |
| 6504 | W293 | `opt/services/backup_manager.py` | 115 | blank line contains whitespace |
| 6503 | W293 | `opt/services/backup_manager.py` | 111 | blank line contains whitespace |
| 6502 | W293 | `opt/services/backup_manager.py` | 100 | blank line contains whitespace |
| 6501 | W293 | `opt/services/backup_manager.py` | 75 | blank line contains whitespace |
| 6500 | E999 | `opt/services/backup/dedup_backup_service.py` | 273 | IndentationError: expected an indented block after 'while' statement on line 272 |
| 6499 | W293 | `opt/services/anomaly/core.py` | 1047 | blank line contains whitespace |
| 6498 | W293 | `opt/services/anomaly/core.py` | 354 | blank line contains whitespace |
| 6496 | W293 | `opt/netcfg_tui_app.py` | 220 | blank line contains whitespace |
| 6495 | W293 | `opt/netcfg_tui_app.py` | 218 | blank line contains whitespace |
| 6494 | E117 | `opt/netcfg_tui_app.py` | 209 | over-indented |
| 6493 | E111 | `opt/netcfg_tui_app.py` | 209 | indentation is not a multiple of 4 |
| 6492 | W293 | `opt/netcfg_tui_app.py` | 169 | blank line contains whitespace |
| 6491 | W293 | `opt/netcfg_tui_app.py` | 165 | blank line contains whitespace |
| 6490 | W293 | `opt/netcfg_tui_app.py` | 163 | blank line contains whitespace |
| 6489 | W293 | `opt/netcfg_tui_app.py` | 159 | blank line contains whitespace |
| 6488 | W293 | `opt/netcfg_tui_app.py` | 109 | blank line contains whitespace |
| 6487 | W293 | `opt/netcfg_tui_app.py` | 84 | blank line contains whitespace |
| 6485 | E122 | `opt/core/unified_backend.py` | 603 | continuation line missing indentation or outdented |
| 6484 | E117 | `opt/core/unified_backend.py` | 593 | over-indented |
| 6483 | E111 | `opt/core/unified_backend.py` | 593 | indentation is not a multiple of 4 |
| 6482 | W293 | `opt/core/unified_backend.py` | 576 | blank line contains whitespace |
| 6481 | W293 | `opt/core/unified_backend.py` | 256 | blank line contains whitespace |
| 6480 | W293 | `opt/core/unified_backend.py` | 245 | blank line contains whitespace |
| 6479 | W391 | `opt/core/logging.py` | 122 | blank line at end of file |
| 6478 | W293 | `opt/core/logging.py` | 118 | blank line contains whitespace |
| 6477 | W293 | `opt/core/logging.py` | 115 | blank line contains whitespace |
| 6476 | W293 | `opt/core/logging.py` | 111 | blank line contains whitespace |
| 6475 | W293 | `opt/core/logging.py` | 108 | blank line contains whitespace |
| 6474 | W293 | `opt/core/logging.py` | 102 | blank line contains whitespace |
| 6473 | W293 | `opt/core/logging.py` | 95 | blank line contains whitespace |
| 6472 | W293 | `opt/core/logging.py` | 57 | blank line contains whitespace |
| 6471 | W293 | `opt/core/logging.py` | 53 | blank line contains whitespace |
| 6470 | W291 | `opt/core/logging.py` | 50 | trailing whitespace |
| 6469 | W291 | `opt/core/logging.py` | 48 | trailing whitespace |
| 6466 | W293 | `opt/core/cli_utils.py` | 42 | blank line contains whitespace |
| 6465 | W293 | `opt/core/cli_utils.py` | 37 | blank line contains whitespace |
| 6463 | E302 | `opt/core/audit.py` | 129 | expected 2 blank lines, found 1 |
| 6462 | E305 | `opt/core/audit.py` | 127 | expected 2 blank lines after class or function definition, found 1 |
| 6461 | W293 | `opt/core/audit.py` | 122 | blank line contains whitespace |
| 6460 | W293 | `opt/core/audit.py` | 56 | blank line contains whitespace |
| 6459 | E302 | `opt/core/audit.py` | 20 | expected 2 blank lines, found 1 |
| 6375 | E303 | `opt/netcfg_tui_app.py` | 231 | too many blank lines (2) |
| 6374 | W293 | `opt/netcfg_tui_app.py` | 227 | blank line contains whitespace |
| 6373 | W293 | `opt/netcfg_tui_app.py` | 181 | blank line contains whitespace |
| 6372 | W293 | `opt/netcfg_tui_app.py` | 167 | blank line contains whitespace |
| 6371 | E261 | `opt/netcfg_tui_app.py` | 156 | at least two spaces before inline comment |
| 6370 | W293 | `opt/netcfg_tui_app.py` | 147 | blank line contains whitespace |
| 6369 | W293 | `opt/netcfg_tui_app.py` | 143 | blank line contains whitespace |
| 6368 | W293 | `opt/netcfg_tui_app.py` | 139 | blank line contains whitespace |
| 6367 | W293 | `opt/netcfg_tui_app.py` | 137 | blank line contains whitespace |
| 6366 | W293 | `opt/netcfg_tui_app.py` | 117 | blank line contains whitespace |
| 6365 | W293 | `opt/netcfg_tui_app.py` | 113 | blank line contains whitespace |
| 6364 | W293 | `opt/netcfg_tui_app.py` | 81 | blank line contains whitespace |
| 6363 | W293 | `opt/netcfg_tui_app.py` | 60 | blank line contains whitespace |
| 6361 | W293 | `opt/distributed_tracing.py` | 234 | blank line contains whitespace |
| 6360 | W293 | `opt/distributed_tracing.py` | 195 | blank line contains whitespace |
| 6359 | W293 | `opt/distributed_tracing.py` | 187 | blank line contains whitespace |
| 6358 | W293 | `opt/distributed_tracing.py` | 181 | blank line contains whitespace |
| 6357 | W293 | `opt/distributed_tracing.py` | 154 | blank line contains whitespace |
| 6356 | W293 | `opt/distributed_tracing.py` | 143 | blank line contains whitespace |
| 6280 | E305 | `opt/system/upgrade_manager.py` | 85 | expected 2 blank lines after class or function definition, found 1 |
| 6279 | W293 | `opt/system/upgrade_manager.py` | 77 | blank line contains whitespace |
| 6278 | W293 | `opt/system/upgrade_manager.py` | 74 | blank line contains whitespace |
| 6277 | W293 | `opt/system/upgrade_manager.py` | 61 | blank line contains whitespace |
| 6276 | W293 | `opt/system/upgrade_manager.py` | 59 | blank line contains whitespace |
| 6275 | W293 | `opt/system/upgrade_manager.py` | 56 | blank line contains whitespace |
| 6273 | W293 | `opt/system/upgrade_manager.py` | 52 | blank line contains whitespace |
| 6272 | W293 | `opt/system/upgrade_manager.py` | 49 | blank line contains whitespace |
| 6271 | W293 | `opt/system/upgrade_manager.py` | 20 | blank line contains whitespace |
| 6270 | E302 | `opt/system/upgrade_manager.py` | 16 | expected 2 blank lines, found 1 |
| 6266 | E305 | `opt/security/ssh_hardener.py` | 108 | expected 2 blank lines after class or function definition, found 1 |
| 6265 | W293 | `opt/security/ssh_hardener.py` | 103 | blank line contains whitespace |
| 6264 | E302 | `opt/security/ssh_hardener.py` | 99 | expected 2 blank lines, found 1 |
| 6263 | E302 | `opt/security/ssh_hardener.py` | 82 | expected 2 blank lines, found 1 |
| 6262 | W293 | `opt/security/ssh_hardener.py` | 60 | blank line contains whitespace |
| 6261 | W293 | `opt/security/ssh_hardener.py` | 57 | blank line contains whitespace |
| 6260 | W293 | `opt/security/ssh_hardener.py` | 48 | blank line contains whitespace |
| 6259 | E261 | `opt/security/ssh_hardener.py` | 43 | at least two spaces before inline comment |
| 6258 | E302 | `opt/security/ssh_hardener.py` | 31 | expected 2 blank lines, found 1 |
| 6257 | E302 | `opt/security/ssh_hardener.py` | 23 | expected 2 blank lines, found 1 |
| 6256 | W293 | `opt/dvctl.py` | 243 | blank line contains whitespace |
| 6255 | W293 | `opt/dvctl.py` | 237 | blank line contains whitespace |
| 6254 | W293 | `opt/dvctl.py` | 206 | blank line contains whitespace |
| 6253 | W293 | `opt/dvctl.py` | 152 | blank line contains whitespace |
| 6252 | W293 | `opt/dvctl.py` | 122 | blank line contains whitespace |
| 6251 | W293 | `opt/dvctl.py` | 119 | blank line contains whitespace |
| 6250 | W293 | `opt/dvctl.py` | 116 | blank line contains whitespace |
| 6249 | W293 | `opt/dvctl.py` | 113 | blank line contains whitespace |
| 6248 | E302 | `opt/dvctl.py` | 102 | expected 2 blank lines, found 1 |
| 6247 | W293 | `opt/dvctl.py` | 89 | blank line contains whitespace |
| 6246 | W293 | `opt/dvctl.py` | 84 | blank line contains whitespace |
| 6245 | W293 | `opt/dvctl.py` | 66 | blank line contains whitespace |
| 6244 | E302 | `opt/dvctl.py` | 33 | expected 2 blank lines, found 1 |
| 6239 | W293 | `opt/discovery/zerotouch.py` | 123 | blank line contains whitespace |
| 6238 | W293 | `opt/discovery/zerotouch.py` | 121 | blank line contains whitespace |
| 6237 | W293 | `opt/discovery/zerotouch.py` | 118 | blank line contains whitespace |
| 6236 | W293 | `opt/discovery/zerotouch.py` | 115 | blank line contains whitespace |
| 6235 | E305 | `opt/discovery/zerotouch.py` | 111 | expected 2 blank lines after class or function definition, found 1 |
| 6234 | E302 | `opt/discovery/zerotouch.py` | 98 | expected 2 blank lines, found 1 |
| 6233 | W293 | `opt/discovery/zerotouch.py` | 94 | blank line contains whitespace |
| 6232 | W293 | `opt/discovery/zerotouch.py` | 91 | blank line contains whitespace |
| 6230 | E302 | `opt/discovery/zerotouch.py` | 86 | expected 2 blank lines, found 1 |
| 6229 | W293 | `opt/discovery/zerotouch.py` | 75 | blank line contains whitespace |
| 6228 | E261 | `opt/discovery/zerotouch.py` | 67 | at least two spaces before inline comment |
| 6227 | W293 | `opt/discovery/zerotouch.py` | 62 | blank line contains whitespace |
| 6226 | W293 | `opt/discovery/zerotouch.py` | 60 | blank line contains whitespace |
| 6225 | E302 | `opt/discovery/zerotouch.py` | 56 | expected 2 blank lines, found 1 |
| 6224 | W293 | `opt/discovery/zerotouch.py` | 42 | blank line contains whitespace |
| 6223 | E302 | `opt/discovery/zerotouch.py` | 26 | expected 2 blank lines, found 1 |
| 6221 | E402 | `tests/test_netcfg_mock.py` | 36 | module level import not at top of file |
| 6220 | E402 | `tests/test_netcfg_mock.py` | 35 | module level import not at top of file |
| 6219 | E402 | `tests/test_netcfg_mock.py` | 22 | module level import not at top of file |
| 6218 | E501 | `opt/tools/first_boot_keygen.py` | 67 | line too long (126 > 120 characters) |
| 6217 | E305 | `opt/dvctl.py` | 117 | expected 2 blank lines after class or function definition, found 1 |
| 6216 | W293 | `opt/dvctl.py` | 101 | blank line contains whitespace |
| 6215 | W293 | `opt/dvctl.py` | 99 | blank line contains whitespace |
| 6214 | W293 | `opt/dvctl.py` | 210 | blank line contains whitespace |
| 6213 | W293 | `opt/dvctl.py` | 82 | blank line contains whitespace |
| 6212 | W293 | `opt/dvctl.py` | 202 | blank line contains whitespace |
| 6211 | W293 | `opt/dvctl.py` | 200 | blank line contains whitespace |
| 6210 | E302 | `opt/dvctl.py` | 197 | expected 2 blank lines, found 1 |
| 6209 | W293 | `opt/dvctl.py` | 51 | blank line contains whitespace |
| 6208 | W293 | `opt/dvctl.py` | 47 | blank line contains whitespace |
| 6207 | W293 | `opt/dvctl.py` | 43 | blank line contains whitespace |
| 6206 | W293 | `opt/dvctl.py` | 39 | blank line contains whitespace |
| 6205 | E302 | `opt/dvctl.py` | 29 | expected 2 blank lines, found 1 |
| 5758 | E301 | `opt/web/panel/core/rpc_client.py` | 397 | expected 1 blank line, found 0 |
| 5757 | E303 | `opt/web/panel/core/rpc_client.py` | 395 | too many blank lines (3) |
| 5753 | E501 | `opt/web/panel/api_versioning.py` | 495 | line too long (151 > 120 characters) |
| 5752 | E501 | `opt/web/panel/api_versioning.py` | 420 | line too long (167 > 120 characters) |
| 5738 | E501 | `opt/services/reporting_scheduler.py` | 373 | line too long (125 > 120 characters) |
| 5737 | E501 | `opt/services/rbac/fine_grained_rbac.py` | 344 | line too long (131 > 120 characters) |
| 5732 | E131 | `opt/services/backup/dedup_backup_service.py` | 509 | continuation line unaligned for hanging indent |
| 5727 | W293 | `opt/services/network/multitenant_network.py` | 216 | blank line contains whitespace |
| 5726 | W293 | `opt/services/network/multitenant_network.py` | 209 | blank line contains whitespace |
| 5718 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1071 | blank line contains whitespace |
| 5717 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1069 | blank line contains whitespace |
| 5716 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1064 | blank line contains whitespace |
| 5715 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1062 | blank line contains whitespace |
| 5714 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1059 | blank line contains whitespace |
| 5713 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1056 | blank line contains whitespace |
| 5712 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1050 | blank line contains whitespace |
| 5711 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1047 | blank line contains whitespace |
| 5710 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1041 | blank line contains whitespace |
| 5709 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1033 | blank line contains whitespace |
| 5708 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1028 | blank line contains whitespace |
| 5707 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1019 | blank line contains whitespace |
| 5706 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1014 | blank line contains whitespace |
| 5705 | W293 | `opt/services/multiregion/replication_scheduler.py` | 1000 | blank line contains whitespace |
| 5704 | W293 | `opt/services/multiregion/replication_scheduler.py` | 995 | blank line contains whitespace |
| 5703 | W293 | `opt/services/multiregion/replication_scheduler.py` | 993 | blank line contains whitespace |
| 5702 | W293 | `opt/services/multiregion/replication_scheduler.py` | 970 | blank line contains whitespace |
| 5701 | W293 | `opt/services/multiregion/replication_scheduler.py` | 954 | blank line contains whitespace |
| 5700 | W293 | `opt/services/multiregion/replication_scheduler.py` | 950 | blank line contains whitespace |
| 5699 | W293 | `opt/services/multiregion/replication_scheduler.py` | 946 | blank line contains whitespace |
| 5698 | W293 | `opt/services/multiregion/replication_scheduler.py` | 942 | blank line contains whitespace |
| 5697 | W293 | `opt/services/multiregion/replication_scheduler.py` | 938 | blank line contains whitespace |
| 5696 | W293 | `opt/services/multiregion/replication_scheduler.py` | 934 | blank line contains whitespace |
| 5695 | W293 | `opt/services/multiregion/replication_scheduler.py` | 928 | blank line contains whitespace |
| 5694 | W293 | `opt/services/multiregion/replication_scheduler.py` | 926 | blank line contains whitespace |
| 5693 | W293 | `opt/services/multiregion/replication_scheduler.py` | 918 | blank line contains whitespace |
| 5692 | W293 | `opt/services/multiregion/replication_scheduler.py` | 913 | blank line contains whitespace |
| 5691 | W293 | `opt/services/multiregion/replication_scheduler.py` | 911 | blank line contains whitespace |
| 5690 | W293 | `opt/services/multiregion/replication_scheduler.py` | 907 | blank line contains whitespace |
| 5689 | W293 | `opt/services/multiregion/replication_scheduler.py` | 903 | blank line contains whitespace |
| 5688 | W293 | `opt/services/multiregion/replication_scheduler.py` | 899 | blank line contains whitespace |
| 5687 | W293 | `opt/services/multiregion/replication_scheduler.py` | 893 | blank line contains whitespace |
| 5686 | W293 | `opt/services/multiregion/replication_scheduler.py` | 891 | blank line contains whitespace |
| 5685 | W293 | `opt/services/multiregion/replication_scheduler.py` | 883 | blank line contains whitespace |
| 5684 | W293 | `opt/services/multiregion/replication_scheduler.py` | 877 | blank line contains whitespace |
| 5683 | W293 | `opt/services/multiregion/replication_scheduler.py` | 872 | blank line contains whitespace |
| 5682 | W293 | `opt/services/multiregion/replication_scheduler.py` | 865 | blank line contains whitespace |
| 5681 | W293 | `opt/services/multiregion/replication_scheduler.py` | 857 | blank line contains whitespace |
| 5680 | W293 | `opt/services/multiregion/replication_scheduler.py` | 851 | blank line contains whitespace |
| 5679 | W293 | `opt/services/multiregion/replication_scheduler.py` | 849 | blank line contains whitespace |
| 5678 | W293 | `opt/services/multiregion/replication_scheduler.py` | 842 | blank line contains whitespace |
| 5677 | W293 | `opt/services/multiregion/replication_scheduler.py` | 835 | blank line contains whitespace |
| 5676 | W293 | `opt/services/multiregion/replication_scheduler.py` | 828 | blank line contains whitespace |
| 5675 | W293 | `opt/services/multiregion/replication_scheduler.py` | 824 | blank line contains whitespace |
| 5674 | W293 | `opt/services/multiregion/replication_scheduler.py` | 822 | blank line contains whitespace |
| 5673 | W293 | `opt/services/multiregion/replication_scheduler.py` | 819 | blank line contains whitespace |
| 5672 | W293 | `opt/services/multiregion/replication_scheduler.py` | 816 | blank line contains whitespace |
| 5671 | W293 | `opt/services/multiregion/replication_scheduler.py` | 813 | blank line contains whitespace |
| 5670 | W293 | `opt/services/multiregion/replication_scheduler.py` | 811 | blank line contains whitespace |
| 5669 | W293 | `opt/services/multiregion/replication_scheduler.py` | 806 | blank line contains whitespace |
| 5668 | W293 | `opt/services/multiregion/replication_scheduler.py` | 802 | blank line contains whitespace |
| 5667 | W293 | `opt/services/multiregion/replication_scheduler.py` | 800 | blank line contains whitespace |
| 5666 | W293 | `opt/services/multiregion/replication_scheduler.py` | 793 | blank line contains whitespace |
| 5665 | W293 | `opt/services/multiregion/replication_scheduler.py` | 791 | blank line contains whitespace |
| 5664 | W293 | `opt/services/multiregion/replication_scheduler.py` | 788 | blank line contains whitespace |
| 5663 | W293 | `opt/services/multiregion/replication_scheduler.py` | 782 | blank line contains whitespace |
| 5662 | W293 | `opt/services/multiregion/replication_scheduler.py` | 779 | blank line contains whitespace |
| 5661 | W293 | `opt/services/multiregion/replication_scheduler.py` | 777 | blank line contains whitespace |
| 5660 | W293 | `opt/services/multiregion/replication_scheduler.py` | 763 | blank line contains whitespace |
| 5659 | W293 | `opt/services/multiregion/replication_scheduler.py` | 761 | blank line contains whitespace |
| 5658 | W293 | `opt/services/multiregion/replication_scheduler.py` | 759 | blank line contains whitespace |
| 5657 | W293 | `opt/services/multiregion/replication_scheduler.py` | 749 | blank line contains whitespace |
| 5656 | W293 | `opt/services/multiregion/replication_scheduler.py` | 746 | blank line contains whitespace |
| 5655 | W293 | `opt/services/multiregion/replication_scheduler.py` | 739 | blank line contains whitespace |
| 5654 | W293 | `opt/services/multiregion/replication_scheduler.py` | 735 | blank line contains whitespace |
| 5653 | W291 | `opt/services/multiregion/replication_scheduler.py` | 731 | trailing whitespace |
| 5652 | W293 | `opt/services/multiregion/replication_scheduler.py` | 730 | blank line contains whitespace |
| 5651 | W291 | `opt/services/multiregion/replication_scheduler.py` | 718 | trailing whitespace |
| 5650 | W293 | `opt/services/multiregion/replication_scheduler.py` | 717 | blank line contains whitespace |
| 5649 | W293 | `opt/services/multiregion/replication_scheduler.py` | 714 | blank line contains whitespace |
| 5648 | W293 | `opt/services/multiregion/replication_scheduler.py` | 708 | blank line contains whitespace |
| 5647 | W293 | `opt/services/multiregion/replication_scheduler.py` | 705 | blank line contains whitespace |
| 5646 | W293 | `opt/services/multiregion/replication_scheduler.py` | 700 | blank line contains whitespace |
| 5645 | W293 | `opt/services/multiregion/replication_scheduler.py` | 697 | blank line contains whitespace |
| 5644 | W293 | `opt/services/multiregion/replication_scheduler.py` | 690 | blank line contains whitespace |
| 5643 | W293 | `opt/services/multiregion/replication_scheduler.py` | 684 | blank line contains whitespace |
| 5642 | W293 | `opt/services/multiregion/replication_scheduler.py` | 681 | blank line contains whitespace |
| 5641 | W293 | `opt/services/multiregion/replication_scheduler.py` | 675 | blank line contains whitespace |
| 5640 | W293 | `opt/services/multiregion/replication_scheduler.py` | 670 | blank line contains whitespace |
| 5639 | W293 | `opt/services/multiregion/replication_scheduler.py` | 667 | blank line contains whitespace |
| 5638 | W293 | `opt/services/multiregion/replication_scheduler.py` | 662 | blank line contains whitespace |
| 5637 | W293 | `opt/services/multiregion/replication_scheduler.py` | 654 | blank line contains whitespace |
| 5636 | W293 | `opt/services/multiregion/replication_scheduler.py` | 649 | blank line contains whitespace |
| 5635 | W293 | `opt/services/multiregion/replication_scheduler.py` | 646 | blank line contains whitespace |
| 5634 | W293 | `opt/services/multiregion/replication_scheduler.py` | 641 | blank line contains whitespace |
| 5633 | W293 | `opt/services/multiregion/replication_scheduler.py` | 637 | blank line contains whitespace |
| 5632 | W293 | `opt/services/multiregion/replication_scheduler.py` | 634 | blank line contains whitespace |
| 5631 | W293 | `opt/services/multiregion/replication_scheduler.py` | 625 | blank line contains whitespace |
| 5630 | W293 | `opt/services/multiregion/replication_scheduler.py` | 621 | blank line contains whitespace |
| 5629 | W293 | `opt/services/multiregion/replication_scheduler.py` | 616 | blank line contains whitespace |
| 5628 | W293 | `opt/services/multiregion/replication_scheduler.py` | 611 | blank line contains whitespace |
| 5627 | W293 | `opt/services/multiregion/replication_scheduler.py` | 608 | blank line contains whitespace |
| 5626 | W293 | `opt/services/multiregion/replication_scheduler.py` | 600 | blank line contains whitespace |
| 5625 | W293 | `opt/services/multiregion/replication_scheduler.py` | 596 | blank line contains whitespace |
| 5624 | W293 | `opt/services/multiregion/replication_scheduler.py` | 592 | blank line contains whitespace |
| 5623 | W293 | `opt/services/multiregion/replication_scheduler.py` | 588 | blank line contains whitespace |
| 5622 | W293 | `opt/services/multiregion/replication_scheduler.py` | 584 | blank line contains whitespace |
| 5621 | W293 | `opt/services/multiregion/replication_scheduler.py` | 582 | blank line contains whitespace |
| 5620 | W293 | `opt/services/multiregion/replication_scheduler.py` | 576 | blank line contains whitespace |
| 5619 | W293 | `opt/services/multiregion/replication_scheduler.py` | 570 | blank line contains whitespace |
| 5618 | W293 | `opt/services/multiregion/replication_scheduler.py` | 567 | blank line contains whitespace |
| 5617 | W293 | `opt/services/multiregion/replication_scheduler.py` | 563 | blank line contains whitespace |
| 5616 | W291 | `opt/services/multiregion/replication_scheduler.py` | 557 | trailing whitespace |
| 5615 | W293 | `opt/services/multiregion/replication_scheduler.py` | 556 | blank line contains whitespace |
| 5614 | W293 | `opt/services/multiregion/replication_scheduler.py` | 554 | blank line contains whitespace |
| 5613 | W293 | `opt/services/multiregion/replication_scheduler.py` | 551 | blank line contains whitespace |
| 5612 | W293 | `opt/services/multiregion/replication_scheduler.py` | 548 | blank line contains whitespace |
| 5611 | W293 | `opt/services/multiregion/replication_scheduler.py` | 538 | blank line contains whitespace |
| 5610 | W293 | `opt/services/multiregion/replication_scheduler.py` | 534 | blank line contains whitespace |
| 5609 | W293 | `opt/services/multiregion/replication_scheduler.py` | 529 | blank line contains whitespace |
| 5608 | W293 | `opt/services/multiregion/replication_scheduler.py` | 526 | blank line contains whitespace |
| 5607 | W293 | `opt/services/multiregion/replication_scheduler.py` | 519 | blank line contains whitespace |
| 5606 | W293 | `opt/services/multiregion/replication_scheduler.py` | 515 | blank line contains whitespace |
| 5605 | W293 | `opt/services/multiregion/replication_scheduler.py` | 507 | blank line contains whitespace |
| 5604 | W293 | `opt/services/multiregion/replication_scheduler.py` | 499 | blank line contains whitespace |
| 5603 | W293 | `opt/services/multiregion/replication_scheduler.py` | 495 | blank line contains whitespace |
| 5602 | W293 | `opt/services/multiregion/replication_scheduler.py` | 488 | blank line contains whitespace |
| 5601 | W293 | `opt/services/multiregion/replication_scheduler.py` | 483 | blank line contains whitespace |
| 5600 | W293 | `opt/services/multiregion/replication_scheduler.py` | 479 | blank line contains whitespace |
| 5599 | W293 | `opt/services/multiregion/replication_scheduler.py` | 470 | blank line contains whitespace |
| 5598 | W293 | `opt/services/multiregion/replication_scheduler.py` | 466 | blank line contains whitespace |
| 5597 | W293 | `opt/services/multiregion/replication_scheduler.py` | 462 | blank line contains whitespace |
| 5596 | W293 | `opt/services/multiregion/replication_scheduler.py` | 454 | blank line contains whitespace |
| 5595 | W293 | `opt/services/multiregion/replication_scheduler.py` | 449 | blank line contains whitespace |
| 5594 | W293 | `opt/services/multiregion/replication_scheduler.py` | 445 | blank line contains whitespace |
| 5593 | W293 | `opt/services/multiregion/replication_scheduler.py` | 440 | blank line contains whitespace |
| 5592 | W293 | `opt/services/multiregion/replication_scheduler.py` | 430 | blank line contains whitespace |
| 5591 | W293 | `opt/services/multiregion/replication_scheduler.py` | 425 | blank line contains whitespace |
| 5590 | W293 | `opt/services/multiregion/replication_scheduler.py` | 418 | blank line contains whitespace |
| 5589 | W293 | `opt/services/multiregion/replication_scheduler.py` | 410 | blank line contains whitespace |
| 5588 | W293 | `opt/services/multiregion/replication_scheduler.py` | 400 | blank line contains whitespace |
| 5587 | W293 | `opt/services/multiregion/replication_scheduler.py` | 387 | blank line contains whitespace |
| 5586 | W293 | `opt/services/multiregion/replication_scheduler.py` | 379 | blank line contains whitespace |
| 5585 | W293 | `opt/services/multiregion/replication_scheduler.py` | 372 | blank line contains whitespace |
| 5584 | W293 | `opt/services/multiregion/replication_scheduler.py` | 362 | blank line contains whitespace |
| 5583 | W293 | `opt/services/multiregion/replication_scheduler.py` | 354 | blank line contains whitespace |
| 5582 | W293 | `opt/services/multiregion/replication_scheduler.py` | 349 | blank line contains whitespace |
| 5581 | W293 | `opt/services/multiregion/replication_scheduler.py` | 334 | blank line contains whitespace |
| 5580 | W293 | `opt/services/multiregion/replication_scheduler.py` | 329 | blank line contains whitespace |
| 5579 | W293 | `opt/services/multiregion/replication_scheduler.py` | 327 | blank line contains whitespace |
| 5578 | W293 | `opt/services/multiregion/replication_scheduler.py` | 319 | blank line contains whitespace |
| 5577 | W293 | `opt/services/multiregion/replication_scheduler.py` | 313 | blank line contains whitespace |
| 5576 | W293 | `opt/services/multiregion/replication_scheduler.py` | 309 | blank line contains whitespace |
| 5575 | W293 | `opt/services/multiregion/replication_scheduler.py` | 306 | blank line contains whitespace |
| 5574 | W293 | `opt/services/multiregion/replication_scheduler.py` | 299 | blank line contains whitespace |
| 5573 | W293 | `opt/services/multiregion/replication_scheduler.py` | 295 | blank line contains whitespace |
| 5572 | W293 | `opt/services/multiregion/replication_scheduler.py` | 285 | blank line contains whitespace |
| 5571 | W293 | `opt/services/multiregion/replication_scheduler.py` | 280 | blank line contains whitespace |
| 5570 | W293 | `opt/services/multiregion/replication_scheduler.py` | 275 | blank line contains whitespace |
| 5569 | W293 | `opt/services/multiregion/replication_scheduler.py` | 269 | blank line contains whitespace |
| 5568 | W293 | `opt/services/multiregion/replication_scheduler.py` | 240 | blank line contains whitespace |
| 5567 | W293 | `opt/services/multiregion/replication_scheduler.py` | 236 | blank line contains whitespace |
| 5566 | W293 | `opt/services/multiregion/replication_scheduler.py` | 233 | blank line contains whitespace |
| 5565 | W293 | `opt/services/multiregion/replication_scheduler.py` | 228 | blank line contains whitespace |
| 5564 | W293 | `opt/services/multiregion/replication_scheduler.py` | 199 | blank line contains whitespace |
| 5563 | W293 | `opt/services/multiregion/replication_scheduler.py` | 191 | blank line contains whitespace |
| 5562 | W293 | `opt/services/multiregion/replication_scheduler.py` | 184 | blank line contains whitespace |
| 5561 | W293 | `opt/services/multiregion/replication_scheduler.py` | 179 | blank line contains whitespace |
| 5560 | W293 | `opt/services/multiregion/replication_scheduler.py` | 173 | blank line contains whitespace |
| 5559 | W293 | `opt/services/multiregion/replication_scheduler.py` | 167 | blank line contains whitespace |
| 5558 | W293 | `opt/services/multiregion/replication_scheduler.py` | 161 | blank line contains whitespace |
| 5557 | W293 | `opt/services/multiregion/replication_scheduler.py` | 144 | blank line contains whitespace |
| 5556 | W293 | `opt/services/multiregion/replication_scheduler.py` | 140 | blank line contains whitespace |
| 5555 | W293 | `opt/services/multiregion/replication_scheduler.py` | 136 | blank line contains whitespace |
| 5554 | W293 | `opt/services/multiregion/replication_scheduler.py` | 132 | blank line contains whitespace |
| 5553 | W293 | `opt/services/multiregion/replication_scheduler.py` | 126 | blank line contains whitespace |
| 5552 | W293 | `opt/services/multiregion/replication_scheduler.py` | 108 | blank line contains whitespace |
| 5549 | W293 | `opt/services/multiregion/k8s_integration.py` | 187 | blank line contains whitespace |
| 5548 | W293 | `opt/services/multiregion/k8s_integration.py` | 177 | blank line contains whitespace |
| 5547 | W293 | `opt/services/multiregion/k8s_integration.py` | 152 | blank line contains whitespace |
| 5546 | W293 | `opt/services/multiregion/k8s_integration.py` | 147 | blank line contains whitespace |
| 5545 | W293 | `opt/services/multiregion/k8s_integration.py` | 142 | blank line contains whitespace |
| 5544 | W293 | `opt/services/multiregion/k8s_integration.py` | 79 | blank line contains whitespace |
| 5543 | W293 | `opt/services/multiregion/k8s_integration.py` | 74 | blank line contains whitespace |
| 5542 | W293 | `opt/services/multiregion/k8s_integration.py` | 71 | blank line contains whitespace |
| 5541 | W293 | `opt/services/multiregion/k8s_integration.py` | 62 | blank line contains whitespace |
| 5540 | W293 | `opt/services/multiregion/k8s_integration.py` | 43 | blank line contains whitespace |
| 5539 | W293 | `opt/services/multiregion/failover.py` | 116 | blank line contains whitespace |
| 5538 | W293 | `opt/services/multiregion/failover.py` | 112 | blank line contains whitespace |
| 5537 | W293 | `opt/services/multiregion/failover.py` | 108 | blank line contains whitespace |
| 5536 | W293 | `opt/services/multiregion/failover.py` | 106 | blank line contains whitespace |
| 5535 | W293 | `opt/services/multiregion/failover.py` | 103 | blank line contains whitespace |
| 5534 | W293 | `opt/services/multiregion/failover.py` | 84 | blank line contains whitespace |
| 5533 | W293 | `opt/services/multiregion/failover.py` | 69 | blank line contains whitespace |
| 5532 | W293 | `opt/services/multiregion/failover.py` | 65 | blank line contains whitespace |
| 5530 | W293 | `opt/services/multiregion/core.py` | 967 | blank line contains whitespace |
| 5529 | W293 | `opt/services/multiregion/core.py` | 964 | blank line contains whitespace |
| 5528 | W293 | `opt/services/multiregion/core.py` | 941 | blank line contains whitespace |
| 5527 | W293 | `opt/services/multiregion/core.py` | 937 | blank line contains whitespace |
| 5526 | W293 | `opt/services/multiregion/core.py` | 928 | blank line contains whitespace |
| 5525 | W293 | `opt/services/multiregion/core.py` | 920 | blank line contains whitespace |
| 5524 | W293 | `opt/services/multiregion/core.py` | 902 | blank line contains whitespace |
| 5523 | W293 | `opt/services/multiregion/core.py` | 896 | blank line contains whitespace |
| 5522 | W293 | `opt/services/multiregion/core.py` | 889 | blank line contains whitespace |
| 5521 | W293 | `opt/services/multiregion/core.py` | 882 | blank line contains whitespace |
| 5520 | W293 | `opt/services/multiregion/core.py` | 879 | blank line contains whitespace |
| 5519 | W293 | `opt/services/multiregion/core.py` | 872 | blank line contains whitespace |
| 5518 | W293 | `opt/services/multiregion/core.py` | 866 | blank line contains whitespace |
| 5517 | W293 | `opt/services/multiregion/core.py` | 861 | blank line contains whitespace |
| 5516 | W293 | `opt/services/multiregion/core.py` | 857 | blank line contains whitespace |
| 5515 | W293 | `opt/services/multiregion/core.py` | 848 | blank line contains whitespace |
| 5514 | W293 | `opt/services/multiregion/core.py` | 842 | blank line contains whitespace |
| 5513 | W293 | `opt/services/multiregion/core.py` | 833 | blank line contains whitespace |
| 5512 | W293 | `opt/services/multiregion/core.py` | 826 | blank line contains whitespace |
| 5511 | W293 | `opt/services/multiregion/core.py` | 823 | blank line contains whitespace |
| 5510 | W293 | `opt/services/multiregion/core.py` | 818 | blank line contains whitespace |
| 5509 | W293 | `opt/services/multiregion/core.py` | 811 | blank line contains whitespace |
| 5508 | W293 | `opt/services/multiregion/core.py` | 806 | blank line contains whitespace |
| 5507 | W293 | `opt/services/multiregion/core.py` | 796 | blank line contains whitespace |
| 5506 | W293 | `opt/services/multiregion/core.py` | 791 | blank line contains whitespace |
| 5505 | W293 | `opt/services/multiregion/core.py` | 781 | blank line contains whitespace |
| 5504 | W293 | `opt/services/multiregion/core.py` | 777 | blank line contains whitespace |
| 5503 | W293 | `opt/services/multiregion/core.py` | 765 | blank line contains whitespace |
| 5502 | W293 | `opt/services/multiregion/core.py` | 762 | blank line contains whitespace |
| 5501 | W293 | `opt/services/multiregion/core.py` | 760 | blank line contains whitespace |
| 5500 | W293 | `opt/services/multiregion/core.py` | 753 | blank line contains whitespace |
| 5499 | W293 | `opt/services/multiregion/core.py` | 742 | blank line contains whitespace |
| 5498 | W293 | `opt/services/multiregion/core.py` | 740 | blank line contains whitespace |
| 5497 | W293 | `opt/services/multiregion/core.py` | 736 | blank line contains whitespace |
| 5496 | W293 | `opt/services/multiregion/core.py` | 721 | blank line contains whitespace |
| 5495 | W293 | `opt/services/multiregion/core.py` | 707 | blank line contains whitespace |
| 5494 | W293 | `opt/services/multiregion/core.py` | 703 | blank line contains whitespace |
| 5493 | W293 | `opt/services/multiregion/core.py` | 698 | blank line contains whitespace |
| 5492 | W293 | `opt/services/multiregion/core.py` | 692 | blank line contains whitespace |
| 5491 | W293 | `opt/services/multiregion/core.py` | 686 | blank line contains whitespace |
| 5490 | W293 | `opt/services/multiregion/core.py` | 680 | blank line contains whitespace |
| 5489 | W293 | `opt/services/multiregion/core.py` | 666 | blank line contains whitespace |
| 5488 | W293 | `opt/services/multiregion/core.py` | 661 | blank line contains whitespace |
| 5487 | W293 | `opt/services/multiregion/core.py` | 659 | blank line contains whitespace |
| 5486 | W293 | `opt/services/multiregion/core.py` | 654 | blank line contains whitespace |
| 5485 | W293 | `opt/services/multiregion/core.py` | 651 | blank line contains whitespace |
| 5484 | W293 | `opt/services/multiregion/core.py` | 647 | blank line contains whitespace |
| 5483 | W293 | `opt/services/multiregion/core.py` | 639 | blank line contains whitespace |
| 5482 | W293 | `opt/services/multiregion/core.py` | 634 | blank line contains whitespace |
| 5481 | W293 | `opt/services/multiregion/core.py` | 624 | blank line contains whitespace |
| 5480 | W293 | `opt/services/multiregion/core.py` | 616 | blank line contains whitespace |
| 5479 | W293 | `opt/services/multiregion/core.py` | 608 | blank line contains whitespace |
| 5478 | W293 | `opt/services/multiregion/core.py` | 603 | blank line contains whitespace |
| 5477 | W293 | `opt/services/multiregion/core.py` | 596 | blank line contains whitespace |
| 5476 | W293 | `opt/services/multiregion/core.py` | 581 | blank line contains whitespace |
| 5475 | W293 | `opt/services/multiregion/core.py` | 578 | blank line contains whitespace |
| 5474 | W293 | `opt/services/multiregion/core.py` | 570 | blank line contains whitespace |
| 5473 | W293 | `opt/services/multiregion/core.py` | 566 | blank line contains whitespace |
| 5472 | W293 | `opt/services/multiregion/core.py` | 563 | blank line contains whitespace |
| 5471 | W293 | `opt/services/multiregion/core.py` | 560 | blank line contains whitespace |
| 5470 | W293 | `opt/services/multiregion/core.py` | 556 | blank line contains whitespace |
| 5469 | W293 | `opt/services/multiregion/core.py` | 549 | blank line contains whitespace |
| 5468 | W293 | `opt/services/multiregion/core.py` | 546 | blank line contains whitespace |
| 5467 | W293 | `opt/services/multiregion/core.py` | 535 | blank line contains whitespace |
| 5466 | W293 | `opt/services/multiregion/core.py` | 532 | blank line contains whitespace |
| 5465 | W293 | `opt/services/multiregion/core.py` | 521 | blank line contains whitespace |
| 5464 | W293 | `opt/services/multiregion/core.py` | 513 | blank line contains whitespace |
| 5463 | W293 | `opt/services/multiregion/core.py` | 510 | blank line contains whitespace |
| 5462 | W293 | `opt/services/multiregion/core.py` | 505 | blank line contains whitespace |
| 5461 | W293 | `opt/services/multiregion/core.py` | 501 | blank line contains whitespace |
| 5460 | W293 | `opt/services/multiregion/core.py` | 492 | blank line contains whitespace |
| 5459 | W293 | `opt/services/multiregion/core.py` | 487 | blank line contains whitespace |
| 5458 | W293 | `opt/services/multiregion/core.py` | 482 | blank line contains whitespace |
| 5457 | W293 | `opt/services/multiregion/core.py` | 475 | blank line contains whitespace |
| 5455 | W293 | `opt/services/multiregion/core.py` | 382 | blank line contains whitespace |
| 5454 | W293 | `opt/services/multiregion/core.py` | 283 | blank line contains whitespace |
| 5453 | W293 | `opt/services/multiregion/core.py` | 270 | blank line contains whitespace |
| 5452 | W293 | `opt/services/multiregion/core.py` | 258 | blank line contains whitespace |
| 5451 | W293 | `opt/services/multiregion/core.py` | 241 | blank line contains whitespace |
| 5450 | W293 | `opt/services/multiregion/core.py` | 203 | blank line contains whitespace |
| 5444 | W293 | `opt/services/multiregion/cli.py` | 468 | blank line contains whitespace |
| 5443 | W293 | `opt/services/multiregion/cli.py` | 463 | blank line contains whitespace |
| 5442 | W293 | `opt/services/multiregion/cli.py` | 459 | blank line contains whitespace |
| 5441 | W293 | `opt/services/multiregion/cli.py` | 454 | blank line contains whitespace |
| 5440 | W293 | `opt/services/multiregion/cli.py` | 447 | blank line contains whitespace |
| 5439 | W293 | `opt/services/multiregion/cli.py` | 437 | blank line contains whitespace |
| 5438 | W293 | `opt/services/multiregion/cli.py` | 433 | blank line contains whitespace |
| 5436 | W293 | `opt/services/multiregion/cli.py` | 427 | blank line contains whitespace |
| 5435 | W293 | `opt/services/multiregion/cli.py` | 418 | blank line contains whitespace |
| 5434 | W293 | `opt/services/multiregion/cli.py` | 404 | blank line contains whitespace |
| 5433 | W293 | `opt/services/multiregion/cli.py` | 397 | blank line contains whitespace |
| 5432 | W293 | `opt/services/multiregion/cli.py` | 385 | blank line contains whitespace |
| 5430 | W293 | `opt/services/multiregion/cli.py` | 376 | blank line contains whitespace |
| 5428 | W293 | `opt/services/multiregion/cli.py` | 368 | blank line contains whitespace |
| 5427 | W293 | `opt/services/multiregion/cli.py` | 360 | blank line contains whitespace |
| 5426 | W293 | `opt/services/multiregion/cli.py` | 351 | blank line contains whitespace |
| 5423 | W293 | `opt/services/multiregion/cli.py` | 345 | blank line contains whitespace |
| 5422 | W293 | `opt/services/multiregion/cli.py` | 331 | blank line contains whitespace |
| 5421 | W293 | `opt/services/multiregion/cli.py` | 329 | blank line contains whitespace |
| 5420 | W293 | `opt/services/multiregion/cli.py` | 314 | blank line contains whitespace |
| 5419 | W293 | `opt/services/multiregion/cli.py` | 309 | blank line contains whitespace |
| 5417 | W293 | `opt/services/multiregion/cli.py` | 301 | blank line contains whitespace |
| 5416 | W291 | `opt/services/multiregion/cli.py` | 298 | trailing whitespace |
| 5415 | W293 | `opt/services/multiregion/cli.py` | 289 | blank line contains whitespace |
| 5414 | W293 | `opt/services/multiregion/cli.py` | 287 | blank line contains whitespace |
| 5413 | W293 | `opt/services/multiregion/cli.py` | 275 | blank line contains whitespace |
| 5412 | W293 | `opt/services/multiregion/cli.py` | 271 | blank line contains whitespace |
| 5411 | W293 | `opt/services/multiregion/cli.py` | 263 | blank line contains whitespace |
| 5410 | W293 | `opt/services/multiregion/cli.py` | 258 | blank line contains whitespace |
| 5409 | W293 | `opt/services/multiregion/cli.py` | 248 | blank line contains whitespace |
| 5408 | W293 | `opt/services/multiregion/cli.py` | 231 | blank line contains whitespace |
| 5407 | W293 | `opt/services/multiregion/cli.py` | 219 | blank line contains whitespace |
| 5406 | W293 | `opt/services/multiregion/cli.py` | 217 | blank line contains whitespace |
| 5405 | W293 | `opt/services/multiregion/cli.py` | 200 | blank line contains whitespace |
| 5404 | W293 | `opt/services/multiregion/cli.py` | 198 | blank line contains whitespace |
| 5403 | W293 | `opt/services/multiregion/cli.py` | 187 | blank line contains whitespace |
| 5402 | W293 | `opt/services/multiregion/cli.py` | 180 | blank line contains whitespace |
| 5401 | W293 | `opt/services/multiregion/cli.py` | 167 | blank line contains whitespace |
| 5400 | W293 | `opt/services/multiregion/cli.py` | 163 | blank line contains whitespace |
| 5399 | W293 | `opt/services/multiregion/cli.py` | 156 | blank line contains whitespace |
| 5398 | W293 | `opt/services/multiregion/cli.py` | 152 | blank line contains whitespace |
| 5397 | W293 | `opt/services/multiregion/cli.py` | 145 | blank line contains whitespace |
| 5396 | W293 | `opt/services/multiregion/cli.py` | 135 | blank line contains whitespace |
| 5395 | W293 | `opt/services/multiregion/cli.py` | 131 | blank line contains whitespace |
| 5394 | W293 | `opt/services/multiregion/cli.py` | 124 | blank line contains whitespace |
| 5393 | W293 | `opt/services/multiregion/cli.py` | 119 | blank line contains whitespace |
| 5392 | W293 | `opt/services/multiregion/cli.py` | 110 | blank line contains whitespace |
| 5391 | W293 | `opt/services/multiregion/cli.py` | 106 | blank line contains whitespace |
| 5390 | W293 | `opt/services/multiregion/cli.py` | 101 | blank line contains whitespace |
| 5389 | W293 | `opt/services/multiregion/cli.py` | 96 | blank line contains whitespace |
| 5388 | W293 | `opt/services/multiregion/cli.py` | 90 | blank line contains whitespace |
| 5387 | W293 | `opt/services/multiregion/cli.py` | 83 | blank line contains whitespace |
| 5386 | W293 | `opt/services/multiregion/cli.py` | 74 | blank line contains whitespace |
| 5385 | W293 | `opt/services/multiregion/cli.py` | 70 | blank line contains whitespace |
| 5384 | W293 | `opt/services/multiregion/cli.py` | 68 | blank line contains whitespace |
| 5383 | W293 | `opt/services/multiregion/cli.py` | 48 | blank line contains whitespace |
| 5381 | W293 | `opt/services/multiregion/cli.py` | 30 | blank line contains whitespace |
| 5380 | W293 | `opt/services/multiregion/cli.py` | 27 | blank line contains whitespace |
| 5379 | W293 | `opt/services/multiregion/cli.py` | 21 | blank line contains whitespace |
| 5374 | W293 | `opt/services/multiregion/api.py` | 568 | blank line contains whitespace |
| 5373 | W293 | `opt/services/multiregion/api.py` | 563 | blank line contains whitespace |
| 5372 | W293 | `opt/services/multiregion/api.py` | 557 | blank line contains whitespace |
| 5371 | W293 | `opt/services/multiregion/api.py` | 551 | blank line contains whitespace |
| 5370 | W293 | `opt/services/multiregion/api.py` | 544 | blank line contains whitespace |
| 5369 | W293 | `opt/services/multiregion/api.py` | 538 | blank line contains whitespace |
| 5368 | W293 | `opt/services/multiregion/api.py` | 533 | blank line contains whitespace |
| 5367 | W293 | `opt/services/multiregion/api.py` | 528 | blank line contains whitespace |
| 5366 | W293 | `opt/services/multiregion/api.py` | 522 | blank line contains whitespace |
| 5365 | W293 | `opt/services/multiregion/api.py` | 517 | blank line contains whitespace |
| 5364 | W293 | `opt/services/multiregion/api.py` | 512 | blank line contains whitespace |
| 5363 | W293 | `opt/services/multiregion/api.py` | 507 | blank line contains whitespace |
| 5362 | W293 | `opt/services/multiregion/api.py` | 502 | blank line contains whitespace |
| 5361 | W293 | `opt/services/multiregion/api.py` | 496 | blank line contains whitespace |
| 5360 | W293 | `opt/services/multiregion/api.py` | 493 | blank line contains whitespace |
| 5359 | W293 | `opt/services/multiregion/api.py` | 485 | blank line contains whitespace |
| 5358 | W293 | `opt/services/multiregion/api.py` | 482 | blank line contains whitespace |
| 5357 | W293 | `opt/services/multiregion/api.py` | 470 | blank line contains whitespace |
| 5356 | W293 | `opt/services/multiregion/api.py` | 463 | blank line contains whitespace |
| 5355 | W293 | `opt/services/multiregion/api.py` | 456 | blank line contains whitespace |
| 5354 | W293 | `opt/services/multiregion/api.py` | 445 | blank line contains whitespace |
| 5353 | W293 | `opt/services/multiregion/api.py` | 438 | blank line contains whitespace |
| 5352 | W293 | `opt/services/multiregion/api.py` | 432 | blank line contains whitespace |
| 5351 | W293 | `opt/services/multiregion/api.py` | 424 | blank line contains whitespace |
| 5350 | W293 | `opt/services/multiregion/api.py` | 421 | blank line contains whitespace |
| 5349 | W293 | `opt/services/multiregion/api.py` | 410 | blank line contains whitespace |
| 5348 | W293 | `opt/services/multiregion/api.py` | 405 | blank line contains whitespace |
| 5347 | W293 | `opt/services/multiregion/api.py` | 396 | blank line contains whitespace |
| 5346 | W293 | `opt/services/multiregion/api.py` | 392 | blank line contains whitespace |
| 5345 | W293 | `opt/services/multiregion/api.py` | 381 | blank line contains whitespace |
| 5344 | W293 | `opt/services/multiregion/api.py` | 366 | blank line contains whitespace |
| 5343 | W293 | `opt/services/multiregion/api.py` | 353 | blank line contains whitespace |
| 5342 | W293 | `opt/services/multiregion/api.py` | 351 | blank line contains whitespace |
| 5341 | W293 | `opt/services/multiregion/api.py` | 343 | blank line contains whitespace |
| 5340 | W293 | `opt/services/multiregion/api.py` | 340 | blank line contains whitespace |
| 5339 | W293 | `opt/services/multiregion/api.py` | 329 | blank line contains whitespace |
| 5338 | W293 | `opt/services/multiregion/api.py` | 327 | blank line contains whitespace |
| 5337 | W293 | `opt/services/multiregion/api.py` | 319 | blank line contains whitespace |
| 5336 | W293 | `opt/services/multiregion/api.py` | 316 | blank line contains whitespace |
| 5335 | W293 | `opt/services/multiregion/api.py` | 309 | blank line contains whitespace |
| 5334 | W293 | `opt/services/multiregion/api.py` | 300 | blank line contains whitespace |
| 5333 | W293 | `opt/services/multiregion/api.py` | 288 | blank line contains whitespace |
| 5332 | W293 | `opt/services/multiregion/api.py` | 286 | blank line contains whitespace |
| 5331 | W293 | `opt/services/multiregion/api.py` | 278 | blank line contains whitespace |
| 5330 | W293 | `opt/services/multiregion/api.py` | 275 | blank line contains whitespace |
| 5329 | W293 | `opt/services/multiregion/api.py` | 268 | blank line contains whitespace |
| 5328 | W293 | `opt/services/multiregion/api.py` | 261 | blank line contains whitespace |
| 5327 | W293 | `opt/services/multiregion/api.py` | 253 | blank line contains whitespace |
| 5326 | W293 | `opt/services/multiregion/api.py` | 246 | blank line contains whitespace |
| 5325 | W293 | `opt/services/multiregion/api.py` | 238 | blank line contains whitespace |
| 5324 | W293 | `opt/services/multiregion/api.py` | 235 | blank line contains whitespace |
| 5323 | W293 | `opt/services/multiregion/api.py` | 224 | blank line contains whitespace |
| 5322 | W293 | `opt/services/multiregion/api.py` | 222 | blank line contains whitespace |
| 5321 | W293 | `opt/services/multiregion/api.py` | 214 | blank line contains whitespace |
| 5320 | W293 | `opt/services/multiregion/api.py` | 211 | blank line contains whitespace |
| 5319 | W293 | `opt/services/multiregion/api.py` | 204 | blank line contains whitespace |
| 5318 | W293 | `opt/services/multiregion/api.py` | 195 | blank line contains whitespace |
| 5317 | W293 | `opt/services/multiregion/api.py` | 191 | blank line contains whitespace |
| 5316 | W293 | `opt/services/multiregion/api.py` | 182 | blank line contains whitespace |
| 5315 | W293 | `opt/services/multiregion/api.py` | 176 | blank line contains whitespace |
| 5314 | W293 | `opt/services/multiregion/api.py` | 173 | blank line contains whitespace |
| 5313 | W293 | `opt/services/multiregion/api.py` | 166 | blank line contains whitespace |
| 5312 | W293 | `opt/services/multiregion/api.py` | 164 | blank line contains whitespace |
| 5311 | W293 | `opt/services/multiregion/api.py` | 156 | blank line contains whitespace |
| 5310 | W293 | `opt/services/multiregion/api.py` | 153 | blank line contains whitespace |
| 5309 | W293 | `opt/services/multiregion/api.py` | 146 | blank line contains whitespace |
| 5308 | W293 | `opt/services/multiregion/api.py` | 140 | blank line contains whitespace |
| 5307 | W293 | `opt/services/multiregion/api.py` | 129 | blank line contains whitespace |
| 5306 | W293 | `opt/services/multiregion/api.py` | 126 | blank line contains whitespace |
| 5305 | W293 | `opt/services/multiregion/api.py` | 119 | blank line contains whitespace |
| 5304 | W293 | `opt/services/multiregion/api.py` | 112 | blank line contains whitespace |
| 5303 | W293 | `opt/services/multiregion/api.py` | 104 | blank line contains whitespace |
| 5302 | W293 | `opt/services/multiregion/api.py` | 96 | blank line contains whitespace |
| 5301 | W293 | `opt/services/multiregion/api.py` | 93 | blank line contains whitespace |
| 5300 | W293 | `opt/services/multiregion/api.py` | 76 | blank line contains whitespace |
| 5299 | W293 | `opt/services/multiregion/api.py` | 71 | blank line contains whitespace |
| 5298 | W293 | `opt/services/multiregion/api.py` | 61 | blank line contains whitespace |
| 5297 | W293 | `opt/services/multiregion/api.py` | 58 | blank line contains whitespace |
| 5296 | W293 | `opt/services/multiregion/api.py` | 49 | blank line contains whitespace |
| 5295 | W293 | `opt/services/multiregion/api.py` | 43 | blank line contains whitespace |
| 5294 | W293 | `opt/services/multiregion/api.py` | 28 | blank line contains whitespace |
| 5290 | W293 | `opt/services/multiregion/**init**.py` | 20 | blank line contains whitespace |
| 5289 | W293 | `opt/services/multiregion/**init**.py` | 17 | blank line contains whitespace |
| 5288 | W293 | `opt/services/multiregion/**init**.py` | 13 | blank line contains whitespace |
| 5287 | W293 | `opt/services/multiregion/**init**.py` | 10 | blank line contains whitespace |
| 5286 | W391 | `opt/services/multi_cluster.py` | 634 | blank line at end of file |
| 5285 | W293 | `opt/services/multi_cluster.py` | 630 | blank line contains whitespace |
| 5284 | W293 | `opt/services/multi_cluster.py` | 617 | blank line contains whitespace |
| 5283 | W293 | `opt/services/multi_cluster.py` | 609 | blank line contains whitespace |
| 5282 | W293 | `opt/services/multi_cluster.py` | 583 | blank line contains whitespace |
| 5281 | W293 | `opt/services/multi_cluster.py` | 575 | blank line contains whitespace |
| 5280 | W293 | `opt/services/multi_cluster.py` | 563 | blank line contains whitespace |
| 5279 | W293 | `opt/services/multi_cluster.py` | 557 | blank line contains whitespace |
| 5278 | W291 | `opt/services/multi_cluster.py` | 553 | trailing whitespace |
| 5277 | W293 | `opt/services/multi_cluster.py` | 544 | blank line contains whitespace |
| 5276 | W293 | `opt/services/multi_cluster.py` | 541 | blank line contains whitespace |
| 5275 | W293 | `opt/services/multi_cluster.py` | 534 | blank line contains whitespace |
| 5274 | W293 | `opt/services/multi_cluster.py` | 514 | blank line contains whitespace |
| 5273 | W291 | `opt/services/multi_cluster.py` | 512 | trailing whitespace |
| 5272 | W293 | `opt/services/multi_cluster.py` | 510 | blank line contains whitespace |
| 5271 | W293 | `opt/services/multi_cluster.py` | 508 | blank line contains whitespace |
| 5270 | W293 | `opt/services/multi_cluster.py` | 501 | blank line contains whitespace |
| 5269 | W293 | `opt/services/multi_cluster.py` | 497 | blank line contains whitespace |
| 5268 | W293 | `opt/services/multi_cluster.py` | 491 | blank line contains whitespace |
| 5267 | W293 | `opt/services/multi_cluster.py` | 484 | blank line contains whitespace |
| 5266 | W293 | `opt/services/multi_cluster.py` | 478 | blank line contains whitespace |
| 5265 | W293 | `opt/services/multi_cluster.py` | 475 | blank line contains whitespace |
| 5264 | W293 | `opt/services/multi_cluster.py` | 468 | blank line contains whitespace |
| 5263 | W293 | `opt/services/multi_cluster.py` | 464 | blank line contains whitespace |
| 5262 | W291 | `opt/services/multi_cluster.py` | 460 | trailing whitespace |
| 5261 | W293 | `opt/services/multi_cluster.py` | 454 | blank line contains whitespace |
| 5260 | W293 | `opt/services/multi_cluster.py` | 450 | blank line contains whitespace |
| 5259 | W293 | `opt/services/multi_cluster.py` | 444 | blank line contains whitespace |
| 5258 | W293 | `opt/services/multi_cluster.py` | 437 | blank line contains whitespace |
| 5257 | W293 | `opt/services/multi_cluster.py` | 433 | blank line contains whitespace |
| 5256 | W293 | `opt/services/multi_cluster.py` | 430 | blank line contains whitespace |
| 5255 | W293 | `opt/services/multi_cluster.py` | 424 | blank line contains whitespace |
| 5254 | W293 | `opt/services/multi_cluster.py` | 420 | blank line contains whitespace |
| 5253 | W293 | `opt/services/multi_cluster.py` | 410 | blank line contains whitespace |
| 5252 | W293 | `opt/services/multi_cluster.py` | 400 | blank line contains whitespace |
| 5251 | W291 | `opt/services/multi_cluster.py` | 396 | trailing whitespace |
| 5250 | W293 | `opt/services/multi_cluster.py` | 393 | blank line contains whitespace |
| 5249 | W293 | `opt/services/multi_cluster.py` | 390 | blank line contains whitespace |
| 5248 | W293 | `opt/services/multi_cluster.py` | 378 | blank line contains whitespace |
| 5247 | W293 | `opt/services/multi_cluster.py` | 372 | blank line contains whitespace |
| 5246 | W293 | `opt/services/multi_cluster.py` | 359 | blank line contains whitespace |
| 5245 | W293 | `opt/services/multi_cluster.py` | 355 | blank line contains whitespace |
| 5244 | W293 | `opt/services/multi_cluster.py` | 349 | blank line contains whitespace |
| 5243 | W293 | `opt/services/multi_cluster.py` | 342 | blank line contains whitespace |
| 5242 | W293 | `opt/services/multi_cluster.py` | 335 | blank line contains whitespace |
| 5241 | W293 | `opt/services/multi_cluster.py` | 331 | blank line contains whitespace |
| 5240 | W293 | `opt/services/multi_cluster.py` | 325 | blank line contains whitespace |
| 5239 | W293 | `opt/services/multi_cluster.py` | 323 | blank line contains whitespace |
| 5238 | W291 | `opt/services/multi_cluster.py` | 318 | trailing whitespace |
| 5237 | W293 | `opt/services/multi_cluster.py` | 308 | blank line contains whitespace |
| 5236 | W293 | `opt/services/multi_cluster.py` | 304 | blank line contains whitespace |
| 5235 | W293 | `opt/services/multi_cluster.py` | 293 | blank line contains whitespace |
| 5234 | W293 | `opt/services/multi_cluster.py` | 290 | blank line contains whitespace |
| 5233 | W293 | `opt/services/multi_cluster.py` | 279 | blank line contains whitespace |
| 5232 | W293 | `opt/services/multi_cluster.py` | 275 | blank line contains whitespace |
| 5231 | W293 | `opt/services/multi_cluster.py` | 265 | blank line contains whitespace |
| 5230 | W293 | `opt/services/multi_cluster.py` | 262 | blank line contains whitespace |
| 5229 | W293 | `opt/services/multi_cluster.py` | 256 | blank line contains whitespace |
| 5228 | W293 | `opt/services/multi_cluster.py` | 252 | blank line contains whitespace |
| 5227 | W291 | `opt/services/multi_cluster.py` | 245 | trailing whitespace |
| 5226 | W293 | `opt/services/multi_cluster.py` | 239 | blank line contains whitespace |
| 5225 | W293 | `opt/services/multi_cluster.py` | 236 | blank line contains whitespace |
| 5224 | W293 | `opt/services/multi_cluster.py` | 229 | blank line contains whitespace |
| 5223 | W293 | `opt/services/multi_cluster.py` | 224 | blank line contains whitespace |
| 5222 | W293 | `opt/services/multi_cluster.py` | 217 | blank line contains whitespace |
| 5221 | W293 | `opt/services/multi_cluster.py` | 212 | blank line contains whitespace |
| 5220 | W291 | `opt/services/multi_cluster.py` | 208 | trailing whitespace |
| 5219 | W293 | `opt/services/multi_cluster.py` | 199 | blank line contains whitespace |
| 5218 | W293 | `opt/services/multi_cluster.py` | 196 | blank line contains whitespace |
| 5217 | W293 | `opt/services/multi_cluster.py` | 184 | blank line contains whitespace |
| 5216 | W293 | `opt/services/multi_cluster.py` | 177 | blank line contains whitespace |
| 5215 | W293 | `opt/services/multi_cluster.py` | 174 | blank line contains whitespace |
| 5214 | W293 | `opt/services/multi_cluster.py` | 166 | blank line contains whitespace |
| 5213 | W293 | `opt/services/multi_cluster.py` | 159 | blank line contains whitespace |
| 5212 | W293 | `opt/services/multi_cluster.py` | 156 | blank line contains whitespace |
| 5211 | W293 | `opt/services/multi_cluster.py` | 145 | blank line contains whitespace |
| 5210 | W293 | `opt/services/multi_cluster.py` | 94 | blank line contains whitespace |
| 5209 | W293 | `opt/services/multi_cluster.py` | 71 | blank line contains whitespace |
| 5203 | W293 | `opt/services/cache/core.py` | 151 | blank line contains whitespace |
| 5202 | W293 | `opt/services/cache/core.py` | 148 | blank line contains whitespace |
| 5201 | W293 | `opt/services/cache/core.py` | 145 | blank line contains whitespace |
| 5200 | W293 | `opt/services/cache/core.py` | 142 | blank line contains whitespace |
| 5199 | W293 | `opt/services/cache/core.py` | 134 | blank line contains whitespace |
| 5198 | W291 | `opt/services/cache/core.py` | 88 | trailing whitespace |
| 5197 | W291 | `opt/services/cache/core.py` | 87 | trailing whitespace |
| 5196 | W291 | `opt/services/cache/core.py` | 86 | trailing whitespace |
| 5195 | W291 | `opt/services/cache/core.py` | 85 | trailing whitespace |
| 5194 | W293 | `opt/services/cache/core.py` | 80 | blank line contains whitespace |
| 5193 | W293 | `opt/services/cache/core.py` | 51 | blank line contains whitespace |
| 5192 | W293 | `opt/services/cache/core.py` | 47 | blank line contains whitespace |
| 5191 | W293 | `opt/services/cache/core.py` | 39 | blank line contains whitespace |
| 5190 | W293 | `opt/services/cache/core.py` | 24 | blank line contains whitespace |
| 5184 | W293 | `opt/services/backup_manager.py` | 264 | blank line contains whitespace |
| 5183 | W293 | `opt/services/backup_manager.py` | 258 | blank line contains whitespace |
| 5182 | W293 | `opt/services/backup_manager.py` | 254 | blank line contains whitespace |
| 5181 | W293 | `opt/services/backup_manager.py` | 245 | blank line contains whitespace |
| 5180 | W293 | `opt/services/backup_manager.py` | 243 | blank line contains whitespace |
| 5179 | W293 | `opt/services/backup_manager.py` | 241 | blank line contains whitespace |
| 5178 | W293 | `opt/services/backup_manager.py` | 230 | blank line contains whitespace |
| 5177 | W293 | `opt/services/backup_manager.py` | 228 | blank line contains whitespace |
| 5176 | W293 | `opt/services/backup_manager.py` | 221 | blank line contains whitespace |
| 5175 | W293 | `opt/services/backup_manager.py` | 216 | blank line contains whitespace |
| 5174 | W293 | `opt/services/backup_manager.py` | 208 | blank line contains whitespace |
| 5173 | W293 | `opt/services/backup_manager.py` | 204 | blank line contains whitespace |
| 5172 | W293 | `opt/services/backup_manager.py` | 189 | blank line contains whitespace |
| 5171 | W293 | `opt/services/backup_manager.py` | 151 | blank line contains whitespace |
| 5170 | W293 | `opt/services/backup_manager.py` | 142 | blank line contains whitespace |
| 5169 | W293 | `opt/services/backup_manager.py` | 140 | blank line contains whitespace |
| 5168 | W293 | `opt/services/backup_manager.py` | 134 | blank line contains whitespace |
| 5167 | W293 | `opt/services/backup_manager.py` | 131 | blank line contains whitespace |
| 5166 | W293 | `opt/services/backup_manager.py` | 128 | blank line contains whitespace |
| 5165 | W293 | `opt/services/backup_manager.py` | 125 | blank line contains whitespace |
| 5164 | W291 | `opt/services/backup_manager.py` | 122 | trailing whitespace |
| 5163 | W291 | `opt/services/backup_manager.py` | 117 | trailing whitespace |
| 5162 | W293 | `opt/services/backup_manager.py` | 115 | blank line contains whitespace |
| 5160 | W293 | `opt/services/backup_manager.py` | 108 | blank line contains whitespace |
| 5159 | W293 | `opt/services/backup_manager.py` | 101 | blank line contains whitespace |
| 5158 | W293 | `opt/services/backup_manager.py` | 94 | blank line contains whitespace |
| 5157 | W293 | `opt/services/backup_manager.py` | 89 | blank line contains whitespace |
| 5156 | W293 | `opt/services/backup_manager.py` | 87 | blank line contains whitespace |
| 5155 | W293 | `opt/services/backup_manager.py` | 63 | blank line contains whitespace |
| 5154 | W293 | `opt/services/backup_manager.py` | 58 | blank line contains whitespace |
| 5153 | W293 | `opt/services/backup_manager.py` | 56 | blank line contains whitespace |
| 5152 | W293 | `opt/services/backup_manager.py` | 47 | blank line contains whitespace |
| 5150 | W293 | `fix_code_scanning.py` | 64 | blank line contains whitespace |
| 5149 | W293 | `fix_code_scanning.py` | 51 | blank line contains whitespace |
| 5148 | W293 | `fix_code_scanning.py` | 43 | blank line contains whitespace |
| 5147 | W293 | `fix_code_scanning.py` | 38 | blank line contains whitespace |
| 5146 | W293 | `fix_code_scanning.py` | 29 | blank line contains whitespace |
| 5144 | W293 | `cleanup_implemented.py` | 29 | blank line contains whitespace |
| 5142 | E261 | `opt/web/panel/socketio_server.py` | 654 | at least two spaces before inline comment |
| 5141 | E305 | `opt/services/cache/core.py` | 156 | expected 2 blank lines after class or function definition, found 1 |
| 5140 | E302 | `opt/services/cache/core.py` | 132 | expected 2 blank lines, found 1 |
| 5139 | E701 | `opt/services/cache/core.py` | 125 | multiple statements on one line (colon) |
| 5138 | E701 | `opt/services/cache/core.py` | 117 | multiple statements on one line (colon) |
| 5137 | E701 | `opt/services/cache/core.py` | 108 | multiple statements on one line (colon) |
| 5136 | E701 | `opt/services/cache/core.py` | 97 | multiple statements on one line (colon) |
| 5135 | E302 | `opt/services/cache/core.py` | 78 | expected 2 blank lines, found 1 |
| 5134 | E302 | `opt/services/cache/core.py` | 45 | expected 2 blank lines, found 1 |
| 5133 | E302 | `opt/services/cache/core.py` | 22 | expected 2 blank lines, found 1 |
| 5132 | E305 | `opt/services/backup_manager.py` | 273 | expected 2 blank lines after class or function definition, found 1 |
| 5131 | E302 | `opt/services/backup_manager.py` | 267 | expected 2 blank lines, found 1 |
| 5130 | E305 | `fix_code_scanning.py` | 101 | expected 2 blank lines after class or function definition, found 1 |
| 5129 | E302 | `fix_code_scanning.py` | 86 | expected 2 blank lines, found 1 |
| 5128 | E302 | `fix_code_scanning.py` | 5 | expected 2 blank lines, found 1 |
| 5127 | W293 | `opt/netcfg_tui_app.py` | 78 | blank line contains whitespace |
| 5126 | W293 | `opt/netcfg_tui_app.py` | 75 | blank line contains whitespace |
| 5125 | W293 | `opt/netcfg_tui_app.py` | 61 | blank line contains whitespace |
| 5124 | W293 | `opt/netcfg_tui_app.py` | 55 | blank line contains whitespace |
| 5123 | W293 | `opt/netcfg_tui_app.py` | 40 | blank line contains whitespace |
| 5122 | W293 | `opt/netcfg_tui_app.py` | 31 | blank line contains whitespace |
| 5121 | W291 | `opt/netcfg_tui_app.py` | 17 | trailing whitespace |
| 5120 | W291 | `opt/netcfg_tui_app.py` | 16 | trailing whitespace |
| 5116 | E305 | `opt/netcfg_tui_app.py` | 93 | expected 2 blank lines after class or function definition, found 1 |
| 5115 | E302 | `opt/netcfg_tui_app.py` | 26 | expected 2 blank lines, found 1 |
| 5114 | E402 | `opt/netcfg_tui_app.py` | 15 | module level import not at top of file |
| 5113 | W293 | `opt/services/migration/import_wizard.py` | 897 | blank line contains whitespace |
| 5112 | W293 | `opt/services/migration/import_wizard.py` | 891 | blank line contains whitespace |
| 5111 | W293 | `opt/services/migration/import_wizard.py` | 885 | blank line contains whitespace |
| 5110 | W293 | `opt/services/migration/import_wizard.py` | 883 | blank line contains whitespace |
| 5109 | W293 | `opt/services/migration/import_wizard.py` | 880 | blank line contains whitespace |
| 5108 | E305 | `scripts/fix_markdown_lint_comprehensive.py` | 157 | expected 2 blank lines after class or function definition, found 1 |
| 5107 | E501 | `scripts/fix_markdown_lint_comprehensive.py` | 151 | line too long (133 > 120 characters) |
| 5106 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 135 | expected 2 blank lines, found 1 |
| 5105 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 117 | expected 2 blank lines, found 1 |
| 5104 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 106 | expected 2 blank lines, found 1 |
| 5103 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 102 | expected 2 blank lines, found 1 |
| 5102 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 98 | expected 2 blank lines, found 1 |
| 5101 | E306 | `scripts/fix_markdown_lint_comprehensive.py` | 93 | expected 1 blank line before a nested definition, found 0 |
| 5100 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 90 | expected 2 blank lines, found 1 |
| 5099 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 64 | expected 2 blank lines, found 1 |
| 5098 | E117 | `scripts/fix_markdown_lint_comprehensive.py` | 53 | over-indented |
| 5097 | E111 | `scripts/fix_markdown_lint_comprehensive.py` | 53 | indentation is not a multiple of 4 |
| 5096 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 44 | expected 2 blank lines, found 1 |
| 5095 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 11 | expected 2 blank lines, found 1 |
| 5094 | W293 | `opt/services/migration/import_wizard.py` | 873 | blank line contains whitespace |
| 5093 | W293 | `opt/services/migration/import_wizard.py` | 871 | blank line contains whitespace |
| 5092 | W293 | `opt/services/migration/import_wizard.py` | 863 | blank line contains whitespace |
| 5091 | W293 | `opt/services/migration/import_wizard.py` | 861 | blank line contains whitespace |
| 5090 | W293 | `opt/services/migration/import_wizard.py` | 858 | blank line contains whitespace |
| 5089 | W293 | `opt/services/migration/import_wizard.py` | 851 | blank line contains whitespace |
| 5088 | W293 | `opt/services/migration/import_wizard.py` | 846 | blank line contains whitespace |
| 5087 | W293 | `opt/services/migration/import_wizard.py` | 844 | blank line contains whitespace |
| 5086 | W293 | `opt/services/migration/import_wizard.py` | 838 | blank line contains whitespace |
| 5085 | W293 | `opt/services/migration/import_wizard.py` | 835 | blank line contains whitespace |
| 5084 | W293 | `opt/services/migration/import_wizard.py` | 831 | blank line contains whitespace |
| 5083 | W293 | `opt/services/migration/import_wizard.py` | 823 | blank line contains whitespace |
| 5082 | W293 | `opt/services/migration/import_wizard.py` | 820 | blank line contains whitespace |
| 5081 | W293 | `opt/services/migration/import_wizard.py` | 816 | blank line contains whitespace |
| 5080 | W293 | `opt/services/migration/import_wizard.py` | 814 | blank line contains whitespace |
| 5079 | W293 | `opt/services/migration/import_wizard.py` | 801 | blank line contains whitespace |
| 5078 | W293 | `opt/services/migration/import_wizard.py` | 798 | blank line contains whitespace |
| 5077 | W293 | `opt/services/migration/import_wizard.py` | 791 | blank line contains whitespace |
| 5076 | W293 | `opt/services/migration/import_wizard.py` | 784 | blank line contains whitespace |
| 5075 | W293 | `opt/services/migration/import_wizard.py` | 780 | blank line contains whitespace |
| 5074 | W293 | `opt/services/migration/import_wizard.py` | 771 | blank line contains whitespace |
| 5073 | W293 | `opt/services/migration/import_wizard.py` | 764 | blank line contains whitespace |
| 5072 | W293 | `opt/services/migration/import_wizard.py` | 756 | blank line contains whitespace |
| 5071 | W293 | `opt/services/migration/import_wizard.py` | 744 | blank line contains whitespace |
| 5070 | W293 | `opt/services/migration/import_wizard.py` | 739 | blank line contains whitespace |
| 5069 | W293 | `opt/services/migration/import_wizard.py` | 732 | blank line contains whitespace |
| 5068 | W293 | `opt/services/migration/import_wizard.py` | 725 | blank line contains whitespace |
| 5067 | W293 | `opt/services/migration/import_wizard.py` | 723 | blank line contains whitespace |
| 5066 | W293 | `opt/services/migration/import_wizard.py` | 718 | blank line contains whitespace |
| 5065 | W293 | `opt/services/migration/import_wizard.py` | 715 | blank line contains whitespace |
| 5064 | W293 | `opt/services/migration/import_wizard.py` | 709 | blank line contains whitespace |
| 5063 | W293 | `opt/services/migration/import_wizard.py` | 701 | blank line contains whitespace |
| 5062 | W293 | `opt/services/migration/import_wizard.py` | 697 | blank line contains whitespace |
| 5061 | W293 | `opt/services/migration/import_wizard.py` | 688 | blank line contains whitespace |
| 5060 | W293 | `opt/services/migration/import_wizard.py` | 680 | blank line contains whitespace |
| 5059 | W293 | `opt/services/migration/import_wizard.py` | 658 | blank line contains whitespace |
| 5057 | W293 | `opt/services/migration/import_wizard.py` | 650 | blank line contains whitespace |
| 5056 | W293 | `opt/services/migration/import_wizard.py` | 645 | blank line contains whitespace |
| 5054 | W293 | `opt/services/migration/import_wizard.py` | 629 | blank line contains whitespace |
| 5053 | W293 | `opt/services/migration/import_wizard.py` | 621 | blank line contains whitespace |
| 5052 | W293 | `opt/services/migration/import_wizard.py` | 619 | blank line contains whitespace |
| 5051 | W293 | `opt/services/migration/import_wizard.py` | 614 | blank line contains whitespace |
| 5050 | W293 | `opt/services/migration/import_wizard.py` | 612 | blank line contains whitespace |
| 5049 | W293 | `opt/services/migration/import_wizard.py` | 600 | blank line contains whitespace |
| 5048 | W293 | `opt/services/migration/import_wizard.py` | 598 | blank line contains whitespace |
| 5047 | W293 | `opt/services/migration/import_wizard.py` | 583 | blank line contains whitespace |
| 5046 | W293 | `opt/services/migration/import_wizard.py` | 570 | blank line contains whitespace |
| 5045 | W293 | `opt/services/migration/import_wizard.py` | 567 | blank line contains whitespace |
| 5044 | W293 | `opt/services/migration/import_wizard.py` | 553 | blank line contains whitespace |
| 5043 | W293 | `opt/services/migration/import_wizard.py` | 542 | blank line contains whitespace |
| 5042 | W293 | `opt/services/migration/import_wizard.py` | 532 | blank line contains whitespace |
| 5041 | W293 | `opt/services/migration/import_wizard.py` | 527 | blank line contains whitespace |
| 5040 | W293 | `opt/services/migration/import_wizard.py` | 521 | blank line contains whitespace |
| 5039 | W293 | `opt/services/migration/import_wizard.py` | 515 | blank line contains whitespace |
| 5038 | W293 | `opt/services/migration/import_wizard.py` | 509 | blank line contains whitespace |
| 5037 | W293 | `opt/services/migration/import_wizard.py` | 504 | blank line contains whitespace |
| 5036 | W293 | `opt/services/migration/import_wizard.py` | 497 | blank line contains whitespace |
| 5035 | W293 | `opt/services/migration/import_wizard.py` | 493 | blank line contains whitespace |
| 5034 | W293 | `opt/services/migration/import_wizard.py` | 490 | blank line contains whitespace |
| 5033 | W293 | `opt/services/migration/import_wizard.py` | 485 | blank line contains whitespace |
| 5032 | W293 | `opt/services/migration/import_wizard.py` | 478 | blank line contains whitespace |
| 5031 | W293 | `opt/services/migration/import_wizard.py` | 469 | blank line contains whitespace |
| 5030 | W293 | `opt/services/migration/import_wizard.py` | 452 | blank line contains whitespace |
| 5029 | W293 | `opt/services/migration/import_wizard.py` | 443 | blank line contains whitespace |
| 5028 | W293 | `opt/services/migration/import_wizard.py` | 436 | blank line contains whitespace |
| 5027 | W293 | `opt/services/migration/import_wizard.py` | 419 | blank line contains whitespace |
| 5026 | W293 | `opt/services/migration/import_wizard.py` | 399 | blank line contains whitespace |
| 5025 | W293 | `opt/services/migration/import_wizard.py` | 395 | blank line contains whitespace |
| 5024 | W293 | `opt/services/migration/import_wizard.py` | 384 | blank line contains whitespace |
| 5023 | W293 | `opt/services/migration/import_wizard.py` | 378 | blank line contains whitespace |
| 5022 | W293 | `opt/services/migration/import_wizard.py` | 372 | blank line contains whitespace |
| 5021 | W293 | `opt/services/migration/import_wizard.py` | 369 | blank line contains whitespace |
| 5020 | W293 | `opt/services/migration/import_wizard.py` | 359 | blank line contains whitespace |
| 5019 | W293 | `opt/services/migration/import_wizard.py` | 357 | blank line contains whitespace |
| 5018 | W293 | `opt/services/migration/import_wizard.py` | 350 | blank line contains whitespace |
| 5017 | W293 | `opt/services/migration/import_wizard.py` | 344 | blank line contains whitespace |
| 5016 | W293 | `opt/services/migration/import_wizard.py` | 336 | blank line contains whitespace |
| 5015 | W293 | `opt/services/migration/import_wizard.py` | 329 | blank line contains whitespace |
| 5014 | W293 | `opt/services/migration/import_wizard.py` | 322 | blank line contains whitespace |
| 5013 | W293 | `opt/services/migration/import_wizard.py` | 291 | blank line contains whitespace |
| 5012 | W293 | `opt/services/migration/import_wizard.py` | 288 | blank line contains whitespace |
| 5011 | W293 | `opt/services/migration/import_wizard.py` | 272 | blank line contains whitespace |
| 5010 | W293 | `opt/services/migration/import_wizard.py` | 263 | blank line contains whitespace |
| 5009 | W293 | `opt/services/migration/import_wizard.py` | 253 | blank line contains whitespace |
| 5008 | W293 | `opt/services/migration/import_wizard.py` | 248 | blank line contains whitespace |
| 5007 | W293 | `opt/services/migration/import_wizard.py` | 245 | blank line contains whitespace |
| 5006 | W293 | `opt/services/migration/import_wizard.py` | 240 | blank line contains whitespace |
| 5005 | W293 | `opt/services/migration/import_wizard.py` | 236 | blank line contains whitespace |
| 5004 | W293 | `opt/services/migration/import_wizard.py` | 231 | blank line contains whitespace |
| 5003 | W293 | `opt/services/migration/import_wizard.py` | 226 | blank line contains whitespace |
| 5002 | W293 | `opt/services/migration/import_wizard.py` | 210 | blank line contains whitespace |
| 5001 | W293 | `opt/services/migration/import_wizard.py` | 206 | blank line contains whitespace |
| 4998 | W293 | `opt/services/migration/import_wizard.py` | 198 | blank line contains whitespace |
| 4997 | W293 | `opt/services/migration/import_wizard.py` | 194 | blank line contains whitespace |
| 4996 | W293 | `opt/services/migration/import_wizard.py` | 185 | blank line contains whitespace |
| 4995 | W293 | `opt/services/migration/import_wizard.py` | 179 | blank line contains whitespace |
| 4994 | W293 | `opt/services/migration/import_wizard.py` | 174 | blank line contains whitespace |
| 4993 | W293 | `opt/services/migration/import_wizard.py` | 169 | blank line contains whitespace |
| 4992 | W293 | `opt/services/migration/import_wizard.py` | 164 | blank line contains whitespace |
| 4989 | W293 | `opt/services/migration/advanced_migration.py` | 1207 | blank line contains whitespace |
| 4988 | W293 | `opt/services/migration/advanced_migration.py` | 1200 | blank line contains whitespace |
| 4987 | W293 | `opt/services/migration/advanced_migration.py` | 1198 | blank line contains whitespace |
| 4986 | W293 | `opt/services/migration/advanced_migration.py` | 1195 | blank line contains whitespace |
| 4985 | W293 | `opt/services/migration/advanced_migration.py` | 1193 | blank line contains whitespace |
| 4983 | W293 | `opt/services/migration/advanced_migration.py` | 1186 | blank line contains whitespace |
| 4982 | W293 | `opt/services/migration/advanced_migration.py` | 1183 | blank line contains whitespace |
| 4981 | W293 | `opt/services/migration/advanced_migration.py` | 1181 | blank line contains whitespace |
| 4980 | W293 | `opt/services/migration/advanced_migration.py` | 1174 | blank line contains whitespace |
| 4979 | W293 | `opt/services/migration/advanced_migration.py` | 1166 | blank line contains whitespace |
| 4978 | W293 | `opt/services/migration/advanced_migration.py` | 1163 | blank line contains whitespace |
| 4977 | W293 | `opt/services/migration/advanced_migration.py` | 1156 | blank line contains whitespace |
| 4976 | W293 | `opt/services/migration/advanced_migration.py` | 1148 | blank line contains whitespace |
| 4975 | W293 | `opt/services/migration/advanced_migration.py` | 1144 | blank line contains whitespace |
| 4974 | W293 | `opt/services/migration/advanced_migration.py` | 1141 | blank line contains whitespace |
| 4973 | W293 | `opt/services/migration/advanced_migration.py` | 1137 | blank line contains whitespace |
| 4972 | W293 | `opt/services/migration/advanced_migration.py` | 1133 | blank line contains whitespace |
| 4971 | W293 | `opt/services/migration/advanced_migration.py` | 1128 | blank line contains whitespace |
| 4970 | W293 | `opt/services/migration/advanced_migration.py` | 1121 | blank line contains whitespace |
| 4969 | W293 | `opt/services/migration/advanced_migration.py` | 1118 | blank line contains whitespace |
| 4968 | W293 | `opt/services/migration/advanced_migration.py` | 1115 | blank line contains whitespace |
| 4967 | W293 | `opt/services/migration/advanced_migration.py` | 1111 | blank line contains whitespace |
| 4966 | W293 | `opt/services/migration/advanced_migration.py` | 1093 | blank line contains whitespace |
| 4965 | W293 | `opt/services/migration/advanced_migration.py` | 1089 | blank line contains whitespace |
| 4964 | W293 | `opt/services/migration/advanced_migration.py` | 1085 | blank line contains whitespace |
| 4963 | W293 | `opt/services/migration/advanced_migration.py` | 1081 | blank line contains whitespace |
| 4962 | W293 | `opt/services/migration/advanced_migration.py` | 1075 | blank line contains whitespace |
| 4961 | W293 | `opt/services/migration/advanced_migration.py` | 1062 | blank line contains whitespace |
| 4960 | W293 | `opt/services/migration/advanced_migration.py` | 1060 | blank line contains whitespace |
| 4959 | W293 | `opt/services/migration/advanced_migration.py` | 1051 | blank line contains whitespace |
| 4958 | W293 | `opt/services/migration/advanced_migration.py` | 1047 | blank line contains whitespace |
| 4957 | W293 | `opt/services/migration/advanced_migration.py` | 1037 | blank line contains whitespace |
| 4956 | W293 | `opt/services/migration/advanced_migration.py` | 1034 | blank line contains whitespace |
| 4955 | W293 | `opt/services/migration/advanced_migration.py` | 1016 | blank line contains whitespace |
| 4954 | W293 | `opt/services/migration/advanced_migration.py` | 1014 | blank line contains whitespace |
| 4953 | W293 | `opt/services/migration/advanced_migration.py` | 1008 | blank line contains whitespace |
| 4952 | W293 | `opt/services/migration/advanced_migration.py` | 1002 | blank line contains whitespace |
| 4951 | W293 | `opt/services/migration/advanced_migration.py` | 985 | blank line contains whitespace |
| 4950 | W293 | `opt/services/migration/advanced_migration.py` | 981 | blank line contains whitespace |
| 4949 | W293 | `opt/services/migration/advanced_migration.py` | 961 | blank line contains whitespace |
| 4948 | W293 | `opt/services/migration/advanced_migration.py` | 957 | blank line contains whitespace |
| 4947 | W293 | `opt/services/migration/advanced_migration.py` | 947 | blank line contains whitespace |
| 4946 | W293 | `opt/services/migration/advanced_migration.py` | 940 | blank line contains whitespace |
| 4945 | W293 | `opt/services/migration/advanced_migration.py` | 930 | blank line contains whitespace |
| 4944 | W293 | `opt/services/migration/advanced_migration.py` | 927 | blank line contains whitespace |
| 4943 | W293 | `opt/services/migration/advanced_migration.py` | 923 | blank line contains whitespace |
| 4942 | W293 | `opt/services/migration/advanced_migration.py` | 919 | blank line contains whitespace |
| 4941 | W293 | `opt/services/migration/advanced_migration.py` | 915 | blank line contains whitespace |
| 4940 | W293 | `opt/services/migration/advanced_migration.py` | 904 | blank line contains whitespace |
| 4939 | W293 | `opt/services/migration/advanced_migration.py` | 901 | blank line contains whitespace |
| 4938 | W293 | `opt/services/migration/advanced_migration.py` | 897 | blank line contains whitespace |
| 4937 | W293 | `opt/services/migration/advanced_migration.py` | 893 | blank line contains whitespace |
| 4936 | W293 | `opt/services/migration/advanced_migration.py` | 889 | blank line contains whitespace |
| 4935 | W293 | `opt/services/migration/advanced_migration.py` | 877 | blank line contains whitespace |
| 4934 | W293 | `opt/services/migration/advanced_migration.py` | 869 | blank line contains whitespace |
| 4933 | W293 | `opt/services/migration/advanced_migration.py` | 866 | blank line contains whitespace |
| 4932 | W293 | `opt/services/migration/advanced_migration.py` | 863 | blank line contains whitespace |
| 4931 | W293 | `opt/services/migration/advanced_migration.py` | 856 | blank line contains whitespace |
| 4930 | W293 | `opt/services/migration/advanced_migration.py` | 852 | blank line contains whitespace |
| 4929 | W293 | `opt/services/migration/advanced_migration.py` | 849 | blank line contains whitespace |
| 4928 | W293 | `opt/services/migration/advanced_migration.py` | 842 | blank line contains whitespace |
| 4927 | W293 | `opt/services/migration/advanced_migration.py` | 833 | blank line contains whitespace |
| 4926 | W293 | `opt/services/migration/advanced_migration.py` | 830 | blank line contains whitespace |
| 4925 | W293 | `opt/services/migration/advanced_migration.py` | 820 | blank line contains whitespace |
| 4924 | W293 | `opt/services/migration/advanced_migration.py` | 813 | blank line contains whitespace |
| 4923 | W293 | `opt/services/migration/advanced_migration.py` | 801 | blank line contains whitespace |
| 4922 | W293 | `opt/services/migration/advanced_migration.py` | 797 | blank line contains whitespace |
| 4921 | W293 | `opt/services/migration/advanced_migration.py` | 789 | blank line contains whitespace |
| 4920 | W293 | `opt/services/migration/advanced_migration.py` | 787 | blank line contains whitespace |
| 4919 | W293 | `opt/services/migration/advanced_migration.py` | 785 | blank line contains whitespace |
| 4918 | W293 | `opt/services/migration/advanced_migration.py` | 782 | blank line contains whitespace |
| 4917 | W293 | `opt/services/migration/advanced_migration.py` | 780 | blank line contains whitespace |
| 4916 | W293 | `opt/services/migration/advanced_migration.py` | 772 | blank line contains whitespace |
| 4915 | W293 | `opt/services/migration/advanced_migration.py` | 767 | blank line contains whitespace |
| 4914 | W293 | `opt/services/migration/advanced_migration.py` | 764 | blank line contains whitespace |
| 4913 | W293 | `opt/services/migration/advanced_migration.py` | 756 | blank line contains whitespace |
| 4912 | W293 | `opt/services/migration/advanced_migration.py` | 753 | blank line contains whitespace |
| 4911 | W293 | `opt/services/migration/advanced_migration.py` | 747 | blank line contains whitespace |
| 4910 | W293 | `opt/services/migration/advanced_migration.py` | 743 | blank line contains whitespace |
| 4909 | W293 | `opt/services/migration/advanced_migration.py` | 735 | blank line contains whitespace |
| 4908 | W293 | `opt/services/migration/advanced_migration.py` | 722 | blank line contains whitespace |
| 4907 | W293 | `opt/services/migration/advanced_migration.py` | 718 | blank line contains whitespace |
| 4906 | W293 | `opt/services/migration/advanced_migration.py` | 714 | blank line contains whitespace |
| 4905 | W293 | `opt/services/migration/advanced_migration.py` | 710 | blank line contains whitespace |
| 4904 | W293 | `opt/services/migration/advanced_migration.py` | 707 | blank line contains whitespace |
| 4903 | W293 | `opt/services/migration/advanced_migration.py` | 702 | blank line contains whitespace |
| 4902 | W293 | `opt/services/migration/advanced_migration.py` | 699 | blank line contains whitespace |
| 4901 | W293 | `opt/services/migration/advanced_migration.py` | 696 | blank line contains whitespace |
| 4900 | W293 | `opt/services/migration/advanced_migration.py` | 694 | blank line contains whitespace |
| 4899 | W293 | `opt/services/migration/advanced_migration.py` | 690 | blank line contains whitespace |
| 4898 | W293 | `opt/services/migration/advanced_migration.py` | 681 | blank line contains whitespace |
| 4897 | W293 | `opt/services/migration/advanced_migration.py` | 678 | blank line contains whitespace |
| 4896 | W293 | `opt/services/migration/advanced_migration.py` | 674 | blank line contains whitespace |
| 4895 | W293 | `opt/services/migration/advanced_migration.py` | 668 | blank line contains whitespace |
| 4894 | W293 | `opt/services/migration/advanced_migration.py` | 665 | blank line contains whitespace |
| 4893 | W293 | `opt/services/migration/advanced_migration.py` | 662 | blank line contains whitespace |
| 4892 | W293 | `opt/services/migration/advanced_migration.py` | 658 | blank line contains whitespace |
| 4891 | W293 | `opt/services/migration/advanced_migration.py` | 656 | blank line contains whitespace |
| 4890 | W293 | `opt/services/migration/advanced_migration.py` | 651 | blank line contains whitespace |
| 4889 | W293 | `opt/services/migration/advanced_migration.py` | 643 | blank line contains whitespace |
| 4888 | W293 | `opt/services/migration/advanced_migration.py` | 639 | blank line contains whitespace |
| 4887 | W293 | `opt/services/migration/advanced_migration.py` | 635 | blank line contains whitespace |
| 4886 | W293 | `opt/services/migration/advanced_migration.py` | 632 | blank line contains whitespace |
| 4885 | W293 | `opt/services/migration/advanced_migration.py` | 627 | blank line contains whitespace |
| 4884 | W293 | `opt/services/migration/advanced_migration.py` | 623 | blank line contains whitespace |
| 4883 | W293 | `opt/services/migration/advanced_migration.py` | 620 | blank line contains whitespace |
| 4882 | W293 | `opt/services/migration/advanced_migration.py` | 616 | blank line contains whitespace |
| 4881 | W293 | `opt/services/migration/advanced_migration.py` | 607 | blank line contains whitespace |
| 4880 | W293 | `opt/services/migration/advanced_migration.py` | 602 | blank line contains whitespace |
| 4879 | W293 | `opt/services/migration/advanced_migration.py` | 598 | blank line contains whitespace |
| 4878 | W293 | `opt/services/migration/advanced_migration.py` | 594 | blank line contains whitespace |
| 4877 | W293 | `opt/services/migration/advanced_migration.py` | 590 | blank line contains whitespace |
| 4876 | W293 | `opt/services/migration/advanced_migration.py` | 588 | blank line contains whitespace |
| 4875 | W293 | `opt/services/migration/advanced_migration.py` | 582 | blank line contains whitespace |
| 4874 | W293 | `opt/services/migration/advanced_migration.py` | 578 | blank line contains whitespace |
| 4873 | W293 | `opt/services/migration/advanced_migration.py` | 572 | blank line contains whitespace |
| 4872 | W293 | `opt/services/migration/advanced_migration.py` | 569 | blank line contains whitespace |
| 4871 | W293 | `opt/services/migration/advanced_migration.py` | 557 | blank line contains whitespace |
| 4870 | W293 | `opt/services/migration/advanced_migration.py` | 552 | blank line contains whitespace |
| 4869 | W293 | `opt/services/migration/advanced_migration.py` | 547 | blank line contains whitespace |
| 4868 | W293 | `opt/services/migration/advanced_migration.py` | 538 | blank line contains whitespace |
| 4867 | W293 | `opt/services/migration/advanced_migration.py` | 534 | blank line contains whitespace |
| 4866 | W293 | `opt/services/migration/advanced_migration.py` | 524 | blank line contains whitespace |
| 4865 | W293 | `opt/services/migration/advanced_migration.py` | 517 | blank line contains whitespace |
| 4864 | W293 | `opt/services/migration/advanced_migration.py` | 491 | blank line contains whitespace |
| 4863 | W293 | `opt/services/migration/advanced_migration.py` | 489 | blank line contains whitespace |
| 4862 | W293 | `opt/services/migration/advanced_migration.py` | 485 | blank line contains whitespace |
| 4861 | W293 | `opt/services/migration/advanced_migration.py` | 481 | blank line contains whitespace |
| 4860 | W293 | `opt/services/migration/advanced_migration.py` | 479 | blank line contains whitespace |
| 4859 | W293 | `opt/services/migration/advanced_migration.py` | 473 | blank line contains whitespace |
| 4858 | W293 | `opt/services/migration/advanced_migration.py` | 467 | blank line contains whitespace |
| 4857 | W293 | `opt/services/migration/advanced_migration.py` | 457 | blank line contains whitespace |
| 4856 | W293 | `opt/services/migration/advanced_migration.py` | 449 | blank line contains whitespace |
| 4855 | W293 | `opt/services/migration/advanced_migration.py` | 446 | blank line contains whitespace |
| 4854 | W293 | `opt/services/migration/advanced_migration.py` | 432 | blank line contains whitespace |
| 4853 | W293 | `opt/services/migration/advanced_migration.py` | 429 | blank line contains whitespace |
| 4852 | W293 | `opt/services/migration/advanced_migration.py` | 423 | blank line contains whitespace |
| 4851 | W293 | `opt/services/migration/advanced_migration.py` | 409 | blank line contains whitespace |
| 4850 | W293 | `opt/services/migration/advanced_migration.py` | 386 | blank line contains whitespace |
| 4849 | W293 | `opt/services/migration/advanced_migration.py` | 382 | blank line contains whitespace |
| 4848 | W293 | `opt/services/migration/advanced_migration.py` | 379 | blank line contains whitespace |
| 4847 | W293 | `opt/services/migration/advanced_migration.py` | 376 | blank line contains whitespace |
| 4846 | W293 | `opt/services/migration/advanced_migration.py` | 367 | blank line contains whitespace |
| 4845 | W293 | `opt/services/migration/advanced_migration.py` | 360 | blank line contains whitespace |
| 4844 | W293 | `opt/services/migration/advanced_migration.py` | 348 | blank line contains whitespace |
| 4843 | W293 | `opt/services/migration/advanced_migration.py` | 344 | blank line contains whitespace |
| 4842 | W293 | `opt/services/migration/advanced_migration.py` | 340 | blank line contains whitespace |
| 4841 | W293 | `opt/services/migration/advanced_migration.py` | 336 | blank line contains whitespace |
| 4840 | W293 | `opt/services/migration/advanced_migration.py` | 332 | blank line contains whitespace |
| 4839 | W293 | `opt/services/migration/advanced_migration.py` | 325 | blank line contains whitespace |
| 4838 | W293 | `opt/services/migration/advanced_migration.py` | 317 | blank line contains whitespace |
| 4837 | W293 | `opt/services/migration/advanced_migration.py` | 310 | blank line contains whitespace |
| 4836 | W293 | `opt/services/migration/advanced_migration.py` | 300 | blank line contains whitespace |
| 4835 | W293 | `opt/services/migration/advanced_migration.py` | 293 | blank line contains whitespace |
| 4834 | W293 | `opt/services/migration/advanced_migration.py` | 287 | blank line contains whitespace |
| 4833 | W293 | `opt/services/migration/advanced_migration.py` | 283 | blank line contains whitespace |
| 4832 | W293 | `opt/services/migration/advanced_migration.py` | 279 | blank line contains whitespace |
| 4831 | W293 | `opt/services/migration/advanced_migration.py` | 277 | blank line contains whitespace |
| 4830 | W293 | `opt/services/migration/advanced_migration.py` | 270 | blank line contains whitespace |
| 4829 | W293 | `opt/services/migration/advanced_migration.py` | 264 | blank line contains whitespace |
| 4828 | W293 | `opt/services/migration/advanced_migration.py` | 255 | blank line contains whitespace |
| 4827 | W293 | `opt/services/migration/advanced_migration.py` | 248 | blank line contains whitespace |
| 4826 | W293 | `opt/services/migration/advanced_migration.py` | 245 | blank line contains whitespace |
| 4825 | W293 | `opt/services/migration/advanced_migration.py` | 236 | blank line contains whitespace |
| 4824 | W293 | `opt/services/migration/advanced_migration.py` | 227 | blank line contains whitespace |
| 4823 | W293 | `opt/services/migration/advanced_migration.py` | 224 | blank line contains whitespace |
| 4822 | W293 | `opt/services/migration/advanced_migration.py` | 221 | blank line contains whitespace |
| 4821 | W293 | `opt/services/migration/advanced_migration.py` | 212 | blank line contains whitespace |
| 4820 | W293 | `opt/services/migration/advanced_migration.py` | 207 | blank line contains whitespace |
| 4819 | W293 | `opt/services/migration/advanced_migration.py` | 204 | blank line contains whitespace |
| 4818 | W293 | `opt/services/migration/advanced_migration.py` | 200 | blank line contains whitespace |
| 4817 | W293 | `opt/services/migration/advanced_migration.py` | 195 | blank line contains whitespace |
| 4816 | W293 | `opt/services/migration/advanced_migration.py` | 188 | blank line contains whitespace |
| 4810 | W293 | `opt/services/message_queue.py` | 277 | blank line contains whitespace |
| 4809 | W293 | `opt/services/message_queue.py` | 265 | blank line contains whitespace |
| 4808 | W293 | `opt/services/message_queue.py` | 260 | blank line contains whitespace |
| 4807 | W293 | `opt/services/message_queue.py` | 256 | blank line contains whitespace |
| 4806 | W293 | `opt/services/message_queue.py` | 230 | blank line contains whitespace |
| 4805 | W293 | `opt/services/message_queue.py` | 202 | blank line contains whitespace |
| 4804 | W293 | `opt/services/message_queue.py` | 196 | blank line contains whitespace |
| 4803 | W293 | `opt/services/message_queue.py` | 193 | blank line contains whitespace |
| 4802 | W293 | `opt/services/message_queue.py` | 191 | blank line contains whitespace |
| 4801 | W293 | `opt/services/message_queue.py` | 183 | blank line contains whitespace |
| 4800 | W293 | `opt/services/message_queue.py` | 171 | blank line contains whitespace |
| 4799 | W293 | `opt/services/message_queue.py` | 167 | blank line contains whitespace |
| 4798 | W293 | `opt/services/message_queue.py` | 153 | blank line contains whitespace |
| 4797 | W293 | `opt/services/message_queue.py` | 150 | blank line contains whitespace |
| 4796 | W293 | `opt/services/message_queue.py` | 139 | blank line contains whitespace |
| 4795 | W293 | `opt/services/message_queue.py` | 136 | blank line contains whitespace |
| 4794 | W293 | `opt/services/message_queue.py` | 117 | blank line contains whitespace |
| 4793 | W293 | `opt/services/message_queue.py` | 104 | blank line contains whitespace |
| 4792 | W293 | `opt/services/message_queue.py` | 94 | blank line contains whitespace |
| 4791 | W293 | `opt/services/message_queue.py` | 89 | blank line contains whitespace |
| 4790 | W293 | `opt/services/message_queue.py` | 83 | blank line contains whitespace |
| 4789 | W293 | `opt/services/message_queue.py` | 79 | blank line contains whitespace |
| 4788 | W293 | `opt/services/message_queue.py` | 65 | blank line contains whitespace |
| 4787 | W293 | `opt/services/message_queue.py` | 62 | blank line contains whitespace |
| 4786 | W293 | `opt/services/message_queue.py` | 46 | blank line contains whitespace |
| 4785 | W293 | `opt/services/message_queue.py` | 37 | blank line contains whitespace |
| 4784 | W293 | `opt/services/message_queue.py` | 33 | blank line contains whitespace |
| 4783 | W293 | `opt/services/marketplace/marketplace_service.py` | 1210 | blank line contains whitespace |
| 4782 | W293 | `opt/services/marketplace/marketplace_service.py` | 1204 | blank line contains whitespace |
| 4781 | W293 | `opt/services/marketplace/marketplace_service.py` | 1201 | blank line contains whitespace |
| 4780 | W293 | `opt/services/marketplace/marketplace_service.py` | 1196 | blank line contains whitespace |
| 4779 | W293 | `opt/services/marketplace/marketplace_service.py` | 1191 | blank line contains whitespace |
| 4778 | W293 | `opt/services/marketplace/marketplace_service.py` | 1171 | blank line contains whitespace |
| 4777 | W293 | `opt/services/marketplace/marketplace_service.py` | 1145 | blank line contains whitespace |
| 4776 | W293 | `opt/services/marketplace/marketplace_service.py` | 1143 | blank line contains whitespace |
| 4775 | W293 | `opt/services/marketplace/marketplace_service.py` | 1139 | blank line contains whitespace |
| 4774 | W293 | `opt/services/marketplace/marketplace_service.py` | 1135 | blank line contains whitespace |
| 4773 | W293 | `opt/services/marketplace/marketplace_service.py` | 1133 | blank line contains whitespace |
| 4771 | W293 | `opt/services/marketplace/marketplace_service.py` | 1121 | blank line contains whitespace |
| 4770 | W293 | `opt/services/marketplace/marketplace_service.py` | 1117 | blank line contains whitespace |
| 4769 | W293 | `opt/services/marketplace/marketplace_service.py` | 1113 | blank line contains whitespace |
| 4768 | W293 | `opt/services/marketplace/marketplace_service.py` | 1108 | blank line contains whitespace |
| 4767 | W293 | `opt/services/marketplace/marketplace_service.py` | 1104 | blank line contains whitespace |
| 4766 | W293 | `opt/services/marketplace/marketplace_service.py` | 1098 | blank line contains whitespace |
| 4765 | W293 | `opt/services/marketplace/marketplace_service.py` | 1094 | blank line contains whitespace |
| 4764 | W293 | `opt/services/marketplace/marketplace_service.py` | 1089 | blank line contains whitespace |
| 4763 | W293 | `opt/services/marketplace/marketplace_service.py` | 1085 | blank line contains whitespace |
| 4762 | W293 | `opt/services/marketplace/marketplace_service.py` | 1078 | blank line contains whitespace |
| 4761 | W293 | `opt/services/marketplace/marketplace_service.py` | 1067 | blank line contains whitespace |
| 4760 | W293 | `opt/services/marketplace/marketplace_service.py` | 1061 | blank line contains whitespace |
| 4759 | W293 | `opt/services/marketplace/marketplace_service.py` | 1059 | blank line contains whitespace |
| 4758 | W293 | `opt/services/marketplace/marketplace_service.py` | 1053 | blank line contains whitespace |
| 4757 | W293 | `opt/services/marketplace/marketplace_service.py` | 1046 | blank line contains whitespace |
| 4756 | W293 | `opt/services/marketplace/marketplace_service.py` | 1042 | blank line contains whitespace |
| 4755 | W293 | `opt/services/marketplace/marketplace_service.py` | 1040 | blank line contains whitespace |
| 4754 | W293 | `opt/services/marketplace/marketplace_service.py` | 1028 | blank line contains whitespace |
| 4753 | W293 | `opt/services/marketplace/marketplace_service.py` | 1021 | blank line contains whitespace |
| 4752 | W293 | `opt/services/marketplace/marketplace_service.py` | 1011 | blank line contains whitespace |
| 4751 | W293 | `opt/services/marketplace/marketplace_service.py` | 1009 | blank line contains whitespace |
| 4750 | W293 | `opt/services/marketplace/marketplace_service.py` | 1004 | blank line contains whitespace |
| 4749 | W293 | `opt/services/marketplace/marketplace_service.py` | 1001 | blank line contains whitespace |
| 4748 | W293 | `opt/services/marketplace/marketplace_service.py` | 989 | blank line contains whitespace |
| 4747 | W293 | `opt/services/marketplace/marketplace_service.py` | 987 | blank line contains whitespace |
| 4746 | W293 | `opt/services/marketplace/marketplace_service.py` | 980 | blank line contains whitespace |
| 4745 | W293 | `opt/services/marketplace/marketplace_service.py` | 970 | blank line contains whitespace |
| 4744 | W293 | `opt/services/marketplace/marketplace_service.py` | 967 | blank line contains whitespace |
| 4743 | W293 | `opt/services/marketplace/marketplace_service.py` | 963 | blank line contains whitespace |
| 4742 | W293 | `opt/services/marketplace/marketplace_service.py` | 960 | blank line contains whitespace |
| 4741 | W293 | `opt/services/marketplace/marketplace_service.py` | 949 | blank line contains whitespace |
| 4740 | W293 | `opt/services/marketplace/marketplace_service.py` | 944 | blank line contains whitespace |
| 4739 | W293 | `opt/services/marketplace/marketplace_service.py` | 940 | blank line contains whitespace |
| 4738 | W293 | `opt/services/marketplace/marketplace_service.py` | 926 | blank line contains whitespace |
| 4737 | W293 | `opt/services/marketplace/marketplace_service.py` | 922 | blank line contains whitespace |
| 4736 | W293 | `opt/services/marketplace/marketplace_service.py` | 917 | blank line contains whitespace |
| 4735 | W293 | `opt/services/marketplace/marketplace_service.py` | 910 | blank line contains whitespace |
| 4734 | W293 | `opt/services/marketplace/marketplace_service.py` | 905 | blank line contains whitespace |
| 4733 | W293 | `opt/services/marketplace/marketplace_service.py` | 903 | blank line contains whitespace |
| 4732 | W293 | `opt/services/marketplace/marketplace_service.py` | 896 | blank line contains whitespace |
| 4731 | W293 | `opt/services/marketplace/marketplace_service.py` | 893 | blank line contains whitespace |
| 4730 | W293 | `opt/services/marketplace/marketplace_service.py` | 890 | blank line contains whitespace |
| 4729 | W293 | `opt/services/marketplace/marketplace_service.py` | 881 | blank line contains whitespace |
| 4728 | W293 | `opt/services/marketplace/marketplace_service.py` | 878 | blank line contains whitespace |
| 4727 | W293 | `opt/services/marketplace/marketplace_service.py` | 869 | blank line contains whitespace |
| 4726 | W293 | `opt/services/marketplace/marketplace_service.py` | 862 | blank line contains whitespace |
| 4725 | W293 | `opt/services/marketplace/marketplace_service.py` | 858 | blank line contains whitespace |
| 4724 | W293 | `opt/services/marketplace/marketplace_service.py` | 848 | blank line contains whitespace |
| 4723 | W293 | `opt/services/marketplace/marketplace_service.py` | 842 | blank line contains whitespace |
| 4722 | W293 | `opt/services/marketplace/marketplace_service.py` | 831 | blank line contains whitespace |
| 4721 | W293 | `opt/services/marketplace/marketplace_service.py` | 828 | blank line contains whitespace |
| 4720 | W293 | `opt/services/marketplace/marketplace_service.py` | 824 | blank line contains whitespace |
| 4719 | W293 | `opt/services/marketplace/marketplace_service.py` | 818 | blank line contains whitespace |
| 4718 | W293 | `opt/services/marketplace/marketplace_service.py` | 811 | blank line contains whitespace |
| 4717 | W293 | `opt/services/marketplace/marketplace_service.py` | 807 | blank line contains whitespace |
| 4716 | W293 | `opt/services/marketplace/marketplace_service.py` | 805 | blank line contains whitespace |
| 4715 | W293 | `opt/services/marketplace/marketplace_service.py` | 792 | blank line contains whitespace |
| 4714 | W293 | `opt/services/marketplace/marketplace_service.py` | 788 | blank line contains whitespace |
| 4713 | W293 | `opt/services/marketplace/marketplace_service.py` | 782 | blank line contains whitespace |
| 4712 | W293 | `opt/services/marketplace/marketplace_service.py` | 777 | blank line contains whitespace |
| 4711 | W293 | `opt/services/marketplace/marketplace_service.py` | 764 | blank line contains whitespace |
| 4710 | W293 | `opt/services/marketplace/marketplace_service.py` | 758 | blank line contains whitespace |
| 4709 | W293 | `opt/services/marketplace/marketplace_service.py` | 752 | blank line contains whitespace |
| 4708 | W293 | `opt/services/marketplace/marketplace_service.py` | 746 | blank line contains whitespace |
| 4707 | W293 | `opt/services/marketplace/marketplace_service.py` | 738 | blank line contains whitespace |
| 4706 | W293 | `opt/services/marketplace/marketplace_service.py` | 734 | blank line contains whitespace |
| 4705 | W293 | `opt/services/marketplace/marketplace_service.py` | 730 | blank line contains whitespace |
| 4704 | W293 | `opt/services/marketplace/marketplace_service.py` | 724 | blank line contains whitespace |
| 4703 | W293 | `opt/services/marketplace/marketplace_service.py` | 718 | blank line contains whitespace |
| 4702 | W293 | `opt/services/marketplace/marketplace_service.py` | 709 | blank line contains whitespace |
| 4701 | W293 | `opt/services/marketplace/marketplace_service.py` | 700 | blank line contains whitespace |
| 4700 | W293 | `opt/services/marketplace/marketplace_service.py` | 695 | blank line contains whitespace |
| 4699 | W293 | `opt/services/marketplace/marketplace_service.py` | 689 | blank line contains whitespace |
| 4698 | W293 | `opt/services/marketplace/marketplace_service.py` | 642 | blank line contains whitespace |
| 4697 | W293 | `opt/services/marketplace/marketplace_service.py` | 638 | blank line contains whitespace |
| 4696 | W293 | `opt/services/marketplace/marketplace_service.py` | 634 | blank line contains whitespace |
| 4695 | W293 | `opt/services/marketplace/marketplace_service.py` | 627 | blank line contains whitespace |
| 4694 | W293 | `opt/services/marketplace/marketplace_service.py` | 621 | blank line contains whitespace |
| 4693 | W293 | `opt/services/marketplace/marketplace_service.py` | 618 | blank line contains whitespace |
| 4692 | W293 | `opt/services/marketplace/marketplace_service.py` | 614 | blank line contains whitespace |
| 4691 | W293 | `opt/services/marketplace/marketplace_service.py` | 611 | blank line contains whitespace |
| 4690 | W293 | `opt/services/marketplace/marketplace_service.py` | 605 | blank line contains whitespace |
| 4689 | W293 | `opt/services/marketplace/marketplace_service.py` | 600 | blank line contains whitespace |
| 4688 | W293 | `opt/services/marketplace/marketplace_service.py` | 594 | blank line contains whitespace |
| 4687 | W293 | `opt/services/marketplace/marketplace_service.py` | 571 | blank line contains whitespace |
| 4686 | W293 | `opt/services/marketplace/marketplace_service.py` | 561 | blank line contains whitespace |
| 4685 | W293 | `opt/services/marketplace/marketplace_service.py` | 555 | blank line contains whitespace |
| 4684 | W293 | `opt/services/marketplace/marketplace_service.py` | 553 | blank line contains whitespace |
| 4683 | W293 | `opt/services/marketplace/marketplace_service.py` | 545 | blank line contains whitespace |
| 4682 | W293 | `opt/services/marketplace/marketplace_service.py` | 536 | blank line contains whitespace |
| 4681 | W293 | `opt/services/marketplace/marketplace_service.py` | 534 | blank line contains whitespace |
| 4680 | W293 | `opt/services/marketplace/marketplace_service.py` | 532 | blank line contains whitespace |
| 4679 | W293 | `opt/services/marketplace/marketplace_service.py` | 524 | blank line contains whitespace |
| 4678 | W293 | `opt/services/marketplace/marketplace_service.py` | 518 | blank line contains whitespace |
| 4677 | W293 | `opt/services/marketplace/marketplace_service.py` | 512 | blank line contains whitespace |
| 4676 | W293 | `opt/services/marketplace/marketplace_service.py` | 507 | blank line contains whitespace |
| 4675 | W293 | `opt/services/marketplace/marketplace_service.py` | 502 | blank line contains whitespace |
| 4674 | W293 | `opt/services/marketplace/marketplace_service.py` | 498 | blank line contains whitespace |
| 4673 | W293 | `opt/services/marketplace/marketplace_service.py` | 495 | blank line contains whitespace |
| 4672 | W293 | `opt/services/marketplace/marketplace_service.py` | 489 | blank line contains whitespace |
| 4671 | W293 | `opt/services/marketplace/marketplace_service.py` | 486 | blank line contains whitespace |
| 4670 | W293 | `opt/services/marketplace/marketplace_service.py` | 478 | blank line contains whitespace |
| 4669 | W293 | `opt/services/marketplace/marketplace_service.py` | 474 | blank line contains whitespace |
| 4668 | W293 | `opt/services/marketplace/marketplace_service.py` | 468 | blank line contains whitespace |
| 4667 | W293 | `opt/services/marketplace/marketplace_service.py` | 453 | blank line contains whitespace |
| 4666 | W293 | `opt/services/marketplace/marketplace_service.py` | 446 | blank line contains whitespace |
| 4665 | W293 | `opt/services/marketplace/marketplace_service.py` | 436 | blank line contains whitespace |
| 4664 | W293 | `opt/services/marketplace/marketplace_service.py` | 433 | blank line contains whitespace |
| 4663 | W293 | `opt/services/marketplace/marketplace_service.py` | 422 | blank line contains whitespace |
| 4662 | W293 | `opt/services/marketplace/marketplace_service.py` | 416 | blank line contains whitespace |
| 4661 | W293 | `opt/services/marketplace/marketplace_service.py` | 409 | blank line contains whitespace |
| 4660 | W293 | `opt/services/marketplace/marketplace_service.py` | 404 | blank line contains whitespace |
| 4659 | W293 | `opt/services/marketplace/marketplace_service.py` | 399 | blank line contains whitespace |
| 4658 | W293 | `opt/services/marketplace/marketplace_service.py` | 395 | blank line contains whitespace |
| 4657 | W293 | `opt/services/marketplace/marketplace_service.py` | 393 | blank line contains whitespace |
| 4656 | W293 | `opt/services/marketplace/marketplace_service.py` | 388 | blank line contains whitespace |
| 4655 | W293 | `opt/services/marketplace/marketplace_service.py` | 384 | blank line contains whitespace |
| 4654 | W293 | `opt/services/marketplace/marketplace_service.py` | 381 | blank line contains whitespace |
| 4653 | W293 | `opt/services/marketplace/marketplace_service.py` | 359 | blank line contains whitespace |
| 4652 | W293 | `opt/services/marketplace/marketplace_service.py` | 337 | blank line contains whitespace |
| 4651 | W293 | `opt/services/marketplace/marketplace_service.py` | 326 | blank line contains whitespace |
| 4650 | W293 | `opt/services/marketplace/marketplace_service.py` | 320 | blank line contains whitespace |
| 4649 | W293 | `opt/services/marketplace/marketplace_service.py` | 307 | blank line contains whitespace |
| 4648 | W293 | `opt/services/marketplace/marketplace_service.py` | 305 | blank line contains whitespace |
| 4647 | W293 | `opt/services/marketplace/marketplace_service.py` | 297 | blank line contains whitespace |
| 4646 | W293 | `opt/services/marketplace/marketplace_service.py` | 293 | blank line contains whitespace |
| 4645 | W293 | `opt/services/marketplace/marketplace_service.py` | 289 | blank line contains whitespace |
| 4644 | W293 | `opt/services/marketplace/marketplace_service.py` | 285 | blank line contains whitespace |
| 4643 | W293 | `opt/services/marketplace/marketplace_service.py` | 277 | blank line contains whitespace |
| 4642 | W293 | `opt/services/marketplace/marketplace_service.py` | 272 | blank line contains whitespace |
| 4641 | W293 | `opt/services/marketplace/marketplace_service.py` | 245 | blank line contains whitespace |
| 4640 | W293 | `opt/services/marketplace/marketplace_service.py` | 233 | blank line contains whitespace |
| 4639 | W293 | `opt/services/marketplace/marketplace_service.py` | 221 | blank line contains whitespace |
| 4638 | W293 | `opt/services/marketplace/marketplace_service.py` | 208 | blank line contains whitespace |
| 4637 | W293 | `opt/services/marketplace/marketplace_service.py` | 203 | blank line contains whitespace |
| 4636 | W293 | `opt/services/marketplace/marketplace_service.py` | 178 | blank line contains whitespace |
| 4635 | W293 | `opt/services/marketplace/marketplace_service.py` | 175 | blank line contains whitespace |
| 4634 | W293 | `opt/services/marketplace/marketplace_service.py` | 171 | blank line contains whitespace |
| 4633 | W293 | `opt/services/marketplace/marketplace_service.py` | 166 | blank line contains whitespace |
| 4632 | W293 | `opt/services/marketplace/marketplace_service.py` | 160 | blank line contains whitespace |
| 4631 | W293 | `opt/services/marketplace/marketplace_service.py` | 155 | blank line contains whitespace |
| 4630 | W293 | `opt/services/marketplace/marketplace_service.py` | 104 | blank line contains whitespace |
| 4624 | W293 | `opt/services/licensing/licensing_server.py` | 785 | blank line contains whitespace |
| 4623 | W293 | `opt/services/licensing/licensing_server.py` | 773 | blank line contains whitespace |
| 4622 | W293 | `opt/services/licensing/licensing_server.py` | 758 | blank line contains whitespace |
| 4621 | W293 | `opt/services/licensing/licensing_server.py` | 754 | blank line contains whitespace |
| 4620 | W293 | `opt/services/licensing/licensing_server.py` | 752 | blank line contains whitespace |
| 4619 | W293 | `opt/services/licensing/licensing_server.py` | 747 | blank line contains whitespace |
| 4618 | W293 | `opt/services/licensing/licensing_server.py` | 740 | blank line contains whitespace |
| 4617 | W293 | `opt/services/licensing/licensing_server.py` | 709 | blank line contains whitespace |
| 4616 | W293 | `opt/services/licensing/licensing_server.py` | 706 | blank line contains whitespace |
| 4615 | W293 | `opt/services/licensing/licensing_server.py` | 701 | blank line contains whitespace |
| 4614 | W293 | `opt/services/licensing/licensing_server.py` | 693 | blank line contains whitespace |
| 4613 | W293 | `opt/services/licensing/licensing_server.py` | 689 | blank line contains whitespace |
| 4612 | W293 | `opt/services/licensing/licensing_server.py` | 684 | blank line contains whitespace |
| 4611 | W293 | `opt/services/licensing/licensing_server.py` | 682 | blank line contains whitespace |
| 4610 | W293 | `opt/services/licensing/licensing_server.py` | 677 | blank line contains whitespace |
| 4609 | W293 | `opt/services/licensing/licensing_server.py` | 668 | blank line contains whitespace |
| 4608 | W293 | `opt/services/licensing/licensing_server.py` | 661 | blank line contains whitespace |
| 4607 | W293 | `opt/services/licensing/licensing_server.py` | 655 | blank line contains whitespace |
| 4606 | W293 | `opt/services/licensing/licensing_server.py` | 650 | blank line contains whitespace |
| 4605 | W293 | `opt/services/licensing/licensing_server.py` | 641 | blank line contains whitespace |
| 4604 | W293 | `opt/services/licensing/licensing_server.py` | 634 | blank line contains whitespace |
| 4603 | W293 | `opt/services/licensing/licensing_server.py` | 627 | blank line contains whitespace |
| 4602 | W293 | `opt/services/licensing/licensing_server.py` | 623 | blank line contains whitespace |
| 4601 | W293 | `opt/services/licensing/licensing_server.py` | 617 | blank line contains whitespace |
| 4600 | W293 | `opt/services/licensing/licensing_server.py` | 610 | blank line contains whitespace |
| 4599 | W293 | `opt/services/licensing/licensing_server.py` | 608 | blank line contains whitespace |
| 4598 | W293 | `opt/services/licensing/licensing_server.py` | 603 | blank line contains whitespace |
| 4597 | W293 | `opt/services/licensing/licensing_server.py` | 596 | blank line contains whitespace |
| 4596 | W293 | `opt/services/licensing/licensing_server.py` | 594 | blank line contains whitespace |
| 4595 | W293 | `opt/services/licensing/licensing_server.py` | 581 | blank line contains whitespace |
| 4594 | W293 | `opt/services/licensing/licensing_server.py` | 572 | blank line contains whitespace |
| 4593 | W293 | `opt/services/licensing/licensing_server.py` | 560 | blank line contains whitespace |
| 4592 | W293 | `opt/services/licensing/licensing_server.py` | 558 | blank line contains whitespace |
| 4591 | W293 | `opt/services/licensing/licensing_server.py` | 552 | blank line contains whitespace |
| 4590 | W293 | `opt/services/licensing/licensing_server.py` | 550 | blank line contains whitespace |
| 4589 | W293 | `opt/services/licensing/licensing_server.py` | 542 | blank line contains whitespace |
| 4588 | W293 | `opt/services/licensing/licensing_server.py` | 536 | blank line contains whitespace |
| 4587 | W293 | `opt/services/licensing/licensing_server.py` | 517 | blank line contains whitespace |
| 4586 | W293 | `opt/services/licensing/licensing_server.py` | 507 | blank line contains whitespace |
| 4585 | W293 | `opt/services/licensing/licensing_server.py` | 501 | blank line contains whitespace |
| 4584 | W293 | `opt/services/licensing/licensing_server.py` | 498 | blank line contains whitespace |
| 4583 | W293 | `opt/services/licensing/licensing_server.py` | 488 | blank line contains whitespace |
| 4582 | W293 | `opt/services/licensing/licensing_server.py` | 486 | blank line contains whitespace |
| 4581 | W293 | `opt/services/licensing/licensing_server.py` | 474 | blank line contains whitespace |
| 4580 | W293 | `opt/services/licensing/licensing_server.py` | 472 | blank line contains whitespace |
| 4579 | W293 | `opt/services/licensing/licensing_server.py` | 466 | blank line contains whitespace |
| 4578 | W293 | `opt/services/licensing/licensing_server.py` | 461 | blank line contains whitespace |
| 4577 | W293 | `opt/services/licensing/licensing_server.py` | 452 | blank line contains whitespace |
| 4576 | W293 | `opt/services/licensing/licensing_server.py` | 443 | blank line contains whitespace |
| 4575 | W293 | `opt/services/licensing/licensing_server.py` | 438 | blank line contains whitespace |
| 4574 | W293 | `opt/services/licensing/licensing_server.py` | 433 | blank line contains whitespace |
| 4573 | W293 | `opt/services/licensing/licensing_server.py` | 426 | blank line contains whitespace |
| 4572 | W293 | `opt/services/licensing/licensing_server.py` | 423 | blank line contains whitespace |
| 4571 | W293 | `opt/services/licensing/licensing_server.py` | 419 | blank line contains whitespace |
| 4570 | W293 | `opt/services/licensing/licensing_server.py` | 410 | blank line contains whitespace |
| 4569 | W293 | `opt/services/licensing/licensing_server.py` | 407 | blank line contains whitespace |
| 4568 | W293 | `opt/services/licensing/licensing_server.py` | 391 | blank line contains whitespace |
| 4567 | W293 | `opt/services/licensing/licensing_server.py` | 385 | blank line contains whitespace |
| 4566 | W293 | `opt/services/licensing/licensing_server.py` | 378 | blank line contains whitespace |
| 4565 | W293 | `opt/services/licensing/licensing_server.py` | 373 | blank line contains whitespace |
| 4564 | W293 | `opt/services/licensing/licensing_server.py` | 367 | blank line contains whitespace |
| 4563 | W293 | `opt/services/licensing/licensing_server.py` | 364 | blank line contains whitespace |
| 4562 | W293 | `opt/services/licensing/licensing_server.py` | 360 | blank line contains whitespace |
| 4561 | W293 | `opt/services/licensing/licensing_server.py` | 356 | blank line contains whitespace |
| 4560 | W293 | `opt/services/licensing/licensing_server.py` | 350 | blank line contains whitespace |
| 4559 | W293 | `opt/services/licensing/licensing_server.py` | 338 | blank line contains whitespace |
| 4558 | W293 | `opt/services/licensing/licensing_server.py` | 324 | blank line contains whitespace |
| 4557 | W293 | `opt/services/licensing/licensing_server.py` | 311 | blank line contains whitespace |
| 4556 | W293 | `opt/services/licensing/licensing_server.py` | 307 | blank line contains whitespace |
| 4555 | W293 | `opt/services/licensing/licensing_server.py` | 303 | blank line contains whitespace |
| 4554 | W293 | `opt/services/licensing/licensing_server.py` | 292 | blank line contains whitespace |
| 4553 | W293 | `opt/services/licensing/licensing_server.py` | 278 | blank line contains whitespace |
| 4552 | W293 | `opt/services/licensing/licensing_server.py` | 263 | blank line contains whitespace |
| 4551 | W293 | `opt/services/licensing/licensing_server.py` | 258 | blank line contains whitespace |
| 4550 | W293 | `opt/services/licensing/licensing_server.py` | 249 | blank line contains whitespace |
| 4549 | W293 | `opt/services/licensing/licensing_server.py` | 243 | blank line contains whitespace |
| 4548 | W293 | `opt/services/licensing/licensing_server.py` | 239 | blank line contains whitespace |
| 4547 | W293 | `opt/services/licensing/licensing_server.py` | 234 | blank line contains whitespace |
| 4546 | W293 | `opt/services/licensing/licensing_server.py` | 230 | blank line contains whitespace |
| 4545 | W293 | `opt/services/licensing/licensing_server.py` | 225 | blank line contains whitespace |
| 4544 | W293 | `opt/services/licensing/licensing_server.py` | 222 | blank line contains whitespace |
| 4543 | W293 | `opt/services/licensing/licensing_server.py` | 214 | blank line contains whitespace |
| 4542 | W293 | `opt/services/licensing/licensing_server.py` | 181 | blank line contains whitespace |
| 4541 | W293 | `opt/services/licensing/licensing_server.py` | 159 | blank line contains whitespace |
| 4540 | W293 | `opt/services/licensing/licensing_server.py` | 129 | blank line contains whitespace |
| 4539 | W293 | `opt/services/licensing/licensing_server.py` | 123 | blank line contains whitespace |
| 4538 | W293 | `opt/services/licensing/licensing_server.py` | 71 | blank line contains whitespace |
| 4537 | W293 | `opt/services/licensing/licensing_server.py` | 65 | blank line contains whitespace |
| 4533 | W293 | `opt/services/health_check.py` | 476 | blank line contains whitespace |
| 4532 | W293 | `opt/services/health_check.py` | 472 | blank line contains whitespace |
| 4531 | W293 | `opt/services/health_check.py` | 469 | blank line contains whitespace |
| 4530 | W293 | `opt/services/health_check.py` | 465 | blank line contains whitespace |
| 4529 | W293 | `opt/services/health_check.py` | 456 | blank line contains whitespace |
| 4528 | W293 | `opt/services/health_check.py` | 444 | blank line contains whitespace |
| 4527 | W293 | `opt/services/health_check.py` | 440 | blank line contains whitespace |
| 4526 | W293 | `opt/services/health_check.py` | 436 | blank line contains whitespace |
| 4525 | W293 | `opt/services/health_check.py` | 433 | blank line contains whitespace |
| 4523 | W293 | `opt/services/health_check.py` | 428 | blank line contains whitespace |
| 4522 | W293 | `opt/services/health_check.py` | 423 | blank line contains whitespace |
| 4519 | W293 | `opt/services/health_check.py` | 410 | blank line contains whitespace |
| 4518 | W293 | `opt/services/health_check.py` | 407 | blank line contains whitespace |
| 4517 | W293 | `opt/services/health_check.py` | 398 | blank line contains whitespace |
| 4516 | W293 | `opt/services/health_check.py` | 392 | blank line contains whitespace |
| 4515 | W293 | `opt/services/health_check.py` | 384 | blank line contains whitespace |
| 4514 | W293 | `opt/services/health_check.py` | 376 | blank line contains whitespace |
| 4513 | W293 | `opt/services/health_check.py` | 372 | blank line contains whitespace |
| 4512 | W293 | `opt/services/health_check.py` | 361 | blank line contains whitespace |
| 4511 | W293 | `opt/services/health_check.py` | 357 | blank line contains whitespace |
| 4510 | W293 | `opt/services/health_check.py` | 348 | blank line contains whitespace |
| 4509 | W293 | `opt/services/health_check.py` | 345 | blank line contains whitespace |
| 4508 | W293 | `opt/services/health_check.py` | 330 | blank line contains whitespace |
| 4507 | W293 | `opt/services/health_check.py` | 323 | blank line contains whitespace |
| 4506 | W293 | `opt/services/health_check.py` | 311 | blank line contains whitespace |
| 4505 | W293 | `opt/services/health_check.py` | 293 | blank line contains whitespace |
| 4504 | W293 | `opt/services/health_check.py` | 289 | blank line contains whitespace |
| 4503 | W293 | `opt/services/health_check.py` | 275 | blank line contains whitespace |
| 4502 | W293 | `opt/services/health_check.py` | 269 | blank line contains whitespace |
| 4501 | W293 | `opt/services/health_check.py` | 262 | blank line contains whitespace |
| 4500 | W293 | `opt/services/health_check.py` | 250 | blank line contains whitespace |
| 4499 | W293 | `opt/services/health_check.py` | 245 | blank line contains whitespace |
| 4498 | W293 | `opt/services/health_check.py` | 239 | blank line contains whitespace |
| 4497 | W293 | `opt/services/health_check.py` | 225 | blank line contains whitespace |
| 4496 | W293 | `opt/services/health_check.py` | 218 | blank line contains whitespace |
| 4495 | W293 | `opt/services/health_check.py` | 199 | blank line contains whitespace |
| 4494 | W293 | `opt/services/health_check.py` | 195 | blank line contains whitespace |
| 4493 | W293 | `opt/services/health_check.py` | 189 | blank line contains whitespace |
| 4492 | W293 | `opt/services/health_check.py` | 175 | blank line contains whitespace |
| 4491 | W293 | `opt/services/health_check.py` | 168 | blank line contains whitespace |
| 4490 | W293 | `opt/services/health_check.py` | 155 | blank line contains whitespace |
| 4489 | W293 | `opt/services/health_check.py` | 151 | blank line contains whitespace |
| 4488 | W293 | `opt/services/health_check.py` | 143 | blank line contains whitespace |
| 4487 | W293 | `opt/services/health_check.py` | 129 | blank line contains whitespace |
| 4486 | W293 | `opt/services/health_check.py` | 122 | blank line contains whitespace |
| 4485 | W293 | `opt/services/health_check.py` | 108 | blank line contains whitespace |
| 4484 | W293 | `opt/services/health_check.py` | 103 | blank line contains whitespace |
| 4483 | W293 | `opt/services/health_check.py` | 87 | blank line contains whitespace |
| 4482 | W293 | `opt/services/health_check.py` | 62 | blank line contains whitespace |
| 4479 | W293 | `opt/services/ha/fencing_agent.py` | 695 | blank line contains whitespace |
| 4478 | W293 | `opt/services/ha/fencing_agent.py` | 679 | blank line contains whitespace |
| 4477 | W293 | `opt/services/ha/fencing_agent.py` | 671 | blank line contains whitespace |
| 4476 | W293 | `opt/services/ha/fencing_agent.py` | 653 | blank line contains whitespace |
| 4475 | W293 | `opt/services/ha/fencing_agent.py` | 649 | blank line contains whitespace |
| 4474 | W293 | `opt/services/ha/fencing_agent.py` | 647 | blank line contains whitespace |
| 4473 | W293 | `opt/services/ha/fencing_agent.py` | 642 | blank line contains whitespace |
| 4472 | W293 | `opt/services/ha/fencing_agent.py` | 633 | blank line contains whitespace |
| 4471 | W293 | `opt/services/ha/fencing_agent.py` | 626 | blank line contains whitespace |
| 4470 | W293 | `opt/services/ha/fencing_agent.py` | 618 | blank line contains whitespace |
| 4469 | W293 | `opt/services/ha/fencing_agent.py` | 613 | blank line contains whitespace |
| 4468 | W293 | `opt/services/ha/fencing_agent.py` | 607 | blank line contains whitespace |
| 4467 | W293 | `opt/services/ha/fencing_agent.py` | 599 | blank line contains whitespace |
| 4466 | W293 | `opt/services/ha/fencing_agent.py` | 594 | blank line contains whitespace |
| 4465 | W293 | `opt/services/ha/fencing_agent.py` | 587 | blank line contains whitespace |
| 4464 | W293 | `opt/services/ha/fencing_agent.py` | 584 | blank line contains whitespace |
| 4463 | W293 | `opt/services/ha/fencing_agent.py` | 566 | blank line contains whitespace |
| 4462 | W293 | `opt/services/ha/fencing_agent.py` | 539 | blank line contains whitespace |
| 4461 | W293 | `opt/services/ha/fencing_agent.py` | 533 | blank line contains whitespace |
| 4460 | W293 | `opt/services/ha/fencing_agent.py` | 531 | blank line contains whitespace |
| 4459 | W293 | `opt/services/ha/fencing_agent.py` | 526 | blank line contains whitespace |
| 4458 | W293 | `opt/services/ha/fencing_agent.py` | 516 | blank line contains whitespace |
| 4457 | W293 | `opt/services/ha/fencing_agent.py` | 509 | blank line contains whitespace |
| 4456 | W293 | `opt/services/ha/fencing_agent.py` | 501 | blank line contains whitespace |
| 4455 | W293 | `opt/services/ha/fencing_agent.py` | 498 | blank line contains whitespace |
| 4454 | W293 | `opt/services/ha/fencing_agent.py` | 493 | blank line contains whitespace |
| 4453 | W293 | `opt/services/ha/fencing_agent.py` | 488 | blank line contains whitespace |
| 4452 | W293 | `opt/services/ha/fencing_agent.py` | 480 | blank line contains whitespace |
| 4451 | W293 | `opt/services/ha/fencing_agent.py` | 467 | blank line contains whitespace |
| 4450 | W293 | `opt/services/ha/fencing_agent.py` | 463 | blank line contains whitespace |
| 4449 | W293 | `opt/services/ha/fencing_agent.py` | 456 | blank line contains whitespace |
| 4446 | W293 | `opt/services/ha/fencing_agent.py` | 451 | blank line contains whitespace |
| 4445 | W293 | `opt/services/ha/fencing_agent.py` | 447 | blank line contains whitespace |
| 4444 | W293 | `opt/services/ha/fencing_agent.py` | 439 | blank line contains whitespace |
| 4443 | W293 | `opt/services/ha/fencing_agent.py` | 433 | blank line contains whitespace |
| 4442 | W293 | `opt/services/ha/fencing_agent.py` | 424 | blank line contains whitespace |
| 4441 | W293 | `opt/services/ha/fencing_agent.py` | 420 | blank line contains whitespace |
| 4440 | W293 | `opt/services/ha/fencing_agent.py` | 413 | blank line contains whitespace |
| 4439 | W293 | `opt/services/ha/fencing_agent.py` | 407 | blank line contains whitespace |
| 4438 | W293 | `opt/services/ha/fencing_agent.py` | 403 | blank line contains whitespace |
| 4437 | W293 | `opt/services/ha/fencing_agent.py` | 398 | blank line contains whitespace |
| 4436 | W293 | `opt/services/ha/fencing_agent.py` | 385 | blank line contains whitespace |
| 4435 | W293 | `opt/services/ha/fencing_agent.py` | 370 | blank line contains whitespace |
| 4434 | W293 | `opt/services/ha/fencing_agent.py` | 365 | blank line contains whitespace |
| 4433 | W293 | `opt/services/ha/fencing_agent.py` | 361 | blank line contains whitespace |
| 4431 | W293 | `opt/services/ha/fencing_agent.py` | 354 | blank line contains whitespace |
| 4430 | W293 | `opt/services/ha/fencing_agent.py` | 346 | blank line contains whitespace |
| 4429 | W293 | `opt/services/ha/fencing_agent.py` | 344 | blank line contains whitespace |
| 4428 | W293 | `opt/services/ha/fencing_agent.py` | 335 | blank line contains whitespace |
| 4427 | W293 | `opt/services/ha/fencing_agent.py` | 331 | blank line contains whitespace |
| 4426 | W293 | `opt/services/ha/fencing_agent.py` | 326 | blank line contains whitespace |
| 4425 | W293 | `opt/services/ha/fencing_agent.py` | 323 | blank line contains whitespace |
| 4424 | W293 | `opt/services/ha/fencing_agent.py` | 315 | blank line contains whitespace |
| 4423 | W293 | `opt/services/ha/fencing_agent.py` | 313 | blank line contains whitespace |
| 4422 | W293 | `opt/services/ha/fencing_agent.py` | 308 | blank line contains whitespace |
| 4420 | W293 | `opt/services/ha/fencing_agent.py` | 291 | blank line contains whitespace |
| 4419 | W293 | `opt/services/ha/fencing_agent.py` | 289 | blank line contains whitespace |
| 4418 | W293 | `opt/services/ha/fencing_agent.py` | 283 | blank line contains whitespace |
| 4417 | W293 | `opt/services/ha/fencing_agent.py` | 280 | blank line contains whitespace |
| 4416 | W293 | `opt/services/ha/fencing_agent.py` | 262 | blank line contains whitespace |
| 4415 | W293 | `opt/services/ha/fencing_agent.py` | 255 | blank line contains whitespace |
| 4414 | W293 | `opt/services/ha/fencing_agent.py` | 236 | blank line contains whitespace |
| 4413 | W293 | `opt/services/ha/fencing_agent.py` | 229 | blank line contains whitespace |
| 4412 | W293 | `opt/services/ha/fencing_agent.py` | 222 | blank line contains whitespace |
| 4411 | W293 | `opt/services/ha/fencing_agent.py` | 214 | blank line contains whitespace |
| 4410 | W293 | `opt/services/ha/fencing_agent.py` | 211 | blank line contains whitespace |
| 4409 | W293 | `opt/services/ha/fencing_agent.py` | 208 | blank line contains whitespace |
| 4408 | W293 | `opt/services/ha/fencing_agent.py` | 204 | blank line contains whitespace |
| 4407 | W293 | `opt/services/ha/fencing_agent.py` | 201 | blank line contains whitespace |
| 4406 | W293 | `opt/services/ha/fencing_agent.py` | 194 | blank line contains whitespace |
| 4405 | W293 | `opt/services/ha/fencing_agent.py` | 190 | blank line contains whitespace |
| 4404 | W293 | `opt/services/ha/fencing_agent.py` | 185 | blank line contains whitespace |
| 4403 | W293 | `opt/services/ha/fencing_agent.py` | 180 | blank line contains whitespace |
| 4402 | W293 | `opt/services/ha/fencing_agent.py` | 174 | blank line contains whitespace |
| 4401 | W293 | `opt/services/ha/fencing_agent.py` | 162 | blank line contains whitespace |
| 4400 | W293 | `opt/services/ha/fencing_agent.py` | 152 | blank line contains whitespace |
| 4399 | W293 | `opt/services/ha/fencing_agent.py` | 145 | blank line contains whitespace |
| 4398 | W293 | `opt/services/ha/fencing_agent.py` | 137 | blank line contains whitespace |
| 4397 | W293 | `opt/services/ha/fencing_agent.py` | 135 | blank line contains whitespace |
| 4396 | W293 | `opt/services/ha/fencing_agent.py` | 128 | blank line contains whitespace |
| 4395 | W293 | `opt/services/ha/fencing_agent.py` | 121 | blank line contains whitespace |
| 4394 | W293 | `opt/services/ha/fencing_agent.py` | 117 | blank line contains whitespace |
| 4393 | W293 | `opt/services/ha/fencing_agent.py` | 110 | blank line contains whitespace |
| 4392 | W293 | `opt/services/ha/fencing_agent.py` | 107 | blank line contains whitespace |
| 4391 | W293 | `opt/services/ha/fencing_agent.py` | 98 | blank line contains whitespace |
| 4390 | W293 | `opt/services/ha/fencing_agent.py` | 93 | blank line contains whitespace |
| 4389 | W293 | `opt/services/fleet/federation_manager.py` | 1020 | blank line contains whitespace |
| 4387 | W293 | `opt/services/fleet/federation_manager.py` | 1013 | blank line contains whitespace |
| 4386 | W293 | `opt/services/fleet/federation_manager.py` | 1005 | blank line contains whitespace |
| 4385 | W293 | `opt/services/fleet/federation_manager.py` | 996 | blank line contains whitespace |
| 4384 | W293 | `opt/services/fleet/federation_manager.py` | 983 | blank line contains whitespace |
| 4383 | W293 | `opt/services/fleet/federation_manager.py` | 980 | blank line contains whitespace |
| 4382 | W293 | `opt/services/fleet/federation_manager.py` | 978 | blank line contains whitespace |
| 4381 | W293 | `opt/services/fleet/federation_manager.py` | 974 | blank line contains whitespace |
| 4380 | W293 | `opt/services/fleet/federation_manager.py` | 969 | blank line contains whitespace |
| 4379 | W293 | `opt/services/fleet/federation_manager.py` | 967 | blank line contains whitespace |
| 4378 | W293 | `opt/services/fleet/federation_manager.py` | 945 | blank line contains whitespace |
| 4377 | W293 | `opt/services/fleet/federation_manager.py` | 940 | blank line contains whitespace |
| 4376 | W293 | `opt/services/fleet/federation_manager.py` | 935 | blank line contains whitespace |
| 4375 | W293 | `opt/services/fleet/federation_manager.py` | 931 | blank line contains whitespace |
| 4374 | W293 | `opt/services/fleet/federation_manager.py` | 924 | blank line contains whitespace |
| 4373 | W293 | `opt/services/fleet/federation_manager.py` | 917 | blank line contains whitespace |
| 4372 | W293 | `opt/services/fleet/federation_manager.py` | 904 | blank line contains whitespace |
| 4371 | W293 | `opt/services/fleet/federation_manager.py` | 900 | blank line contains whitespace |
| 4370 | W293 | `opt/services/fleet/federation_manager.py` | 890 | blank line contains whitespace |
| 4369 | W293 | `opt/services/fleet/federation_manager.py` | 886 | blank line contains whitespace |
| 4368 | W293 | `opt/services/fleet/federation_manager.py` | 879 | blank line contains whitespace |
| 4367 | W293 | `opt/services/fleet/federation_manager.py` | 877 | blank line contains whitespace |
| 4366 | W293 | `opt/services/fleet/federation_manager.py` | 869 | blank line contains whitespace |
| 4365 | W293 | `opt/services/fleet/federation_manager.py` | 864 | blank line contains whitespace |
| 4364 | W293 | `opt/services/fleet/federation_manager.py` | 859 | blank line contains whitespace |
| 4363 | W293 | `opt/services/fleet/federation_manager.py` | 852 | blank line contains whitespace |
| 4362 | W293 | `opt/services/fleet/federation_manager.py` | 847 | blank line contains whitespace |
| 4361 | W293 | `opt/services/fleet/federation_manager.py` | 839 | blank line contains whitespace |
| 4360 | W293 | `opt/services/fleet/federation_manager.py` | 837 | blank line contains whitespace |
| 4359 | W293 | `opt/services/fleet/federation_manager.py` | 832 | blank line contains whitespace |
| 4358 | W293 | `opt/services/fleet/federation_manager.py` | 828 | blank line contains whitespace |
| 4357 | W293 | `opt/services/fleet/federation_manager.py` | 820 | blank line contains whitespace |
| 4356 | W293 | `opt/services/fleet/federation_manager.py` | 813 | blank line contains whitespace |
| 4355 | W293 | `opt/services/fleet/federation_manager.py` | 809 | blank line contains whitespace |
| 4354 | W293 | `opt/services/fleet/federation_manager.py` | 805 | blank line contains whitespace |
| 4353 | W293 | `opt/services/fleet/federation_manager.py` | 799 | blank line contains whitespace |
| 4352 | W293 | `opt/services/fleet/federation_manager.py` | 795 | blank line contains whitespace |
| 4351 | W293 | `opt/services/fleet/federation_manager.py` | 790 | blank line contains whitespace |
| 4350 | W293 | `opt/services/fleet/federation_manager.py` | 770 | blank line contains whitespace |
| 4349 | W293 | `opt/services/fleet/federation_manager.py` | 767 | blank line contains whitespace |
| 4348 | W293 | `opt/services/fleet/federation_manager.py` | 762 | blank line contains whitespace |
| 4347 | W293 | `opt/services/fleet/federation_manager.py` | 757 | blank line contains whitespace |
| 4346 | W293 | `opt/services/fleet/federation_manager.py` | 750 | blank line contains whitespace |
| 4345 | W293 | `opt/services/fleet/federation_manager.py` | 743 | blank line contains whitespace |
| 4344 | W293 | `opt/services/fleet/federation_manager.py` | 739 | blank line contains whitespace |
| 4343 | W293 | `opt/services/fleet/federation_manager.py` | 734 | blank line contains whitespace |
| 4342 | W293 | `opt/services/fleet/federation_manager.py` | 730 | blank line contains whitespace |
| 4341 | W293 | `opt/services/fleet/federation_manager.py` | 702 | blank line contains whitespace |
| 4340 | W293 | `opt/services/fleet/federation_manager.py` | 698 | blank line contains whitespace |
| 4339 | W293 | `opt/services/fleet/federation_manager.py` | 692 | blank line contains whitespace |
| 4338 | W293 | `opt/services/fleet/federation_manager.py` | 652 | blank line contains whitespace |
| 4337 | W293 | `opt/services/fleet/federation_manager.py` | 650 | blank line contains whitespace |
| 4336 | W293 | `opt/services/fleet/federation_manager.py` | 645 | blank line contains whitespace |
| 4335 | W293 | `opt/services/fleet/federation_manager.py` | 640 | blank line contains whitespace |
| 4334 | W293 | `opt/services/fleet/federation_manager.py` | 637 | blank line contains whitespace |
| 4333 | W293 | `opt/services/fleet/federation_manager.py` | 631 | blank line contains whitespace |
| 4332 | W293 | `opt/services/fleet/federation_manager.py` | 615 | blank line contains whitespace |
| 4331 | W293 | `opt/services/fleet/federation_manager.py` | 612 | blank line contains whitespace |
| 4330 | W293 | `opt/services/fleet/federation_manager.py` | 609 | blank line contains whitespace |
| 4329 | W293 | `opt/services/fleet/federation_manager.py` | 600 | blank line contains whitespace |
| 4328 | W293 | `opt/services/fleet/federation_manager.py` | 598 | blank line contains whitespace |
| 4327 | W293 | `opt/services/fleet/federation_manager.py` | 593 | blank line contains whitespace |
| 4326 | W293 | `opt/services/fleet/federation_manager.py` | 588 | blank line contains whitespace |
| 4325 | W293 | `opt/services/fleet/federation_manager.py` | 583 | blank line contains whitespace |
| 4324 | W293 | `opt/services/fleet/federation_manager.py` | 578 | blank line contains whitespace |
| 4323 | W293 | `opt/services/fleet/federation_manager.py` | 574 | blank line contains whitespace |
| 4322 | W293 | `opt/services/fleet/federation_manager.py` | 571 | blank line contains whitespace |
| 4321 | W293 | `opt/services/fleet/federation_manager.py` | 565 | blank line contains whitespace |
| 4320 | W293 | `opt/services/fleet/federation_manager.py` | 561 | blank line contains whitespace |
| 4319 | W293 | `opt/services/fleet/federation_manager.py` | 557 | blank line contains whitespace |
| 4318 | W293 | `opt/services/fleet/federation_manager.py` | 552 | blank line contains whitespace |
| 4317 | W293 | `opt/services/fleet/federation_manager.py` | 546 | blank line contains whitespace |
| 4316 | W293 | `opt/services/fleet/federation_manager.py` | 540 | blank line contains whitespace |
| 4315 | W293 | `opt/services/fleet/federation_manager.py` | 530 | blank line contains whitespace |
| 4314 | W293 | `opt/services/fleet/federation_manager.py` | 519 | blank line contains whitespace |
| 4313 | W293 | `opt/services/fleet/federation_manager.py` | 510 | blank line contains whitespace |
| 4312 | W293 | `opt/services/fleet/federation_manager.py` | 505 | blank line contains whitespace |
| 4311 | W293 | `opt/services/fleet/federation_manager.py` | 498 | blank line contains whitespace |
| 4310 | W293 | `opt/services/fleet/federation_manager.py` | 494 | blank line contains whitespace |
| 4309 | W293 | `opt/services/fleet/federation_manager.py` | 487 | blank line contains whitespace |
| 4308 | W293 | `opt/services/fleet/federation_manager.py` | 482 | blank line contains whitespace |
| 4307 | W293 | `opt/services/fleet/federation_manager.py` | 480 | blank line contains whitespace |
| 4306 | W293 | `opt/services/fleet/federation_manager.py` | 477 | blank line contains whitespace |
| 4305 | W293 | `opt/services/fleet/federation_manager.py` | 475 | blank line contains whitespace |
| 4304 | W293 | `opt/services/fleet/federation_manager.py` | 472 | blank line contains whitespace |
| 4303 | W293 | `opt/services/fleet/federation_manager.py` | 468 | blank line contains whitespace |
| 4302 | W293 | `opt/services/fleet/federation_manager.py` | 464 | blank line contains whitespace |
| 4301 | W293 | `opt/services/fleet/federation_manager.py` | 459 | blank line contains whitespace |
| 4300 | W293 | `opt/services/fleet/federation_manager.py` | 442 | blank line contains whitespace |
| 4299 | W293 | `opt/services/fleet/federation_manager.py` | 436 | blank line contains whitespace |
| 4298 | W293 | `opt/services/fleet/federation_manager.py` | 428 | blank line contains whitespace |
| 4297 | W293 | `opt/services/fleet/federation_manager.py` | 423 | blank line contains whitespace |
| 4296 | W293 | `opt/services/fleet/federation_manager.py` | 420 | blank line contains whitespace |
| 4295 | W293 | `opt/services/fleet/federation_manager.py` | 416 | blank line contains whitespace |
| 4294 | W293 | `opt/services/fleet/federation_manager.py` | 411 | blank line contains whitespace |
| 4293 | W293 | `opt/services/fleet/federation_manager.py` | 405 | blank line contains whitespace |
| 4292 | W293 | `opt/services/fleet/federation_manager.py` | 402 | blank line contains whitespace |
| 4291 | W293 | `opt/services/fleet/federation_manager.py` | 398 | blank line contains whitespace |
| 4290 | W293 | `opt/services/fleet/federation_manager.py` | 386 | blank line contains whitespace |
| 4289 | W293 | `opt/services/fleet/federation_manager.py` | 383 | blank line contains whitespace |
| 4288 | W293 | `opt/services/fleet/federation_manager.py` | 378 | blank line contains whitespace |
| 4287 | W293 | `opt/services/fleet/federation_manager.py` | 374 | blank line contains whitespace |
| 4286 | W293 | `opt/services/fleet/federation_manager.py` | 358 | blank line contains whitespace |
| 4285 | W293 | `opt/services/fleet/federation_manager.py` | 335 | blank line contains whitespace |
| 4284 | W293 | `opt/services/fleet/federation_manager.py` | 328 | blank line contains whitespace |
| 4283 | W293 | `opt/services/fleet/federation_manager.py` | 309 | blank line contains whitespace |
| 4282 | W293 | `opt/services/fleet/federation_manager.py` | 299 | blank line contains whitespace |
| 4281 | W293 | `opt/services/fleet/federation_manager.py` | 289 | blank line contains whitespace |
| 4280 | W293 | `opt/services/fleet/federation_manager.py` | 279 | blank line contains whitespace |
| 4279 | W293 | `opt/services/fleet/federation_manager.py` | 266 | blank line contains whitespace |
| 4278 | W293 | `opt/services/fleet/federation_manager.py` | 250 | blank line contains whitespace |
| 4277 | W293 | `opt/services/fleet/federation_manager.py` | 243 | blank line contains whitespace |
| 4276 | W293 | `opt/services/fleet/federation_manager.py` | 234 | blank line contains whitespace |
| 4275 | W293 | `opt/services/fleet/federation_manager.py` | 216 | blank line contains whitespace |
| 4274 | W293 | `opt/services/fleet/federation_manager.py` | 209 | blank line contains whitespace |
| 4273 | W293 | `opt/services/fleet/federation_manager.py` | 200 | blank line contains whitespace |
| 4272 | W293 | `opt/services/fleet/federation_manager.py` | 198 | blank line contains whitespace |
| 4271 | W293 | `opt/services/fleet/federation_manager.py` | 192 | blank line contains whitespace |
| 4270 | W293 | `opt/services/fleet/federation_manager.py` | 189 | blank line contains whitespace |
| 4269 | W293 | `opt/services/fleet/federation_manager.py` | 185 | blank line contains whitespace |
| 4268 | W293 | `opt/services/fleet/federation_manager.py` | 181 | blank line contains whitespace |
| 4261 | W391 | `opt/services/diagnostics.py` | 507 | blank line at end of file |
| 4260 | W293 | `opt/services/diagnostics.py` | 490 | blank line contains whitespace |
| 4259 | W293 | `opt/services/diagnostics.py` | 475 | blank line contains whitespace |
| 4258 | W293 | `opt/services/diagnostics.py` | 470 | blank line contains whitespace |
| 4257 | W293 | `opt/services/diagnostics.py` | 467 | blank line contains whitespace |
| 4256 | W293 | `opt/services/diagnostics.py` | 461 | blank line contains whitespace |
| 4255 | W293 | `opt/services/diagnostics.py` | 456 | blank line contains whitespace |
| 4254 | W293 | `opt/services/diagnostics.py` | 451 | blank line contains whitespace |
| 4253 | W293 | `opt/services/diagnostics.py` | 448 | blank line contains whitespace |
| 4252 | W293 | `opt/services/diagnostics.py` | 440 | blank line contains whitespace |
| 4251 | W293 | `opt/services/diagnostics.py` | 430 | blank line contains whitespace |
| 4250 | W293 | `opt/services/diagnostics.py` | 422 | blank line contains whitespace |
| 4249 | W293 | `opt/services/diagnostics.py` | 415 | blank line contains whitespace |
| 4248 | W293 | `opt/services/diagnostics.py` | 413 | blank line contains whitespace |
| 4247 | W293 | `opt/services/diagnostics.py` | 401 | blank line contains whitespace |
| 4246 | W293 | `opt/services/diagnostics.py` | 386 | blank line contains whitespace |
| 4245 | W293 | `opt/services/diagnostics.py` | 383 | blank line contains whitespace |
| 4244 | W293 | `opt/services/diagnostics.py` | 378 | blank line contains whitespace |
| 4243 | W293 | `opt/services/diagnostics.py` | 368 | blank line contains whitespace |
| 4242 | W293 | `opt/services/diagnostics.py` | 351 | blank line contains whitespace |
| 4241 | W293 | `opt/services/diagnostics.py` | 348 | blank line contains whitespace |
| 4240 | W293 | `opt/services/diagnostics.py` | 335 | blank line contains whitespace |
| 4239 | W293 | `opt/services/diagnostics.py` | 333 | blank line contains whitespace |
| 4238 | W293 | `opt/services/diagnostics.py` | 325 | blank line contains whitespace |
| 4237 | W293 | `opt/services/diagnostics.py` | 309 | blank line contains whitespace |
| 4236 | W293 | `opt/services/diagnostics.py` | 297 | blank line contains whitespace |
| 4235 | W293 | `opt/services/diagnostics.py` | 292 | blank line contains whitespace |
| 4234 | W293 | `opt/services/diagnostics.py` | 288 | blank line contains whitespace |
| 4233 | W293 | `opt/services/diagnostics.py` | 284 | blank line contains whitespace |
| 4232 | W293 | `opt/services/diagnostics.py` | 272 | blank line contains whitespace |
| 4231 | W293 | `opt/services/diagnostics.py` | 270 | blank line contains whitespace |
| 4230 | W293 | `opt/services/diagnostics.py` | 252 | blank line contains whitespace |
| 4229 | W293 | `opt/services/diagnostics.py` | 235 | blank line contains whitespace |
| 4228 | W293 | `opt/services/diagnostics.py` | 230 | blank line contains whitespace |
| 4227 | W293 | `opt/services/diagnostics.py` | 226 | blank line contains whitespace |
| 4226 | W293 | `opt/services/diagnostics.py` | 222 | blank line contains whitespace |
| 4225 | W293 | `opt/services/diagnostics.py` | 210 | blank line contains whitespace |
| 4224 | W293 | `opt/services/diagnostics.py` | 208 | blank line contains whitespace |
| 4223 | W293 | `opt/services/diagnostics.py` | 199 | blank line contains whitespace |
| 4222 | W293 | `opt/services/diagnostics.py` | 189 | blank line contains whitespace |
| 4221 | W293 | `opt/services/diagnostics.py` | 173 | blank line contains whitespace |
| 4220 | W293 | `opt/services/diagnostics.py` | 168 | blank line contains whitespace |
| 4219 | W293 | `opt/services/diagnostics.py` | 164 | blank line contains whitespace |
| 4218 | W293 | `opt/services/diagnostics.py` | 161 | blank line contains whitespace |
| 4217 | W293 | `opt/services/diagnostics.py` | 149 | blank line contains whitespace |
| 4216 | W293 | `opt/services/diagnostics.py` | 147 | blank line contains whitespace |
| 4215 | W293 | `opt/services/diagnostics.py` | 137 | blank line contains whitespace |
| 4214 | W293 | `opt/services/diagnostics.py` | 124 | blank line contains whitespace |
| 4213 | W293 | `opt/services/diagnostics.py` | 117 | blank line contains whitespace |
| 4212 | W293 | `opt/services/diagnostics.py` | 113 | blank line contains whitespace |
| 4211 | W293 | `opt/services/diagnostics.py` | 110 | blank line contains whitespace |
| 4210 | W293 | `opt/services/diagnostics.py` | 101 | blank line contains whitespace |
| 4209 | W293 | `opt/services/diagnostics.py` | 90 | blank line contains whitespace |
| 4208 | W293 | `opt/services/diagnostics.py` | 86 | blank line contains whitespace |
| 4205 | W293 | `opt/services/database/query_optimizer.py` | 596 | blank line contains whitespace |
| 4204 | W293 | `opt/services/database/query_optimizer.py` | 591 | blank line contains whitespace |
| 4203 | W293 | `opt/services/database/query_optimizer.py` | 588 | blank line contains whitespace |
| 4202 | W293 | `opt/services/database/query_optimizer.py` | 584 | blank line contains whitespace |
| 4201 | W293 | `opt/services/database/query_optimizer.py` | 576 | blank line contains whitespace |
| 4200 | W293 | `opt/services/database/query_optimizer.py` | 569 | blank line contains whitespace |
| 4199 | W293 | `opt/services/database/query_optimizer.py` | 558 | blank line contains whitespace |
| 4198 | W293 | `opt/services/database/query_optimizer.py` | 555 | blank line contains whitespace |
| 4197 | W293 | `opt/services/database/query_optimizer.py` | 546 | blank line contains whitespace |
| 4196 | W293 | `opt/services/database/query_optimizer.py` | 537 | blank line contains whitespace |
| 4195 | W293 | `opt/services/database/query_optimizer.py` | 534 | blank line contains whitespace |
| 4194 | W293 | `opt/services/database/query_optimizer.py` | 526 | blank line contains whitespace |
| 4193 | W293 | `opt/services/database/query_optimizer.py` | 516 | blank line contains whitespace |
| 4192 | W293 | `opt/services/database/query_optimizer.py` | 513 | blank line contains whitespace |
| 4191 | W293 | `opt/services/database/query_optimizer.py` | 501 | blank line contains whitespace |
| 4190 | W293 | `opt/services/database/query_optimizer.py` | 497 | blank line contains whitespace |
| 4189 | W293 | `opt/services/database/query_optimizer.py` | 493 | blank line contains whitespace |
| 4188 | W293 | `opt/services/database/query_optimizer.py` | 488 | blank line contains whitespace |
| 4187 | W293 | `opt/services/database/query_optimizer.py` | 485 | blank line contains whitespace |
| 4186 | W293 | `opt/services/database/query_optimizer.py` | 477 | blank line contains whitespace |
| 4185 | W293 | `opt/services/database/query_optimizer.py` | 469 | blank line contains whitespace |
| 4184 | W293 | `opt/services/database/query_optimizer.py` | 464 | blank line contains whitespace |
| 4183 | W293 | `opt/services/database/query_optimizer.py` | 460 | blank line contains whitespace |
| 4182 | W293 | `opt/services/database/query_optimizer.py` | 454 | blank line contains whitespace |
| 4181 | W293 | `opt/services/database/query_optimizer.py` | 450 | blank line contains whitespace |
| 4180 | W293 | `opt/services/database/query_optimizer.py` | 448 | blank line contains whitespace |
| 4179 | W293 | `opt/services/database/query_optimizer.py` | 445 | blank line contains whitespace |
| 4178 | W293 | `opt/services/database/query_optimizer.py` | 441 | blank line contains whitespace |
| 4177 | W293 | `opt/services/database/query_optimizer.py` | 430 | blank line contains whitespace |
| 4176 | W293 | `opt/services/database/query_optimizer.py` | 419 | blank line contains whitespace |
| 4175 | W293 | `opt/services/database/query_optimizer.py` | 408 | blank line contains whitespace |
| 4174 | W293 | `opt/services/database/query_optimizer.py` | 404 | blank line contains whitespace |
| 4173 | W293 | `opt/services/database/query_optimizer.py` | 402 | blank line contains whitespace |
| 4172 | W293 | `opt/services/database/query_optimizer.py` | 397 | blank line contains whitespace |
| 4171 | W293 | `opt/services/database/query_optimizer.py` | 393 | blank line contains whitespace |
| 4170 | W293 | `opt/services/database/query_optimizer.py` | 387 | blank line contains whitespace |
| 4169 | W293 | `opt/services/database/query_optimizer.py` | 376 | blank line contains whitespace |
| 4168 | W293 | `opt/services/database/query_optimizer.py` | 372 | blank line contains whitespace |
| 4167 | W293 | `opt/services/database/query_optimizer.py` | 369 | blank line contains whitespace |
| 4166 | W293 | `opt/services/database/query_optimizer.py` | 367 | blank line contains whitespace |
| 4165 | W293 | `opt/services/database/query_optimizer.py` | 365 | blank line contains whitespace |
| 4164 | W293 | `opt/services/database/query_optimizer.py` | 356 | blank line contains whitespace |
| 4163 | W293 | `opt/services/database/query_optimizer.py` | 354 | blank line contains whitespace |
| 4162 | W293 | `opt/services/database/query_optimizer.py` | 344 | blank line contains whitespace |
| 4161 | W293 | `opt/services/database/query_optimizer.py` | 337 | blank line contains whitespace |
| 4160 | W293 | `opt/services/database/query_optimizer.py` | 332 | blank line contains whitespace |
| 4159 | W293 | `opt/services/database/query_optimizer.py` | 321 | blank line contains whitespace |
| 4158 | W293 | `opt/services/database/query_optimizer.py` | 317 | blank line contains whitespace |
| 4157 | W293 | `opt/services/database/query_optimizer.py` | 315 | blank line contains whitespace |
| 4156 | W293 | `opt/services/database/query_optimizer.py` | 310 | blank line contains whitespace |
| 4155 | W293 | `opt/services/database/query_optimizer.py` | 308 | blank line contains whitespace |
| 4154 | W293 | `opt/services/database/query_optimizer.py` | 304 | blank line contains whitespace |
| 4153 | W293 | `opt/services/database/query_optimizer.py` | 300 | blank line contains whitespace |
| 4152 | W293 | `opt/services/database/query_optimizer.py` | 297 | blank line contains whitespace |
| 4151 | W293 | `opt/services/database/query_optimizer.py` | 291 | blank line contains whitespace |
| 4150 | W293 | `opt/services/database/query_optimizer.py` | 288 | blank line contains whitespace |
| 4149 | W293 | `opt/services/database/query_optimizer.py` | 283 | blank line contains whitespace |
| 4148 | W293 | `opt/services/database/query_optimizer.py` | 279 | blank line contains whitespace |
| 4147 | W293 | `opt/services/database/query_optimizer.py` | 277 | blank line contains whitespace |
| 4146 | W293 | `opt/services/database/query_optimizer.py` | 275 | blank line contains whitespace |
| 4145 | W293 | `opt/services/database/query_optimizer.py` | 265 | blank line contains whitespace |
| 4144 | W293 | `opt/services/database/query_optimizer.py` | 261 | blank line contains whitespace |
| 4143 | W293 | `opt/services/database/query_optimizer.py` | 258 | blank line contains whitespace |
| 4142 | W293 | `opt/services/database/query_optimizer.py` | 254 | blank line contains whitespace |
| 4141 | W293 | `opt/services/database/query_optimizer.py` | 251 | blank line contains whitespace |
| 4140 | W293 | `opt/services/database/query_optimizer.py` | 239 | blank line contains whitespace |
| 4139 | W293 | `opt/services/database/query_optimizer.py` | 236 | blank line contains whitespace |
| 4138 | W293 | `opt/services/database/query_optimizer.py` | 223 | blank line contains whitespace |
| 4137 | W293 | `opt/services/database/query_optimizer.py` | 218 | blank line contains whitespace |
| 4136 | W293 | `opt/services/database/query_optimizer.py` | 215 | blank line contains whitespace |
| 4135 | W293 | `opt/services/database/query_optimizer.py` | 211 | blank line contains whitespace |
| 4134 | W293 | `opt/services/database/query_optimizer.py` | 205 | blank line contains whitespace |
| 4133 | W293 | `opt/services/database/query_optimizer.py` | 200 | blank line contains whitespace |
| 4132 | W293 | `opt/services/database/query_optimizer.py` | 197 | blank line contains whitespace |
| 4131 | W293 | `opt/services/database/query_optimizer.py` | 194 | blank line contains whitespace |
| 4130 | W293 | `opt/services/database/query_optimizer.py` | 187 | blank line contains whitespace |
| 4129 | W293 | `opt/services/database/query_optimizer.py` | 184 | blank line contains whitespace |
| 4128 | W293 | `opt/services/database/query_optimizer.py` | 180 | blank line contains whitespace |
| 4127 | W293 | `opt/services/database/query_optimizer.py` | 169 | blank line contains whitespace |
| 4126 | W293 | `opt/services/database/query_optimizer.py` | 165 | blank line contains whitespace |
| 4125 | W293 | `opt/services/database/query_optimizer.py` | 162 | blank line contains whitespace |
| 4124 | W293 | `opt/services/database/query_optimizer.py` | 156 | blank line contains whitespace |
| 4123 | W293 | `opt/services/database/query_optimizer.py` | 152 | blank line contains whitespace |
| 4122 | W293 | `opt/services/database/query_optimizer.py` | 147 | blank line contains whitespace |
| 4121 | W293 | `opt/services/database/query_optimizer.py` | 142 | blank line contains whitespace |
| 4120 | W293 | `opt/services/database/query_optimizer.py` | 136 | blank line contains whitespace |
| 4119 | W293 | `opt/services/database/query_optimizer.py` | 132 | blank line contains whitespace |
| 4118 | W293 | `opt/services/database/query_optimizer.py` | 128 | blank line contains whitespace |
| 4117 | W293 | `opt/services/database/query_optimizer.py` | 120 | blank line contains whitespace |
| 4116 | W293 | `opt/services/database/query_optimizer.py` | 114 | blank line contains whitespace |
| 4115 | W293 | `opt/services/database/query_optimizer.py` | 109 | blank line contains whitespace |
| 4114 | W293 | `opt/services/database/query_optimizer.py` | 103 | blank line contains whitespace |
| 4113 | W293 | `opt/services/database/query_optimizer.py` | 100 | blank line contains whitespace |
| 4112 | W293 | `opt/services/database/query_optimizer.py` | 66 | blank line contains whitespace |
| 4111 | W293 | `opt/services/database/query_optimizer.py` | 58 | blank line contains whitespace |
| 4110 | W293 | `opt/services/database/query_optimizer.py` | 55 | blank line contains whitespace |
| 4109 | W293 | `opt/services/database/query_optimizer.py` | 50 | blank line contains whitespace |
| 4106 | W293 | `opt/services/cost_optimization/core.py` | 131 | blank line contains whitespace |
| 4105 | W293 | `opt/services/cost_optimization/core.py` | 128 | blank line contains whitespace |
| 4104 | W293 | `opt/services/cost_optimization/core.py` | 126 | blank line contains whitespace |
| 4103 | W293 | `opt/services/cost_optimization/core.py` | 120 | blank line contains whitespace |
| 4102 | W293 | `opt/services/cost_optimization/core.py` | 92 | blank line contains whitespace |
| 4101 | W293 | `opt/services/cost_optimization/core.py` | 81 | blank line contains whitespace |
| 4100 | W293 | `opt/services/cost_optimization/core.py` | 65 | blank line contains whitespace |
| 4097 | W293 | `opt/services/cost_optimization/cli.py` | 87 | blank line contains whitespace |
| 4096 | W293 | `opt/services/cost_optimization/cli.py` | 76 | blank line contains whitespace |
| 4095 | W293 | `opt/services/cost_optimization/cli.py` | 28 | blank line contains whitespace |
| 4091 | W293 | `opt/services/cost/cost_engine.py` | 725 | blank line contains whitespace |
| 4090 | W293 | `opt/services/cost/cost_engine.py` | 721 | blank line contains whitespace |
| 4089 | W293 | `opt/services/cost/cost_engine.py` | 710 | blank line contains whitespace |
| 4088 | W293 | `opt/services/cost/cost_engine.py` | 694 | blank line contains whitespace |
| 4087 | W293 | `opt/services/cost/cost_engine.py` | 690 | blank line contains whitespace |
| 4086 | W293 | `opt/services/cost/cost_engine.py` | 683 | blank line contains whitespace |
| 4085 | W293 | `opt/services/cost/cost_engine.py` | 681 | blank line contains whitespace |
| 4084 | W293 | `opt/services/cost/cost_engine.py` | 676 | blank line contains whitespace |
| 4083 | W293 | `opt/services/cost/cost_engine.py` | 670 | blank line contains whitespace |
| 4082 | W293 | `opt/services/cost/cost_engine.py` | 662 | blank line contains whitespace |
| 4081 | W293 | `opt/services/cost/cost_engine.py` | 631 | blank line contains whitespace |
| 4080 | W293 | `opt/services/cost/cost_engine.py` | 621 | blank line contains whitespace |
| 4079 | W293 | `opt/services/cost/cost_engine.py` | 604 | blank line contains whitespace |
| 4078 | W293 | `opt/services/cost/cost_engine.py` | 599 | blank line contains whitespace |
| 4077 | W293 | `opt/services/cost/cost_engine.py` | 595 | blank line contains whitespace |
| 4076 | W293 | `opt/services/cost/cost_engine.py` | 590 | blank line contains whitespace |
| 4075 | W293 | `opt/services/cost/cost_engine.py` | 581 | blank line contains whitespace |
| 4074 | W293 | `opt/services/cost/cost_engine.py` | 573 | blank line contains whitespace |
| 4073 | W293 | `opt/services/cost/cost_engine.py` | 570 | blank line contains whitespace |
| 4072 | W293 | `opt/services/cost/cost_engine.py` | 566 | blank line contains whitespace |
| 4071 | W293 | `opt/services/cost/cost_engine.py` | 560 | blank line contains whitespace |
| 4070 | W293 | `opt/services/cost/cost_engine.py` | 557 | blank line contains whitespace |
| 4069 | W293 | `opt/services/cost/cost_engine.py` | 554 | blank line contains whitespace |
| 4068 | W293 | `opt/services/cost/cost_engine.py` | 545 | blank line contains whitespace |
| 4067 | W293 | `opt/services/cost/cost_engine.py` | 533 | blank line contains whitespace |
| 4066 | W293 | `opt/services/cost/cost_engine.py` | 529 | blank line contains whitespace |
| 4065 | W293 | `opt/services/cost/cost_engine.py` | 527 | blank line contains whitespace |
| 4064 | W293 | `opt/services/cost/cost_engine.py` | 523 | blank line contains whitespace |
| 4063 | W293 | `opt/services/cost/cost_engine.py` | 519 | blank line contains whitespace |
| 4062 | W293 | `opt/services/cost/cost_engine.py` | 517 | blank line contains whitespace |
| 4061 | W293 | `opt/services/cost/cost_engine.py` | 513 | blank line contains whitespace |
| 4060 | W293 | `opt/services/cost/cost_engine.py` | 509 | blank line contains whitespace |
| 4059 | W293 | `opt/services/cost/cost_engine.py` | 501 | blank line contains whitespace |
| 4058 | W293 | `opt/services/cost/cost_engine.py` | 493 | blank line contains whitespace |
| 4057 | W293 | `opt/services/cost/cost_engine.py` | 488 | blank line contains whitespace |
| 4055 | W293 | `opt/services/cost/cost_engine.py` | 482 | blank line contains whitespace |
| 4053 | W293 | `opt/services/cost/cost_engine.py` | 476 | blank line contains whitespace |
| 4052 | W293 | `opt/services/cost/cost_engine.py` | 472 | blank line contains whitespace |
| 4051 | W293 | `opt/services/cost/cost_engine.py` | 461 | blank line contains whitespace |
| 4050 | W293 | `opt/services/cost/cost_engine.py` | 443 | blank line contains whitespace |
| 4049 | W293 | `opt/services/cost/cost_engine.py` | 430 | blank line contains whitespace |
| 4048 | W293 | `opt/services/cost/cost_engine.py` | 424 | blank line contains whitespace |
| 4047 | W293 | `opt/services/cost/cost_engine.py` | 419 | blank line contains whitespace |
| 4046 | W293 | `opt/services/cost/cost_engine.py` | 414 | blank line contains whitespace |
| 4045 | W293 | `opt/services/cost/cost_engine.py` | 404 | blank line contains whitespace |
| 4044 | W293 | `opt/services/cost/cost_engine.py` | 396 | blank line contains whitespace |
| 4043 | W293 | `opt/services/cost/cost_engine.py` | 391 | blank line contains whitespace |
| 4042 | W293 | `opt/services/cost/cost_engine.py` | 386 | blank line contains whitespace |
| 4041 | W293 | `opt/services/cost/cost_engine.py` | 376 | blank line contains whitespace |
| 4040 | W293 | `opt/services/cost/cost_engine.py` | 372 | blank line contains whitespace |
| 4039 | W293 | `opt/services/cost/cost_engine.py` | 366 | blank line contains whitespace |
| 4038 | W293 | `opt/services/cost/cost_engine.py` | 353 | blank line contains whitespace |
| 4037 | W293 | `opt/services/cost/cost_engine.py` | 351 | blank line contains whitespace |
| 4036 | W293 | `opt/services/cost/cost_engine.py` | 342 | blank line contains whitespace |
| 4035 | W293 | `opt/services/cost/cost_engine.py` | 340 | blank line contains whitespace |
| 4034 | W293 | `opt/services/cost/cost_engine.py` | 337 | blank line contains whitespace |
| 4033 | W293 | `opt/services/cost/cost_engine.py` | 335 | blank line contains whitespace |
| 4032 | W293 | `opt/services/cost/cost_engine.py` | 319 | blank line contains whitespace |
| 4031 | W293 | `opt/services/cost/cost_engine.py` | 304 | blank line contains whitespace |
| 4030 | W293 | `opt/services/cost/cost_engine.py` | 302 | blank line contains whitespace |
| 4029 | W293 | `opt/services/cost/cost_engine.py` | 296 | blank line contains whitespace |
| 4028 | W293 | `opt/services/cost/cost_engine.py` | 291 | blank line contains whitespace |
| 4027 | W293 | `opt/services/cost/cost_engine.py` | 283 | blank line contains whitespace |
| 4026 | W293 | `opt/services/cost/cost_engine.py` | 275 | blank line contains whitespace |
| 4025 | W293 | `opt/services/cost/cost_engine.py` | 269 | blank line contains whitespace |
| 4024 | W293 | `opt/services/cost/cost_engine.py` | 264 | blank line contains whitespace |
| 4023 | W293 | `opt/services/cost/cost_engine.py` | 259 | blank line contains whitespace |
| 4022 | W293 | `opt/services/cost/cost_engine.py` | 255 | blank line contains whitespace |
| 4021 | W293 | `opt/services/cost/cost_engine.py` | 251 | blank line contains whitespace |
| 4020 | W293 | `opt/services/cost/cost_engine.py` | 246 | blank line contains whitespace |
| 4019 | W293 | `opt/services/cost/cost_engine.py` | 242 | blank line contains whitespace |
| 4018 | W293 | `opt/services/cost/cost_engine.py` | 234 | blank line contains whitespace |
| 4017 | W293 | `opt/services/cost/cost_engine.py` | 231 | blank line contains whitespace |
| 4016 | W293 | `opt/services/cost/cost_engine.py` | 228 | blank line contains whitespace |
| 4015 | W293 | `opt/services/cost/cost_engine.py` | 225 | blank line contains whitespace |
| 4014 | W293 | `opt/services/cost/cost_engine.py` | 222 | blank line contains whitespace |
| 4013 | W293 | `opt/services/cost/cost_engine.py` | 218 | blank line contains whitespace |
| 4012 | W293 | `opt/services/cost/cost_engine.py` | 215 | blank line contains whitespace |
| 4011 | W293 | `opt/services/cost/cost_engine.py` | 211 | blank line contains whitespace |
| 4010 | W293 | `opt/services/cost/cost_engine.py` | 193 | blank line contains whitespace |
| 4009 | W293 | `opt/services/cost/cost_engine.py` | 187 | blank line contains whitespace |
| 4008 | W293 | `opt/services/cost/cost_engine.py` | 163 | blank line contains whitespace |
| 4007 | W293 | `opt/services/cost/cost_engine.py` | 157 | blank line contains whitespace |
| 4006 | W293 | `opt/services/cost/cost_engine.py` | 154 | blank line contains whitespace |
| 4005 | W293 | `opt/services/cost/cost_engine.py` | 124 | blank line contains whitespace |
| 4004 | W293 | `opt/services/cost/cost_engine.py` | 119 | blank line contains whitespace |
| 4003 | W293 | `opt/services/cost/cost_engine.py` | 98 | blank line contains whitespace |
| 4002 | W293 | `opt/services/cost/cost_engine.py` | 78 | blank line contains whitespace |
| 4001 | W293 | `opt/services/containers/container_integration.py` | 1321 | blank line contains whitespace |
| 4000 | W293 | `opt/services/containers/container_integration.py` | 1314 | blank line contains whitespace |
| 3999 | W293 | `opt/services/containers/container_integration.py` | 1310 | blank line contains whitespace |
| 3998 | W293 | `opt/services/containers/container_integration.py` | 1299 | blank line contains whitespace |
| 3997 | W293 | `opt/services/containers/container_integration.py` | 1293 | blank line contains whitespace |
| 3996 | W293 | `opt/services/containers/container_integration.py` | 1288 | blank line contains whitespace |
| 3995 | W293 | `opt/services/containers/container_integration.py` | 1284 | blank line contains whitespace |
| 3994 | W293 | `opt/services/containers/container_integration.py` | 1281 | blank line contains whitespace |
| 3993 | W293 | `opt/services/containers/container_integration.py` | 1267 | blank line contains whitespace |
| 3992 | W293 | `opt/services/containers/container_integration.py` | 1260 | blank line contains whitespace |
| 3991 | W293 | `opt/services/containers/container_integration.py` | 1249 | blank line contains whitespace |
| 3990 | W293 | `opt/services/containers/container_integration.py` | 1240 | blank line contains whitespace |
| 3989 | W293 | `opt/services/containers/container_integration.py` | 1232 | blank line contains whitespace |
| 3988 | W293 | `opt/services/containers/container_integration.py` | 1228 | blank line contains whitespace |
| 3987 | W293 | `opt/services/containers/container_integration.py` | 1226 | blank line contains whitespace |
| 3986 | W293 | `opt/services/containers/container_integration.py` | 1218 | blank line contains whitespace |
| 3985 | W293 | `opt/services/containers/container_integration.py` | 1211 | blank line contains whitespace |
| 3984 | W293 | `opt/services/containers/container_integration.py` | 1207 | blank line contains whitespace |
| 3983 | W293 | `opt/services/containers/container_integration.py` | 1203 | blank line contains whitespace |
| 3982 | W293 | `opt/services/containers/container_integration.py` | 1185 | blank line contains whitespace |
| 3981 | W293 | `opt/services/containers/container_integration.py` | 1183 | blank line contains whitespace |
| 3980 | W293 | `opt/services/containers/container_integration.py` | 1178 | blank line contains whitespace |
| 3979 | W293 | `opt/services/containers/container_integration.py` | 1162 | blank line contains whitespace |
| 3978 | W293 | `opt/services/containers/container_integration.py` | 1154 | blank line contains whitespace |
| 3977 | W293 | `opt/services/containers/container_integration.py` | 1145 | blank line contains whitespace |
| 3976 | W293 | `opt/services/containers/container_integration.py` | 1134 | blank line contains whitespace |
| 3975 | W293 | `opt/services/containers/container_integration.py` | 1130 | blank line contains whitespace |
| 3974 | W293 | `opt/services/containers/container_integration.py` | 1118 | blank line contains whitespace |
| 3973 | W293 | `opt/services/containers/container_integration.py` | 1110 | blank line contains whitespace |
| 3972 | W293 | `opt/services/containers/container_integration.py` | 1101 | blank line contains whitespace |
| 3971 | W293 | `opt/services/containers/container_integration.py` | 1088 | blank line contains whitespace |
| 3970 | W293 | `opt/services/containers/container_integration.py` | 1083 | blank line contains whitespace |
| 3969 | W293 | `opt/services/containers/container_integration.py` | 1056 | blank line contains whitespace |
| 3968 | W293 | `opt/services/containers/container_integration.py` | 1045 | blank line contains whitespace |
| 3967 | W293 | `opt/services/containers/container_integration.py` | 1034 | blank line contains whitespace |
| 3966 | W293 | `opt/services/containers/container_integration.py` | 1017 | blank line contains whitespace |
| 3965 | W293 | `opt/services/containers/container_integration.py` | 1015 | blank line contains whitespace |
| 3964 | W293 | `opt/services/containers/container_integration.py` | 998 | blank line contains whitespace |
| 3963 | W293 | `opt/services/containers/container_integration.py` | 987 | blank line contains whitespace |
| 3962 | W293 | `opt/services/containers/container_integration.py` | 970 | blank line contains whitespace |
| 3961 | W293 | `opt/services/containers/container_integration.py` | 966 | blank line contains whitespace |
| 3960 | W293 | `opt/services/containers/container_integration.py` | 952 | blank line contains whitespace |
| 3959 | W293 | `opt/services/containers/container_integration.py` | 947 | blank line contains whitespace |
| 3958 | W293 | `opt/services/containers/container_integration.py` | 941 | blank line contains whitespace |
| 3957 | W293 | `opt/services/containers/container_integration.py` | 933 | blank line contains whitespace |
| 3956 | W293 | `opt/services/containers/container_integration.py` | 925 | blank line contains whitespace |
| 3955 | W293 | `opt/services/containers/container_integration.py` | 914 | blank line contains whitespace |
| 3954 | W293 | `opt/services/containers/container_integration.py` | 911 | blank line contains whitespace |
| 3953 | W293 | `opt/services/containers/container_integration.py` | 898 | blank line contains whitespace |
| 3952 | W293 | `opt/services/containers/container_integration.py` | 888 | blank line contains whitespace |
| 3951 | W293 | `opt/services/containers/container_integration.py` | 878 | blank line contains whitespace |
| 3950 | W293 | `opt/services/containers/container_integration.py` | 874 | blank line contains whitespace |
| 3949 | W293 | `opt/services/containers/container_integration.py` | 858 | blank line contains whitespace |
| 3948 | W293 | `opt/services/containers/container_integration.py` | 853 | blank line contains whitespace |
| 3947 | W293 | `opt/services/containers/container_integration.py` | 842 | blank line contains whitespace |
| 3946 | W293 | `opt/services/containers/container_integration.py` | 836 | blank line contains whitespace |
| 3945 | W293 | `opt/services/containers/container_integration.py` | 832 | blank line contains whitespace |
| 3944 | W293 | `opt/services/containers/container_integration.py` | 827 | blank line contains whitespace |
| 3943 | W293 | `opt/services/containers/container_integration.py` | 825 | blank line contains whitespace |
| 3942 | W293 | `opt/services/containers/container_integration.py` | 813 | blank line contains whitespace |
| 3941 | W293 | `opt/services/containers/container_integration.py` | 801 | blank line contains whitespace |
| 3940 | W293 | `opt/services/containers/container_integration.py` | 797 | blank line contains whitespace |
| 3939 | W293 | `opt/services/containers/container_integration.py` | 785 | blank line contains whitespace |
| 3938 | W293 | `opt/services/containers/container_integration.py` | 783 | blank line contains whitespace |
| 3937 | W293 | `opt/services/containers/container_integration.py` | 771 | blank line contains whitespace |
| 3936 | W293 | `opt/services/containers/container_integration.py` | 762 | blank line contains whitespace |
| 3935 | W293 | `opt/services/containers/container_integration.py` | 754 | blank line contains whitespace |
| 3934 | W293 | `opt/services/containers/container_integration.py` | 744 | blank line contains whitespace |
| 3933 | W293 | `opt/services/containers/container_integration.py` | 733 | blank line contains whitespace |
| 3932 | W293 | `opt/services/containers/container_integration.py` | 721 | blank line contains whitespace |
| 3931 | W293 | `opt/services/containers/container_integration.py` | 709 | blank line contains whitespace |
| 3930 | W293 | `opt/services/containers/container_integration.py` | 706 | blank line contains whitespace |
| 3929 | W293 | `opt/services/containers/container_integration.py` | 686 | blank line contains whitespace |
| 3928 | W293 | `opt/services/containers/container_integration.py` | 673 | blank line contains whitespace |
| 3926 | W293 | `opt/services/containers/container_integration.py` | 663 | blank line contains whitespace |
| 3925 | W293 | `opt/services/containers/container_integration.py` | 658 | blank line contains whitespace |
| 3923 | W293 | `opt/services/containers/container_integration.py` | 653 | blank line contains whitespace |
| 3922 | W293 | `opt/services/containers/container_integration.py` | 648 | blank line contains whitespace |
| 3921 | W293 | `opt/services/containers/container_integration.py` | 632 | blank line contains whitespace |
| 3920 | W293 | `opt/services/containers/container_integration.py` | 607 | blank line contains whitespace |
| 3919 | W293 | `opt/services/containers/container_integration.py` | 600 | blank line contains whitespace |
| 3918 | W293 | `opt/services/containers/container_integration.py` | 587 | blank line contains whitespace |
| 3917 | W293 | `opt/services/containers/container_integration.py` | 584 | blank line contains whitespace |
| 3916 | W293 | `opt/services/containers/container_integration.py` | 571 | blank line contains whitespace |
| 3915 | W293 | `opt/services/containers/container_integration.py` | 565 | blank line contains whitespace |
| 3914 | W293 | `opt/services/containers/container_integration.py` | 555 | blank line contains whitespace |
| 3913 | W293 | `opt/services/containers/container_integration.py` | 552 | blank line contains whitespace |
| 3912 | W293 | `opt/services/containers/container_integration.py` | 538 | blank line contains whitespace |
| 3911 | W293 | `opt/services/containers/container_integration.py` | 530 | blank line contains whitespace |
| 3910 | W293 | `opt/services/containers/container_integration.py` | 528 | blank line contains whitespace |
| 3907 | W293 | `opt/services/containers/container_integration.py` | 507 | blank line contains whitespace |
| 3906 | W293 | `opt/services/containers/container_integration.py` | 490 | blank line contains whitespace |
| 3905 | W293 | `opt/services/containers/container_integration.py` | 473 | blank line contains whitespace |
| 3904 | W293 | `opt/services/containers/container_integration.py` | 467 | blank line contains whitespace |
| 3903 | W293 | `opt/services/containers/container_integration.py` | 432 | blank line contains whitespace |
| 3902 | W293 | `opt/services/containers/container_integration.py` | 429 | blank line contains whitespace |
| 3901 | W293 | `opt/services/containers/container_integration.py` | 423 | blank line contains whitespace |
| 3900 | W293 | `opt/services/containers/container_integration.py` | 406 | blank line contains whitespace |
| 3899 | W293 | `opt/services/containers/container_integration.py` | 404 | blank line contains whitespace |
| 3898 | W293 | `opt/services/containers/container_integration.py` | 391 | blank line contains whitespace |
| 3897 | W293 | `opt/services/containers/container_integration.py` | 385 | blank line contains whitespace |
| 3896 | W293 | `opt/services/containers/container_integration.py` | 379 | blank line contains whitespace |
| 3895 | W293 | `opt/services/containers/container_integration.py` | 372 | blank line contains whitespace |
| 3894 | W293 | `opt/services/containers/container_integration.py` | 366 | blank line contains whitespace |
| 3893 | W293 | `opt/services/containers/container_integration.py` | 357 | blank line contains whitespace |
| 3892 | W293 | `opt/services/containers/container_integration.py` | 346 | blank line contains whitespace |
| 3891 | W293 | `opt/services/containers/container_integration.py` | 343 | blank line contains whitespace |
| 3890 | W293 | `opt/services/containers/container_integration.py` | 339 | blank line contains whitespace |
| 3889 | W293 | `opt/services/containers/container_integration.py` | 327 | blank line contains whitespace |
| 3888 | W293 | `opt/services/containers/container_integration.py` | 315 | blank line contains whitespace |
| 3887 | W293 | `opt/services/containers/container_integration.py` | 312 | blank line contains whitespace |
| 3886 | W293 | `opt/services/containers/container_integration.py` | 307 | blank line contains whitespace |
| 3885 | W293 | `opt/services/containers/container_integration.py` | 290 | blank line contains whitespace |
| 3883 | W293 | `opt/services/containers/container_integration.py` | 286 | blank line contains whitespace |
| 3882 | W293 | `opt/services/containers/container_integration.py` | 277 | blank line contains whitespace |
| 3881 | W293 | `opt/services/containers/container_integration.py` | 267 | blank line contains whitespace |
| 3880 | W293 | `opt/services/containers/container_integration.py` | 260 | blank line contains whitespace |
| 3879 | W293 | `opt/services/containers/container_integration.py` | 242 | blank line contains whitespace |
| 3878 | W293 | `opt/services/containers/container_integration.py` | 231 | blank line contains whitespace |
| 3877 | W293 | `opt/services/containers/container_integration.py` | 212 | blank line contains whitespace |
| 3876 | W293 | `opt/services/containers/container_integration.py` | 206 | blank line contains whitespace |
| 3871 | W293 | `opt/services/connection_pool.py` | 800 | blank line contains whitespace |
| 3870 | W293 | `opt/services/connection_pool.py` | 797 | blank line contains whitespace |
| 3869 | W293 | `opt/services/connection_pool.py` | 794 | blank line contains whitespace |
| 3868 | W293 | `opt/services/connection_pool.py` | 788 | blank line contains whitespace |
| 3867 | W293 | `opt/services/connection_pool.py` | 776 | blank line contains whitespace |
| 3866 | W293 | `opt/services/connection_pool.py` | 774 | blank line contains whitespace |
| 3864 | W293 | `opt/services/connection_pool.py` | 757 | blank line contains whitespace |
| 3863 | W293 | `opt/services/connection_pool.py` | 752 | blank line contains whitespace |
| 3862 | W293 | `opt/services/connection_pool.py` | 731 | blank line contains whitespace |
| 3861 | W293 | `opt/services/connection_pool.py` | 723 | blank line contains whitespace |
| 3860 | W293 | `opt/services/connection_pool.py` | 717 | blank line contains whitespace |
| 3859 | W293 | `opt/services/connection_pool.py` | 712 | blank line contains whitespace |
| 3858 | W293 | `opt/services/connection_pool.py` | 707 | blank line contains whitespace |
| 3857 | W293 | `opt/services/connection_pool.py` | 704 | blank line contains whitespace |
| 3856 | W293 | `opt/services/connection_pool.py` | 687 | blank line contains whitespace |
| 3855 | W293 | `opt/services/connection_pool.py` | 685 | blank line contains whitespace |
| 3854 | W293 | `opt/services/connection_pool.py` | 680 | blank line contains whitespace |
| 3853 | W293 | `opt/services/connection_pool.py` | 668 | blank line contains whitespace |
| 3852 | W293 | `opt/services/connection_pool.py` | 657 | blank line contains whitespace |
| 3851 | W293 | `opt/services/connection_pool.py` | 653 | blank line contains whitespace |
| 3850 | W293 | `opt/services/connection_pool.py` | 646 | blank line contains whitespace |
| 3849 | W293 | `opt/services/connection_pool.py` | 638 | blank line contains whitespace |
| 3848 | W293 | `opt/services/connection_pool.py` | 634 | blank line contains whitespace |
| 3847 | W293 | `opt/services/connection_pool.py` | 632 | blank line contains whitespace |
| 3846 | W293 | `opt/services/connection_pool.py` | 625 | blank line contains whitespace |
| 3845 | W293 | `opt/services/connection_pool.py` | 620 | blank line contains whitespace |
| 3844 | W293 | `opt/services/connection_pool.py` | 616 | blank line contains whitespace |
| 3843 | W293 | `opt/services/connection_pool.py` | 611 | blank line contains whitespace |
| 3842 | W293 | `opt/services/connection_pool.py` | 608 | blank line contains whitespace |
| 3841 | W293 | `opt/services/connection_pool.py` | 602 | blank line contains whitespace |
| 3840 | W293 | `opt/services/connection_pool.py` | 598 | blank line contains whitespace |
| 3839 | W293 | `opt/services/connection_pool.py` | 592 | blank line contains whitespace |
| 3838 | W293 | `opt/services/connection_pool.py` | 587 | blank line contains whitespace |
| 3837 | W293 | `opt/services/connection_pool.py` | 581 | blank line contains whitespace |
| 3836 | W293 | `opt/services/connection_pool.py` | 575 | blank line contains whitespace |
| 3835 | W293 | `opt/services/connection_pool.py` | 571 | blank line contains whitespace |
| 3834 | W293 | `opt/services/connection_pool.py` | 563 | blank line contains whitespace |
| 3833 | W293 | `opt/services/connection_pool.py` | 561 | blank line contains whitespace |
| 3832 | W293 | `opt/services/connection_pool.py` | 558 | blank line contains whitespace |
| 3831 | W293 | `opt/services/connection_pool.py` | 554 | blank line contains whitespace |
| 3830 | W293 | `opt/services/connection_pool.py` | 549 | blank line contains whitespace |
| 3829 | W293 | `opt/services/connection_pool.py` | 545 | blank line contains whitespace |
| 3828 | W293 | `opt/services/connection_pool.py` | 539 | blank line contains whitespace |
| 3827 | W293 | `opt/services/connection_pool.py` | 529 | blank line contains whitespace |
| 3826 | W293 | `opt/services/connection_pool.py` | 523 | blank line contains whitespace |
| 3825 | W293 | `opt/services/connection_pool.py` | 518 | blank line contains whitespace |
| 3824 | W293 | `opt/services/connection_pool.py` | 514 | blank line contains whitespace |
| 3823 | W293 | `opt/services/connection_pool.py` | 511 | blank line contains whitespace |
| 3822 | W293 | `opt/services/connection_pool.py` | 508 | blank line contains whitespace |
| 3821 | W293 | `opt/services/connection_pool.py` | 505 | blank line contains whitespace |
| 3820 | W293 | `opt/services/connection_pool.py` | 500 | blank line contains whitespace |
| 3819 | W293 | `opt/services/connection_pool.py` | 494 | blank line contains whitespace |
| 3818 | W293 | `opt/services/connection_pool.py` | 490 | blank line contains whitespace |
| 3817 | W293 | `opt/services/connection_pool.py` | 483 | blank line contains whitespace |
| 3816 | W293 | `opt/services/connection_pool.py` | 481 | blank line contains whitespace |
| 3815 | W293 | `opt/services/connection_pool.py` | 476 | blank line contains whitespace |
| 3814 | W293 | `opt/services/connection_pool.py` | 470 | blank line contains whitespace |
| 3813 | W293 | `opt/services/connection_pool.py` | 466 | blank line contains whitespace |
| 3812 | W293 | `opt/services/connection_pool.py` | 450 | blank line contains whitespace |
| 3811 | W293 | `opt/services/connection_pool.py` | 442 | blank line contains whitespace |
| 3810 | W293 | `opt/services/connection_pool.py` | 437 | blank line contains whitespace |
| 3809 | W293 | `opt/services/connection_pool.py` | 427 | blank line contains whitespace |
| 3808 | W293 | `opt/services/connection_pool.py` | 421 | blank line contains whitespace |
| 3807 | W293 | `opt/services/connection_pool.py` | 417 | blank line contains whitespace |
| 3806 | W293 | `opt/services/connection_pool.py` | 408 | blank line contains whitespace |
| 3805 | W293 | `opt/services/connection_pool.py` | 403 | blank line contains whitespace |
| 3804 | W293 | `opt/services/connection_pool.py` | 399 | blank line contains whitespace |
| 3803 | W293 | `opt/services/connection_pool.py` | 395 | blank line contains whitespace |
| 3802 | W293 | `opt/services/connection_pool.py` | 393 | blank line contains whitespace |
| 3801 | W293 | `opt/services/connection_pool.py` | 388 | blank line contains whitespace |
| 3800 | W293 | `opt/services/connection_pool.py` | 386 | blank line contains whitespace |
| 3799 | W293 | `opt/services/connection_pool.py` | 381 | blank line contains whitespace |
| 3798 | W293 | `opt/services/connection_pool.py` | 379 | blank line contains whitespace |
| 3797 | W293 | `opt/services/connection_pool.py` | 376 | blank line contains whitespace |
| 3796 | W293 | `opt/services/connection_pool.py` | 367 | blank line contains whitespace |
| 3795 | W293 | `opt/services/connection_pool.py` | 355 | blank line contains whitespace |
| 3794 | W293 | `opt/services/connection_pool.py` | 349 | blank line contains whitespace |
| 3793 | W293 | `opt/services/connection_pool.py` | 346 | blank line contains whitespace |
| 3792 | W293 | `opt/services/connection_pool.py` | 339 | blank line contains whitespace |
| 3791 | W293 | `opt/services/connection_pool.py` | 335 | blank line contains whitespace |
| 3790 | W293 | `opt/services/connection_pool.py` | 332 | blank line contains whitespace |
| 3789 | W293 | `opt/services/connection_pool.py` | 324 | blank line contains whitespace |
| 3788 | W293 | `opt/services/connection_pool.py` | 320 | blank line contains whitespace |
| 3787 | W293 | `opt/services/connection_pool.py` | 318 | blank line contains whitespace |
| 3786 | W293 | `opt/services/connection_pool.py` | 312 | blank line contains whitespace |
| 3785 | W293 | `opt/services/connection_pool.py` | 308 | blank line contains whitespace |
| 3784 | W293 | `opt/services/connection_pool.py` | 306 | blank line contains whitespace |
| 3783 | W293 | `opt/services/connection_pool.py` | 302 | blank line contains whitespace |
| 3782 | W293 | `opt/services/connection_pool.py` | 298 | blank line contains whitespace |
| 3781 | W293 | `opt/services/connection_pool.py` | 295 | blank line contains whitespace |
| 3780 | W293 | `opt/services/connection_pool.py` | 289 | blank line contains whitespace |
| 3779 | W293 | `opt/services/connection_pool.py` | 280 | blank line contains whitespace |
| 3778 | W293 | `opt/services/connection_pool.py` | 271 | blank line contains whitespace |
| 3777 | W293 | `opt/services/connection_pool.py` | 262 | blank line contains whitespace |
| 3776 | W293 | `opt/services/connection_pool.py` | 246 | blank line contains whitespace |
| 3775 | W293 | `opt/services/connection_pool.py` | 234 | blank line contains whitespace |
| 3774 | W293 | `opt/services/connection_pool.py` | 228 | blank line contains whitespace |
| 3773 | W293 | `opt/services/connection_pool.py` | 224 | blank line contains whitespace |
| 3772 | W293 | `opt/services/connection_pool.py` | 216 | blank line contains whitespace |
| 3771 | W293 | `opt/services/connection_pool.py` | 203 | blank line contains whitespace |
| 3770 | W293 | `opt/services/connection_pool.py` | 198 | blank line contains whitespace |
| 3769 | W293 | `opt/services/connection_pool.py` | 193 | blank line contains whitespace |
| 3768 | W293 | `opt/services/connection_pool.py` | 177 | blank line contains whitespace |
| 3767 | W293 | `opt/services/connection_pool.py` | 171 | blank line contains whitespace |
| 3766 | W293 | `opt/services/connection_pool.py` | 168 | blank line contains whitespace |
| 3765 | W293 | `opt/services/connection_pool.py` | 163 | blank line contains whitespace |
| 3764 | W293 | `opt/services/connection_pool.py` | 140 | blank line contains whitespace |
| 3763 | W293 | `opt/services/connection_pool.py` | 136 | blank line contains whitespace |
| 3762 | W293 | `opt/services/connection_pool.py` | 132 | blank line contains whitespace |
| 3761 | W293 | `opt/services/connection_pool.py` | 125 | blank line contains whitespace |
| 3760 | W293 | `opt/services/connection_pool.py` | 120 | blank line contains whitespace |
| 3759 | W293 | `opt/services/connection_pool.py` | 108 | blank line contains whitespace |
| 3758 | W293 | `opt/services/connection_pool.py` | 103 | blank line contains whitespace |
| 3757 | W293 | `opt/services/connection_pool.py` | 94 | blank line contains whitespace |
| 3756 | W293 | `opt/services/connection_pool.py` | 85 | blank line contains whitespace |
| 3755 | W293 | `opt/services/connection_pool.py` | 80 | blank line contains whitespace |
| 3754 | W293 | `opt/services/connection_pool.py` | 74 | blank line contains whitespace |
| 3753 | W293 | `opt/services/connection_pool.py` | 69 | blank line contains whitespace |
| 3752 | W293 | `opt/services/connection_pool.py` | 65 | blank line contains whitespace |
| 3747 | W293 | `opt/services/compliance/core.py` | 92 | blank line contains whitespace |
| 3746 | W293 | `opt/services/compliance/core.py` | 88 | blank line contains whitespace |
| 3745 | W293 | `opt/services/compliance/core.py` | 83 | blank line contains whitespace |
| 3740 | W293 | `opt/services/compliance/cli.py` | 61 | blank line contains whitespace |
| 3739 | W293 | `opt/services/compliance/cli.py` | 34 | blank line contains whitespace |
| 3738 | W293 | `opt/services/compliance/cli.py` | 24 | blank line contains whitespace |
| 3730 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1260 | blank line contains whitespace |
| 3729 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1254 | blank line contains whitespace |
| 3728 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1248 | blank line contains whitespace |
| 3727 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1241 | blank line contains whitespace |
| 3726 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1235 | blank line contains whitespace |
| 3725 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1224 | blank line contains whitespace |
| 3724 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1215 | blank line contains whitespace |
| 3722 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1206 | blank line contains whitespace |
| 3721 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1204 | blank line contains whitespace |
| 3720 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1187 | blank line contains whitespace |
| 3719 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1182 | blank line contains whitespace |
| 3718 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1175 | blank line contains whitespace |
| 3717 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1159 | blank line contains whitespace |
| 3716 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1155 | blank line contains whitespace |
| 3715 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1148 | blank line contains whitespace |
| 3714 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1144 | blank line contains whitespace |
| 3713 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1132 | blank line contains whitespace |
| 3712 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1123 | blank line contains whitespace |
| 3711 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1117 | blank line contains whitespace |
| 3710 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1114 | blank line contains whitespace |
| 3709 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1109 | blank line contains whitespace |
| 3708 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1104 | blank line contains whitespace |
| 3707 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1102 | blank line contains whitespace |
| 3706 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1095 | blank line contains whitespace |
| 3705 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1085 | blank line contains whitespace |
| 3704 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1072 | blank line contains whitespace |
| 3703 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1060 | blank line contains whitespace |
| 3702 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1050 | blank line contains whitespace |
| 3701 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1042 | blank line contains whitespace |
| 3700 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1027 | blank line contains whitespace |
| 3699 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1024 | blank line contains whitespace |
| 3698 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1014 | blank line contains whitespace |
| 3697 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1009 | blank line contains whitespace |
| 3696 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 1005 | blank line contains whitespace |
| 3695 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 996 | blank line contains whitespace |
| 3694 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 987 | blank line contains whitespace |
| 3693 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 970 | blank line contains whitespace |
| 3692 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 960 | blank line contains whitespace |
| 3691 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 958 | blank line contains whitespace |
| 3690 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 952 | blank line contains whitespace |
| 3689 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 939 | blank line contains whitespace |
| 3688 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 925 | blank line contains whitespace |
| 3687 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 923 | blank line contains whitespace |
| 3686 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 920 | blank line contains whitespace |
| 3685 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 909 | blank line contains whitespace |
| 3684 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 906 | blank line contains whitespace |
| 3683 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 897 | blank line contains whitespace |
| 3682 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 893 | blank line contains whitespace |
| 3681 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 874 | blank line contains whitespace |
| 3680 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 864 | blank line contains whitespace |
| 3679 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 851 | blank line contains whitespace |
| 3678 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 849 | blank line contains whitespace |
| 3677 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 846 | blank line contains whitespace |
| 3676 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 841 | blank line contains whitespace |
| 3675 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 826 | blank line contains whitespace |
| 3674 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 822 | blank line contains whitespace |
| 3673 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 800 | blank line contains whitespace |
| 3672 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 798 | blank line contains whitespace |
| 3671 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 793 | blank line contains whitespace |
| 3670 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 786 | blank line contains whitespace |
| 3669 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 782 | blank line contains whitespace |
| 3668 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 780 | blank line contains whitespace |
| 3667 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 776 | blank line contains whitespace |
| 3666 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 771 | blank line contains whitespace |
| 3665 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 765 | blank line contains whitespace |
| 3664 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 761 | blank line contains whitespace |
| 3663 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 752 | blank line contains whitespace |
| 3662 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 750 | blank line contains whitespace |
| 3661 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 745 | blank line contains whitespace |
| 3660 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 738 | blank line contains whitespace |
| 3659 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 730 | blank line contains whitespace |
| 3658 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 723 | blank line contains whitespace |
| 3657 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 721 | blank line contains whitespace |
| 3656 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 716 | blank line contains whitespace |
| 3655 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 713 | blank line contains whitespace |
| 3654 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 708 | blank line contains whitespace |
| 3653 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 705 | blank line contains whitespace |
| 3652 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 697 | blank line contains whitespace |
| 3651 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 693 | blank line contains whitespace |
| 3650 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 687 | blank line contains whitespace |
| 3649 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 680 | blank line contains whitespace |
| 3648 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 668 | blank line contains whitespace |
| 3647 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 659 | blank line contains whitespace |
| 3646 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 655 | blank line contains whitespace |
| 3645 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 652 | blank line contains whitespace |
| 3644 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 647 | blank line contains whitespace |
| 3643 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 645 | blank line contains whitespace |
| 3642 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 641 | blank line contains whitespace |
| 3641 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 629 | blank line contains whitespace |
| 3640 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 616 | blank line contains whitespace |
| 3639 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 607 | blank line contains whitespace |
| 3638 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 604 | blank line contains whitespace |
| 3637 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 601 | blank line contains whitespace |
| 3636 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 588 | blank line contains whitespace |
| 3635 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 575 | blank line contains whitespace |
| 3634 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 573 | blank line contains whitespace |
| 3633 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 567 | blank line contains whitespace |
| 3632 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 563 | blank line contains whitespace |
| 3631 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 551 | blank line contains whitespace |
| 3630 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 538 | blank line contains whitespace |
| 3629 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 528 | blank line contains whitespace |
| 3628 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 523 | blank line contains whitespace |
| 3627 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 518 | blank line contains whitespace |
| 3626 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 508 | blank line contains whitespace |
| 3625 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 505 | blank line contains whitespace |
| 3624 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 502 | blank line contains whitespace |
| 3623 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 498 | blank line contains whitespace |
| 3622 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 496 | blank line contains whitespace |
| 3621 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 492 | blank line contains whitespace |
| 3620 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 485 | blank line contains whitespace |
| 3619 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 482 | blank line contains whitespace |
| 3618 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 478 | blank line contains whitespace |
| 3617 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 473 | blank line contains whitespace |
| 3616 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 470 | blank line contains whitespace |
| 3615 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 455 | blank line contains whitespace |
| 3614 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 453 | blank line contains whitespace |
| 3613 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 445 | blank line contains whitespace |
| 3612 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 441 | blank line contains whitespace |
| 3611 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 433 | blank line contains whitespace |
| 3610 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 426 | blank line contains whitespace |
| 3609 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 418 | blank line contains whitespace |
| 3608 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 412 | blank line contains whitespace |
| 3607 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 406 | blank line contains whitespace |
| 3606 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 402 | blank line contains whitespace |
| 3605 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 397 | blank line contains whitespace |
| 3604 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 393 | blank line contains whitespace |
| 3603 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 389 | blank line contains whitespace |
| 3602 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 379 | blank line contains whitespace |
| 3601 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 372 | blank line contains whitespace |
| 3600 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 367 | blank line contains whitespace |
| 3599 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 355 | blank line contains whitespace |
| 3598 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 351 | blank line contains whitespace |
| 3597 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 349 | blank line contains whitespace |
| 3596 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 342 | blank line contains whitespace |
| 3595 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 335 | blank line contains whitespace |
| 3594 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 327 | blank line contains whitespace |
| 3593 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 322 | blank line contains whitespace |
| 3592 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 314 | blank line contains whitespace |
| 3591 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 309 | blank line contains whitespace |
| 3590 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 307 | blank line contains whitespace |
| 3589 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 304 | blank line contains whitespace |
| 3588 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 298 | blank line contains whitespace |
| 3587 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 296 | blank line contains whitespace |
| 3586 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 291 | blank line contains whitespace |
| 3585 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 289 | blank line contains whitespace |
| 3584 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 286 | blank line contains whitespace |
| 3583 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 279 | blank line contains whitespace |
| 3581 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 273 | blank line contains whitespace |
| 3580 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 266 | blank line contains whitespace |
| 3579 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 256 | blank line contains whitespace |
| 3578 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 246 | blank line contains whitespace |
| 3577 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 243 | blank line contains whitespace |
| 3576 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 238 | blank line contains whitespace |
| 3575 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 232 | blank line contains whitespace |
| 3574 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 227 | blank line contains whitespace |
| 3573 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 224 | blank line contains whitespace |
| 3572 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 219 | blank line contains whitespace |
| 3571 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 213 | blank line contains whitespace |
| 3570 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 208 | blank line contains whitespace |
| 3569 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 204 | blank line contains whitespace |
| 3568 | W293 | `opt/services/cluster/large_cluster_optimizer.py` | 199 | blank line contains whitespace |
| 3562 | W293 | `opt/services/cache.py` | 585 | blank line contains whitespace |
| 3561 | W293 | `opt/services/cache.py` | 580 | blank line contains whitespace |
| 3560 | W293 | `opt/services/cache.py` | 569 | blank line contains whitespace |
| 3559 | W293 | `opt/services/cache.py` | 557 | blank line contains whitespace |
| 3558 | W293 | `opt/services/cache.py` | 552 | blank line contains whitespace |
| 3557 | W293 | `opt/services/cache.py` | 546 | blank line contains whitespace |
| 3556 | W293 | `opt/services/cache.py` | 544 | blank line contains whitespace |
| 3555 | W293 | `opt/services/cache.py` | 542 | blank line contains whitespace |
| 3554 | W293 | `opt/services/cache.py` | 538 | blank line contains whitespace |
| 3553 | W293 | `opt/services/cache.py` | 535 | blank line contains whitespace |
| 3552 | W293 | `opt/services/cache.py` | 529 | blank line contains whitespace |
| 3551 | W293 | `opt/services/cache.py` | 522 | blank line contains whitespace |
| 3550 | W293 | `opt/services/cache.py` | 504 | blank line contains whitespace |
| 3549 | W293 | `opt/services/cache.py` | 499 | blank line contains whitespace |
| 3548 | W293 | `opt/services/cache.py` | 493 | blank line contains whitespace |
| 3547 | W293 | `opt/services/cache.py` | 487 | blank line contains whitespace |
| 3546 | W293 | `opt/services/cache.py` | 481 | blank line contains whitespace |
| 3545 | W293 | `opt/services/cache.py` | 475 | blank line contains whitespace |
| 3544 | W293 | `opt/services/cache.py` | 457 | blank line contains whitespace |
| 3543 | W293 | `opt/services/cache.py` | 453 | blank line contains whitespace |
| 3542 | W293 | `opt/services/cache.py` | 442 | blank line contains whitespace |
| 3541 | W293 | `opt/services/cache.py` | 432 | blank line contains whitespace |
| 3540 | W293 | `opt/services/cache.py` | 421 | blank line contains whitespace |
| 3539 | W293 | `opt/services/cache.py` | 413 | blank line contains whitespace |
| 3538 | W293 | `opt/services/cache.py` | 405 | blank line contains whitespace |
| 3537 | W293 | `opt/services/cache.py` | 400 | blank line contains whitespace |
| 3536 | W293 | `opt/services/cache.py` | 389 | blank line contains whitespace |
| 3535 | W293 | `opt/services/cache.py` | 384 | blank line contains whitespace |
| 3534 | W293 | `opt/services/cache.py` | 364 | blank line contains whitespace |
| 3533 | W293 | `opt/services/cache.py` | 359 | blank line contains whitespace |
| 3532 | W293 | `opt/services/cache.py` | 351 | blank line contains whitespace |
| 3531 | W293 | `opt/services/cache.py` | 346 | blank line contains whitespace |
| 3530 | W293 | `opt/services/cache.py` | 330 | blank line contains whitespace |
| 3529 | W293 | `opt/services/cache.py` | 324 | blank line contains whitespace |
| 3528 | W293 | `opt/services/cache.py` | 315 | blank line contains whitespace |
| 3527 | W293 | `opt/services/cache.py` | 306 | blank line contains whitespace |
| 3526 | W293 | `opt/services/cache.py` | 302 | blank line contains whitespace |
| 3525 | W293 | `opt/services/cache.py` | 296 | blank line contains whitespace |
| 3524 | W293 | `opt/services/cache.py` | 289 | blank line contains whitespace |
| 3523 | W293 | `opt/services/cache.py` | 274 | blank line contains whitespace |
| 3522 | W293 | `opt/services/cache.py` | 269 | blank line contains whitespace |
| 3521 | W293 | `opt/services/cache.py` | 261 | blank line contains whitespace |
| 3520 | W293 | `opt/services/cache.py` | 255 | blank line contains whitespace |
| 3519 | W293 | `opt/services/cache.py` | 244 | blank line contains whitespace |
| 3518 | W293 | `opt/services/cache.py` | 232 | blank line contains whitespace |
| 3517 | W293 | `opt/services/cache.py` | 224 | blank line contains whitespace |
| 3516 | W293 | `opt/services/cache.py` | 211 | blank line contains whitespace |
| 3515 | W293 | `opt/services/cache.py` | 198 | blank line contains whitespace |
| 3514 | W293 | `opt/services/cache.py` | 196 | blank line contains whitespace |
| 3513 | W293 | `opt/services/cache.py` | 189 | blank line contains whitespace |
| 3512 | W293 | `opt/services/cache.py` | 185 | blank line contains whitespace |
| 3511 | W293 | `opt/services/cache.py` | 178 | blank line contains whitespace |
| 3510 | W293 | `opt/services/cache.py` | 173 | blank line contains whitespace |
| 3509 | W293 | `opt/services/cache.py` | 167 | blank line contains whitespace |
| 3508 | W293 | `opt/services/cache.py` | 161 | blank line contains whitespace |
| 3507 | W293 | `opt/services/cache.py` | 152 | blank line contains whitespace |
| 3506 | W293 | `opt/services/cache.py` | 147 | blank line contains whitespace |
| 3505 | W293 | `opt/services/cache.py` | 142 | blank line contains whitespace |
| 3504 | W293 | `opt/services/cache.py` | 137 | blank line contains whitespace |
| 3503 | W293 | `opt/services/cache.py` | 132 | blank line contains whitespace |
| 3502 | W293 | `opt/services/cache.py` | 127 | blank line contains whitespace |
| 3501 | W293 | `opt/services/cache.py` | 122 | blank line contains whitespace |
| 3500 | W293 | `opt/services/cache.py` | 105 | blank line contains whitespace |
| 3499 | W293 | `opt/services/cache.py` | 98 | blank line contains whitespace |
| 3498 | W293 | `opt/services/cache.py` | 78 | blank line contains whitespace |
| 3497 | W293 | `opt/services/cache.py` | 72 | blank line contains whitespace |
| 3493 | W293 | `opt/services/business_metrics.py` | 859 | blank line contains whitespace |
| 3492 | W293 | `opt/services/business_metrics.py` | 853 | blank line contains whitespace |
| 3491 | W293 | `opt/services/business_metrics.py` | 848 | blank line contains whitespace |
| 3490 | W293 | `opt/services/business_metrics.py` | 842 | blank line contains whitespace |
| 3489 | W293 | `opt/services/business_metrics.py` | 837 | blank line contains whitespace |
| 3488 | W293 | `opt/services/business_metrics.py` | 831 | blank line contains whitespace |
| 3487 | W293 | `opt/services/business_metrics.py` | 828 | blank line contains whitespace |
| 3486 | W293 | `opt/services/business_metrics.py` | 825 | blank line contains whitespace |
| 3485 | W293 | `opt/services/business_metrics.py` | 793 | blank line contains whitespace |
| 3484 | W293 | `opt/services/business_metrics.py` | 782 | blank line contains whitespace |
| 3483 | W293 | `opt/services/business_metrics.py` | 779 | blank line contains whitespace |
| 3482 | W293 | `opt/services/business_metrics.py` | 774 | blank line contains whitespace |
| 3481 | W293 | `opt/services/business_metrics.py` | 771 | blank line contains whitespace |
| 3480 | W293 | `opt/services/business_metrics.py` | 764 | blank line contains whitespace |
| 3479 | W293 | `opt/services/business_metrics.py` | 758 | blank line contains whitespace |
| 3478 | W293 | `opt/services/business_metrics.py` | 753 | blank line contains whitespace |
| 3477 | W293 | `opt/services/business_metrics.py` | 750 | blank line contains whitespace |
| 3476 | W293 | `opt/services/business_metrics.py` | 739 | blank line contains whitespace |
| 3475 | W293 | `opt/services/business_metrics.py` | 735 | blank line contains whitespace |
| 3474 | W293 | `opt/services/business_metrics.py` | 719 | blank line contains whitespace |
| 3473 | W293 | `opt/services/business_metrics.py` | 697 | blank line contains whitespace |
| 3472 | W293 | `opt/services/business_metrics.py` | 686 | blank line contains whitespace |
| 3471 | W293 | `opt/services/business_metrics.py` | 682 | blank line contains whitespace |
| 3470 | W293 | `opt/services/business_metrics.py` | 673 | blank line contains whitespace |
| 3469 | W293 | `opt/services/business_metrics.py` | 659 | blank line contains whitespace |
| 3468 | W293 | `opt/services/business_metrics.py` | 642 | blank line contains whitespace |
| 3467 | W293 | `opt/services/business_metrics.py` | 638 | blank line contains whitespace |
| 3466 | W293 | `opt/services/business_metrics.py` | 636 | blank line contains whitespace |
| 3465 | W293 | `opt/services/business_metrics.py` | 632 | blank line contains whitespace |
| 3464 | W293 | `opt/services/business_metrics.py` | 624 | blank line contains whitespace |
| 3463 | W293 | `opt/services/business_metrics.py` | 615 | blank line contains whitespace |
| 3462 | W293 | `opt/services/business_metrics.py` | 610 | blank line contains whitespace |
| 3461 | W293 | `opt/services/business_metrics.py` | 606 | blank line contains whitespace |
| 3460 | W293 | `opt/services/business_metrics.py` | 602 | blank line contains whitespace |
| 3459 | W293 | `opt/services/business_metrics.py` | 600 | blank line contains whitespace |
| 3458 | W293 | `opt/services/business_metrics.py` | 595 | blank line contains whitespace |
| 3457 | W293 | `opt/services/business_metrics.py` | 590 | blank line contains whitespace |
| 3456 | W293 | `opt/services/business_metrics.py` | 586 | blank line contains whitespace |
| 3455 | W293 | `opt/services/business_metrics.py` | 582 | blank line contains whitespace |
| 3454 | W293 | `opt/services/business_metrics.py` | 577 | blank line contains whitespace |
| 3453 | W293 | `opt/services/business_metrics.py` | 573 | blank line contains whitespace |
| 3452 | W293 | `opt/services/business_metrics.py` | 554 | blank line contains whitespace |
| 3451 | W293 | `opt/services/business_metrics.py` | 550 | blank line contains whitespace |
| 3450 | W293 | `opt/services/business_metrics.py` | 541 | blank line contains whitespace |
| 3449 | W293 | `opt/services/business_metrics.py` | 537 | blank line contains whitespace |
| 3448 | W293 | `opt/services/business_metrics.py` | 533 | blank line contains whitespace |
| 3447 | W293 | `opt/services/business_metrics.py` | 529 | blank line contains whitespace |
| 3446 | W293 | `opt/services/business_metrics.py` | 525 | blank line contains whitespace |
| 3445 | W293 | `opt/services/business_metrics.py` | 521 | blank line contains whitespace |
| 3444 | W293 | `opt/services/business_metrics.py` | 514 | blank line contains whitespace |
| 3443 | W293 | `opt/services/business_metrics.py` | 510 | blank line contains whitespace |
| 3442 | W293 | `opt/services/business_metrics.py` | 499 | blank line contains whitespace |
| 3441 | W293 | `opt/services/business_metrics.py` | 488 | blank line contains whitespace |
| 3440 | W293 | `opt/services/business_metrics.py` | 478 | blank line contains whitespace |
| 3439 | W293 | `opt/services/business_metrics.py` | 474 | blank line contains whitespace |
| 3438 | W293 | `opt/services/business_metrics.py` | 472 | blank line contains whitespace |
| 3437 | W293 | `opt/services/business_metrics.py` | 468 | blank line contains whitespace |
| 3436 | W293 | `opt/services/business_metrics.py` | 459 | blank line contains whitespace |
| 3435 | W293 | `opt/services/business_metrics.py` | 450 | blank line contains whitespace |
| 3434 | W293 | `opt/services/business_metrics.py` | 446 | blank line contains whitespace |
| 3433 | W293 | `opt/services/business_metrics.py` | 437 | blank line contains whitespace |
| 3432 | W293 | `opt/services/business_metrics.py` | 425 | blank line contains whitespace |
| 3431 | W293 | `opt/services/business_metrics.py` | 415 | blank line contains whitespace |
| 3430 | W293 | `opt/services/business_metrics.py` | 406 | blank line contains whitespace |
| 3429 | W293 | `opt/services/business_metrics.py` | 402 | blank line contains whitespace |
| 3428 | W293 | `opt/services/business_metrics.py` | 398 | blank line contains whitespace |
| 3427 | W293 | `opt/services/business_metrics.py` | 388 | blank line contains whitespace |
| 3426 | W293 | `opt/services/business_metrics.py` | 379 | blank line contains whitespace |
| 3425 | W293 | `opt/services/business_metrics.py` | 375 | blank line contains whitespace |
| 3424 | W293 | `opt/services/business_metrics.py` | 371 | blank line contains whitespace |
| 3423 | W293 | `opt/services/business_metrics.py` | 365 | blank line contains whitespace |
| 3422 | W293 | `opt/services/business_metrics.py` | 357 | blank line contains whitespace |
| 3421 | W293 | `opt/services/business_metrics.py` | 355 | blank line contains whitespace |
| 3420 | W293 | `opt/services/business_metrics.py` | 350 | blank line contains whitespace |
| 3419 | W293 | `opt/services/business_metrics.py` | 335 | blank line contains whitespace |
| 3418 | W293 | `opt/services/business_metrics.py` | 319 | blank line contains whitespace |
| 3417 | W293 | `opt/services/business_metrics.py` | 304 | blank line contains whitespace |
| 3416 | W293 | `opt/services/business_metrics.py` | 289 | blank line contains whitespace |
| 3415 | W293 | `opt/services/business_metrics.py` | 274 | blank line contains whitespace |
| 3414 | W293 | `opt/services/business_metrics.py` | 254 | blank line contains whitespace |
| 3413 | W293 | `opt/services/business_metrics.py` | 231 | blank line contains whitespace |
| 3412 | W293 | `opt/services/business_metrics.py` | 200 | blank line contains whitespace |
| 3411 | W293 | `opt/services/business_metrics.py` | 192 | blank line contains whitespace |
| 3410 | W293 | `opt/services/business_metrics.py` | 176 | blank line contains whitespace |
| 3409 | W293 | `opt/services/business_metrics.py` | 164 | blank line contains whitespace |
| 3408 | W293 | `opt/services/business_metrics.py` | 159 | blank line contains whitespace |
| 3407 | W293 | `opt/services/business_metrics.py` | 154 | blank line contains whitespace |
| 3406 | W293 | `opt/services/business_metrics.py` | 149 | blank line contains whitespace |
| 3405 | W293 | `opt/services/business_metrics.py` | 142 | blank line contains whitespace |
| 3404 | W293 | `opt/services/business_metrics.py` | 137 | blank line contains whitespace |
| 3403 | W293 | `opt/services/business_metrics.py` | 131 | blank line contains whitespace |
| 3402 | W293 | `opt/services/business_metrics.py` | 125 | blank line contains whitespace |
| 3401 | W293 | `opt/services/business_metrics.py` | 113 | blank line contains whitespace |
| 3400 | W293 | `opt/services/business_metrics.py` | 108 | blank line contains whitespace |
| 3399 | W293 | `opt/services/business_metrics.py` | 104 | blank line contains whitespace |
| 3398 | W293 | `opt/services/business_metrics.py` | 94 | blank line contains whitespace |
| 3397 | W293 | `opt/services/business_metrics.py` | 84 | blank line contains whitespace |
| 3396 | W293 | `opt/services/business_metrics.py` | 77 | blank line contains whitespace |
| 3393 | W293 | `opt/services/billing/billing_integration.py` | 1079 | blank line contains whitespace |
| 3392 | W293 | `opt/services/billing/billing_integration.py` | 1077 | blank line contains whitespace |
| 3391 | W293 | `opt/services/billing/billing_integration.py` | 1072 | blank line contains whitespace |
| 3390 | W293 | `opt/services/billing/billing_integration.py` | 1061 | blank line contains whitespace |
| 3389 | W293 | `opt/services/billing/billing_integration.py` | 1055 | blank line contains whitespace |
| 3388 | W293 | `opt/services/billing/billing_integration.py` | 1048 | blank line contains whitespace |
| 3387 | W293 | `opt/services/billing/billing_integration.py` | 1044 | blank line contains whitespace |
| 3386 | W293 | `opt/services/billing/billing_integration.py` | 1040 | blank line contains whitespace |
| 3385 | W293 | `opt/services/billing/billing_integration.py` | 1036 | blank line contains whitespace |
| 3384 | W293 | `opt/services/billing/billing_integration.py` | 1028 | blank line contains whitespace |
| 3383 | W293 | `opt/services/billing/billing_integration.py` | 1026 | blank line contains whitespace |
| 3382 | W291 | `opt/services/billing/billing_integration.py` | 1012 | trailing whitespace |
| 3381 | W293 | `opt/services/billing/billing_integration.py` | 1003 | blank line contains whitespace |
| 3380 | W293 | `opt/services/billing/billing_integration.py` | 999 | blank line contains whitespace |
| 3379 | W293 | `opt/services/billing/billing_integration.py` | 990 | blank line contains whitespace |
| 3378 | W291 | `opt/services/billing/billing_integration.py` | 986 | trailing whitespace |
| 3377 | W293 | `opt/services/billing/billing_integration.py` | 972 | blank line contains whitespace |
| 3376 | W293 | `opt/services/billing/billing_integration.py` | 968 | blank line contains whitespace |
| 3375 | W293 | `opt/services/billing/billing_integration.py` | 965 | blank line contains whitespace |
| 3374 | W293 | `opt/services/billing/billing_integration.py` | 962 | blank line contains whitespace |
| 3373 | W293 | `opt/services/billing/billing_integration.py` | 959 | blank line contains whitespace |
| 3372 | W293 | `opt/services/billing/billing_integration.py` | 951 | blank line contains whitespace |
| 3371 | W293 | `opt/services/billing/billing_integration.py` | 943 | blank line contains whitespace |
| 3370 | W293 | `opt/services/billing/billing_integration.py` | 937 | blank line contains whitespace |
| 3369 | W293 | `opt/services/billing/billing_integration.py` | 932 | blank line contains whitespace |
| 3368 | W291 | `opt/services/billing/billing_integration.py` | 926 | trailing whitespace |
| 3367 | W293 | `opt/services/billing/billing_integration.py` | 925 | blank line contains whitespace |
| 3366 | W293 | `opt/services/billing/billing_integration.py` | 921 | blank line contains whitespace |
| 3365 | W293 | `opt/services/billing/billing_integration.py` | 918 | blank line contains whitespace |
| 3364 | W293 | `opt/services/billing/billing_integration.py` | 913 | blank line contains whitespace |
| 3363 | W293 | `opt/services/billing/billing_integration.py` | 910 | blank line contains whitespace |
| 3362 | W293 | `opt/services/billing/billing_integration.py` | 905 | blank line contains whitespace |
| 3361 | W293 | `opt/services/billing/billing_integration.py` | 901 | blank line contains whitespace |
| 3360 | W293 | `opt/services/billing/billing_integration.py` | 893 | blank line contains whitespace |
| 3359 | W293 | `opt/services/billing/billing_integration.py` | 890 | blank line contains whitespace |
| 3358 | W293 | `opt/services/billing/billing_integration.py` | 884 | blank line contains whitespace |
| 3357 | W293 | `opt/services/billing/billing_integration.py` | 875 | blank line contains whitespace |
| 3356 | W293 | `opt/services/billing/billing_integration.py` | 872 | blank line contains whitespace |
| 3355 | W293 | `opt/services/billing/billing_integration.py` | 866 | blank line contains whitespace |
| 3354 | W293 | `opt/services/billing/billing_integration.py` | 862 | blank line contains whitespace |
| 3353 | W293 | `opt/services/billing/billing_integration.py` | 858 | blank line contains whitespace |
| 3352 | W293 | `opt/services/billing/billing_integration.py` | 856 | blank line contains whitespace |
| 3351 | W293 | `opt/services/billing/billing_integration.py` | 850 | blank line contains whitespace |
| 3350 | W293 | `opt/services/billing/billing_integration.py` | 847 | blank line contains whitespace |
| 3349 | W293 | `opt/services/billing/billing_integration.py` | 843 | blank line contains whitespace |
| 3348 | W293 | `opt/services/billing/billing_integration.py` | 838 | blank line contains whitespace |
| 3347 | W293 | `opt/services/billing/billing_integration.py` | 835 | blank line contains whitespace |
| 3346 | W293 | `opt/services/billing/billing_integration.py` | 832 | blank line contains whitespace |
| 3345 | W293 | `opt/services/billing/billing_integration.py` | 827 | blank line contains whitespace |
| 3344 | W293 | `opt/services/billing/billing_integration.py` | 822 | blank line contains whitespace |
| 3343 | W293 | `opt/services/billing/billing_integration.py` | 818 | blank line contains whitespace |
| 3342 | W293 | `opt/services/billing/billing_integration.py` | 810 | blank line contains whitespace |
| 3341 | W293 | `opt/services/billing/billing_integration.py` | 806 | blank line contains whitespace |
| 3340 | W293 | `opt/services/billing/billing_integration.py` | 804 | blank line contains whitespace |
| 3339 | W293 | `opt/services/billing/billing_integration.py` | 797 | blank line contains whitespace |
| 3338 | W293 | `opt/services/billing/billing_integration.py` | 792 | blank line contains whitespace |
| 3337 | W293 | `opt/services/billing/billing_integration.py` | 785 | blank line contains whitespace |
| 3336 | W293 | `opt/services/billing/billing_integration.py` | 780 | blank line contains whitespace |
| 3335 | W293 | `opt/services/billing/billing_integration.py` | 777 | blank line contains whitespace |
| 3334 | W293 | `opt/services/billing/billing_integration.py` | 772 | blank line contains whitespace |
| 3333 | W293 | `opt/services/billing/billing_integration.py` | 762 | blank line contains whitespace |
| 3332 | W293 | `opt/services/billing/billing_integration.py` | 752 | blank line contains whitespace |
| 3331 | W293 | `opt/services/billing/billing_integration.py` | 748 | blank line contains whitespace |
| 3330 | W293 | `opt/services/billing/billing_integration.py` | 733 | blank line contains whitespace |
| 3329 | W293 | `opt/services/billing/billing_integration.py` | 728 | blank line contains whitespace |
| 3328 | W293 | `opt/services/billing/billing_integration.py` | 724 | blank line contains whitespace |
| 3327 | W293 | `opt/services/billing/billing_integration.py` | 721 | blank line contains whitespace |
| 3326 | W293 | `opt/services/billing/billing_integration.py` | 713 | blank line contains whitespace |
| 3325 | W293 | `opt/services/billing/billing_integration.py` | 708 | blank line contains whitespace |
| 3324 | W293 | `opt/services/billing/billing_integration.py` | 700 | blank line contains whitespace |
| 3323 | W293 | `opt/services/billing/billing_integration.py` | 689 | blank line contains whitespace |
| 3322 | W293 | `opt/services/billing/billing_integration.py` | 680 | blank line contains whitespace |
| 3321 | W293 | `opt/services/billing/billing_integration.py` | 660 | blank line contains whitespace |
| 3320 | W293 | `opt/services/billing/billing_integration.py` | 656 | blank line contains whitespace |
| 3319 | W293 | `opt/services/billing/billing_integration.py` | 635 | blank line contains whitespace |
| 3318 | W293 | `opt/services/billing/billing_integration.py` | 629 | blank line contains whitespace |
| 3317 | W293 | `opt/services/billing/billing_integration.py` | 624 | blank line contains whitespace |
| 3316 | W293 | `opt/services/billing/billing_integration.py` | 622 | blank line contains whitespace |
| 3315 | W293 | `opt/services/billing/billing_integration.py` | 610 | blank line contains whitespace |
| 3314 | W293 | `opt/services/billing/billing_integration.py` | 604 | blank line contains whitespace |
| 3313 | W293 | `opt/services/billing/billing_integration.py` | 594 | blank line contains whitespace |
| 3312 | W293 | `opt/services/billing/billing_integration.py` | 589 | blank line contains whitespace |
| 3311 | W293 | `opt/services/billing/billing_integration.py` | 576 | blank line contains whitespace |
| 3310 | W293 | `opt/services/billing/billing_integration.py` | 571 | blank line contains whitespace |
| 3309 | W293 | `opt/services/billing/billing_integration.py` | 559 | blank line contains whitespace |
| 3308 | W293 | `opt/services/billing/billing_integration.py` | 557 | blank line contains whitespace |
| 3307 | W293 | `opt/services/billing/billing_integration.py` | 554 | blank line contains whitespace |
| 3306 | W293 | `opt/services/billing/billing_integration.py` | 549 | blank line contains whitespace |
| 3305 | W293 | `opt/services/billing/billing_integration.py` | 544 | blank line contains whitespace |
| 3304 | W293 | `opt/services/billing/billing_integration.py` | 541 | blank line contains whitespace |
| 3303 | W293 | `opt/services/billing/billing_integration.py` | 532 | blank line contains whitespace |
| 3302 | W293 | `opt/services/billing/billing_integration.py` | 527 | blank line contains whitespace |
| 3301 | W293 | `opt/services/billing/billing_integration.py` | 517 | blank line contains whitespace |
| 3300 | W293 | `opt/services/billing/billing_integration.py` | 512 | blank line contains whitespace |
| 3299 | W293 | `opt/services/billing/billing_integration.py` | 507 | blank line contains whitespace |
| 3298 | W293 | `opt/services/billing/billing_integration.py` | 490 | blank line contains whitespace |
| 3297 | W293 | `opt/services/billing/billing_integration.py` | 486 | blank line contains whitespace |
| 3296 | W293 | `opt/services/billing/billing_integration.py` | 477 | blank line contains whitespace |
| 3295 | W293 | `opt/services/billing/billing_integration.py` | 465 | blank line contains whitespace |
| 3294 | W293 | `opt/services/billing/billing_integration.py` | 458 | blank line contains whitespace |
| 3293 | W293 | `opt/services/billing/billing_integration.py` | 454 | blank line contains whitespace |
| 3292 | W293 | `opt/services/billing/billing_integration.py` | 444 | blank line contains whitespace |
| 3291 | W293 | `opt/services/billing/billing_integration.py` | 441 | blank line contains whitespace |
| 3290 | W293 | `opt/services/billing/billing_integration.py` | 434 | blank line contains whitespace |
| 3289 | W293 | `opt/services/billing/billing_integration.py` | 431 | blank line contains whitespace |
| 3288 | W293 | `opt/services/billing/billing_integration.py` | 427 | blank line contains whitespace |
| 3287 | W293 | `opt/services/billing/billing_integration.py` | 424 | blank line contains whitespace |
| 3286 | W293 | `opt/services/billing/billing_integration.py` | 418 | blank line contains whitespace |
| 3285 | W293 | `opt/services/billing/billing_integration.py` | 414 | blank line contains whitespace |
| 3284 | W293 | `opt/services/billing/billing_integration.py` | 402 | blank line contains whitespace |
| 3283 | W293 | `opt/services/billing/billing_integration.py` | 396 | blank line contains whitespace |
| 3282 | W293 | `opt/services/billing/billing_integration.py` | 381 | blank line contains whitespace |
| 3281 | W293 | `opt/services/billing/billing_integration.py` | 372 | blank line contains whitespace |
| 3280 | W293 | `opt/services/billing/billing_integration.py` | 359 | blank line contains whitespace |
| 3279 | W291 | `opt/services/billing/billing_integration.py` | 355 | trailing whitespace |
| 3278 | W293 | `opt/services/billing/billing_integration.py` | 353 | blank line contains whitespace |
| 3277 | W291 | `opt/services/billing/billing_integration.py` | 349 | trailing whitespace |
| 3276 | W293 | `opt/services/billing/billing_integration.py` | 347 | blank line contains whitespace |
| 3275 | W293 | `opt/services/billing/billing_integration.py` | 341 | blank line contains whitespace |
| 3274 | W293 | `opt/services/billing/billing_integration.py` | 335 | blank line contains whitespace |
| 3273 | W291 | `opt/services/billing/billing_integration.py` | 331 | trailing whitespace |
| 3272 | W293 | `opt/services/billing/billing_integration.py` | 329 | blank line contains whitespace |
| 3271 | W293 | `opt/services/billing/billing_integration.py` | 298 | blank line contains whitespace |
| 3270 | W293 | `opt/services/billing/billing_integration.py` | 218 | blank line contains whitespace |
| 3269 | W293 | `opt/services/billing/billing_integration.py` | 211 | blank line contains whitespace |
| 3268 | W293 | `opt/services/billing/billing_integration.py` | 181 | blank line contains whitespace |
| 3267 | W293 | `opt/services/billing/billing_integration.py` | 174 | blank line contains whitespace |
| 3266 | W293 | `opt/services/billing/billing_integration.py` | 167 | blank line contains whitespace |
| 3265 | W293 | `opt/services/billing/billing_integration.py` | 148 | blank line contains whitespace |
| 3259 | W293 | `opt/services/backup_manager.py` | 341 | blank line contains whitespace |
| 3258 | W293 | `opt/services/backup_manager.py` | 332 | blank line contains whitespace |
| 3257 | W293 | `opt/services/backup_manager.py` | 328 | blank line contains whitespace |
| 3256 | W293 | `opt/services/backup_manager.py` | 319 | blank line contains whitespace |
| 3255 | W293 | `opt/services/backup_manager.py` | 317 | blank line contains whitespace |
| 3254 | W293 | `opt/services/backup_manager.py` | 315 | blank line contains whitespace |
| 3253 | W293 | `opt/services/backup_manager.py` | 308 | blank line contains whitespace |
| 3252 | W293 | `opt/services/backup_manager.py` | 298 | blank line contains whitespace |
| 3251 | W293 | `opt/services/backup_manager.py` | 295 | blank line contains whitespace |
| 3250 | W293 | `opt/services/backup_manager.py` | 293 | blank line contains whitespace |
| 3249 | W293 | `opt/services/backup_manager.py` | 289 | blank line contains whitespace |
| 3248 | W293 | `opt/services/backup_manager.py` | 281 | blank line contains whitespace |
| 3247 | W293 | `opt/services/backup_manager.py` | 278 | blank line contains whitespace |
| 3246 | W293 | `opt/services/backup_manager.py` | 271 | blank line contains whitespace |
| 3245 | W293 | `opt/services/backup_manager.py` | 266 | blank line contains whitespace |
| 3244 | W293 | `opt/services/backup_manager.py` | 256 | blank line contains whitespace |
| 3243 | W293 | `opt/services/backup_manager.py` | 252 | blank line contains whitespace |
| 3242 | W293 | `opt/services/backup_manager.py` | 202 | blank line contains whitespace |
| 3241 | W293 | `opt/services/backup_manager.py` | 243 | blank line contains whitespace |
| 3240 | W293 | `opt/services/backup_manager.py` | 240 | blank line contains whitespace |
| 3239 | W293 | `opt/services/backup_manager.py` | 231 | blank line contains whitespace |
| 3238 | W293 | `opt/services/backup_manager.py` | 221 | blank line contains whitespace |
| 3237 | W293 | `opt/services/backup_manager.py` | 215 | blank line contains whitespace |
| 3236 | W293 | `opt/services/backup_manager.py` | 212 | blank line contains whitespace |
| 3235 | W293 | `opt/services/backup_manager.py` | 200 | blank line contains whitespace |
| 3234 | W293 | `opt/services/backup_manager.py` | 197 | blank line contains whitespace |
| 3233 | W293 | `opt/services/backup_manager.py` | 177 | blank line contains whitespace |
| 3232 | W293 | `opt/services/backup_manager.py` | 174 | blank line contains whitespace |
| 3231 | W293 | `opt/services/backup_manager.py` | 161 | blank line contains whitespace |
| 3230 | W293 | `opt/services/backup_manager.py` | 158 | blank line contains whitespace |
| 3229 | W293 | `opt/services/backup_manager.py` | 154 | blank line contains whitespace |
| 3228 | W293 | `opt/services/backup_manager.py` | 150 | blank line contains whitespace |
| 3227 | W293 | `opt/services/backup_manager.py` | 146 | blank line contains whitespace |
| 3226 | W293 | `opt/services/backup_manager.py` | 137 | blank line contains whitespace |
| 3225 | W293 | `opt/services/backup_manager.py` | 134 | blank line contains whitespace |
| 3224 | W293 | `opt/services/backup_manager.py` | 128 | blank line contains whitespace |
| 3223 | W293 | `opt/services/backup_manager.py` | 126 | blank line contains whitespace |
| 3222 | W293 | `opt/services/backup_manager.py` | 121 | blank line contains whitespace |
| 3221 | W293 | `opt/services/backup_manager.py` | 118 | blank line contains whitespace |
| 3220 | W293 | `opt/services/backup_manager.py` | 113 | blank line contains whitespace |
| 3219 | W293 | `opt/services/backup_manager.py` | 108 | blank line contains whitespace |
| 3218 | W293 | `opt/services/backup_manager.py` | 105 | blank line contains whitespace |
| 3217 | W293 | `opt/services/backup_manager.py` | 95 | blank line contains whitespace |
| 3216 | W293 | `opt/services/backup_manager.py` | 92 | blank line contains whitespace |
| 3215 | W293 | `opt/services/backup_manager.py` | 76 | blank line contains whitespace |
| 3214 | W293 | `opt/services/backup_manager.py` | 73 | blank line contains whitespace |
| 3213 | W293 | `opt/services/backup_manager.py` | 61 | blank line contains whitespace |
| 3212 | W293 | `opt/services/backup_manager.py` | 58 | blank line contains whitespace |
| 3211 | W293 | `opt/services/backup_manager.py` | 54 | blank line contains whitespace |
| 3210 | W293 | `opt/services/backup_manager.py` | 50 | blank line contains whitespace |
| 3209 | W293 | `opt/services/backup_manager.py` | 46 | blank line contains whitespace |
| 3205 | W293 | `opt/services/backup/dedup_backup_service.py` | 802 | blank line contains whitespace |
| 3204 | W293 | `opt/services/backup/dedup_backup_service.py` | 798 | blank line contains whitespace |
| 3203 | W293 | `opt/services/backup/dedup_backup_service.py` | 793 | blank line contains whitespace |
| 3202 | W293 | `opt/services/backup/dedup_backup_service.py` | 788 | blank line contains whitespace |
| 3201 | W293 | `opt/services/backup/dedup_backup_service.py` | 783 | blank line contains whitespace |
| 3200 | W293 | `opt/services/backup/dedup_backup_service.py` | 779 | blank line contains whitespace |
| 3199 | W293 | `opt/services/backup/dedup_backup_service.py` | 772 | blank line contains whitespace |
| 3198 | W293 | `opt/services/backup/dedup_backup_service.py` | 770 | blank line contains whitespace |
| 3197 | W293 | `opt/services/backup/dedup_backup_service.py` | 757 | blank line contains whitespace |
| 3196 | W293 | `opt/services/backup/dedup_backup_service.py` | 745 | blank line contains whitespace |
| 3195 | W293 | `opt/services/backup/dedup_backup_service.py` | 739 | blank line contains whitespace |
| 3194 | W293 | `opt/services/backup/dedup_backup_service.py` | 731 | blank line contains whitespace |
| 3193 | W293 | `opt/services/backup/dedup_backup_service.py` | 726 | blank line contains whitespace |
| 3192 | W293 | `opt/services/backup/dedup_backup_service.py` | 714 | blank line contains whitespace |
| 3191 | W293 | `opt/services/backup/dedup_backup_service.py` | 710 | blank line contains whitespace |
| 3190 | W293 | `opt/services/backup/dedup_backup_service.py` | 705 | blank line contains whitespace |
| 3189 | W293 | `opt/services/backup/dedup_backup_service.py` | 700 | blank line contains whitespace |
| 3188 | W293 | `opt/services/backup/dedup_backup_service.py` | 697 | blank line contains whitespace |
| 3187 | W293 | `opt/services/backup/dedup_backup_service.py` | 690 | blank line contains whitespace |
| 3186 | W293 | `opt/services/backup/dedup_backup_service.py` | 686 | blank line contains whitespace |
| 3185 | W293 | `opt/services/backup/dedup_backup_service.py` | 679 | blank line contains whitespace |
| 3184 | W293 | `opt/services/backup/dedup_backup_service.py` | 674 | blank line contains whitespace |
| 3183 | W293 | `opt/services/backup/dedup_backup_service.py` | 671 | blank line contains whitespace |
| 3182 | W293 | `opt/services/backup/dedup_backup_service.py` | 662 | blank line contains whitespace |
| 3181 | W293 | `opt/services/backup/dedup_backup_service.py` | 650 | blank line contains whitespace |
| 3180 | W293 | `opt/services/backup/dedup_backup_service.py` | 646 | blank line contains whitespace |
| 3179 | W293 | `opt/services/backup/dedup_backup_service.py` | 639 | blank line contains whitespace |
| 3178 | W293 | `opt/services/backup/dedup_backup_service.py` | 634 | blank line contains whitespace |
| 3177 | W293 | `opt/services/backup/dedup_backup_service.py` | 631 | blank line contains whitespace |
| 3176 | W293 | `opt/services/backup/dedup_backup_service.py` | 625 | blank line contains whitespace |
| 3175 | W293 | `opt/services/backup/dedup_backup_service.py` | 622 | blank line contains whitespace |
| 3174 | W293 | `opt/services/backup/dedup_backup_service.py` | 616 | blank line contains whitespace |
| 3173 | W293 | `opt/services/backup/dedup_backup_service.py` | 613 | blank line contains whitespace |
| 3172 | W293 | `opt/services/backup/dedup_backup_service.py` | 606 | blank line contains whitespace |
| 3171 | W293 | `opt/services/backup/dedup_backup_service.py` | 600 | blank line contains whitespace |
| 3170 | W293 | `opt/services/backup/dedup_backup_service.py` | 597 | blank line contains whitespace |
| 3169 | W293 | `opt/services/backup/dedup_backup_service.py` | 594 | blank line contains whitespace |
| 3168 | W293 | `opt/services/backup/dedup_backup_service.py` | 583 | blank line contains whitespace |
| 3167 | W293 | `opt/services/backup/dedup_backup_service.py` | 577 | blank line contains whitespace |
| 3166 | W293 | `opt/services/backup/dedup_backup_service.py` | 573 | blank line contains whitespace |
| 3165 | W293 | `opt/services/backup/dedup_backup_service.py` | 567 | blank line contains whitespace |
| 3164 | W293 | `opt/services/backup/dedup_backup_service.py` | 564 | blank line contains whitespace |
| 3163 | W293 | `opt/services/backup/dedup_backup_service.py` | 561 | blank line contains whitespace |
| 3162 | W293 | `opt/services/backup/dedup_backup_service.py` | 550 | blank line contains whitespace |
| 3161 | W293 | `opt/services/backup/dedup_backup_service.py` | 543 | blank line contains whitespace |
| 3160 | W293 | `opt/services/backup/dedup_backup_service.py` | 539 | blank line contains whitespace |
| 3159 | W293 | `opt/services/backup/dedup_backup_service.py` | 535 | blank line contains whitespace |
| 3158 | W293 | `opt/services/backup/dedup_backup_service.py` | 530 | blank line contains whitespace |
| 3157 | W293 | `opt/services/backup/dedup_backup_service.py` | 511 | blank line contains whitespace |
| 3156 | W293 | `opt/services/backup/dedup_backup_service.py` | 488 | blank line contains whitespace |
| 3155 | W293 | `opt/services/backup/dedup_backup_service.py` | 479 | blank line contains whitespace |
| 3154 | W293 | `opt/services/backup/dedup_backup_service.py` | 459 | blank line contains whitespace |
| 3153 | W293 | `opt/services/backup/dedup_backup_service.py` | 449 | blank line contains whitespace |
| 3152 | W293 | `opt/services/backup/dedup_backup_service.py` | 439 | blank line contains whitespace |
| 3151 | W293 | `opt/services/backup/dedup_backup_service.py` | 432 | blank line contains whitespace |
| 3150 | W293 | `opt/services/backup/dedup_backup_service.py` | 418 | blank line contains whitespace |
| 3149 | W293 | `opt/services/backup/dedup_backup_service.py` | 416 | blank line contains whitespace |
| 3148 | W293 | `opt/services/backup/dedup_backup_service.py` | 413 | blank line contains whitespace |
| 3147 | W293 | `opt/services/backup/dedup_backup_service.py` | 409 | blank line contains whitespace |
| 3146 | W293 | `opt/services/backup/dedup_backup_service.py` | 406 | blank line contains whitespace |
| 3145 | W293 | `opt/services/backup/dedup_backup_service.py` | 403 | blank line contains whitespace |
| 3144 | W293 | `opt/services/backup/dedup_backup_service.py` | 398 | blank line contains whitespace |
| 3143 | W293 | `opt/services/backup/dedup_backup_service.py` | 395 | blank line contains whitespace |
| 3142 | W293 | `opt/services/backup/dedup_backup_service.py` | 383 | blank line contains whitespace |
| 3141 | W293 | `opt/services/backup/dedup_backup_service.py` | 377 | blank line contains whitespace |
| 3140 | W293 | `opt/services/backup/dedup_backup_service.py` | 371 | blank line contains whitespace |
| 3139 | W293 | `opt/services/backup/dedup_backup_service.py` | 368 | blank line contains whitespace |
| 3138 | W293 | `opt/services/backup/dedup_backup_service.py` | 361 | blank line contains whitespace |
| 3137 | W293 | `opt/services/backup/dedup_backup_service.py` | 356 | blank line contains whitespace |
| 3136 | W293 | `opt/services/backup/dedup_backup_service.py` | 352 | blank line contains whitespace |
| 3135 | W293 | `opt/services/backup/dedup_backup_service.py` | 335 | blank line contains whitespace |
| 3134 | W293 | `opt/services/backup/dedup_backup_service.py` | 314 | blank line contains whitespace |
| 3133 | W293 | `opt/services/backup/dedup_backup_service.py` | 309 | blank line contains whitespace |
| 3132 | W293 | `opt/services/backup/dedup_backup_service.py` | 303 | blank line contains whitespace |
| 3131 | W293 | `opt/services/backup/dedup_backup_service.py` | 293 | blank line contains whitespace |
| 3130 | W293 | `opt/services/backup/dedup_backup_service.py` | 286 | blank line contains whitespace |
| 3129 | W293 | `opt/services/backup/dedup_backup_service.py` | 284 | blank line contains whitespace |
| 3128 | W293 | `opt/services/backup/dedup_backup_service.py` | 282 | blank line contains whitespace |
| 3127 | W293 | `opt/services/backup/dedup_backup_service.py` | 276 | blank line contains whitespace |
| 3126 | W293 | `opt/services/backup/dedup_backup_service.py` | 274 | blank line contains whitespace |
| 3125 | W293 | `opt/services/backup/dedup_backup_service.py` | 260 | blank line contains whitespace |
| 3124 | W293 | `opt/services/backup/dedup_backup_service.py` | 257 | blank line contains whitespace |
| 3123 | W293 | `opt/services/backup/dedup_backup_service.py` | 251 | blank line contains whitespace |
| 3122 | W293 | `opt/services/backup/dedup_backup_service.py` | 245 | blank line contains whitespace |
| 3121 | W293 | `opt/services/backup/dedup_backup_service.py` | 234 | blank line contains whitespace |
| 3120 | W293 | `opt/services/backup/dedup_backup_service.py` | 228 | blank line contains whitespace |
| 3119 | W293 | `opt/services/backup/dedup_backup_service.py` | 226 | blank line contains whitespace |
| 3118 | W293 | `opt/services/backup/dedup_backup_service.py` | 212 | blank line contains whitespace |
| 3117 | W293 | `opt/services/backup/dedup_backup_service.py` | 206 | blank line contains whitespace |
| 3116 | W293 | `opt/services/backup/dedup_backup_service.py` | 193 | blank line contains whitespace |
| 3115 | W293 | `opt/services/backup/dedup_backup_service.py` | 189 | blank line contains whitespace |
| 3114 | W293 | `opt/services/backup/dedup_backup_service.py` | 184 | blank line contains whitespace |
| 3113 | W293 | `opt/services/backup/dedup_backup_service.py` | 178 | blank line contains whitespace |
| 3112 | W293 | `opt/services/backup/dedup_backup_service.py` | 175 | blank line contains whitespace |
| 3111 | W293 | `opt/services/backup/dedup_backup_service.py` | 170 | blank line contains whitespace |
| 3110 | W293 | `opt/services/backup/dedup_backup_service.py` | 165 | blank line contains whitespace |
| 3109 | W293 | `opt/services/backup/dedup_backup_service.py` | 160 | blank line contains whitespace |
| 3108 | W293 | `opt/services/backup/dedup_backup_service.py` | 152 | blank line contains whitespace |
| 3107 | W293 | `opt/services/backup/dedup_backup_service.py` | 148 | blank line contains whitespace |
| 3106 | W293 | `opt/services/backup/dedup_backup_service.py` | 142 | blank line contains whitespace |
| 3105 | W293 | `opt/services/backup/dedup_backup_service.py` | 136 | blank line contains whitespace |
| 3104 | W293 | `opt/services/backup/dedup_backup_service.py` | 133 | blank line contains whitespace |
| 3097 | W293 | `opt/services/backup/backup_intelligence.py` | 1297 | blank line contains whitespace |
| 3096 | W293 | `opt/services/backup/backup_intelligence.py` | 1292 | blank line contains whitespace |
| 3095 | W293 | `opt/services/backup/backup_intelligence.py` | 1282 | blank line contains whitespace |
| 3094 | W293 | `opt/services/backup/backup_intelligence.py` | 1278 | blank line contains whitespace |
| 3093 | W293 | `opt/services/backup/backup_intelligence.py` | 1273 | blank line contains whitespace |
| 3092 | W293 | `opt/services/backup/backup_intelligence.py` | 1267 | blank line contains whitespace |
| 3091 | W293 | `opt/services/backup/backup_intelligence.py` | 1264 | blank line contains whitespace |
| 3090 | W293 | `opt/services/backup/backup_intelligence.py` | 1257 | blank line contains whitespace |
| 3089 | W293 | `opt/services/backup/backup_intelligence.py` | 1254 | blank line contains whitespace |
| 3088 | W293 | `opt/services/backup/backup_intelligence.py` | 1249 | blank line contains whitespace |
| 3087 | W293 | `opt/services/backup/backup_intelligence.py` | 1241 | blank line contains whitespace |
| 3086 | W293 | `opt/services/backup/backup_intelligence.py` | 1238 | blank line contains whitespace |
| 3085 | W293 | `opt/services/backup/backup_intelligence.py` | 1227 | blank line contains whitespace |
| 3084 | W293 | `opt/services/backup/backup_intelligence.py` | 1219 | blank line contains whitespace |
| 3083 | W293 | `opt/services/backup/backup_intelligence.py` | 1213 | blank line contains whitespace |
| 3082 | W293 | `opt/services/backup/backup_intelligence.py` | 1210 | blank line contains whitespace |
| 3081 | W293 | `opt/services/backup/backup_intelligence.py` | 1202 | blank line contains whitespace |
| 3080 | W293 | `opt/services/backup/backup_intelligence.py` | 1199 | blank line contains whitespace |
| 3079 | W293 | `opt/services/backup/backup_intelligence.py` | 1190 | blank line contains whitespace |
| 3078 | W293 | `opt/services/backup/backup_intelligence.py` | 1181 | blank line contains whitespace |
| 3077 | W293 | `opt/services/backup/backup_intelligence.py` | 1171 | blank line contains whitespace |
| 3076 | W293 | `opt/services/backup/backup_intelligence.py` | 1168 | blank line contains whitespace |
| 3075 | W293 | `opt/services/backup/backup_intelligence.py` | 1164 | blank line contains whitespace |
| 3074 | W291 | `opt/services/backup/backup_intelligence.py` | 1147 | trailing whitespace |
| 3073 | W293 | `opt/services/backup/backup_intelligence.py` | 1137 | blank line contains whitespace |
| 3072 | W293 | `opt/services/backup/backup_intelligence.py` | 1132 | blank line contains whitespace |
| 3071 | W293 | `opt/services/backup/backup_intelligence.py` | 1127 | blank line contains whitespace |
| 3070 | W293 | `opt/services/backup/backup_intelligence.py` | 1122 | blank line contains whitespace |
| 3069 | W293 | `opt/services/backup/backup_intelligence.py` | 1117 | blank line contains whitespace |
| 3068 | W293 | `opt/services/backup/backup_intelligence.py` | 1114 | blank line contains whitespace |
| 3067 | W293 | `opt/services/backup/backup_intelligence.py` | 1108 | blank line contains whitespace |
| 3066 | W293 | `opt/services/backup/backup_intelligence.py` | 1105 | blank line contains whitespace |
| 3065 | W293 | `opt/services/backup/backup_intelligence.py` | 1101 | blank line contains whitespace |
| 3064 | W293 | `opt/services/backup/backup_intelligence.py` | 1098 | blank line contains whitespace |
| 3063 | W293 | `opt/services/backup/backup_intelligence.py` | 1094 | blank line contains whitespace |
| 3062 | W293 | `opt/services/backup/backup_intelligence.py` | 1085 | blank line contains whitespace |
| 3061 | W293 | `opt/services/backup/backup_intelligence.py` | 1069 | blank line contains whitespace |
| 3060 | W293 | `opt/services/backup/backup_intelligence.py` | 1066 | blank line contains whitespace |
| 3059 | W293 | `opt/services/backup/backup_intelligence.py` | 1055 | blank line contains whitespace |
| 3058 | W293 | `opt/services/backup/backup_intelligence.py` | 1047 | blank line contains whitespace |
| 3057 | W293 | `opt/services/backup/backup_intelligence.py` | 1045 | blank line contains whitespace |
| 3056 | W293 | `opt/services/backup/backup_intelligence.py` | 1040 | blank line contains whitespace |
| 3055 | W293 | `opt/services/backup/backup_intelligence.py` | 1033 | blank line contains whitespace |
| 3054 | W293 | `opt/services/backup/backup_intelligence.py` | 1029 | blank line contains whitespace |
| 3053 | W293 | `opt/services/backup/backup_intelligence.py` | 1020 | blank line contains whitespace |
| 3052 | W293 | `opt/services/backup/backup_intelligence.py` | 1011 | blank line contains whitespace |
| 3051 | W293 | `opt/services/backup/backup_intelligence.py` | 1008 | blank line contains whitespace |
| 3050 | W293 | `opt/services/backup/backup_intelligence.py` | 990 | blank line contains whitespace |
| 3049 | W293 | `opt/services/backup/backup_intelligence.py` | 986 | blank line contains whitespace |
| 3048 | W293 | `opt/services/backup/backup_intelligence.py` | 983 | blank line contains whitespace |
| 3047 | W293 | `opt/services/backup/backup_intelligence.py` | 960 | blank line contains whitespace |
| 3046 | W293 | `opt/services/backup/backup_intelligence.py` | 954 | blank line contains whitespace |
| 3045 | W293 | `opt/services/backup/backup_intelligence.py` | 947 | blank line contains whitespace |
| 3044 | W293 | `opt/services/backup/backup_intelligence.py` | 939 | blank line contains whitespace |
| 3043 | W293 | `opt/services/backup/backup_intelligence.py` | 918 | blank line contains whitespace |
| 3042 | W293 | `opt/services/backup/backup_intelligence.py` | 914 | blank line contains whitespace |
| 3041 | W293 | `opt/services/backup/backup_intelligence.py` | 909 | blank line contains whitespace |
| 3040 | W293 | `opt/services/backup/backup_intelligence.py` | 906 | blank line contains whitespace |
| 3039 | W293 | `opt/services/backup/backup_intelligence.py` | 899 | blank line contains whitespace |
| 3038 | W293 | `opt/services/backup/backup_intelligence.py` | 890 | blank line contains whitespace |
| 3037 | W293 | `opt/services/backup/backup_intelligence.py` | 879 | blank line contains whitespace |
| 3036 | W293 | `opt/services/backup/backup_intelligence.py` | 875 | blank line contains whitespace |
| 3035 | W293 | `opt/services/backup/backup_intelligence.py` | 868 | blank line contains whitespace |
| 3034 | W293 | `opt/services/backup/backup_intelligence.py` | 852 | blank line contains whitespace |
| 3033 | W293 | `opt/services/backup/backup_intelligence.py` | 848 | blank line contains whitespace |
| 3032 | W293 | `opt/services/backup/backup_intelligence.py` | 846 | blank line contains whitespace |
| 3031 | W293 | `opt/services/backup/backup_intelligence.py` | 843 | blank line contains whitespace |
| 3030 | W293 | `opt/services/backup/backup_intelligence.py` | 839 | blank line contains whitespace |
| 3029 | W293 | `opt/services/backup/backup_intelligence.py` | 824 | blank line contains whitespace |
| 3028 | W293 | `opt/services/backup/backup_intelligence.py` | 819 | blank line contains whitespace |
| 3027 | W293 | `opt/services/backup/backup_intelligence.py` | 816 | blank line contains whitespace |
| 3026 | W293 | `opt/services/backup/backup_intelligence.py` | 810 | blank line contains whitespace |
| 3025 | W293 | `opt/services/backup/backup_intelligence.py` | 807 | blank line contains whitespace |
| 3024 | W293 | `opt/services/backup/backup_intelligence.py` | 798 | blank line contains whitespace |
| 3023 | W293 | `opt/services/backup/backup_intelligence.py` | 794 | blank line contains whitespace |
| 3022 | W293 | `opt/services/backup/backup_intelligence.py` | 787 | blank line contains whitespace |
| 3021 | W293 | `opt/services/backup/backup_intelligence.py` | 780 | blank line contains whitespace |
| 3020 | W293 | `opt/services/backup/backup_intelligence.py` | 775 | blank line contains whitespace |
| 3019 | W293 | `opt/services/backup/backup_intelligence.py` | 772 | blank line contains whitespace |
| 3018 | W293 | `opt/services/backup/backup_intelligence.py` | 769 | blank line contains whitespace |
| 3017 | W293 | `opt/services/backup/backup_intelligence.py` | 760 | blank line contains whitespace |
| 3016 | W293 | `opt/services/backup/backup_intelligence.py` | 752 | blank line contains whitespace |
| 3015 | W293 | `opt/services/backup/backup_intelligence.py` | 748 | blank line contains whitespace |
| 3014 | W293 | `opt/services/backup/backup_intelligence.py` | 738 | blank line contains whitespace |
| 3013 | W293 | `opt/services/backup/backup_intelligence.py` | 734 | blank line contains whitespace |
| 3012 | W293 | `opt/services/backup/backup_intelligence.py` | 731 | blank line contains whitespace |
| 3011 | W293 | `opt/services/backup/backup_intelligence.py` | 722 | blank line contains whitespace |
| 3010 | W293 | `opt/services/backup/backup_intelligence.py` | 719 | blank line contains whitespace |
| 3009 | W293 | `opt/services/backup/backup_intelligence.py` | 714 | blank line contains whitespace |
| 3008 | W293 | `opt/services/backup/backup_intelligence.py` | 709 | blank line contains whitespace |
| 3007 | W293 | `opt/services/backup/backup_intelligence.py` | 706 | blank line contains whitespace |
| 3006 | W293 | `opt/services/backup/backup_intelligence.py` | 700 | blank line contains whitespace |
| 3005 | W293 | `opt/services/backup/backup_intelligence.py` | 693 | blank line contains whitespace |
| 3004 | W293 | `opt/services/backup/backup_intelligence.py` | 683 | blank line contains whitespace |
| 3003 | W293 | `opt/services/backup/backup_intelligence.py` | 680 | blank line contains whitespace |
| 3002 | W293 | `opt/services/backup/backup_intelligence.py` | 677 | blank line contains whitespace |
| 3001 | W293 | `opt/services/backup/backup_intelligence.py` | 669 | blank line contains whitespace |
| 3000 | W293 | `opt/services/backup/backup_intelligence.py` | 661 | blank line contains whitespace |
| 2999 | W293 | `opt/services/backup/backup_intelligence.py` | 658 | blank line contains whitespace |
| 2998 | W293 | `opt/services/backup/backup_intelligence.py` | 654 | blank line contains whitespace |
| 2997 | W293 | `opt/services/backup/backup_intelligence.py` | 651 | blank line contains whitespace |
| 2996 | W293 | `opt/services/backup/backup_intelligence.py` | 647 | blank line contains whitespace |
| 2995 | W293 | `opt/services/backup/backup_intelligence.py` | 643 | blank line contains whitespace |
| 2994 | W293 | `opt/services/backup/backup_intelligence.py` | 641 | blank line contains whitespace |
| 2993 | W293 | `opt/services/backup/backup_intelligence.py` | 638 | blank line contains whitespace |
| 2992 | W293 | `opt/services/backup/backup_intelligence.py` | 636 | blank line contains whitespace |
| 2991 | W293 | `opt/services/backup/backup_intelligence.py` | 629 | blank line contains whitespace |
| 2990 | W293 | `opt/services/backup/backup_intelligence.py` | 626 | blank line contains whitespace |
| 2989 | W293 | `opt/services/backup/backup_intelligence.py` | 619 | blank line contains whitespace |
| 2988 | W293 | `opt/services/backup/backup_intelligence.py` | 616 | blank line contains whitespace |
| 2987 | W291 | `opt/services/backup/backup_intelligence.py` | 612 | trailing whitespace |
| 2986 | W293 | `opt/services/backup/backup_intelligence.py` | 609 | blank line contains whitespace |
| 2985 | W293 | `opt/services/backup/backup_intelligence.py` | 606 | blank line contains whitespace |
| 2984 | W293 | `opt/services/backup/backup_intelligence.py` | 604 | blank line contains whitespace |
| 2983 | W293 | `opt/services/backup/backup_intelligence.py` | 598 | blank line contains whitespace |
| 2982 | W293 | `opt/services/backup/backup_intelligence.py` | 596 | blank line contains whitespace |
| 2981 | W293 | `opt/services/backup/backup_intelligence.py` | 585 | blank line contains whitespace |
| 2980 | W293 | `opt/services/backup/backup_intelligence.py` | 577 | blank line contains whitespace |
| 2979 | W293 | `opt/services/backup/backup_intelligence.py` | 575 | blank line contains whitespace |
| 2978 | W293 | `opt/services/backup/backup_intelligence.py` | 572 | blank line contains whitespace |
| 2977 | W293 | `opt/services/backup/backup_intelligence.py` | 569 | blank line contains whitespace |
| 2976 | W293 | `opt/services/backup/backup_intelligence.py` | 565 | blank line contains whitespace |
| 2975 | W293 | `opt/services/backup/backup_intelligence.py` | 563 | blank line contains whitespace |
| 2974 | W293 | `opt/services/backup/backup_intelligence.py` | 560 | blank line contains whitespace |
| 2973 | W293 | `opt/services/backup/backup_intelligence.py` | 558 | blank line contains whitespace |
| 2972 | W293 | `opt/services/backup/backup_intelligence.py` | 553 | blank line contains whitespace |
| 2971 | W293 | `opt/services/backup/backup_intelligence.py` | 551 | blank line contains whitespace |
| 2970 | W293 | `opt/services/backup/backup_intelligence.py` | 547 | blank line contains whitespace |
| 2969 | W293 | `opt/services/backup/backup_intelligence.py` | 543 | blank line contains whitespace |
| 2968 | W293 | `opt/services/backup/backup_intelligence.py` | 538 | blank line contains whitespace |
| 2967 | W293 | `opt/services/backup/backup_intelligence.py` | 535 | blank line contains whitespace |
| 2966 | W293 | `opt/services/backup/backup_intelligence.py` | 527 | blank line contains whitespace |
| 2965 | W293 | `opt/services/backup/backup_intelligence.py` | 523 | blank line contains whitespace |
| 2964 | W293 | `opt/services/backup/backup_intelligence.py` | 519 | blank line contains whitespace |
| 2963 | W293 | `opt/services/backup/backup_intelligence.py` | 513 | blank line contains whitespace |
| 2962 | W293 | `opt/services/backup/backup_intelligence.py` | 510 | blank line contains whitespace |
| 2961 | W293 | `opt/services/backup/backup_intelligence.py` | 506 | blank line contains whitespace |
| 2960 | W293 | `opt/services/backup/backup_intelligence.py` | 504 | blank line contains whitespace |
| 2959 | W293 | `opt/services/backup/backup_intelligence.py` | 499 | blank line contains whitespace |
| 2958 | W293 | `opt/services/backup/backup_intelligence.py` | 496 | blank line contains whitespace |
| 2957 | W293 | `opt/services/backup/backup_intelligence.py` | 493 | blank line contains whitespace |
| 2956 | W293 | `opt/services/backup/backup_intelligence.py` | 485 | blank line contains whitespace |
| 2955 | W293 | `opt/services/backup/backup_intelligence.py` | 474 | blank line contains whitespace |
| 2954 | W293 | `opt/services/backup/backup_intelligence.py` | 471 | blank line contains whitespace |
| 2953 | W291 | `opt/services/backup/backup_intelligence.py` | 468 | trailing whitespace |
| 2952 | W293 | `opt/services/backup/backup_intelligence.py` | 462 | blank line contains whitespace |
| 2951 | W293 | `opt/services/backup/backup_intelligence.py` | 458 | blank line contains whitespace |
| 2950 | W293 | `opt/services/backup/backup_intelligence.py` | 448 | blank line contains whitespace |
| 2949 | W293 | `opt/services/backup/backup_intelligence.py` | 441 | blank line contains whitespace |
| 2948 | W293 | `opt/services/backup/backup_intelligence.py` | 431 | blank line contains whitespace |
| 2947 | W293 | `opt/services/backup/backup_intelligence.py` | 417 | blank line contains whitespace |
| 2946 | W293 | `opt/services/backup/backup_intelligence.py` | 413 | blank line contains whitespace |
| 2945 | W293 | `opt/services/backup/backup_intelligence.py` | 411 | blank line contains whitespace |
| 2944 | W293 | `opt/services/backup/backup_intelligence.py` | 403 | blank line contains whitespace |
| 2943 | W293 | `opt/services/backup/backup_intelligence.py` | 393 | blank line contains whitespace |
| 2942 | W293 | `opt/services/backup/backup_intelligence.py` | 389 | blank line contains whitespace |
| 2941 | W293 | `opt/services/backup/backup_intelligence.py` | 385 | blank line contains whitespace |
| 2940 | W293 | `opt/services/backup/backup_intelligence.py` | 382 | blank line contains whitespace |
| 2939 | W293 | `opt/services/backup/backup_intelligence.py` | 380 | blank line contains whitespace |
| 2938 | W293 | `opt/services/backup/backup_intelligence.py` | 377 | blank line contains whitespace |
| 2937 | W293 | `opt/services/backup/backup_intelligence.py` | 373 | blank line contains whitespace |
| 2936 | W293 | `opt/services/backup/backup_intelligence.py` | 369 | blank line contains whitespace |
| 2935 | W293 | `opt/services/backup/backup_intelligence.py` | 365 | blank line contains whitespace |
| 2934 | W293 | `opt/services/backup/backup_intelligence.py` | 361 | blank line contains whitespace |
| 2933 | W293 | `opt/services/backup/backup_intelligence.py` | 357 | blank line contains whitespace |
| 2932 | W293 | `opt/services/backup/backup_intelligence.py` | 355 | blank line contains whitespace |
| 2931 | W293 | `opt/services/backup/backup_intelligence.py` | 351 | blank line contains whitespace |
| 2930 | W293 | `opt/services/backup/backup_intelligence.py` | 342 | blank line contains whitespace |
| 2929 | W293 | `opt/services/backup/backup_intelligence.py` | 334 | blank line contains whitespace |
| 2928 | W293 | `opt/services/backup/backup_intelligence.py` | 332 | blank line contains whitespace |
| 2927 | W293 | `opt/services/backup/backup_intelligence.py` | 330 | blank line contains whitespace |
| 2926 | W293 | `opt/services/backup/backup_intelligence.py` | 327 | blank line contains whitespace |
| 2925 | W293 | `opt/services/backup/backup_intelligence.py` | 323 | blank line contains whitespace |
| 2924 | W293 | `opt/services/backup/backup_intelligence.py` | 318 | blank line contains whitespace |
| 2923 | W293 | `opt/services/backup/backup_intelligence.py` | 316 | blank line contains whitespace |
| 2922 | W293 | `opt/services/backup/backup_intelligence.py` | 311 | blank line contains whitespace |
| 2921 | W293 | `opt/services/backup/backup_intelligence.py` | 304 | blank line contains whitespace |
| 2920 | W293 | `opt/services/backup/backup_intelligence.py` | 298 | blank line contains whitespace |
| 2919 | W293 | `opt/services/backup/backup_intelligence.py` | 292 | blank line contains whitespace |
| 2918 | W293 | `opt/services/backup/backup_intelligence.py` | 290 | blank line contains whitespace |
| 2917 | W291 | `opt/services/backup/backup_intelligence.py` | 287 | trailing whitespace |
| 2916 | W293 | `opt/services/backup/backup_intelligence.py` | 283 | blank line contains whitespace |
| 2915 | W293 | `opt/services/backup/backup_intelligence.py` | 278 | blank line contains whitespace |
| 2914 | W293 | `opt/services/backup/backup_intelligence.py` | 273 | blank line contains whitespace |
| 2913 | W293 | `opt/services/backup/backup_intelligence.py` | 268 | blank line contains whitespace |
| 2912 | W293 | `opt/services/backup/backup_intelligence.py` | 264 | blank line contains whitespace |
| 2911 | W293 | `opt/services/backup/backup_intelligence.py` | 261 | blank line contains whitespace |
| 2910 | W293 | `opt/services/backup/backup_intelligence.py` | 259 | blank line contains whitespace |
| 2909 | W293 | `opt/services/backup/backup_intelligence.py` | 253 | blank line contains whitespace |
| 2908 | W293 | `opt/services/backup/backup_intelligence.py` | 246 | blank line contains whitespace |
| 2907 | W293 | `opt/services/backup/backup_intelligence.py` | 242 | blank line contains whitespace |
| 2906 | W293 | `opt/services/backup/backup_intelligence.py` | 237 | blank line contains whitespace |
| 2905 | W293 | `opt/services/backup/backup_intelligence.py` | 234 | blank line contains whitespace |
| 2904 | W293 | `opt/services/backup/backup_intelligence.py` | 231 | blank line contains whitespace |
| 2903 | W293 | `opt/services/backup/backup_intelligence.py` | 229 | blank line contains whitespace |
| 2902 | W293 | `opt/services/backup/backup_intelligence.py` | 226 | blank line contains whitespace |
| 2901 | W293 | `opt/services/backup/backup_intelligence.py` | 216 | blank line contains whitespace |
| 2900 | W293 | `opt/services/backup/backup_intelligence.py` | 207 | blank line contains whitespace |
| 2899 | W293 | `opt/services/backup/backup_intelligence.py` | 201 | blank line contains whitespace |
| 2895 | W293 | `opt/services/auth/ldap_backend.py` | 503 | blank line contains whitespace |
| 2894 | W293 | `opt/services/auth/ldap_backend.py` | 494 | blank line contains whitespace |
| 2893 | W293 | `opt/services/auth/ldap_backend.py` | 492 | blank line contains whitespace |
| 2892 | W293 | `opt/services/auth/ldap_backend.py` | 483 | blank line contains whitespace |
| 2891 | W293 | `opt/services/auth/ldap_backend.py` | 475 | blank line contains whitespace |
| 2890 | W293 | `opt/services/auth/ldap_backend.py` | 472 | blank line contains whitespace |
| 2889 | W293 | `opt/services/auth/ldap_backend.py` | 464 | blank line contains whitespace |
| 2888 | W293 | `opt/services/auth/ldap_backend.py` | 460 | blank line contains whitespace |
| 2887 | W293 | `opt/services/auth/ldap_backend.py` | 457 | blank line contains whitespace |
| 2886 | W293 | `opt/services/auth/ldap_backend.py` | 447 | blank line contains whitespace |
| 2885 | W293 | `opt/services/auth/ldap_backend.py` | 442 | blank line contains whitespace |
| 2884 | W293 | `opt/services/auth/ldap_backend.py` | 437 | blank line contains whitespace |
| 2883 | W293 | `opt/services/auth/ldap_backend.py` | 431 | blank line contains whitespace |
| 2882 | W293 | `opt/services/auth/ldap_backend.py` | 428 | blank line contains whitespace |
| 2881 | W293 | `opt/services/auth/ldap_backend.py` | 423 | blank line contains whitespace |
| 2880 | W293 | `opt/services/auth/ldap_backend.py` | 420 | blank line contains whitespace |
| 2879 | W293 | `opt/services/auth/ldap_backend.py` | 415 | blank line contains whitespace |
| 2878 | W293 | `opt/services/auth/ldap_backend.py` | 413 | blank line contains whitespace |
| 2877 | W293 | `opt/services/auth/ldap_backend.py` | 410 | blank line contains whitespace |
| 2875 | W293 | `opt/services/auth/ldap_backend.py` | 408 | blank line contains whitespace |
| 2874 | W293 | `opt/services/auth/ldap_backend.py` | 404 | blank line contains whitespace |
| 2873 | W293 | `opt/services/auth/ldap_backend.py` | 399 | blank line contains whitespace |
| 2872 | W293 | `opt/services/auth/ldap_backend.py` | 397 | blank line contains whitespace |
| 2871 | W293 | `opt/services/auth/ldap_backend.py` | 387 | blank line contains whitespace |
| 2870 | W293 | `opt/services/auth/ldap_backend.py` | 380 | blank line contains whitespace |
| 2869 | W293 | `opt/services/auth/ldap_backend.py` | 374 | blank line contains whitespace |
| 2868 | W293 | `opt/services/auth/ldap_backend.py` | 371 | blank line contains whitespace |
| 2867 | W293 | `opt/services/auth/ldap_backend.py` | 367 | blank line contains whitespace |
| 2866 | W293 | `opt/services/auth/ldap_backend.py` | 354 | blank line contains whitespace |
| 2865 | W293 | `opt/services/auth/ldap_backend.py` | 348 | blank line contains whitespace |
| 2864 | W293 | `opt/services/auth/ldap_backend.py` | 345 | blank line contains whitespace |
| 2863 | W293 | `opt/services/auth/ldap_backend.py` | 342 | blank line contains whitespace |
| 2862 | W293 | `opt/services/auth/ldap_backend.py` | 336 | blank line contains whitespace |
| 2861 | W293 | `opt/services/auth/ldap_backend.py` | 332 | blank line contains whitespace |
| 2860 | W293 | `opt/services/auth/ldap_backend.py` | 329 | blank line contains whitespace |
| 2859 | W293 | `opt/services/auth/ldap_backend.py` | 326 | blank line contains whitespace |
| 2858 | W293 | `opt/services/auth/ldap_backend.py` | 323 | blank line contains whitespace |
| 2857 | W291 | `opt/services/auth/ldap_backend.py` | 321 | trailing whitespace |
| 2856 | W293 | `opt/services/auth/ldap_backend.py` | 320 | blank line contains whitespace |
| 2855 | W293 | `opt/services/auth/ldap_backend.py` | 310 | blank line contains whitespace |
| 2854 | W293 | `opt/services/auth/ldap_backend.py` | 305 | blank line contains whitespace |
| 2853 | W293 | `opt/services/auth/ldap_backend.py` | 301 | blank line contains whitespace |
| 2852 | W293 | `opt/services/auth/ldap_backend.py` | 292 | blank line contains whitespace |
| 2851 | W293 | `opt/services/auth/ldap_backend.py` | 288 | blank line contains whitespace |
| 2850 | W293 | `opt/services/auth/ldap_backend.py` | 285 | blank line contains whitespace |
| 2849 | W293 | `opt/services/auth/ldap_backend.py` | 282 | blank line contains whitespace |
| 2848 | W293 | `opt/services/auth/ldap_backend.py` | 279 | blank line contains whitespace |
| 2847 | W293 | `opt/services/auth/ldap_backend.py` | 276 | blank line contains whitespace |
| 2846 | W293 | `opt/services/auth/ldap_backend.py` | 274 | blank line contains whitespace |
| 2845 | W293 | `opt/services/auth/ldap_backend.py` | 271 | blank line contains whitespace |
| 2844 | W293 | `opt/services/auth/ldap_backend.py` | 262 | blank line contains whitespace |
| 2843 | W293 | `opt/services/auth/ldap_backend.py` | 257 | blank line contains whitespace |
| 2842 | W293 | `opt/services/auth/ldap_backend.py` | 248 | blank line contains whitespace |
| 2841 | W293 | `opt/services/auth/ldap_backend.py` | 244 | blank line contains whitespace |
| 2840 | W293 | `opt/services/auth/ldap_backend.py` | 240 | blank line contains whitespace |
| 2839 | W293 | `opt/services/auth/ldap_backend.py` | 237 | blank line contains whitespace |
| 2838 | W293 | `opt/services/auth/ldap_backend.py` | 234 | blank line contains whitespace |
| 2837 | W293 | `opt/services/auth/ldap_backend.py` | 229 | blank line contains whitespace |
| 2836 | W293 | `opt/services/auth/ldap_backend.py` | 219 | blank line contains whitespace |
| 2835 | W293 | `opt/services/auth/ldap_backend.py` | 215 | blank line contains whitespace |
| 2834 | W293 | `opt/services/auth/ldap_backend.py` | 211 | blank line contains whitespace |
| 2833 | W293 | `opt/services/auth/ldap_backend.py` | 207 | blank line contains whitespace |
| 2832 | W293 | `opt/services/auth/ldap_backend.py` | 201 | blank line contains whitespace |
| 2831 | W293 | `opt/services/auth/ldap_backend.py` | 192 | blank line contains whitespace |
| 2830 | W293 | `opt/services/auth/ldap_backend.py` | 187 | blank line contains whitespace |
| 2829 | W293 | `opt/services/auth/ldap_backend.py` | 182 | blank line contains whitespace |
| 2828 | W293 | `opt/services/auth/ldap_backend.py` | 168 | blank line contains whitespace |
| 2827 | W293 | `opt/services/auth/ldap_backend.py` | 163 | blank line contains whitespace |
| 2826 | W293 | `opt/services/auth/ldap_backend.py` | 155 | blank line contains whitespace |
| 2825 | W293 | `opt/services/auth/ldap_backend.py` | 151 | blank line contains whitespace |
| 2824 | W293 | `opt/services/auth/ldap_backend.py` | 147 | blank line contains whitespace |
| 2823 | W293 | `opt/services/auth/ldap_backend.py` | 144 | blank line contains whitespace |
| 2822 | W293 | `opt/services/auth/ldap_backend.py` | 141 | blank line contains whitespace |
| 2821 | W293 | `opt/services/auth/ldap_backend.py` | 138 | blank line contains whitespace |
| 2820 | W293 | `opt/services/auth/ldap_backend.py` | 134 | blank line contains whitespace |
| 2819 | W293 | `opt/services/auth/ldap_backend.py` | 131 | blank line contains whitespace |
| 2818 | W293 | `opt/services/auth/ldap_backend.py` | 128 | blank line contains whitespace |
| 2817 | W293 | `opt/services/auth/ldap_backend.py` | 121 | blank line contains whitespace |
| 2816 | W293 | `opt/services/auth/ldap_backend.py` | 114 | blank line contains whitespace |
| 2815 | W293 | `opt/services/auth/ldap_backend.py` | 98 | blank line contains whitespace |
| 2814 | W293 | `opt/services/auth/ldap_backend.py` | 94 | blank line contains whitespace |
| 2813 | W293 | `opt/services/auth/ldap_backend.py` | 68 | blank line contains whitespace |
| 2811 | W293 | `opt/services/audit_encryption.py` | 783 | blank line contains whitespace |
| 2810 | W293 | `opt/services/audit_encryption.py` | 779 | blank line contains whitespace |
| 2809 | W293 | `opt/services/audit_encryption.py` | 769 | blank line contains whitespace |
| 2808 | W293 | `opt/services/audit_encryption.py` | 766 | blank line contains whitespace |
| 2807 | W293 | `opt/services/audit_encryption.py` | 761 | blank line contains whitespace |
| 2806 | W293 | `opt/services/audit_encryption.py` | 758 | blank line contains whitespace |
| 2805 | W293 | `opt/services/audit_encryption.py` | 753 | blank line contains whitespace |
| 2804 | W293 | `opt/services/audit_encryption.py` | 750 | blank line contains whitespace |
| 2803 | W293 | `opt/services/audit_encryption.py` | 745 | blank line contains whitespace |
| 2802 | W293 | `opt/services/audit_encryption.py` | 740 | blank line contains whitespace |
| 2801 | W293 | `opt/services/audit_encryption.py` | 725 | blank line contains whitespace |
| 2800 | W293 | `opt/services/audit_encryption.py` | 708 | blank line contains whitespace |
| 2799 | W293 | `opt/services/audit_encryption.py` | 693 | blank line contains whitespace |
| 2798 | W293 | `opt/services/audit_encryption.py` | 690 | blank line contains whitespace |
| 2797 | W293 | `opt/services/audit_encryption.py` | 687 | blank line contains whitespace |
| 2796 | W293 | `opt/services/audit_encryption.py` | 677 | blank line contains whitespace |
| 2795 | W293 | `opt/services/audit_encryption.py` | 671 | blank line contains whitespace |
| 2794 | W293 | `opt/services/audit_encryption.py` | 666 | blank line contains whitespace |
| 2793 | W293 | `opt/services/audit_encryption.py` | 662 | blank line contains whitespace |
| 2792 | W293 | `opt/services/audit_encryption.py` | 637 | blank line contains whitespace |
| 2791 | W293 | `opt/services/audit_encryption.py` | 630 | blank line contains whitespace |
| 2790 | W293 | `opt/services/audit_encryption.py` | 625 | blank line contains whitespace |
| 2789 | W293 | `opt/services/audit_encryption.py` | 620 | blank line contains whitespace |
| 2788 | W293 | `opt/services/audit_encryption.py` | 611 | blank line contains whitespace |
| 2787 | W293 | `opt/services/audit_encryption.py` | 609 | blank line contains whitespace |
| 2786 | W293 | `opt/services/audit_encryption.py` | 605 | blank line contains whitespace |
| 2785 | W293 | `opt/services/audit_encryption.py` | 597 | blank line contains whitespace |
| 2784 | W293 | `opt/services/audit_encryption.py` | 592 | blank line contains whitespace |
| 2783 | W293 | `opt/services/audit_encryption.py` | 586 | blank line contains whitespace |
| 2782 | W293 | `opt/services/audit_encryption.py` | 576 | blank line contains whitespace |
| 2781 | W293 | `opt/services/audit_encryption.py` | 569 | blank line contains whitespace |
| 2780 | W293 | `opt/services/audit_encryption.py` | 566 | blank line contains whitespace |
| 2779 | W293 | `opt/services/audit_encryption.py` | 562 | blank line contains whitespace |
| 2778 | W293 | `opt/services/audit_encryption.py` | 560 | blank line contains whitespace |
| 2777 | W293 | `opt/services/audit_encryption.py` | 551 | blank line contains whitespace |
| 2776 | W293 | `opt/services/audit_encryption.py` | 542 | blank line contains whitespace |
| 2775 | W293 | `opt/services/audit_encryption.py` | 531 | blank line contains whitespace |
| 2774 | W293 | `opt/services/audit_encryption.py` | 526 | blank line contains whitespace |
| 2773 | W293 | `opt/services/audit_encryption.py` | 523 | blank line contains whitespace |
| 2772 | W293 | `opt/services/audit_encryption.py` | 519 | blank line contains whitespace |
| 2771 | W293 | `opt/services/audit_encryption.py` | 517 | blank line contains whitespace |
| 2770 | W293 | `opt/services/audit_encryption.py` | 510 | blank line contains whitespace |
| 2769 | W293 | `opt/services/audit_encryption.py` | 505 | blank line contains whitespace |
| 2768 | W293 | `opt/services/audit_encryption.py` | 500 | blank line contains whitespace |
| 2767 | W293 | `opt/services/audit_encryption.py` | 491 | blank line contains whitespace |
| 2766 | W293 | `opt/services/audit_encryption.py` | 474 | blank line contains whitespace |
| 2765 | W293 | `opt/services/audit_encryption.py` | 468 | blank line contains whitespace |
| 2764 | W293 | `opt/services/audit_encryption.py` | 464 | blank line contains whitespace |
| 2763 | W293 | `opt/services/audit_encryption.py` | 462 | blank line contains whitespace |
| 2762 | W293 | `opt/services/audit_encryption.py` | 460 | blank line contains whitespace |
| 2761 | W293 | `opt/services/audit_encryption.py` | 457 | blank line contains whitespace |
| 2760 | W293 | `opt/services/audit_encryption.py` | 442 | blank line contains whitespace |
| 2759 | W293 | `opt/services/audit_encryption.py` | 432 | blank line contains whitespace |
| 2758 | W293 | `opt/services/audit_encryption.py` | 421 | blank line contains whitespace |
| 2757 | W293 | `opt/services/audit_encryption.py` | 416 | blank line contains whitespace |
| 2756 | W293 | `opt/services/audit_encryption.py` | 407 | blank line contains whitespace |
| 2755 | W293 | `opt/services/audit_encryption.py` | 402 | blank line contains whitespace |
| 2754 | W293 | `opt/services/audit_encryption.py` | 399 | blank line contains whitespace |
| 2753 | W293 | `opt/services/audit_encryption.py` | 393 | blank line contains whitespace |
| 2752 | W293 | `opt/services/audit_encryption.py` | 382 | blank line contains whitespace |
| 2751 | W293 | `opt/services/audit_encryption.py` | 367 | blank line contains whitespace |
| 2750 | W293 | `opt/services/audit_encryption.py` | 365 | blank line contains whitespace |
| 2749 | W293 | `opt/services/audit_encryption.py` | 357 | blank line contains whitespace |
| 2748 | W293 | `opt/services/audit_encryption.py` | 349 | blank line contains whitespace |
| 2747 | W293 | `opt/services/audit_encryption.py` | 342 | blank line contains whitespace |
| 2746 | W293 | `opt/services/audit_encryption.py` | 329 | blank line contains whitespace |
| 2745 | W293 | `opt/services/audit_encryption.py` | 325 | blank line contains whitespace |
| 2744 | W293 | `opt/services/audit_encryption.py` | 322 | blank line contains whitespace |
| 2743 | W293 | `opt/services/audit_encryption.py` | 317 | blank line contains whitespace |
| 2742 | W293 | `opt/services/audit_encryption.py` | 312 | blank line contains whitespace |
| 2741 | W293 | `opt/services/audit_encryption.py` | 308 | blank line contains whitespace |
| 2740 | W293 | `opt/services/audit_encryption.py` | 305 | blank line contains whitespace |
| 2739 | W293 | `opt/services/audit_encryption.py` | 301 | blank line contains whitespace |
| 2738 | W293 | `opt/services/audit_encryption.py` | 299 | blank line contains whitespace |
| 2737 | W293 | `opt/services/audit_encryption.py` | 296 | blank line contains whitespace |
| 2736 | W293 | `opt/services/audit_encryption.py` | 294 | blank line contains whitespace |
| 2735 | W293 | `opt/services/audit_encryption.py` | 290 | blank line contains whitespace |
| 2734 | W293 | `opt/services/audit_encryption.py` | 281 | blank line contains whitespace |
| 2733 | W293 | `opt/services/audit_encryption.py` | 277 | blank line contains whitespace |
| 2732 | W293 | `opt/services/audit_encryption.py` | 275 | blank line contains whitespace |
| 2731 | W293 | `opt/services/audit_encryption.py` | 272 | blank line contains whitespace |
| 2730 | W293 | `opt/services/audit_encryption.py` | 268 | blank line contains whitespace |
| 2729 | W293 | `opt/services/audit_encryption.py` | 263 | blank line contains whitespace |
| 2728 | W293 | `opt/services/audit_encryption.py` | 260 | blank line contains whitespace |
| 2727 | W293 | `opt/services/audit_encryption.py` | 253 | blank line contains whitespace |
| 2726 | W293 | `opt/services/audit_encryption.py` | 250 | blank line contains whitespace |
| 2725 | W293 | `opt/services/audit_encryption.py` | 246 | blank line contains whitespace |
| 2724 | W293 | `opt/services/audit_encryption.py` | 241 | blank line contains whitespace |
| 2723 | W293 | `opt/services/audit_encryption.py` | 238 | blank line contains whitespace |
| 2722 | W293 | `opt/services/audit_encryption.py` | 236 | blank line contains whitespace |
| 2721 | W293 | `opt/services/audit_encryption.py` | 229 | blank line contains whitespace |
| 2720 | W293 | `opt/services/audit_encryption.py` | 225 | blank line contains whitespace |
| 2719 | W293 | `opt/services/audit_encryption.py` | 221 | blank line contains whitespace |
| 2718 | W293 | `opt/services/audit_encryption.py` | 218 | blank line contains whitespace |
| 2717 | W293 | `opt/services/audit_encryption.py` | 214 | blank line contains whitespace |
| 2716 | W293 | `opt/services/audit_encryption.py` | 205 | blank line contains whitespace |
| 2715 | W293 | `opt/services/audit_encryption.py` | 201 | blank line contains whitespace |
| 2714 | W293 | `opt/services/audit_encryption.py` | 187 | blank line contains whitespace |
| 2713 | W293 | `opt/services/audit_encryption.py` | 185 | blank line contains whitespace |
| 2712 | W293 | `opt/services/audit_encryption.py` | 179 | blank line contains whitespace |
| 2711 | W293 | `opt/services/audit_encryption.py` | 171 | blank line contains whitespace |
| 2710 | W293 | `opt/services/audit_encryption.py` | 163 | blank line contains whitespace |
| 2709 | W293 | `opt/services/audit_encryption.py` | 156 | blank line contains whitespace |
| 2708 | W293 | `opt/services/audit_encryption.py` | 152 | blank line contains whitespace |
| 2707 | W293 | `opt/services/audit_encryption.py` | 140 | blank line contains whitespace |
| 2706 | W293 | `opt/services/audit_encryption.py` | 136 | blank line contains whitespace |
| 2705 | W293 | `opt/services/audit_encryption.py` | 131 | blank line contains whitespace |
| 2704 | W293 | `opt/services/audit_encryption.py` | 124 | blank line contains whitespace |
| 2703 | W293 | `opt/services/audit_encryption.py` | 107 | blank line contains whitespace |
| 2702 | W293 | `opt/services/audit_encryption.py` | 96 | blank line contains whitespace |
| 2701 | W293 | `opt/services/audit_encryption.py` | 89 | blank line contains whitespace |
| 2700 | W293 | `opt/services/audit_encryption.py` | 75 | blank line contains whitespace |
| 2699 | W293 | `opt/services/audit_encryption.py` | 72 | blank line contains whitespace |
| 2698 | W293 | `opt/services/audit_encryption.py` | 64 | blank line contains whitespace |
| 2695 | W293 | `opt/services/api_key_rotation.py` | 776 | blank line contains whitespace |
| 2694 | W293 | `opt/services/api_key_rotation.py` | 772 | blank line contains whitespace |
| 2693 | W293 | `opt/services/api_key_rotation.py` | 768 | blank line contains whitespace |
| 2692 | W293 | `opt/services/api_key_rotation.py` | 762 | blank line contains whitespace |
| 2691 | W293 | `opt/services/api_key_rotation.py` | 758 | blank line contains whitespace |
| 2690 | W293 | `opt/services/api_key_rotation.py` | 755 | blank line contains whitespace |
| 2689 | W293 | `opt/services/api_key_rotation.py` | 748 | blank line contains whitespace |
| 2688 | W293 | `opt/services/api_key_rotation.py` | 745 | blank line contains whitespace |
| 2687 | W293 | `opt/services/api_key_rotation.py` | 743 | blank line contains whitespace |
| 2685 | W293 | `opt/services/api_key_rotation.py` | 718 | blank line contains whitespace |
| 2684 | W293 | `opt/services/api_key_rotation.py` | 713 | blank line contains whitespace |
| 2683 | W293 | `opt/services/api_key_rotation.py` | 709 | blank line contains whitespace |
| 2682 | W293 | `opt/services/api_key_rotation.py` | 707 | blank line contains whitespace |
| 2681 | W293 | `opt/services/api_key_rotation.py` | 704 | blank line contains whitespace |
| 2680 | W293 | `opt/services/api_key_rotation.py` | 696 | blank line contains whitespace |
| 2679 | W293 | `opt/services/api_key_rotation.py` | 691 | blank line contains whitespace |
| 2678 | W293 | `opt/services/api_key_rotation.py` | 687 | blank line contains whitespace |
| 2677 | W293 | `opt/services/api_key_rotation.py` | 683 | blank line contains whitespace |
| 2676 | W293 | `opt/services/api_key_rotation.py` | 677 | blank line contains whitespace |
| 2675 | W293 | `opt/services/api_key_rotation.py` | 668 | blank line contains whitespace |
| 2674 | W293 | `opt/services/api_key_rotation.py` | 663 | blank line contains whitespace |
| 2673 | W293 | `opt/services/api_key_rotation.py` | 659 | blank line contains whitespace |
| 2672 | W293 | `opt/services/api_key_rotation.py` | 643 | blank line contains whitespace |
| 2671 | W293 | `opt/services/api_key_rotation.py` | 636 | blank line contains whitespace |
| 2670 | W293 | `opt/services/api_key_rotation.py` | 632 | blank line contains whitespace |
| 2669 | W293 | `opt/services/api_key_rotation.py` | 623 | blank line contains whitespace |
| 2668 | W293 | `opt/services/api_key_rotation.py` | 621 | blank line contains whitespace |
| 2667 | W293 | `opt/services/api_key_rotation.py` | 615 | blank line contains whitespace |
| 2666 | W293 | `opt/services/api_key_rotation.py` | 605 | blank line contains whitespace |
| 2665 | W293 | `opt/services/api_key_rotation.py` | 596 | blank line contains whitespace |
| 2664 | W293 | `opt/services/api_key_rotation.py` | 586 | blank line contains whitespace |
| 2663 | W293 | `opt/services/api_key_rotation.py` | 584 | blank line contains whitespace |
| 2662 | W293 | `opt/services/api_key_rotation.py` | 578 | blank line contains whitespace |
| 2661 | W293 | `opt/services/api_key_rotation.py` | 565 | blank line contains whitespace |
| 2660 | W293 | `opt/services/api_key_rotation.py` | 554 | blank line contains whitespace |
| 2659 | W293 | `opt/services/api_key_rotation.py` | 551 | blank line contains whitespace |
| 2658 | W293 | `opt/services/api_key_rotation.py` | 546 | blank line contains whitespace |
| 2657 | W293 | `opt/services/api_key_rotation.py` | 542 | blank line contains whitespace |
| 2656 | W293 | `opt/services/api_key_rotation.py` | 540 | blank line contains whitespace |
| 2655 | W293 | `opt/services/api_key_rotation.py` | 534 | blank line contains whitespace |
| 2654 | W293 | `opt/services/api_key_rotation.py` | 529 | blank line contains whitespace |
| 2653 | W293 | `opt/services/api_key_rotation.py` | 521 | blank line contains whitespace |
| 2652 | W293 | `opt/services/api_key_rotation.py` | 519 | blank line contains whitespace |
| 2651 | W293 | `opt/services/api_key_rotation.py` | 512 | blank line contains whitespace |
| 2650 | W293 | `opt/services/api_key_rotation.py` | 509 | blank line contains whitespace |
| 2649 | W293 | `opt/services/api_key_rotation.py` | 507 | blank line contains whitespace |
| 2648 | W293 | `opt/services/api_key_rotation.py` | 503 | blank line contains whitespace |
| 2647 | W293 | `opt/services/api_key_rotation.py` | 499 | blank line contains whitespace |
| 2646 | W293 | `opt/services/api_key_rotation.py` | 497 | blank line contains whitespace |
| 2645 | W293 | `opt/services/api_key_rotation.py` | 493 | blank line contains whitespace |
| 2644 | W293 | `opt/services/api_key_rotation.py` | 482 | blank line contains whitespace |
| 2643 | W293 | `opt/services/api_key_rotation.py` | 478 | blank line contains whitespace |
| 2642 | W293 | `opt/services/api_key_rotation.py` | 471 | blank line contains whitespace |
| 2641 | W293 | `opt/services/api_key_rotation.py` | 466 | blank line contains whitespace |
| 2640 | W293 | `opt/services/api_key_rotation.py` | 457 | blank line contains whitespace |
| 2639 | W293 | `opt/services/api_key_rotation.py` | 455 | blank line contains whitespace |
| 2638 | W293 | `opt/services/api_key_rotation.py` | 450 | blank line contains whitespace |
| 2637 | W293 | `opt/services/api_key_rotation.py` | 442 | blank line contains whitespace |
| 2636 | W293 | `opt/services/api_key_rotation.py` | 435 | blank line contains whitespace |
| 2635 | W293 | `opt/services/api_key_rotation.py` | 423 | blank line contains whitespace |
| 2634 | W293 | `opt/services/api_key_rotation.py` | 419 | blank line contains whitespace |
| 2633 | W293 | `opt/services/api_key_rotation.py` | 415 | blank line contains whitespace |
| 2632 | W293 | `opt/services/api_key_rotation.py` | 408 | blank line contains whitespace |
| 2631 | W293 | `opt/services/api_key_rotation.py` | 404 | blank line contains whitespace |
| 2630 | W293 | `opt/services/api_key_rotation.py` | 401 | blank line contains whitespace |
| 2629 | W293 | `opt/services/api_key_rotation.py` | 399 | blank line contains whitespace |
| 2628 | W293 | `opt/services/api_key_rotation.py` | 395 | blank line contains whitespace |
| 2627 | W293 | `opt/services/api_key_rotation.py` | 390 | blank line contains whitespace |
| 2626 | W293 | `opt/services/api_key_rotation.py` | 385 | blank line contains whitespace |
| 2625 | W293 | `opt/services/api_key_rotation.py` | 376 | blank line contains whitespace |
| 2624 | W293 | `opt/services/api_key_rotation.py` | 374 | blank line contains whitespace |
| 2623 | W293 | `opt/services/api_key_rotation.py` | 372 | blank line contains whitespace |
| 2622 | W293 | `opt/services/api_key_rotation.py` | 365 | blank line contains whitespace |
| 2621 | W293 | `opt/services/api_key_rotation.py` | 361 | blank line contains whitespace |
| 2620 | W293 | `opt/services/api_key_rotation.py` | 351 | blank line contains whitespace |
| 2619 | W293 | `opt/services/api_key_rotation.py` | 349 | blank line contains whitespace |
| 2618 | W293 | `opt/services/api_key_rotation.py` | 344 | blank line contains whitespace |
| 2617 | W293 | `opt/services/api_key_rotation.py` | 339 | blank line contains whitespace |
| 2616 | W293 | `opt/services/api_key_rotation.py` | 334 | blank line contains whitespace |
| 2615 | W293 | `opt/services/api_key_rotation.py` | 327 | blank line contains whitespace |
| 2614 | W293 | `opt/services/api_key_rotation.py` | 316 | blank line contains whitespace |
| 2613 | W293 | `opt/services/api_key_rotation.py` | 312 | blank line contains whitespace |
| 2612 | W293 | `opt/services/api_key_rotation.py` | 310 | blank line contains whitespace |
| 2611 | W293 | `opt/services/api_key_rotation.py` | 307 | blank line contains whitespace |
| 2610 | W293 | `opt/services/api_key_rotation.py` | 304 | blank line contains whitespace |
| 2609 | W293 | `opt/services/api_key_rotation.py` | 299 | blank line contains whitespace |
| 2608 | W293 | `opt/services/api_key_rotation.py` | 292 | blank line contains whitespace |
| 2607 | W293 | `opt/services/api_key_rotation.py` | 284 | blank line contains whitespace |
| 2606 | W293 | `opt/services/api_key_rotation.py` | 276 | blank line contains whitespace |
| 2605 | W293 | `opt/services/api_key_rotation.py` | 265 | blank line contains whitespace |
| 2604 | W293 | `opt/services/api_key_rotation.py` | 258 | blank line contains whitespace |
| 2603 | W293 | `opt/services/api_key_rotation.py` | 253 | blank line contains whitespace |
| 2602 | W293 | `opt/services/api_key_rotation.py` | 249 | blank line contains whitespace |
| 2601 | W293 | `opt/services/api_key_rotation.py` | 243 | blank line contains whitespace |
| 2600 | W293 | `opt/services/api_key_rotation.py` | 240 | blank line contains whitespace |
| 2599 | W293 | `opt/services/api_key_rotation.py` | 235 | blank line contains whitespace |
| 2598 | W293 | `opt/services/api_key_rotation.py` | 230 | blank line contains whitespace |
| 2597 | W293 | `opt/services/api_key_rotation.py` | 223 | blank line contains whitespace |
| 2596 | W293 | `opt/services/api_key_rotation.py` | 220 | blank line contains whitespace |
| 2595 | W293 | `opt/services/api_key_rotation.py` | 218 | blank line contains whitespace |
| 2594 | W293 | `opt/services/api_key_rotation.py` | 213 | blank line contains whitespace |
| 2593 | W293 | `opt/services/api_key_rotation.py` | 211 | blank line contains whitespace |
| 2592 | W293 | `opt/services/api_key_rotation.py` | 206 | blank line contains whitespace |
| 2591 | W293 | `opt/services/api_key_rotation.py` | 204 | blank line contains whitespace |
| 2590 | W293 | `opt/services/api_key_rotation.py` | 197 | blank line contains whitespace |
| 2589 | W293 | `opt/services/api_key_rotation.py` | 192 | blank line contains whitespace |
| 2588 | W293 | `opt/services/api_key_rotation.py` | 182 | blank line contains whitespace |
| 2587 | W293 | `opt/services/api_key_rotation.py` | 179 | blank line contains whitespace |
| 2586 | W293 | `opt/services/api_key_rotation.py` | 158 | blank line contains whitespace |
| 2585 | W293 | `opt/services/api_key_rotation.py` | 147 | blank line contains whitespace |
| 2584 | W293 | `opt/services/api_key_rotation.py` | 125 | blank line contains whitespace |
| 2583 | W293 | `opt/services/api_key_rotation.py` | 117 | blank line contains whitespace |
| 2582 | W293 | `opt/services/api_key_rotation.py` | 110 | blank line contains whitespace |
| 2581 | W293 | `opt/services/api_key_rotation.py` | 103 | blank line contains whitespace |
| 2580 | W293 | `opt/services/api_key_rotation.py` | 97 | blank line contains whitespace |
| 2579 | W293 | `opt/services/api_key_rotation.py` | 92 | blank line contains whitespace |
| 2578 | W293 | `opt/services/api_key_rotation.py` | 85 | blank line contains whitespace |
| 2577 | W293 | `opt/services/api_key_rotation.py` | 80 | blank line contains whitespace |
| 2576 | W293 | `opt/services/api_key_rotation.py` | 70 | blank line contains whitespace |
| 2575 | W293 | `opt/services/api_key_rotation.py` | 65 | blank line contains whitespace |
| 2574 | W293 | `opt/services/api_key_rotation.py` | 60 | blank line contains whitespace |
| 2571 | W293 | `opt/services/api_key_manager.py` | 453 | blank line contains whitespace |
| 2570 | W293 | `opt/services/api_key_manager.py` | 449 | blank line contains whitespace |
| 2569 | W293 | `opt/services/api_key_manager.py` | 440 | blank line contains whitespace |
| 2568 | W293 | `opt/services/api_key_manager.py` | 438 | blank line contains whitespace |
| 2567 | W293 | `opt/services/api_key_manager.py` | 431 | blank line contains whitespace |
| 2566 | W293 | `opt/services/api_key_manager.py` | 418 | blank line contains whitespace |
| 2565 | W293 | `opt/services/api_key_manager.py` | 410 | blank line contains whitespace |
| 2564 | W293 | `opt/services/api_key_manager.py` | 408 | blank line contains whitespace |
| 2563 | W293 | `opt/services/api_key_manager.py` | 405 | blank line contains whitespace |
| 2562 | W293 | `opt/services/api_key_manager.py` | 398 | blank line contains whitespace |
| 2561 | W293 | `opt/services/api_key_manager.py` | 392 | blank line contains whitespace |
| 2560 | W293 | `opt/services/api_key_manager.py` | 387 | blank line contains whitespace |
| 2559 | W293 | `opt/services/api_key_manager.py` | 383 | blank line contains whitespace |
| 2558 | W293 | `opt/services/api_key_manager.py` | 381 | blank line contains whitespace |
| 2557 | W293 | `opt/services/api_key_manager.py` | 366 | blank line contains whitespace |
| 2556 | W293 | `opt/services/api_key_manager.py` | 363 | blank line contains whitespace |
| 2555 | W293 | `opt/services/api_key_manager.py` | 357 | blank line contains whitespace |
| 2554 | W293 | `opt/services/api_key_manager.py` | 353 | blank line contains whitespace |
| 2553 | W293 | `opt/services/api_key_manager.py` | 351 | blank line contains whitespace |
| 2552 | W293 | `opt/services/api_key_manager.py` | 346 | blank line contains whitespace |
| 2551 | W293 | `opt/services/api_key_manager.py` | 341 | blank line contains whitespace |
| 2550 | W293 | `opt/services/api_key_manager.py` | 337 | blank line contains whitespace |
| 2549 | W293 | `opt/services/api_key_manager.py` | 330 | blank line contains whitespace |
| 2548 | W293 | `opt/services/api_key_manager.py` | 325 | blank line contains whitespace |
| 2547 | W293 | `opt/services/api_key_manager.py` | 317 | blank line contains whitespace |
| 2546 | W293 | `opt/services/api_key_manager.py` | 314 | blank line contains whitespace |
| 2545 | W293 | `opt/services/api_key_manager.py` | 308 | blank line contains whitespace |
| 2544 | W293 | `opt/services/api_key_manager.py` | 306 | blank line contains whitespace |
| 2543 | W293 | `opt/services/api_key_manager.py` | 301 | blank line contains whitespace |
| 2542 | W293 | `opt/services/api_key_manager.py` | 289 | blank line contains whitespace |
| 2541 | W293 | `opt/services/api_key_manager.py` | 287 | blank line contains whitespace |
| 2540 | W293 | `opt/services/api_key_manager.py` | 281 | blank line contains whitespace |
| 2539 | W293 | `opt/services/api_key_manager.py` | 273 | blank line contains whitespace |
| 2538 | W293 | `opt/services/api_key_manager.py` | 270 | blank line contains whitespace |
| 2537 | W293 | `opt/services/api_key_manager.py` | 263 | blank line contains whitespace |
| 2536 | W293 | `opt/services/api_key_manager.py` | 260 | blank line contains whitespace |
| 2535 | W293 | `opt/services/api_key_manager.py` | 252 | blank line contains whitespace |
| 2534 | W293 | `opt/services/api_key_manager.py` | 249 | blank line contains whitespace |
| 2533 | W293 | `opt/services/api_key_manager.py` | 247 | blank line contains whitespace |
| 2532 | W293 | `opt/services/api_key_manager.py` | 242 | blank line contains whitespace |
| 2531 | W293 | `opt/services/api_key_manager.py` | 231 | blank line contains whitespace |
| 2530 | W293 | `opt/services/api_key_manager.py` | 220 | blank line contains whitespace |
| 2529 | W293 | `opt/services/api_key_manager.py` | 216 | blank line contains whitespace |
| 2528 | W293 | `opt/services/api_key_manager.py` | 212 | blank line contains whitespace |
| 2527 | W293 | `opt/services/api_key_manager.py` | 210 | blank line contains whitespace |
| 2526 | W293 | `opt/services/api_key_manager.py` | 205 | blank line contains whitespace |
| 2525 | W293 | `opt/services/api_key_manager.py` | 193 | blank line contains whitespace |
| 2524 | W293 | `opt/services/api_key_manager.py` | 189 | blank line contains whitespace |
| 2523 | W293 | `opt/services/api_key_manager.py` | 176 | blank line contains whitespace |
| 2522 | W293 | `opt/services/api_key_manager.py` | 171 | blank line contains whitespace |
| 2521 | W293 | `opt/services/api_key_manager.py` | 163 | blank line contains whitespace |
| 2520 | W293 | `opt/services/api_key_manager.py` | 153 | blank line contains whitespace |
| 2519 | W293 | `opt/services/api_key_manager.py` | 149 | blank line contains whitespace |
| 2518 | W293 | `opt/services/api_key_manager.py` | 144 | blank line contains whitespace |
| 2517 | W293 | `opt/services/api_key_manager.py` | 139 | blank line contains whitespace |
| 2516 | W293 | `opt/services/api_key_manager.py` | 136 | blank line contains whitespace |
| 2515 | W293 | `opt/services/api_key_manager.py` | 126 | blank line contains whitespace |
| 2514 | W293 | `opt/services/api_key_manager.py` | 117 | blank line contains whitespace |
| 2513 | W293 | `opt/services/api_key_manager.py` | 106 | blank line contains whitespace |
| 2512 | W293 | `opt/services/api_key_manager.py` | 101 | blank line contains whitespace |
| 2511 | W293 | `opt/services/api_key_manager.py` | 97 | blank line contains whitespace |
| 2510 | W293 | `opt/services/api_key_manager.py` | 90 | blank line contains whitespace |
| 2509 | W293 | `opt/services/api_key_manager.py` | 87 | blank line contains whitespace |
| 2508 | W291 | `opt/services/api_key_manager.py` | 67 | trailing whitespace |
| 2507 | W293 | `opt/services/api_key_manager.py` | 60 | blank line contains whitespace |
| 2506 | W293 | `opt/services/api_key_manager.py` | 51 | blank line contains whitespace |
| 2505 | W293 | `opt/services/anomaly/test_lstm.py` | 56 | blank line contains whitespace |
| 2504 | W291 | `opt/services/anomaly/test_lstm.py` | 52 | trailing whitespace |
| 2503 | W291 | `opt/services/anomaly/test_lstm.py` | 51 | trailing whitespace |
| 2502 | W291 | `opt/services/anomaly/test_lstm.py` | 41 | trailing whitespace |
| 2501 | W291 | `opt/services/anomaly/test_lstm.py` | 40 | trailing whitespace |
| 2500 | W293 | `opt/services/anomaly/test_lstm.py` | 31 | blank line contains whitespace |
| 2499 | W291 | `opt/services/anomaly/test_lstm.py` | 23 | trailing whitespace |
| 2498 | W291 | `opt/services/anomaly/test_lstm.py` | 22 | trailing whitespace |
| 2497 | W291 | `opt/services/anomaly/test_lstm.py` | 21 | trailing whitespace |
| 2496 | W293 | `opt/services/anomaly/test_lstm.py` | 16 | blank line contains whitespace |
| 2494 | W293 | `opt/services/anomaly/core.py` | 1021 | blank line contains whitespace |
| 2493 | W293 | `opt/services/anomaly/core.py` | 1018 | blank line contains whitespace |
| 2492 | W293 | `opt/services/anomaly/core.py` | 1006 | blank line contains whitespace |
| 2491 | W293 | `opt/services/anomaly/core.py` | 1003 | blank line contains whitespace |
| 2490 | W293 | `opt/services/anomaly/core.py` | 999 | blank line contains whitespace |
| 2489 | W293 | `opt/services/anomaly/core.py` | 995 | blank line contains whitespace |
| 2488 | W293 | `opt/services/anomaly/core.py` | 988 | blank line contains whitespace |
| 2487 | W293 | `opt/services/anomaly/core.py` | 985 | blank line contains whitespace |
| 2486 | W293 | `opt/services/anomaly/core.py` | 982 | blank line contains whitespace |
| 2485 | W293 | `opt/services/anomaly/core.py` | 970 | blank line contains whitespace |
| 2484 | W293 | `opt/services/anomaly/core.py` | 966 | blank line contains whitespace |
| 2483 | W293 | `opt/services/anomaly/core.py` | 954 | blank line contains whitespace |
| 2482 | W293 | `opt/services/anomaly/core.py` | 951 | blank line contains whitespace |
| 2481 | W293 | `opt/services/anomaly/core.py` | 931 | blank line contains whitespace |
| 2480 | W293 | `opt/services/anomaly/core.py` | 924 | blank line contains whitespace |
| 2479 | W293 | `opt/services/anomaly/core.py` | 919 | blank line contains whitespace |
| 2478 | W293 | `opt/services/anomaly/core.py` | 916 | blank line contains whitespace |
| 2477 | W293 | `opt/services/anomaly/core.py` | 913 | blank line contains whitespace |
| 2476 | W293 | `opt/services/anomaly/core.py` | 911 | blank line contains whitespace |
| 2475 | W293 | `opt/services/anomaly/core.py` | 906 | blank line contains whitespace |
| 2474 | W293 | `opt/services/anomaly/core.py` | 901 | blank line contains whitespace |
| 2473 | W293 | `opt/services/anomaly/core.py` | 891 | blank line contains whitespace |
| 2472 | W293 | `opt/services/anomaly/core.py` | 888 | blank line contains whitespace |
| 2471 | W293 | `opt/services/anomaly/core.py` | 885 | blank line contains whitespace |
| 2470 | W293 | `opt/services/anomaly/core.py` | 880 | blank line contains whitespace |
| 2469 | W293 | `opt/services/anomaly/core.py` | 876 | blank line contains whitespace |
| 2468 | W293 | `opt/services/anomaly/core.py` | 867 | blank line contains whitespace |
| 2467 | W293 | `opt/services/anomaly/core.py` | 855 | blank line contains whitespace |
| 2466 | W293 | `opt/services/anomaly/core.py` | 850 | blank line contains whitespace |
| 2465 | W293 | `opt/services/anomaly/core.py` | 840 | blank line contains whitespace |
| 2464 | W293 | `opt/services/anomaly/core.py` | 837 | blank line contains whitespace |
| 2463 | W293 | `opt/services/anomaly/core.py` | 824 | blank line contains whitespace |
| 2462 | W293 | `opt/services/anomaly/core.py` | 821 | blank line contains whitespace |
| 2461 | W293 | `opt/services/anomaly/core.py` | 818 | blank line contains whitespace |
| 2460 | W293 | `opt/services/anomaly/core.py` | 810 | blank line contains whitespace |
| 2459 | W293 | `opt/services/anomaly/core.py` | 807 | blank line contains whitespace |
| 2458 | W293 | `opt/services/anomaly/core.py` | 803 | blank line contains whitespace |
| 2457 | W293 | `opt/services/anomaly/core.py` | 800 | blank line contains whitespace |
| 2456 | W293 | `opt/services/anomaly/core.py` | 794 | blank line contains whitespace |
| 2455 | W293 | `opt/services/anomaly/core.py` | 791 | blank line contains whitespace |
| 2454 | W293 | `opt/services/anomaly/core.py` | 786 | blank line contains whitespace |
| 2453 | W293 | `opt/services/anomaly/core.py` | 781 | blank line contains whitespace |
| 2452 | W293 | `opt/services/anomaly/core.py` | 767 | blank line contains whitespace |
| 2451 | W293 | `opt/services/anomaly/core.py` | 764 | blank line contains whitespace |
| 2450 | W293 | `opt/services/anomaly/core.py` | 761 | blank line contains whitespace |
| 2449 | W293 | `opt/services/anomaly/core.py` | 755 | blank line contains whitespace |
| 2448 | W293 | `opt/services/anomaly/core.py` | 740 | blank line contains whitespace |
| 2447 | W293 | `opt/services/anomaly/core.py` | 738 | blank line contains whitespace |
| 2446 | W293 | `opt/services/anomaly/core.py` | 731 | blank line contains whitespace |
| 2445 | W293 | `opt/services/anomaly/core.py` | 729 | blank line contains whitespace |
| 2444 | W293 | `opt/services/anomaly/core.py` | 723 | blank line contains whitespace |
| 2443 | W293 | `opt/services/anomaly/core.py` | 719 | blank line contains whitespace |
| 2442 | W293 | `opt/services/anomaly/core.py` | 717 | blank line contains whitespace |
| 2441 | W293 | `opt/services/anomaly/core.py` | 712 | blank line contains whitespace |
| 2440 | W293 | `opt/services/anomaly/core.py` | 708 | blank line contains whitespace |
| 2439 | W293 | `opt/services/anomaly/core.py` | 704 | blank line contains whitespace |
| 2438 | W293 | `opt/services/anomaly/core.py` | 696 | blank line contains whitespace |
| 2437 | W293 | `opt/services/anomaly/core.py` | 684 | blank line contains whitespace |
| 2436 | W293 | `opt/services/anomaly/core.py` | 669 | blank line contains whitespace |
| 2435 | W293 | `opt/services/anomaly/core.py` | 667 | blank line contains whitespace |
| 2434 | W293 | `opt/services/anomaly/core.py` | 660 | blank line contains whitespace |
| 2433 | W293 | `opt/services/anomaly/core.py` | 658 | blank line contains whitespace |
| 2432 | W293 | `opt/services/anomaly/core.py` | 652 | blank line contains whitespace |
| 2431 | W293 | `opt/services/anomaly/core.py` | 650 | blank line contains whitespace |
| 2430 | W293 | `opt/services/anomaly/core.py` | 647 | blank line contains whitespace |
| 2429 | W293 | `opt/services/anomaly/core.py` | 643 | blank line contains whitespace |
| 2428 | W293 | `opt/services/anomaly/core.py` | 641 | blank line contains whitespace |
| 2427 | W293 | `opt/services/anomaly/core.py` | 638 | blank line contains whitespace |
| 2426 | W293 | `opt/services/anomaly/core.py` | 626 | blank line contains whitespace |
| 2425 | W293 | `opt/services/anomaly/core.py` | 611 | blank line contains whitespace |
| 2424 | W293 | `opt/services/anomaly/core.py` | 609 | blank line contains whitespace |
| 2423 | W293 | `opt/services/anomaly/core.py` | 603 | blank line contains whitespace |
| 2422 | W293 | `opt/services/anomaly/core.py` | 599 | blank line contains whitespace |
| 2421 | W293 | `opt/services/anomaly/core.py` | 592 | blank line contains whitespace |
| 2420 | W293 | `opt/services/anomaly/core.py` | 578 | blank line contains whitespace |
| 2419 | W293 | `opt/services/anomaly/core.py` | 563 | blank line contains whitespace |
| 2418 | W293 | `opt/services/anomaly/core.py` | 558 | blank line contains whitespace |
| 2417 | W293 | `opt/services/anomaly/core.py` | 552 | blank line contains whitespace |
| 2416 | W293 | `opt/services/anomaly/core.py` | 549 | blank line contains whitespace |
| 2415 | W293 | `opt/services/anomaly/core.py` | 542 | blank line contains whitespace |
| 2414 | W293 | `opt/services/anomaly/core.py` | 540 | blank line contains whitespace |
| 2413 | W293 | `opt/services/anomaly/core.py` | 527 | blank line contains whitespace |
| 2412 | W293 | `opt/services/anomaly/core.py` | 522 | blank line contains whitespace |
| 2411 | W293 | `opt/services/anomaly/core.py` | 506 | blank line contains whitespace |
| 2410 | W293 | `opt/services/anomaly/core.py` | 498 | blank line contains whitespace |
| 2409 | W293 | `opt/services/anomaly/core.py` | 490 | blank line contains whitespace |
| 2408 | W293 | `opt/services/anomaly/core.py` | 482 | blank line contains whitespace |
| 2407 | W293 | `opt/services/anomaly/core.py` | 479 | blank line contains whitespace |
| 2406 | W293 | `opt/services/anomaly/core.py` | 468 | blank line contains whitespace |
| 2405 | W293 | `opt/services/anomaly/core.py` | 462 | blank line contains whitespace |
| 2404 | W293 | `opt/services/anomaly/core.py` | 449 | blank line contains whitespace |
| 2403 | W293 | `opt/services/anomaly/core.py` | 445 | blank line contains whitespace |
| 2402 | W293 | `opt/services/anomaly/core.py` | 415 | blank line contains whitespace |
| 2401 | W293 | `opt/services/anomaly/core.py` | 413 | blank line contains whitespace |
| 2400 | W293 | `opt/services/anomaly/core.py` | 409 | blank line contains whitespace |
| 2399 | W293 | `opt/services/anomaly/core.py` | 404 | blank line contains whitespace |
| 2398 | W293 | `opt/services/anomaly/core.py` | 399 | blank line contains whitespace |
| 2397 | W293 | `opt/services/anomaly/core.py` | 389 | blank line contains whitespace |
| 2396 | W293 | `opt/services/anomaly/core.py` | 382 | blank line contains whitespace |
| 2395 | W293 | `opt/services/anomaly/core.py` | 378 | blank line contains whitespace |
| 2394 | W293 | `opt/services/anomaly/core.py` | 370 | blank line contains whitespace |
| 2393 | W293 | `opt/services/anomaly/core.py` | 354 | blank line contains whitespace |
| 2392 | W293 | `opt/services/anomaly/core.py` | 342 | blank line contains whitespace |
| 2391 | W293 | `opt/services/anomaly/core.py` | 331 | blank line contains whitespace |
| 2390 | W293 | `opt/services/anomaly/core.py` | 319 | blank line contains whitespace |
| 2389 | W293 | `opt/services/anomaly/core.py` | 305 | blank line contains whitespace |
| 2388 | W293 | `opt/services/anomaly/core.py` | 302 | blank line contains whitespace |
| 2387 | W293 | `opt/services/anomaly/core.py` | 299 | blank line contains whitespace |
| 2386 | W293 | `opt/services/anomaly/core.py` | 290 | blank line contains whitespace |
| 2385 | W291 | `opt/services/anomaly/core.py` | 287 | trailing whitespace |
| 2383 | W293 | `opt/services/anomaly/core.py` | 282 | blank line contains whitespace |
| 2380 | W293 | `opt/services/anomaly/core.py` | 277 | blank line contains whitespace |
| 2378 | W293 | `opt/services/anomaly/core.py` | 275 | blank line contains whitespace |
| 2377 | W293 | `opt/services/anomaly/core.py` | 270 | blank line contains whitespace |
| 2376 | W293 | `opt/services/anomaly/core.py` | 263 | blank line contains whitespace |
| 2375 | W293 | `opt/services/anomaly/core.py` | 253 | blank line contains whitespace |
| 2374 | W293 | `opt/services/anomaly/core.py` | 250 | blank line contains whitespace |
| 2373 | W293 | `opt/services/anomaly/core.py` | 246 | blank line contains whitespace |
| 2372 | W293 | `opt/services/anomaly/core.py` | 242 | blank line contains whitespace |
| 2371 | W293 | `opt/services/anomaly/core.py` | 238 | blank line contains whitespace |
| 2370 | W293 | `opt/services/anomaly/core.py` | 236 | blank line contains whitespace |
| 2369 | W293 | `opt/services/anomaly/core.py` | 222 | blank line contains whitespace |
| 2368 | W293 | `opt/services/anomaly/core.py` | 216 | blank line contains whitespace |
| 2367 | W293 | `opt/services/anomaly/core.py` | 208 | blank line contains whitespace |
| 2366 | W293 | `opt/services/anomaly/core.py` | 203 | blank line contains whitespace |
| 2361 | W293 | `opt/services/anomaly/cli.py` | 648 | blank line contains whitespace |
| 2360 | W293 | `opt/services/anomaly/cli.py` | 643 | blank line contains whitespace |
| 2359 | W293 | `opt/services/anomaly/cli.py` | 637 | blank line contains whitespace |
| 2358 | W293 | `opt/services/anomaly/cli.py` | 631 | blank line contains whitespace |
| 2357 | W293 | `opt/services/anomaly/cli.py` | 622 | blank line contains whitespace |
| 2356 | W293 | `opt/services/anomaly/cli.py` | 597 | blank line contains whitespace |
| 2355 | W293 | `opt/services/anomaly/cli.py` | 588 | blank line contains whitespace |
| 2354 | W293 | `opt/services/anomaly/cli.py` | 582 | blank line contains whitespace |
| 2353 | W293 | `opt/services/anomaly/cli.py` | 566 | blank line contains whitespace |
| 2352 | W293 | `opt/services/anomaly/cli.py` | 552 | blank line contains whitespace |
| 2351 | W293 | `opt/services/anomaly/cli.py` | 532 | blank line contains whitespace |
| 2350 | W293 | `opt/services/anomaly/cli.py` | 524 | blank line contains whitespace |
| 2349 | W293 | `opt/services/anomaly/cli.py` | 515 | blank line contains whitespace |
| 2348 | W293 | `opt/services/anomaly/cli.py` | 502 | blank line contains whitespace |
| 2347 | W293 | `opt/services/anomaly/cli.py` | 495 | blank line contains whitespace |
| 2346 | W293 | `opt/services/anomaly/cli.py` | 486 | blank line contains whitespace |
| 2345 | W293 | `opt/services/anomaly/cli.py` | 472 | blank line contains whitespace |
| 2344 | W293 | `opt/services/anomaly/cli.py` | 463 | blank line contains whitespace |
| 2343 | W293 | `opt/services/anomaly/cli.py` | 447 | blank line contains whitespace |
| 2342 | W293 | `opt/services/anomaly/cli.py` | 434 | blank line contains whitespace |
| 2341 | W293 | `opt/services/anomaly/cli.py` | 427 | blank line contains whitespace |
| 2340 | W293 | `opt/services/anomaly/cli.py` | 413 | blank line contains whitespace |
| 2339 | W293 | `opt/services/anomaly/cli.py` | 411 | blank line contains whitespace |
| 2338 | W293 | `opt/services/anomaly/cli.py` | 404 | blank line contains whitespace |
| 2337 | W293 | `opt/services/anomaly/cli.py` | 392 | blank line contains whitespace |
| 2336 | W293 | `opt/services/anomaly/cli.py` | 369 | blank line contains whitespace |
| 2335 | W293 | `opt/services/anomaly/cli.py` | 365 | blank line contains whitespace |
| 2334 | W293 | `opt/services/anomaly/cli.py` | 360 | blank line contains whitespace |
| 2333 | W293 | `opt/services/anomaly/cli.py` | 350 | blank line contains whitespace |
| 2332 | W293 | `opt/services/anomaly/cli.py` | 341 | blank line contains whitespace |
| 2331 | W293 | `opt/services/anomaly/cli.py` | 335 | blank line contains whitespace |
| 2329 | W293 | `opt/services/anomaly/cli.py` | 321 | blank line contains whitespace |
| 2328 | W293 | `opt/services/anomaly/cli.py` | 300 | blank line contains whitespace |
| 2327 | W293 | `opt/services/anomaly/cli.py` | 294 | blank line contains whitespace |
| 2326 | W293 | `opt/services/anomaly/cli.py` | 290 | blank line contains whitespace |
| 2325 | W293 | `opt/services/anomaly/cli.py` | 285 | blank line contains whitespace |
| 2324 | W293 | `opt/services/anomaly/cli.py` | 275 | blank line contains whitespace |
| 2323 | W293 | `opt/services/anomaly/cli.py` | 267 | blank line contains whitespace |
| 2322 | W293 | `opt/services/anomaly/cli.py` | 259 | blank line contains whitespace |
| 2321 | W293 | `opt/services/anomaly/cli.py` | 243 | blank line contains whitespace |
| 2320 | W293 | `opt/services/anomaly/cli.py` | 226 | blank line contains whitespace |
| 2319 | W293 | `opt/services/anomaly/cli.py` | 222 | blank line contains whitespace |
| 2318 | W293 | `opt/services/anomaly/cli.py` | 216 | blank line contains whitespace |
| 2317 | W293 | `opt/services/anomaly/cli.py` | 213 | blank line contains whitespace |
| 2316 | W293 | `opt/services/anomaly/cli.py` | 204 | blank line contains whitespace |
| 2315 | W293 | `opt/services/anomaly/cli.py` | 200 | blank line contains whitespace |
| 2314 | W293 | `opt/services/anomaly/cli.py` | 197 | blank line contains whitespace |
| 2313 | W293 | `opt/services/anomaly/cli.py` | 188 | blank line contains whitespace |
| 2312 | W293 | `opt/services/anomaly/cli.py` | 182 | blank line contains whitespace |
| 2311 | W293 | `opt/services/anomaly/cli.py` | 173 | blank line contains whitespace |
| 2310 | W293 | `opt/services/anomaly/cli.py` | 167 | blank line contains whitespace |
| 2309 | W293 | `opt/services/anomaly/cli.py` | 161 | blank line contains whitespace |
| 2308 | W293 | `opt/services/anomaly/cli.py` | 156 | blank line contains whitespace |
| 2307 | W293 | `opt/services/anomaly/cli.py` | 145 | blank line contains whitespace |
| 2306 | W293 | `opt/services/anomaly/cli.py` | 138 | blank line contains whitespace |
| 2305 | W293 | `opt/services/anomaly/cli.py` | 128 | blank line contains whitespace |
| 2304 | W293 | `opt/services/anomaly/cli.py` | 124 | blank line contains whitespace |
| 2303 | W293 | `opt/services/anomaly/cli.py` | 118 | blank line contains whitespace |
| 2302 | W293 | `opt/services/anomaly/cli.py` | 107 | blank line contains whitespace |
| 2301 | W293 | `opt/services/anomaly/cli.py` | 102 | blank line contains whitespace |
| 2300 | W293 | `opt/services/anomaly/cli.py` | 96 | blank line contains whitespace |
| 2299 | W293 | `opt/services/anomaly/cli.py` | 89 | blank line contains whitespace |
| 2298 | W293 | `opt/services/anomaly/cli.py` | 86 | blank line contains whitespace |
| 2297 | W293 | `opt/services/anomaly/cli.py` | 83 | blank line contains whitespace |
| 2296 | W293 | `opt/services/anomaly/cli.py` | 80 | blank line contains whitespace |
| 2295 | W293 | `opt/services/anomaly/cli.py` | 77 | blank line contains whitespace |
| 2294 | W293 | `opt/services/anomaly/cli.py` | 74 | blank line contains whitespace |
| 2293 | W293 | `opt/services/anomaly/cli.py` | 71 | blank line contains whitespace |
| 2292 | W293 | `opt/services/anomaly/cli.py` | 69 | blank line contains whitespace |
| 2291 | W293 | `opt/services/anomaly/cli.py` | 62 | blank line contains whitespace |
| 2290 | W293 | `opt/services/anomaly/cli.py` | 49 | blank line contains whitespace |
| 2289 | W293 | `opt/services/anomaly/cli.py` | 32 | blank line contains whitespace |
| 2288 | W293 | `opt/services/anomaly/cli.py` | 29 | blank line contains whitespace |
| 2287 | W293 | `opt/services/anomaly/cli.py` | 23 | blank line contains whitespace |
| 2284 | W293 | `opt/services/anomaly/api.py` | 809 | blank line contains whitespace |
| 2283 | W293 | `opt/services/anomaly/api.py` | 800 | blank line contains whitespace |
| 2282 | W293 | `opt/services/anomaly/api.py` | 796 | blank line contains whitespace |
| 2281 | W293 | `opt/services/anomaly/api.py` | 792 | blank line contains whitespace |
| 2280 | W293 | `opt/services/anomaly/api.py` | 788 | blank line contains whitespace |
| 2279 | W293 | `opt/services/anomaly/api.py` | 784 | blank line contains whitespace |
| 2278 | W293 | `opt/services/anomaly/api.py` | 780 | blank line contains whitespace |
| 2277 | W293 | `opt/services/anomaly/api.py` | 776 | blank line contains whitespace |
| 2276 | W293 | `opt/services/anomaly/api.py` | 771 | blank line contains whitespace |
| 2275 | W293 | `opt/services/anomaly/api.py` | 767 | blank line contains whitespace |
| 2274 | W293 | `opt/services/anomaly/api.py` | 763 | blank line contains whitespace |
| 2273 | W293 | `opt/services/anomaly/api.py` | 759 | blank line contains whitespace |
| 2272 | W293 | `opt/services/anomaly/api.py` | 755 | blank line contains whitespace |
| 2271 | W293 | `opt/services/anomaly/api.py` | 751 | blank line contains whitespace |
| 2270 | W293 | `opt/services/anomaly/api.py` | 747 | blank line contains whitespace |
| 2269 | W293 | `opt/services/anomaly/api.py` | 743 | blank line contains whitespace |
| 2268 | W293 | `opt/services/anomaly/api.py` | 739 | blank line contains whitespace |
| 2267 | W293 | `opt/services/anomaly/api.py` | 735 | blank line contains whitespace |
| 2266 | W293 | `opt/services/anomaly/api.py` | 731 | blank line contains whitespace |
| 2265 | W293 | `opt/services/anomaly/api.py` | 727 | blank line contains whitespace |
| 2264 | W293 | `opt/services/anomaly/api.py` | 723 | blank line contains whitespace |
| 2263 | W293 | `opt/services/anomaly/api.py` | 719 | blank line contains whitespace |
| 2262 | W293 | `opt/services/anomaly/api.py` | 715 | blank line contains whitespace |
| 2261 | W293 | `opt/services/anomaly/api.py` | 711 | blank line contains whitespace |
| 2260 | W293 | `opt/services/anomaly/api.py` | 708 | blank line contains whitespace |
| 2259 | W293 | `opt/services/anomaly/api.py` | 705 | blank line contains whitespace |
| 2258 | W293 | `opt/services/anomaly/api.py` | 699 | blank line contains whitespace |
| 2257 | W293 | `opt/services/anomaly/api.py` | 696 | blank line contains whitespace |
| 2256 | W293 | `opt/services/anomaly/api.py` | 676 | blank line contains whitespace |
| 2255 | W293 | `opt/services/anomaly/api.py` | 671 | blank line contains whitespace |
| 2254 | W293 | `opt/services/anomaly/api.py` | 658 | blank line contains whitespace |
| 2253 | W293 | `opt/services/anomaly/api.py` | 652 | blank line contains whitespace |
| 2252 | W293 | `opt/services/anomaly/api.py` | 650 | blank line contains whitespace |
| 2251 | W293 | `opt/services/anomaly/api.py` | 646 | blank line contains whitespace |
| 2250 | W293 | `opt/services/anomaly/api.py` | 644 | blank line contains whitespace |
| 2249 | W293 | `opt/services/anomaly/api.py` | 638 | blank line contains whitespace |
| 2248 | W293 | `opt/services/anomaly/api.py` | 631 | blank line contains whitespace |
| 2247 | W293 | `opt/services/anomaly/api.py` | 620 | blank line contains whitespace |
| 2246 | W293 | `opt/services/anomaly/api.py` | 618 | blank line contains whitespace |
| 2245 | W293 | `opt/services/anomaly/api.py` | 610 | blank line contains whitespace |
| 2244 | W293 | `opt/services/anomaly/api.py` | 603 | blank line contains whitespace |
| 2243 | W293 | `opt/services/anomaly/api.py` | 599 | blank line contains whitespace |
| 2242 | W293 | `opt/services/anomaly/api.py` | 596 | blank line contains whitespace |
| 2241 | W293 | `opt/services/anomaly/api.py` | 586 | blank line contains whitespace |
| 2240 | W293 | `opt/services/anomaly/api.py` | 575 | blank line contains whitespace |
| 2239 | W293 | `opt/services/anomaly/api.py` | 570 | blank line contains whitespace |
| 2238 | W293 | `opt/services/anomaly/api.py` | 556 | blank line contains whitespace |
| 2237 | W293 | `opt/services/anomaly/api.py` | 544 | blank line contains whitespace |
| 2236 | W293 | `opt/services/anomaly/api.py` | 538 | blank line contains whitespace |
| 2235 | W293 | `opt/services/anomaly/api.py` | 532 | blank line contains whitespace |
| 2234 | W293 | `opt/services/anomaly/api.py` | 529 | blank line contains whitespace |
| 2233 | W293 | `opt/services/anomaly/api.py` | 526 | blank line contains whitespace |
| 2232 | W293 | `opt/services/anomaly/api.py` | 523 | blank line contains whitespace |
| 2231 | W293 | `opt/services/anomaly/api.py` | 515 | blank line contains whitespace |
| 2230 | W293 | `opt/services/anomaly/api.py` | 506 | blank line contains whitespace |
| 2229 | W293 | `opt/services/anomaly/api.py` | 500 | blank line contains whitespace |
| 2228 | W293 | `opt/services/anomaly/api.py` | 494 | blank line contains whitespace |
| 2227 | W293 | `opt/services/anomaly/api.py` | 484 | blank line contains whitespace |
| 2226 | W293 | `opt/services/anomaly/api.py` | 477 | blank line contains whitespace |
| 2225 | W293 | `opt/services/anomaly/api.py` | 471 | blank line contains whitespace |
| 2224 | W293 | `opt/services/anomaly/api.py` | 466 | blank line contains whitespace |
| 2223 | W293 | `opt/services/anomaly/api.py` | 456 | blank line contains whitespace |
| 2222 | W293 | `opt/services/anomaly/api.py` | 448 | blank line contains whitespace |
| 2221 | W293 | `opt/services/anomaly/api.py` | 435 | blank line contains whitespace |
| 2220 | W293 | `opt/services/anomaly/api.py` | 429 | blank line contains whitespace |
| 2219 | W293 | `opt/services/anomaly/api.py` | 423 | blank line contains whitespace |
| 2218 | W293 | `opt/services/anomaly/api.py` | 413 | blank line contains whitespace |
| 2217 | W293 | `opt/services/anomaly/api.py` | 406 | blank line contains whitespace |
| 2216 | W293 | `opt/services/anomaly/api.py` | 400 | blank line contains whitespace |
| 2215 | W293 | `opt/services/anomaly/api.py` | 391 | blank line contains whitespace |
| 2214 | W293 | `opt/services/anomaly/api.py` | 380 | blank line contains whitespace |
| 2213 | W293 | `opt/services/anomaly/api.py` | 372 | blank line contains whitespace |
| 2212 | W293 | `opt/services/anomaly/api.py` | 365 | blank line contains whitespace |
| 2211 | W293 | `opt/services/anomaly/api.py` | 360 | blank line contains whitespace |
| 2210 | W293 | `opt/services/anomaly/api.py` | 357 | blank line contains whitespace |
| 2209 | W293 | `opt/services/anomaly/api.py` | 346 | blank line contains whitespace |
| 2208 | W293 | `opt/services/anomaly/api.py` | 335 | blank line contains whitespace |
| 2207 | W293 | `opt/services/anomaly/api.py` | 330 | blank line contains whitespace |
| 2206 | W293 | `opt/services/anomaly/api.py` | 328 | blank line contains whitespace |
| 2205 | W293 | `opt/services/anomaly/api.py` | 322 | blank line contains whitespace |
| 2204 | W293 | `opt/services/anomaly/api.py` | 320 | blank line contains whitespace |
| 2203 | W293 | `opt/services/anomaly/api.py` | 305 | blank line contains whitespace |
| 2202 | W293 | `opt/services/anomaly/api.py` | 299 | blank line contains whitespace |
| 2201 | W293 | `opt/services/anomaly/api.py` | 297 | blank line contains whitespace |
| 2200 | W293 | `opt/services/anomaly/api.py` | 293 | blank line contains whitespace |
| 2199 | W293 | `opt/services/anomaly/api.py` | 291 | blank line contains whitespace |
| 2198 | W293 | `opt/services/anomaly/api.py` | 285 | blank line contains whitespace |
| 2197 | W293 | `opt/services/anomaly/api.py` | 278 | blank line contains whitespace |
| 2196 | W293 | `opt/services/anomaly/api.py` | 273 | blank line contains whitespace |
| 2195 | W293 | `opt/services/anomaly/api.py` | 267 | blank line contains whitespace |
| 2194 | W293 | `opt/services/anomaly/api.py` | 261 | blank line contains whitespace |
| 2193 | W293 | `opt/services/anomaly/api.py` | 253 | blank line contains whitespace |
| 2192 | W293 | `opt/services/anomaly/api.py` | 246 | blank line contains whitespace |
| 2191 | W293 | `opt/services/anomaly/api.py` | 242 | blank line contains whitespace |
| 2190 | W293 | `opt/services/anomaly/api.py` | 239 | blank line contains whitespace |
| 2189 | W293 | `opt/services/anomaly/api.py` | 229 | blank line contains whitespace |
| 2188 | W293 | `opt/services/anomaly/api.py` | 216 | blank line contains whitespace |
| 2187 | W293 | `opt/services/anomaly/api.py` | 202 | blank line contains whitespace |
| 2186 | W293 | `opt/services/anomaly/api.py` | 200 | blank line contains whitespace |
| 2185 | W293 | `opt/services/anomaly/api.py` | 194 | blank line contains whitespace |
| 2184 | W293 | `opt/services/anomaly/api.py` | 192 | blank line contains whitespace |
| 2183 | W293 | `opt/services/anomaly/api.py` | 184 | blank line contains whitespace |
| 2182 | W293 | `opt/services/anomaly/api.py` | 178 | blank line contains whitespace |
| 2181 | W293 | `opt/services/anomaly/api.py` | 171 | blank line contains whitespace |
| 2180 | W293 | `opt/services/anomaly/api.py` | 165 | blank line contains whitespace |
| 2179 | W293 | `opt/services/anomaly/api.py` | 157 | blank line contains whitespace |
| 2178 | W293 | `opt/services/anomaly/api.py` | 151 | blank line contains whitespace |
| 2177 | W293 | `opt/services/anomaly/api.py` | 149 | blank line contains whitespace |
| 2176 | W293 | `opt/services/anomaly/api.py` | 141 | blank line contains whitespace |
| 2175 | W293 | `opt/services/anomaly/api.py` | 134 | blank line contains whitespace |
| 2174 | W293 | `opt/services/anomaly/api.py` | 126 | blank line contains whitespace |
| 2173 | W293 | `opt/services/anomaly/api.py` | 124 | blank line contains whitespace |
| 2172 | W293 | `opt/services/anomaly/api.py` | 116 | blank line contains whitespace |
| 2171 | W293 | `opt/services/anomaly/api.py` | 109 | blank line contains whitespace |
| 2170 | W293 | `opt/services/anomaly/api.py` | 105 | blank line contains whitespace |
| 2169 | W293 | `opt/services/anomaly/api.py` | 102 | blank line contains whitespace |
| 2168 | W293 | `opt/services/anomaly/api.py` | 92 | blank line contains whitespace |
| 2167 | W293 | `opt/services/anomaly/api.py` | 83 | blank line contains whitespace |
| 2166 | W293 | `opt/services/anomaly/api.py` | 80 | blank line contains whitespace |
| 2165 | W293 | `opt/services/anomaly/api.py` | 72 | blank line contains whitespace |
| 2164 | W293 | `opt/services/anomaly/api.py` | 67 | blank line contains whitespace |
| 2163 | W293 | `opt/services/anomaly/api.py` | 54 | blank line contains whitespace |
| 2162 | W293 | `opt/services/anomaly/api.py` | 50 | blank line contains whitespace |
| 2161 | W293 | `opt/services/anomaly/api.py` | 37 | blank line contains whitespace |
| 2158 | W293 | `opt/services/anomaly/**init**.py` | 84 | blank line contains whitespace |
| 2157 | W293 | `opt/services/anomaly/**init**.py` | 80 | blank line contains whitespace |
| 2156 | W293 | `opt/services/anomaly/**init**.py` | 74 | blank line contains whitespace |
| 2155 | W293 | `opt/services/anomaly/**init**.py` | 68 | blank line contains whitespace |
| 2154 | W293 | `opt/services/anomaly/**init**.py` | 37 | blank line contains whitespace |
| 2153 | W293 | `opt/services/anomaly/**init**.py` | 34 | blank line contains whitespace |
| 2152 | W293 | `opt/services/anomaly/**init**.py` | 31 | blank line contains whitespace |
| 2151 | W293 | `opt/services/anomaly/**init**.py` | 28 | blank line contains whitespace |
| 2150 | W293 | `opt/services/anomaly/**init**.py` | 24 | blank line contains whitespace |
| 2149 | W293 | `opt/services/anomaly/**init**.py` | 21 | blank line contains whitespace |
| 2148 | W293 | `opt/security_testing.py` | 239 | blank line contains whitespace |
| 2147 | W293 | `opt/security/hardening_scanner.py` | 236 | blank line contains whitespace |
| 2146 | W293 | `opt/security/hardening_scanner.py` | 227 | blank line contains whitespace |
| 2144 | W293 | `opt/security/hardening_scanner.py` | 219 | blank line contains whitespace |
| 2143 | W293 | `opt/security/hardening_scanner.py` | 209 | blank line contains whitespace |
| 2142 | W293 | `opt/security/hardening_scanner.py` | 197 | blank line contains whitespace |
| 2141 | W293 | `opt/security/hardening_scanner.py` | 187 | blank line contains whitespace |
| 2140 | W293 | `opt/security/hardening_scanner.py` | 176 | blank line contains whitespace |
| 2139 | W293 | `opt/security/hardening_scanner.py` | 166 | blank line contains whitespace |
| 2138 | W293 | `opt/security/hardening_scanner.py` | 156 | blank line contains whitespace |
| 2137 | W293 | `opt/security/hardening_scanner.py` | 147 | blank line contains whitespace |
| 2136 | W293 | `opt/security/hardening_scanner.py` | 137 | blank line contains whitespace |
| 2135 | W293 | `opt/security/hardening_scanner.py` | 121 | blank line contains whitespace |
| 2134 | W293 | `opt/security/hardening_scanner.py` | 111 | blank line contains whitespace |
| 2133 | W293 | `opt/security/hardening_scanner.py` | 101 | blank line contains whitespace |
| 2132 | W293 | `opt/security/hardening_scanner.py` | 91 | blank line contains whitespace |
| 2131 | W293 | `opt/security/hardening_scanner.py` | 78 | blank line contains whitespace |
| 2130 | W293 | `opt/security/hardening_scanner.py` | 67 | blank line contains whitespace |
| 2129 | W293 | `opt/security/hardening_scanner.py` | 51 | blank line contains whitespace |
| 2117 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 89 | blank line contains whitespace |
| 2116 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 86 | blank line contains whitespace |
| 2115 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 74 | blank line contains whitespace |
| 2114 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 68 | blank line contains whitespace |
| 2113 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 62 | blank line contains whitespace |
| 2112 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 60 | blank line contains whitespace |
| 2111 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 50 | blank line contains whitespace |
| 2110 | W293 | `opt/netcfg-tui/tests/test_netcfg.py` | 42 | blank line contains whitespace |
| 2109 | W291 | `opt/netcfg-tui/tests/test_netcfg.py` | 13 | trailing whitespace |
| 2107 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1249 | blank line contains whitespace |
| 2106 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1191 | blank line contains whitespace |
| 2105 | W291 | `opt/netcfg-tui/netcfg_tui.py` | 1185 | trailing whitespace |
| 2104 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1182 | blank line contains whitespace |
| 2103 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1162 | blank line contains whitespace |
| 2102 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1105 | blank line contains whitespace |
| 2101 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1102 | blank line contains whitespace |
| 2100 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1092 | blank line contains whitespace |
| 2099 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1085 | blank line contains whitespace |
| 2098 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1080 | blank line contains whitespace |
| 2097 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1068 | blank line contains whitespace |
| 2096 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1062 | blank line contains whitespace |
| 2095 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1047 | blank line contains whitespace |
| 2094 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1041 | blank line contains whitespace |
| 2093 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1038 | blank line contains whitespace |
| 2092 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1033 | blank line contains whitespace |
| 2091 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1031 | blank line contains whitespace |
| 2090 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1014 | blank line contains whitespace |
| 2089 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1011 | blank line contains whitespace |
| 2088 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 1003 | blank line contains whitespace |
| 2087 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 997 | blank line contains whitespace |
| 2086 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 991 | blank line contains whitespace |
| 2085 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 989 | blank line contains whitespace |
| 2084 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 980 | blank line contains whitespace |
| 2082 | W291 | `opt/netcfg-tui/netcfg_tui.py` | 927 | trailing whitespace |
| 2081 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 910 | blank line contains whitespace |
| 2080 | W291 | `opt/netcfg-tui/netcfg_tui.py` | 901 | trailing whitespace |
| 2079 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 873 | blank line contains whitespace |
| 2078 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 867 | blank line contains whitespace |
| 2077 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 856 | blank line contains whitespace |
| 2076 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 785 | blank line contains whitespace |
| 2075 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 782 | blank line contains whitespace |
| 2074 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 774 | blank line contains whitespace |
| 2072 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 756 | blank line contains whitespace |
| 2070 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 659 | blank line contains whitespace |
| 2069 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 646 | blank line contains whitespace |
| 2068 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 614 | blank line contains whitespace |
| 2067 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 607 | blank line contains whitespace |
| 2066 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 601 | blank line contains whitespace |
| 2065 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 598 | blank line contains whitespace |
| 2064 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 509 | blank line contains whitespace |
| 2063 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 455 | blank line contains whitespace |
| 2062 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 317 | blank line contains whitespace |
| 2061 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 224 | blank line contains whitespace |
| 2060 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 205 | blank line contains whitespace |
| 2059 | W293 | `opt/netcfg-tui/netcfg_tui.py` | 138 | blank line contains whitespace |
| 2057 | W293 | `opt/netcfg-tui/mock_mode.py` | 634 | blank line contains whitespace |
| 2055 | W293 | `opt/netcfg-tui/mock_mode.py` | 631 | blank line contains whitespace |
| 2054 | W293 | `opt/netcfg-tui/mock_mode.py` | 628 | blank line contains whitespace |
| 2053 | W293 | `opt/netcfg-tui/mock_mode.py` | 625 | blank line contains whitespace |
| 2052 | W293 | `opt/netcfg-tui/mock_mode.py` | 622 | blank line contains whitespace |
| 2051 | W293 | `opt/netcfg-tui/mock_mode.py` | 619 | blank line contains whitespace |
| 2050 | W293 | `opt/netcfg-tui/mock_mode.py` | 614 | blank line contains whitespace |
| 2049 | W293 | `opt/netcfg-tui/mock_mode.py` | 610 | blank line contains whitespace |
| 2048 | W293 | `opt/netcfg-tui/mock_mode.py` | 604 | blank line contains whitespace |
| 2047 | W293 | `opt/netcfg-tui/mock_mode.py` | 602 | blank line contains whitespace |
| 2046 | W293 | `opt/netcfg-tui/mock_mode.py` | 569 | blank line contains whitespace |
| 2045 | W293 | `opt/netcfg-tui/mock_mode.py` | 562 | blank line contains whitespace |
| 2044 | W293 | `opt/netcfg-tui/mock_mode.py` | 550 | blank line contains whitespace |
| 2043 | W293 | `opt/netcfg-tui/mock_mode.py` | 540 | blank line contains whitespace |
| 2042 | W293 | `opt/netcfg-tui/mock_mode.py` | 535 | blank line contains whitespace |
| 2041 | W293 | `opt/netcfg-tui/mock_mode.py` | 519 | blank line contains whitespace |
| 2040 | W293 | `opt/netcfg-tui/mock_mode.py` | 515 | blank line contains whitespace |
| 2039 | W293 | `opt/netcfg-tui/mock_mode.py` | 509 | blank line contains whitespace |
| 2038 | W293 | `opt/netcfg-tui/mock_mode.py` | 504 | blank line contains whitespace |
| 2037 | W293 | `opt/netcfg-tui/mock_mode.py` | 500 | blank line contains whitespace |
| 2036 | W293 | `opt/netcfg-tui/mock_mode.py` | 496 | blank line contains whitespace |
| 2035 | W293 | `opt/netcfg-tui/mock_mode.py` | 492 | blank line contains whitespace |
| 2034 | W293 | `opt/netcfg-tui/mock_mode.py` | 487 | blank line contains whitespace |
| 2033 | W293 | `opt/netcfg-tui/mock_mode.py` | 474 | blank line contains whitespace |
| 2032 | W293 | `opt/netcfg-tui/mock_mode.py` | 472 | blank line contains whitespace |
| 2031 | W293 | `opt/netcfg-tui/mock_mode.py` | 469 | blank line contains whitespace |
| 2030 | W293 | `opt/netcfg-tui/mock_mode.py` | 464 | blank line contains whitespace |
| 2029 | W293 | `opt/netcfg-tui/mock_mode.py` | 458 | blank line contains whitespace |
| 2028 | W293 | `opt/netcfg-tui/mock_mode.py` | 447 | blank line contains whitespace |
| 2027 | W293 | `opt/netcfg-tui/mock_mode.py` | 440 | blank line contains whitespace |
| 2026 | W293 | `opt/netcfg-tui/mock_mode.py` | 431 | blank line contains whitespace |
| 2025 | W293 | `opt/netcfg-tui/mock_mode.py` | 424 | blank line contains whitespace |
| 2024 | W293 | `opt/netcfg-tui/mock_mode.py` | 420 | blank line contains whitespace |
| 2023 | W293 | `opt/netcfg-tui/mock_mode.py` | 417 | blank line contains whitespace |
| 2022 | W293 | `opt/netcfg-tui/mock_mode.py` | 412 | blank line contains whitespace |
| 2021 | W293 | `opt/netcfg-tui/mock_mode.py` | 405 | blank line contains whitespace |
| 2020 | W293 | `opt/netcfg-tui/mock_mode.py` | 396 | blank line contains whitespace |
| 2019 | W293 | `opt/netcfg-tui/mock_mode.py` | 394 | blank line contains whitespace |
| 2018 | W293 | `opt/netcfg-tui/mock_mode.py` | 391 | blank line contains whitespace |
| 2017 | W293 | `opt/netcfg-tui/mock_mode.py` | 386 | blank line contains whitespace |
| 2016 | W293 | `opt/netcfg-tui/mock_mode.py` | 379 | blank line contains whitespace |
| 2015 | W293 | `opt/netcfg-tui/mock_mode.py` | 376 | blank line contains whitespace |
| 2014 | W293 | `opt/netcfg-tui/mock_mode.py` | 371 | blank line contains whitespace |
| 2013 | W293 | `opt/netcfg-tui/mock_mode.py` | 365 | blank line contains whitespace |
| 2012 | W293 | `opt/netcfg-tui/mock_mode.py` | 358 | blank line contains whitespace |
| 2011 | W293 | `opt/netcfg-tui/mock_mode.py` | 353 | blank line contains whitespace |
| 2010 | W293 | `opt/netcfg-tui/mock_mode.py` | 347 | blank line contains whitespace |
| 2009 | W293 | `opt/netcfg-tui/mock_mode.py` | 340 | blank line contains whitespace |
| 2008 | W293 | `opt/netcfg-tui/mock_mode.py` | 338 | blank line contains whitespace |
| 2007 | W293 | `opt/netcfg-tui/mock_mode.py` | 333 | blank line contains whitespace |
| 2006 | W293 | `opt/netcfg-tui/mock_mode.py` | 327 | blank line contains whitespace |
| 2005 | W293 | `opt/netcfg-tui/mock_mode.py` | 320 | blank line contains whitespace |
| 2004 | W293 | `opt/netcfg-tui/mock_mode.py` | 318 | blank line contains whitespace |
| 2003 | W293 | `opt/netcfg-tui/mock_mode.py` | 313 | blank line contains whitespace |
| 2002 | W293 | `opt/netcfg-tui/mock_mode.py` | 309 | blank line contains whitespace |
| 2001 | W293 | `opt/netcfg-tui/mock_mode.py` | 304 | blank line contains whitespace |
| 2000 | W293 | `opt/netcfg-tui/mock_mode.py` | 300 | blank line contains whitespace |
| 1999 | W293 | `opt/netcfg-tui/mock_mode.py` | 295 | blank line contains whitespace |
| 1998 | W293 | `opt/netcfg-tui/mock_mode.py` | 290 | blank line contains whitespace |
| 1997 | W293 | `opt/netcfg-tui/mock_mode.py` | 286 | blank line contains whitespace |
| 1996 | W293 | `opt/netcfg-tui/mock_mode.py` | 283 | blank line contains whitespace |
| 1995 | W293 | `opt/netcfg-tui/mock_mode.py` | 242 | blank line contains whitespace |
| 1994 | W293 | `opt/netcfg-tui/mock_mode.py` | 238 | blank line contains whitespace |
| 1993 | W293 | `opt/netcfg-tui/mock_mode.py` | 229 | blank line contains whitespace |
| 1992 | W293 | `opt/netcfg-tui/mock_mode.py` | 218 | blank line contains whitespace |
| 1991 | W293 | `opt/netcfg-tui/mock_mode.py` | 210 | blank line contains whitespace |
| 1990 | W293 | `opt/netcfg-tui/mock_mode.py` | 206 | blank line contains whitespace |
| 1989 | W293 | `opt/netcfg-tui/mock_mode.py` | 195 | blank line contains whitespace |
| 1988 | W293 | `opt/netcfg-tui/mock_mode.py` | 185 | blank line contains whitespace |
| 1987 | W293 | `opt/netcfg-tui/mock_mode.py` | 171 | blank line contains whitespace |
| 1986 | W293 | `opt/netcfg-tui/mock_mode.py` | 160 | blank line contains whitespace |
| 1985 | W293 | `opt/netcfg-tui/mock_mode.py` | 145 | blank line contains whitespace |
| 1984 | W293 | `opt/netcfg-tui/mock_mode.py` | 134 | blank line contains whitespace |
| 1983 | W293 | `opt/netcfg-tui/mock_mode.py` | 130 | blank line contains whitespace |
| 1982 | W293 | `opt/netcfg-tui/mock_mode.py` | 118 | blank line contains whitespace |
| 1981 | W293 | `opt/netcfg-tui/mock_mode.py` | 113 | blank line contains whitespace |
| 1980 | W293 | `opt/netcfg-tui/mock_mode.py` | 105 | blank line contains whitespace |
| 1979 | W293 | `opt/netcfg-tui/mock_mode.py` | 101 | blank line contains whitespace |
| 1978 | W293 | `opt/netcfg-tui/mock_mode.py` | 95 | blank line contains whitespace |
| 1977 | W293 | `opt/netcfg-tui/mock_mode.py` | 93 | blank line contains whitespace |
| 1976 | W293 | `opt/netcfg-tui/mock_mode.py` | 62 | blank line contains whitespace |
| 1974 | W391 | `opt/netcfg-tui/main.py` | 573 | blank line at end of file |
| 1973 | W293 | `opt/netcfg-tui/main.py` | 567 | blank line contains whitespace |
| 1972 | W293 | `opt/netcfg-tui/main.py` | 562 | blank line contains whitespace |
| 1971 | W293 | `opt/netcfg-tui/main.py` | 556 | blank line contains whitespace |
| 1970 | W293 | `opt/netcfg-tui/main.py` | 547 | blank line contains whitespace |
| 1969 | W293 | `opt/netcfg-tui/main.py` | 543 | blank line contains whitespace |
| 1968 | W293 | `opt/netcfg-tui/main.py` | 540 | blank line contains whitespace |
| 1967 | W293 | `opt/netcfg-tui/main.py` | 536 | blank line contains whitespace |
| 1966 | W293 | `opt/netcfg-tui/main.py` | 531 | blank line contains whitespace |
| 1965 | W293 | `opt/netcfg-tui/main.py` | 529 | blank line contains whitespace |
| 1964 | W293 | `opt/netcfg-tui/main.py` | 527 | blank line contains whitespace |
| 1963 | W293 | `opt/netcfg-tui/main.py` | 496 | blank line contains whitespace |
| 1962 | W293 | `opt/netcfg-tui/main.py` | 494 | blank line contains whitespace |
| 1961 | W293 | `opt/netcfg-tui/main.py` | 489 | blank line contains whitespace |
| 1960 | W293 | `opt/netcfg-tui/main.py` | 485 | blank line contains whitespace |
| 1959 | W293 | `opt/netcfg-tui/main.py` | 479 | blank line contains whitespace |
| 1958 | W293 | `opt/netcfg-tui/main.py` | 474 | blank line contains whitespace |
| 1957 | W293 | `opt/netcfg-tui/main.py` | 470 | blank line contains whitespace |
| 1956 | W293 | `opt/netcfg-tui/main.py` | 464 | blank line contains whitespace |
| 1955 | W293 | `opt/netcfg-tui/main.py` | 459 | blank line contains whitespace |
| 1954 | W293 | `opt/netcfg-tui/main.py` | 454 | blank line contains whitespace |
| 1953 | W293 | `opt/netcfg-tui/main.py` | 448 | blank line contains whitespace |
| 1952 | W293 | `opt/netcfg-tui/main.py` | 442 | blank line contains whitespace |
| 1951 | W293 | `opt/netcfg-tui/main.py` | 439 | blank line contains whitespace |
| 1950 | W293 | `opt/netcfg-tui/main.py` | 418 | blank line contains whitespace |
| 1949 | W293 | `opt/netcfg-tui/main.py` | 407 | blank line contains whitespace |
| 1948 | W293 | `opt/netcfg-tui/main.py` | 395 | blank line contains whitespace |
| 1947 | W293 | `opt/netcfg-tui/main.py` | 390 | blank line contains whitespace |
| 1946 | W293 | `opt/netcfg-tui/main.py` | 384 | blank line contains whitespace |
| 1945 | W293 | `opt/netcfg-tui/main.py` | 374 | blank line contains whitespace |
| 1944 | W293 | `opt/netcfg-tui/main.py` | 368 | blank line contains whitespace |
| 1943 | W293 | `opt/netcfg-tui/main.py` | 357 | blank line contains whitespace |
| 1942 | W293 | `opt/netcfg-tui/main.py` | 328 | blank line contains whitespace |
| 1941 | W293 | `opt/netcfg-tui/main.py` | 326 | blank line contains whitespace |
| 1940 | W293 | `opt/netcfg-tui/main.py` | 319 | blank line contains whitespace |
| 1939 | W293 | `opt/netcfg-tui/main.py` | 315 | blank line contains whitespace |
| 1938 | W293 | `opt/netcfg-tui/main.py` | 310 | blank line contains whitespace |
| 1937 | W293 | `opt/netcfg-tui/main.py` | 305 | blank line contains whitespace |
| 1936 | W293 | `opt/netcfg-tui/main.py` | 302 | blank line contains whitespace |
| 1935 | W293 | `opt/netcfg-tui/main.py` | 293 | blank line contains whitespace |
| 1934 | W293 | `opt/netcfg-tui/main.py` | 290 | blank line contains whitespace |
| 1933 | W293 | `opt/netcfg-tui/main.py` | 285 | blank line contains whitespace |
| 1932 | W293 | `opt/netcfg-tui/main.py` | 272 | blank line contains whitespace |
| 1931 | W293 | `opt/netcfg-tui/main.py` | 265 | blank line contains whitespace |
| 1930 | W293 | `opt/netcfg-tui/main.py` | 262 | blank line contains whitespace |
| 1929 | W293 | `opt/netcfg-tui/main.py` | 253 | blank line contains whitespace |
| 1928 | W293 | `opt/netcfg-tui/main.py` | 250 | blank line contains whitespace |
| 1927 | W293 | `opt/netcfg-tui/main.py` | 248 | blank line contains whitespace |
| 1926 | W293 | `opt/netcfg-tui/main.py` | 235 | blank line contains whitespace |
| 1925 | W293 | `opt/netcfg-tui/main.py` | 232 | blank line contains whitespace |
| 1924 | W293 | `opt/netcfg-tui/main.py` | 213 | blank line contains whitespace |
| 1923 | W291 | `opt/netcfg-tui/main.py` | 209 | trailing whitespace |
| 1922 | W293 | `opt/netcfg-tui/main.py` | 205 | blank line contains whitespace |
| 1921 | W293 | `opt/netcfg-tui/main.py` | 188 | blank line contains whitespace |
| 1920 | W293 | `opt/netcfg-tui/main.py` | 179 | blank line contains whitespace |
| 1919 | W293 | `opt/netcfg-tui/main.py` | 172 | blank line contains whitespace |
| 1918 | W293 | `opt/netcfg-tui/main.py` | 160 | blank line contains whitespace |
| 1917 | W293 | `opt/netcfg-tui/main.py` | 147 | blank line contains whitespace |
| 1916 | W293 | `opt/netcfg-tui/main.py` | 114 | blank line contains whitespace |
| 1915 | W293 | `opt/netcfg-tui/main.py` | 99 | blank line contains whitespace |
| 1914 | W293 | `opt/netcfg-tui/main.py` | 79 | blank line contains whitespace |
| 1913 | W293 | `opt/netcfg-tui/main.py` | 59 | blank line contains whitespace |
| 1908 | W293 | `opt/models/phase4_models.py` | 395 | blank line contains whitespace |
| 1907 | W293 | `opt/models/phase4_models.py` | 392 | blank line contains whitespace |
| 1906 | W293 | `opt/models/phase4_models.py` | 387 | blank line contains whitespace |
| 1905 | W293 | `opt/models/phase4_models.py` | 384 | blank line contains whitespace |
| 1904 | W293 | `opt/models/phase4_models.py` | 380 | blank line contains whitespace |
| 1903 | W293 | `opt/models/phase4_models.py` | 376 | blank line contains whitespace |
| 1902 | W293 | `opt/models/phase4_models.py` | 373 | blank line contains whitespace |
| 1901 | W293 | `opt/models/phase4_models.py` | 371 | blank line contains whitespace |
| 1900 | W293 | `opt/models/phase4_models.py` | 359 | blank line contains whitespace |
| 1899 | W293 | `opt/models/phase4_models.py` | 356 | blank line contains whitespace |
| 1898 | W293 | `opt/models/phase4_models.py` | 352 | blank line contains whitespace |
| 1897 | W293 | `opt/models/phase4_models.py` | 348 | blank line contains whitespace |
| 1896 | W293 | `opt/models/phase4_models.py` | 343 | blank line contains whitespace |
| 1895 | W293 | `opt/models/phase4_models.py` | 340 | blank line contains whitespace |
| 1894 | W293 | `opt/models/phase4_models.py` | 338 | blank line contains whitespace |
| 1893 | W293 | `opt/models/phase4_models.py` | 328 | blank line contains whitespace |
| 1892 | W293 | `opt/models/phase4_models.py` | 325 | blank line contains whitespace |
| 1891 | W293 | `opt/models/phase4_models.py` | 321 | blank line contains whitespace |
| 1890 | W293 | `opt/models/phase4_models.py` | 318 | blank line contains whitespace |
| 1889 | W293 | `opt/models/phase4_models.py` | 314 | blank line contains whitespace |
| 1888 | W293 | `opt/models/phase4_models.py` | 311 | blank line contains whitespace |
| 1887 | W293 | `opt/models/phase4_models.py` | 303 | blank line contains whitespace |
| 1886 | W293 | `opt/models/phase4_models.py` | 300 | blank line contains whitespace |
| 1885 | W293 | `opt/models/phase4_models.py` | 298 | blank line contains whitespace |
| 1884 | W293 | `opt/models/phase4_models.py` | 287 | blank line contains whitespace |
| 1883 | W293 | `opt/models/phase4_models.py` | 280 | blank line contains whitespace |
| 1882 | W293 | `opt/models/phase4_models.py` | 276 | blank line contains whitespace |
| 1881 | W293 | `opt/models/phase4_models.py` | 271 | blank line contains whitespace |
| 1880 | W293 | `opt/models/phase4_models.py` | 268 | blank line contains whitespace |
| 1879 | W293 | `opt/models/phase4_models.py` | 263 | blank line contains whitespace |
| 1878 | W293 | `opt/models/phase4_models.py` | 259 | blank line contains whitespace |
| 1877 | W293 | `opt/models/phase4_models.py` | 255 | blank line contains whitespace |
| 1876 | W293 | `opt/models/phase4_models.py` | 251 | blank line contains whitespace |
| 1875 | W293 | `opt/models/phase4_models.py` | 246 | blank line contains whitespace |
| 1874 | W293 | `opt/models/phase4_models.py` | 243 | blank line contains whitespace |
| 1873 | W293 | `opt/models/phase4_models.py` | 241 | blank line contains whitespace |
| 1872 | W293 | `opt/models/phase4_models.py` | 232 | blank line contains whitespace |
| 1871 | W293 | `opt/models/phase4_models.py` | 228 | blank line contains whitespace |
| 1870 | W293 | `opt/models/phase4_models.py` | 224 | blank line contains whitespace |
| 1869 | W293 | `opt/models/phase4_models.py` | 218 | blank line contains whitespace |
| 1868 | W293 | `opt/models/phase4_models.py` | 214 | blank line contains whitespace |
| 1867 | W293 | `opt/models/phase4_models.py` | 211 | blank line contains whitespace |
| 1866 | W293 | `opt/models/phase4_models.py` | 208 | blank line contains whitespace |
| 1865 | W293 | `opt/models/phase4_models.py` | 206 | blank line contains whitespace |
| 1864 | W293 | `opt/models/phase4_models.py` | 195 | blank line contains whitespace |
| 1863 | W293 | `opt/models/phase4_models.py` | 192 | blank line contains whitespace |
| 1862 | W293 | `opt/models/phase4_models.py` | 189 | blank line contains whitespace |
| 1861 | W293 | `opt/models/phase4_models.py` | 185 | blank line contains whitespace |
| 1860 | W293 | `opt/models/phase4_models.py` | 180 | blank line contains whitespace |
| 1859 | W293 | `opt/models/phase4_models.py` | 172 | blank line contains whitespace |
| 1858 | W293 | `opt/models/phase4_models.py` | 169 | blank line contains whitespace |
| 1857 | W293 | `opt/models/phase4_models.py` | 167 | blank line contains whitespace |
| 1856 | W293 | `opt/models/phase4_models.py` | 157 | blank line contains whitespace |
| 1855 | W293 | `opt/models/phase4_models.py` | 154 | blank line contains whitespace |
| 1854 | W293 | `opt/models/phase4_models.py` | 150 | blank line contains whitespace |
| 1853 | W293 | `opt/models/phase4_models.py` | 146 | blank line contains whitespace |
| 1852 | W293 | `opt/models/phase4_models.py` | 142 | blank line contains whitespace |
| 1851 | W293 | `opt/models/phase4_models.py` | 137 | blank line contains whitespace |
| 1850 | W293 | `opt/models/phase4_models.py` | 129 | blank line contains whitespace |
| 1849 | W293 | `opt/models/phase4_models.py` | 126 | blank line contains whitespace |
| 1848 | W293 | `opt/models/phase4_models.py` | 124 | blank line contains whitespace |
| 1847 | W293 | `opt/models/phase4_models.py` | 113 | blank line contains whitespace |
| 1846 | W293 | `opt/models/phase4_models.py` | 110 | blank line contains whitespace |
| 1845 | W293 | `opt/models/phase4_models.py` | 106 | blank line contains whitespace |
| 1844 | W293 | `opt/models/phase4_models.py` | 101 | blank line contains whitespace |
| 1843 | W293 | `opt/models/phase4_models.py` | 93 | blank line contains whitespace |
| 1842 | W293 | `opt/models/phase4_models.py` | 90 | blank line contains whitespace |
| 1841 | W293 | `opt/models/phase4_models.py` | 88 | blank line contains whitespace |
| 1840 | W293 | `opt/models/phase4_models.py` | 78 | blank line contains whitespace |
| 1839 | W293 | `opt/models/phase4_models.py` | 61 | blank line contains whitespace |
| 1838 | W293 | `opt/models/phase4_models.py` | 56 | blank line contains whitespace |
| 1837 | W293 | `opt/models/phase4_models.py` | 53 | blank line contains whitespace |
| 1836 | W293 | `opt/models/phase4_models.py` | 50 | blank line contains whitespace |
| 1835 | W293 | `opt/models/phase4_models.py` | 45 | blank line contains whitespace |
| 1834 | W293 | `opt/models/phase4_models.py` | 42 | blank line contains whitespace |
| 1833 | W293 | `opt/models/phase4_models.py` | 39 | blank line contains whitespace |
| 1832 | W293 | `opt/models/phase4_models.py` | 37 | blank line contains whitespace |
| 1830 | W293 | `opt/models/migrations.py` | 357 | blank line contains whitespace |
| 1829 | W293 | `opt/models/migrations.py` | 348 | blank line contains whitespace |
| 1828 | W293 | `opt/models/migrations.py` | 338 | blank line contains whitespace |
| 1826 | W293 | `opt/models/migrations.py` | 327 | blank line contains whitespace |
| 1825 | W293 | `opt/models/migrations.py` | 322 | blank line contains whitespace |
| 1824 | W293 | `opt/models/migrations.py` | 317 | blank line contains whitespace |
| 1823 | W293 | `opt/models/migrations.py` | 310 | blank line contains whitespace |
| 1822 | W293 | `opt/models/migrations.py` | 304 | blank line contains whitespace |
| 1821 | W293 | `opt/models/migrations.py` | 300 | blank line contains whitespace |
| 1820 | W293 | `opt/models/migrations.py` | 298 | blank line contains whitespace |
| 1819 | W293 | `opt/models/migrations.py` | 293 | blank line contains whitespace |
| 1818 | W293 | `opt/models/migrations.py` | 251 | blank line contains whitespace |
| 1817 | W293 | `opt/models/migrations.py` | 230 | blank line contains whitespace |
| 1816 | W293 | `opt/models/migrations.py` | 222 | blank line contains whitespace |
| 1815 | W293 | `opt/models/migrations.py` | 219 | blank line contains whitespace |
| 1814 | W293 | `opt/models/migrations.py` | 217 | blank line contains whitespace |
| 1813 | W293 | `opt/models/migrations.py` | 209 | blank line contains whitespace |
| 1812 | W293 | `opt/models/migrations.py` | 206 | blank line contains whitespace |
| 1811 | W293 | `opt/models/migrations.py` | 197 | blank line contains whitespace |
| 1810 | W293 | `opt/models/migrations.py` | 194 | blank line contains whitespace |
| 1809 | W293 | `opt/models/migrations.py` | 192 | blank line contains whitespace |
| 1808 | W293 | `opt/models/migrations.py` | 184 | blank line contains whitespace |
| 1807 | W293 | `opt/models/migrations.py` | 182 | blank line contains whitespace |
| 1806 | W293 | `opt/models/migrations.py` | 172 | blank line contains whitespace |
| 1805 | W293 | `opt/models/migrations.py` | 167 | blank line contains whitespace |
| 1804 | W293 | `opt/models/migrations.py` | 164 | blank line contains whitespace |
| 1803 | W293 | `opt/models/migrations.py` | 145 | blank line contains whitespace |
| 1802 | W293 | `opt/models/migrations.py` | 135 | blank line contains whitespace |
| 1801 | W293 | `opt/models/migrations.py` | 127 | blank line contains whitespace |
| 1800 | W293 | `opt/models/migrations.py` | 120 | blank line contains whitespace |
| 1799 | W293 | `opt/models/migrations.py` | 111 | blank line contains whitespace |
| 1798 | W293 | `opt/models/migrations.py` | 102 | blank line contains whitespace |
| 1797 | W293 | `opt/models/migrations.py` | 93 | blank line contains whitespace |
| 1796 | W293 | `opt/models/migrations.py` | 85 | blank line contains whitespace |
| 1795 | W293 | `opt/models/migrations.py` | 77 | blank line contains whitespace |
| 1794 | W293 | `opt/models/migrations.py` | 69 | blank line contains whitespace |
| 1793 | W293 | `opt/models/migrations.py` | 61 | blank line contains whitespace |
| 1792 | W293 | `opt/models/migrations.py` | 53 | blank line contains whitespace |
| 1791 | W293 | `opt/models/migrations.py` | 43 | blank line contains whitespace |
| 1773 | W293 | `opt/installer/install_profile_logger.py` | 797 | blank line contains whitespace |
| 1772 | W293 | `opt/installer/install_profile_logger.py` | 781 | blank line contains whitespace |
| 1771 | W293 | `opt/installer/install_profile_logger.py` | 772 | blank line contains whitespace |
| 1770 | W293 | `opt/installer/install_profile_logger.py` | 767 | blank line contains whitespace |
| 1769 | W293 | `opt/installer/install_profile_logger.py` | 758 | blank line contains whitespace |
| 1768 | W293 | `opt/installer/install_profile_logger.py` | 756 | blank line contains whitespace |
| 1767 | W293 | `opt/installer/install_profile_logger.py` | 752 | blank line contains whitespace |
| 1766 | W293 | `opt/installer/install_profile_logger.py` | 749 | blank line contains whitespace |
| 1765 | W293 | `opt/installer/install_profile_logger.py` | 746 | blank line contains whitespace |
| 1764 | W293 | `opt/installer/install_profile_logger.py` | 739 | blank line contains whitespace |
| 1763 | W293 | `opt/installer/install_profile_logger.py` | 737 | blank line contains whitespace |
| 1762 | W293 | `opt/installer/install_profile_logger.py` | 732 | blank line contains whitespace |
| 1761 | W293 | `opt/installer/install_profile_logger.py` | 715 | blank line contains whitespace |
| 1760 | W293 | `opt/installer/install_profile_logger.py` | 708 | blank line contains whitespace |
| 1759 | W293 | `opt/installer/install_profile_logger.py` | 705 | blank line contains whitespace |
| 1758 | W293 | `opt/installer/install_profile_logger.py` | 683 | blank line contains whitespace |
| 1757 | W293 | `opt/installer/install_profile_logger.py` | 631 | blank line contains whitespace |
| 1756 | W293 | `opt/installer/install_profile_logger.py` | 621 | blank line contains whitespace |
| 1755 | W293 | `opt/installer/install_profile_logger.py` | 611 | blank line contains whitespace |
| 1754 | W293 | `opt/installer/install_profile_logger.py` | 598 | blank line contains whitespace |
| 1753 | W293 | `opt/installer/install_profile_logger.py` | 594 | blank line contains whitespace |
| 1752 | W293 | `opt/installer/install_profile_logger.py` | 586 | blank line contains whitespace |
| 1751 | W293 | `opt/installer/install_profile_logger.py` | 581 | blank line contains whitespace |
| 1750 | W293 | `opt/installer/install_profile_logger.py` | 576 | blank line contains whitespace |
| 1749 | W293 | `opt/installer/install_profile_logger.py` | 572 | blank line contains whitespace |
| 1748 | W293 | `opt/installer/install_profile_logger.py` | 567 | blank line contains whitespace |
| 1747 | W293 | `opt/installer/install_profile_logger.py` | 560 | blank line contains whitespace |
| 1746 | W293 | `opt/installer/install_profile_logger.py` | 556 | blank line contains whitespace |
| 1745 | W293 | `opt/installer/install_profile_logger.py` | 552 | blank line contains whitespace |
| 1744 | W293 | `opt/installer/install_profile_logger.py` | 548 | blank line contains whitespace |
| 1743 | W293 | `opt/installer/install_profile_logger.py` | 544 | blank line contains whitespace |
| 1742 | W293 | `opt/installer/install_profile_logger.py` | 537 | blank line contains whitespace |
| 1741 | W293 | `opt/installer/install_profile_logger.py` | 531 | blank line contains whitespace |
| 1740 | W293 | `opt/installer/install_profile_logger.py` | 524 | blank line contains whitespace |
| 1739 | W293 | `opt/installer/install_profile_logger.py` | 517 | blank line contains whitespace |
| 1738 | W293 | `opt/installer/install_profile_logger.py` | 511 | blank line contains whitespace |
| 1737 | W293 | `opt/installer/install_profile_logger.py` | 507 | blank line contains whitespace |
| 1736 | W293 | `opt/installer/install_profile_logger.py` | 493 | blank line contains whitespace |
| 1735 | W293 | `opt/installer/install_profile_logger.py` | 491 | blank line contains whitespace |
| 1734 | W293 | `opt/installer/install_profile_logger.py` | 483 | blank line contains whitespace |
| 1733 | W293 | `opt/installer/install_profile_logger.py` | 481 | blank line contains whitespace |
| 1732 | W293 | `opt/installer/install_profile_logger.py` | 474 | blank line contains whitespace |
| 1731 | W293 | `opt/installer/install_profile_logger.py` | 465 | blank line contains whitespace |
| 1730 | W293 | `opt/installer/install_profile_logger.py` | 443 | blank line contains whitespace |
| 1729 | W293 | `opt/installer/install_profile_logger.py` | 438 | blank line contains whitespace |
| 1728 | W293 | `opt/installer/install_profile_logger.py` | 435 | blank line contains whitespace |
| 1727 | W293 | `opt/installer/install_profile_logger.py` | 427 | blank line contains whitespace |
| 1726 | W293 | `opt/installer/install_profile_logger.py` | 422 | blank line contains whitespace |
| 1725 | W293 | `opt/installer/install_profile_logger.py` | 411 | blank line contains whitespace |
| 1724 | W293 | `opt/installer/install_profile_logger.py` | 389 | blank line contains whitespace |
| 1723 | W293 | `opt/installer/install_profile_logger.py` | 376 | blank line contains whitespace |
| 1722 | W293 | `opt/installer/install_profile_logger.py` | 362 | blank line contains whitespace |
| 1721 | W293 | `opt/installer/install_profile_logger.py` | 350 | blank line contains whitespace |
| 1720 | W293 | `opt/installer/install_profile_logger.py` | 348 | blank line contains whitespace |
| 1719 | W293 | `opt/installer/install_profile_logger.py` | 345 | blank line contains whitespace |
| 1718 | W293 | `opt/installer/install_profile_logger.py` | 342 | blank line contains whitespace |
| 1717 | W293 | `opt/installer/install_profile_logger.py` | 339 | blank line contains whitespace |
| 1716 | W293 | `opt/installer/install_profile_logger.py` | 331 | blank line contains whitespace |
| 1715 | W293 | `opt/installer/install_profile_logger.py` | 323 | blank line contains whitespace |
| 1714 | W293 | `opt/installer/install_profile_logger.py` | 320 | blank line contains whitespace |
| 1713 | W293 | `opt/installer/install_profile_logger.py` | 314 | blank line contains whitespace |
| 1712 | W293 | `opt/installer/install_profile_logger.py` | 308 | blank line contains whitespace |
| 1711 | W293 | `opt/installer/install_profile_logger.py` | 302 | blank line contains whitespace |
| 1710 | W293 | `opt/installer/install_profile_logger.py` | 296 | blank line contains whitespace |
| 1709 | W293 | `opt/installer/install_profile_logger.py` | 288 | blank line contains whitespace |
| 1708 | W293 | `opt/installer/install_profile_logger.py` | 286 | blank line contains whitespace |
| 1707 | W293 | `opt/installer/install_profile_logger.py` | 282 | blank line contains whitespace |
| 1706 | W293 | `opt/installer/install_profile_logger.py` | 278 | blank line contains whitespace |
| 1705 | W293 | `opt/installer/install_profile_logger.py` | 275 | blank line contains whitespace |
| 1704 | W293 | `opt/installer/install_profile_logger.py` | 270 | blank line contains whitespace |
| 1703 | W293 | `opt/installer/install_profile_logger.py` | 265 | blank line contains whitespace |
| 1702 | W293 | `opt/installer/install_profile_logger.py` | 261 | blank line contains whitespace |
| 1701 | W293 | `opt/installer/install_profile_logger.py` | 254 | blank line contains whitespace |
| 1700 | W293 | `opt/installer/install_profile_logger.py` | 250 | blank line contains whitespace |
| 1699 | W293 | `opt/installer/install_profile_logger.py` | 244 | blank line contains whitespace |
| 1698 | W293 | `opt/installer/install_profile_logger.py` | 240 | blank line contains whitespace |
| 1697 | W293 | `opt/installer/install_profile_logger.py` | 232 | blank line contains whitespace |
| 1696 | W293 | `opt/installer/install_profile_logger.py` | 220 | blank line contains whitespace |
| 1695 | W293 | `opt/installer/install_profile_logger.py` | 212 | blank line contains whitespace |
| 1694 | W293 | `opt/installer/install_profile_logger.py` | 207 | blank line contains whitespace |
| 1693 | W293 | `opt/installer/install_profile_logger.py` | 201 | blank line contains whitespace |
| 1692 | W293 | `opt/installer/install_profile_logger.py` | 190 | blank line contains whitespace |
| 1691 | W293 | `opt/installer/install_profile_logger.py` | 186 | blank line contains whitespace |
| 1690 | W293 | `opt/installer/install_profile_logger.py` | 172 | blank line contains whitespace |
| 1689 | W293 | `opt/installer/install_profile_logger.py` | 167 | blank line contains whitespace |
| 1688 | W293 | `opt/installer/install_profile_logger.py` | 162 | blank line contains whitespace |
| 1687 | W293 | `opt/installer/install_profile_logger.py` | 158 | blank line contains whitespace |
| 1686 | W293 | `opt/installer/install_profile_logger.py` | 155 | blank line contains whitespace |
| 1685 | W293 | `opt/installer/install_profile_logger.py` | 150 | blank line contains whitespace |
| 1684 | W293 | `opt/installer/install_profile_logger.py` | 147 | blank line contains whitespace |
| 1683 | W293 | `opt/installer/install_profile_logger.py` | 142 | blank line contains whitespace |
| 1672 | W291 | `opt/hvctl_enhanced.py` | 745 | trailing whitespace |
| 1671 | W293 | `opt/hvctl_enhanced.py` | 683 | blank line contains whitespace |
| 1670 | W293 | `opt/hvctl_enhanced.py` | 676 | blank line contains whitespace |
| 1669 | W293 | `opt/hvctl_enhanced.py` | 660 | blank line contains whitespace |
| 1668 | W293 | `opt/hvctl_enhanced.py` | 658 | blank line contains whitespace |
| 1667 | W293 | `opt/hvctl_enhanced.py` | 654 | blank line contains whitespace |
| 1666 | W293 | `opt/hvctl_enhanced.py` | 648 | blank line contains whitespace |
| 1665 | W293 | `opt/hvctl_enhanced.py` | 644 | blank line contains whitespace |
| 1664 | W293 | `opt/hvctl_enhanced.py` | 641 | blank line contains whitespace |
| 1662 | W293 | `opt/hvctl_enhanced.py` | 619 | blank line contains whitespace |
| 1659 | W293 | `opt/hvctl_enhanced.py` | 406 | blank line contains whitespace |
| 1657 | W293 | `opt/hvctl_enhanced.py` | 360 | blank line contains whitespace |
| 1654 | W293 | `opt/hvctl_enhanced.py` | 342 | blank line contains whitespace |
| 1653 | W293 | `opt/hvctl_enhanced.py` | 324 | blank line contains whitespace |
| 1652 | W293 | `opt/hvctl_enhanced.py` | 317 | blank line contains whitespace |
| 1651 | W293 | `opt/hvctl_enhanced.py` | 285 | blank line contains whitespace |
| 1650 | W293 | `opt/hvctl_enhanced.py` | 272 | blank line contains whitespace |
| 1649 | W293 | `opt/hvctl_enhanced.py` | 268 | blank line contains whitespace |
| 1648 | W293 | `opt/hvctl_enhanced.py` | 265 | blank line contains whitespace |
| 1647 | W293 | `opt/hvctl_enhanced.py` | 262 | blank line contains whitespace |
| 1646 | W293 | `opt/hvctl_enhanced.py` | 259 | blank line contains whitespace |
| 1645 | W293 | `opt/helpers/standardization.py` | 600 | blank line contains whitespace |
| 1644 | W293 | `opt/helpers/standardization.py` | 596 | blank line contains whitespace |
| 1643 | W293 | `opt/helpers/standardization.py` | 588 | blank line contains whitespace |
| 1642 | W293 | `opt/helpers/standardization.py` | 583 | blank line contains whitespace |
| 1641 | W293 | `opt/helpers/standardization.py` | 579 | blank line contains whitespace |
| 1640 | W293 | `opt/helpers/standardization.py` | 575 | blank line contains whitespace |
| 1639 | W293 | `opt/helpers/standardization.py` | 563 | blank line contains whitespace |
| 1638 | W293 | `opt/helpers/standardization.py` | 560 | blank line contains whitespace |
| 1637 | W293 | `opt/helpers/standardization.py` | 556 | blank line contains whitespace |
| 1636 | W293 | `opt/helpers/standardization.py` | 554 | blank line contains whitespace |
| 1635 | W293 | `opt/helpers/standardization.py` | 549 | blank line contains whitespace |
| 1634 | W293 | `opt/helpers/standardization.py` | 544 | blank line contains whitespace |
| 1633 | W293 | `opt/helpers/standardization.py` | 542 | blank line contains whitespace |
| 1632 | W293 | `opt/helpers/standardization.py` | 536 | blank line contains whitespace |
| 1631 | W293 | `opt/helpers/standardization.py` | 531 | blank line contains whitespace |
| 1630 | W293 | `opt/helpers/standardization.py` | 521 | blank line contains whitespace |
| 1629 | W293 | `opt/helpers/standardization.py` | 518 | blank line contains whitespace |
| 1628 | W293 | `opt/helpers/standardization.py` | 512 | blank line contains whitespace |
| 1627 | W293 | `opt/helpers/standardization.py` | 508 | blank line contains whitespace |
| 1626 | W293 | `opt/helpers/standardization.py` | 502 | blank line contains whitespace |
| 1625 | W293 | `opt/helpers/standardization.py` | 499 | blank line contains whitespace |
| 1624 | W293 | `opt/helpers/standardization.py` | 488 | blank line contains whitespace |
| 1623 | W293 | `opt/helpers/standardization.py` | 481 | blank line contains whitespace |
| 1622 | W293 | `opt/helpers/standardization.py` | 471 | blank line contains whitespace |
| 1621 | W293 | `opt/helpers/standardization.py` | 467 | blank line contains whitespace |
| 1620 | W293 | `opt/helpers/standardization.py` | 458 | blank line contains whitespace |
| 1619 | W293 | `opt/helpers/standardization.py` | 456 | blank line contains whitespace |
| 1618 | W293 | `opt/helpers/standardization.py` | 451 | blank line contains whitespace |
| 1617 | W293 | `opt/helpers/standardization.py` | 449 | blank line contains whitespace |
| 1616 | W293 | `opt/helpers/standardization.py` | 440 | blank line contains whitespace |
| 1615 | W293 | `opt/helpers/standardization.py` | 436 | blank line contains whitespace |
| 1614 | W293 | `opt/helpers/standardization.py` | 431 | blank line contains whitespace |
| 1613 | W293 | `opt/helpers/standardization.py` | 426 | blank line contains whitespace |
| 1612 | W293 | `opt/helpers/standardization.py` | 418 | blank line contains whitespace |
| 1611 | W293 | `opt/helpers/standardization.py` | 406 | blank line contains whitespace |
| 1610 | W293 | `opt/helpers/standardization.py` | 385 | blank line contains whitespace |
| 1609 | W293 | `opt/helpers/standardization.py` | 374 | blank line contains whitespace |
| 1608 | W293 | `opt/helpers/standardization.py` | 369 | blank line contains whitespace |
| 1607 | W293 | `opt/helpers/standardization.py` | 366 | blank line contains whitespace |
| 1606 | W293 | `opt/helpers/standardization.py` | 362 | blank line contains whitespace |
| 1605 | W293 | `opt/helpers/standardization.py` | 351 | blank line contains whitespace |
| 1604 | W293 | `opt/helpers/standardization.py` | 342 | blank line contains whitespace |
| 1603 | W293 | `opt/helpers/standardization.py` | 334 | blank line contains whitespace |
| 1602 | W293 | `opt/helpers/standardization.py` | 327 | blank line contains whitespace |
| 1601 | W293 | `opt/helpers/standardization.py` | 322 | blank line contains whitespace |
| 1600 | W293 | `opt/helpers/standardization.py` | 319 | blank line contains whitespace |
| 1599 | W293 | `opt/helpers/standardization.py` | 308 | blank line contains whitespace |
| 1598 | W293 | `opt/helpers/standardization.py` | 306 | blank line contains whitespace |
| 1597 | W293 | `opt/helpers/standardization.py` | 294 | blank line contains whitespace |
| 1596 | W293 | `opt/helpers/standardization.py` | 288 | blank line contains whitespace |
| 1595 | W293 | `opt/helpers/standardization.py` | 283 | blank line contains whitespace |
| 1594 | W293 | `opt/helpers/standardization.py` | 280 | blank line contains whitespace |
| 1593 | W293 | `opt/helpers/standardization.py` | 275 | blank line contains whitespace |
| 1592 | W293 | `opt/helpers/standardization.py` | 266 | blank line contains whitespace |
| 1591 | W293 | `opt/helpers/standardization.py` | 261 | blank line contains whitespace |
| 1590 | W293 | `opt/helpers/standardization.py` | 257 | blank line contains whitespace |
| 1589 | W293 | `opt/helpers/standardization.py` | 251 | blank line contains whitespace |
| 1588 | W293 | `opt/helpers/standardization.py` | 244 | blank line contains whitespace |
| 1587 | W293 | `opt/helpers/standardization.py` | 240 | blank line contains whitespace |
| 1586 | W293 | `opt/helpers/standardization.py` | 235 | blank line contains whitespace |
| 1585 | W293 | `opt/helpers/standardization.py` | 231 | blank line contains whitespace |
| 1584 | W293 | `opt/helpers/standardization.py` | 227 | blank line contains whitespace |
| 1583 | W293 | `opt/helpers/standardization.py` | 223 | blank line contains whitespace |
| 1582 | W293 | `opt/helpers/standardization.py` | 218 | blank line contains whitespace |
| 1581 | W293 | `opt/helpers/standardization.py` | 216 | blank line contains whitespace |
| 1580 | W293 | `opt/helpers/standardization.py` | 211 | blank line contains whitespace |
| 1579 | W293 | `opt/helpers/standardization.py` | 208 | blank line contains whitespace |
| 1578 | W293 | `opt/helpers/standardization.py` | 203 | blank line contains whitespace |
| 1577 | W293 | `opt/helpers/standardization.py` | 200 | blank line contains whitespace |
| 1576 | W293 | `opt/helpers/standardization.py` | 196 | blank line contains whitespace |
| 1575 | W293 | `opt/helpers/standardization.py` | 194 | blank line contains whitespace |
| 1574 | W293 | `opt/helpers/standardization.py` | 189 | blank line contains whitespace |
| 1573 | W293 | `opt/helpers/standardization.py` | 185 | blank line contains whitespace |
| 1572 | W293 | `opt/helpers/standardization.py` | 179 | blank line contains whitespace |
| 1571 | W293 | `opt/helpers/standardization.py` | 176 | blank line contains whitespace |
| 1570 | W293 | `opt/helpers/standardization.py` | 168 | blank line contains whitespace |
| 1569 | W293 | `opt/helpers/standardization.py` | 166 | blank line contains whitespace |
| 1568 | W293 | `opt/helpers/standardization.py` | 159 | blank line contains whitespace |
| 1567 | W293 | `opt/helpers/standardization.py` | 151 | blank line contains whitespace |
| 1566 | W293 | `opt/helpers/standardization.py` | 149 | blank line contains whitespace |
| 1565 | W293 | `opt/helpers/standardization.py` | 135 | blank line contains whitespace |
| 1564 | W293 | `opt/helpers/standardization.py` | 126 | blank line contains whitespace |
| 1563 | W293 | `opt/helpers/standardization.py` | 113 | blank line contains whitespace |
| 1562 | W293 | `opt/helpers/standardization.py` | 107 | blank line contains whitespace |
| 1561 | W293 | `opt/helpers/standardization.py` | 103 | blank line contains whitespace |
| 1560 | W293 | `opt/helpers/standardization.py` | 84 | blank line contains whitespace |
| 1559 | W293 | `opt/helpers/standardization.py` | 75 | blank line contains whitespace |
| 1558 | W293 | `opt/helpers/standardization.py` | 69 | blank line contains whitespace |
| 1557 | W293 | `opt/helpers/standardization.py` | 60 | blank line contains whitespace |
| 1556 | W293 | `opt/helpers/standardization.py` | 50 | blank line contains whitespace |
| 1555 | W293 | `opt/helpers/standardization.py` | 41 | blank line contains whitespace |
| 1554 | W293 | `opt/helpers/standardization.py` | 32 | blank line contains whitespace |
| 1547 | W291 | `opt/graphql_api.py` | 993 | trailing whitespace |
| 1546 | W291 | `opt/graphql_api.py` | 989 | trailing whitespace |
| 1545 | W293 | `opt/graphql_api.py` | 983 | blank line contains whitespace |
| 1544 | W293 | `opt/graphql_api.py` | 970 | blank line contains whitespace |
| 1543 | W293 | `opt/graphql_api.py` | 962 | blank line contains whitespace |
| 1542 | W293 | `opt/graphql_api.py` | 955 | blank line contains whitespace |
| 1541 | W293 | `opt/graphql_api.py` | 952 | blank line contains whitespace |
| 1540 | W291 | `opt/graphql_api.py` | 947 | trailing whitespace |
| 1539 | W293 | `opt/graphql_api.py` | 945 | blank line contains whitespace |
| 1538 | W293 | `opt/graphql_api.py` | 940 | blank line contains whitespace |
| 1537 | W293 | `opt/graphql_api.py` | 933 | blank line contains whitespace |
| 1536 | W293 | `opt/graphql_api.py` | 929 | blank line contains whitespace |
| 1535 | W291 | `opt/graphql_api.py` | 924 | trailing whitespace |
| 1534 | W291 | `opt/graphql_api.py` | 923 | trailing whitespace |
| 1533 | W293 | `opt/graphql_api.py` | 921 | blank line contains whitespace |
| 1532 | W293 | `opt/graphql_api.py` | 919 | blank line contains whitespace |
| 1531 | W293 | `opt/graphql_api.py` | 910 | blank line contains whitespace |
| 1530 | W293 | `opt/graphql_api.py` | 904 | blank line contains whitespace |
| 1529 | W293 | `opt/graphql_api.py` | 898 | blank line contains whitespace |
| 1528 | W293 | `opt/graphql_api.py` | 894 | blank line contains whitespace |
| 1527 | W293 | `opt/graphql_api.py` | 890 | blank line contains whitespace |
| 1526 | W293 | `opt/graphql_api.py` | 888 | blank line contains whitespace |
| 1525 | W293 | `opt/graphql_api.py` | 886 | blank line contains whitespace |
| 1524 | W293 | `opt/graphql_api.py` | 883 | blank line contains whitespace |
| 1523 | W293 | `opt/graphql_api.py` | 880 | blank line contains whitespace |
| 1522 | W293 | `opt/graphql_api.py` | 876 | blank line contains whitespace |
| 1521 | W293 | `opt/graphql_api.py` | 874 | blank line contains whitespace |
| 1520 | W293 | `opt/graphql_api.py` | 867 | blank line contains whitespace |
| 1519 | W293 | `opt/graphql_api.py` | 864 | blank line contains whitespace |
| 1518 | W293 | `opt/graphql_api.py` | 860 | blank line contains whitespace |
| 1517 | W293 | `opt/graphql_api.py` | 858 | blank line contains whitespace |
| 1516 | W293 | `opt/graphql_api.py` | 856 | blank line contains whitespace |
| 1515 | W293 | `opt/graphql_api.py` | 853 | blank line contains whitespace |
| 1514 | W293 | `opt/graphql_api.py` | 848 | blank line contains whitespace |
| 1513 | W293 | `opt/graphql_api.py` | 846 | blank line contains whitespace |
| 1512 | W293 | `opt/graphql_api.py` | 837 | blank line contains whitespace |
| 1511 | W293 | `opt/graphql_api.py` | 831 | blank line contains whitespace |
| 1510 | W293 | `opt/graphql_api.py` | 826 | blank line contains whitespace |
| 1509 | W293 | `opt/graphql_api.py` | 817 | blank line contains whitespace |
| 1508 | W293 | `opt/graphql_api.py` | 810 | blank line contains whitespace |
| 1507 | W293 | `opt/graphql_api.py` | 804 | blank line contains whitespace |
| 1506 | W293 | `opt/graphql_api.py` | 778 | blank line contains whitespace |
| 1505 | W293 | `opt/graphql_api.py` | 774 | blank line contains whitespace |
| 1504 | W293 | `opt/graphql_api.py` | 769 | blank line contains whitespace |
| 1503 | W293 | `opt/graphql_api.py` | 766 | blank line contains whitespace |
| 1502 | W293 | `opt/graphql_api.py` | 762 | blank line contains whitespace |
| 1501 | W293 | `opt/graphql_api.py` | 758 | blank line contains whitespace |
| 1500 | W293 | `opt/graphql_api.py` | 752 | blank line contains whitespace |
| 1499 | W293 | `opt/graphql_api.py` | 747 | blank line contains whitespace |
| 1498 | W291 | `opt/graphql_api.py` | 740 | trailing whitespace |
| 1497 | W293 | `opt/graphql_api.py` | 738 | blank line contains whitespace |
| 1496 | W293 | `opt/graphql_api.py` | 734 | blank line contains whitespace |
| 1495 | W293 | `opt/graphql_api.py` | 674 | blank line contains whitespace |
| 1494 | W291 | `opt/graphql_api.py` | 577 | trailing whitespace |
| 1493 | W293 | `opt/graphql_api.py` | 490 | blank line contains whitespace |
| 1492 | W293 | `opt/graphql_api.py` | 173 | blank line contains whitespace |
| 1491 | W293 | `opt/graphql_api.py` | 127 | blank line contains whitespace |
| 1490 | W293 | `opt/graphql_api.py` | 124 | blank line contains whitespace |
| 1489 | W293 | `opt/graphql_api.py` | 86 | blank line contains whitespace |
| 1486 | W293 | `opt/deployment/migrations.py` | 522 | blank line contains whitespace |
| 1485 | W293 | `opt/deployment/migrations.py` | 515 | blank line contains whitespace |
| 1484 | W293 | `opt/deployment/migrations.py` | 511 | blank line contains whitespace |
| 1483 | W293 | `opt/deployment/migrations.py` | 507 | blank line contains whitespace |
| 1482 | W293 | `opt/deployment/migrations.py` | 501 | blank line contains whitespace |
| 1481 | W293 | `opt/deployment/migrations.py` | 495 | blank line contains whitespace |
| 1480 | W293 | `opt/deployment/migrations.py` | 493 | blank line contains whitespace |
| 1479 | W293 | `opt/deployment/migrations.py` | 483 | blank line contains whitespace |
| 1478 | W293 | `opt/deployment/migrations.py` | 473 | blank line contains whitespace |
| 1477 | W293 | `opt/deployment/migrations.py` | 467 | blank line contains whitespace |
| 1476 | W293 | `opt/deployment/migrations.py` | 465 | blank line contains whitespace |
| 1475 | W293 | `opt/deployment/migrations.py` | 448 | blank line contains whitespace |
| 1474 | W293 | `opt/deployment/migrations.py` | 428 | blank line contains whitespace |
| 1473 | W293 | `opt/deployment/migrations.py` | 406 | blank line contains whitespace |
| 1472 | W293 | `opt/deployment/migrations.py` | 389 | blank line contains whitespace |
| 1471 | W293 | `opt/deployment/migrations.py` | 371 | blank line contains whitespace |
| 1470 | W293 | `opt/deployment/migrations.py` | 351 | blank line contains whitespace |
| 1469 | W293 | `opt/deployment/migrations.py` | 345 | blank line contains whitespace |
| 1468 | W293 | `opt/deployment/migrations.py` | 341 | blank line contains whitespace |
| 1467 | W293 | `opt/deployment/migrations.py` | 328 | blank line contains whitespace |
| 1466 | W293 | `opt/deployment/migrations.py` | 322 | blank line contains whitespace |
| 1465 | W293 | `opt/deployment/migrations.py` | 319 | blank line contains whitespace |
| 1464 | W293 | `opt/deployment/migrations.py` | 315 | blank line contains whitespace |
| 1463 | W293 | `opt/deployment/migrations.py` | 307 | blank line contains whitespace |
| 1462 | W293 | `opt/deployment/migrations.py` | 304 | blank line contains whitespace |
| 1461 | W293 | `opt/deployment/migrations.py` | 295 | blank line contains whitespace |
| 1460 | W293 | `opt/deployment/migrations.py` | 293 | blank line contains whitespace |
| 1459 | W293 | `opt/deployment/migrations.py` | 285 | blank line contains whitespace |
| 1458 | W293 | `opt/deployment/migrations.py` | 281 | blank line contains whitespace |
| 1457 | W293 | `opt/deployment/migrations.py` | 276 | blank line contains whitespace |
| 1456 | W293 | `opt/deployment/migrations.py` | 272 | blank line contains whitespace |
| 1455 | W293 | `opt/deployment/migrations.py` | 268 | blank line contains whitespace |
| 1454 | W293 | `opt/deployment/migrations.py` | 258 | blank line contains whitespace |
| 1453 | W293 | `opt/deployment/migrations.py` | 250 | blank line contains whitespace |
| 1452 | W293 | `opt/deployment/migrations.py` | 244 | blank line contains whitespace |
| 1451 | W293 | `opt/deployment/migrations.py` | 238 | blank line contains whitespace |
| 1450 | W293 | `opt/deployment/migrations.py` | 236 | blank line contains whitespace |
| 1449 | W293 | `opt/deployment/migrations.py` | 221 | blank line contains whitespace |
| 1448 | W293 | `opt/deployment/migrations.py` | 218 | blank line contains whitespace |
| 1447 | W293 | `opt/deployment/migrations.py` | 214 | blank line contains whitespace |
| 1446 | W293 | `opt/deployment/migrations.py` | 212 | blank line contains whitespace |
| 1445 | W293 | `opt/deployment/migrations.py` | 202 | blank line contains whitespace |
| 1444 | W293 | `opt/deployment/migrations.py` | 194 | blank line contains whitespace |
| 1443 | W293 | `opt/deployment/migrations.py` | 192 | blank line contains whitespace |
| 1442 | W291 | `opt/deployment/migrations.py` | 180 | trailing whitespace |
| 1441 | W293 | `opt/deployment/migrations.py` | 176 | blank line contains whitespace |
| 1440 | W293 | `opt/deployment/migrations.py` | 173 | blank line contains whitespace |
| 1439 | W293 | `opt/deployment/migrations.py` | 170 | blank line contains whitespace |
| 1438 | W293 | `opt/deployment/migrations.py` | 168 | blank line contains whitespace |
| 1437 | W293 | `opt/deployment/migrations.py` | 158 | blank line contains whitespace |
| 1436 | W293 | `opt/deployment/migrations.py` | 152 | blank line contains whitespace |
| 1435 | W293 | `opt/deployment/migrations.py` | 141 | blank line contains whitespace |
| 1434 | W293 | `opt/deployment/migrations.py` | 137 | blank line contains whitespace |
| 1433 | W293 | `opt/deployment/migrations.py` | 128 | blank line contains whitespace |
| 1432 | W293 | `opt/deployment/migrations.py` | 119 | blank line contains whitespace |
| 1431 | W293 | `opt/deployment/migrations.py` | 110 | blank line contains whitespace |
| 1430 | W293 | `opt/deployment/migrations.py` | 96 | blank line contains whitespace |
| 1429 | W293 | `opt/deployment/migrations.py` | 77 | blank line contains whitespace |
| 1428 | W293 | `opt/deployment/migrations.py` | 60 | blank line contains whitespace |
| 1425 | W293 | `opt/deployment/configuration.py` | 597 | blank line contains whitespace |
| 1424 | W293 | `opt/deployment/configuration.py` | 570 | blank line contains whitespace |
| 1423 | W293 | `opt/deployment/configuration.py` | 544 | blank line contains whitespace |
| 1422 | W293 | `opt/deployment/configuration.py` | 537 | blank line contains whitespace |
| 1421 | W293 | `opt/deployment/configuration.py` | 517 | blank line contains whitespace |
| 1420 | W293 | `opt/deployment/configuration.py` | 497 | blank line contains whitespace |
| 1419 | W293 | `opt/deployment/configuration.py` | 474 | blank line contains whitespace |
| 1418 | W293 | `opt/deployment/configuration.py` | 472 | blank line contains whitespace |
| 1417 | W293 | `opt/deployment/configuration.py` | 464 | blank line contains whitespace |
| 1416 | W293 | `opt/deployment/configuration.py` | 459 | blank line contains whitespace |
| 1415 | W293 | `opt/deployment/configuration.py` | 454 | blank line contains whitespace |
| 1414 | W293 | `opt/deployment/configuration.py` | 450 | blank line contains whitespace |
| 1413 | W293 | `opt/deployment/configuration.py` | 448 | blank line contains whitespace |
| 1412 | W293 | `opt/deployment/configuration.py` | 441 | blank line contains whitespace |
| 1411 | W293 | `opt/deployment/configuration.py` | 437 | blank line contains whitespace |
| 1410 | W293 | `opt/deployment/configuration.py` | 431 | blank line contains whitespace |
| 1409 | W293 | `opt/deployment/configuration.py` | 427 | blank line contains whitespace |
| 1408 | W293 | `opt/deployment/configuration.py` | 422 | blank line contains whitespace |
| 1407 | W293 | `opt/deployment/configuration.py` | 415 | blank line contains whitespace |
| 1406 | W293 | `opt/deployment/configuration.py` | 412 | blank line contains whitespace |
| 1405 | W293 | `opt/deployment/configuration.py` | 408 | blank line contains whitespace |
| 1404 | W293 | `opt/deployment/configuration.py` | 402 | blank line contains whitespace |
| 1403 | W293 | `opt/deployment/configuration.py` | 390 | blank line contains whitespace |
| 1402 | W293 | `opt/deployment/configuration.py` | 363 | blank line contains whitespace |
| 1401 | W293 | `opt/deployment/configuration.py` | 357 | blank line contains whitespace |
| 1400 | W293 | `opt/deployment/configuration.py` | 319 | blank line contains whitespace |
| 1399 | W293 | `opt/deployment/configuration.py` | 317 | blank line contains whitespace |
| 1398 | W293 | `opt/deployment/configuration.py` | 304 | blank line contains whitespace |
| 1397 | W293 | `opt/deployment/configuration.py` | 302 | blank line contains whitespace |
| 1396 | W293 | `opt/deployment/configuration.py` | 290 | blank line contains whitespace |
| 1395 | W293 | `opt/deployment/configuration.py` | 288 | blank line contains whitespace |
| 1394 | W293 | `opt/deployment/configuration.py` | 284 | blank line contains whitespace |
| 1393 | W293 | `opt/deployment/configuration.py` | 259 | blank line contains whitespace |
| 1392 | W293 | `opt/deployment/configuration.py` | 253 | blank line contains whitespace |
| 1391 | W293 | `opt/deployment/configuration.py` | 251 | blank line contains whitespace |
| 1390 | W293 | `opt/deployment/configuration.py` | 241 | blank line contains whitespace |
| 1389 | W293 | `opt/deployment/configuration.py` | 226 | blank line contains whitespace |
| 1388 | W293 | `opt/deployment/configuration.py` | 165 | blank line contains whitespace |
| 1387 | W293 | `opt/deployment/configuration.py` | 160 | blank line contains whitespace |
| 1386 | W293 | `opt/deployment/configuration.py` | 124 | blank line contains whitespace |
| 1385 | W293 | `opt/deployment/configuration.py` | 116 | blank line contains whitespace |
| 1384 | W293 | `opt/deployment/configuration.py` | 114 | blank line contains whitespace |
| 1383 | W293 | `opt/deployment/configuration.py` | 99 | blank line contains whitespace |
| 1382 | W293 | `opt/deployment/configuration.py` | 93 | blank line contains whitespace |
| 1381 | W293 | `opt/deployment/configuration.py` | 65 | blank line contains whitespace |
| 1378 | W293 | `opt/core/unified_backend.py` | 883 | blank line contains whitespace |
| 1377 | W293 | `opt/core/unified_backend.py` | 879 | blank line contains whitespace |
| 1376 | W293 | `opt/core/unified_backend.py` | 875 | blank line contains whitespace |
| 1375 | W293 | `opt/core/unified_backend.py` | 871 | blank line contains whitespace |
| 1374 | W293 | `opt/core/unified_backend.py` | 866 | blank line contains whitespace |
| 1373 | W293 | `opt/core/unified_backend.py` | 857 | blank line contains whitespace |
| 1372 | W293 | `opt/core/unified_backend.py` | 854 | blank line contains whitespace |
| 1371 | W293 | `opt/core/unified_backend.py` | 849 | blank line contains whitespace |
| 1370 | W293 | `opt/core/unified_backend.py` | 841 | blank line contains whitespace |
| 1369 | W293 | `opt/core/unified_backend.py` | 833 | blank line contains whitespace |
| 1368 | W293 | `opt/core/unified_backend.py` | 831 | blank line contains whitespace |
| 1367 | W293 | `opt/core/unified_backend.py` | 826 | blank line contains whitespace |
| 1366 | W293 | `opt/core/unified_backend.py` | 821 | blank line contains whitespace |
| 1365 | W293 | `opt/core/unified_backend.py` | 814 | blank line contains whitespace |
| 1364 | W293 | `opt/core/unified_backend.py` | 807 | blank line contains whitespace |
| 1363 | W293 | `opt/core/unified_backend.py` | 800 | blank line contains whitespace |
| 1362 | W293 | `opt/core/unified_backend.py` | 790 | blank line contains whitespace |
| 1361 | W293 | `opt/core/unified_backend.py` | 774 | blank line contains whitespace |
| 1360 | W293 | `opt/core/unified_backend.py` | 750 | blank line contains whitespace |
| 1359 | W293 | `opt/core/unified_backend.py` | 743 | blank line contains whitespace |
| 1358 | W293 | `opt/core/unified_backend.py` | 739 | blank line contains whitespace |
| 1357 | W293 | `opt/core/unified_backend.py` | 735 | blank line contains whitespace |
| 1356 | W293 | `opt/core/unified_backend.py` | 731 | blank line contains whitespace |
| 1355 | W293 | `opt/core/unified_backend.py` | 718 | blank line contains whitespace |
| 1354 | W293 | `opt/core/unified_backend.py` | 716 | blank line contains whitespace |
| 1353 | W293 | `opt/core/unified_backend.py` | 709 | blank line contains whitespace |
| 1352 | W293 | `opt/core/unified_backend.py` | 698 | blank line contains whitespace |
| 1351 | W293 | `opt/core/unified_backend.py` | 692 | blank line contains whitespace |
| 1350 | W293 | `opt/core/unified_backend.py` | 679 | blank line contains whitespace |
| 1349 | W293 | `opt/core/unified_backend.py` | 665 | blank line contains whitespace |
| 1348 | W293 | `opt/core/unified_backend.py` | 660 | blank line contains whitespace |
| 1347 | W293 | `opt/core/unified_backend.py` | 658 | blank line contains whitespace |
| 1346 | W293 | `opt/core/unified_backend.py` | 652 | blank line contains whitespace |
| 1345 | W293 | `opt/core/unified_backend.py` | 639 | blank line contains whitespace |
| 1344 | W293 | `opt/core/unified_backend.py` | 637 | blank line contains whitespace |
| 1343 | W293 | `opt/core/unified_backend.py` | 623 | blank line contains whitespace |
| 1342 | W293 | `opt/core/unified_backend.py` | 621 | blank line contains whitespace |
| 1341 | W293 | `opt/core/unified_backend.py` | 614 | blank line contains whitespace |
| 1340 | W293 | `opt/core/unified_backend.py` | 604 | blank line contains whitespace |
| 1339 | W293 | `opt/core/unified_backend.py` | 591 | blank line contains whitespace |
| 1338 | W293 | `opt/core/unified_backend.py` | 589 | blank line contains whitespace |
| 1337 | W293 | `opt/core/unified_backend.py` | 584 | blank line contains whitespace |
| 1336 | W293 | `opt/core/unified_backend.py` | 582 | blank line contains whitespace |
| 1335 | W293 | `opt/core/unified_backend.py` | 574 | blank line contains whitespace |
| 1334 | W293 | `opt/core/unified_backend.py` | 569 | blank line contains whitespace |
| 1333 | W293 | `opt/core/unified_backend.py` | 565 | blank line contains whitespace |
| 1332 | W293 | `opt/core/unified_backend.py` | 549 | blank line contains whitespace |
| 1331 | W293 | `opt/core/unified_backend.py` | 532 | blank line contains whitespace |
| 1330 | W293 | `opt/core/unified_backend.py` | 517 | blank line contains whitespace |
| 1329 | W293 | `opt/core/unified_backend.py` | 502 | blank line contains whitespace |
| 1328 | W293 | `opt/core/unified_backend.py` | 500 | blank line contains whitespace |
| 1327 | W293 | `opt/core/unified_backend.py` | 484 | blank line contains whitespace |
| 1326 | W293 | `opt/core/unified_backend.py` | 480 | blank line contains whitespace |
| 1325 | W293 | `opt/core/unified_backend.py` | 453 | blank line contains whitespace |
| 1324 | W293 | `opt/core/unified_backend.py` | 451 | blank line contains whitespace |
| 1323 | W293 | `opt/core/unified_backend.py` | 447 | blank line contains whitespace |
| 1322 | W293 | `opt/core/unified_backend.py` | 444 | blank line contains whitespace |
| 1321 | W293 | `opt/core/unified_backend.py` | 441 | blank line contains whitespace |
| 1320 | W293 | `opt/core/unified_backend.py` | 438 | blank line contains whitespace |
| 1319 | W293 | `opt/core/unified_backend.py` | 433 | blank line contains whitespace |
| 1318 | W293 | `opt/core/unified_backend.py` | 428 | blank line contains whitespace |
| 1317 | W293 | `opt/core/unified_backend.py` | 414 | blank line contains whitespace |
| 1316 | W293 | `opt/core/unified_backend.py` | 408 | blank line contains whitespace |
| 1315 | W293 | `opt/core/unified_backend.py` | 402 | blank line contains whitespace |
| 1314 | W293 | `opt/core/unified_backend.py` | 397 | blank line contains whitespace |
| 1313 | W293 | `opt/core/unified_backend.py` | 393 | blank line contains whitespace |
| 1312 | W293 | `opt/core/unified_backend.py` | 378 | blank line contains whitespace |
| 1311 | W293 | `opt/core/unified_backend.py` | 373 | blank line contains whitespace |
| 1310 | W293 | `opt/core/unified_backend.py` | 365 | blank line contains whitespace |
| 1309 | W293 | `opt/core/unified_backend.py` | 360 | blank line contains whitespace |
| 1308 | W293 | `opt/core/unified_backend.py` | 352 | blank line contains whitespace |
| 1307 | W293 | `opt/core/unified_backend.py` | 341 | blank line contains whitespace |
| 1306 | W293 | `opt/core/unified_backend.py` | 336 | blank line contains whitespace |
| 1305 | W293 | `opt/core/unified_backend.py` | 327 | blank line contains whitespace |
| 1304 | W293 | `opt/core/unified_backend.py` | 324 | blank line contains whitespace |
| 1303 | W293 | `opt/core/unified_backend.py` | 321 | blank line contains whitespace |
| 1302 | W293 | `opt/core/unified_backend.py` | 318 | blank line contains whitespace |
| 1301 | W293 | `opt/core/unified_backend.py` | 312 | blank line contains whitespace |
| 1300 | W293 | `opt/core/unified_backend.py` | 306 | blank line contains whitespace |
| 1299 | W293 | `opt/core/unified_backend.py` | 289 | blank line contains whitespace |
| 1298 | W291 | `opt/core/unified_backend.py` | 262 | trailing whitespace |
| 1297 | W293 | `opt/core/unified_backend.py` | 247 | blank line contains whitespace |
| 1296 | W293 | `opt/core/unified_backend.py` | 228 | blank line contains whitespace |
| 1295 | W293 | `opt/core/unified_backend.py` | 157 | blank line contains whitespace |
| 1294 | W293 | `opt/core/unified_backend.py` | 151 | blank line contains whitespace |
| 1293 | W293 | `opt/core/unified_backend.py` | 146 | blank line contains whitespace |
| 1292 | W293 | `opt/core/unified_backend.py` | 139 | blank line contains whitespace |
| 1291 | W293 | `opt/core/unified_backend.py` | 135 | blank line contains whitespace |
| 1290 | W293 | `opt/core/unified_backend.py` | 126 | blank line contains whitespace |
| 1289 | W293 | `opt/core/unified_backend.py` | 109 | blank line contains whitespace |
| 1288 | W293 | `opt/core/unified_backend.py` | 104 | blank line contains whitespace |
| 1287 | W293 | `opt/core/unified_backend.py` | 97 | blank line contains whitespace |
| 1286 | W293 | `opt/core/unified_backend.py` | 94 | blank line contains whitespace |
| 1285 | W293 | `opt/core/unified_backend.py` | 76 | blank line contains whitespace |
| 1284 | W293 | `opt/core/unified_backend.py` | 68 | blank line contains whitespace |
| 1283 | W293 | `opt/core/unified_backend.py` | 61 | blank line contains whitespace |
| 1282 | W293 | `opt/core/unified_backend.py` | 50 | blank line contains whitespace |
| 1281 | W291 | `opt/core/unified_backend.py` | 44 | trailing whitespace |
| 1280 | W293 | `opt/core/unified_backend.py` | 43 | blank line contains whitespace |
| 1279 | W293 | `opt/core/unified_backend.py` | 39 | blank line contains whitespace |
| 1274 | W293 | `opt/core/request_context.py` | 773 | blank line contains whitespace |
| 1273 | W293 | `opt/core/request_context.py` | 769 | blank line contains whitespace |
| 1272 | W293 | `opt/core/request_context.py` | 767 | blank line contains whitespace |
| 1271 | W293 | `opt/core/request_context.py` | 764 | blank line contains whitespace |
| 1270 | W293 | `opt/core/request_context.py` | 760 | blank line contains whitespace |
| 1269 | W293 | `opt/core/request_context.py` | 758 | blank line contains whitespace |
| 1268 | W293 | `opt/core/request_context.py` | 754 | blank line contains whitespace |
| 1267 | W293 | `opt/core/request_context.py` | 740 | blank line contains whitespace |
| 1266 | W293 | `opt/core/request_context.py` | 731 | blank line contains whitespace |
| 1265 | W293 | `opt/core/request_context.py` | 726 | blank line contains whitespace |
| 1264 | W293 | `opt/core/request_context.py` | 723 | blank line contains whitespace |
| 1263 | W293 | `opt/core/request_context.py` | 716 | blank line contains whitespace |
| 1262 | W293 | `opt/core/request_context.py` | 707 | blank line contains whitespace |
| 1261 | W293 | `opt/core/request_context.py` | 702 | blank line contains whitespace |
| 1260 | W293 | `opt/core/request_context.py` | 699 | blank line contains whitespace |
| 1259 | W293 | `opt/core/request_context.py` | 685 | blank line contains whitespace |
| 1258 | W293 | `opt/core/request_context.py` | 680 | blank line contains whitespace |
| 1257 | W293 | `opt/core/request_context.py` | 675 | blank line contains whitespace |
| 1256 | W293 | `opt/core/request_context.py` | 670 | blank line contains whitespace |
| 1255 | W293 | `opt/core/request_context.py` | 665 | blank line contains whitespace |
| 1254 | W293 | `opt/core/request_context.py` | 658 | blank line contains whitespace |
| 1253 | W293 | `opt/core/request_context.py` | 652 | blank line contains whitespace |
| 1252 | W293 | `opt/core/request_context.py` | 648 | blank line contains whitespace |
| 1251 | W293 | `opt/core/request_context.py` | 643 | blank line contains whitespace |
| 1250 | W293 | `opt/core/request_context.py` | 641 | blank line contains whitespace |
| 1249 | W293 | `opt/core/request_context.py` | 634 | blank line contains whitespace |
| 1248 | W293 | `opt/core/request_context.py` | 625 | blank line contains whitespace |
| 1247 | W293 | `opt/core/request_context.py` | 620 | blank line contains whitespace |
| 1246 | W293 | `opt/core/request_context.py` | 617 | blank line contains whitespace |
| 1245 | W293 | `opt/core/request_context.py` | 604 | blank line contains whitespace |
| 1244 | W293 | `opt/core/request_context.py` | 597 | blank line contains whitespace |
| 1243 | W293 | `opt/core/request_context.py` | 590 | blank line contains whitespace |
| 1242 | W293 | `opt/core/request_context.py` | 588 | blank line contains whitespace |
| 1241 | W293 | `opt/core/request_context.py` | 584 | blank line contains whitespace |
| 1240 | W293 | `opt/core/request_context.py` | 579 | blank line contains whitespace |
| 1239 | W293 | `opt/core/request_context.py` | 575 | blank line contains whitespace |
| 1238 | W293 | `opt/core/request_context.py` | 571 | blank line contains whitespace |
| 1237 | W293 | `opt/core/request_context.py` | 563 | blank line contains whitespace |
| 1236 | W293 | `opt/core/request_context.py` | 558 | blank line contains whitespace |
| 1235 | W293 | `opt/core/request_context.py` | 544 | blank line contains whitespace |
| 1234 | W293 | `opt/core/request_context.py` | 541 | blank line contains whitespace |
| 1233 | W293 | `opt/core/request_context.py` | 534 | blank line contains whitespace |
| 1232 | W293 | `opt/core/request_context.py` | 529 | blank line contains whitespace |
| 1231 | W293 | `opt/core/request_context.py` | 521 | blank line contains whitespace |
| 1230 | W293 | `opt/core/request_context.py` | 516 | blank line contains whitespace |
| 1229 | W293 | `opt/core/request_context.py` | 509 | blank line contains whitespace |
| 1228 | W293 | `opt/core/request_context.py` | 494 | blank line contains whitespace |
| 1227 | W293 | `opt/core/request_context.py` | 490 | blank line contains whitespace |
| 1226 | W293 | `opt/core/request_context.py` | 486 | blank line contains whitespace |
| 1225 | W293 | `opt/core/request_context.py` | 467 | blank line contains whitespace |
| 1224 | W293 | `opt/core/request_context.py` | 462 | blank line contains whitespace |
| 1223 | W293 | `opt/core/request_context.py` | 455 | blank line contains whitespace |
| 1222 | W293 | `opt/core/request_context.py` | 448 | blank line contains whitespace |
| 1221 | W293 | `opt/core/request_context.py` | 444 | blank line contains whitespace |
| 1220 | W293 | `opt/core/request_context.py` | 438 | blank line contains whitespace |
| 1219 | W293 | `opt/core/request_context.py` | 432 | blank line contains whitespace |
| 1218 | W293 | `opt/core/request_context.py` | 426 | blank line contains whitespace |
| 1217 | W293 | `opt/core/request_context.py` | 420 | blank line contains whitespace |
| 1216 | W293 | `opt/core/request_context.py` | 414 | blank line contains whitespace |
| 1215 | W293 | `opt/core/request_context.py` | 410 | blank line contains whitespace |
| 1214 | W293 | `opt/core/request_context.py` | 408 | blank line contains whitespace |
| 1213 | W293 | `opt/core/request_context.py` | 392 | blank line contains whitespace |
| 1212 | W293 | `opt/core/request_context.py` | 388 | blank line contains whitespace |
| 1211 | W293 | `opt/core/request_context.py` | 384 | blank line contains whitespace |
| 1210 | W293 | `opt/core/request_context.py` | 379 | blank line contains whitespace |
| 1209 | W293 | `opt/core/request_context.py` | 376 | blank line contains whitespace |
| 1208 | W293 | `opt/core/request_context.py` | 369 | blank line contains whitespace |
| 1207 | W293 | `opt/core/request_context.py` | 365 | blank line contains whitespace |
| 1206 | W293 | `opt/core/request_context.py` | 357 | blank line contains whitespace |
| 1205 | W293 | `opt/core/request_context.py` | 353 | blank line contains whitespace |
| 1204 | W293 | `opt/core/request_context.py` | 348 | blank line contains whitespace |
| 1203 | W293 | `opt/core/request_context.py` | 339 | blank line contains whitespace |
| 1202 | W293 | `opt/core/request_context.py` | 334 | blank line contains whitespace |
| 1201 | W293 | `opt/core/request_context.py` | 330 | blank line contains whitespace |
| 1200 | W293 | `opt/core/request_context.py` | 325 | blank line contains whitespace |
| 1199 | W293 | `opt/core/request_context.py` | 305 | blank line contains whitespace |
| 1198 | W293 | `opt/core/request_context.py` | 294 | blank line contains whitespace |
| 1197 | W293 | `opt/core/request_context.py` | 289 | blank line contains whitespace |
| 1196 | W293 | `opt/core/request_context.py` | 274 | blank line contains whitespace |
| 1195 | W293 | `opt/core/request_context.py` | 263 | blank line contains whitespace |
| 1194 | W293 | `opt/core/request_context.py` | 255 | blank line contains whitespace |
| 1193 | W293 | `opt/core/request_context.py` | 247 | blank line contains whitespace |
| 1192 | W293 | `opt/core/request_context.py` | 236 | blank line contains whitespace |
| 1191 | W293 | `opt/core/request_context.py` | 233 | blank line contains whitespace |
| 1190 | W293 | `opt/core/request_context.py` | 225 | blank line contains whitespace |
| 1189 | W293 | `opt/core/request_context.py` | 217 | blank line contains whitespace |
| 1188 | W293 | `opt/core/request_context.py` | 195 | blank line contains whitespace |
| 1187 | W293 | `opt/core/request_context.py` | 191 | blank line contains whitespace |
| 1186 | W293 | `opt/core/request_context.py` | 180 | blank line contains whitespace |
| 1185 | W293 | `opt/core/request_context.py` | 178 | blank line contains whitespace |
| 1184 | W293 | `opt/core/request_context.py` | 168 | blank line contains whitespace |
| 1183 | W293 | `opt/core/request_context.py` | 165 | blank line contains whitespace |
| 1182 | W293 | `opt/core/request_context.py` | 160 | blank line contains whitespace |
| 1181 | W293 | `opt/core/request_context.py` | 158 | blank line contains whitespace |
| 1180 | W293 | `opt/core/request_context.py` | 145 | blank line contains whitespace |
| 1179 | W293 | `opt/core/request_context.py` | 137 | blank line contains whitespace |
| 1178 | W293 | `opt/core/request_context.py` | 133 | blank line contains whitespace |
| 1177 | W293 | `opt/core/request_context.py` | 116 | blank line contains whitespace |
| 1176 | W293 | `opt/core/request_context.py` | 113 | blank line contains whitespace |
| 1175 | W293 | `opt/core/request_context.py` | 109 | blank line contains whitespace |
| 1174 | W293 | `opt/core/request_context.py` | 100 | blank line contains whitespace |
| 1173 | W293 | `opt/core/request_context.py` | 97 | blank line contains whitespace |
| 1172 | W293 | `opt/core/request_context.py` | 92 | blank line contains whitespace |
| 1171 | W293 | `opt/core/request_context.py` | 88 | blank line contains whitespace |
| 1170 | W293 | `opt/core/request_context.py` | 85 | blank line contains whitespace |
| 1169 | W293 | `opt/core/request_context.py` | 80 | blank line contains whitespace |
| 1168 | W293 | `opt/core/request_context.py` | 76 | blank line contains whitespace |
| 1167 | W293 | `opt/core/request_context.py` | 73 | blank line contains whitespace |
| 1164 | W293 | `opt/config_distributor.py` | 214 | blank line contains whitespace |
| 1163 | W293 | `opt/config_distributor.py` | 212 | blank line contains whitespace |
| 1162 | W293 | `opt/config_distributor.py` | 206 | blank line contains whitespace |
| 1161 | W293 | `opt/config_distributor.py` | 200 | blank line contains whitespace |
| 1160 | W293 | `opt/config_distributor.py` | 195 | blank line contains whitespace |
| 1159 | W293 | `opt/config_distributor.py` | 192 | blank line contains whitespace |
| 1158 | W293 | `opt/config_distributor.py` | 186 | blank line contains whitespace |
| 1157 | W293 | `opt/config_distributor.py` | 181 | blank line contains whitespace |
| 1156 | W293 | `opt/config_distributor.py` | 177 | blank line contains whitespace |
| 1155 | W293 | `opt/config_distributor.py` | 174 | blank line contains whitespace |
| 1154 | W293 | `opt/config_distributor.py` | 170 | blank line contains whitespace |
| 1153 | W293 | `opt/config_distributor.py` | 168 | blank line contains whitespace |
| 1151 | W293 | `opt/config_distributor.py` | 165 | blank line contains whitespace |
| 1150 | W293 | `opt/config_distributor.py` | 160 | blank line contains whitespace |
| 1149 | W293 | `opt/config_distributor.py` | 155 | blank line contains whitespace |
| 1148 | W293 | `opt/config_distributor.py` | 153 | blank line contains whitespace |
| 1147 | W293 | `opt/config_distributor.py` | 145 | blank line contains whitespace |
| 1146 | W293 | `opt/config_distributor.py` | 136 | blank line contains whitespace |
| 1145 | W293 | `opt/config_distributor.py` | 132 | blank line contains whitespace |
| 1144 | W293 | `opt/config_distributor.py` | 123 | blank line contains whitespace |
| 1143 | W293 | `opt/config_distributor.py` | 116 | blank line contains whitespace |
| 1142 | W293 | `opt/config_distributor.py` | 113 | blank line contains whitespace |
| 1141 | W293 | `opt/config_distributor.py` | 109 | blank line contains whitespace |
| 1140 | W293 | `opt/config_distributor.py` | 80 | blank line contains whitespace |
| 1139 | W293 | `opt/config_distributor.py` | 58 | blank line contains whitespace |
| 1137 | W293 | `opt/cert_manager.py` | 292 | blank line contains whitespace |
| 1136 | W291 | `opt/cert_manager.py` | 288 | trailing whitespace |
| 1135 | W291 | `opt/cert_manager.py` | 287 | trailing whitespace |
| 1134 | W293 | `opt/cert_manager.py` | 281 | blank line contains whitespace |
| 1133 | W293 | `opt/cert_manager.py` | 274 | blank line contains whitespace |
| 1132 | W293 | `opt/cert_manager.py` | 268 | blank line contains whitespace |
| 1131 | W293 | `opt/cert_manager.py` | 265 | blank line contains whitespace |
| 1130 | W293 | `opt/cert_manager.py` | 261 | blank line contains whitespace |
| 1129 | W293 | `opt/cert_manager.py` | 259 | blank line contains whitespace |
| 1128 | W293 | `opt/cert_manager.py` | 252 | blank line contains whitespace |
| 1127 | W293 | `opt/cert_manager.py` | 246 | blank line contains whitespace |
| 1126 | W293 | `opt/cert_manager.py` | 242 | blank line contains whitespace |
| 1125 | W293 | `opt/cert_manager.py` | 240 | blank line contains whitespace |
| 1124 | W293 | `opt/cert_manager.py` | 231 | blank line contains whitespace |
| 1123 | W293 | `opt/cert_manager.py` | 223 | blank line contains whitespace |
| 1122 | W293 | `opt/cert_manager.py` | 219 | blank line contains whitespace |
| 1121 | W293 | `opt/cert_manager.py` | 214 | blank line contains whitespace |
| 1120 | W293 | `opt/cert_manager.py` | 203 | blank line contains whitespace |
| 1119 | W293 | `opt/cert_manager.py` | 200 | blank line contains whitespace |
| 1118 | W293 | `opt/cert_manager.py` | 132 | blank line contains whitespace |
| 1117 | W293 | `opt/cert_manager.py` | 109 | blank line contains whitespace |
| 1116 | W293 | `opt/cert_manager.py` | 105 | blank line contains whitespace |
| 1115 | W293 | `opt/cert_manager.py` | 66 | blank line contains whitespace |
| 1094 | W293 | `opt/build/validate-iso.py` | 350 | blank line contains whitespace |
| 1093 | W293 | `opt/build/validate-iso.py` | 347 | blank line contains whitespace |
| 1092 | W293 | `opt/build/validate-iso.py` | 345 | blank line contains whitespace |
| 1091 | W293 | `opt/build/validate-iso.py` | 334 | blank line contains whitespace |
| 1090 | W293 | `opt/build/validate-iso.py` | 331 | blank line contains whitespace |
| 1089 | W293 | `opt/build/validate-iso.py` | 326 | blank line contains whitespace |
| 1088 | W293 | `opt/build/validate-iso.py` | 321 | blank line contains whitespace |
| 1087 | W293 | `opt/build/validate-iso.py` | 316 | blank line contains whitespace |
| 1086 | W293 | `opt/build/validate-iso.py` | 310 | blank line contains whitespace |
| 1085 | W293 | `opt/build/validate-iso.py` | 298 | blank line contains whitespace |
| 1084 | W293 | `opt/build/validate-iso.py` | 296 | blank line contains whitespace |
| 1083 | W293 | `opt/build/validate-iso.py` | 285 | blank line contains whitespace |
| 1082 | W293 | `opt/build/validate-iso.py` | 279 | blank line contains whitespace |
| 1081 | W293 | `opt/build/validate-iso.py` | 275 | blank line contains whitespace |
| 1080 | W293 | `opt/build/validate-iso.py` | 271 | blank line contains whitespace |
| 1079 | W293 | `opt/build/validate-iso.py` | 267 | blank line contains whitespace |
| 1078 | W293 | `opt/build/validate-iso.py` | 259 | blank line contains whitespace |
| 1077 | W293 | `opt/build/validate-iso.py` | 251 | blank line contains whitespace |
| 1076 | W293 | `opt/build/validate-iso.py` | 242 | blank line contains whitespace |
| 1075 | W293 | `opt/build/validate-iso.py` | 235 | blank line contains whitespace |
| 1074 | W293 | `opt/build/validate-iso.py` | 231 | blank line contains whitespace |
| 1073 | W293 | `opt/build/validate-iso.py` | 227 | blank line contains whitespace |
| 1072 | W293 | `opt/build/validate-iso.py` | 223 | blank line contains whitespace |
| 1071 | W293 | `opt/build/validate-iso.py` | 210 | blank line contains whitespace |
| 1070 | W293 | `opt/build/validate-iso.py` | 205 | blank line contains whitespace |
| 1069 | W293 | `opt/build/validate-iso.py` | 201 | blank line contains whitespace |
| 1068 | W293 | `opt/build/validate-iso.py` | 198 | blank line contains whitespace |
| 1067 | W293 | `opt/build/validate-iso.py` | 196 | blank line contains whitespace |
| 1066 | W293 | `opt/build/validate-iso.py` | 187 | blank line contains whitespace |
| 1065 | W293 | `opt/build/validate-iso.py` | 183 | blank line contains whitespace |
| 1064 | W293 | `opt/build/validate-iso.py` | 178 | blank line contains whitespace |
| 1063 | W293 | `opt/build/validate-iso.py` | 173 | blank line contains whitespace |
| 1062 | W293 | `opt/build/validate-iso.py` | 166 | blank line contains whitespace |
| 1061 | W293 | `opt/build/validate-iso.py` | 162 | blank line contains whitespace |
| 1060 | W293 | `opt/build/validate-iso.py` | 158 | blank line contains whitespace |
| 1059 | W293 | `opt/build/validate-iso.py` | 153 | blank line contains whitespace |
| 1058 | W293 | `opt/build/validate-iso.py` | 142 | blank line contains whitespace |
| 1057 | W293 | `opt/build/validate-iso.py` | 134 | blank line contains whitespace |
| 1056 | W293 | `opt/build/validate-iso.py` | 125 | blank line contains whitespace |
| 1055 | W293 | `opt/build/validate-iso.py` | 121 | blank line contains whitespace |
| 1054 | W293 | `opt/build/validate-iso.py` | 110 | blank line contains whitespace |
| 1053 | W293 | `opt/build/validate-iso.py` | 100 | blank line contains whitespace |
| 1052 | W293 | `opt/build/validate-iso.py` | 95 | blank line contains whitespace |
| 1051 | W293 | `opt/build/validate-iso.py` | 90 | blank line contains whitespace |
| 1050 | W293 | `opt/build/validate-iso.py` | 80 | blank line contains whitespace |
| 1049 | W293 | `opt/build/validate-iso.py` | 75 | blank line contains whitespace |
| 1048 | W293 | `opt/build/validate-iso.py` | 71 | blank line contains whitespace |
| 1047 | W293 | `opt/build/validate-iso.py` | 65 | blank line contains whitespace |
| 1046 | W293 | `opt/build/validate-iso.py` | 62 | blank line contains whitespace |
| 1045 | W293 | `opt/build/validate-iso.py` | 59 | blank line contains whitespace |
| 1044 | W293 | `opt/build/validate-iso.py` | 56 | blank line contains whitespace |
| 1043 | W293 | `opt/build/validate-iso.py` | 53 | blank line contains whitespace |
| 1042 | W293 | `opt/build/validate-iso.py` | 50 | blank line contains whitespace |
| 1041 | W293 | `opt/build/validate-iso.py` | 47 | blank line contains whitespace |
| 1040 | W293 | `opt/build/validate-iso.py` | 45 | blank line contains whitespace |
| 1039 | W293 | `opt/build/validate-iso.py` | 42 | blank line contains whitespace |
| 1038 | W293 | `opt/build/validate-iso.py` | 39 | blank line contains whitespace |
| 1037 | W293 | `opt/build/validate-iso.py` | 35 | blank line contains whitespace |
| 1036 | W293 | `opt/build/validate-iso.py` | 27 | blank line contains whitespace |
| 1032 | W293 | `opt/ansible/validate-inventory.py` | 329 | blank line contains whitespace |
| 1031 | W293 | `opt/ansible/validate-inventory.py` | 326 | blank line contains whitespace |
| 1030 | W293 | `opt/ansible/validate-inventory.py` | 324 | blank line contains whitespace |
| 1029 | W293 | `opt/ansible/validate-inventory.py` | 312 | blank line contains whitespace |
| 1028 | W293 | `opt/ansible/validate-inventory.py` | 310 | blank line contains whitespace |
| 1027 | W293 | `opt/ansible/validate-inventory.py` | 307 | blank line contains whitespace |
| 1026 | W293 | `opt/ansible/validate-inventory.py` | 302 | blank line contains whitespace |
| 1025 | W293 | `opt/ansible/validate-inventory.py` | 297 | blank line contains whitespace |
| 1024 | W293 | `opt/ansible/validate-inventory.py` | 293 | blank line contains whitespace |
| 1023 | W293 | `opt/ansible/validate-inventory.py` | 291 | blank line contains whitespace |
| 1022 | W293 | `opt/ansible/validate-inventory.py` | 289 | blank line contains whitespace |
| 1021 | W293 | `opt/ansible/validate-inventory.py` | 284 | blank line contains whitespace |
| 1020 | W293 | `opt/ansible/validate-inventory.py` | 279 | blank line contains whitespace |
| 1019 | W293 | `opt/ansible/validate-inventory.py` | 274 | blank line contains whitespace |
| 1018 | W293 | `opt/ansible/validate-inventory.py` | 269 | blank line contains whitespace |
| 1017 | W293 | `opt/ansible/validate-inventory.py` | 267 | blank line contains whitespace |
| 1016 | W293 | `opt/ansible/validate-inventory.py` | 264 | blank line contains whitespace |
| 1015 | W293 | `opt/ansible/validate-inventory.py` | 260 | blank line contains whitespace |
| 1014 | W293 | `opt/ansible/validate-inventory.py` | 258 | blank line contains whitespace |
| 1013 | W293 | `opt/ansible/validate-inventory.py` | 245 | blank line contains whitespace |
| 1012 | W293 | `opt/ansible/validate-inventory.py` | 232 | blank line contains whitespace |
| 1011 | W293 | `opt/ansible/validate-inventory.py` | 228 | blank line contains whitespace |
| 1010 | W293 | `opt/ansible/validate-inventory.py` | 225 | blank line contains whitespace |
| 1009 | W293 | `opt/ansible/validate-inventory.py` | 221 | blank line contains whitespace |
| 1008 | W293 | `opt/ansible/validate-inventory.py` | 216 | blank line contains whitespace |
| 1007 | W293 | `opt/ansible/validate-inventory.py` | 213 | blank line contains whitespace |
| 1006 | W293 | `opt/ansible/validate-inventory.py` | 208 | blank line contains whitespace |
| 1005 | W293 | `opt/ansible/validate-inventory.py` | 203 | blank line contains whitespace |
| 1004 | W293 | `opt/ansible/validate-inventory.py` | 193 | blank line contains whitespace |
| 1003 | W293 | `opt/ansible/validate-inventory.py` | 191 | blank line contains whitespace |
| 1002 | W293 | `opt/ansible/validate-inventory.py` | 187 | blank line contains whitespace |
| 1001 | W293 | `opt/ansible/validate-inventory.py` | 183 | blank line contains whitespace |
| 1000 | W293 | `opt/ansible/validate-inventory.py` | 166 | blank line contains whitespace |
| 999 | W293 | `opt/ansible/validate-inventory.py` | 161 | blank line contains whitespace |
| 998 | W293 | `opt/ansible/validate-inventory.py` | 148 | blank line contains whitespace |
| 997 | W293 | `opt/ansible/validate-inventory.py` | 146 | blank line contains whitespace |
| 996 | W293 | `opt/ansible/validate-inventory.py` | 143 | blank line contains whitespace |
| 995 | W293 | `opt/ansible/validate-inventory.py` | 139 | blank line contains whitespace |
| 994 | W293 | `opt/ansible/validate-inventory.py` | 127 | blank line contains whitespace |
| 993 | W293 | `opt/ansible/validate-inventory.py` | 121 | blank line contains whitespace |
| 992 | W293 | `opt/ansible/validate-inventory.py` | 116 | blank line contains whitespace |
| 991 | W293 | `opt/ansible/validate-inventory.py` | 112 | blank line contains whitespace |
| 990 | W293 | `opt/ansible/validate-inventory.py` | 98 | blank line contains whitespace |
| 989 | W293 | `opt/ansible/validate-inventory.py` | 96 | blank line contains whitespace |
| 988 | W293 | `opt/ansible/validate-inventory.py` | 83 | blank line contains whitespace |
| 987 | W293 | `opt/ansible/validate-inventory.py` | 78 | blank line contains whitespace |
| 986 | W293 | `opt/ansible/validate-inventory.py` | 76 | blank line contains whitespace |
| 985 | W293 | `opt/ansible/validate-inventory.py` | 66 | blank line contains whitespace |
| 984 | W293 | `opt/ansible/validate-inventory.py` | 64 | blank line contains whitespace |
| 983 | W293 | `opt/ansible/validate-inventory.py` | 60 | blank line contains whitespace |
| 982 | W293 | `opt/ansible/validate-inventory.py` | 54 | blank line contains whitespace |
| 981 | W293 | `opt/ansible/validate-inventory.py` | 38 | blank line contains whitespace |
| 980 | W293 | `opt/ansible/validate-inventory.py` | 30 | blank line contains whitespace |
| 973 | W292 | `mock_mode.py` | 2 | no newline at end of file |
| 970 | W293 | `etc/debvisor/test_validate_blocklists.py` | 525 | blank line contains whitespace |
| 969 | W291 | `etc/debvisor/test_validate_blocklists.py` | 507 | trailing whitespace |
| 968 | W293 | `etc/debvisor/test_validate_blocklists.py` | 503 | blank line contains whitespace |
| 967 | W293 | `etc/debvisor/test_validate_blocklists.py` | 481 | blank line contains whitespace |
| 966 | W293 | `etc/debvisor/test_validate_blocklists.py` | 478 | blank line contains whitespace |
| 964 | W293 | `etc/debvisor/test_validate_blocklists.py` | 471 | blank line contains whitespace |
| 963 | W293 | `etc/debvisor/test_validate_blocklists.py` | 464 | blank line contains whitespace |
| 962 | W293 | `etc/debvisor/test_validate_blocklists.py` | 457 | blank line contains whitespace |
| 961 | W293 | `etc/debvisor/test_validate_blocklists.py` | 449 | blank line contains whitespace |
| 960 | W293 | `etc/debvisor/test_validate_blocklists.py` | 443 | blank line contains whitespace |
| 959 | W293 | `etc/debvisor/test_validate_blocklists.py` | 436 | blank line contains whitespace |
| 958 | W293 | `etc/debvisor/test_validate_blocklists.py` | 410 | blank line contains whitespace |
| 957 | W293 | `etc/debvisor/test_validate_blocklists.py` | 387 | blank line contains whitespace |
| 956 | W293 | `etc/debvisor/test_validate_blocklists.py` | 362 | blank line contains whitespace |
| 955 | W293 | `etc/debvisor/test_validate_blocklists.py` | 341 | blank line contains whitespace |
| 954 | W293 | `etc/debvisor/test_validate_blocklists.py` | 335 | blank line contains whitespace |
| 953 | W293 | `etc/debvisor/test_validate_blocklists.py` | 329 | blank line contains whitespace |
| 952 | W293 | `etc/debvisor/test_validate_blocklists.py` | 326 | blank line contains whitespace |
| 951 | W293 | `etc/debvisor/test_validate_blocklists.py` | 320 | blank line contains whitespace |
| 950 | W293 | `etc/debvisor/test_validate_blocklists.py` | 317 | blank line contains whitespace |
| 949 | W293 | `etc/debvisor/test_validate_blocklists.py` | 310 | blank line contains whitespace |
| 948 | W293 | `etc/debvisor/test_validate_blocklists.py` | 307 | blank line contains whitespace |
| 947 | W293 | `etc/debvisor/test_validate_blocklists.py` | 296 | blank line contains whitespace |
| 946 | W293 | `etc/debvisor/test_validate_blocklists.py` | 293 | blank line contains whitespace |
| 945 | W293 | `etc/debvisor/test_validate_blocklists.py` | 286 | blank line contains whitespace |
| 944 | W293 | `etc/debvisor/test_validate_blocklists.py` | 283 | blank line contains whitespace |
| 943 | W293 | `etc/debvisor/test_validate_blocklists.py` | 275 | blank line contains whitespace |
| 942 | W293 | `etc/debvisor/test_validate_blocklists.py` | 268 | blank line contains whitespace |
| 941 | W293 | `etc/debvisor/test_validate_blocklists.py` | 261 | blank line contains whitespace |
| 940 | W293 | `etc/debvisor/test_validate_blocklists.py` | 258 | blank line contains whitespace |
| 939 | W293 | `etc/debvisor/test_validate_blocklists.py` | 246 | blank line contains whitespace |
| 938 | W293 | `etc/debvisor/test_validate_blocklists.py` | 243 | blank line contains whitespace |
| 937 | W293 | `etc/debvisor/test_validate_blocklists.py` | 240 | blank line contains whitespace |
| 936 | W293 | `etc/debvisor/test_validate_blocklists.py` | 233 | blank line contains whitespace |
| 935 | W293 | `etc/debvisor/test_validate_blocklists.py` | 230 | blank line contains whitespace |
| 934 | W293 | `etc/debvisor/test_validate_blocklists.py` | 223 | blank line contains whitespace |
| 933 | W293 | `etc/debvisor/test_validate_blocklists.py` | 220 | blank line contains whitespace |
| 932 | W293 | `etc/debvisor/test_validate_blocklists.py` | 213 | blank line contains whitespace |
| 931 | W293 | `etc/debvisor/test_validate_blocklists.py` | 210 | blank line contains whitespace |
| 930 | W293 | `etc/debvisor/test_validate_blocklists.py` | 203 | blank line contains whitespace |
| 929 | W293 | `etc/debvisor/test_validate_blocklists.py` | 200 | blank line contains whitespace |
| 928 | W293 | `etc/debvisor/test_validate_blocklists.py` | 194 | blank line contains whitespace |
| 927 | W293 | `etc/debvisor/test_validate_blocklists.py` | 191 | blank line contains whitespace |
| 926 | W293 | `etc/debvisor/test_validate_blocklists.py` | 170 | blank line contains whitespace |
| 925 | W293 | `etc/debvisor/test_validate_blocklists.py` | 147 | blank line contains whitespace |
| 924 | W293 | `etc/debvisor/test_validate_blocklists.py` | 126 | blank line contains whitespace |
| 923 | W293 | `etc/debvisor/test_validate_blocklists.py` | 110 | blank line contains whitespace |
| 922 | W293 | `etc/debvisor/test_validate_blocklists.py` | 107 | blank line contains whitespace |
| 921 | W293 | `etc/debvisor/test_validate_blocklists.py` | 93 | blank line contains whitespace |
| 920 | W293 | `etc/debvisor/test_validate_blocklists.py` | 78 | blank line contains whitespace |
| 917 | E305 | `tests/test_webhook_system.py` | 471 | expected 2 blank lines after class or function definition, found 1 |
| 916 | E302 | `tests/test_webhook_system.py` | 414 | expected 2 blank lines, found 1 |
| 915 | E302 | `tests/test_webhook_system.py` | 326 | expected 2 blank lines, found 1 |
| 914 | E302 | `tests/test_webhook_system.py` | 121 | expected 2 blank lines, found 1 |
| 913 | E302 | `tests/test_webhook_system.py` | 64 | expected 2 blank lines, found 1 |
| 912 | E302 | `tests/test_webhook_system.py` | 24 | expected 2 blank lines, found 1 |
| 911 | E305 | `tests/test_slo_tracking.py` | 487 | expected 2 blank lines after class or function definition, found 1 |
| 910 | E302 | `tests/test_slo_tracking.py` | 427 | expected 2 blank lines, found 1 |
| 909 | E302 | `tests/test_slo_tracking.py` | 353 | expected 2 blank lines, found 1 |
| 908 | E302 | `tests/test_slo_tracking.py` | 235 | expected 2 blank lines, found 1 |
| 907 | E302 | `tests/test_slo_tracking.py` | 157 | expected 2 blank lines, found 1 |
| 906 | E302 | `tests/test_slo_tracking.py` | 130 | expected 2 blank lines, found 1 |
| 905 | E302 | `tests/test_slo_tracking.py` | 91 | expected 2 blank lines, found 1 |
| 904 | E302 | `tests/test_slo_tracking.py` | 54 | expected 2 blank lines, found 1 |
| 903 | E302 | `tests/test_slo_tracking.py` | 33 | expected 2 blank lines, found 1 |
| 902 | E305 | `tests/test_security_testing.py` | 442 | expected 2 blank lines after class or function definition, found 1 |
| 901 | E302 | `tests/test_security_testing.py` | 405 | expected 2 blank lines, found 1 |
| 900 | E302 | `tests/test_security_testing.py` | 296 | expected 2 blank lines, found 1 |
| 899 | E302 | `tests/test_security_testing.py` | 212 | expected 2 blank lines, found 1 |
| 898 | E302 | `tests/test_security_testing.py` | 158 | expected 2 blank lines, found 1 |
| 897 | E302 | `tests/test_security_testing.py` | 23 | expected 2 blank lines, found 1 |
| 896 | E305 | `tests/test_scheduler.py` | 578 | expected 2 blank lines after class or function definition, found 1 |
| 895 | E302 | `tests/test_scheduler.py` | 512 | expected 2 blank lines, found 1 |
| 894 | E302 | `tests/test_scheduler.py` | 385 | expected 2 blank lines, found 1 |
| 893 | E302 | `tests/test_scheduler.py` | 284 | expected 2 blank lines, found 1 |
| 892 | E302 | `tests/test_scheduler.py` | 77 | expected 2 blank lines, found 1 |
| 891 | E302 | `tests/test_scheduler.py` | 32 | expected 2 blank lines, found 1 |
| 890 | E305 | `tests/test_rpc_security.py` | 756 | expected 2 blank lines after class or function definition, found 1 |
| 889 | E302 | `tests/test_rpc_security.py` | 710 | expected 2 blank lines, found 1 |
| 888 | E302 | `tests/test_rpc_security.py` | 656 | expected 2 blank lines, found 1 |
| 887 | E302 | `tests/test_rpc_security.py` | 573 | expected 2 blank lines, found 1 |
| 886 | E302 | `tests/test_rpc_security.py` | 482 | expected 2 blank lines, found 1 |
| 885 | E302 | `tests/test_rpc_security.py` | 393 | expected 2 blank lines, found 1 |
| 884 | E302 | `tests/test_rpc_security.py` | 312 | expected 2 blank lines, found 1 |
| 883 | E302 | `tests/test_rpc_security.py` | 216 | expected 2 blank lines, found 1 |
| 882 | E302 | `tests/test_rpc_security.py` | 126 | expected 2 blank lines, found 1 |
| 881 | E302 | `tests/test_rpc_security.py` | 114 | expected 2 blank lines, found 1 |
| 880 | E302 | `tests/test_rpc_security.py` | 102 | expected 2 blank lines, found 1 |
| 879 | E302 | `tests/test_rpc_security.py` | 89 | expected 2 blank lines, found 1 |
| 878 | E302 | `tests/test_rpc_security.py` | 77 | expected 2 blank lines, found 1 |
| 877 | E302 | `tests/test_rpc_security.py` | 63 | expected 2 blank lines, found 1 |
| 876 | E302 | `tests/test_rpc_security.py` | 52 | expected 2 blank lines, found 1 |
| 875 | E302 | `tests/test_rpc_security.py` | 42 | expected 2 blank lines, found 1 |
| 874 | E302 | `tests/test_rpc_security.py` | 36 | expected 2 blank lines, found 1 |
| 873 | E302 | `tests/test_rpc_security.py` | 28 | expected 2 blank lines, found 1 |
| 872 | E305 | `tests/test_resilience.py` | 434 | expected 2 blank lines after class or function definition, found 1 |
| 871 | E302 | `tests/test_resilience.py` | 402 | expected 2 blank lines, found 1 |
| 870 | E302 | `tests/test_resilience.py` | 362 | expected 2 blank lines, found 1 |
| 869 | E302 | `tests/test_resilience.py` | 304 | expected 2 blank lines, found 1 |
| 868 | E302 | `tests/test_resilience.py` | 259 | expected 2 blank lines, found 1 |
| 867 | E302 | `tests/test_resilience.py` | 176 | expected 2 blank lines, found 1 |
| 866 | E302 | `tests/test_resilience.py` | 39 | expected 2 blank lines, found 1 |
| 865 | E305 | `tests/test_property_based.py` | 449 | expected 2 blank lines after class or function definition, found 1 |
| 864 | E302 | `tests/test_property_based.py` | 407 | expected 2 blank lines, found 1 |
| 863 | E302 | `tests/test_property_based.py` | 361 | expected 2 blank lines, found 1 |
| 862 | E302 | `tests/test_property_based.py` | 301 | expected 2 blank lines, found 1 |
| 861 | E302 | `tests/test_property_based.py` | 243 | expected 2 blank lines, found 1 |
| 860 | E302 | `tests/test_property_based.py` | 202 | expected 2 blank lines, found 1 |
| 859 | E302 | `tests/test_property_based.py` | 180 | expected 2 blank lines, found 1 |
| 858 | E302 | `tests/test_property_based.py` | 157 | expected 2 blank lines, found 1 |
| 857 | E302 | `tests/test_property_based.py` | 119 | expected 2 blank lines, found 1 |
| 856 | E302 | `tests/test_property_based.py` | 101 | expected 2 blank lines, found 1 |
| 855 | E302 | `tests/test_property_based.py` | 86 | expected 2 blank lines, found 1 |
| 854 | E302 | `tests/test_property_based.py` | 70 | expected 2 blank lines, found 1 |
| 853 | E305 | `tests/test_plugin_architecture.py` | 427 | expected 2 blank lines after class or function definition, found 1 |
| 852 | E302 | `tests/test_plugin_architecture.py` | 373 | expected 2 blank lines, found 1 |
| 851 | E302 | `tests/test_plugin_architecture.py` | 356 | expected 2 blank lines, found 1 |
| 850 | E302 | `tests/test_plugin_architecture.py` | 307 | expected 2 blank lines, found 1 |
| 849 | E302 | `tests/test_plugin_architecture.py` | 164 | expected 2 blank lines, found 1 |
| 848 | E302 | `tests/test_plugin_architecture.py` | 130 | expected 2 blank lines, found 1 |
| 847 | E302 | `tests/test_plugin_architecture.py` | 99 | expected 2 blank lines, found 1 |
| 846 | E302 | `tests/test_plugin_architecture.py` | 62 | expected 2 blank lines, found 1 |
| 845 | E302 | `tests/test_plugin_architecture.py` | 24 | expected 2 blank lines, found 1 |
| 844 | E305 | `tests/test_phase6_vnc.py` | 781 | expected 2 blank lines after class or function definition, found 1 |
| 843 | E302 | `tests/test_phase6_vnc.py` | 713 | expected 2 blank lines, found 1 |
| 842 | E302 | `tests/test_phase6_vnc.py` | 640 | expected 2 blank lines, found 1 |
| 841 | E302 | `tests/test_phase6_vnc.py` | 539 | expected 2 blank lines, found 1 |
| 840 | E302 | `tests/test_phase6_vnc.py` | 447 | expected 2 blank lines, found 1 |
| 839 | E302 | `tests/test_phase6_vnc.py` | 366 | expected 2 blank lines, found 1 |
| 838 | E302 | `tests/test_phase6_vnc.py` | 285 | expected 2 blank lines, found 1 |
| 837 | E302 | `tests/test_phase6_vnc.py` | 200 | expected 2 blank lines, found 1 |
| 836 | E302 | `tests/test_phase6_vnc.py` | 105 | expected 2 blank lines, found 1 |
| 835 | E302 | `tests/test_phase6_vnc.py` | 90 | expected 2 blank lines, found 1 |
| 834 | E302 | `tests/test_phase6_vnc.py` | 81 | expected 2 blank lines, found 1 |
| 833 | E302 | `tests/test_phase6_vnc.py` | 66 | expected 2 blank lines, found 1 |
| 832 | E302 | `tests/test_phase6_vnc.py` | 54 | expected 2 blank lines, found 1 |
| 831 | E302 | `tests/test_phase6_vnc.py` | 40 | expected 2 blank lines, found 1 |
| 830 | E302 | `tests/test_phase6_vnc.py` | 27 | expected 2 blank lines, found 1 |
| 829 | E305 | `tests/test_phase6_vm.py` | 742 | expected 2 blank lines after class or function definition, found 1 |
| 828 | E302 | `tests/test_phase6_vm.py` | 658 | expected 2 blank lines, found 1 |
| 827 | E302 | `tests/test_phase6_vm.py` | 601 | expected 2 blank lines, found 1 |
| 826 | E302 | `tests/test_phase6_vm.py` | 504 | expected 2 blank lines, found 1 |
| 825 | E302 | `tests/test_phase6_vm.py` | 407 | expected 2 blank lines, found 1 |
| 824 | E302 | `tests/test_phase6_vm.py` | 320 | expected 2 blank lines, found 1 |
| 823 | E302 | `tests/test_phase6_vm.py` | 230 | expected 2 blank lines, found 1 |
| 822 | E302 | `tests/test_phase6_vm.py` | 118 | expected 2 blank lines, found 1 |
| 821 | E302 | `tests/test_phase6_vm.py` | 106 | expected 2 blank lines, found 1 |
| 820 | E302 | `tests/test_phase6_vm.py` | 94 | expected 2 blank lines, found 1 |
| 819 | E302 | `tests/test_phase6_vm.py` | 80 | expected 2 blank lines, found 1 |
| 818 | E302 | `tests/test_phase6_vm.py` | 69 | expected 2 blank lines, found 1 |
| 817 | E302 | `tests/test_phase6_vm.py` | 55 | expected 2 blank lines, found 1 |
| 816 | E302 | `tests/test_phase6_vm.py` | 43 | expected 2 blank lines, found 1 |
| 815 | E302 | `tests/test_phase6_vm.py` | 34 | expected 2 blank lines, found 1 |
| 814 | E302 | `tests/test_phase6_vm.py` | 26 | expected 2 blank lines, found 1 |
| 813 | E305 | `tests/test_phase6_dns.py` | 517 | expected 2 blank lines after class or function definition, found 1 |
| 812 | E302 | `tests/test_phase6_dns.py` | 479 | expected 2 blank lines, found 1 |
| 811 | E302 | `tests/test_phase6_dns.py` | 446 | expected 2 blank lines, found 1 |
| 810 | E302 | `tests/test_phase6_dns.py` | 398 | expected 2 blank lines, found 1 |
| 809 | E302 | `tests/test_phase6_dns.py` | 335 | expected 2 blank lines, found 1 |
| 808 | E302 | `tests/test_phase6_dns.py` | 293 | expected 2 blank lines, found 1 |
| 807 | E302 | `tests/test_phase6_dns.py` | 225 | expected 2 blank lines, found 1 |
| 806 | E302 | `tests/test_phase6_dns.py` | 178 | expected 2 blank lines, found 1 |
| 805 | E302 | `tests/test_phase6_dns.py` | 105 | expected 2 blank lines, found 1 |
| 804 | E302 | `tests/test_phase6_dns.py` | 45 | expected 2 blank lines, found 1 |
| 803 | E302 | `tests/test_phase6_dns.py` | 36 | expected 2 blank lines, found 1 |
| 802 | E302 | `tests/test_phase6_dns.py` | 31 | expected 2 blank lines, found 1 |
| 801 | E302 | `tests/test_phase6_dns.py` | 26 | expected 2 blank lines, found 1 |
| 800 | E302 | `tests/test_phase6_dns.py` | 21 | expected 2 blank lines, found 1 |
| 799 | E302 | `tests/test_phase6_dns.py` | 15 | expected 2 blank lines, found 1 |
| 798 | E305 | `tests/test_phase6_cloudinit.py` | 436 | expected 2 blank lines after class or function definition, found 1 |
| 797 | E302 | `tests/test_phase6_cloudinit.py` | 393 | expected 2 blank lines, found 1 |
| 796 | E302 | `tests/test_phase6_cloudinit.py` | 365 | expected 2 blank lines, found 1 |
| 795 | E302 | `tests/test_phase6_cloudinit.py` | 337 | expected 2 blank lines, found 1 |
| 794 | E302 | `tests/test_phase6_cloudinit.py` | 298 | expected 2 blank lines, found 1 |
| 793 | E302 | `tests/test_phase6_cloudinit.py` | 240 | expected 2 blank lines, found 1 |
| 792 | E302 | `tests/test_phase6_cloudinit.py` | 187 | expected 2 blank lines, found 1 |
| 791 | E302 | `tests/test_phase6_cloudinit.py` | 107 | expected 2 blank lines, found 1 |
| 790 | E302 | `tests/test_phase6_cloudinit.py` | 60 | expected 2 blank lines, found 1 |
| 789 | E302 | `tests/test_phase6_cloudinit.py` | 46 | expected 2 blank lines, found 1 |
| 788 | E302 | `tests/test_phase6_cloudinit.py` | 35 | expected 2 blank lines, found 1 |
| 787 | E302 | `tests/test_phase6_cloudinit.py` | 21 | expected 2 blank lines, found 1 |
| 786 | E302 | `tests/test_phase6_cloudinit.py` | 15 | expected 2 blank lines, found 1 |
| 785 | E305 | `tests/test_performance_testing.py` | 406 | expected 2 blank lines after class or function definition, found 1 |
| 784 | E302 | `tests/test_performance_testing.py` | 385 | expected 2 blank lines, found 1 |
| 783 | E302 | `tests/test_performance_testing.py` | 235 | expected 2 blank lines, found 1 |
| 782 | E302 | `tests/test_performance_testing.py` | 219 | expected 2 blank lines, found 1 |
| 781 | E302 | `tests/test_performance_testing.py` | 192 | expected 2 blank lines, found 1 |
| 780 | E302 | `tests/test_performance_testing.py` | 143 | expected 2 blank lines, found 1 |
| 779 | E302 | `tests/test_performance_testing.py` | 100 | expected 2 blank lines, found 1 |
| 778 | E302 | `tests/test_performance_testing.py` | 25 | expected 2 blank lines, found 1 |
| 777 | E305 | `tests/test_passthrough.py` | 440 | expected 2 blank lines after class or function definition, found 1 |
| 776 | E302 | `tests/test_passthrough.py` | 409 | expected 2 blank lines, found 1 |
| 775 | E302 | `tests/test_passthrough.py` | 370 | expected 2 blank lines, found 1 |
| 774 | E302 | `tests/test_passthrough.py` | 328 | expected 2 blank lines, found 1 |
| 773 | E302 | `tests/test_passthrough.py` | 274 | expected 2 blank lines, found 1 |
| 772 | E302 | `tests/test_passthrough.py` | 229 | expected 2 blank lines, found 1 |
| 771 | E302 | `tests/test_passthrough.py` | 200 | expected 2 blank lines, found 1 |
| 770 | E302 | `tests/test_passthrough.py` | 150 | expected 2 blank lines, found 1 |
| 769 | E501 | `tests/test_passthrough.py` | 136 | line too long (126 > 120 characters) |
| 768 | E302 | `tests/test_passthrough.py` | 127 | expected 2 blank lines, found 1 |
| 767 | E302 | `tests/test_passthrough.py` | 113 | expected 2 blank lines, found 1 |
| 766 | E302 | `tests/test_passthrough.py` | 102 | expected 2 blank lines, found 1 |
| 765 | E302 | `tests/test_passthrough.py` | 60 | expected 2 blank lines, found 1 |
| 764 | E301 | `tests/test_passthrough.py` | 33 | expected 1 blank line, found 0 |
| 763 | E305 | `tests/test_oidc_oauth2.py` | 394 | expected 2 blank lines after class or function definition, found 1 |
| 762 | E302 | `tests/test_oidc_oauth2.py` | 345 | expected 2 blank lines, found 1 |
| 761 | E302 | `tests/test_oidc_oauth2.py` | 289 | expected 2 blank lines, found 1 |
| 760 | E302 | `tests/test_oidc_oauth2.py` | 235 | expected 2 blank lines, found 1 |
| 759 | E302 | `tests/test_oidc_oauth2.py` | 156 | expected 2 blank lines, found 1 |
| 758 | E302 | `tests/test_oidc_oauth2.py` | 84 | expected 2 blank lines, found 1 |
| 757 | E302 | `tests/test_oidc_oauth2.py` | 24 | expected 2 blank lines, found 1 |
| 756 | E305 | `tests/test_network_backends.py` | 684 | expected 2 blank lines after class or function definition, found 1 |
| 755 | E302 | `tests/test_network_backends.py` | 634 | expected 2 blank lines, found 1 |
| 754 | E302 | `tests/test_network_backends.py` | 568 | expected 2 blank lines, found 1 |
| 753 | E302 | `tests/test_network_backends.py` | 489 | expected 2 blank lines, found 1 |
| 752 | E302 | `tests/test_network_backends.py` | 398 | expected 2 blank lines, found 1 |
| 751 | E302 | `tests/test_network_backends.py` | 316 | expected 2 blank lines, found 1 |
| 750 | E128 | `tests/test_network_backends.py` | 272 | continuation line under-indented for visual indent |
| 749 | E302 | `tests/test_network_backends.py` | 215 | expected 2 blank lines, found 1 |
| 748 | E128 | `tests/test_network_backends.py` | 193 | continuation line under-indented for visual indent |
| 747 | E302 | `tests/test_network_backends.py` | 121 | expected 2 blank lines, found 1 |
| 746 | E302 | `tests/test_network_backends.py` | 109 | expected 2 blank lines, found 1 |
| 745 | E302 | `tests/test_network_backends.py` | 97 | expected 2 blank lines, found 1 |
| 744 | E302 | `tests/test_network_backends.py` | 84 | expected 2 blank lines, found 1 |
| 743 | E302 | `tests/test_network_backends.py` | 71 | expected 2 blank lines, found 1 |
| 742 | E302 | `tests/test_network_backends.py` | 62 | expected 2 blank lines, found 1 |
| 741 | E302 | `tests/test_network_backends.py` | 52 | expected 2 blank lines, found 1 |
| 740 | E302 | `tests/test_network_backends.py` | 41 | expected 2 blank lines, found 1 |
| 739 | E302 | `tests/test_network_backends.py` | 35 | expected 2 blank lines, found 1 |
| 738 | E302 | `tests/test_network_backends.py` | 27 | expected 2 blank lines, found 1 |
| 737 | E305 | `tests/test_netcfg_tui_full.py` | 631 | expected 2 blank lines after class or function definition, found 1 |
| 736 | E302 | `tests/test_netcfg_tui_full.py` | 447 | expected 2 blank lines, found 1 |
| 735 | E302 | `tests/test_netcfg_tui_full.py` | 416 | expected 2 blank lines, found 1 |
| 734 | E302 | `tests/test_netcfg_tui_full.py` | 338 | expected 2 blank lines, found 1 |
| 733 | E302 | `tests/test_netcfg_tui_full.py` | 293 | expected 2 blank lines, found 1 |
| 732 | E302 | `tests/test_netcfg_tui_full.py` | 268 | expected 2 blank lines, found 1 |
| 731 | E302 | `tests/test_netcfg_tui_full.py` | 223 | expected 2 blank lines, found 1 |
| 730 | E302 | `tests/test_netcfg_tui_full.py` | 188 | expected 2 blank lines, found 1 |
| 729 | E302 | `tests/test_netcfg_tui_full.py` | 91 | expected 2 blank lines, found 1 |
| 728 | E302 | `tests/test_netcfg_tui_full.py` | 28 | expected 2 blank lines, found 1 |
| 727 | E305 | `tests/test_netcfg_mock.py` | 620 | expected 2 blank lines after class or function definition, found 1 |
| 726 | E302 | `tests/test_netcfg_mock.py` | 570 | expected 2 blank lines, found 1 |
| 725 | E302 | `tests/test_netcfg_mock.py` | 540 | expected 2 blank lines, found 1 |
| 724 | E302 | `tests/test_netcfg_mock.py` | 514 | expected 2 blank lines, found 1 |
| 723 | E302 | `tests/test_netcfg_mock.py` | 487 | expected 2 blank lines, found 1 |
| 722 | E302 | `tests/test_netcfg_mock.py` | 428 | expected 2 blank lines, found 1 |
| 721 | E302 | `tests/test_netcfg_mock.py` | 361 | expected 2 blank lines, found 1 |
| 720 | E302 | `tests/test_netcfg_mock.py` | 185 | expected 2 blank lines, found 1 |
| 719 | E302 | `tests/test_netcfg_mock.py` | 92 | expected 2 blank lines, found 1 |
| 718 | E302 | `tests/test_netcfg_mock.py` | 39 | expected 2 blank lines, found 1 |
| 717 | E402 | `tests/test_netcfg_mock.py` | 23 | module level import not at top of file |
| 716 | E305 | `tests/test_multiregion.py` | 597 | expected 2 blank lines after class or function definition, found 1 |
| 715 | E302 | `tests/test_multiregion.py` | 507 | expected 2 blank lines, found 1 |
| 714 | E302 | `tests/test_multiregion.py` | 470 | expected 2 blank lines, found 1 |
| 713 | E302 | `tests/test_multiregion.py` | 417 | expected 2 blank lines, found 1 |
| 712 | E302 | `tests/test_multiregion.py` | 337 | expected 2 blank lines, found 1 |
| 711 | E302 | `tests/test_multiregion.py` | 278 | expected 2 blank lines, found 1 |
| 710 | E302 | `tests/test_multiregion.py` | 190 | expected 2 blank lines, found 1 |
| 709 | E302 | `tests/test_multiregion.py` | 147 | expected 2 blank lines, found 1 |
| 708 | E302 | `tests/test_multiregion.py` | 31 | expected 2 blank lines, found 1 |
| 707 | E305 | `tests/test_multi_cluster.py` | 407 | expected 2 blank lines after class or function definition, found 1 |
| 706 | E302 | `tests/test_multi_cluster.py` | 345 | expected 2 blank lines, found 1 |
| 705 | E302 | `tests/test_multi_cluster.py` | 243 | expected 2 blank lines, found 1 |
| 704 | E302 | `tests/test_multi_cluster.py` | 164 | expected 2 blank lines, found 1 |
| 703 | E302 | `tests/test_multi_cluster.py` | 30 | expected 2 blank lines, found 1 |
| 702 | E305 | `tests/test_monitoring.py` | 635 | expected 2 blank lines after class or function definition, found 1 |
| 701 | E302 | `tests/test_monitoring.py` | 598 | expected 2 blank lines, found 1 |
| 700 | E302 | `tests/test_monitoring.py` | 526 | expected 2 blank lines, found 1 |
| 699 | E302 | `tests/test_monitoring.py` | 460 | expected 2 blank lines, found 1 |
| 698 | E302 | `tests/test_monitoring.py` | 377 | expected 2 blank lines, found 1 |
| 697 | E128 | `tests/test_monitoring.py` | 306 | continuation line under-indented for visual indent |
| 696 | E302 | `tests/test_monitoring.py` | 285 | expected 2 blank lines, found 1 |
| 695 | E302 | `tests/test_monitoring.py` | 197 | expected 2 blank lines, found 1 |
| 694 | E128 | `tests/test_monitoring.py` | 155 | continuation line under-indented for visual indent |
| 693 | E302 | `tests/test_monitoring.py` | 102 | expected 2 blank lines, found 1 |
| 692 | E302 | `tests/test_monitoring.py` | 90 | expected 2 blank lines, found 1 |
| 691 | E302 | `tests/test_monitoring.py` | 78 | expected 2 blank lines, found 1 |
| 690 | E302 | `tests/test_monitoring.py` | 66 | expected 2 blank lines, found 1 |
| 689 | E302 | `tests/test_monitoring.py` | 53 | expected 2 blank lines, found 1 |
| 688 | E302 | `tests/test_monitoring.py` | 42 | expected 2 blank lines, found 1 |
| 687 | E302 | `tests/test_monitoring.py` | 32 | expected 2 blank lines, found 1 |
| 686 | E302 | `tests/test_monitoring.py` | 26 | expected 2 blank lines, found 1 |
| 685 | E305 | `tests/test_mock_mode.py` | 664 | expected 2 blank lines after class or function definition, found 1 |
| 684 | E302 | `tests/test_mock_mode.py` | 586 | expected 2 blank lines, found 1 |
| 683 | E302 | `tests/test_mock_mode.py` | 534 | expected 2 blank lines, found 1 |
| 682 | E302 | `tests/test_mock_mode.py` | 500 | expected 2 blank lines, found 1 |
| 681 | E302 | `tests/test_mock_mode.py` | 456 | expected 2 blank lines, found 1 |
| 680 | E302 | `tests/test_mock_mode.py` | 381 | expected 2 blank lines, found 1 |
| 679 | E302 | `tests/test_mock_mode.py` | 347 | expected 2 blank lines, found 1 |
| 678 | E302 | `tests/test_mock_mode.py` | 329 | expected 2 blank lines, found 1 |
| 677 | E302 | `tests/test_mock_mode.py` | 295 | expected 2 blank lines, found 1 |
| 676 | E302 | `tests/test_mock_mode.py` | 261 | expected 2 blank lines, found 1 |
| 675 | E302 | `tests/test_mock_mode.py` | 161 | expected 2 blank lines, found 1 |
| 674 | E302 | `tests/test_mock_mode.py` | 99 | expected 2 blank lines, found 1 |
| 673 | E302 | `tests/test_mock_mode.py` | 41 | expected 2 blank lines, found 1 |
| 672 | E302 | `tests/test_integration_suite.py` | 585 | expected 2 blank lines, found 1 |
| 671 | E302 | `tests/test_integration_suite.py` | 432 | expected 2 blank lines, found 1 |
| 670 | E302 | `tests/test_integration_suite.py` | 314 | expected 2 blank lines, found 1 |
| 669 | E302 | `tests/test_integration_suite.py` | 168 | expected 2 blank lines, found 1 |
| 668 | E302 | `tests/test_integration_suite.py` | 95 | expected 2 blank lines, found 1 |
| 667 | E302 | `tests/test_integration_suite.py` | 63 | expected 2 blank lines, found 1 |
| 666 | E302 | `tests/test_integration_suite.py` | 58 | expected 2 blank lines, found 1 |
| 665 | E302 | `tests/test_integration_suite.py` | 44 | expected 2 blank lines, found 1 |
| 664 | E302 | `tests/test_integration_suite.py` | 37 | expected 2 blank lines, found 1 |
| 663 | E302 | `tests/test_health_detail.py` | 30 | expected 2 blank lines, found 1 |
| 662 | E302 | `tests/test_health_detail.py` | 19 | expected 2 blank lines, found 1 |
| 661 | E302 | `tests/test_health_detail.py` | 4 | expected 2 blank lines, found 1 |
| 660 | E305 | `tests/test_graphql_api.py` | 422 | expected 2 blank lines after class or function definition, found 1 |
| 659 | E302 | `tests/test_graphql_api.py` | 382 | expected 2 blank lines, found 1 |
| 658 | E302 | `tests/test_graphql_api.py` | 327 | expected 2 blank lines, found 1 |
| 657 | E302 | `tests/test_graphql_api.py` | 283 | expected 2 blank lines, found 1 |
| 656 | E302 | `tests/test_graphql_api.py` | 237 | expected 2 blank lines, found 1 |
| 655 | E501 | `tests/test_graphql_api.py` | 212 | line too long (146 > 120 characters) |
| 654 | E302 | `tests/test_graphql_api.py` | 188 | expected 2 blank lines, found 1 |
| 653 | E302 | `tests/test_graphql_api.py` | 121 | expected 2 blank lines, found 1 |
| 652 | E302 | `tests/test_graphql_api.py` | 82 | expected 2 blank lines, found 1 |
| 651 | E302 | `tests/test_graphql_api.py` | 29 | expected 2 blank lines, found 1 |
| 650 | E305 | `tests/test_e2e_testing.py` | 306 | expected 2 blank lines after class or function definition, found 1 |
| 649 | E302 | `tests/test_e2e_testing.py` | 261 | expected 2 blank lines, found 1 |
| 648 | E302 | `tests/test_e2e_testing.py` | 171 | expected 2 blank lines, found 1 |
| 647 | E302 | `tests/test_e2e_testing.py` | 149 | expected 2 blank lines, found 1 |
| 646 | E302 | `tests/test_e2e_testing.py` | 115 | expected 2 blank lines, found 1 |
| 645 | E302 | `tests/test_e2e_testing.py` | 89 | expected 2 blank lines, found 1 |
| 644 | E302 | `tests/test_e2e_testing.py` | 60 | expected 2 blank lines, found 1 |
| 643 | E302 | `tests/test_e2e_testing.py` | 24 | expected 2 blank lines, found 1 |
| 642 | E305 | `tests/test_distributed_tracing.py` | 429 | expected 2 blank lines after class or function definition, found 1 |
| 641 | E302 | `tests/test_distributed_tracing.py` | 375 | expected 2 blank lines, found 1 |
| 640 | E302 | `tests/test_distributed_tracing.py` | 338 | expected 2 blank lines, found 1 |
| 639 | E302 | `tests/test_distributed_tracing.py` | 301 | expected 2 blank lines, found 1 |
| 638 | E302 | `tests/test_distributed_tracing.py` | 264 | expected 2 blank lines, found 1 |
| 637 | E302 | `tests/test_distributed_tracing.py` | 190 | expected 2 blank lines, found 1 |
| 636 | E302 | `tests/test_distributed_tracing.py` | 124 | expected 2 blank lines, found 1 |
| 635 | E302 | `tests/test_distributed_tracing.py` | 80 | expected 2 blank lines, found 1 |
| 634 | E302 | `tests/test_distributed_tracing.py` | 26 | expected 2 blank lines, found 1 |
| 633 | E305 | `tests/test_diagnostics.py` | 282 | expected 2 blank lines after class or function definition, found 1 |
| 632 | E302 | `tests/test_diagnostics.py` | 260 | expected 2 blank lines, found 1 |
| 631 | E302 | `tests/test_diagnostics.py` | 244 | expected 2 blank lines, found 1 |
| 630 | E302 | `tests/test_diagnostics.py` | 31 | expected 2 blank lines, found 1 |
| 629 | E302 | `tests/test_dashboard.py` | 28 | expected 2 blank lines, found 1 |
| 628 | E302 | `tests/test_dashboard.py` | 20 | expected 2 blank lines, found 1 |
| 627 | E302 | `tests/test_dashboard.py` | 15 | expected 2 blank lines, found 1 |
| 626 | E302 | `tests/test_dashboard.py` | 11 | expected 2 blank lines, found 1 |
| 625 | E302 | `tests/test_dashboard.py` | 5 | expected 2 blank lines, found 1 |
| 624 | E302 | `tests/test_cost_optimization.py` | 57 | expected 2 blank lines, found 1 |
| 623 | E302 | `tests/test_cost_optimization.py` | 50 | expected 2 blank lines, found 1 |
| 622 | E302 | `tests/test_cost_optimization.py` | 43 | expected 2 blank lines, found 1 |
| 621 | E302 | `tests/test_cost_optimization.py` | 36 | expected 2 blank lines, found 1 |
| 620 | E302 | `tests/test_cost_optimization.py` | 28 | expected 2 blank lines, found 1 |
| 619 | E302 | `tests/test_cost_optimization.py` | 8 | expected 2 blank lines, found 1 |
| 618 | E302 | `tests/test_cost_optimization.py` | 4 | expected 2 blank lines, found 1 |
| 617 | E305 | `tests/test_contracts.py` | 702 | expected 2 blank lines after class or function definition, found 1 |
| 616 | E501 | `tests/test_contracts.py` | 662 | line too long (126 > 120 characters) |
| 615 | E302 | `tests/test_contracts.py` | 656 | expected 2 blank lines, found 1 |
| 614 | E302 | `tests/test_contracts.py` | 619 | expected 2 blank lines, found 1 |
| 613 | E302 | `tests/test_contracts.py` | 569 | expected 2 blank lines, found 1 |
| 612 | E302 | `tests/test_contracts.py` | 481 | expected 2 blank lines, found 1 |
| 611 | E302 | `tests/test_contracts.py` | 321 | expected 2 blank lines, found 1 |
| 610 | E302 | `tests/test_contracts.py` | 238 | expected 2 blank lines, found 1 |
| 609 | E302 | `tests/test_contracts.py` | 234 | expected 2 blank lines, found 1 |
| 608 | E302 | `tests/test_contracts.py` | 168 | expected 2 blank lines, found 1 |
| 607 | E302 | `tests/test_contracts.py` | 155 | expected 2 blank lines, found 1 |
| 606 | E302 | `tests/test_contracts.py` | 146 | expected 2 blank lines, found 1 |
| 605 | E302 | `tests/test_contracts.py` | 138 | expected 2 blank lines, found 1 |
| 604 | E302 | `tests/test_contracts.py` | 128 | expected 2 blank lines, found 1 |
| 603 | E302 | `tests/test_contracts.py` | 108 | expected 2 blank lines, found 1 |
| 602 | E302 | `tests/test_contracts.py` | 91 | expected 2 blank lines, found 1 |
| 601 | E302 | `tests/test_contracts.py` | 82 | expected 2 blank lines, found 1 |
| 600 | E302 | `tests/test_contracts.py` | 69 | expected 2 blank lines, found 1 |
| 599 | E302 | `tests/test_contracts.py` | 60 | expected 2 blank lines, found 1 |
| 598 | E302 | `tests/test_contracts.py` | 50 | expected 2 blank lines, found 1 |
| 597 | E302 | `tests/test_contracts.py` | 37 | expected 2 blank lines, found 1 |
| 596 | E302 | `tests/test_contracts.py` | 29 | expected 2 blank lines, found 1 |
| 595 | E741 | `tests/test_compliance.py` | 59 | ambiguous variable name 'l' |
| 594 | E302 | `tests/test_compliance.py` | 43 | expected 2 blank lines, found 1 |
| 593 | E741 | `tests/test_compliance.py` | 41 | ambiguous variable name 'l' |
| 592 | E302 | `tests/test_compliance.py` | 37 | expected 2 blank lines, found 1 |
| 591 | E302 | `tests/test_compliance.py` | 30 | expected 2 blank lines, found 1 |
| 590 | E302 | `tests/test_compliance.py` | 19 | expected 2 blank lines, found 1 |
| 589 | E302 | `tests/test_compliance.py` | 15 | expected 2 blank lines, found 1 |
| 588 | E302 | `tests/test_compliance.py` | 8 | expected 2 blank lines, found 1 |
| 587 | E302 | `tests/test_compliance.py` | 4 | expected 2 blank lines, found 1 |
| 586 | E305 | `tests/test_cli_wrappers.py` | 429 | expected 2 blank lines after class or function definition, found 1 |
| 585 | E302 | `tests/test_cli_wrappers.py` | 392 | expected 2 blank lines, found 1 |
| 584 | E302 | `tests/test_cli_wrappers.py` | 337 | expected 2 blank lines, found 1 |
| 583 | E302 | `tests/test_cli_wrappers.py` | 224 | expected 2 blank lines, found 1 |
| 582 | E302 | `tests/test_cli_wrappers.py` | 120 | expected 2 blank lines, found 1 |
| 581 | E302 | `tests/test_cli_wrappers.py` | 23 | expected 2 blank lines, found 1 |
| 580 | E305 | `tests/test_chaos_engineering.py` | 736 | expected 2 blank lines after class or function definition, found 1 |
| 579 | E302 | `tests/test_chaos_engineering.py` | 713 | expected 2 blank lines, found 1 |
| 578 | E302 | `tests/test_chaos_engineering.py` | 680 | expected 2 blank lines, found 1 |
| 577 | E302 | `tests/test_chaos_engineering.py` | 633 | expected 2 blank lines, found 1 |
| 576 | E302 | `tests/test_chaos_engineering.py` | 599 | expected 2 blank lines, found 1 |
| 575 | E302 | `tests/test_chaos_engineering.py` | 529 | expected 2 blank lines, found 1 |
| 574 | E302 | `tests/test_chaos_engineering.py` | 458 | expected 2 blank lines, found 1 |
| 573 | E302 | `tests/test_chaos_engineering.py` | 387 | expected 2 blank lines, found 1 |
| 572 | E302 | `tests/test_chaos_engineering.py` | 378 | expected 2 blank lines, found 1 |
| 571 | E302 | `tests/test_chaos_engineering.py` | 373 | expected 2 blank lines, found 1 |
| 570 | E302 | `tests/test_chaos_engineering.py` | 368 | expected 2 blank lines, found 1 |
| 569 | E302 | `tests/test_chaos_engineering.py` | 355 | expected 2 blank lines, found 1 |
| 568 | E302 | `tests/test_chaos_engineering.py` | 231 | expected 2 blank lines, found 1 |
| 567 | E302 | `tests/test_chaos_engineering.py` | 202 | expected 2 blank lines, found 1 |
| 566 | E302 | `tests/test_chaos_engineering.py` | 154 | expected 2 blank lines, found 1 |
| 565 | E302 | `tests/test_chaos_engineering.py` | 114 | expected 2 blank lines, found 1 |
| 564 | E302 | `tests/test_chaos_engineering.py` | 93 | expected 2 blank lines, found 1 |
| 563 | E302 | `tests/test_chaos_engineering.py` | 76 | expected 2 blank lines, found 1 |
| 562 | E302 | `tests/test_chaos_engineering.py` | 60 | expected 2 blank lines, found 1 |
| 561 | E302 | `tests/test_chaos_engineering.py` | 47 | expected 2 blank lines, found 1 |
| 560 | E302 | `tests/test_chaos_engineering.py` | 37 | expected 2 blank lines, found 1 |
| 559 | E305 | `tests/test_backup_service.py` | 717 | expected 2 blank lines after class or function definition, found 1 |
| 558 | E302 | `tests/test_backup_service.py` | 661 | expected 2 blank lines, found 1 |
| 557 | E302 | `tests/test_backup_service.py` | 605 | expected 2 blank lines, found 1 |
| 556 | E302 | `tests/test_backup_service.py` | 535 | expected 2 blank lines, found 1 |
| 555 | E302 | `tests/test_backup_service.py` | 479 | expected 2 blank lines, found 1 |
| 554 | E302 | `tests/test_backup_service.py` | 396 | expected 2 blank lines, found 1 |
| 553 | E302 | `tests/test_backup_service.py` | 341 | expected 2 blank lines, found 1 |
| 552 | E302 | `tests/test_backup_service.py` | 298 | expected 2 blank lines, found 1 |
| 551 | E302 | `tests/test_backup_service.py` | 217 | expected 2 blank lines, found 1 |
| 550 | E302 | `tests/test_backup_service.py` | 162 | expected 2 blank lines, found 1 |
| 549 | E302 | `tests/test_backup_service.py` | 148 | expected 2 blank lines, found 1 |
| 548 | E302 | `tests/test_backup_service.py` | 114 | expected 2 blank lines, found 1 |
| 547 | E302 | `tests/test_backup_service.py` | 67 | expected 2 blank lines, found 1 |
| 546 | E302 | `tests/test_backup_service.py` | 57 | expected 2 blank lines, found 1 |
| 545 | E305 | `tests/test_api_versioning.py` | 515 | expected 2 blank lines after class or function definition, found 1 |
| 544 | E302 | `tests/test_api_versioning.py` | 470 | expected 2 blank lines, found 1 |
| 543 | E302 | `tests/test_api_versioning.py` | 424 | expected 2 blank lines, found 1 |
| 542 | E302 | `tests/test_api_versioning.py` | 381 | expected 2 blank lines, found 1 |
| 541 | E501 | `tests/test_api_versioning.py` | 335 | line too long (132 > 120 characters) |
| 540 | E302 | `tests/test_api_versioning.py` | 307 | expected 2 blank lines, found 1 |
| 539 | E302 | `tests/test_api_versioning.py` | 196 | expected 2 blank lines, found 1 |
| 538 | E731 | `tests/test_api_versioning.py` | 166 | do not assign a lambda expression, use a def |
| 537 | E731 | `tests/test_api_versioning.py` | 165 | do not assign a lambda expression, use a def |
| 536 | E302 | `tests/test_api_versioning.py` | 144 | expected 2 blank lines, found 1 |
| 535 | E302 | `tests/test_api_versioning.py` | 113 | expected 2 blank lines, found 1 |
| 534 | E302 | `tests/test_api_versioning.py` | 31 | expected 2 blank lines, found 1 |
| 533 | E302 | `tests/test_api_key_manager.py` | 353 | expected 2 blank lines, found 1 |
| 532 | E302 | `tests/test_api_key_manager.py` | 316 | expected 2 blank lines, found 1 |
| 531 | E302 | `tests/test_api_key_manager.py` | 271 | expected 2 blank lines, found 1 |
| 530 | E302 | `tests/test_api_key_manager.py` | 230 | expected 2 blank lines, found 1 |
| 529 | E302 | `tests/test_api_key_manager.py` | 187 | expected 2 blank lines, found 1 |
| 528 | E302 | `tests/test_api_key_manager.py` | 161 | expected 2 blank lines, found 1 |
| 527 | E302 | `tests/test_api_key_manager.py` | 92 | expected 2 blank lines, found 1 |
| 526 | E302 | `tests/test_api_key_manager.py` | 40 | expected 2 blank lines, found 1 |
| 525 | E302 | `tests/test_api_key_manager.py` | 29 | expected 2 blank lines, found 1 |
| 524 | E302 | `tests/test_api_key_manager.py` | 22 | expected 2 blank lines, found 1 |
| 523 | E305 | `tests/test_anomaly.py` | 689 | expected 2 blank lines after class or function definition, found 1 |
| 522 | E302 | `tests/test_anomaly.py` | 645 | expected 2 blank lines, found 1 |
| 521 | E302 | `tests/test_anomaly.py` | 564 | expected 2 blank lines, found 1 |
| 520 | E302 | `tests/test_anomaly.py` | 531 | expected 2 blank lines, found 1 |
| 519 | E302 | `tests/test_anomaly.py` | 489 | expected 2 blank lines, found 1 |
| 518 | E302 | `tests/test_anomaly.py` | 390 | expected 2 blank lines, found 1 |
| 517 | E302 | `tests/test_anomaly.py` | 314 | expected 2 blank lines, found 1 |
| 516 | E302 | `tests/test_anomaly.py` | 282 | expected 2 blank lines, found 1 |
| 515 | E302 | `tests/test_anomaly.py` | 239 | expected 2 blank lines, found 1 |
| 514 | E302 | `tests/test_anomaly.py` | 160 | expected 2 blank lines, found 1 |
| 513 | E302 | `tests/test_anomaly.py` | 90 | expected 2 blank lines, found 1 |
| 512 | E302 | `tests/test_anomaly.py` | 30 | expected 2 blank lines, found 1 |
| 511 | E305 | `tests/test_analytics.py` | 258 | expected 2 blank lines after class or function definition, found 1 |
| 510 | E302 | `tests/test_analytics.py` | 223 | expected 2 blank lines, found 1 |
| 509 | E302 | `tests/test_analytics.py` | 25 | expected 2 blank lines, found 1 |
| 508 | E305 | `tests/test_advanced_features.py` | 547 | expected 2 blank lines after class or function definition, found 1 |
| 507 | E302 | `tests/test_advanced_features.py` | 423 | expected 2 blank lines, found 1 |
| 506 | E731 | `tests/test_advanced_features.py` | 378 | do not assign a lambda expression, use a def |
| 505 | E302 | `tests/test_advanced_features.py` | 369 | expected 2 blank lines, found 1 |
| 504 | E302 | `tests/test_advanced_features.py` | 337 | expected 2 blank lines, found 1 |
| 503 | E302 | `tests/test_advanced_features.py` | 279 | expected 2 blank lines, found 1 |
| 502 | E731 | `tests/test_advanced_features.py` | 200 | do not assign a lambda expression, use a def |
| 501 | E302 | `tests/test_advanced_features.py` | 166 | expected 2 blank lines, found 1 |
| 500 | E302 | `tests/test_advanced_features.py` | 132 | expected 2 blank lines, found 1 |
| 499 | E302 | `tests/test_advanced_features.py` | 104 | expected 2 blank lines, found 1 |
| 498 | E302 | `tests/test_advanced_features.py` | 60 | expected 2 blank lines, found 1 |
| 497 | E302 | `tests/test_advanced_features.py` | 27 | expected 2 blank lines, found 1 |
| 496 | E305 | `tests/test_advanced_documentation.py` | 551 | expected 2 blank lines after class or function definition, found 1 |
| 495 | E302 | `tests/test_advanced_documentation.py` | 354 | expected 2 blank lines, found 1 |
| 494 | E302 | `tests/test_advanced_documentation.py` | 311 | expected 2 blank lines, found 1 |
| 493 | E302 | `tests/test_advanced_documentation.py` | 271 | expected 2 blank lines, found 1 |
| 492 | E302 | `tests/test_advanced_documentation.py` | 238 | expected 2 blank lines, found 1 |
| 491 | E302 | `tests/test_advanced_documentation.py` | 203 | expected 2 blank lines, found 1 |
| 490 | E302 | `tests/test_advanced_documentation.py` | 104 | expected 2 blank lines, found 1 |
| 489 | E302 | `tests/test_advanced_documentation.py` | 63 | expected 2 blank lines, found 1 |
| 488 | E302 | `tests/test_advanced_documentation.py` | 28 | expected 2 blank lines, found 1 |
| 487 | E305 | `scripts/test_anchors.py` | 18 | expected 2 blank lines after class or function definition, found 1 |
| 486 | E302 | `scripts/test_anchors.py` | 5 | expected 2 blank lines, found 1 |
| 485 | E305 | `scripts/fix_markdown_lint_comprehensive.py` | 286 | expected 2 blank lines after class or function definition, found 1 |
| 484 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 268 | expected 2 blank lines, found 1 |
| 483 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 249 | expected 2 blank lines, found 1 |
| 482 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 237 | expected 2 blank lines, found 1 |
| 481 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 229 | expected 2 blank lines, found 1 |
| 480 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 221 | expected 2 blank lines, found 1 |
| 479 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 203 | expected 2 blank lines, found 1 |
| 478 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 189 | expected 2 blank lines, found 1 |
| 477 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 176 | expected 2 blank lines, found 1 |
| 476 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 161 | expected 2 blank lines, found 1 |
| 475 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 145 | expected 2 blank lines, found 1 |
| 474 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 131 | expected 2 blank lines, found 1 |
| 473 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 127 | expected 2 blank lines, found 1 |
| 472 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 114 | expected 2 blank lines, found 1 |
| 471 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 107 | expected 2 blank lines, found 1 |
| 470 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 95 | expected 2 blank lines, found 1 |
| 469 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 70 | expected 2 blank lines, found 1 |
| 468 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 44 | expected 2 blank lines, found 1 |
| 467 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 30 | expected 2 blank lines, found 1 |
| 466 | E302 | `scripts/fix_markdown_lint_comprehensive.py` | 10 | expected 2 blank lines, found 1 |
| 465 | E305 | `scripts/fix_datetime.py` | 59 | expected 2 blank lines after class or function definition, found 1 |
| 464 | E302 | `scripts/fix_datetime.py` | 40 | expected 2 blank lines, found 1 |
| 463 | E302 | `scripts/fix_datetime.py` | 4 | expected 2 blank lines, found 1 |
| 462 | E305 | `scripts/debug_anchors.py` | 16 | expected 2 blank lines after class or function definition, found 1 |
| 461 | E302 | `scripts/debug_anchors.py` | 4 | expected 2 blank lines, found 1 |
| 460 | E305 | `scripts/clean_test_imports.py` | 66 | expected 2 blank lines after class or function definition, found 1 |
| 459 | E302 | `scripts/clean_test_imports.py` | 51 | expected 2 blank lines, found 1 |
| 458 | E302 | `scripts/clean_test_imports.py` | 12 | expected 2 blank lines, found 1 |
| 457 | E501 | `scripts/actions_inspector.py` | 366 | line too long (121 > 120 characters) |
| 456 | E501 | `scripts/actions_inspector.py` | 286 | line too long (129 > 120 characters) |
| 455 | E501 | `scripts/actions_inspector.py` | 268 | line too long (121 > 120 characters) |
| 454 | E302 | `scripts/actions_inspector.py` | 243 | expected 2 blank lines, found 1 |
| 453 | E302 | `scripts/actions_inspector.py` | 206 | expected 2 blank lines, found 1 |
| 452 | E302 | `scripts/actions_inspector.py` | 166 | expected 2 blank lines, found 1 |
| 451 | E302 | `scripts/actions_inspector.py` | 155 | expected 2 blank lines, found 1 |
| 450 | E302 | `scripts/actions_inspector.py` | 152 | expected 2 blank lines, found 1 |
| 449 | E702 | `scripts/actions_inspector.py` | 149 | multiple statements on one line (semicolon) |
| 448 | E702 | `scripts/actions_inspector.py` | 147 | multiple statements on one line (semicolon) |
| 447 | E501 | `scripts/actions_inspector.py` | 145 | line too long (122 > 120 characters) |
| 446 | E702 | `scripts/actions_inspector.py` | 145 | multiple statements on one line (semicolon) |
| 445 | E702 | `scripts/actions_inspector.py` | 114 | multiple statements on one line (semicolon) |
| 444 | E702 | `scripts/actions_inspector.py` | 109 | multiple statements on one line (semicolon) |
| 443 | E231 | `scripts/actions_inspector.py` | 109 | missing whitespace after ',' |
| 442 | E702 | `scripts/actions_inspector.py` | 107 | multiple statements on one line (semicolon) |
| 441 | E231 | `scripts/actions_inspector.py` | 107 | missing whitespace after ',' |
| 440 | E302 | `passthrough_manager.py` | 29 | expected 2 blank lines, found 1 |
| 439 | E302 | `passthrough_manager.py` | 23 | expected 2 blank lines, found 1 |
| 438 | E302 | `passthrough_manager.py` | 14 | expected 2 blank lines, found 1 |
| 437 | E302 | `passthrough_manager.py` | 4 | expected 2 blank lines, found 1 |
| 436 | E128 | `opt/webhook_system.py` | 463 | continuation line under-indented for visual indent |
| 435 | E128 | `opt/webhook_system.py` | 462 | continuation line under-indented for visual indent |
| 434 | E128 | `opt/webhook_system.py` | 341 | continuation line under-indented for visual indent |
| 433 | E128 | `opt/webhook_system.py` | 319 | continuation line under-indented for visual indent |
| 432 | E128 | `opt/webhook_system.py` | 183 | continuation line under-indented for visual indent |
| 431 | E402 | `opt/web/panel/validation/schemas.py` | 526 | module level import not at top of file |
| 430 | E402 | `opt/web/panel/validation/schemas.py` | 525 | module level import not at top of file |
| 429 | E501 | `opt/web/panel/validation/schemas.py` | 32 | line too long (127 > 120 characters) |
| 428 | E127 | `opt/web/panel/security.py` | 366 | continuation line over-indented for visual indent |
| 427 | E127 | `opt/web/panel/security.py` | 364 | continuation line over-indented for visual indent |
| 426 | E501 | `opt/web/panel/reporting.py` | 483 | line too long (124 > 120 characters) |
| 425 | E501 | `opt/web/panel/reporting.py` | 482 | line too long (121 > 120 characters) |
| 424 | E501 | `opt/web/panel/reporting.py` | 478 | line too long (137 > 120 characters) |
| 423 | E501 | `opt/web/panel/reporting.py` | 477 | line too long (134 > 120 characters) |
| 422 | E501 | `opt/web/panel/reporting.py` | 255 | line too long (124 > 120 characters) |
| 421 | E501 | `opt/web/panel/reporting.py` | 251 | line too long (121 > 120 characters) |
| 420 | E501 | `opt/web/panel/models/user.py` | 35 | line too long (128 > 120 characters) |
| 419 | E501 | `opt/web/panel/models/snapshot.py` | 45 | line too long (128 > 120 characters) |
| 418 | E501 | `opt/web/panel/models/node.py` | 41 | line too long (128 > 120 characters) |
| 417 | E128 | `opt/web/panel/core/rpc_client.py` | 623 | continuation line under-indented for visual indent |
| 416 | E128 | `opt/web/panel/core/rpc_client.py` | 577 | continuation line under-indented for visual indent |
| 415 | E128 | `opt/web/panel/core/rpc_client.py` | 543 | continuation line under-indented for visual indent |
| 414 | E128 | `opt/web/panel/core/rpc_client.py` | 458 | continuation line under-indented for visual indent |
| 413 | E128 | `opt/web/panel/core/rpc_client.py` | 457 | continuation line under-indented for visual indent |
| 412 | E128 | `opt/web/panel/core/rpc_client.py` | 456 | continuation line under-indented for visual indent |
| 411 | E127 | `opt/web/panel/core/rpc_client.py` | 223 | continuation line over-indented for visual indent |
| 410 | E501 | `opt/web/panel/auth_2fa.py` | 538 | line too long (154 > 120 characters) |
| 409 | E501 | `opt/web/panel/app.py` | 623 | line too long (139 > 120 characters) |
| 408 | E231 | `opt/web/panel/app.py` | 623 | missing whitespace after ',' |
| 407 | E231 | `opt/web/panel/app.py` | 623 | missing whitespace after ',' |
| 406 | E231 | `opt/web/panel/app.py` | 604 | missing whitespace after ',' |
| 405 | E231 | `opt/web/panel/app.py` | 604 | missing whitespace after ',' |
| 404 | E231 | `opt/web/panel/app.py` | 489 | missing whitespace after ',' |
| 403 | E231 | `opt/web/panel/app.py` | 489 | missing whitespace after ',' |
| 402 | E501 | `opt/web/panel/app.py` | 191 | line too long (125 > 120 characters) |
| 401 | E501 | `opt/web/panel/api_versioning.py` | 415 | line too long (122 > 120 characters) |
| 400 | E501 | `opt/web/panel/api_versioning.py` | 200 | line too long (138 > 120 characters) |
| 399 | E261 | `opt/web/panel/api_versioning.py` | 36 | at least two spaces before inline comment |
| 398 | E302 | `opt/web/dashboard/app.py` | 23 | expected 2 blank lines, found 1 |
| 397 | E302 | `opt/web/dashboard/app.py` | 12 | expected 2 blank lines, found 1 |
| 396 | E302 | `opt/web/dashboard/app.py` | 8 | expected 2 blank lines, found 1 |
| 395 | E305 | `opt/tools/first_boot_keygen.py` | 133 | expected 2 blank lines after class or function definition, found 1 |
| 394 | E302 | `opt/tools/first_boot_keygen.py` | 113 | expected 2 blank lines, found 1 |
| 393 | E302 | `opt/tools/first_boot_keygen.py` | 89 | expected 2 blank lines, found 1 |
| 392 | E302 | `opt/tools/first_boot_keygen.py` | 52 | expected 2 blank lines, found 1 |
| 391 | E302 | `opt/tools/first_boot_keygen.py` | 34 | expected 2 blank lines, found 1 |
| 390 | E402 | `opt/tools/first_boot_keygen.py` | 26 | module level import not at top of file |
| 389 | E305 | `opt/tools/debvisor_menu.py` | 143 | expected 2 blank lines after class or function definition, found 1 |
| 388 | E501 | `opt/tools/debvisor_menu.py` | 77 | line too long (132 > 120 characters) |
| 387 | E302 | `opt/tools/debvisor_menu.py` | 68 | expected 2 blank lines, found 1 |
| 386 | E261 | `opt/tools/debvisor_menu.py` | 66 | at least two spaces before inline comment |
| 385 | E302 | `opt/tools/debvisor_menu.py` | 59 | expected 2 blank lines, found 1 |
| 384 | E302 | `opt/tools/debvisor_menu.py` | 54 | expected 2 blank lines, found 1 |
| 383 | E302 | `opt/tools/debvisor_menu.py` | 43 | expected 2 blank lines, found 1 |
| 382 | E302 | `opt/tools/debvisor_menu.py` | 33 | expected 2 blank lines, found 1 |
| 381 | E302 | `opt/testing/mock_mode.py` | 1255 | expected 2 blank lines, found 1 |
| 380 | E302 | `opt/testing/mock_mode.py` | 1251 | expected 2 blank lines, found 1 |
| 379 | E302 | `opt/testing/mock_mode.py` | 1241 | expected 2 blank lines, found 1 |
| 378 | E501 | `opt/testing/mock_mode.py` | 1202 | line too long (124 > 120 characters) |
| 377 | E302 | `opt/testing/mock_mode.py` | 1074 | expected 2 blank lines, found 1 |
| 376 | E302 | `opt/testing/mock_mode.py` | 1066 | expected 2 blank lines, found 1 |
| 375 | E302 | `opt/testing/mock_mode.py` | 1063 | expected 2 blank lines, found 1 |
| 374 | E302 | `opt/testing/mock_mode.py` | 1060 | expected 2 blank lines, found 1 |
| 373 | E501 | `opt/testing/mock_mode.py` | 1058 | line too long (123 > 120 characters) |
| 372 | E501 | `opt/testing/mock_mode.py` | 1053 | line too long (135 > 120 characters) |
| 371 | E501 | `opt/testing/mock_mode.py` | 1042 | line too long (173 > 120 characters) |
| 370 | E501 | `opt/testing/mock_mode.py` | 1041 | line too long (173 > 120 characters) |
| 369 | E501 | `opt/testing/mock_mode.py` | 1040 | line too long (196 > 120 characters) |
| 368 | E302 | `opt/testing/mock_mode.py` | 1026 | expected 2 blank lines, found 1 |
| 367 | E301 | `opt/testing/mock_mode.py` | 1021 | expected 1 blank line, found 0 |
| 366 | E302 | `opt/testing/mock_mode.py` | 1019 | expected 2 blank lines, found 1 |
| 365 | E302 | `opt/testing/mock_mode.py` | 992 | expected 2 blank lines, found 1 |
| 364 | E302 | `opt/testing/mock_mode.py` | 985 | expected 2 blank lines, found 1 |
| 363 | E302 | `opt/testing/mock_mode.py` | 981 | expected 2 blank lines, found 1 |
| 362 | E302 | `opt/testing/mock_mode.py` | 973 | expected 2 blank lines, found 1 |
| 361 | E402 | `opt/testing/mock_mode.py` | 971 | module level import not at top of file |
| 360 | E402 | `opt/testing/mock_mode.py` | 970 | module level import not at top of file |
| 359 | E402 | `opt/testing/mock_mode.py` | 969 | module level import not at top of file |
| 358 | E402 | `opt/testing/mock_mode.py` | 968 | module level import not at top of file |
| 357 | E402 | `opt/testing/mock_mode.py` | 957 | module level import not at top of file |
| 356 | E261 | `opt/testing/mock_mode.py` | 53 | at least two spaces before inline comment |
| 355 | E302 | `opt/testing/mock_mode.py` | 48 | expected 2 blank lines, found 1 |
| 354 | E501 | `opt/system/passthrough_manager.py` | 240 | line too long (123 > 120 characters) |
| 353 | E305 | `opt/system/passthrough_manager.py` | 229 | expected 2 blank lines after class or function definition, found 1 |
| 352 | E302 | `opt/system/passthrough_manager.py` | 47 | expected 2 blank lines, found 1 |
| 351 | E302 | `opt/system/passthrough_manager.py` | 41 | expected 2 blank lines, found 1 |
| 350 | E302 | `opt/system/passthrough_manager.py` | 31 | expected 2 blank lines, found 1 |
| 349 | E302 | `opt/system/passthrough_manager.py` | 21 | expected 2 blank lines, found 1 |
| 348 | E302 | `opt/system/hypervisor/xen_driver.py` | 35 | expected 2 blank lines, found 1 |
| 347 | E129 | `opt/system/hardware_detection.py` | 401 | visually indented line with same indent as next logical line |
| 346 | E501 | `opt/system/hardware_detection.py` | 244 | line too long (124 > 120 characters) |
| 345 | E261 | `opt/system/hardware_detection.py` | 43 | at least two spaces before inline comment |
| 344 | E501 | `opt/services/tracing.py` | 484 | line too long (124 > 120 characters) |
| 343 | E501 | `opt/services/tracing.py` | 483 | line too long (122 > 120 characters) |
| 342 | E301 | `opt/services/slo_tracking.py` | 1244 | expected 1 blank line, found 0 |
| 341 | E402 | `opt/services/slo_tracking.py` | 798 | module level import not at top of file |
| 340 | E501 | `opt/services/slo_tracking.py` | 786 | line too long (122 > 120 characters) |
| 339 | E722 | `opt/services/slo_tracking.py` | 521 | do not use bare 'except' |
| 338 | E501 | `opt/services/security/firewall_manager.py` | 978 | line too long (125 > 120 characters) |
| 337 | E128 | `opt/services/security/firewall_manager.py` | 513 | continuation line under-indented for visual indent |
| 336 | E128 | `opt/services/security/firewall_manager.py` | 512 | continuation line under-indented for visual indent |
| 335 | E128 | `opt/services/security/firewall_manager.py` | 511 | continuation line under-indented for visual indent |
| 334 | E402 | `opt/services/security/cert_pinning.py` | 423 | module level import not at top of file |
| 333 | E501 | `opt/services/security/acme_certificates.py` | 796 | line too long (130 > 120 characters) |
| 332 | E501 | `opt/services/security/acme_certificates.py` | 770 | line too long (186 > 120 characters) |
| 331 | E127 | `opt/services/security/acme_certificates.py` | 414 | continuation line over-indented for visual indent |
| 330 | E128 | `opt/services/sdn/sdn_controller.py` | 683 | continuation line under-indented for visual indent |
| 329 | E128 | `opt/services/scheduler/cli.py` | 157 | continuation line under-indented for visual indent |
| 328 | E128 | `opt/services/scheduler/cli.py` | 148 | continuation line under-indented for visual indent |
| 327 | E128 | `opt/services/scheduler/cli.py` | 137 | continuation line under-indented for visual indent |
| 326 | E128 | `opt/services/scheduler/cli.py` | 128 | continuation line under-indented for visual indent |
| 325 | E128 | `opt/services/scheduler/cli.py` | 122 | continuation line under-indented for visual indent |
| 324 | E128 | `opt/services/scheduler/cli.py` | 105 | continuation line under-indented for visual indent |
| 323 | E128 | `opt/services/scheduler/cli.py` | 99 | continuation line under-indented for visual indent |
| 322 | E128 | `opt/services/scheduler/cli.py` | 92 | continuation line under-indented for visual indent |
| 321 | E128 | `opt/services/scheduler/cli.py` | 85 | continuation line under-indented for visual indent |
| 320 | E402 | `opt/services/rpc/validators.py` | 393 | module level import not at top of file |
| 319 | E722 | `opt/services/rpc/validators.py` | 387 | do not use bare 'except' |
| 318 | E722 | `opt/services/rpc/validators.py` | 309 | do not use bare 'except' |
| 317 | E501 | `opt/services/rpc/validators.py` | 25 | line too long (128 > 120 characters) |
| 316 | E128 | `opt/services/rpc/server.py` | 350 | continuation line under-indented for visual indent |
| 315 | E501 | `opt/services/rpc/server.py` | 228 | line too long (126 > 120 characters) |
| 314 | E501 | `opt/services/rpc/server.py` | 69 | line too long (142 > 120 characters) |
| 313 | E722 | `opt/services/rpc/cert_manager.py` | 196 | do not use bare 'except' |
| 312 | E722 | `opt/services/rpc/cert_manager.py` | 193 | do not use bare 'except' |
| 311 | E261 | `opt/services/rpc/authz.py` | 237 | at least two spaces before inline comment |
| 310 | E128 | `opt/services/rpc/authz.py` | 99 | continuation line under-indented for visual indent |
| 309 | E128 | `opt/services/rpc/authz.py` | 98 | continuation line under-indented for visual indent |
| 308 | E501 | `opt/services/reporting_scheduler.py` | 372 | line too long (136 > 120 characters) |
| 307 | E501 | `opt/services/rbac/fine_grained_rbac.py` | 343 | line too long (142 > 120 characters) |
| 306 | E722 | `opt/services/profiling.py` | 210 | do not use bare 'except' |
| 305 | E501 | `opt/services/profiling.py` | 152 | line too long (134 > 120 characters) |
| 304 | E128 | `opt/services/observability/cardinality_controller.py` | 1027 | continuation line under-indented for visual indent |
| 303 | E261 | `opt/services/observability/cardinality_controller.py` | 974 | at least two spaces before inline comment |
| 302 | E128 | `opt/services/observability/cardinality_controller.py` | 542 | continuation line under-indented for visual indent |
| 301 | E129 | `opt/services/observability/cardinality_controller.py` | 514 | visually indented line with same indent as next logical line |
| 300 | E501 | `opt/services/network/multitenant_network.py` | 693 | line too long (128 > 120 characters) |
| 299 | E501 | `opt/services/network/multitenant_network.py` | 565 | line too long (127 > 120 characters) |
| 298 | E501 | `opt/services/network/multitenant_network.py` | 385 | line too long (138 > 120 characters) |
| 297 | E127 | `opt/services/multiregion/replication_scheduler.py` | 719 | continuation line over-indented for visual indent |
| 296 | E128 | `opt/services/multiregion/replication_scheduler.py` | 336 | continuation line under-indented for visual indent |
| 295 | E128 | `opt/services/multiregion/replication_scheduler.py` | 301 | continuation line under-indented for visual indent |
| 294 | E128 | `opt/services/multiregion/replication_scheduler.py` | 288 | continuation line under-indented for visual indent |
| 293 | E128 | `opt/services/multiregion/replication_scheduler.py` | 272 | continuation line under-indented for visual indent |
| 292 | E261 | `opt/services/multiregion/replication_scheduler.py` | 44 | at least two spaces before inline comment |
| 291 | E261 | `opt/services/multiregion/k8s_integration.py` | 185 | at least two spaces before inline comment |
| 290 | E501 | `opt/services/multiregion/k8s_integration.py` | 107 | line too long (128 > 120 characters) |
| 289 | E302 | `opt/services/multiregion/k8s_integration.py` | 38 | expected 2 blank lines, found 1 |
| 288 | E302 | `opt/services/multiregion/k8s_integration.py` | 27 | expected 2 blank lines, found 1 |
| 287 | E305 | `opt/services/multiregion/failover.py` | 101 | expected 2 blank lines after class or function definition, found 1 |
| 286 | E261 | `opt/services/multiregion/failover.py` | 68 | at least two spaces before inline comment |
| 285 | E501 | `opt/services/multiregion/core.py` | 359 | line too long (131 > 120 characters) |
| 284 | E501 | `opt/services/multiregion/core.py` | 330 | line too long (162 > 120 characters) |
| 283 | E501 | `opt/services/multiregion/core.py` | 329 | line too long (138 > 120 characters) |
| 282 | E501 | `opt/services/multiregion/core.py` | 313 | line too long (138 > 120 characters) |
| 281 | E302 | `opt/services/multiregion/core.py` | 34 | expected 2 blank lines, found 1 |
| 280 | E128 | `opt/services/multiregion/cli.py` | 141 | continuation line under-indented for visual indent |
| 279 | E501 | `opt/services/multiregion/cli.py` | 115 | line too long (124 > 120 characters) |
| 278 | E128 | `opt/services/multiregion/cli.py` | 87 | continuation line under-indented for visual indent |
| 277 | E128 | `opt/services/multi_cluster.py` | 606 | continuation line under-indented for visual indent |
| 276 | E128 | `opt/services/multi_cluster.py` | 605 | continuation line under-indented for visual indent |
| 275 | E128 | `opt/services/multi_cluster.py` | 604 | continuation line under-indented for visual indent |
| 274 | E128 | `opt/services/multi_cluster.py` | 603 | continuation line under-indented for visual indent |
| 273 | E128 | `opt/services/multi_cluster.py` | 513 | continuation line under-indented for visual indent |
| 272 | E128 | `opt/services/multi_cluster.py` | 209 | continuation line under-indented for visual indent |
| 271 | E501 | `opt/services/migration/import_wizard.py` | 536 | line too long (136 > 120 characters) |
| 270 | E501 | `opt/services/migration/import_wizard.py` | 427 | line too long (122 > 120 characters) |
| 269 | E501 | `opt/services/migration/import_wizard.py` | 313 | line too long (133 > 120 characters) |
| 268 | E501 | `opt/services/migration/import_wizard.py` | 300 | line too long (134 > 120 characters) |
| 267 | E302 | `opt/services/migration/import_wizard.py` | 35 | expected 2 blank lines, found 1 |
| 266 | E302 | `opt/services/message_queue.py` | 254 | expected 2 blank lines, found 1 |
| 265 | E302 | `opt/services/message_queue.py` | 27 | expected 2 blank lines, found 1 |
| 264 | E501 | `opt/services/marketplace/marketplace_service.py` | 262 | line too long (122 > 120 characters) |
| 263 | E501 | `opt/services/marketplace/marketplace_service.py` | 106 | line too long (126 > 120 characters) |
| 262 | E302 | `opt/services/marketplace/marketplace_service.py` | 41 | expected 2 blank lines, found 1 |
| 261 | E128 | `opt/services/licensing/licensing_server.py` | 743 | continuation line under-indented for visual indent |
| 260 | E501 | `opt/services/licensing/licensing_server.py` | 186 | line too long (126 > 120 characters) |
| 259 | E501 | `opt/services/fleet/federation_manager.py` | 777 | line too long (128 > 120 characters) |
| 258 | E302 | `opt/services/fleet/federation_manager.py` | 34 | expected 2 blank lines, found 1 |
| 257 | E722 | `opt/services/diagnostics.py` | 307 | do not use bare 'except' |
| 256 | E501 | `opt/services/cost_optimization/core.py` | 97 | line too long (206 > 120 characters) |
| 255 | E302 | `opt/services/cost_optimization/core.py` | 37 | expected 2 blank lines, found 1 |
| 254 | E302 | `opt/services/cost_optimization/core.py` | 27 | expected 2 blank lines, found 1 |
| 253 | E302 | `opt/services/cost_optimization/core.py` | 18 | expected 2 blank lines, found 1 |
| 252 | E302 | `opt/services/cost_optimization/core.py` | 11 | expected 2 blank lines, found 1 |
| 251 | E261 | `opt/services/cost_optimization/cli.py` | 44 | at least two spaces before inline comment |
| 250 | E302 | `opt/services/cost_optimization/cli.py` | 26 | expected 2 blank lines, found 1 |
| 249 | E302 | `opt/services/cost_optimization/cli.py` | 7 | expected 2 blank lines, found 1 |
| 248 | E302 | `opt/services/cost_optimization/api.py` | 32 | expected 2 blank lines, found 1 |
| 247 | E302 | `opt/services/cost_optimization/api.py` | 27 | expected 2 blank lines, found 1 |
| 246 | E302 | `opt/services/cost_optimization/api.py` | 21 | expected 2 blank lines, found 1 |
| 245 | E128 | `opt/services/cost/cost_engine.py` | 673 | continuation line under-indented for visual indent |
| 244 | E501 | `opt/services/cost/cost_engine.py` | 516 | line too long (149 > 120 characters) |
| 243 | E501 | `opt/services/cost/cost_engine.py` | 515 | line too long (143 > 120 characters) |
| 242 | E501 | `opt/services/cost/cost_engine.py` | 284 | line too long (126 > 120 characters) |
| 241 | E501 | `opt/services/cost/cost_engine.py` | 258 | line too long (134 > 120 characters) |
| 240 | E501 | `opt/services/cost/cost_engine.py` | 245 | line too long (129 > 120 characters) |
| 239 | E501 | `opt/services/cost/cost_engine.py` | 241 | line too long (128 > 120 characters) |
| 238 | E501 | `opt/services/cost/cost_engine.py` | 240 | line too long (128 > 120 characters) |
| 237 | E501 | `opt/services/containers/container_integration.py` | 624 | line too long (127 > 120 characters) |
| 236 | E302 | `opt/services/compliance/core.py` | 39 | expected 2 blank lines, found 1 |
| 235 | E302 | `opt/services/compliance/core.py` | 30 | expected 2 blank lines, found 1 |
| 234 | E302 | `opt/services/compliance/core.py` | 21 | expected 2 blank lines, found 1 |
| 233 | E302 | `opt/services/compliance/core.py` | 11 | expected 2 blank lines, found 1 |
| 232 | E302 | `opt/services/compliance/cli.py` | 22 | expected 2 blank lines, found 1 |
| 231 | E302 | `opt/services/compliance/cli.py` | 7 | expected 2 blank lines, found 1 |
| 230 | E302 | `opt/services/compliance/api.py` | 23 | expected 2 blank lines, found 1 |
| 229 | E302 | `opt/services/compliance/api.py` | 19 | expected 2 blank lines, found 1 |
| 228 | E302 | `opt/services/compliance/api.py` | 14 | expected 2 blank lines, found 1 |
| 227 | E402 | `opt/services/cache.py` | 37 | module level import not at top of file |
| 226 | E402 | `opt/services/cache.py` | 36 | module level import not at top of file |
| 225 | E128 | `opt/services/billing/billing_integration.py` | 934 | continuation line under-indented for visual indent |
| 224 | E128 | `opt/services/billing/billing_integration.py` | 907 | continuation line under-indented for visual indent |
| 223 | E128 | `opt/services/billing/billing_integration.py` | 869 | continuation line under-indented for visual indent |
| 222 | E128 | `opt/services/billing/billing_integration.py` | 868 | continuation line under-indented for visual indent |
| 221 | E128 | `opt/services/billing/billing_integration.py` | 812 | continuation line under-indented for visual indent |
| 220 | E128 | `opt/services/billing/billing_integration.py` | 735 | continuation line under-indented for visual indent |
| 219 | E128 | `opt/services/billing/billing_integration.py` | 626 | continuation line under-indented for visual indent |
| 218 | E128 | `opt/services/billing/billing_integration.py` | 591 | continuation line under-indented for visual indent |
| 217 | E128 | `opt/services/billing/billing_integration.py` | 529 | continuation line under-indented for visual indent |
| 216 | E128 | `opt/services/billing/billing_integration.py` | 460 | continuation line under-indented for visual indent |
| 215 | E128 | `opt/services/billing/billing_integration.py` | 436 | continuation line under-indented for visual indent |
| 214 | E128 | `opt/services/billing/billing_integration.py` | 383 | continuation line under-indented for visual indent |
| 213 | E128 | `opt/services/billing/billing_integration.py` | 356 | continuation line under-indented for visual indent |
| 212 | E128 | `opt/services/billing/billing_integration.py` | 350 | continuation line under-indented for visual indent |
| 211 | E128 | `opt/services/billing/billing_integration.py` | 332 | continuation line under-indented for visual indent |
| 210 | E305 | `opt/services/backup_manager.py` | 344 | expected 2 blank lines after class or function definition, found 1 |
| 209 | E261 | `opt/services/backup_manager.py` | 265 | at least two spaces before inline comment |
| 208 | E501 | `opt/services/backup/dedup_backup_service.py` | 736 | line too long (138 > 120 characters) |
| 207 | E501 | `opt/services/backup/dedup_backup_service.py` | 505 | line too long (123 > 120 characters) |
| 206 | E302 | `opt/services/backup/dedup_backup_service.py` | 37 | expected 2 blank lines, found 1 |
| 205 | E131 | `opt/services/backup/backup_intelligence.py` | 1148 | continuation line unaligned for hanging indent |
| 204 | E128 | `opt/services/backup/backup_intelligence.py` | 469 | continuation line under-indented for visual indent |
| 203 | E402 | `opt/services/auth/ldap_backend.py` | 507 | module level import not at top of file |
| 202 | E128 | `opt/services/auth/ldap_backend.py` | 322 | continuation line under-indented for visual indent |
| 201 | E722 | `opt/services/auth/ldap_backend.py` | 175 | do not use bare 'except' |
| 200 | E261 | `opt/services/auth/ldap_backend.py` | 52 | at least two spaces before inline comment |
| 199 | E261 | `opt/services/auth/ldap_backend.py` | 42 | at least two spaces before inline comment |
| 198 | E305 | `opt/services/anomaly/test_lstm.py` | 61 | expected 2 blank lines after class or function definition, found 1 |
| 197 | E302 | `opt/services/anomaly/test_lstm.py` | 6 | expected 2 blank lines, found 1 |
| 196 | E303 | `opt/services/anomaly/core.py` | 774 | too many blank lines (2) |
| 195 | E701 | `opt/services/anomaly/core.py` | 261 | multiple statements on one line (colon) |
| 194 | E128 | `opt/security_testing.py` | 500 | continuation line under-indented for visual indent |
| 193 | E128 | `opt/security_testing.py` | 498 | continuation line under-indented for visual indent |
| 192 | E128 | `opt/security_testing.py` | 496 | continuation line under-indented for visual indent |
| 191 | E128 | `opt/security_testing.py` | 494 | continuation line under-indented for visual indent |
| 190 | E305 | `opt/security/hardening_scanner.py` | 239 | expected 2 blank lines after class or function definition, found 1 |
| 189 | E302 | `opt/security/hardening_scanner.py` | 31 | expected 2 blank lines, found 1 |
| 188 | E302 | `opt/security/hardening_scanner.py` | 22 | expected 2 blank lines, found 1 |
| 187 | E128 | `opt/oidc_oauth2.py` | 448 | continuation line under-indented for visual indent |
| 186 | E128 | `opt/oidc_oauth2.py` | 447 | continuation line under-indented for visual indent |
| 185 | E128 | `opt/oidc_oauth2.py` | 150 | continuation line under-indented for visual indent |
| 184 | E402 | `opt/netcfg_tui_full.py` | 693 | module level import not at top of file |
| 183 | E305 | `opt/netcfg-tui/tests/test_netcfg.py` | 97 | expected 2 blank lines after class or function definition, found 1 |
| 182 | E261 | `opt/netcfg-tui/tests/test_netcfg.py` | 85 | at least two spaces before inline comment |
| 181 | E261 | `opt/netcfg-tui/tests/test_netcfg.py` | 84 | at least two spaces before inline comment |
| 180 | E302 | `opt/netcfg-tui/tests/test_netcfg.py` | 38 | expected 2 blank lines, found 1 |
| 179 | E302 | `opt/netcfg-tui/tests/test_netcfg.py` | 18 | expected 2 blank lines, found 1 |
| 178 | E402 | `opt/netcfg-tui/tests/test_netcfg.py` | 12 | module level import not at top of file |
| 177 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 1231 | line too long (124 > 120 characters) |
| 176 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 1192 | line too long (122 > 120 characters) |
| 175 | E117 | `opt/netcfg-tui/netcfg_tui.py` | 1118 | over-indented |
| 174 | E111 | `opt/netcfg-tui/netcfg_tui.py` | 1118 | indentation is not a multiple of 4 |
| 173 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 1117 | at least two spaces before inline comment |
| 172 | E117 | `opt/netcfg-tui/netcfg_tui.py` | 1115 | over-indented |
| 171 | E111 | `opt/netcfg-tui/netcfg_tui.py` | 1115 | indentation is not a multiple of 4 |
| 170 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 1114 | at least two spaces before inline comment |
| 169 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 1095 | line too long (123 > 120 characters) |
| 168 | E203 | `opt/netcfg-tui/netcfg_tui.py` | 1075 | whitespace before ':' |
| 167 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 1045 | line too long (121 > 120 characters) |
| 166 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 981 | at least two spaces before inline comment |
| 165 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 935 | at least two spaces before inline comment |
| 164 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 913 | at least two spaces before inline comment |
| 163 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 861 | line too long (140 > 120 characters) |
| 162 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 846 | line too long (124 > 120 characters) |
| 161 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 825 | line too long (191 > 120 characters) |
| 160 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 758 | at least two spaces before inline comment |
| 159 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 747 | at least two spaces before inline comment |
| 158 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 609 | line too long (123 > 120 characters) |
| 157 | E261 | `opt/netcfg-tui/netcfg_tui.py` | 609 | at least two spaces before inline comment |
| 156 | E501 | `opt/netcfg-tui/netcfg_tui.py` | 492 | line too long (129 > 120 characters) |
| 155 | E303 | `opt/netcfg-tui/netcfg_tui.py` | 21 | too many blank lines (3) |
| 154 | E722 | `opt/netcfg-tui/main.py` | 177 | do not use bare 'except' |
| 153 | E305 | `opt/monitoring/fixtures/generator/app.py` | 82 | expected 2 blank lines after class or function definition, found 1 |
| 152 | E302 | `opt/monitoring/fixtures/generator/app.py` | 11 | expected 2 blank lines, found 1 |
| 151 | E501 | `opt/models/phase4_models.py` | 231 | line too long (122 > 120 characters) |
| 150 | E501 | `opt/models/phase4_models.py` | 153 | line too long (122 > 120 characters) |
| 149 | E501 | `opt/models/phase4_models.py` | 59 | line too long (122 > 120 characters) |
| 148 | E128 | `opt/k8sctl_enhanced.py` | 478 | continuation line under-indented for visual indent |
| 147 | E128 | `opt/k8sctl_enhanced.py` | 477 | continuation line under-indented for visual indent |
| 146 | E128 | `opt/k8sctl_enhanced.py` | 450 | continuation line under-indented for visual indent |
| 145 | E128 | `opt/k8sctl_enhanced.py` | 448 | continuation line under-indented for visual indent |
| 144 | E128 | `opt/k8sctl_enhanced.py` | 446 | continuation line under-indented for visual indent |
| 143 | E501 | `opt/k8sctl_enhanced.py` | 332 | line too long (140 > 120 characters) |
| 142 | E501 | `opt/k8sctl_enhanced.py` | 323 | line too long (142 > 120 characters) |
| 141 | E501 | `opt/k8sctl_enhanced.py` | 321 | line too long (127 > 120 characters) |
| 140 | E501 | `opt/k8sctl_enhanced.py` | 316 | line too long (132 > 120 characters) |
| 139 | E128 | `opt/k8sctl_enhanced.py` | 305 | continuation line under-indented for visual indent |
| 138 | E128 | `opt/k8sctl_enhanced.py` | 289 | continuation line under-indented for visual indent |
| 137 | E128 | `opt/k8sctl_enhanced.py` | 234 | continuation line under-indented for visual indent |
| 136 | E128 | `opt/k8sctl_enhanced.py` | 194 | continuation line under-indented for visual indent |
| 135 | E128 | `opt/installer/install_profile_logger.py` | 744 | continuation line under-indented for visual indent |
| 134 | E128 | `opt/installer/install_profile_logger.py` | 530 | continuation line under-indented for visual indent |
| 133 | E128 | `opt/installer/install_profile_logger.py` | 523 | continuation line under-indented for visual indent |
| 132 | E128 | `opt/installer/install_profile_logger.py` | 347 | continuation line under-indented for visual indent |
| 131 | E128 | `opt/hvctl_enhanced.py` | 746 | continuation line under-indented for visual indent |
| 130 | E128 | `opt/hvctl_enhanced.py` | 707 | continuation line under-indented for visual indent |
| 129 | E128 | `opt/hvctl_enhanced.py` | 705 | continuation line under-indented for visual indent |
| 128 | E128 | `opt/hvctl_enhanced.py` | 703 | continuation line under-indented for visual indent |
| 127 | E261 | `opt/hvctl_enhanced.py` | 689 | at least two spaces before inline comment |
| 126 | E261 | `opt/hvctl_enhanced.py` | 639 | at least two spaces before inline comment |
| 125 | E501 | `opt/hvctl_enhanced.py` | 639 | line too long (158 > 120 characters) |
| 124 | E128 | `opt/hvctl_enhanced.py` | 430 | continuation line under-indented for visual indent |
| 123 | E128 | `opt/hvctl_enhanced.py` | 429 | continuation line under-indented for visual indent |
| 122 | E501 | `opt/hvctl_enhanced.py` | 393 | line too long (121 > 120 characters) |
| 121 | E501 | `opt/hvctl_enhanced.py` | 374 | line too long (121 > 120 characters) |
| 120 | E128 | `opt/graphql_integration.py` | 52 | continuation line under-indented for visual indent |
| 119 | E501 | `opt/graphql_api.py` | 1017 | line too long (149 > 120 characters) |
| 118 | E128 | `opt/graphql_api.py` | 647 | continuation line under-indented for visual indent |
| 117 | E128 | `opt/graphql_api.py` | 646 | continuation line under-indented for visual indent |
| 116 | E128 | `opt/graphql_api.py` | 602 | continuation line under-indented for visual indent |
| 115 | E128 | `opt/graphql_api.py` | 579 | continuation line under-indented for visual indent |
| 114 | E128 | `opt/graphql_api.py` | 578 | continuation line under-indented for visual indent |
| 113 | E128 | `opt/graphql_api.py` | 516 | continuation line under-indented for visual indent |
| 112 | E203 | `opt/graphql_api.py` | 154 | whitespace before ':' |
| 111 | E501 | `opt/e2e_testing.py` | 673 | line too long (134 > 120 characters) |
| 110 | E128 | `opt/distributed_tracing.py` | 485 | continuation line under-indented for visual indent |
| 109 | E128 | `opt/distributed_tracing.py` | 203 | continuation line under-indented for visual indent |
| 108 | E128 | `opt/distributed_tracing.py` | 168 | continuation line under-indented for visual indent |
| 107 | E128 | `opt/distributed_tracing.py` | 167 | continuation line under-indented for visual indent |
| 106 | E128 | `opt/core/unified_backend.py` | 824 | continuation line under-indented for visual indent |
| 105 | E731 | `opt/core/unified_backend.py` | 657 | do not assign a lambda expression, use a def |
| 104 | E305 | `opt/config_distributor.py` | 226 | expected 2 blank lines after class or function definition, found 1 |
| 103 | E302 | `opt/config_distributor.py` | 223 | expected 2 blank lines, found 1 |
| 102 | E701 | `opt/config_distributor.py` | 209 | multiple statements on one line (colon) |
| 101 | E305 | `opt/cert_manager.py` | 295 | expected 2 blank lines after class or function definition, found 1 |
| 100 | E261 | `opt/cert_manager.py` | 93 | at least two spaces before inline comment |
| 99 | E128 | `opt/cephctl_enhanced.py` | 466 | continuation line under-indented for visual indent |
| 98 | E128 | `opt/cephctl_enhanced.py` | 464 | continuation line under-indented for visual indent |
| 97 | E128 | `opt/cephctl_enhanced.py` | 462 | continuation line under-indented for visual indent |
| 96 | E501 | `opt/advanced_features.py` | 482 | line too long (121 > 120 characters) |
| 95 | E261 | `etc/debvisor/test_validate_blocklists.py` | 98 | at least two spaces before inline comment |
