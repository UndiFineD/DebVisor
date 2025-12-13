\n\n# Security Scan Report\n\n**Total
Alerts:**8946\n**Open:**
1117 |**Dismissed/Fixed:** 7829\n\nGenerated via GitHub CLI.\n\n## 🔴 Critical
Severity
(0)\n\n*No
alerts found.*\n\n## 🟠 High Severity (0)\n\n*No alerts found.*\n\n## 🟡 Medium
Severity
(0)\n\n*No
alerts found.*\n\n## 🟢 Low Severity (0)\n\n*No alerts found.*\n\n## ⚪ Other
(1117)\n\n| ID
| Rule |
Tool | File | Line | Message |\n|----|------|------|------|------|---------|\n| 8946 |
F821 | flake8
| `scripts/fix_all_errors.py`| 3635 | undefined name 'filtered_summary' |\n| 8945 | F821 | flake8
|`scripts/fix_all_errors.py`| 3633 | undefined name 'filtered_issues' |\n| 8944 | F821 | flake8
|`scripts/fix_all_errors.py`| 3632 | undefined name 'report_path' |\n| 8943 | E303 | flake8
|`scripts/fix_all_errors.py`| 3631 | too many blank lines (2) |\n| 8942 | E115 | flake8
|`scripts/fix_all_errors.py`| 3555 | expected an indented block (comment) |\n| 8941 | E115 | flake8
|`scripts/fix_all_errors.py`| 3537 | expected an indented block (comment) |\n| 8940 | E115 | flake8
|`scripts/fix_all_errors.py`| 3519 | expected an indented block (comment) |\n| 8939 | E115 | flake8
|`scripts/fix_all_errors.py`| 3504 | expected an indented block (comment) |\n| 8938 | E115 | flake8
|`scripts/fix_all_errors.py`| 3496 | expected an indented block (comment) |\n| 8937 | E115 | flake8
|`scripts/fix_all_errors.py`| 3482 | expected an indented block (comment) |\n| 8936 | E115 | flake8
|`scripts/fix_all_errors.py`| 3467 | expected an indented block (comment) |\n| 8935 | E115 | flake8
|`scripts/fix_all_errors.py`| 3462 | expected an indented block (comment) |\n| 8934 | E115 | flake8
|`scripts/fix_all_errors.py`| 3459 | expected an indented block (comment) |\n| 8933 | E115 | flake8
|`scripts/fix_all_errors.py`| 3448 | expected an indented block (comment) |\n| 8932 | E115 | flake8
|`scripts/fix_all_errors.py`| 3446 | expected an indented block (comment) |\n| 8931 | E115 | flake8
|`scripts/fix_all_errors.py`| 3429 | expected an indented block (comment) |\n| 8930 | E115 | flake8
|`scripts/fix_all_errors.py`| 3419 | expected an indented block (comment) |\n| 8929 | E115 | flake8
|`scripts/fix_all_errors.py`| 3407 | expected an indented block (comment) |\n| 8928 | E115 | flake8
|`scripts/fix_all_errors.py`| 3370 | expected an indented block (comment) |\n| 8927 | E128 | flake8
|`scripts/fix_all_errors.py`| 3354 | continuation line under-indented for visual indent |\n| 8926 |
E302 | flake8 |`scripts/fix_all_errors.py`| 3329 | expected 2 blank lines, found 1 |\n|
8925 | E128
| flake8 |`scripts/fix_all_errors.py`| 2755 | continuation line under-indented for visual indent
|\n| 8924 | E302 | flake8 |`scripts/passthrough_manager.py`| 16 | expected 2 blank lines, found 1
|\n| 8923 | E115 | flake8 |`scripts/generate_notifications_report.py`| 80 | expected an indented
block (comment) |\n| 8922 | E128 | flake8 |`scripts/fix_all_errors.py`| 2756 |
continuation line
under-indented for visual indent |\n| 8921 | PinnedDependenciesID | Scorecard
|`.github/workflows/test.yml`| 40 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8916 | E115 | flake8
|`tests/test_ssh_hardening.py`| 22 |
expected an indented block (comment) |\n| 8915 | E115 | flake8
|`tests/test_slo_tracking.py`| 434 |
expected an indented block (comment) |\n| 8914 | F401 | flake8
|`tests/test_rpc_security.py`| 14 |
'unittest' imported but unused |\n| 8913 | F401 | flake8 |`tests/test_property_based.py`|
16 |
'unittest' imported but unused |\n| 8912 | F401 | flake8 |`tests/test_phase6_vnc.py`| 14 |
'unittest' imported but unused |\n| 8911 | F401 | flake8 |`tests/test_phase6_vm.py`| 14 |
'unittest'
imported but unused |\n| 8910 | E115 | flake8 |`tests/test_phase6_dns.py`| 287 | expected
an
indented block (comment) |\n| 8909 | E302 | flake8 |`tests/test_phase6_dns.py`| 17 |
expected 2
blank lines, found 1 |\n| 8908 | E115 | flake8 |`tests/test_phase6_cloudinit.py`| 333 |
expected an
indented block (comment) |\n| 8907 | E115 | flake8 |`tests/test_passthrough.py`| 340 |
expected an
indented block (comment) |\n| 8906 | E115 | flake8 |`tests/test_passthrough.py`| 143 |
expected an
indented block (comment) |\n| 8905 | F811 | flake8 |`tests/test_passthrough.py`| 18 |
redefinition
of unused 'patch' from line 15 |\n| 8904 | F401 | flake8 |`tests/test_passthrough.py`| 14
|
'unittest' imported but unused |\n| 8903 | F401 | flake8
|`tests/test_network_backends.py`| 14 |
'unittest' imported but unused |\n| 8902 | E115 | flake8 |`tests/test_netcfg_mock.py`| 420
|
expected an indented block (comment) |\n| 8901 | F401 | flake8
|`tests/test_monitoring.py`| 14 |
'unittest' imported but unused |\n| 8900 | F401 | flake8 |`tests/test_mock_mode.py`| 6 |
'pytest'
imported but unused |\n| 8899 | F821 | flake8 |`tests/test_migrations.py`| 16 | undefined
name
'Flask' |\n| 8898 | E302 | flake8 |`tests/test_migrations.py`| 14 | expected 2 blank
lines, found 0
|\n| 8897 | F401 | flake8 |`tests/test_migrations.py`| 13 | 'datetime.datetime' imported but unused
|\n| 8896 | F401 | flake8 |`tests/test_migrations.py`| 12 | 'pytest' imported but unused |\n| 8895 |
F401 | flake8 |`tests/test_migrations.py`| 11 | 'unittest.mock.MagicMock' imported but
unused |\n|
8894 | F401 | flake8 |`tests/test_migrations.py`| 11 | 'unittest.mock.patch' imported but
unused
|\n| 8893 | F821 | flake8 |`tests/test_marketplace_governance.py`| 64 | undefined name
'SecurityScanResult' |\n| 8892 | F821 | flake8 |`tests/test_marketplace_governance.py`| 50
|
undefined name 'SecurityScanResult' |\n| 8891 | F821 | flake8
|`tests/test_marketplace_governance.py`| 29 | undefined name 'SecurityScanResult' |\n| 8890 | E115 |
flake8 |`tests/test_marketplace_governance.py`| 28 | expected an indented block (comment)
|\n| 8889
| E115 | flake8 |`tests/test_marketplace_governance.py`| 23 | expected an indented block (comment)
|\n| 8888 | F821 | flake8 |`tests/test_marketplace_governance.py`| 12 | undefined name 'Recipe' |\n|
8887 | F821 | flake8 |`tests/test_marketplace_governance.py`| 11 | undefined name
'SecurityScanner'
|\n| 8886 | F401 | flake8 |`tests/test_marketplace_governance.py`| 7 | 'datetime.datetime' imported
but unused |\n| 8885 | F401 | flake8 |`tests/test_marketplace_governance.py`| 6 | 'pytest'
imported
but unused |\n| 8884 | F401 | flake8 |`tests/test_marketplace_governance.py`| 5 |
'unittest.mock.MagicMock' imported but unused |\n| 8883 | F401 | flake8
|`tests/test_marketplace_governance.py`| 5 | 'unittest.mock.patch' imported but unused |\n| 8882 |
F821 | flake8 |`tests/test_licensing.py`| 134 | undefined name 'ECDSAVerifier' |\n| 8881 |
F821 |
flake8 |`tests/test_licensing.py`| 125 | undefined name 'HardwareFingerprint' |\n| 8880 |
F821 |
flake8 |`tests/test_licensing.py`| 121 | undefined name 'MagicMock' |\n| 8879 | F821 |
flake8
|`tests/test_licensing.py`| 111 | undefined name 'HardwareFingerprint' |\n| 8878 | F821 | flake8
|`tests/test_licensing.py`| 110 | undefined name 'mock_open' |\n| 8877 | F821 | flake8
|`tests/test_licensing.py`| 94 | undefined name 'LicenseBundle' |\n| 8876 | F821 | flake8
|`tests/test_licensing.py`| 82 | undefined name 'timezone' |\n| 8875 | F821 | flake8
|`tests/test_licensing.py`| 79 | undefined name 'LicenseBundle' |\n| 8874 | F821 | flake8
|`tests/test_licensing.py`| 76 | undefined name 'timezone' |\n| 8873 | F821 | flake8
|`tests/test_licensing.py`| 75 | undefined name 'LicenseTier' |\n| 8872 | F821 | flake8
|`tests/test_licensing.py`| 74 | undefined name 'LicenseFeatures' |\n| 8871 | F821 | flake8
|`tests/test_licensing.py`| 67 | undefined name 'FeatureFlag' |\n| 8870 | F821 | flake8
|`tests/test_licensing.py`| 66 | undefined name 'FeatureFlag' |\n| 8869 | F821 | flake8
|`tests/test_licensing.py`| 60 | undefined name 'LicenseTier' |\n| 8868 | F821 | flake8
|`tests/test_licensing.py`| 59 | undefined name 'LicenseFeatures' |\n| 8867 | F821 | flake8
|`tests/test_licensing.py`| 55 | undefined name 'FeatureFlag' |\n| 8866 | F821 | flake8
|`tests/test_licensing.py`| 54 | undefined name 'FeatureFlag' |\n| 8865 | F821 | flake8
|`tests/test_licensing.py`| 53 | undefined name 'FeatureFlag' |\n| 8864 | F821 | flake8
|`tests/test_licensing.py`| 50 | undefined name 'LicenseTier' |\n| 8863 | F821 | flake8
|`tests/test_licensing.py`| 50 | undefined name 'LicenseFeatures' |\n| 8862 | F821 | flake8
|`tests/test_licensing.py`| 45 | undefined name 'LicenseTier' |\n| 8861 | F821 | flake8
|`tests/test_licensing.py`| 45 | undefined name 'LicenseFeatures' |\n| 8860 | F821 | flake8
|`tests/test_licensing.py`| 40 | undefined name 'timedelta' |\n| 8859 | F821 | flake8
|`tests/test_licensing.py`| 37 | undefined name 'LicenseTier' |\n| 8858 | F821 | flake8
|`tests/test_licensing.py`| 36 | undefined name 'LicenseFeatures' |\n| 8857 | F821 | flake8
|`tests/test_licensing.py`| 35 | undefined name 'timezone' |\n| 8856 | F401 | flake8
|`tests/test_hvctl_xen.py`| 4 | 'unittest' imported but unused |\n| 8855 | E115 | flake8
|`tests/test_feature_flags.py`| 54 | expected an indented block (comment) |\n| 8854 | E115 | flake8
|`tests/test_feature_flags.py`| 48 | expected an indented block (comment) |\n| 8853 | E115 | flake8
|`tests/test_feature_flags.py`| 42 | expected an indented block (comment) |\n| 8852 | E115 | flake8
|`tests/test_feature_flags.py`| 35 | expected an indented block (comment) |\n| 8851 | F811 | flake8
|`tests/test_feature_flags.py`| 11 | redefinition of unused 'patch' from line 8 |\n| 8850 | F401 |
flake8 |`tests/test_energy_telemetry.py`| 4 | 'unittest' imported but unused |\n| 8849 |
E128 |
flake8 |`tests/test_dns_hosting.py`| 76 | continuation line under-indented for visual
indent |\n|
8848 | F811 | flake8 |`tests/test_diagnostics.py`| 15 | redefinition of unused 'patch'
from line 13
|\n| 8847 | F401 | flake8 |`tests/test_dashboard.py`| 1 | 'unittest' imported but unused |\n| 8846 |
F401 | flake8 |`tests/test_cost_optimization.py`| 1 | 'unittest' imported but unused |\n|
8845 |
E115 | flake8 |`tests/test_compliance_reporting.py`| 52 | expected an indented block
(comment) |\n|
8844 | E115 | flake8 |`tests/test_compliance_reporting.py`| 19 | expected an indented
block
(comment) |\n| 8843 | E302 | flake8 |`tests/test_compliance_reporting.py`| 11 | expected 2
blank
lines, found 0 |\n| 8842 | F401 | flake8 |`tests/test_compliance_reporting.py`| 10 |
'datetime.datetime' imported but unused |\n| 8841 | F401 | flake8
|`tests/test_compliance_reporting.py`| 9 | 'pytest' imported but unused |\n| 8840 | F811 | flake8
|`tests/test_compliance_reporting.py`| 8 | redefinition of unused 'MagicMock' from line 3 |\n| 8839
| F811 | flake8 |`tests/test_compliance_reporting.py`| 8 | redefinition of unused 'patch' from line
3 |\n| 8838 | F811 | flake8 |`tests/test_compliance_reporting.py`| 3 | redefinition of
unused
'patch' from line 1 |\n| 8837 | F811 | flake8 |`tests/test_compliance_remediation.py`| 7 |
redefinition of unused 'patch' from line 5 |\n| 8836 | F401 | flake8
|`tests/test_compliance_remediation.py`| 4 | 'unittest' imported but unused |\n| 8835 | F401 |
flake8 |`tests/test_compliance.py`| 1 | 'unittest' imported but unused |\n| 8834 | F811 |
flake8
|`tests/test_cli_wrappers.py`| 15 | redefinition of unused 'patch' from line 3 |\n| 8833 | E115 |
flake8 |`tests/test_chaos_engineering.py`| 712 | expected an indented block (comment) |\n|
8832 |
E115 | flake8 |`tests/test_chaos_engineering.py`| 561 | expected an indented block
(comment) |\n|
8831 | E115 | flake8 |`tests/test_chaos_engineering.py`| 535 | expected an indented block
(comment)
|\n| 8830 | E115 | flake8 |`tests/test_chaos_engineering.py`| 501 | expected an indented block
(comment) |\n| 8829 | E115 | flake8 |`tests/test_chaos_engineering.py`| 340 | expected an
indented
block (comment) |\n| 8828 | F401 | flake8 |`tests/test_chaos_engineering.py`| 3 |
'unittest'
imported but unused |\n| 8827 | F401 | flake8 |`tests/test_backup_service.py`| 15 |
'unittest'
imported but unused |\n| 8826 | E302 | flake8 |`tests/test_backup_manager_encryption.py`|
17 |
expected 2 blank lines, found 1 |\n| 8825 | F401 | flake8
|`tests/test_backup_manager_encryption.py`| 2 | 'unittest.mock.patch' imported but unused |\n| 8824
| F401 | flake8 |`tests/test_backup_manager_encryption.py`| 1 | 'unittest' imported but unused |\n|
8823 | F811 | flake8 |`tests/test_audit_encryption.py`| 15 | redefinition of unused
'patch' from
line 12 |\n| 8822 | F821 | flake8 |`tests/test_audit_chain.py`| 69 | undefined name 'db'
|\n| 8821 |
E115 | flake8 |`tests/test_audit_chain.py`| 63 | expected an indented block (comment) |\n|
8820 |
F821 | flake8 |`tests/test_audit_chain.py`| 55 | undefined name 'db' |\n| 8819 | E115 |
flake8
|`tests/test_audit_chain.py`| 31 | expected an indented block (comment) |\n| 8818 | F821 | flake8
|`tests/test_audit_chain.py`| 27 | undefined name 'db' |\n| 8817 | F821 | flake8
|`tests/test_audit_chain.py`| 26 | undefined name 'db' |\n| 8816 | F821 | flake8
|`tests/test_audit_chain.py`| 23 | undefined name 'db' |\n| 8815 | F821 | flake8
|`tests/test_audit_chain.py`| 20 | undefined name 'db' |\n| 8814 | F821 | flake8
|`tests/test_audit_chain.py`| 14 | undefined name 'Flask' |\n| 8813 | F401 | flake8
|`tests/test_audit_chain.py`| 2 | 'unittest.mock.MagicMock' imported but unused |\n| 8812 | F401 |
flake8 |`tests/test_audit_chain.py`| 2 | 'unittest.mock.patch' imported but unused |\n|
8811 | F811
| flake8 |`tests/test_audit_chain.py`| 2 | redefinition of unused 'patch' from line 1 |\n| 8810 |
E115 | flake8 |`tests/test_api_versioning.py`| 379 | expected an indented block (comment)
|\n| 8809
| E115 | flake8 |`tests/test_api_versioning.py`| 332 | expected an indented block (comment) |\n|
8808 | F401 | flake8 |`tests/test_api_versioning.py`| 13 | 'unittest.mock.patch' imported
but unused
|\n| 8807 | F401 | flake8 |`tests/test_api_versioning.py`| 12 | 'unittest' imported but unused |\n|
8806 | E115 | flake8 |`tests/test_analytics.py`| 214 | expected an indented block
(comment) |\n|
8805 | F401 | flake8 |`tests/test_acme_certificates.py`| 1 | 'unittest' imported but
unused |\n|
8804 | E115 | flake8 |`tests/fuzzing/fuzz_validator.py`| 35 | expected an indented block
(comment)
|\n| 8803 | E115 | flake8 |`tests/benchmarks/test_performance.py`| 822 | expected an indented block
(comment) |\n| 8802 | E115 | flake8 |`tests/benchmarks/test_performance.py`| 629 |
expected an
indented block (comment) |\n| 8801 | F401 | flake8
|`tests/benchmarks/test_performance.py`| 14 |
'pytest' imported but unused |\n| 8800 | F541 | flake8 |`scripts/update_type_ignore.py`|
394 |
f-string is missing placeholders |\n| 8799 | F541 | flake8
|`scripts/update_type_ignore.py`| 387 |
f-string is missing placeholders |\n| 8798 | E115 | flake8
|`scripts/update_type_ignore.py`| 298 |
expected an indented block (comment) |\n| 8797 | E115 | flake8
|`scripts/update_type_ignore.py`| 279
| expected an indented block (comment) |\n| 8796 | E501 | flake8 |`scripts/update_type_ignore.py`|
242 | line too long (121 > 120 characters) |\n| 8795 | E115 | flake8
|`scripts/update_type_ignore.py`| 118 | expected an indented block (comment) |\n| 8794 | F401 |
flake8 |`scripts/update_type_ignore.py`| 33 | 'typing.Set' imported but unused |\n| 8793 |
E115 |
flake8 |`scripts/sbom_diff.py`| 134 | expected an indented block (comment) |\n| 8792 |
E115 | flake8
|`scripts/passthrough_manager.py`| 46 | expected an indented block (comment) |\n| 8791 | E115 |
flake8 |`scripts/generate_security_report_v2.py`| 49 | expected an indented block
(comment) |\n|
8788 | E128 | flake8 |`scripts/fix_all_errors.py`| 3294 | continuation line under-indented
for
visual indent |\n| 8787 | E303 | flake8 |`scripts/fix_all_errors.py`| 3222 | too many
blank lines
(3) |\n| 8786 | E128 | flake8 |`scripts/fix_all_errors.py`| 3179 | continuation line
under-indented
for visual indent |\n| 8785 | E128 | flake8 |`scripts/fix_all_errors.py`| 3145 |
continuation line
under-indented for visual indent |\n| 8784 | E128 | flake8 |`scripts/fix_all_errors.py`|
3114 |
continuation line under-indented for visual indent |\n| 8783 | E128 | flake8
|`scripts/fix_all_errors.py`| 3082 | continuation line under-indented for visual indent |\n| 8782 |
E115 | flake8 |`scripts/fix_all_errors.py`| 3073 | expected an indented block (comment)
|\n| 8781 |
F841 | flake8 |`scripts/fix_all_errors.py`| 3059 | local variable 'original' is assigned
to but
never used |\n| 8780 | E115 | flake8 |`scripts/fix_all_errors.py`| 2980 | expected an
indented block
(comment) |\n| 8779 | F841 | flake8 |`scripts/fix_all_errors.py`| 2970 | local variable
'close_paren' is assigned to but never used |\n| 8778 | E115 | flake8
|`scripts/fix_all_errors.py`|
2968 | expected an indented block (comment) |\n| 8777 | E115 | flake8
|`scripts/fix_all_errors.py`|
2933 | expected an indented block (comment) |\n| 8776 | E128 | flake8
|`scripts/fix_all_errors.py`|
2901 | continuation line under-indented for visual indent |\n| 8775 | E115 |
flake8
|`scripts/fix_all_errors.py`| 2895 | expected an indented block (comment) |\n| 8774 | E115 | flake8
|`scripts/fix_all_errors.py`| 2892 | expected an indented block (comment) |\n| 8773 | F841 | flake8
|`scripts/fix_all_errors.py`| 2886 | local variable 'original' is assigned to but never used |\n|
8772 | E115 | flake8 |`scripts/fix_all_errors.py`| 2849 | expected an indented block
(comment) |\n|
8771 | E115 | flake8 |`scripts/fix_all_errors.py`| 2839 | expected an indented block
(comment) |\n|
8770 | E303 | flake8 |`scripts/fix_all_errors.py`| 2807 | too many blank lines (3) |\n|
8769 | E115
| flake8 |`scripts/fix_all_errors.py`| 2791 | expected an indented block (comment) |\n| 8768 | E115
| flake8 |`scripts/fix_all_errors.py`| 2784 | expected an indented block (comment) |\n| 8767 | E115
| flake8 |`scripts/fix_all_errors.py`| 2778 | expected an indented block (comment) |\n| 8766 | E128
| flake8 |`scripts/fix_all_errors.py`| 2758 | continuation line under-indented for visual indent
|\n| 8765 | E128 | flake8 |`scripts/fix_all_errors.py`| 2757 | continuation line under-indented for
visual indent |\n| 8764 | E115 | flake8 |`scripts/fix_all_errors.py`| 2743 | expected an
indented
block (comment) |\n| 8763 | E115 | flake8 |`scripts/fix_all_errors.py`| 2736 | expected an
indented
block (comment) |\n| 8762 | E115 | flake8 |`scripts/fix_all_errors.py`| 2729 | expected an
indented
block (comment) |\n| 8761 | E115 | flake8 |`scripts/fix_all_errors.py`| 2638 | expected an
indented
block (comment) |\n| 8760 | E115 | flake8 |`scripts/fix_all_errors.py`| 2565 | expected an
indented
block (comment) |\n| 8759 | E115 | flake8 |`scripts/fix_all_errors.py`| 2558 | expected an
indented
block (comment) |\n| 8758 | E115 | flake8 |`scripts/fix_all_errors.py`| 2553 | expected an
indented
block (comment) |\n| 8757 | E115 | flake8 |`scripts/fix_all_errors.py`| 2510 | expected an
indented
block (comment) |\n| 8756 | E115 | flake8 |`scripts/fix_all_errors.py`| 2507 | expected an
indented
block (comment) |\n| 8755 | E115 | flake8 |`scripts/fix_all_errors.py`| 2498 | expected an
indented
block (comment) |\n| 8754 | E115 | flake8 |`scripts/fix_all_errors.py`| 2495 | expected an
indented
block (comment) |\n| 8753 | E115 | flake8 |`scripts/fix_all_errors.py`| 2493 | expected an
indented
block (comment) |\n| 8752 | E115 | flake8 |`scripts/fix_all_errors.py`| 2446 | expected an
indented
block (comment) |\n| 8751 | E115 | flake8 |`scripts/fix_all_errors.py`| 2444 | expected an
indented
block (comment) |\n| 8750 | E115 | flake8 |`scripts/fix_all_errors.py`| 2330 | expected an
indented
block (comment) |\n| 8749 | E128 | flake8 |`scripts/fix_all_errors.py`| 2294 |
continuation line
under-indented for visual indent |\n| 8748 | E128 | flake8 |`scripts/fix_all_errors.py`|
2262 |
continuation line under-indented for visual indent |\n| 8747 | E115 | flake8
|`scripts/fix_all_errors.py`| 2260 | expected an indented block (comment) |\n| 8746 | E128 | flake8
|`scripts/fix_all_errors.py`| 2258 | continuation line under-indented for visual indent |\n| 8745 |
E115 | flake8 |`scripts/fix_all_errors.py`| 2256 | expected an indented block (comment)
|\n| 8744 |
E115 | flake8 |`scripts/fix_all_errors.py`| 2250 | expected an indented block (comment)
|\n| 8743 |
E115 | flake8 |`scripts/fix_all_errors.py`| 2248 | expected an indented block (comment)
|\n| 8742 |
E128 | flake8 |`scripts/fix_all_errors.py`| 2232 | continuation line under-indented for
visual
indent |\n| 8741 | E128 | flake8 |`scripts/fix_all_errors.py`| 2217 | continuation line
under-indented for visual indent |\n| 8740 | E115 | flake8 |`scripts/fix_all_errors.py`|
2195 |
expected an indented block (comment) |\n| 8739 | E115 | flake8
|`scripts/fix_all_errors.py`| 2176 |
expected an indented block (comment) |\n| 8738 | E231 | flake8
|`scripts/fix_all_errors.py`| 2153 |
missing whitespace after ',' |\n| 8737 | E115 | flake8 |`scripts/fix_all_errors.py`| 2111
| expected
an indented block (comment) |\n| 8736 | E128 | flake8 |`scripts/fix_all_errors.py`| 2108 |
continuation line under-indented for visual indent |\n| 8735 | E115 | flake8
|`scripts/fix_all_errors.py`| 2104 | expected an indented block (comment) |\n| 8734 | E128 | flake8
|`scripts/fix_all_errors.py`| 2096 | continuation line under-indented for visual indent |\n| 8733 |
E115 | flake8 |`scripts/fix_all_errors.py`| 2086 | expected an indented block (comment)
|\n| 8732 |
E128 | flake8 |`scripts/fix_all_errors.py`| 2084 | continuation line under-indented for
visual
indent |\n| 8731 | F841 | flake8 |`scripts/fix_all_errors.py`| 2078 | local variable
'original_config' is assigned to but never used |\n| 8730 | E128 | flake8
|`scripts/fix_all_errors.py`| 2072 | continuation line under-indented for visual indent |\n| 8729 |
E128 | flake8 |`scripts/fix_all_errors.py`| 2053 | continuation line under-indented for
visual
indent |\n| 8728 | E128 | flake8 |`scripts/fix_all_errors.py`| 2031 | continuation line
under-indented for visual indent |\n| 8727 | E128 | flake8 |`scripts/fix_all_errors.py`|
1981 |
continuation line under-indented for visual indent |\n| 8726 | F841 | flake8
|`scripts/fix_all_errors.py`| 1974 | local variable 'modified' is assigned to but never used |\n|
8725 | E128 | flake8 |`scripts/fix_all_errors.py`| 1932 | continuation line under-indented
for
visual indent |\n| 8724 | E128 | flake8 |`scripts/fix_all_errors.py`| 1918 | continuation
line
under-indented for visual indent |\n| 8723 | E128 | flake8 |`scripts/fix_all_errors.py`|
1917 |
continuation line under-indented for visual indent |\n| 8722 | E501 | flake8
|`scripts/fix_all_errors.py`| 1915 | line too long (151 > 120 characters) |\n| 8721 | E128 | flake8
|`scripts/fix_all_errors.py`| 1914 | continuation line under-indented for visual indent |\n| 8720 |
E501 | flake8 |`scripts/fix_all_errors.py`| 1912 | line too long (149 > 120 characters)
|\n| 8719 |
E115 | flake8 |`scripts/fix_all_errors.py`| 1892 | expected an indented block (comment)
|\n| 8718 |
E115 | flake8 |`scripts/fix_all_errors.py`| 1882 | expected an indented block (comment)
|\n| 8717 |
E115 | flake8 |`scripts/fix_all_errors.py`| 1847 | expected an indented block (comment)
|\n| 8716 |
E128 | flake8 |`scripts/fix_all_errors.py`| 1819 | continuation line under-indented for
visual
indent |\n| 8715 | E128 | flake8 |`scripts/fix_all_errors.py`| 1814 | continuation line
under-indented for visual indent |\n| 8714 | E202 | flake8 |`scripts/fix_all_errors.py`|
1790 |
whitespace before '}' |\n| 8713 | E201 | flake8 |`scripts/fix_all_errors.py`| 1790 |
whitespace
after '{' |\n| 8712 | E202 | flake8 |`scripts/fix_all_errors.py`| 1789 | whitespace before
'}' |\n|
8711 | E201 | flake8 |`scripts/fix_all_errors.py`| 1789 | whitespace after '{' |\n| 8710 |
E115 |
flake8 |`scripts/fix_all_errors.py`| 1731 | expected an indented block (comment) |\n| 8709
| E115 |
flake8 |`scripts/fix_all_errors.py`| 1675 | expected an indented block (comment) |\n| 8708
| E115 |
flake8 |`scripts/fix_all_errors.py`| 1671 | expected an indented block (comment) |\n| 8707
| E115 |
flake8 |`scripts/fix_all_errors.py`| 1635 | expected an indented block (comment) |\n| 8706
| E128 |
flake8 |`scripts/fix_all_errors.py`| 1633 | continuation line under-indented for visual
indent |\n|
8705 | E115 | flake8 |`scripts/fix_all_errors.py`| 1601 | expected an indented block
(comment) |\n|
8704 | E302 | flake8 |`scripts/fix_all_errors.py`| 1597 | expected 2 blank lines, found 1
|\n| 8703
| E128 | flake8 |`scripts/fix_all_errors.py`| 1258 | continuation line under-indented for visual
indent |\n| 8702 | E302 | flake8 |`scripts/fix_all_errors.py`| 1074 | expected 2 blank
lines, found
1 |\n| 8701 | E115 | flake8 |`scripts/fix_all_errors.py`| 950 | expected an indented block
(comment)
|\n| 8700 | F541 | flake8 |`scripts/fix_all_errors.py`| 925 | f-string is missing placeholders |\n|
8699 | E115 | flake8 |`scripts/fix_all_errors.py`| 865 | expected an indented block
(comment) |\n|
8698 | E115 | flake8 |`scripts/fix_all_errors.py`| 855 | expected an indented block
(comment) |\n|
8697 | E115 | flake8 |`scripts/fix_all_errors.py`| 823 | expected an indented block
(comment) |\n|
8696 | E115 | flake8 |`scripts/fix_all_errors.py`| 816 | expected an indented block
(comment) |\n|
8695 | E115 | flake8 |`scripts/fix_all_errors.py`| 814 | expected an indented block
(comment) |\n|
8694 | E115 | flake8 |`scripts/fix_all_errors.py`| 808 | expected an indented block
(comment) |\n|
8693 | E115 | flake8 |`scripts/fix_all_errors.py`| 716 | expected an indented block
(comment) |\n|
8692 | E303 | flake8 |`scripts/fix_all_errors.py`| 715 | too many blank lines (2) |\n|
8691 | F811 |
flake8 |`scripts/fix_all_errors.py`| 715 | redefinition of unused 'run' from line 175 |\n|
8690 |
E115 | flake8 |`scripts/fix_all_errors.py`| 686 | expected an indented block (comment)
|\n| 8689 |
E115 | flake8 |`scripts/fix_all_errors.py`| 676 | expected an indented block (comment)
|\n| 8688 |
E115 | flake8 |`scripts/fix_all_errors.py`| 661 | expected an indented block (comment)
|\n| 8687 |
E115 | flake8 |`scripts/fix_all_errors.py`| 656 | expected an indented block (comment)
|\n| 8686 |
E306 | flake8 |`scripts/fix_all_errors.py`| 585 | expected 1 blank line before a nested
definition,
found 0 |\n| 8685 | E128 | flake8 |`scripts/fix_all_errors.py`| 307 | continuation line
under-indented for visual indent |\n| 8684 | E128 | flake8 |`scripts/fix_all_errors.py`|
306 |
continuation line under-indented for visual indent |\n| 8683 | E115 | flake8
|`scripts/fix_all_errors.py`| 182 | expected an indented block (comment) |\n| 8682 | F401 | flake8
|`scripts/fix_all_errors.py`| 46 | 'typing.Callable' imported but unused |\n| 8681 | F401 | flake8
|`scripts/fix_all_errors.py`| 37 | 'os' imported but unused |\n| 8680 | E115 | flake8
|`scripts/dev-setup.py`| 763 | expected an indented block (comment) |\n| 8679 | E115 | flake8
|`scripts/check_type_coverage.py`| 128 | expected an indented block (comment) |\n| 8678 | E115 |
flake8 |`scripts/check_type_coverage.py`| 56 | expected an indented block (comment) |\n|
8677 | E115
| flake8 |`scripts/check_type_coverage.py`| 52 | expected an indented block (comment) |\n| 8676 |
E115 | flake8 |`scripts/actions_inspector.py`| 452 | expected an indented block (comment)
|\n| 8675
| E115 | flake8 |`scripts/actions_inspector.py`| 280 | expected an indented block (comment) |\n|
8674 | E115 | flake8 |`scripts/actions_inspector.py`| 274 | expected an indented block
(comment)
|\n| 8673 | E115 | flake8 |`scripts/actions_inspector.py`| 135 | expected an indented block
(comment) |\n| 8672 | E115 | flake8 |`scripts/actions_inspector.py`| 127 | expected an
indented
block (comment) |\n| 8671 | E115 | flake8 |`scripts/actions_inspector.py`| 118 | expected
an
indented block (comment) |\n| 8670 | E115 | flake8 |`scripts/actions_inspector.py`| 113 |
expected
an indented block (comment) |\n| 8669 | E115 | flake8 |`scripts/actions_inspector.py`| 105
|
expected an indented block (comment) |\n| 8668 | E115 | flake8
|`opt/web/panel/socketio_server.py`|
717 | expected an indented block (comment) |\n| 8667 | E115 | flake8
|`opt/web/panel/socketio_server.py`| 192 | expected an indented block (comment) |\n| 8666 | E115 |
flake8 |`opt/web/panel/routes/storage.py`| 270 | expected an indented block (comment) |\n|
8665 |
E115 | flake8 |`opt/web/panel/routes/storage.py`| 198 | expected an indented block
(comment) |\n|
8664 | E115 | flake8 |`opt/web/panel/routes/passthrough.py`| 487 | expected an indented
block
(comment) |\n| 8663 | E115 | flake8 |`opt/web/panel/routes/passthrough.py`| 293 | expected
an
indented block (comment) |\n| 8662 | E115 | flake8 |`opt/web/panel/routes/nodes.py`| 271 |
expected
an indented block (comment) |\n| 8661 | E115 | flake8 |`opt/web/panel/routes/nodes.py`|
199 |
expected an indented block (comment) |\n| 8660 | E115 | flake8
|`opt/web/panel/routes/health.py`| 95
| expected an indented block (comment) |\n| 8659 | E115 | flake8 |`opt/web/panel/routes/auth.py`|
447 | expected an indented block (comment) |\n| 8658 | E115 | flake8
|`opt/web/panel/routes/auth.py`| 401 | expected an indented block (comment) |\n| 8657 | E115 |
flake8 |`opt/web/panel/routes/auth.py`| 321 | expected an indented block (comment) |\n|
8656 | F821
| flake8 |`opt/web/panel/routes/auth.py`| 160 | undefined name 'time' |\n| 8655 | E115 | flake8
|`opt/web/panel/rbac.py`| 244 | expected an indented block (comment) |\n| 8654 | E122 | flake8
|`opt/web/panel/rbac.py`| 164 | continuation line missing indentation or outdented |\n| 8653 | E122
| flake8 |`opt/web/panel/rbac.py`| 157 | continuation line missing indentation or outdented |\n|
8652 | E122 | flake8 |`opt/web/panel/rbac.py`| 147 | continuation line missing indentation
or
outdented |\n| 8651 | E122 | flake8 |`opt/web/panel/rbac.py`| 128 | continuation line
missing
indentation or outdented |\n| 8650 | E115 | flake8 |`opt/web/panel/models/audit_log.py`|
369 |
expected an indented block (comment) |\n| 8649 | E115 | flake8
|`opt/web/panel/models/audit_log.py`|
358 | expected an indented block (comment) |\n| 8648 | E115 | flake8
|`opt/web/panel/models/audit_log.py`| 219 | expected an indented block (comment) |\n| 8647 | E115 |
flake8 |`opt/web/panel/graceful_shutdown.py`| 735 | expected an indented block (comment)
|\n| 8646 |
E115 | flake8 |`opt/web/panel/graceful_shutdown.py`| 641 | expected an indented block
(comment) |\n|
8645 | E115 | flake8 |`opt/web/panel/graceful_shutdown.py`| 425 | expected an indented
block
(comment) |\n| 8644 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 679 | expected an
indented
block (comment) |\n| 8643 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 657 |
expected an
indented block (comment) |\n| 8642 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`|
631 |
expected an indented block (comment) |\n| 8641 | E115 | flake8
|`opt/web/panel/core/rpc_client.py`|
598 | expected an indented block (comment) |\n| 8640 | E115 | flake8
|`opt/web/panel/core/rpc_client.py`| 575 | expected an indented block (comment) |\n| 8639 | E115 |
flake8 |`opt/web/panel/core/rpc_client.py`| 548 | expected an indented block (comment)
|\n| 8638 |
E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 515 | expected an indented block
(comment) |\n|
8637 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 463 | expected an indented block
(comment)
|\n| 8636 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 442 | expected an indented block
(comment) |\n| 8635 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 435 | expected an
indented
block (comment) |\n| 8634 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 384 |
expected an
indented block (comment) |\n| 8633 | E115 | flake8 |`opt/web/panel/core/rpc_client.py`|
282 |
expected an indented block (comment) |\n| 8632 | E115 | flake8
|`opt/web/panel/core/rpc_client.py`|
266 | expected an indented block (comment) |\n| 8631 | E115 | flake8
|`opt/web/panel/core/rpc_client.py`| 252 | expected an indented block (comment) |\n| 8630 | E115 |
flake8 |`opt/web/panel/core/rpc_client.py`| 221 | expected an indented block (comment)
|\n| 8629 |
E115 | flake8 |`opt/web/panel/core/rpc_client.py`| 212 | expected an indented block
(comment) |\n|
8628 | E115 | flake8 |`opt/web/panel/config.py`| 180 | expected an indented block
(comment) |\n|
8627 | E122 | flake8 |`opt/web/panel/config.py`| 109 | continuation line missing
indentation or
outdented |\n| 8626 | E115 | flake8 |`opt/web/panel/batch_operations.py`| 568 | expected
an indented
block (comment) |\n| 8625 | E115 | flake8 |`opt/web/panel/batch_operations.py`| 558 |
expected an
indented block (comment) |\n| 8624 | E115 | flake8 |`opt/web/panel/batch_operations.py`|
464 |
expected an indented block (comment) |\n| 8623 | E115 | flake8
|`opt/web/panel/batch_operations.py`|
430 | expected an indented block (comment) |\n| 8622 | E115 | flake8
|`opt/web/panel/batch_operations.py`| 406 | expected an indented block (comment) |\n| 8621 | E115 |
flake8 |`opt/web/panel/auth_2fa.py`| 864 | expected an indented block (comment) |\n| 8620
| E115 |
flake8 |`opt/web/panel/auth_2fa.py`| 857 | expected an indented block (comment) |\n| 8619
| E115 |
flake8 |`opt/web/panel/auth_2fa.py`| 853 | expected an indented block (comment) |\n| 8618
| E117 |
flake8 |`opt/web/panel/auth_2fa.py`| 774 | over-indented (comment) |\n| 8617 | E115 |
flake8
|`opt/web/panel/auth_2fa.py`| 772 | expected an indented block (comment) |\n| 8616 | E115 | flake8
|`opt/web/panel/auth_2fa.py`| 625 | expected an indented block (comment) |\n| 8615 | E115 | flake8
|`opt/web/panel/auth_2fa.py`| 421 | expected an indented block (comment) |\n| 8614 | E115 | flake8
|`opt/web/panel/auth_2fa.py`| 197 | expected an indented block (comment) |\n| 8613 | E115 | flake8
|`opt/web/panel/app.py`| 544 | expected an indented block (comment) |\n| 8612 | E115 | flake8
|`opt/web/panel/app.py`| 534 | expected an indented block (comment) |\n| 8611 | E115 | flake8
|`opt/web/panel/app.py`| 445 | expected an indented block (comment) |\n| 8610 | E115 | flake8
|`opt/web/panel/api_versioning.py`| 383 | expected an indented block (comment) |\n| 8609 | E115 |
flake8 |`opt/web/panel/api_versioning.py`| 360 | expected an indented block (comment) |\n|
8608 |
E115 | flake8 |`opt/web/panel/api_versioning.py`| 325 | expected an indented block
(comment) |\n|
8607 | E115 | flake8 |`opt/web/panel/analytics.py`| 442 | expected an indented block
(comment) |\n|
8606 | E115 | flake8 |`opt/web/panel/analytics.py`| 435 | expected an indented block
(comment) |\n|
8605 | E115 | flake8 |`opt/web/panel/analytics.py`| 399 | expected an indented block
(comment) |\n|
8604 | E115 | flake8 |`opt/web/panel/advanced_auth.py`| 491 | expected an indented block
(comment)
|\n| 8603 | E115 | flake8 |`opt/web/panel/advanced_auth.py`| 286 | expected an indented block
(comment) |\n| 8602 | E115 | flake8 |`opt/web/panel/advanced_auth.py`| 254 | expected an
indented
block (comment) |\n| 8601 | E115 | flake8 |`opt/tracing_integration.py`| 299 | expected an
indented
block (comment) |\n| 8600 | E115 | flake8 |`opt/tracing_integration.py`| 249 | expected an
indented
block (comment) |\n| 8599 | E115 | flake8 |`opt/tracing_integration.py`| 235 | expected an
indented
block (comment) |\n| 8598 | E115 | flake8 |`opt/tools/debvisor_menu.py`| 170 | expected an
indented
block (comment) |\n| 8597 | E115 | flake8 |`opt/tools/debvisor_menu.py`| 163 | expected an
indented
block (comment) |\n| 8596 | E115 | flake8 |`opt/tools/debvisor_menu.py`| 153 | expected an
indented
block (comment) |\n| 8595 | E115 | flake8 |`opt/testing/test_phase4_week4.py`| 632 |
expected an
indented block (comment) |\n| 8594 | E115 | flake8 |`opt/testing/test_phase4_week4.py`|
177 |
expected an indented block (comment) |\n| 8593 | E122 | flake8
|`opt/testing/test_e2e_comprehensive.py`| 603 | continuation line missing indentation or outdented
|\n| 8592 | E115 | flake8 |`opt/testing/mock_mode.py`| 718 | expected an indented block (comment)
|\n| 8591 | E115 | flake8 |`opt/testing/mock_mode.py`| 248 | expected an indented block (comment)
|\n| 8590 | E115 | flake8 |`opt/testing/framework.py`| 553 | expected an indented block (comment)
|\n| 8589 | E115 | flake8 |`opt/system/hypervisor/xen_driver.py`| 882 | expected an indented block
(comment) |\n| 8588 | E115 | flake8 |`opt/system/hypervisor/xen_driver.py`| 615 | expected
an
indented block (comment) |\n| 8587 | E115 | flake8 |`opt/system/hypervisor/xen_driver.py`|
601 |
expected an indented block (comment) |\n| 8586 | E115 | flake8
|`opt/system/hypervisor/xen_driver.py`| 364 | expected an indented block (comment) |\n| 8585 | E115
| flake8 |`opt/system/hypervisor/xen_driver.py`| 361 | expected an indented block (comment) |\n|
8584 | E115 | flake8 |`opt/system/hardware_detection.py`| 802 | expected an indented block
(comment)
|\n| 8583 | E115 | flake8 |`opt/system/hardware_detection.py`| 748 | expected an indented block
(comment) |\n| 8582 | E115 | flake8 |`opt/system/hardware_detection.py`| 644 | expected an
indented
block (comment) |\n| 8581 | E115 | flake8 |`opt/system/hardware_detection.py`| 512 |
expected an
indented block (comment) |\n| 8580 | E115 | flake8 |`opt/system/hardware_detection.py`|
452 |
expected an indented block (comment) |\n| 8579 | F541 | flake8
|`opt/services/virtualization/xen_manager.py`| 832 | f-string is missing placeholders |\n| 8578 |
E115 | flake8 |`opt/services/virtualization/xen_manager.py`| 704 | expected an indented
block
(comment) |\n| 8577 | E115 | flake8 |`opt/services/virtualization/xen_manager.py`| 671 |
expected an
indented block (comment) |\n| 8576 | F541 | flake8
|`opt/services/virtualization/xen_manager.py`|
552 | f-string is missing placeholders |\n| 8575 | E115 | flake8
|`opt/services/virtualization/xen_manager.py`| 546 | expected an indented block (comment) |\n| 8574
| E115 | flake8 |`opt/services/virtualization/xen_manager.py`| 541 | expected an indented block
(comment) |\n| 8573 | E115 | flake8 |`opt/services/virtualization/xen_manager.py`| 486 |
expected an
indented block (comment) |\n| 8572 | E115 | flake8
|`opt/services/virtualization/xen_manager.py`|
444 | expected an indented block (comment) |\n| 8571 | E115 | flake8
|`opt/services/virtualization/xen_manager.py`| 234 | expected an indented block (comment) |\n| 8570
| E115 | flake8 |`opt/services/virtualization/xen_manager.py`| 209 | expected an indented block
(comment) |\n| 8569 | F401 | flake8 |`opt/services/virtualization/xen_manager.py`| 97 |
'typing.Tuple' imported but unused |\n| 8568 | F401 | flake8
|`opt/services/virtualization/xen_manager.py`| 95 | 'datetime.timezone' imported but unused |\n|
8567 | F401 | flake8 |`opt/services/virtualization/xen_manager.py`| 95 |
'datetime.datetime'
imported but unused |\n| 8566 | F401 | flake8
|`opt/services/virtualization/xen_manager.py`| 88 |
'json' imported but unused |\n| 8565 | E115 | flake8 |`opt/services/tracing.py`| 697 |
expected an
indented block (comment) |\n| 8564 | E115 | flake8 |`opt/services/tracing.py`| 661 |
expected an
indented block (comment) |\n| 8563 | E115 | flake8 |`opt/services/tracing.py`| 438 |
expected an
indented block (comment) |\n| 8562 | E115 | flake8
|`opt/services/storage/multiregion_storage.py`|
741 | expected an indented block (comment) |\n| 8561 | E117 | flake8
|`opt/services/storage/multiregion_storage.py`| 641 | over-indented (comment) |\n| 8560 | E115 |
flake8 |`opt/services/storage/multiregion_storage.py`| 640 | expected an indented block
(comment)
|\n| 8559 | E115 | flake8 |`opt/services/storage/multiregion_storage.py`| 503 | expected an indented
block (comment) |\n| 8558 | E115 | flake8 |`opt/services/storage/multiregion_storage.py`|
401 |
expected an indented block (comment) |\n| 8557 | E115 | flake8
|`opt/services/slo_tracking.py`| 714
| expected an indented block (comment) |\n| 8556 | E115 | flake8 |`opt/services/slo_tracking.py`|
707 | expected an indented block (comment) |\n| 8555 | E115 | flake8
|`opt/services/slo_tracking.py`| 681 | expected an indented block (comment) |\n| 8554 | E115 |
flake8 |`opt/services/slo_tracking.py`| 665 | expected an indented block (comment) |\n|
8553 | E115
| flake8 |`opt/services/slo_tracking.py`| 628 | expected an indented block (comment) |\n| 8552 |
E115 | flake8 |`opt/services/slo_tracking.py`| 612 | expected an indented block (comment)
|\n| 8551
| E115 | flake8 |`opt/services/slo_tracking.py`| 546 | expected an indented block (comment) |\n|
8550 | E122 | flake8 |`opt/services/slo_tracking.py`| 517 | continuation line missing
indentation or
outdented |\n| 8549 | E115 | flake8 |`opt/services/slo_tracking.py`| 213 | expected an
indented
block (comment) |\n| 8548 | E122 | flake8 |`opt/services/security_hardening.py`| 373 |
continuation
line missing indentation or outdented |\n| 8547 | E115 | flake8
|`opt/services/security/ssh_hardening.py`| 819 | expected an indented block (comment) |\n| 8546 |
E115 | flake8 |`opt/services/security/ssh_hardening.py`| 693 | expected an indented block
(comment)
|\n| 8545 | E115 | flake8 |`opt/services/security/ssh_hardening.py`| 579 | expected an indented
block (comment) |\n| 8544 | E115 | flake8 |`opt/services/security/ssh_hardening.py`| 539 |
expected
an indented block (comment) |\n| 8543 | E115 | flake8
|`opt/services/security/firewall_manager.py`|
898 | expected an indented block (comment) |\n| 8542 | E115 | flake8
|`opt/services/security/firewall_manager.py`| 861 | expected an indented block (comment) |\n| 8541 |
E115 | flake8 |`opt/services/security/firewall_manager.py`| 853 | expected an indented
block
(comment) |\n| 8540 | E115 | flake8 |`opt/services/security/cert_pinning.py`| 410 |
expected an
indented block (comment) |\n| 8539 | E115 | flake8
|`opt/services/security/cert_pinning.py`| 330 |
expected an indented block (comment) |\n| 8538 | E115 | flake8
|`opt/services/security/acme_certificates.py`| 748 | expected an indented block (comment) |\n| 8537
| E115 | flake8 |`opt/services/security/acme_certificates.py`| 720 | expected an indented block
(comment) |\n| 8536 | E115 | flake8 |`opt/services/security/acme_certificates.py`| 593 |
expected an
indented block (comment) |\n| 8535 | E115 | flake8
|`opt/services/security/acme_certificates.py`|
540 | expected an indented block (comment) |\n| 8534 | E115 | flake8
|`opt/services/security/acme_certificates.py`| 516 | expected an indented block (comment) |\n| 8533
| E115 | flake8 |`opt/services/security/acme_certificates.py`| 343 | expected an indented block
(comment) |\n| 8532 | E115 | flake8 |`opt/services/secrets_management.py`| 655 | expected
an
indented block (comment) |\n| 8531 | E115 | flake8 |`opt/services/secrets_management.py`|
470 |
expected an indented block (comment) |\n| 8530 | E115 | flake8
|`opt/services/secrets_management.py`| 464 | expected an indented block (comment) |\n| 8529 | E115 |
flake8 |`opt/services/secrets_management.py`| 397 | expected an indented block (comment)
|\n| 8528 |
E115 | flake8 |`opt/services/secrets_management.py`| 340 | expected an indented block
(comment) |\n|
8527 | E115 | flake8 |`opt/services/secrets_management.py`| 276 | expected an indented
block
(comment) |\n| 8526 | E115 | flake8 |`opt/services/secrets_management.py`| 217 | expected
an
indented block (comment) |\n| 8525 | E115 | flake8 |`opt/services/secrets_management.py`|
206 |
expected an indented block (comment) |\n| 8524 | E115 | flake8
|`opt/services/secrets_management.py`| 192 | expected an indented block (comment) |\n| 8523 | E115 |
flake8 |`opt/services/secrets/vault_manager.py`| 564 | expected an indented block
(comment) |\n|
8522 | E115 | flake8 |`opt/services/secrets/vault_manager.py`| 494 | expected an indented
block
(comment) |\n| 8521 | E115 | flake8 |`opt/services/secrets/vault_manager.py`| 275 |
expected an
indented block (comment) |\n| 8520 | E115 | flake8
|`opt/services/secrets/vault_manager.py`| 180 |
expected an indented block (comment) |\n| 8519 | E115 | flake8
|`opt/services/sdn/sdn_controller.py`| 821 | expected an indented block (comment) |\n| 8518 | E115 |
flake8 |`opt/services/sdn/sdn_controller.py`| 667 | expected an indented block (comment)
|\n| 8517 |
E115 | flake8 |`opt/services/sdn/sdn_controller.py`| 156 | expected an indented block
(comment) |\n|
8516 | E115 | flake8 |`opt/services/sdn/sdn_controller.py`| 152 | expected an indented
block
(comment) |\n| 8515 | E115 | flake8 |`opt/services/scheduler/cli.py`| 675 | expected an
indented
block (comment) |\n| 8514 | E115 | flake8 |`opt/services/scheduler/api.py`| 191 | expected
an
indented block (comment) |\n| 8513 | E115 | flake8 |`opt/services/rpc/versioning.py`| 402
| expected
an indented block (comment) |\n| 8512 | E115 | flake8 |`opt/services/rpc/validators.py`|
464 |
expected an indented block (comment) |\n| 8511 | E115 | flake8
|`opt/services/rpc/validators.py`|
460 | expected an indented block (comment) |\n| 8510 | E115 | flake8
|`opt/services/rpc/validators.py`| 431 | expected an indented block (comment) |\n| 8509 | E115 |
flake8 |`opt/services/rpc/validators.py`| 419 | expected an indented block (comment) |\n|
8508 |
E115 | flake8 |`opt/services/rpc/validators.py`| 405 | expected an indented block
(comment) |\n|
8507 | E115 | flake8 |`opt/services/rpc/validators.py`| 330 | expected an indented block
(comment)
|\n| 8506 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 358 | undefined name
'Mock' |\n| 8505 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 357 |
undefined
name 'Mock' |\n| 8504 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 356
|
undefined name 'Mock' |\n| 8503 | F821 | flake8
|`opt/services/rpc/tests/test_rpc_features.py`| 349
| undefined name 'Mock' |\n| 8502 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`|
334 | undefined name 'Mock' |\n| 8501 | F821 | flake8
|`opt/services/rpc/tests/test_rpc_features.py`| 333 | undefined name 'Mock' |\n| 8500 | F821 |
flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 325 | undefined name 'Mock' |\n|
8499 | F821
| flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 158 | undefined name 'patch' |\n| 8498 |
F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 155 | undefined name 'Mock'
|\n| 8497
| F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 150 | undefined name 'Mock' |\n|
8496 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 149 | undefined name
'AsyncMock' |\n| 8495 | F821 | flake8 |`opt/services/rpc/tests/test_rpc_features.py`| 136
|
undefined name 'Mock' |\n| 8494 | F821 | flake8
|`opt/services/rpc/tests/test_rpc_features.py`| 135
| undefined name 'AsyncMock' |\n| 8493 | E115 | flake8 |`opt/services/rpc/service.py`| 381 |
expected an indented block (comment) |\n| 8492 | E115 | flake8
|`opt/services/rpc/service.py`| 214 |
expected an indented block (comment) |\n| 8491 | E115 | flake8
|`opt/services/rpc/service.py`| 203 |
expected an indented block (comment) |\n| 8490 | E115 | flake8
|`opt/services/rpc/server.py`| 761 |
expected an indented block (comment) |\n| 8489 | E115 | flake8
|`opt/services/rpc/server.py`| 710 |
expected an indented block (comment) |\n| 8488 | E115 | flake8
|`opt/services/rpc/server.py`| 573 |
expected an indented block (comment) |\n| 8487 | E115 | flake8
|`opt/services/rpc/server.py`| 412 |
expected an indented block (comment) |\n| 8486 | E115 | flake8
|`opt/services/rpc/server.py`| 360 |
expected an indented block (comment) |\n| 8485 | E115 | flake8
|`opt/services/rpc/server.py`| 310 |
expected an indented block (comment) |\n| 8484 | E115 | flake8
|`opt/services/rpc/server.py`| 270 |
expected an indented block (comment) |\n| 8483 | E115 | flake8
|`opt/services/rpc/server.py`| 222 |
expected an indented block (comment) |\n| 8482 | E115 | flake8
|`opt/services/rpc/server.py`| 170 |
expected an indented block (comment) |\n| 8481 | E116 | flake8
|`opt/services/rpc/server.py`| 150 |
unexpected indentation (comment) |\n| 8480 | E116 | flake8 |`opt/services/rpc/server.py`|
145 |
unexpected indentation (comment) |\n| 8479 | E116 | flake8 |`opt/services/rpc/server.py`|
140 |
unexpected indentation (comment) |\n| 8478 | E115 | flake8
|`opt/services/rpc/security_enhanced.py`|
692 | expected an indented block (comment) |\n| 8477 | E115 | flake8
|`opt/services/rpc/security_enhanced.py`| 599 | expected an indented block (comment) |\n| 8476 |
E115 | flake8 |`opt/services/rpc/rate_limiter.py`| 150 | expected an indented block
(comment) |\n|
8475 | E115 | flake8 |`opt/services/rpc/pool.py`| 376 | expected an indented block
(comment) |\n|
8474 | E115 | flake8 |`opt/services/rpc/pool.py`| 336 | expected an indented block
(comment) |\n|
8473 | E115 | flake8 |`opt/services/rpc/pool.py`| 311 | expected an indented block
(comment) |\n|
8472 | E115 | flake8 |`opt/services/rpc/pool.py`| 273 | expected an indented block
(comment) |\n|
8471 | E115 | flake8 |`opt/services/rpc/pool.py`| 210 | expected an indented block
(comment) |\n|
8470 | E115 | flake8 |`opt/services/rpc/pool.py`| 192 | expected an indented block
(comment) |\n|
8469 | E115 | flake8 |`opt/services/rpc/pool.py`| 130 | expected an indented block
(comment) |\n|
8468 | E115 | flake8 |`opt/services/rpc/health_check.py`| 208 | expected an indented block
(comment)
|\n| 8467 | E115 | flake8 |`opt/services/rpc/error_handling.py`| 336 | expected an indented block
(comment) |\n| 8466 | E115 | flake8 |`opt/services/rpc/compression.py`| 293 | expected an
indented
block (comment) |\n| 8465 | E115 | flake8 |`opt/services/rpc/cert_manager.py`| 196 |
expected an
indented block (comment) |\n| 8464 | E122 | flake8 |`opt/services/rpc/authz.py`| 316 |
continuation
line missing indentation or outdented |\n| 8463 | E115 | flake8
|`opt/services/rpc/authz.py`| 155 |
expected an indented block (comment) |\n| 8462 | E115 | flake8
|`opt/services/rpc/authz.py`| 152 |
expected an indented block (comment) |\n| 8461 | E116 | flake8
|`opt/services/rpc/authz.py`| 115 |
unexpected indentation (comment) |\n| 8460 | E116 | flake8 |`opt/services/rpc/auth.py`|
698 |
unexpected indentation (comment) |\n| 8459 | E115 | flake8 |`opt/services/rpc/auth.py`|
657 |
expected an indented block (comment) |\n| 8458 | E115 | flake8
|`opt/services/rpc/auth.py`| 514 |
expected an indented block (comment) |\n| 8457 | E115 | flake8
|`opt/services/rpc/auth.py`| 425 |
expected an indented block (comment) |\n| 8456 | E115 | flake8
|`opt/services/rpc/auth.py`| 257 |
expected an indented block (comment) |\n| 8455 | E115 | flake8
|`opt/services/rpc/audit.py`| 201 |
expected an indented block (comment) |\n| 8454 | E115 | flake8
|`opt/services/rpc/audit.py`| 175 |
expected an indented block (comment) |\n| 8453 | E115 | flake8
|`opt/services/resilience.py`| 528 |
expected an indented block (comment) |\n| 8452 | E115 | flake8
|`opt/services/resilience.py`| 276 |
expected an indented block (comment) |\n| 8451 | E115 | flake8
|`opt/services/resilience.py`| 244 |
expected an indented block (comment) |\n| 8450 | E115 | flake8
|`opt/services/request_signing.py`|
675 | expected an indented block (comment) |\n| 8449 | E115 | flake8
|`opt/services/request_signing.py`| 412 | expected an indented block (comment) |\n| 8448 | E115 |
flake8 |`opt/services/reporting_scheduler.py`| 522 | expected an indented block (comment)
|\n| 8447
| E115 | flake8 |`opt/services/reporting_scheduler.py`| 474 | expected an indented block (comment)
|\n| 8446 | E115 | flake8 |`opt/services/reporting_scheduler.py`| 383 | expected an indented block
(comment) |\n| 8445 | E115 | flake8 |`opt/services/reporting_scheduler.py`| 219 | expected
an
indented block (comment) |\n| 8444 | F821 | flake8
|`opt/services/rbac/fine_grained_rbac.py`| 592 |
undefined name 'logging' |\n| 8443 | F821 | flake8
|`opt/services/rbac/fine_grained_rbac.py`| 592 |
undefined name 'logging' |\n| 8442 | E115 | flake8
|`opt/services/rbac/fine_grained_rbac.py`| 541 |
expected an indented block (comment) |\n| 8441 | E115 | flake8
|`opt/services/rbac/fine_grained_rbac.py`| 222 | expected an indented block (comment) |\n| 8440 |
E115 | flake8 |`opt/services/rbac/fine_grained_rbac.py`| 182 | expected an indented block
(comment)
|\n| 8439 | F821 | flake8 |`opt/services/rbac/fine_grained_rbac.py`| 88 | undefined name 'logging'
|\n| 8438 | E115 | flake8 |`opt/services/query_optimization_enhanced.py`| 505 | expected an indented
block (comment) |\n| 8437 | E115 | flake8 |`opt/services/query_optimization.py`| 711 |
expected an
indented block (comment) |\n| 8436 | E115 | flake8 |`opt/services/profiling.py`| 588 |
expected an
indented block (comment) |\n| 8435 | E115 | flake8 |`opt/services/profiling.py`| 457 |
expected an
indented block (comment) |\n| 8434 | E115 | flake8 |`opt/services/profiling.py`| 399 |
expected an
indented block (comment) |\n| 8433 | F541 | flake8 |`opt/services/ops/ai_runbooks.py`| 789
|
f-string is missing placeholders |\n| 8432 | F401 | flake8
|`opt/services/ops/ai_runbooks.py`| 96 |
'pathlib.Path' imported but unused |\n| 8431 | F401 | flake8
|`opt/services/ops/ai_runbooks.py`| 95
| 'typing.Tuple' imported but unused |\n| 8430 | F401 | flake8 |`opt/services/ops/ai_runbooks.py`|
93 | 'datetime.timedelta' imported but unused |\n| 8429 | F401 | flake8
|`opt/services/ops/ai_runbooks.py`| 91 | 're' imported but unused |\n| 8428 | F401 | flake8
|`opt/services/ops/ai_runbooks.py`| 89 | 'json' imported but unused |\n| 8427 | E115 | flake8
|`opt/services/observability/energy.py`| 156 | expected an indented block (comment) |\n| 8426 | E115
| flake8 |`opt/services/observability/energy.py`| 119 | expected an indented block (comment) |\n|
8425 | E115 | flake8 |`opt/services/observability/energy.py`| 117 | expected an indented
block
(comment) |\n| 8424 | E115 | flake8
|`opt/services/observability/cardinality_controller.py`| 1248 |
expected an indented block (comment) |\n| 8423 | E115 | flake8
|`opt/services/observability/cardinality_controller.py`| 901 | expected an indented block (comment)
|\n| 8422 | E115 | flake8 |`opt/services/observability/cardinality_controller.py`| 849 | expected an
indented block (comment) |\n| 8421 | E115 | flake8
|`opt/services/observability/cardinality_controller.py`| 561 | expected an indented block (comment)
|\n| 8420 | E115 | flake8 |`opt/services/observability/cardinality_controller.py`| 516 | expected an
indented block (comment) |\n| 8419 | E115 | flake8
|`opt/services/observability/cardinality_controller.py`| 477 | expected an indented block (comment)
|\n| 8418 | F541 | flake8 |`opt/services/observability/carbon_telemetry.py`| 904 | f-string is
missing placeholders |\n| 8417 | E261 | flake8
|`opt/services/observability/carbon_telemetry.py`|
553 | at least two spaces before inline comment |\n| 8416 | E115 | flake8
|`opt/services/observability/carbon_telemetry.py`| 451 | expected an indented block (comment) |\n|
8415 | E115 | flake8 |`opt/services/observability/carbon_telemetry.py`| 416 | expected an
indented
block (comment) |\n| 8414 | E115 | flake8
|`opt/services/observability/carbon_telemetry.py`| 399 |
expected an indented block (comment) |\n| 8413 | E116 | flake8
|`opt/services/observability/carbon_telemetry.py`| 391 | unexpected indentation (comment) |\n| 8412
| E115 | flake8 |`opt/services/observability/carbon_telemetry.py`| 367 | expected an indented block
(comment) |\n| 8411 | E115 | flake8 |`opt/services/observability/carbon_telemetry.py`| 363
|
expected an indented block (comment) |\n| 8410 | E115 | flake8
|`opt/services/observability/carbon_telemetry.py`| 345 | expected an indented block (comment) |\n|
8409 | E301 | flake8 |`opt/services/observability/carbon_telemetry.py`| 342 | expected 1
blank line,
found 0 |\n| 8408 | E115 | flake8 |`opt/services/observability/carbon_telemetry.py`| 330 |
expected
an indented block (comment) |\n| 8407 | E115 | flake8
|`opt/services/observability/carbon_telemetry.py`| 300 | expected an indented block (comment) |\n|
8406 | E115 | flake8 |`opt/services/observability/carbon_telemetry.py`| 295 | expected an
indented
block (comment) |\n| 8405 | F401 | flake8
|`opt/services/observability/carbon_telemetry.py`| 90 |
'json' imported but unused |\n| 8404 | E115 | flake8
|`opt/services/network/multitenant_network.py`|
1146 | expected an indented block (comment) |\n| 8403 | E115 | flake8
|`opt/services/network/multitenant_network.py`| 1091 | expected an indented block (comment) |\n|
8402 | E115 | flake8 |`opt/services/network/multitenant_network.py`| 1086 | expected an
indented
block (comment) |\n| 8401 | E115 | flake8 |`opt/services/network/multitenant_network.py`|
835 |
expected an indented block (comment) |\n| 8400 | E115 | flake8
|`opt/services/network/multitenant_network.py`| 540 | expected an indented block (comment) |\n| 8399
| E115 | flake8 |`opt/services/network/multitenant_network.py`| 535 | expected an indented block
(comment) |\n| 8398 | E115 | flake8 |`opt/services/network/multitenant_network.py`| 355 |
expected
an indented block (comment) |\n| 8397 | E115 | flake8
|`opt/services/network/multitenant_network.py`| 344 | expected an indented block (comment) |\n| 8396
| E115 | flake8 |`opt/services/multiregion/replication_scheduler.py`| 1039 | expected an indented
block (comment) |\n| 8395 | E115 | flake8
|`opt/services/multiregion/replication_scheduler.py`| 1013
| expected an indented block (comment) |\n| 8394 | E115 | flake8
|`opt/services/multiregion/replication_scheduler.py`| 985 | expected an indented block (comment)
|\n| 8393 | E115 | flake8 |`opt/services/multiregion/replication_scheduler.py`| 981 | expected an
indented block (comment) |\n| 8392 | E115 | flake8
|`opt/services/multiregion/replication_scheduler.py`| 727 | expected an indented block (comment)
|\n| 8391 | E115 | flake8 |`opt/services/multiregion/replication_scheduler.py`| 723 | expected an
indented block (comment) |\n| 8390 | E115 | flake8
|`opt/services/multiregion/replication_scheduler.py`| 446 | expected an indented block (comment)
|\n| 8389 | E115 | flake8 |`opt/services/multiregion/k8s_integration.py`| 256 | expected an indented
block (comment) |\n| 8388 | E115 | flake8 |`opt/services/multiregion/k8s_integration.py`|
241 |
expected an indented block (comment) |\n| 8387 | E115 | flake8
|`opt/services/multiregion/k8s_integration.py`| 236 | expected an indented block (comment) |\n| 8386
| E115 | flake8 |`opt/services/multiregion/k8s_integration.py`| 163 | expected an indented block
(comment) |\n| 8385 | E115 | flake8 |`opt/services/multiregion/k8s_integration.py`| 150 |
expected
an indented block (comment) |\n| 8384 | E115 | flake8
|`opt/services/multiregion/failover.py`| 163 |
expected an indented block (comment) |\n| 8383 | F821 | flake8
|`opt/services/multiregion/core.py`|
922 | undefined name 'timezone' |\n| 8382 | F821 | flake8
|`opt/services/multiregion/core.py`| 922 |
undefined name 'datetime' |\n| 8381 | F821 | flake8 |`opt/services/multiregion/core.py`|
899 |
undefined name 'timezone' |\n| 8380 | F821 | flake8 |`opt/services/multiregion/core.py`|
899 |
undefined name 'datetime' |\n| 8379 | F821 | flake8 |`opt/services/multiregion/core.py`|
815 |
undefined name 'timezone' |\n| 8378 | F821 | flake8 |`opt/services/multiregion/core.py`|
815 |
undefined name 'datetime' |\n| 8377 | E115 | flake8 |`opt/services/multiregion/core.py`|
807 |
expected an indented block (comment) |\n| 8376 | F821 | flake8
|`opt/services/multiregion/core.py`|
728 | undefined name 'timezone' |\n| 8375 | F821 | flake8
|`opt/services/multiregion/core.py`| 728 |
undefined name 'datetime' |\n| 8374 | E115 | flake8 |`opt/services/multiregion/core.py`|
717 |
expected an indented block (comment) |\n| 8373 | F821 | flake8
|`opt/services/multiregion/core.py`|
453 | undefined name 'datetime' |\n| 8372 | F821 | flake8
|`opt/services/multiregion/core.py`| 433 |
undefined name 'timezone' |\n| 8371 | F821 | flake8 |`opt/services/multiregion/core.py`|
433 |
undefined name 'datetime' |\n| 8370 | F821 | flake8 |`opt/services/multiregion/core.py`|
431 |
undefined name 'datetime' |\n| 8369 | F821 | flake8 |`opt/services/multiregion/core.py`|
409 |
undefined name 'timezone' |\n| 8368 | F821 | flake8 |`opt/services/multiregion/core.py`|
409 |
undefined name 'datetime' |\n| 8367 | F821 | flake8 |`opt/services/multiregion/core.py`|
407 |
undefined name 'datetime' |\n| 8366 | E115 | flake8 |`opt/services/multiregion/core.py`|
390 |
expected an indented block (comment) |\n| 8365 | F821 | flake8
|`opt/services/multiregion/core.py`|
217 | undefined name 'datetime' |\n| 8364 | F821 | flake8
|`opt/services/multiregion/core.py`| 190 |
undefined name 'timezone' |\n| 8363 | F821 | flake8 |`opt/services/multiregion/core.py`|
190 |
undefined name 'datetime' |\n| 8362 | F821 | flake8 |`opt/services/multiregion/core.py`|
190 |
undefined name 'datetime' |\n| 8361 | F821 | flake8 |`opt/services/multiregion/core.py`|
156 |
undefined name 'timezone' |\n| 8360 | F821 | flake8 |`opt/services/multiregion/core.py`|
156 |
undefined name 'datetime' |\n| 8359 | F821 | flake8 |`opt/services/multiregion/core.py`|
156 |
undefined name 'datetime' |\n| 8358 | F821 | flake8 |`opt/services/multiregion/cli.py`|
557 |
undefined name 'sys' |\n| 8357 | F821 | flake8 |`opt/services/multiregion/cli.py`| 556 |
undefined
name 'sys' |\n| 8356 | F821 | flake8 |`opt/services/multiregion/cli.py`| 547 | undefined
name 'sys'
|\n| 8355 | F821 | flake8 |`opt/services/multiregion/cli.py`| 546 | undefined name 'sys' |\n| 8354 |
F821 | flake8 |`opt/services/multiregion/cli.py`| 528 | undefined name 'sys' |\n| 8353 |
F821 |
flake8 |`opt/services/multiregion/cli.py`| 527 | undefined name 'sys' |\n| 8352 | F821 |
flake8
|`opt/services/multiregion/cli.py`| 486 | undefined name 'sys' |\n| 8351 | F821 | flake8
|`opt/services/multiregion/cli.py`| 485 | undefined name 'sys' |\n| 8350 | F821 | flake8
|`opt/services/multiregion/cli.py`| 482 | undefined name 'sys' |\n| 8349 | F821 | flake8
|`opt/services/multiregion/cli.py`| 481 | undefined name 'sys' |\n| 8348 | F821 | flake8
|`opt/services/multiregion/cli.py`| 452 | undefined name 'sys' |\n| 8347 | F821 | flake8
|`opt/services/multiregion/cli.py`| 451 | undefined name 'sys' |\n| 8346 | F821 | flake8
|`opt/services/multiregion/cli.py`| 448 | undefined name 'sys' |\n| 8345 | F821 | flake8
|`opt/services/multiregion/cli.py`| 447 | undefined name 'sys' |\n| 8344 | F821 | flake8
|`opt/services/multiregion/cli.py`| 432 | undefined name 'sys' |\n| 8343 | F821 | flake8
|`opt/services/multiregion/cli.py`| 431 | undefined name 'sys' |\n| 8342 | F821 | flake8
|`opt/services/multiregion/cli.py`| 426 | undefined name 'sys' |\n| 8341 | F821 | flake8
|`opt/services/multiregion/cli.py`| 425 | undefined name 'sys' |\n| 8340 | F821 | flake8
|`opt/services/multiregion/cli.py`| 418 | undefined name 'sys' |\n| 8339 | F821 | flake8
|`opt/services/multiregion/cli.py`| 417 | undefined name 'sys' |\n| 8338 | F841 | flake8
|`opt/services/multiregion/cli.py`| 416 | local variable 'e' is assigned to but never used |\n| 8337
| F821 | flake8 |`opt/services/multiregion/cli.py`| 415 | undefined name 'sys' |\n| 8336 | F821 |
flake8 |`opt/services/multiregion/cli.py`| 414 | undefined name 'sys' |\n| 8335 | F821 |
flake8
|`opt/services/multiregion/cli.py`| 391 | undefined name 'sys' |\n| 8334 | F821 | flake8
|`opt/services/multiregion/cli.py`| 390 | undefined name 'sys' |\n| 8333 | F821 | flake8
|`opt/services/multiregion/cli.py`| 385 | undefined name 'sys' |\n| 8332 | F821 | flake8
|`opt/services/multiregion/cli.py`| 384 | undefined name 'sys' |\n| 8331 | F821 | flake8
|`opt/services/multiregion/cli.py`| 377 | undefined name 'sys' |\n| 8330 | F821 | flake8
|`opt/services/multiregion/cli.py`| 376 | undefined name 'sys' |\n| 8329 | F821 | flake8
|`opt/services/multiregion/cli.py`| 361 | undefined name 'sys' |\n| 8328 | F821 | flake8
|`opt/services/multiregion/cli.py`| 360 | undefined name 'sys' |\n| 8327 | F821 | flake8
|`opt/services/multiregion/cli.py`| 350 | undefined name 'sys' |\n| 8326 | F821 | flake8
|`opt/services/multiregion/cli.py`| 349 | undefined name 'sys' |\n| 8325 | E501 | flake8
|`opt/services/multiregion/cli.py`| 341 | line too long (121 > 120 characters) |\n| 8324 | F821 |
flake8 |`opt/services/multiregion/cli.py`| 327 | undefined name 'sys' |\n| 8323 | F821 |
flake8
|`opt/services/multiregion/cli.py`| 326 | undefined name 'sys' |\n| 8322 | F821 | flake8
|`opt/services/multiregion/cli.py`| 319 | undefined name 'sys' |\n| 8321 | F821 | flake8
|`opt/services/multiregion/cli.py`| 318 | undefined name 'sys' |\n| 8320 | F821 | flake8
|`opt/services/multiregion/cli.py`| 277 | undefined name 'sys' |\n| 8319 | F821 | flake8
|`opt/services/multiregion/cli.py`| 276 | undefined name 'sys' |\n| 8318 | E115 | flake8
|`opt/services/multi_cluster.py`| 630 | expected an indented block (comment) |\n| 8317 | E115 |
flake8 |`opt/services/multi_cluster.py`| 622 | expected an indented block (comment) |\n|
8316 | E115
| flake8 |`opt/services/multi_cluster.py`| 614 | expected an indented block (comment) |\n| 8315 |
E115 | flake8 |`opt/services/multi_cluster.py`| 580 | expected an indented block (comment)
|\n| 8314
| E115 | flake8 |`opt/services/multi_cluster.py`| 519 | expected an indented block (comment) |\n|
8313 | E115 | flake8 |`opt/services/multi_cluster.py`| 396 | expected an indented block
(comment)
|\n| 8312 | E115 | flake8 |`opt/services/migration/import_wizard.py`| 1295 | expected an indented
block (comment) |\n| 8311 | E115 | flake8 |`opt/services/migration/import_wizard.py`| 839
| expected
an indented block (comment) |\n| 8310 | E115 | flake8
|`opt/services/migration/import_wizard.py`|
481 | expected an indented block (comment) |\n| 8309 | E115 | flake8
|`opt/services/migration/import_wizard.py`| 282 | expected an indented block (comment) |\n| 8308 |
E115 | flake8 |`opt/services/migration/advanced_migration.py`| 977 | expected an indented
block
(comment) |\n| 8307 | E115 | flake8 |`opt/services/migration/advanced_migration.py`| 796 |
expected
an indented block (comment) |\n| 8306 | E115 | flake8
|`opt/services/migration/advanced_migration.py`| 728 | expected an indented block (comment) |\n|
8305 | E115 | flake8 |`opt/services/migration/advanced_migration.py`| 673 | expected an
indented
block (comment) |\n| 8304 | E115 | flake8 |`opt/services/migration/advanced_migration.py`|
450 |
expected an indented block (comment) |\n| 8303 | E115 | flake8
|`opt/services/message_queue.py`| 161
| expected an indented block (comment) |\n| 8302 | E115 | flake8
|`opt/services/marketplace/marketplace_service.py`| 1289 | expected an indented block (comment) |\n|
8301 | E115 | flake8 |`opt/services/marketplace/marketplace_service.py`| 1017 | expected
an indented
block (comment) |\n| 8300 | E115 | flake8
|`opt/services/marketplace/marketplace_service.py`| 990 |
expected an indented block (comment) |\n| 8299 | E115 | flake8
|`opt/services/marketplace/marketplace_service.py`| 680 | expected an indented block (comment) |\n|
8298 | F541 | flake8 |`opt/services/marketplace/governance.py`| 784 | f-string is missing
placeholders |\n| 8297 | E115 | flake8 |`opt/services/marketplace/governance.py`| 614 |
expected an
indented block (comment) |\n| 8296 | E128 | flake8
|`opt/services/marketplace/governance.py`| 608 |
continuation line under-indented for visual indent |\n| 8295 | E115 | flake8
|`opt/services/marketplace/governance.py`| 334 | expected an indented block (comment) |\n| 8294 |
E115 | flake8 |`opt/services/marketplace/governance.py`| 329 | expected an indented block
(comment)
|\n| 8293 | E115 | flake8 |`opt/services/marketplace/governance.py`| 324 | expected an indented
block (comment) |\n| 8292 | E115 | flake8 |`opt/services/marketplace/governance.py`| 319 |
expected
an indented block (comment) |\n| 8291 | E115 | flake8
|`opt/services/marketplace/governance.py`| 317
| expected an indented block (comment) |\n| 8290 | F401 | flake8
|`opt/services/marketplace/governance.py`| 94 | 'subprocess' imported but unused |\n| 8289 | F401 |
flake8 |`opt/services/marketplace/governance.py`| 93 | 'pathlib.Path' imported but unused
|\n| 8288
| F401 | flake8 |`opt/services/marketplace/governance.py`| 92 | 'typing.Tuple' imported but unused
|\n| 8287 | F401 | flake8 |`opt/services/marketplace/governance.py`| 92 | 'typing.Set' imported but
unused |\n| 8286 | F401 | flake8 |`opt/services/marketplace/governance.py`| 90 |
'datetime.timedelta' imported but unused |\n| 8285 | F401 | flake8
|`opt/services/marketplace/governance.py`| 88 | 're' imported but unused |\n| 8284 | F401 | flake8
|`opt/services/marketplace/governance.py`| 86 | 'json' imported but unused |\n| 8283 | F401 | flake8
|`opt/services/marketplace/governance.py`| 85 | 'hashlib' imported but unused |\n| 8282 | E115 |
flake8 |`opt/services/licensing/licensing_server.py`| 902 | expected an indented block
(comment)
|\n| 8281 | E115 | flake8 |`opt/services/licensing/licensing_server.py`| 855 | expected an indented
block (comment) |\n| 8280 | E115 | flake8 |`opt/services/licensing/licensing_server.py`|
665 |
expected an indented block (comment) |\n| 8279 | E115 | flake8
|`opt/services/licensing/licensing_server.py`| 585 | expected an indented block (comment) |\n| 8278
| F821 | flake8 |`opt/services/licensing/licensing_server.py`| 396 | undefined name 'hashlib' |\n|
8277 | F821 | flake8 |`opt/services/licensing/licensing_server.py`| 392 | undefined name
'platform'
|\n| 8276 | F821 | flake8 |`opt/services/licensing/licensing_server.py`| 391 | undefined name
'platform' |\n| 8275 | F821 | flake8 |`opt/services/licensing/licensing_server.py`| 381 |
undefined
name 'platform' |\n| 8274 | F821 | flake8 |`opt/services/licensing/licensing_server.py`|
367 |
undefined name 'platform' |\n| 8273 | F821 | flake8
|`opt/services/licensing/licensing_server.py`|
356 | undefined name 'platform' |\n| 8272 | F821 | flake8
|`opt/services/licensing/licensing_server.py`| 353 | undefined name 'platform' |\n| 8271 | F821 |
flake8 |`opt/services/licensing/licensing_server.py`| 339 | undefined name 'hashlib' |\n|
8270 |
E115 | flake8 |`opt/services/health_check.py`| 352 | expected an indented block (comment)
|\n| 8269
| E115 | flake8 |`opt/services/health_check.py`| 291 | expected an indented block (comment) |\n|
8268 | E115 | flake8 |`opt/services/health_check.py`| 285 | expected an indented block
(comment)
|\n| 8267 | E115 | flake8 |`opt/services/ha/fencing_agent.py`| 732 | expected an indented block
(comment) |\n| 8266 | E115 | flake8 |`opt/services/ha/fencing_agent.py`| 558 | expected an
indented
block (comment) |\n| 8265 | E115 | flake8 |`opt/services/ha/fencing_agent.py`| 413 |
expected an
indented block (comment) |\n| 8264 | E115 | flake8 |`opt/services/ha/fencing_agent.py`|
410 |
expected an indented block (comment) |\n| 8263 | E115 | flake8
|`opt/services/ha/fencing_agent.py`|
406 | expected an indented block (comment) |\n| 8262 | E115 | flake8
|`opt/services/ha/fencing_agent.py`| 375 | expected an indented block (comment) |\n| 8261 | E115 |
flake8 |`opt/services/ha/fencing_agent.py`| 371 | expected an indented block (comment)
|\n| 8260 |
E115 | flake8 |`opt/services/ha/fencing_agent.py`| 369 | expected an indented block
(comment) |\n|
8259 | E115 | flake8 |`opt/services/ha/fencing_agent.py`| 366 | expected an indented block
(comment)
|\n| 8258 | E115 | flake8 |`opt/services/ha/fencing_agent.py`| 241 | expected an indented block
(comment) |\n| 8257 | E115 | flake8 |`opt/services/feature_flags.py`| 153 | expected an
indented
block (comment) |\n| 8256 | E115 | flake8 |`opt/services/feature_flags.py`| 123 | expected
an
indented block (comment) |\n| 8255 | E115 | flake8 |`opt/services/dns/hosting.py`| 274 |
expected an
indented block (comment) |\n| 8254 | E115 | flake8 |`opt/services/diagnostics.py`| 379 |
expected an
indented block (comment) |\n| 8253 | E115 | flake8 |`opt/services/diagnostics.py`| 373 |
expected an
indented block (comment) |\n| 8252 | E115 | flake8 |`opt/services/diagnostics.py`| 307 |
expected an
indented block (comment) |\n| 8251 | E115 | flake8 |`opt/services/diagnostics.py`| 241 |
expected an
indented block (comment) |\n| 8250 | E115 | flake8 |`opt/services/diagnostics.py`| 188 |
expected an
indented block (comment) |\n| 8249 | E115 | flake8
|`opt/services/database/query_optimizer.py`| 625
| expected an indented block (comment) |\n| 8248 | E115 | flake8
|`opt/services/database/query_optimizer.py`| 534 | expected an indented block (comment) |\n| 8247 |
E115 | flake8 |`opt/services/database/query_optimizer.py`| 426 | expected an indented
block
(comment) |\n| 8246 | E115 | flake8 |`opt/services/database/query_optimizer.py`| 275 |
expected an
indented block (comment) |\n| 8245 | E115 | flake8
|`opt/services/cost_optimization/core.py`| 137 |
expected an indented block (comment) |\n| 8244 | E115 | flake8
|`opt/services/cost/cost_engine.py`|
894 | expected an indented block (comment) |\n| 8243 | E115 | flake8
|`opt/services/cost/cost_engine.py`| 494 | expected an indented block (comment) |\n| 8242 | E122 |
flake8 |`opt/services/cost/cost_engine.py`| 312 | continuation line missing indentation or
outdented
|\n| 8241 | E115 | flake8 |`opt/services/containers/container_integration.py`| 1036 | expected an
indented block (comment) |\n| 8240 | E115 | flake8
|`opt/services/containers/container_integration.py`| 878 | expected an indented block (comment) |\n|
8239 | E115 | flake8 |`opt/services/containers/container_integration.py`| 851 | expected
an indented
block (comment) |\n| 8238 | E115 | flake8
|`opt/services/containers/container_integration.py`| 377 |
expected an indented block (comment) |\n| 8237 | E115 | flake8
|`opt/services/containers/container_integration.py`| 372 | expected an indented block (comment) |\n|
8236 | E115 | flake8 |`opt/services/containers/container_integration.py`| 295 | expected
an indented
block (comment) |\n| 8235 | E115 | flake8
|`opt/services/containers/container_integration.py`| 293 |
expected an indented block (comment) |\n| 8234 | E115 | flake8
|`opt/services/connection_pool.py`|
843 | expected an indented block (comment) |\n| 8233 | E115 | flake8
|`opt/services/connection_pool.py`| 698 | expected an indented block (comment) |\n| 8232 | E115 |
flake8 |`opt/services/connection_pool.py`| 662 | expected an indented block (comment) |\n|
8231 |
E115 | flake8 |`opt/services/connection_pool.py`| 499 | expected an indented block
(comment) |\n|
8230 | E115 | flake8 |`opt/services/connection_pool.py`| 496 | expected an indented block
(comment)
|\n| 8229 | E115 | flake8 |`opt/services/compliance/reporting.py`| 132 | expected an indented block
(comment) |\n| 8228 | E115 | flake8 |`opt/services/compliance/remediation.py`| 109 |
expected an
indented block (comment) |\n| 8227 | E115 | flake8 |`opt/services/compliance/cli.py`| 143
| expected
an indented block (comment) |\n| 8226 | F541 | flake8
|`opt/services/compliance/auto_remediation.py`| 795 | f-string is missing placeholders |\n| 8225 |
F541 | flake8 |`opt/services/compliance/auto_remediation.py`| 789 | f-string is missing
placeholders
|\n| 8224 | F541 | flake8 |`opt/services/compliance/auto_remediation.py`| 784 | f-string is missing
placeholders |\n| 8223 | E115 | flake8 |`opt/services/compliance/auto_remediation.py`| 729
|
expected an indented block (comment) |\n| 8222 | E115 | flake8
|`opt/services/compliance/auto_remediation.py`| 560 | expected an indented block (comment) |\n| 8221
| E115 | flake8 |`opt/services/compliance/auto_remediation.py`| 519 | expected an indented block
(comment) |\n| 8220 | E115 | flake8 |`opt/services/compliance/auto_remediation.py`| 471 |
expected
an indented block (comment) |\n| 8219 | E115 | flake8
|`opt/services/compliance/auto_remediation.py`| 234 | expected an indented block (comment) |\n| 8218
| F401 | flake8 |`opt/services/compliance/auto_remediation.py`| 93 | 'pathlib.Path' imported but
unused |\n| 8217 | F401 | flake8 |`opt/services/compliance/auto_remediation.py`| 92 |
'typing.Tuple'
imported but unused |\n| 8216 | F401 | flake8
|`opt/services/compliance/auto_remediation.py`| 92 |
'typing.Callable' imported but unused |\n| 8215 | E115 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 956 | expected an indented block (comment) |\n|
8214 | E115 | flake8 |`opt/services/cluster/large_cluster_optimizer.py`| 945 | expected an
indented
block (comment) |\n| 8213 | E116 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 882 |
unexpected indentation (comment) |\n| 8212 | E115 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 555 | expected an indented block (comment) |\n|
8211 | E115 | flake8 |`opt/services/cluster/large_cluster_optimizer.py`| 523 | expected an
indented
block (comment) |\n| 8210 | E115 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 515 |
expected an indented block (comment) |\n| 8209 | E115 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 508 | expected an indented block (comment) |\n|
8208 | E115 | flake8 |`opt/services/cluster/large_cluster_optimizer.py`| 501 | expected an
indented
block (comment) |\n| 8207 | E115 | flake8
|`opt/services/cluster/large_cluster_optimizer.py`| 407 |
expected an indented block (comment) |\n| 8206 | E115 | flake8 |`opt/services/cache.py`|
584 |
expected an indented block (comment) |\n| 8205 | E115 | flake8 |`opt/services/cache.py`|
528 |
expected an indented block (comment) |\n| 8204 | E115 | flake8 |`opt/services/cache.py`|
523 |
expected an indented block (comment) |\n| 8203 | E115 | flake8 |`opt/services/cache.py`|
505 |
expected an indented block (comment) |\n| 8202 | E115 | flake8 |`opt/services/cache.py`|
274 |
expected an indented block (comment) |\n| 8201 | E122 | flake8
|`opt/services/business_metrics.py`|
299 | continuation line missing indentation or outdented |\n| 8200 | E115 |
flake8
|`opt/services/business_metrics.py`| 180 | expected an indented block (comment) |\n| 8199 | F821 |
flake8 |`opt/services/billing/billing_integration.py`| 587 | undefined name 'hashlib' |\n|
8198 |
E115 | flake8 |`opt/services/backup_manager.py`| 428 | expected an indented block
(comment) |\n|
8197 | E115 | flake8 |`opt/services/backup_manager.py`| 256 | expected an indented block
(comment)
|\n| 8196 | E115 | flake8 |`opt/services/backup_manager.py`| 227 | expected an indented block
(comment) |\n| 8195 | E115 | flake8 |`opt/services/backup_manager.py`| 195 | expected an
indented
block (comment) |\n| 8194 | E115 | flake8 |`opt/services/backup/dedup_backup_service.py`|
848 |
expected an indented block (comment) |\n| 8193 | E115 | flake8
|`opt/services/backup/backup_intelligence.py`| 1114 | expected an indented block (comment) |\n| 8192
| E116 | flake8 |`opt/services/backup/backup_intelligence.py`| 721 | unexpected indentation
(comment) |\n| 8191 | E116 | flake8 |`opt/services/backup/backup_intelligence.py`| 711 |
unexpected
indentation (comment) |\n| 8190 | E116 | flake8
|`opt/services/backup/backup_intelligence.py`| 701 |
unexpected indentation (comment) |\n| 8189 | E115 | flake8
|`opt/services/backup/backup_intelligence.py`| 605 | expected an indented block (comment) |\n| 8188
| E115 | flake8 |`opt/services/backup/backup_intelligence.py`| 431 | expected an indented block
(comment) |\n| 8187 | E115 | flake8 |`opt/services/backup/backup_intelligence.py`| 325 |
expected an
indented block (comment) |\n| 8186 | E115 | flake8 |`opt/services/auth/ldap_backend.py`|
547 |
expected an indented block (comment) |\n| 8185 | E115 | flake8
|`opt/services/auth/ldap_backend.py`|
466 | expected an indented block (comment) |\n| 8184 | E115 | flake8
|`opt/services/auth/ldap_backend.py`| 380 | expected an indented block (comment) |\n| 8183 | E115 |
flake8 |`opt/services/auth/ldap_backend.py`| 364 | expected an indented block (comment)
|\n| 8182 |
E115 | flake8 |`opt/services/auth/ldap_backend.py`| 334 | expected an indented block
(comment) |\n|
8181 | E115 | flake8 |`opt/services/auth/ldap_backend.py`| 322 | expected an indented
block
(comment) |\n| 8180 | E115 | flake8 |`opt/services/auth/ldap_backend.py`| 294 | expected
an indented
block (comment) |\n| 8179 | E115 | flake8 |`opt/services/auth/ldap_backend.py`| 193 |
expected an
indented block (comment) |\n| 8178 | E115 | flake8 |`opt/services/audit_encryption.py`|
405 |
expected an indented block (comment) |\n| 8177 | E115 | flake8
|`opt/services/api_key_rotation.py`|
611 | expected an indented block (comment) |\n| 8176 | E115 | flake8
|`opt/services/api_key_rotation.py`| 284 | expected an indented block (comment) |\n| 8175 | E115 |
flake8 |`opt/services/api_key_manager.py`| 294 | expected an indented block (comment) |\n|
8174 |
E115 | flake8 |`opt/services/anomaly/test_lstm.py`| 83 | expected an indented block
(comment) |\n|
8173 | E115 | flake8 |`opt/services/anomaly/core.py`| 1131 | expected an indented block
(comment)
|\n| 8172 | E115 | flake8 |`opt/services/anomaly/core.py`| 685 | expected an indented block
(comment) |\n| 8171 | E115 | flake8 |`opt/services/anomaly/core.py`| 628 | expected an
indented
block (comment) |\n| 8170 | E115 | flake8 |`opt/services/anomaly/core.py`| 570 | expected
an
indented block (comment) |\n| 8169 | E115 | flake8 |`opt/services/anomaly/core.py`| 363 |
expected
an indented block (comment) |\n| 8168 | E115 | flake8 |`opt/services/anomaly/core.py`| 356
|
expected an indented block (comment) |\n| 8167 | E115 | flake8
|`opt/plugin_architecture.py`| 465 |
expected an indented block (comment) |\n| 8166 | E115 | flake8
|`opt/plugin_architecture.py`| 389 |
expected an indented block (comment) |\n| 8165 | E115 | flake8
|`opt/plugin_architecture.py`| 289 |
expected an indented block (comment) |\n| 8164 | E115 | flake8
|`opt/plugin_architecture.py`| 269 |
expected an indented block (comment) |\n| 8163 | E115 | flake8 |`opt/netcfg_tui_full.py`|
611 |
expected an indented block (comment) |\n| 8162 | E115 | flake8 |`opt/netcfg_tui_full.py`|
609 |
expected an indented block (comment) |\n| 8161 | E115 | flake8 |`opt/netcfg_tui_app.py`|
330 |
expected an indented block (comment) |\n| 8160 | E115 | flake8 |`opt/netcfg_tui_app.py`|
242 |
expected an indented block (comment) |\n| 8159 | E115 | flake8 |`opt/netcfg_tui_app.py`|
120 |
expected an indented block (comment) |\n| 8158 | E115 | flake8 |`opt/netcfg_tui_app.py`|
89 |
expected an indented block (comment) |\n| 8157 | E115 | flake8
|`opt/netcfg-tui/netcfg_tui.py`| 1385
| expected an indented block (comment) |\n| 8156 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`|
1381 | expected an indented block (comment) |\n| 8155 | E115 | flake8
|`opt/netcfg-tui/netcfg_tui.py`| 1377 | expected an indented block (comment) |\n| 8154 | E115 |
flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1350 | expected an indented block (comment) |\n|
8153 | E115
| flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1340 | expected an indented block (comment) |\n| 8152 |
E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1332 | expected an indented block (comment)
|\n| 8151
| E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1161 | expected an indented block (comment) |\n|
8150 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1153 | expected an indented block
(comment)
|\n| 8149 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1147 | expected an indented block
(comment) |\n| 8148 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1116 | expected an
indented
block (comment) |\n| 8147 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 1077 | expected
an
indented block (comment) |\n| 8146 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 904 |
expected
an indented block (comment) |\n| 8145 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 850
|
expected an indented block (comment) |\n| 8144 | E115 | flake8
|`opt/netcfg-tui/netcfg_tui.py`| 835
| expected an indented block (comment) |\n| 8143 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`|
828 | expected an indented block (comment) |\n| 8142 | E115 | flake8
|`opt/netcfg-tui/netcfg_tui.py`| 770 | expected an indented block (comment) |\n| 8141 | E116 |
flake8 |`opt/netcfg-tui/netcfg_tui.py`| 761 | unexpected indentation (comment) |\n| 8140 |
E115 |
flake8 |`opt/netcfg-tui/netcfg_tui.py`| 758 | expected an indented block (comment) |\n|
8139 | E115
| flake8 |`opt/netcfg-tui/netcfg_tui.py`| 711 | expected an indented block (comment) |\n| 8138 |
E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 641 | expected an indented block (comment)
|\n| 8137
| E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 440 | expected an indented block (comment) |\n|
8136 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 289 | expected an indented block
(comment)
|\n| 8135 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 231 | expected an indented block
(comment) |\n| 8134 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 223 | expected an
indented
block (comment) |\n| 8133 | E115 | flake8 |`opt/netcfg-tui/netcfg_tui.py`| 206 | expected
an
indented block (comment) |\n| 8132 | E115 | flake8 |`opt/netcfg-tui/main.py`| 666 |
expected an
indented block (comment) |\n| 8131 | E115 | flake8 |`opt/netcfg-tui/main.py`| 198 |
expected an
indented block (comment) |\n| 8130 | E115 | flake8 |`opt/netcfg-tui/backends.py`| 452 |
expected an
indented block (comment) |\n| 8129 | E115 | flake8
|`opt/monitoring/fixtures/generator/app.py`| 118
| expected an indented block (comment) |\n| 8128 | E115 | flake8 |`opt/monitoring/enhanced.py`| 404
| expected an indented block (comment) |\n| 8127 | E116 | flake8 |`opt/models/migrations.py`| 364 |
unexpected indentation (comment) |\n| 8126 | E122 | flake8 |`opt/models/migrations.py`|
112 |
continuation line missing indentation or outdented |\n| 8125 | E116 | flake8
|`opt/migrations/env.py`| 110 | unexpected indentation (comment) |\n| 8124 | E115 | flake8
|`opt/migrations/env.py`| 90 | expected an indented block (comment) |\n| 8123 | E115 | flake8
|`opt/migrations/env.py`| 87 | expected an indented block (comment) |\n| 8122 | E115 | flake8
|`opt/k8sctl_enhanced.py`| 532 | expected an indented block (comment) |\n| 8121 | E115 | flake8
|`opt/k8sctl_enhanced.py`| 398 | expected an indented block (comment) |\n| 8120 | E115 | flake8
|`opt/k8sctl_enhanced.py`| 314 | expected an indented block (comment) |\n| 8119 | E115 | flake8
|`opt/hvctl_enhanced.py`| 742 | expected an indented block (comment) |\n| 8118 | E115 | flake8
|`opt/hvctl_enhanced.py`| 429 | expected an indented block (comment) |\n| 8117 | E115 | flake8
|`opt/hvctl_enhanced.py`| 400 | expected an indented block (comment) |\n| 8116 | E115 | flake8
|`opt/hvctl_enhanced.py`| 284 | expected an indented block (comment) |\n| 8115 | E115 | flake8
|`opt/graphql_integration.py`| 117 | expected an indented block (comment) |\n| 8114 | E115 | flake8
|`opt/graphql_api.py`| 982 | expected an indented block (comment) |\n| 8113 | E115 | flake8
|`opt/graphql_api.py`| 578 | expected an indented block (comment) |\n| 8112 | E115 | flake8
|`opt/e2e_testing.py`| 590 | expected an indented block (comment) |\n| 8111 | E115 | flake8
|`opt/dvctl.py`| 296 | expected an indented block (comment) |\n| 8110 | E115 | flake8
|`opt/dvctl.py`| 293 | expected an indented block (comment) |\n| 8109 | E115 | flake8
|`opt/distributed_tracing.py`| 444 | expected an indented block (comment) |\n| 8108 | E115 | flake8
|`opt/distributed_tracing.py`| 322 | expected an indented block (comment) |\n| 8107 | E115 | flake8
|`opt/distributed_tracing.py`| 320 | expected an indented block (comment) |\n| 8106 | E115 | flake8
|`opt/distributed_tracing.py`| 251 | expected an indented block (comment) |\n| 8105 | E115 | flake8
|`opt/discovery/zerotouch.py`| 178 | expected an indented block (comment) |\n| 8104 | E115 | flake8
|`opt/deployment/migrations.py`| 289 | expected an indented block (comment) |\n| 8103 | E115 |
flake8 |`opt/deployment/migrations.py`| 243 | expected an indented block (comment) |\n|
8102 | E115
| flake8 |`opt/deployment/configuration.py`| 492 | expected an indented block (comment) |\n| 8101 |
E115 | flake8 |`opt/core/unified_backend.py`| 1103 | expected an indented block (comment)
|\n| 8100
| E115 | flake8 |`opt/core/unified_backend.py`| 171 | expected an indented block (comment) |\n| 8099
| E115 | flake8 |`opt/core/request_context.py`| 699 | expected an indented block (comment) |\n| 8098
| E115 | flake8 |`opt/core/request_context.py`| 695 | expected an indented block (comment) |\n| 8097
| E115 | flake8 |`opt/core/request_context.py`| 647 | expected an indented block (comment) |\n| 8096
| E115 | flake8 |`opt/core/config.py`| 256 | expected an indented block (comment) |\n| 8095 | E115 |
flake8 |`opt/core/config.py`| 123 | expected an indented block (comment) |\n| 8094 | E115
| flake8
|`opt/core/config.py`| 94 | expected an indented block (comment) |\n| 8093 | E115 | flake8
|`opt/core/cli_utils.py`| 102 | expected an indented block (comment) |\n| 8092 | E115 | flake8
|`opt/core/cli_utils.py`| 95 | expected an indented block (comment) |\n| 8091 | E115 | flake8
|`opt/config_distributor.py`| 235 | expected an indented block (comment) |\n| 8090 | E116 | flake8
|`opt/config_distributor.py`| 160 | unexpected indentation (comment) |\n| 8089 | E115 | flake8
|`opt/config/validate-packages.py`| 222 | expected an indented block (comment) |\n| 8088 | E115 |
flake8 |`opt/config/validate-packages.py`| 208 | expected an indented block (comment) |\n|
8087 |
E115 | flake8 |`opt/cephctl_enhanced.py`| 452 | expected an indented block (comment) |\n|
8086 |
E115 | flake8 |`opt/cephctl_enhanced.py`| 314 | expected an indented block (comment) |\n|
8085 |
E115 | flake8 |`opt/cephctl_enhanced.py`| 249 | expected an indented block (comment) |\n|
8084 |
E115 | flake8 |`opt/ansible/validate-inventory.py`| 310 | expected an indented block
(comment) |\n|
8083 | E115 | flake8 |`opt/advanced_features.py`| 737 | expected an indented block
(comment) |\n|
8082 | E115 | flake8 |`etc/debvisor/test_validate_blocklists.py`| 540 | expected an
indented block
(comment) |\n| 8081 | E115 | flake8 |`etc/debvisor/test_validate_blocklists.py`| 157 |
expected an
indented block (comment) |\n| 8080 | E115 | flake8
|`etc/debvisor/test_validate_blocklists.py`| 60 |
expected an indented block (comment) |\n| 8079 | E116 | flake8
|`etc/debvisor/test_validate_blocklists.py`| 35 | unexpected indentation (comment) |\n| 8078 |
py/clear-text-logging-sensitive-data | CodeQL |`scripts/fix_all_errors.py`| 102 | This
expression
logs sensitive data (secret) as clear text. |\n| 8077 | PinnedDependenciesID |
Scorecard
|`.github/workflows/test.yml`| 94 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8076 | PinnedDependenciesID | Scorecard
|`.github/workflows/test.yml`| 80 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8074 | PinnedDependenciesID | Scorecard
|`.github/workflows/test.yml`| 35 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8073 | PinnedDependenciesID | Scorecard
|`.github/workflows/test.yml`| 32 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8072 | PinnedDependenciesID | Scorecard
|`.github/workflows/lint.yml`| 114 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8071 | PinnedDependenciesID | Scorecard
|`.github/workflows/architecture.yml`| 24 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8070 | PinnedDependenciesID |
Scorecard
|`.github/workflows/architecture.yml`| 24 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8069 | PinnedDependenciesID |
Scorecard
|`.github/workflows/validate-syntax.yml`| 141 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8068 | PinnedDependenciesID |
Scorecard
|`.github/workflows/validate-syntax.yml`| 139 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8067 | PinnedDependenciesID |
Scorecard
|`.github/workflows/validate-grafana.yml`| 36 | score is 4: npmCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8066 | PinnedDependenciesID |
Scorecard
|`.github/workflows/validate-configs.yml`| 46 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8065 | PinnedDependenciesID |
Scorecard
|`.github/workflows/type-check.yml`| 35 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8064 | PinnedDependenciesID |
Scorecard
|`.github/workflows/type-check.yml`| 34 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8063 | PinnedDependenciesID |
Scorecard
|`.github/workflows/type-check.yml`| 33 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8062 | PinnedDependenciesID |
Scorecard
|`.github/workflows/type-check.yml`| 32 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8056 | PinnedDependenciesID |
Scorecard
|`.github/workflows/security.yml`| 59 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8055 | PinnedDependenciesID | Scorecard
|`.github/workflows/security.yml`| 36 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8054 | PinnedDependenciesID | Scorecard
|`.github/workflows/security.yml`| 152 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8053 | PinnedDependenciesID | Scorecard
|`.github/workflows/security.yml`| 152 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8052 | PinnedDependenciesID | Scorecard
|`.github/workflows/security.yml`| 129 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8051 | PinnedDependenciesID | Scorecard
|`.github/workflows/sbom.yml`| 26 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8050 | PinnedDependenciesID | Scorecard
|`.github/workflows/sbom.yml`| 23 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8049 | PinnedDependenciesID | Scorecard
|`.github/workflows/sbom.yml`| 23 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8048 | PinnedDependenciesID | Scorecard
|`.github/workflows/release.yml`| 30 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8047 | PinnedDependenciesID | Scorecard
|`.github/workflows/release.yml`| 29 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8046 | PinnedDependenciesID | Scorecard
|`.github/workflows/release.yml`| 486 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8045 | PinnedDependenciesID | Scorecard
|`.github/workflows/release.yml`| 485 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8044 | PinnedDependenciesID | Scorecard
|`.github/workflows/performance.yml`| 29 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8043 | PinnedDependenciesID |
Scorecard
|`.github/workflows/mutation-testing.yml`| 19 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8042 | PinnedDependenciesID |
Scorecard
|`.github/workflows/mutation-testing.yml`| 18 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8041 | PinnedDependenciesID |
Scorecard
|`.github/workflows/mutation-testing.yml`| 17 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8040 | PinnedDependenciesID |
Scorecard
|`.github/workflows/markdown-lint.yml`| 32 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8039 | PinnedDependenciesID |
Scorecard
|`.github/workflows/markdown-lint.yml`| 31 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8038 | PinnedDependenciesID |
Scorecard
|`.github/workflows/manifest-validation.yml`| 192 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8037 | PinnedDependenciesID |
Scorecard
|`.github/workflows/manifest-validation.yml`| 44 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8035 | PinnedDependenciesID |
Scorecard
|`.github/workflows/lint.yml`| 100 | score is 4: npmCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8034 | PinnedDependenciesID | Scorecard
|`.github/workflows/lint.yml`| 27 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8033 | PinnedDependenciesID | Scorecard
|`.github/workflows/lint.yml`| 26 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8032 | PinnedDependenciesID | Scorecard
|`.github/workflows/lint.yml`| 25 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8031 | PinnedDependenciesID | Scorecard
|`.github/workflows/fuzzing.yml`| 27 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8030 | PinnedDependenciesID | Scorecard
|`.github/workflows/fuzzing.yml`| 26 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8029 | PinnedDependenciesID | Scorecard
|`.github/workflows/fuzzing.yml`| 25 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8028 | PinnedDependenciesID | Scorecard
|`.github/workflows/fuzz-testing.yml`| 18 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8027 | PinnedDependenciesID |
Scorecard
|`.github/workflows/fuzz-testing.yml`| 17 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8026 | PinnedDependenciesID |
Scorecard
|`.github/workflows/deploy.yml`| 28 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8025 | PinnedDependenciesID | Scorecard
|`.github/workflows/deploy.yml`| 27 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8024 | PinnedDependenciesID | Scorecard
|`.github/workflows/compliance.yml`| 23 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8023 | PinnedDependenciesID |
Scorecard
|`.github/workflows/compliance.yml`| 22 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8022 | PinnedDependenciesID |
Scorecard
|`.github/workflows/codeql.yml`| 47 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8021 | PinnedDependenciesID | Scorecard
|`.github/workflows/codeql.yml`| 46 | score is 4: pipCommand not pinned by hash Click Remediation
section below to solve this issue |\n| 8020 | PinnedDependenciesID | Scorecard
|`.github/workflows/chaos-testing.yml`| 18 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8019 | PinnedDependenciesID |
Scorecard
|`.github/workflows/chaos-testing.yml`| 17 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8018 | PinnedDependenciesID |
Scorecard
|`.github/workflows/blocklist-integration-tests.yml`| 210 | score is 4: pipCommand not pinned by
hash Click Remediation section below to solve this issue |\n| 8017 |
PinnedDependenciesID
|
Scorecard |`.github/workflows/blocklist-integration-tests.yml`| 209 | score is 4:
pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8016 |
PinnedDependenciesID
| Scorecard |`.github/workflows/blocklist-integration-tests.yml`| 57 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8015 |
PinnedDependenciesID
| Scorecard |`.github/workflows/blocklist-integration-tests.yml`| 56 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8012 |
PinnedDependenciesID
| Scorecard |`.github/workflows/architecture.yml`| 22 | score is 4: pipCommand not pinned by hash
Click Remediation section below to solve this issue |\n| 8011 |
PinnedDependenciesID |
Scorecard
|`.github/workflows/ansible-syntax-check.yml`| 34 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8010 | PinnedDependenciesID |
Scorecard
|`.github/workflows/ansible-syntax-check.yml`| 33 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8009 | PinnedDependenciesID |
Scorecard
|`.github/workflows/ansible-syntax-check.yml`| 32 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8008 | PinnedDependenciesID |
Scorecard
|`.github/workflows/ansible-inventory-validation.yml`| 241 | score is 4: pipCommand not pinned by
hash Click Remediation section below to solve this issue |\n| 8007 |
PinnedDependenciesID
|
Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 240 | score is 4:
pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8006 |
PinnedDependenciesID
| Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 203 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8005 |
PinnedDependenciesID
| Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 202 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8004 |
PinnedDependenciesID
| Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 34 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8003 |
PinnedDependenciesID
| Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 33 | score is 4: pipCommand not
pinned by hash Click Remediation section below to solve this issue |\n| 8002 |
PinnedDependenciesID
| Scorecard |`.github/workflows/_common.yml`| 36 | score is 4: pipCommand not pinned by hash Click
Remediation section below to solve this issue |\n| 8001 | PinnedDependenciesID |
Scorecard
|`.github/workflows/secret-scan.yml`| 62 | score is 4: GitHub-owned GitHubAction not pinned by hash
Remediation tip: update your workflow using
[https://app.stepsecurity.io]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pi]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?en]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?e]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/mai]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/ma]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/m]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.ym]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.y]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-sca]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-sc]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-s]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secre]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secr]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/sec]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/se]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/UndiFineD/]([https://app.stepsecurity.io/secureworkflow/UndiFineD]([https://app.stepsecurity.io/secureworkflow/UndiFine]([https://app.stepsecurity.io/secureworkflow/UndiFin](https://app.stepsecurity.io/secureworkflow/UndiFin)e)D)/)D)e)b)V)i)s)o)r)/)s)e)c)r)e)t)-)s)c)a)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)i)n)
Click Remediation section below for further remediation help |\n| 8000 |
TokenPermissionsID |
Scorecard |`.github/workflows/vex-generate.yml`| 1 | score is 0: no topLevel permission
defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-genera]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-gener]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-gene]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-gen]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-ge]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ve]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)v)e)x)-)g)e)n)e)r)a)t)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7999
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-syntax.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-synta]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-synt]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syn]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-sy]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/)v)a)l)i)d)a)t)e)-)s)y)n)t)a)x).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7998
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-kustomize.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomiz]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustom]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kusto]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kust]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kus]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-ku]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-k]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val)i)d)a)t)e)-)k)u)s)t)o)m)i)z)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7997
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-grafana.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafan]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafa]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-graf]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-gra]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-gr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v)a)l)i)d)a)t)e)-)g)r)a)f)a)n)a).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7996
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-fixtures.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixture]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtur]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixt]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fix]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-f]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/va](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/va)l)i)d)a)t)e)-)f)i)x)t)u)r)e)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7995
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-dashboards.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboard]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboa]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashbo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dash]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-das]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-da]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-d]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali)d)a)t)e)-)d)a)s)h)b)o)a)r)d)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7994
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-configs.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-config]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-confi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-conf]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-con]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/v)a)l)i)d)a)t)e)-)c)o)n)f)i)g)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7993
|
TokenPermissionsID
| Scorecard |`.github/workflows/validate-blocklists.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklist]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blockli]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blockl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-block]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-bloc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-bl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-b]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vali)d)a)t)e)-)b)l)o)c)k)l)i)s)t)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7992
|
TokenPermissionsID
| Scorecard |`.github/workflows/type-check.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-chec]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-che]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-ch]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/typ]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ty]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV)i)s)o)r)/)t)y)p)e)-)c)h)e)c)k).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7991
|
TokenPermissionsID
| Scorecard |`.github/workflows/test.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFine](https://app.stepsecurity.io/secureworkflow/github.com/UndiFine)D)/)D)e)b)V)i)s)o)r)/)t)e)s)t).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7990
|
TokenPermissionsID
| Scorecard |`.github/workflows/test-profile-summary.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summa]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summ]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-sum]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-su]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profil]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-prof]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-pro]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-pr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-)p)r)o)f)i)l)e)-)s)u)m)m)a)r)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7989
|
TokenPermissionsID
| Scorecard |`.github/workflows/test-grafana.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafan]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafa]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-graf]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-gra]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-gr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)t)e)s)t)-)g)r)a)f)a)n)a).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7988
|
TokenPermissionsID
| Scorecard |`.github/workflows/slsa-verify.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verif]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-veri]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-ver]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-ve]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sls]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi)s)o)r)/)s)l)s)a)-)v)e)r)i)f)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7987
|
TokenPermissionsID
| Scorecard |`.github/workflows/security.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/securit]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/securi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secur]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sec]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/se]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De)b)V)i)s)o)r)/)s)e)c)u)r)i)t)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7986
|
TokenPermissionsID
| Scorecard |`.github/workflows/secret-scan.yml`| 20 | score is 0: topLevel 'security-events'
permission set to 'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-sca]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-sc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secre]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sec]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/se]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi)s)o)r)/)s)e)c)r)e)t)-)s)c)a)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7985
|
TokenPermissionsID
| Scorecard |`.github/workflows/sbom.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFine](https://app.stepsecurity.io/secureworkflow/github.com/UndiFine)D)/)D)e)b)V)i)s)o)r)/)s)b)o)m).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7984
|
TokenPermissionsID
| Scorecard |`.github/workflows/sbom-policy.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-polic]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-poli]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-pol]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-po]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi)s)o)r)/)s)b)o)m)-)p)o)l)i)c)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7983
|
TokenPermissionsID
| Scorecard |`.github/workflows/runner-smoke.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smok]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-sm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runne]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runn]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/run]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ru]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/r]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)r)u)n)n)e)r)-)s)m)o)k)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7982
|
TokenPermissionsID
| Scorecard |`.github/workflows/release.yml`| 11 | score is 0: topLevel 'packages' permission set to
'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/releas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/relea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rele]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rel]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/re]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/r]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D)e)b)V)i)s)o)r)/)r)e)l)e)a)s)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7981
|
TokenPermissionsID
| Scorecard |`.github/workflows/release.yml`| 10 | score is 0: topLevel 'contents' permission set to
'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/releas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/relea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rele]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rel]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/re]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/r]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D)e)b)V)i)s)o)r)/)r)e)l)e)a)s)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7980
|
TokenPermissionsID
| Scorecard |`.github/workflows/release-please.yml`| 12 | score is 0: topLevel 'actions' permission
set to 'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-pleas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-plea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-ple]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-pl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/releas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/relea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rele]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rel]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/re]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/r]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor)/)r)e)l)e)a)s)e)-)p)l)e)a)s)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7979
|
TokenPermissionsID
| Scorecard |`.github/workflows/release-please.yml`| 10 | score is 0: topLevel 'contents' permission
set to 'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-pleas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-plea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-ple]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-pl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/releas]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/relea]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rele]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/rel]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/re]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/r]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor)/)r)e)l)e)a)s)e)-)p)l)e)a)s)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7978
|
TokenPermissionsID
| Scorecard |`.github/workflows/push-generator.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generato]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-genera]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-gener]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-gene]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-gen]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-ge]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/pus]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/pu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor)/)p)u)s)h)-)g)e)n)e)r)a)t)o)r).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7977
|
TokenPermissionsID
| Scorecard |`.github/workflows/notifications.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notification]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notificatio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notificati]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notificat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifica]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notific]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notif]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/noti]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/not]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/no]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/n]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso)r)/)n)o)t)i)f)i)c)a)t)i)o)n)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7976
|
TokenPermissionsID
| Scorecard |`.github/workflows/mutation-testing.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutatio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutati]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/muta]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mut]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/m](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/m)u)t)a)t)i)o)n)-)t)e)s)t)i)n)g).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7975
|
TokenPermissionsID
| Scorecard |`.github/workflows/merge-guard.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-gua]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-gu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merg]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mer]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/me]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi)s)o)r)/)m)e)r)g)e)-)g)u)a)r)d).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7974
|
TokenPermissionsID
| Scorecard |`.github/workflows/markdownlint.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownli]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markd]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mark]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)m)a)r)k)d)o)w)n)l)i)n)t).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7973
|
TokenPermissionsID
| Scorecard |`.github/workflows/markdown-lint.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-li]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-l]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markd]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mark]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso)r)/)m)a)r)k)d)o)w)n)-)l)i)n)t).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7972
|
TokenPermissionsID
| Scorecard |`.github/workflows/manifest-validation.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validatio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validati]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manife]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manif]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mani](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mani)f)e)s)t)-)v)a)l)i)d)a)t)i)o)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7971
|
TokenPermissionsID
| Scorecard |`.github/workflows/lint.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/li]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/l]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFine](https://app.stepsecurity.io/secureworkflow/github.com/UndiFine)D)/)D)e)b)V)i)s)o)r)/)l)i)n)t).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7970
|
TokenPermissionsID
| Scorecard |`.github/workflows/labeler.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labele]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/label]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/la]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/l]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D)e)b)V)i)s)o)r)/)l)a)b)e)l)e)r).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7969
|
TokenPermissionsID
| Scorecard |`.github/workflows/fuzz-testing.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuz]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/f]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)f)u)z)z)-)t)e)s)t)i)n)g).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7968
|
TokenPermissionsID
| Scorecard |`.github/workflows/firstboot-smoke-test.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smok]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-sm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstbo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/first](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/first)b)o)o)t)-)s)m)o)k)e)-)t)e)s)t).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7967
|
TokenPermissionsID
| Scorecard |`.github/workflows/doc-integrity.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrit]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integri]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integ]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-inte]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-int]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-in]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-i]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/do]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/d]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso)r)/)d)o)c)-)i)n)t)e)g)r)i)t)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7966
|
TokenPermissionsID
| Scorecard |`.github/workflows/deploy.yml`| 13 | score is 0: topLevel 'contents' permission set to
'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deplo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/depl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/dep]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/de]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/d]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/)D)e)b)V)i)s)o)r)/)d)e)p)l)o)y).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7965
|
TokenPermissionsID
| Scorecard |`.github/workflows/conventional-commits.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commit]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-comm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-com]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventiona]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/convention]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/convent]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conven]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conve](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conve)n)t)i)o)n)a)l)-)c)o)m)m)i)t)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7964
|
TokenPermissionsID
| Scorecard |`.github/workflows/container-scan.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-sca]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-sc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/containe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/contain]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/contai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conta]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/cont]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/con]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor)/)c)o)n)t)a)i)n)e)r)-)s)c)a)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7963
|
TokenPermissionsID
| Scorecard |`.github/workflows/compliance.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/complianc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/complian]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/complia]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compli]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/comp]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/com]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV)i)s)o)r)/)c)o)m)p)l)i)a)n)c)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7962
|
TokenPermissionsID
| Scorecard |`.github/workflows/codeql.yml`| 20 | score is 0: topLevel 'security-events' permission
set to 'write' Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeq]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/code]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/cod]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/)D)e)b)V)i)s)o)r)/)c)o)d)e)q)l).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7961
|
TokenPermissionsID
| Scorecard |`.github/workflows/chaos-testing.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testin]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chao]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/cha]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ch]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso)r)/)c)h)a)o)s)-)t)e)s)t)i)n)g).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7960
|
TokenPermissionsID
| Scorecard |`.github/workflows/build-generator.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generato]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-genera]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-gener]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-gene]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-gen]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-ge]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-g]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/buil]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/bui]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/bu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/b]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/)b)u)i)l)d)-)g)e)n)e)r)a)t)o)r).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7959
|
TokenPermissionsID
| Scorecard |`.github/workflows/blocklist-validate.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blockli]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blockl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/block]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/bloc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blo](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blo)c)k)l)i)s)t)-)v)a)l)i)d)a)t)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7958
|
TokenPermissionsID
| Scorecard |`.github/workflows/blocklist-integration-tests.yml`| 1 | score is 0: no topLevel
permission defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-test]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tes]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-te]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-t]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integratio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integrati]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integrat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integra]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integr]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integ]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-inte]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-int]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-in](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-in)t)e)g)r)a)t)i)o)n)-)t)e)s)t)s).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7957
|
TokenPermissionsID
| Scorecard |`.github/workflows/architecture.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architectur]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architectu]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architect]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architec]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/archite]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/archit]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/archi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/arch]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/arc]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ar]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/a]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis)o)r)/)a)r)c)h)i)t)e)c)t)u)r)e).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7956
|
TokenPermissionsID
| Scorecard |`.github/workflows/ansible-syntax-check.yml`| 1 | score is 0: no topLevel permission
defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-chec]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-che]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-ch]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-synta]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-synt]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syn]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-sy]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-s]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansibl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansib](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansib)l)e)-)s)y)n)t)a)x)-)c)h)e)c)k).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7955
|
TokenPermissionsID
| Scorecard |`.github/workflows/ansible-inventory-validation.yml`| 1 | score is 0: no topLevel
permission defined Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validatio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validati]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validat]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-valida]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-valid]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-vali]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-val]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-va]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-v]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-invento]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-invent]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inven](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inven)t)o)r)y)-)v)a)l)i)d)a)t)i)o)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7954
|
TokenPermissionsID
| Scorecard |`.github/workflows/_common.yml`| 1 | score is 0: no topLevel permission defined
Remediation tip: Visit
[https://app.stepsecurity.io/secureworkflow]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permission]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permissio]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permissi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permiss]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=perm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=per]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=pe]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=p]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enabl]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enab]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?ena]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?en]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?e]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/mai]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/ma]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/m]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.ym]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.y]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_commo]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_comm]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_com]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/*co]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/*c]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/*]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebViso]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVis]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVi]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebV]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/Deb]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/De]([https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/D)e)b)V)i)s)o)r)/)*)c)o)m)m)o)n).)y)m)l)/)m)a)i)n)?)e)n)a)b)l)e)=)p)e)r)m)i)s)s)i)o)n)s).
Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If
you want to
resolve
multiple issues at once, you can visit
[https://app.stepsecurity.io/securerepo]([https://app.stepsecurity.io/securerep]([https://app.stepsecurity.io/securere]([https://app.stepsecurity.io/securer]([https://app.stepsecurity.io/secure]([https://app.stepsecurity.io/secur]([https://app.stepsecurity.io/secu]([https://app.stepsecurity.io/sec]([https://app.stepsecurity.io/se]([https://app.stepsecurity.io/s]([https://app.stepsecurity.io/]([https://app.stepsecurity.io]([https://app.stepsecurity.i]([https://app.stepsecurity.]([https://app.stepsecurity]([https://app.stepsecurit]([https://app.stepsecuri]([https://app.stepsecur]([https://app.stepsecu]([https://app.stepsec]([https://app.stepse]([https://app.steps]([https://app.step]([https://app.ste]([https://app.st]([https://app.s]([https://app.]([https://app]([https://ap]([https://a](https://a)p)p).)s)t)e)p)s)e)c)u)r)i)t)y).)i)o)/)s)e)c)u)r)e)r)e)p)o)
instead. Click Remediation section below for further remediation help |\n| 7953
|
py/stack-trace-exposure | CodeQL |`opt/web/dashboard/app.py`| 234 | Stack trace
information flows to
this location and may be exposed to an external user. |\n| 7951 |
py/stack-trace-exposure
| CodeQL
|`opt/web/dashboard/app.py`| 192 | Stack trace information flows to this location and may be exposed
to an external user. |\n| 7950 | py/stack-trace-exposure | CodeQL
|`opt/web/dashboard/app.py`| 169 |
Stack trace information flows to this location and may be exposed to an external
user.
|\n| 7949 |
py/stack-trace-exposure | CodeQL |`opt/web/dashboard/app.py`| 142 | Stack trace
information flows to
this location and may be exposed to an external user. |\n| 7948 |
py/clear-text-logging-sensitive-data | CodeQL |`opt/services/compliance/core.py`| 308 |
This
expression logs sensitive data (password) as clear text. |\n| 7947 |
py/clear-text-logging-sensitive-data | CodeQL |`opt/services/compliance/core.py`| 259 |
This
expression logs sensitive data (password) as clear text. |\n| 7946 | E305 |
flake8
|`scripts/fix_all_errors.py`| 3639 | expected 2 blank lines after class or function definition,
found 1 |\n| 7941 | E302 | flake8 |`scripts/fix_all_errors.py`| 853 | expected 2 blank
lines, found
1 |\n| 7926 | E302 | flake8 |`scripts/fix_all_errors.py`| 174 | expected 2 blank lines,
found 1 |\n|
7925 | E261 | flake8 |`scripts/fix_all_errors.py`| 167 | at least two spaces before inline
comment
|\n| 7923 | E261 | flake8 |`scripts/fix_all_errors.py`| 158 | at least two spaces before inline
comment |\n| 7918 | F841 | flake8 |`scripts/fix_all_errors.py`| 144 | local variable
'original_content' is assigned to but never used |\n| 7917 | E261 | flake8
|`scripts/fix_all_errors.py`| 142 | at least two spaces before inline comment |\n| 7915 | E302 |
flake8 |`scripts/fix_all_errors.py`| 119 | expected 2 blank lines, found 1 |\n| 7914 |
E302 | flake8
|`scripts/fix_all_errors.py`| 108 | expected 2 blank lines, found 1 |\n| 7913 | E302 | flake8
|`scripts/fix_all_errors.py`| 92 | expected 2 blank lines, found 1 |\n| 7912 | E302 | flake8
|`scripts/fix_all_errors.py`| 84 | expected 2 blank lines, found 1 |\n| 7907 | F401 | flake8
|`scripts/fix_all_errors.py`| 44 | 'dataclasses.asdict' imported but unused |\n| 7905 |
BinaryArtifactsID | Scorecard |`tools/shellcheck.exe`| 1 | score is 9: binary detected
Click
Remediation section below to solve this issue |\n| 7904 | E302 | flake8
|`tests/test_ssh_hardening.py`| 4 | expected 2 blank lines, found 1 |\n| 7900 | E116 | flake8
|`tests/test_migrations.py`| 6 | unexpected indentation (comment) |\n| 7899 | E116 | flake8
|`tests/test_migrations.py`| 4 | unexpected indentation (comment) |\n| 7898 | E302 | flake8
|`tests/test_marketplace_governance.py`| 9 | expected 2 blank lines, found 1 |\n| 7875 | F821 |
flake8 |`tests/test_backup_manager_encryption.py`| 40 | undefined name 'AESGCM' |\n| 7872
| E302 |
flake8 |`tests/test_audit_chain.py`| 12 | expected 2 blank lines, found 1 |\n| 7871 | E116
| flake8
|`tests/test_audit_chain.py`| 10 | unexpected indentation (comment) |\n| 7870 | E116 | flake8
|`tests/test_audit_chain.py`| 9 | unexpected indentation (comment) |\n| 7869 | E116 | flake8
|`tests/test_audit_chain.py`| 8 | unexpected indentation (comment) |\n| 7843 | E116 | flake8
|`opt/services/multiregion/replication_scheduler.py`| 85 | unexpected indentation (comment) |\n|
7839 | E116 | flake8 |`opt/services/migration/advanced_migration.py`| 82 | unexpected
indentation
(comment) |\n| 7838 | E116 | flake8 |`opt/services/marketplace/marketplace_service.py`| 90
|
unexpected indentation (comment) |\n| 7837 | E116 | flake8
|`opt/services/marketplace/marketplace_service.py`| 89 | unexpected indentation (comment) |\n| 7829
| E116 | flake8 |`opt/services/cluster/large_cluster_optimizer.py`| 80 | unexpected indentation
(comment) |\n| 7828 | E116 | flake8 |`opt/services/cluster/large_cluster_optimizer.py`| 79
|
unexpected indentation (comment) |\n| 7795 | F821 | flake8 |`opt/services/cache.py`| 109 |
undefined
name 'logging' |\n| 7791 | E116 | flake8 |`opt/services/billing/billing_integration.py`|
88 |
unexpected indentation (comment) |\n| 7790 | E116 | flake8
|`opt/services/backup/dedup_backup_service.py`| 85 | unexpected indentation (comment) |\n| 7789 |
E116 | flake8 |`opt/services/backup/dedup_backup_service.py`| 81 | unexpected indentation
(comment)
|\n| 7787 | E116 | flake8 |`opt/dvctl.py`| 22 | unexpected indentation (comment) |\n| 7786 | E116 |
flake8 |`opt/dvctl.py`| 21 | unexpected indentation (comment) |\n| 7785 | E116 | flake8
|`opt/dvctl.py`| 20 | unexpected indentation (comment) |\n| 7782 | E402 | flake8
|`tests/test_integration_suite.py`| 32 | module level import not at top of file |\n| 7781 | E402 |
flake8 |`tests/test_integration_suite.py`| 26 | module level import not at top of file
|\n| 7780 |
E402 | flake8 |`tests/test_integration_suite.py`| 25 | module level import not at top of
file |\n|
7766 | E302 | flake8 |`tests/test_cost_optimization.py`| 10 | expected 2 blank lines,
found 1 |\n|
7746 | E301 | flake8 |`opt/webhook_system.py`| 390 | expected 1 blank line, found 0 |\n|
7745 | E302
| flake8 |`opt/web/dashboard/app.py`| 79 | expected 2 blank lines, found 1 |\n| 7744 | E301 | flake8
|`opt/testing/test_e2e_comprehensive.py`| 132 | expected 1 blank line, found 0 |\n| 7742 | E302 |
flake8 |`opt/services/sdn/sdn_controller.py`| 167 | expected 2 blank lines, found 1 |\n|
7280 |
py/stack-trace-exposure | CodeQL |`opt/services/anomaly/api.py`| 878 | Stack trace
information flows
to this location and may be exposed to an external user. |\n| 7279 |
py/stack-trace-exposure |
CodeQL |`opt/services/anomaly/api.py`| 866 | Stack trace information flows to this
location and may
be exposed to an external user. |\n| 7278 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 845 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7277 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 817 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7276 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 801 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7275 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 657 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7274 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 657 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7273 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 596 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7272 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 596 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7271 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 629 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7270 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 624 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 7269 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 585 | Stack trace information flows to this location and may be
exposed to an external user. Stack trace information flows to this location and
may be
exposed to an
external user. |\n| 7268 | py/stack-trace-exposure | CodeQL
|`opt/services/compliance/api.py`| 119 |
Stack trace information flows to this location and may be exposed to an external
user.
|\n| 7267 |
py/stack-trace-exposure | CodeQL |`opt/services/compliance/api.py`| 117 | Stack trace
information
flows to this location and may be exposed to an external user. |\n| 7266 |
py/reflective-xss |
CodeQL |`opt/services/anomaly/api.py`| 866 | Cross-site scripting vulnerability due to a
user-provided value. |\n| 7265 | py/reflective-xss | CodeQL
|`opt/services/anomaly/api.py`| 845 |
Cross-site scripting vulnerability due to a user-provided value. |\n| 7264 |
py/reflective-xss |
CodeQL |`opt/services/anomaly/api.py`| 817 | Cross-site scripting vulnerability due to a
user-provided value. |\n| 7263 | py/reflective-xss | CodeQL
|`opt/services/anomaly/api.py`| 801 |
Cross-site scripting vulnerability due to a user-provided value. |\n| 7262 |
py/reflective-xss |
CodeQL |`opt/services/scheduler/api.py`| 624 | Cross-site scripting vulnerability due to a
user-provided value. |\n| 7261 | py/incomplete-url-substring-sanitization | CodeQL
|`tests/test_acme_certificates.py`| 59 | The string example.com may be at an arbitrary position in
the sanitized URL. |\n| 7141 | py/weak-sensitive-data-hashing | CodeQL
|`opt/services/api_key_rotation.py`| 317 | Sensitive data (password) is used in a hashing algorithm
(SHA256) that is insecure for password hashing, since it is not a
computationally
expensive hash
function. Sensitive data (password) is used in a hashing algorithm (SHA256) that
is
insecure for
password hashing, since it is not a computationally expensive hash function.
Sensitive
data
(password) is used in a hashing algorithm (SHA256) that is insecure for password
hashing,
since it
is not a computationally expensive hash function. |\n| 7128 |
py/clear-text-logging-sensitive-data |
CodeQL |`opt/services/secrets/vault_manager.py`| 712 | This expression logs sensitive data
(secret)
as clear text. This expression logs sensitive data (secret) as clear text. |\n|
7127 |
py/clear-text-logging-sensitive-data | CodeQL |`opt/services/secrets_management.py`| 691 |
This
expression logs sensitive data (password) as clear text. |\n| 7077 |
py/url-redirection |
CodeQL
|`opt/web/panel/app.py`| 552 | Untrusted URL redirection depends on a user-provided value. |\n| 7076
| SecurityPolicyID | Scorecard |`no file associated with this alert`| 1 | score is 4: security
policy file detected: Warn: no linked content found Click Remediation section
below to
solve this
issue |\n| 6925 | py/url-redirection | CodeQL |`opt/web/panel/routes/auth.py`| 193 |
Untrusted URL
redirection depends on a user-provided value. |\n| 6801 | E302 | flake8
|`tests/test_backup_manager_encryption.py`| 22 | expected 2 blank lines, found 1 |\n| 6350 | SASTID
| Scorecard |`no file associated with this alert`| 1 | score is 7: SAST tool detected but not run on
all commits: Warn: 0 commits out of 9 are checked with a SAST tool Click
Remediation
section below
to solve this issue |\n| 6199 | VulnerabilitiesID | Scorecard |`no file associated with
this alert`|
1 | score is 0: 10 existing vulnerabilities detected: Warn: Project is
vulnerable to:
PYSEC-2024-48
/ GHSA-fj7x-q9j7-g6q6 Warn: Project is vulnerable to: GHSA-mr82-8j83-vxmv Warn:
Project is
vulnerable to: GHSA-4grg-w6v8-c28g Warn: Project is vulnerable to:
GHSA-43qf-4rqw-9q2g
Warn: Project
is vulnerable to: GHSA-7rxf-gvfg-47g4 Warn: Project is vulnerable to:
GHSA-84pr-m4jr-85g5
Warn:
Project is vulnerable to: GHSA-8vgw-p6qm-5gr7 Warn: Project is vulnerable to:
PYSEC-2024-71 /
GHSA-hxwh-jpp2-84pm Warn: Project is vulnerable to: GHSA-hc5x-x2vx-497g Warn:
Project is
vulnerable
to: GHSA-w3h3-4rj7-4ph4 Click Remediation section below to solve this issue |\n|
6198 |
MaintainedID
| Scorecard |`no file associated with this alert`| 1 | score is 0: project was created within the
last 90 days. Please review its contents carefully: Warn: Repository was created
within
the last 90
days. Click Remediation section below to solve this issue |\n| 6196 |
CodeReviewID |
Scorecard |`no
file associated with this alert`| 1 | score is 0: Found 0/21 approved changesets -- score
normalized
to 0 Click Remediation section below to solve this issue |\n| 6195 |
CIIBestPracticesID |
Scorecard
|`no file associated with this alert`| 1 | score is 0: no effort to earn an OpenSSF best practices
badge detected Click Remediation section below to solve this issue |\n| 6082 |
PinnedDependenciesID
| Scorecard |`opt/monitoring/fixtures/generator/Dockerfile`| 12 | score is 4: pipCommand not pinned
by hash Click Remediation section below to solve this issue |\n| 6081 |
PinnedDependenciesID |
Scorecard |`opt/monitoring/fixtures/generator/Dockerfile`| 2 | score is 4: containerImage
not pinned
by hash Remediation tip: pin your Docker image by updating python:3.11-slim to
python:3.11-slim@sha256:7cd0079a9bd8800c81632d65251048fc2848bf9afda542224b1b10e0cae45575
Click
Remediation section below for further remediation help |\n| 5770 |
BranchProtectionID |
Scorecard
|`no file associated with this alert`| 1 | score is 3: branch protection is not maximal on
development and all release branches: Warn: could not determine whether
codeowners review
is allowed
Warn: no status checks found to merge onto branch 'main' Warn: PRs are not
required to
make changes
on branch 'main'; or we don't have data to detect it.If you think it might be
the latter,
make sure
to run Scorecard with a PAT or use Repo Rules (that are always public) instead
of Branch
Protection
settings Click Remediation section below to solve this issue |\n| 83 |
py/stack-trace-exposure |
CodeQL |`opt/services/multiregion/api.py`| 651 | Stack trace information flows to this
location and
may be exposed to an external user. |\n| 82 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 651 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 81 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 645 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 80 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 645 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 79 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 638 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 78 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 638 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 77 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 632 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 76 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 632 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 75 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 627 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 74 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 627 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 73 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 622 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 72 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 622 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 71 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 616 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 70 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 616 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 69 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 611 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 68 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 611 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 67 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 606 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 66 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 606 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 65 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 601 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 64 | py/stack-trace-exposure | CodeQL
|`opt/services/multiregion/api.py`| 601 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 60 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 870 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 58 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 858 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 57 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 853 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 56 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 849 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 54 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 837 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 53 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 833 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 52 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 825 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 51 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 821 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 49 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 809 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 48 | py/stack-trace-exposure | CodeQL
|`opt/services/anomaly/api.py`| 805 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 44 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 619 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 43 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 612 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 42 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 607 | Stack trace information flows to this location and may be
exposed to an external user. |\n| 41 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 602 | Stack trace information flows to this location and may be
exposed to an external user. Stack trace information flows to this location and
may be
exposed to an
external user. |\n| 40 | py/stack-trace-exposure | CodeQL
|`opt/services/scheduler/api.py`| 597 |
Stack trace information flows to this location and may be exposed to an external
user.
|\n| 39 |
py/stack-trace-exposure | CodeQL |`opt/services/scheduler/api.py`| 592 | Stack trace
information
flows to this location and may be exposed to an external user. |\n| 37 |
py/weak-sensitive-data-hashing | CodeQL |`opt/services/rpc/auth.py`| 658 | Sensitive data
(password)
is used in a hashing algorithm (SHA256) that is insecure for password hashing,
since it is
not a
computationally expensive hash function. |\n| 34 |
py/weak-sensitive-data-hashing | CodeQL
|`opt/services/api_key_manager.py`| 222 | Sensitive data (password) is used in a hashing algorithm
(SHA256) that is insecure for password hashing, since it is not a
computationally
expensive hash
function. Sensitive data (password) is used in a hashing algorithm (SHA256) that
is
insecure for
password hashing, since it is not a computationally expensive hash function.
Sensitive
data
(password) is used in a hashing algorithm (SHA256) that is insecure for password
hashing,
since it
is not a computationally expensive hash function. Sensitive data (password) is
used in a
hashing
algorithm (SHA256) that is insecure for password hashing, since it is not a
computationally
expensive hash function. |\n| 32 | py/reflective-xss | CodeQL
|`opt/services/multiregion/api.py`|
632 | Cross-site scripting vulnerability due to a user-provided value. |\n| 31 |
py/reflective-xss |
CodeQL |`opt/services/multiregion/api.py`| 616 | Cross-site scripting vulnerability due to
a
user-provided value. |\n| 30 | py/reflective-xss | CodeQL
|`opt/services/multiregion/api.py`| 611 |
Cross-site scripting vulnerability due to a user-provided value. |\n| 29 |
py/reflective-xss |
CodeQL |`opt/services/multiregion/api.py`| 606 | Cross-site scripting vulnerability due to
a
user-provided value. |\n| 27 | py/reflective-xss | CodeQL |`opt/services/anomaly/api.py`|
858 |
Cross-site scripting vulnerability due to a user-provided value. Cross-site
scripting
vulnerability
due to a user-provided value. |\n| 26 | py/reflective-xss | CodeQL
|`opt/services/anomaly/api.py`|
853 | Cross-site scripting vulnerability due to a user-provided value. |\n| 24 |
py/reflective-xss |
CodeQL |`opt/services/anomaly/api.py`| 833 | Cross-site scripting vulnerability due to a
user-provided value. |\n| 23 | py/reflective-xss | CodeQL |`opt/services/anomaly/api.py`|
825 |
Cross-site scripting vulnerability due to a user-provided value. Cross-site
scripting
vulnerability
due to a user-provided value. |\n| 21 | py/reflective-xss | CodeQL
|`opt/services/anomaly/api.py`|
809 | Cross-site scripting vulnerability due to a user-provided value.
Cross-site
scripting
vulnerability due to a user-provided value. |\n| 18 | py/reflective-xss | CodeQL
|`opt/services/scheduler/api.py`| 619 | Cross-site scripting vulnerability due to a user-provided
value. |\n| 17 | py/reflective-xss | CodeQL |`opt/services/scheduler/api.py`| 612 |
Cross-site
scripting vulnerability due to a user-provided value. |\n| 16 |
py/reflective-xss | CodeQL
|`opt/services/scheduler/api.py`| 607 | Cross-site scripting vulnerability due to a user-provided
value. |\n| 15 | py/reflective-xss | CodeQL |`opt/services/scheduler/api.py`| 602 |
Cross-site
scripting vulnerability due to a user-provided value. |\n| 14 |
py/reflective-xss | CodeQL
|`opt/services/scheduler/api.py`| 597 | Cross-site scripting vulnerability due to a user-provided
value. |\n| 11 | py/clear-text-storage-sensitive-data | CodeQL
|`opt/tools/first_boot_keygen.py`|
138 | This expression stores sensitive data (secret) as clear text. |\n| 10 |
py/clear-text-logging-sensitive-data | CodeQL |`opt/system/hypervisor/xen_driver.py`| 1048
| This
expression logs sensitive data (password) as clear text. |\n| 1 |
py/clear-text-logging-sensitive-data | CodeQL |`opt/services/api_key_manager.py` | 519 |
This
expression logs sensitive data (password) as clear text. This expression logs
sensitive
data
(password) as clear text. |\n
