<!-- markdownlint-disable-file -->

# Security Scan Report

**Total Alerts:** 8946
**Open:** 1117 | **Dismissed/Fixed:** 7829

Generated via GitHub CLI.

## 🔴 Critical Severity (0)

*No alerts found.*

## 🟠 High Severity (0)

*No alerts found.*

## 🟡 Medium Severity (0)

*No alerts found.*

## 🟢 Low Severity (0)

*No alerts found.*

## ⚪ Other (1117)

| ID | Rule | Tool | File | Line | Message |
|----|------|------|------|------|---------|
| 8946 | F821 | flake8 | `scripts/fix_all_errors.py` | 3635 | undefined name 'filtered_summary' |
| 8945 | F821 | flake8 | `scripts/fix_all_errors.py` | 3633 | undefined name 'filtered_issues' |
| 8944 | F821 | flake8 | `scripts/fix_all_errors.py` | 3632 | undefined name 'report_path' |
| 8943 | E303 | flake8 | `scripts/fix_all_errors.py` | 3631 | too many blank lines (2) |
| 8942 | E115 | flake8 | `scripts/fix_all_errors.py` | 3555 | expected an indented block (comment) |
| 8941 | E115 | flake8 | `scripts/fix_all_errors.py` | 3537 | expected an indented block (comment) |
| 8940 | E115 | flake8 | `scripts/fix_all_errors.py` | 3519 | expected an indented block (comment) |
| 8939 | E115 | flake8 | `scripts/fix_all_errors.py` | 3504 | expected an indented block (comment) |
| 8938 | E115 | flake8 | `scripts/fix_all_errors.py` | 3496 | expected an indented block (comment) |
| 8937 | E115 | flake8 | `scripts/fix_all_errors.py` | 3482 | expected an indented block (comment) |
| 8936 | E115 | flake8 | `scripts/fix_all_errors.py` | 3467 | expected an indented block (comment) |
| 8935 | E115 | flake8 | `scripts/fix_all_errors.py` | 3462 | expected an indented block (comment) |
| 8934 | E115 | flake8 | `scripts/fix_all_errors.py` | 3459 | expected an indented block (comment) |
| 8933 | E115 | flake8 | `scripts/fix_all_errors.py` | 3448 | expected an indented block (comment) |
| 8932 | E115 | flake8 | `scripts/fix_all_errors.py` | 3446 | expected an indented block (comment) |
| 8931 | E115 | flake8 | `scripts/fix_all_errors.py` | 3429 | expected an indented block (comment) |
| 8930 | E115 | flake8 | `scripts/fix_all_errors.py` | 3419 | expected an indented block (comment) |
| 8929 | E115 | flake8 | `scripts/fix_all_errors.py` | 3407 | expected an indented block (comment) |
| 8928 | E115 | flake8 | `scripts/fix_all_errors.py` | 3370 | expected an indented block (comment) |
| 8927 | E128 | flake8 | `scripts/fix_all_errors.py` | 3354 | continuation line under-indented for visual indent |
| 8926 | E302 | flake8 | `scripts/fix_all_errors.py` | 3329 | expected 2 blank lines, found 1 |
| 8925 | E128 | flake8 | `scripts/fix_all_errors.py` | 2755 | continuation line under-indented for visual indent |
| 8924 | E302 | flake8 | `scripts/passthrough_manager.py` | 16 | expected 2 blank lines, found 1 |
| 8923 | E115 | flake8 | `scripts/generate_notifications_report.py` | 80 | expected an indented block (comment) |
| 8922 | E128 | flake8 | `scripts/fix_all_errors.py` | 2756 | continuation line under-indented for visual indent |
| 8921 | PinnedDependenciesID | Scorecard | `.github/workflows/test.yml` | 40 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8916 | E115 | flake8 | `tests/test_ssh_hardening.py` | 22 | expected an indented block (comment) |
| 8915 | E115 | flake8 | `tests/test_slo_tracking.py` | 434 | expected an indented block (comment) |
| 8914 | F401 | flake8 | `tests/test_rpc_security.py` | 14 | 'unittest' imported but unused |
| 8913 | F401 | flake8 | `tests/test_property_based.py` | 16 | 'unittest' imported but unused |
| 8912 | F401 | flake8 | `tests/test_phase6_vnc.py` | 14 | 'unittest' imported but unused |
| 8911 | F401 | flake8 | `tests/test_phase6_vm.py` | 14 | 'unittest' imported but unused |
| 8910 | E115 | flake8 | `tests/test_phase6_dns.py` | 287 | expected an indented block (comment) |
| 8909 | E302 | flake8 | `tests/test_phase6_dns.py` | 17 | expected 2 blank lines, found 1 |
| 8908 | E115 | flake8 | `tests/test_phase6_cloudinit.py` | 333 | expected an indented block (comment) |
| 8907 | E115 | flake8 | `tests/test_passthrough.py` | 340 | expected an indented block (comment) |
| 8906 | E115 | flake8 | `tests/test_passthrough.py` | 143 | expected an indented block (comment) |
| 8905 | F811 | flake8 | `tests/test_passthrough.py` | 18 | redefinition of unused 'patch' from line 15 |
| 8904 | F401 | flake8 | `tests/test_passthrough.py` | 14 | 'unittest' imported but unused |
| 8903 | F401 | flake8 | `tests/test_network_backends.py` | 14 | 'unittest' imported but unused |
| 8902 | E115 | flake8 | `tests/test_netcfg_mock.py` | 420 | expected an indented block (comment) |
| 8901 | F401 | flake8 | `tests/test_monitoring.py` | 14 | 'unittest' imported but unused |
| 8900 | F401 | flake8 | `tests/test_mock_mode.py` | 6 | 'pytest' imported but unused |
| 8899 | F821 | flake8 | `tests/test_migrations.py` | 16 | undefined name 'Flask' |
| 8898 | E302 | flake8 | `tests/test_migrations.py` | 14 | expected 2 blank lines, found 0 |
| 8897 | F401 | flake8 | `tests/test_migrations.py` | 13 | 'datetime.datetime' imported but unused |
| 8896 | F401 | flake8 | `tests/test_migrations.py` | 12 | 'pytest' imported but unused |
| 8895 | F401 | flake8 | `tests/test_migrations.py` | 11 | 'unittest.mock.MagicMock' imported but unused |
| 8894 | F401 | flake8 | `tests/test_migrations.py` | 11 | 'unittest.mock.patch' imported but unused |
| 8893 | F821 | flake8 | `tests/test_marketplace_governance.py` | 64 | undefined name 'SecurityScanResult' |
| 8892 | F821 | flake8 | `tests/test_marketplace_governance.py` | 50 | undefined name 'SecurityScanResult' |
| 8891 | F821 | flake8 | `tests/test_marketplace_governance.py` | 29 | undefined name 'SecurityScanResult' |
| 8890 | E115 | flake8 | `tests/test_marketplace_governance.py` | 28 | expected an indented block (comment) |
| 8889 | E115 | flake8 | `tests/test_marketplace_governance.py` | 23 | expected an indented block (comment) |
| 8888 | F821 | flake8 | `tests/test_marketplace_governance.py` | 12 | undefined name 'Recipe' |
| 8887 | F821 | flake8 | `tests/test_marketplace_governance.py` | 11 | undefined name 'SecurityScanner' |
| 8886 | F401 | flake8 | `tests/test_marketplace_governance.py` | 7 | 'datetime.datetime' imported but unused |
| 8885 | F401 | flake8 | `tests/test_marketplace_governance.py` | 6 | 'pytest' imported but unused |
| 8884 | F401 | flake8 | `tests/test_marketplace_governance.py` | 5 | 'unittest.mock.MagicMock' imported but unused |
| 8883 | F401 | flake8 | `tests/test_marketplace_governance.py` | 5 | 'unittest.mock.patch' imported but unused |
| 8882 | F821 | flake8 | `tests/test_licensing.py` | 134 | undefined name 'ECDSAVerifier' |
| 8881 | F821 | flake8 | `tests/test_licensing.py` | 125 | undefined name 'HardwareFingerprint' |
| 8880 | F821 | flake8 | `tests/test_licensing.py` | 121 | undefined name 'MagicMock' |
| 8879 | F821 | flake8 | `tests/test_licensing.py` | 111 | undefined name 'HardwareFingerprint' |
| 8878 | F821 | flake8 | `tests/test_licensing.py` | 110 | undefined name 'mock_open' |
| 8877 | F821 | flake8 | `tests/test_licensing.py` | 94 | undefined name 'LicenseBundle' |
| 8876 | F821 | flake8 | `tests/test_licensing.py` | 82 | undefined name 'timezone' |
| 8875 | F821 | flake8 | `tests/test_licensing.py` | 79 | undefined name 'LicenseBundle' |
| 8874 | F821 | flake8 | `tests/test_licensing.py` | 76 | undefined name 'timezone' |
| 8873 | F821 | flake8 | `tests/test_licensing.py` | 75 | undefined name 'LicenseTier' |
| 8872 | F821 | flake8 | `tests/test_licensing.py` | 74 | undefined name 'LicenseFeatures' |
| 8871 | F821 | flake8 | `tests/test_licensing.py` | 67 | undefined name 'FeatureFlag' |
| 8870 | F821 | flake8 | `tests/test_licensing.py` | 66 | undefined name 'FeatureFlag' |
| 8869 | F821 | flake8 | `tests/test_licensing.py` | 60 | undefined name 'LicenseTier' |
| 8868 | F821 | flake8 | `tests/test_licensing.py` | 59 | undefined name 'LicenseFeatures' |
| 8867 | F821 | flake8 | `tests/test_licensing.py` | 55 | undefined name 'FeatureFlag' |
| 8866 | F821 | flake8 | `tests/test_licensing.py` | 54 | undefined name 'FeatureFlag' |
| 8865 | F821 | flake8 | `tests/test_licensing.py` | 53 | undefined name 'FeatureFlag' |
| 8864 | F821 | flake8 | `tests/test_licensing.py` | 50 | undefined name 'LicenseTier' |
| 8863 | F821 | flake8 | `tests/test_licensing.py` | 50 | undefined name 'LicenseFeatures' |
| 8862 | F821 | flake8 | `tests/test_licensing.py` | 45 | undefined name 'LicenseTier' |
| 8861 | F821 | flake8 | `tests/test_licensing.py` | 45 | undefined name 'LicenseFeatures' |
| 8860 | F821 | flake8 | `tests/test_licensing.py` | 40 | undefined name 'timedelta' |
| 8859 | F821 | flake8 | `tests/test_licensing.py` | 37 | undefined name 'LicenseTier' |
| 8858 | F821 | flake8 | `tests/test_licensing.py` | 36 | undefined name 'LicenseFeatures' |
| 8857 | F821 | flake8 | `tests/test_licensing.py` | 35 | undefined name 'timezone' |
| 8856 | F401 | flake8 | `tests/test_hvctl_xen.py` | 4 | 'unittest' imported but unused |
| 8855 | E115 | flake8 | `tests/test_feature_flags.py` | 54 | expected an indented block (comment) |
| 8854 | E115 | flake8 | `tests/test_feature_flags.py` | 48 | expected an indented block (comment) |
| 8853 | E115 | flake8 | `tests/test_feature_flags.py` | 42 | expected an indented block (comment) |
| 8852 | E115 | flake8 | `tests/test_feature_flags.py` | 35 | expected an indented block (comment) |
| 8851 | F811 | flake8 | `tests/test_feature_flags.py` | 11 | redefinition of unused 'patch' from line 8 |
| 8850 | F401 | flake8 | `tests/test_energy_telemetry.py` | 4 | 'unittest' imported but unused |
| 8849 | E128 | flake8 | `tests/test_dns_hosting.py` | 76 | continuation line under-indented for visual indent |
| 8848 | F811 | flake8 | `tests/test_diagnostics.py` | 15 | redefinition of unused 'patch' from line 13 |
| 8847 | F401 | flake8 | `tests/test_dashboard.py` | 1 | 'unittest' imported but unused |
| 8846 | F401 | flake8 | `tests/test_cost_optimization.py` | 1 | 'unittest' imported but unused |
| 8845 | E115 | flake8 | `tests/test_compliance_reporting.py` | 52 | expected an indented block (comment) |
| 8844 | E115 | flake8 | `tests/test_compliance_reporting.py` | 19 | expected an indented block (comment) |
| 8843 | E302 | flake8 | `tests/test_compliance_reporting.py` | 11 | expected 2 blank lines, found 0 |
| 8842 | F401 | flake8 | `tests/test_compliance_reporting.py` | 10 | 'datetime.datetime' imported but unused |
| 8841 | F401 | flake8 | `tests/test_compliance_reporting.py` | 9 | 'pytest' imported but unused |
| 8840 | F811 | flake8 | `tests/test_compliance_reporting.py` | 8 | redefinition of unused 'MagicMock' from line 3 |
| 8839 | F811 | flake8 | `tests/test_compliance_reporting.py` | 8 | redefinition of unused 'patch' from line 3 |
| 8838 | F811 | flake8 | `tests/test_compliance_reporting.py` | 3 | redefinition of unused 'patch' from line 1 |
| 8837 | F811 | flake8 | `tests/test_compliance_remediation.py` | 7 | redefinition of unused 'patch' from line 5 |
| 8836 | F401 | flake8 | `tests/test_compliance_remediation.py` | 4 | 'unittest' imported but unused |
| 8835 | F401 | flake8 | `tests/test_compliance.py` | 1 | 'unittest' imported but unused |
| 8834 | F811 | flake8 | `tests/test_cli_wrappers.py` | 15 | redefinition of unused 'patch' from line 3 |
| 8833 | E115 | flake8 | `tests/test_chaos_engineering.py` | 712 | expected an indented block (comment) |
| 8832 | E115 | flake8 | `tests/test_chaos_engineering.py` | 561 | expected an indented block (comment) |
| 8831 | E115 | flake8 | `tests/test_chaos_engineering.py` | 535 | expected an indented block (comment) |
| 8830 | E115 | flake8 | `tests/test_chaos_engineering.py` | 501 | expected an indented block (comment) |
| 8829 | E115 | flake8 | `tests/test_chaos_engineering.py` | 340 | expected an indented block (comment) |
| 8828 | F401 | flake8 | `tests/test_chaos_engineering.py` | 3 | 'unittest' imported but unused |
| 8827 | F401 | flake8 | `tests/test_backup_service.py` | 15 | 'unittest' imported but unused |
| 8826 | E302 | flake8 | `tests/test_backup_manager_encryption.py` | 17 | expected 2 blank lines, found 1 |
| 8825 | F401 | flake8 | `tests/test_backup_manager_encryption.py` | 2 | 'unittest.mock.patch' imported but unused |
| 8824 | F401 | flake8 | `tests/test_backup_manager_encryption.py` | 1 | 'unittest' imported but unused |
| 8823 | F811 | flake8 | `tests/test_audit_encryption.py` | 15 | redefinition of unused 'patch' from line 12 |
| 8822 | F821 | flake8 | `tests/test_audit_chain.py` | 69 | undefined name 'db' |
| 8821 | E115 | flake8 | `tests/test_audit_chain.py` | 63 | expected an indented block (comment) |
| 8820 | F821 | flake8 | `tests/test_audit_chain.py` | 55 | undefined name 'db' |
| 8819 | E115 | flake8 | `tests/test_audit_chain.py` | 31 | expected an indented block (comment) |
| 8818 | F821 | flake8 | `tests/test_audit_chain.py` | 27 | undefined name 'db' |
| 8817 | F821 | flake8 | `tests/test_audit_chain.py` | 26 | undefined name 'db' |
| 8816 | F821 | flake8 | `tests/test_audit_chain.py` | 23 | undefined name 'db' |
| 8815 | F821 | flake8 | `tests/test_audit_chain.py` | 20 | undefined name 'db' |
| 8814 | F821 | flake8 | `tests/test_audit_chain.py` | 14 | undefined name 'Flask' |
| 8813 | F401 | flake8 | `tests/test_audit_chain.py` | 2 | 'unittest.mock.MagicMock' imported but unused |
| 8812 | F401 | flake8 | `tests/test_audit_chain.py` | 2 | 'unittest.mock.patch' imported but unused |
| 8811 | F811 | flake8 | `tests/test_audit_chain.py` | 2 | redefinition of unused 'patch' from line 1 |
| 8810 | E115 | flake8 | `tests/test_api_versioning.py` | 379 | expected an indented block (comment) |
| 8809 | E115 | flake8 | `tests/test_api_versioning.py` | 332 | expected an indented block (comment) |
| 8808 | F401 | flake8 | `tests/test_api_versioning.py` | 13 | 'unittest.mock.patch' imported but unused |
| 8807 | F401 | flake8 | `tests/test_api_versioning.py` | 12 | 'unittest' imported but unused |
| 8806 | E115 | flake8 | `tests/test_analytics.py` | 214 | expected an indented block (comment) |
| 8805 | F401 | flake8 | `tests/test_acme_certificates.py` | 1 | 'unittest' imported but unused |
| 8804 | E115 | flake8 | `tests/fuzzing/fuzz_validator.py` | 35 | expected an indented block (comment) |
| 8803 | E115 | flake8 | `tests/benchmarks/test_performance.py` | 822 | expected an indented block (comment) |
| 8802 | E115 | flake8 | `tests/benchmarks/test_performance.py` | 629 | expected an indented block (comment) |
| 8801 | F401 | flake8 | `tests/benchmarks/test_performance.py` | 14 | 'pytest' imported but unused |
| 8800 | F541 | flake8 | `scripts/update_type_ignore.py` | 394 | f-string is missing placeholders |
| 8799 | F541 | flake8 | `scripts/update_type_ignore.py` | 387 | f-string is missing placeholders |
| 8798 | E115 | flake8 | `scripts/update_type_ignore.py` | 298 | expected an indented block (comment) |
| 8797 | E115 | flake8 | `scripts/update_type_ignore.py` | 279 | expected an indented block (comment) |
| 8796 | E501 | flake8 | `scripts/update_type_ignore.py` | 242 | line too long (121 > 120 characters) |
| 8795 | E115 | flake8 | `scripts/update_type_ignore.py` | 118 | expected an indented block (comment) |
| 8794 | F401 | flake8 | `scripts/update_type_ignore.py` | 33 | 'typing.Set' imported but unused |
| 8793 | E115 | flake8 | `scripts/sbom_diff.py` | 134 | expected an indented block (comment) |
| 8792 | E115 | flake8 | `scripts/passthrough_manager.py` | 46 | expected an indented block (comment) |
| 8791 | E115 | flake8 | `scripts/generate_security_report_v2.py` | 49 | expected an indented block (comment) |
| 8788 | E128 | flake8 | `scripts/fix_all_errors.py` | 3294 | continuation line under-indented for visual indent |
| 8787 | E303 | flake8 | `scripts/fix_all_errors.py` | 3222 | too many blank lines (3) |
| 8786 | E128 | flake8 | `scripts/fix_all_errors.py` | 3179 | continuation line under-indented for visual indent |
| 8785 | E128 | flake8 | `scripts/fix_all_errors.py` | 3145 | continuation line under-indented for visual indent |
| 8784 | E128 | flake8 | `scripts/fix_all_errors.py` | 3114 | continuation line under-indented for visual indent |
| 8783 | E128 | flake8 | `scripts/fix_all_errors.py` | 3082 | continuation line under-indented for visual indent |
| 8782 | E115 | flake8 | `scripts/fix_all_errors.py` | 3073 | expected an indented block (comment) |
| 8781 | F841 | flake8 | `scripts/fix_all_errors.py` | 3059 | local variable 'original' is assigned to but never used |
| 8780 | E115 | flake8 | `scripts/fix_all_errors.py` | 2980 | expected an indented block (comment) |
| 8779 | F841 | flake8 | `scripts/fix_all_errors.py` | 2970 | local variable 'close_paren' is assigned to but never used |
| 8778 | E115 | flake8 | `scripts/fix_all_errors.py` | 2968 | expected an indented block (comment) |
| 8777 | E115 | flake8 | `scripts/fix_all_errors.py` | 2933 | expected an indented block (comment) |
| 8776 | E128 | flake8 | `scripts/fix_all_errors.py` | 2901 | continuation line under-indented for visual indent |
| 8775 | E115 | flake8 | `scripts/fix_all_errors.py` | 2895 | expected an indented block (comment) |
| 8774 | E115 | flake8 | `scripts/fix_all_errors.py` | 2892 | expected an indented block (comment) |
| 8773 | F841 | flake8 | `scripts/fix_all_errors.py` | 2886 | local variable 'original' is assigned to but never used |
| 8772 | E115 | flake8 | `scripts/fix_all_errors.py` | 2849 | expected an indented block (comment) |
| 8771 | E115 | flake8 | `scripts/fix_all_errors.py` | 2839 | expected an indented block (comment) |
| 8770 | E303 | flake8 | `scripts/fix_all_errors.py` | 2807 | too many blank lines (3) |
| 8769 | E115 | flake8 | `scripts/fix_all_errors.py` | 2791 | expected an indented block (comment) |
| 8768 | E115 | flake8 | `scripts/fix_all_errors.py` | 2784 | expected an indented block (comment) |
| 8767 | E115 | flake8 | `scripts/fix_all_errors.py` | 2778 | expected an indented block (comment) |
| 8766 | E128 | flake8 | `scripts/fix_all_errors.py` | 2758 | continuation line under-indented for visual indent |
| 8765 | E128 | flake8 | `scripts/fix_all_errors.py` | 2757 | continuation line under-indented for visual indent |
| 8764 | E115 | flake8 | `scripts/fix_all_errors.py` | 2743 | expected an indented block (comment) |
| 8763 | E115 | flake8 | `scripts/fix_all_errors.py` | 2736 | expected an indented block (comment) |
| 8762 | E115 | flake8 | `scripts/fix_all_errors.py` | 2729 | expected an indented block (comment) |
| 8761 | E115 | flake8 | `scripts/fix_all_errors.py` | 2638 | expected an indented block (comment) |
| 8760 | E115 | flake8 | `scripts/fix_all_errors.py` | 2565 | expected an indented block (comment) |
| 8759 | E115 | flake8 | `scripts/fix_all_errors.py` | 2558 | expected an indented block (comment) |
| 8758 | E115 | flake8 | `scripts/fix_all_errors.py` | 2553 | expected an indented block (comment) |
| 8757 | E115 | flake8 | `scripts/fix_all_errors.py` | 2510 | expected an indented block (comment) |
| 8756 | E115 | flake8 | `scripts/fix_all_errors.py` | 2507 | expected an indented block (comment) |
| 8755 | E115 | flake8 | `scripts/fix_all_errors.py` | 2498 | expected an indented block (comment) |
| 8754 | E115 | flake8 | `scripts/fix_all_errors.py` | 2495 | expected an indented block (comment) |
| 8753 | E115 | flake8 | `scripts/fix_all_errors.py` | 2493 | expected an indented block (comment) |
| 8752 | E115 | flake8 | `scripts/fix_all_errors.py` | 2446 | expected an indented block (comment) |
| 8751 | E115 | flake8 | `scripts/fix_all_errors.py` | 2444 | expected an indented block (comment) |
| 8750 | E115 | flake8 | `scripts/fix_all_errors.py` | 2330 | expected an indented block (comment) |
| 8749 | E128 | flake8 | `scripts/fix_all_errors.py` | 2294 | continuation line under-indented for visual indent |
| 8748 | E128 | flake8 | `scripts/fix_all_errors.py` | 2262 | continuation line under-indented for visual indent |
| 8747 | E115 | flake8 | `scripts/fix_all_errors.py` | 2260 | expected an indented block (comment) |
| 8746 | E128 | flake8 | `scripts/fix_all_errors.py` | 2258 | continuation line under-indented for visual indent |
| 8745 | E115 | flake8 | `scripts/fix_all_errors.py` | 2256 | expected an indented block (comment) |
| 8744 | E115 | flake8 | `scripts/fix_all_errors.py` | 2250 | expected an indented block (comment) |
| 8743 | E115 | flake8 | `scripts/fix_all_errors.py` | 2248 | expected an indented block (comment) |
| 8742 | E128 | flake8 | `scripts/fix_all_errors.py` | 2232 | continuation line under-indented for visual indent |
| 8741 | E128 | flake8 | `scripts/fix_all_errors.py` | 2217 | continuation line under-indented for visual indent |
| 8740 | E115 | flake8 | `scripts/fix_all_errors.py` | 2195 | expected an indented block (comment) |
| 8739 | E115 | flake8 | `scripts/fix_all_errors.py` | 2176 | expected an indented block (comment) |
| 8738 | E231 | flake8 | `scripts/fix_all_errors.py` | 2153 | missing whitespace after ',' |
| 8737 | E115 | flake8 | `scripts/fix_all_errors.py` | 2111 | expected an indented block (comment) |
| 8736 | E128 | flake8 | `scripts/fix_all_errors.py` | 2108 | continuation line under-indented for visual indent |
| 8735 | E115 | flake8 | `scripts/fix_all_errors.py` | 2104 | expected an indented block (comment) |
| 8734 | E128 | flake8 | `scripts/fix_all_errors.py` | 2096 | continuation line under-indented for visual indent |
| 8733 | E115 | flake8 | `scripts/fix_all_errors.py` | 2086 | expected an indented block (comment) |
| 8732 | E128 | flake8 | `scripts/fix_all_errors.py` | 2084 | continuation line under-indented for visual indent |
| 8731 | F841 | flake8 | `scripts/fix_all_errors.py` | 2078 | local variable 'original_config' is assigned to but never used |
| 8730 | E128 | flake8 | `scripts/fix_all_errors.py` | 2072 | continuation line under-indented for visual indent |
| 8729 | E128 | flake8 | `scripts/fix_all_errors.py` | 2053 | continuation line under-indented for visual indent |
| 8728 | E128 | flake8 | `scripts/fix_all_errors.py` | 2031 | continuation line under-indented for visual indent |
| 8727 | E128 | flake8 | `scripts/fix_all_errors.py` | 1981 | continuation line under-indented for visual indent |
| 8726 | F841 | flake8 | `scripts/fix_all_errors.py` | 1974 | local variable 'modified' is assigned to but never used |
| 8725 | E128 | flake8 | `scripts/fix_all_errors.py` | 1932 | continuation line under-indented for visual indent |
| 8724 | E128 | flake8 | `scripts/fix_all_errors.py` | 1918 | continuation line under-indented for visual indent |
| 8723 | E128 | flake8 | `scripts/fix_all_errors.py` | 1917 | continuation line under-indented for visual indent |
| 8722 | E501 | flake8 | `scripts/fix_all_errors.py` | 1915 | line too long (151 > 120 characters) |
| 8721 | E128 | flake8 | `scripts/fix_all_errors.py` | 1914 | continuation line under-indented for visual indent |
| 8720 | E501 | flake8 | `scripts/fix_all_errors.py` | 1912 | line too long (149 > 120 characters) |
| 8719 | E115 | flake8 | `scripts/fix_all_errors.py` | 1892 | expected an indented block (comment) |
| 8718 | E115 | flake8 | `scripts/fix_all_errors.py` | 1882 | expected an indented block (comment) |
| 8717 | E115 | flake8 | `scripts/fix_all_errors.py` | 1847 | expected an indented block (comment) |
| 8716 | E128 | flake8 | `scripts/fix_all_errors.py` | 1819 | continuation line under-indented for visual indent |
| 8715 | E128 | flake8 | `scripts/fix_all_errors.py` | 1814 | continuation line under-indented for visual indent |
| 8714 | E202 | flake8 | `scripts/fix_all_errors.py` | 1790 | whitespace before '}' |
| 8713 | E201 | flake8 | `scripts/fix_all_errors.py` | 1790 | whitespace after '{' |
| 8712 | E202 | flake8 | `scripts/fix_all_errors.py` | 1789 | whitespace before '}' |
| 8711 | E201 | flake8 | `scripts/fix_all_errors.py` | 1789 | whitespace after '{' |
| 8710 | E115 | flake8 | `scripts/fix_all_errors.py` | 1731 | expected an indented block (comment) |
| 8709 | E115 | flake8 | `scripts/fix_all_errors.py` | 1675 | expected an indented block (comment) |
| 8708 | E115 | flake8 | `scripts/fix_all_errors.py` | 1671 | expected an indented block (comment) |
| 8707 | E115 | flake8 | `scripts/fix_all_errors.py` | 1635 | expected an indented block (comment) |
| 8706 | E128 | flake8 | `scripts/fix_all_errors.py` | 1633 | continuation line under-indented for visual indent |
| 8705 | E115 | flake8 | `scripts/fix_all_errors.py` | 1601 | expected an indented block (comment) |
| 8704 | E302 | flake8 | `scripts/fix_all_errors.py` | 1597 | expected 2 blank lines, found 1 |
| 8703 | E128 | flake8 | `scripts/fix_all_errors.py` | 1258 | continuation line under-indented for visual indent |
| 8702 | E302 | flake8 | `scripts/fix_all_errors.py` | 1074 | expected 2 blank lines, found 1 |
| 8701 | E115 | flake8 | `scripts/fix_all_errors.py` | 950 | expected an indented block (comment) |
| 8700 | F541 | flake8 | `scripts/fix_all_errors.py` | 925 | f-string is missing placeholders |
| 8699 | E115 | flake8 | `scripts/fix_all_errors.py` | 865 | expected an indented block (comment) |
| 8698 | E115 | flake8 | `scripts/fix_all_errors.py` | 855 | expected an indented block (comment) |
| 8697 | E115 | flake8 | `scripts/fix_all_errors.py` | 823 | expected an indented block (comment) |
| 8696 | E115 | flake8 | `scripts/fix_all_errors.py` | 816 | expected an indented block (comment) |
| 8695 | E115 | flake8 | `scripts/fix_all_errors.py` | 814 | expected an indented block (comment) |
| 8694 | E115 | flake8 | `scripts/fix_all_errors.py` | 808 | expected an indented block (comment) |
| 8693 | E115 | flake8 | `scripts/fix_all_errors.py` | 716 | expected an indented block (comment) |
| 8692 | E303 | flake8 | `scripts/fix_all_errors.py` | 715 | too many blank lines (2) |
| 8691 | F811 | flake8 | `scripts/fix_all_errors.py` | 715 | redefinition of unused 'run' from line 175 |
| 8690 | E115 | flake8 | `scripts/fix_all_errors.py` | 686 | expected an indented block (comment) |
| 8689 | E115 | flake8 | `scripts/fix_all_errors.py` | 676 | expected an indented block (comment) |
| 8688 | E115 | flake8 | `scripts/fix_all_errors.py` | 661 | expected an indented block (comment) |
| 8687 | E115 | flake8 | `scripts/fix_all_errors.py` | 656 | expected an indented block (comment) |
| 8686 | E306 | flake8 | `scripts/fix_all_errors.py` | 585 | expected 1 blank line before a nested definition, found 0 |
| 8685 | E128 | flake8 | `scripts/fix_all_errors.py` | 307 | continuation line under-indented for visual indent |
| 8684 | E128 | flake8 | `scripts/fix_all_errors.py` | 306 | continuation line under-indented for visual indent |
| 8683 | E115 | flake8 | `scripts/fix_all_errors.py` | 182 | expected an indented block (comment) |
| 8682 | F401 | flake8 | `scripts/fix_all_errors.py` | 46 | 'typing.Callable' imported but unused |
| 8681 | F401 | flake8 | `scripts/fix_all_errors.py` | 37 | 'os' imported but unused |
| 8680 | E115 | flake8 | `scripts/dev-setup.py` | 763 | expected an indented block (comment) |
| 8679 | E115 | flake8 | `scripts/check_type_coverage.py` | 128 | expected an indented block (comment) |
| 8678 | E115 | flake8 | `scripts/check_type_coverage.py` | 56 | expected an indented block (comment) |
| 8677 | E115 | flake8 | `scripts/check_type_coverage.py` | 52 | expected an indented block (comment) |
| 8676 | E115 | flake8 | `scripts/actions_inspector.py` | 452 | expected an indented block (comment) |
| 8675 | E115 | flake8 | `scripts/actions_inspector.py` | 280 | expected an indented block (comment) |
| 8674 | E115 | flake8 | `scripts/actions_inspector.py` | 274 | expected an indented block (comment) |
| 8673 | E115 | flake8 | `scripts/actions_inspector.py` | 135 | expected an indented block (comment) |
| 8672 | E115 | flake8 | `scripts/actions_inspector.py` | 127 | expected an indented block (comment) |
| 8671 | E115 | flake8 | `scripts/actions_inspector.py` | 118 | expected an indented block (comment) |
| 8670 | E115 | flake8 | `scripts/actions_inspector.py` | 113 | expected an indented block (comment) |
| 8669 | E115 | flake8 | `scripts/actions_inspector.py` | 105 | expected an indented block (comment) |
| 8668 | E115 | flake8 | `opt/web/panel/socketio_server.py` | 717 | expected an indented block (comment) |
| 8667 | E115 | flake8 | `opt/web/panel/socketio_server.py` | 192 | expected an indented block (comment) |
| 8666 | E115 | flake8 | `opt/web/panel/routes/storage.py` | 270 | expected an indented block (comment) |
| 8665 | E115 | flake8 | `opt/web/panel/routes/storage.py` | 198 | expected an indented block (comment) |
| 8664 | E115 | flake8 | `opt/web/panel/routes/passthrough.py` | 487 | expected an indented block (comment) |
| 8663 | E115 | flake8 | `opt/web/panel/routes/passthrough.py` | 293 | expected an indented block (comment) |
| 8662 | E115 | flake8 | `opt/web/panel/routes/nodes.py` | 271 | expected an indented block (comment) |
| 8661 | E115 | flake8 | `opt/web/panel/routes/nodes.py` | 199 | expected an indented block (comment) |
| 8660 | E115 | flake8 | `opt/web/panel/routes/health.py` | 95 | expected an indented block (comment) |
| 8659 | E115 | flake8 | `opt/web/panel/routes/auth.py` | 447 | expected an indented block (comment) |
| 8658 | E115 | flake8 | `opt/web/panel/routes/auth.py` | 401 | expected an indented block (comment) |
| 8657 | E115 | flake8 | `opt/web/panel/routes/auth.py` | 321 | expected an indented block (comment) |
| 8656 | F821 | flake8 | `opt/web/panel/routes/auth.py` | 160 | undefined name 'time' |
| 8655 | E115 | flake8 | `opt/web/panel/rbac.py` | 244 | expected an indented block (comment) |
| 8654 | E122 | flake8 | `opt/web/panel/rbac.py` | 164 | continuation line missing indentation or outdented |
| 8653 | E122 | flake8 | `opt/web/panel/rbac.py` | 157 | continuation line missing indentation or outdented |
| 8652 | E122 | flake8 | `opt/web/panel/rbac.py` | 147 | continuation line missing indentation or outdented |
| 8651 | E122 | flake8 | `opt/web/panel/rbac.py` | 128 | continuation line missing indentation or outdented |
| 8650 | E115 | flake8 | `opt/web/panel/models/audit_log.py` | 369 | expected an indented block (comment) |
| 8649 | E115 | flake8 | `opt/web/panel/models/audit_log.py` | 358 | expected an indented block (comment) |
| 8648 | E115 | flake8 | `opt/web/panel/models/audit_log.py` | 219 | expected an indented block (comment) |
| 8647 | E115 | flake8 | `opt/web/panel/graceful_shutdown.py` | 735 | expected an indented block (comment) |
| 8646 | E115 | flake8 | `opt/web/panel/graceful_shutdown.py` | 641 | expected an indented block (comment) |
| 8645 | E115 | flake8 | `opt/web/panel/graceful_shutdown.py` | 425 | expected an indented block (comment) |
| 8644 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 679 | expected an indented block (comment) |
| 8643 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 657 | expected an indented block (comment) |
| 8642 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 631 | expected an indented block (comment) |
| 8641 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 598 | expected an indented block (comment) |
| 8640 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 575 | expected an indented block (comment) |
| 8639 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 548 | expected an indented block (comment) |
| 8638 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 515 | expected an indented block (comment) |
| 8637 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 463 | expected an indented block (comment) |
| 8636 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 442 | expected an indented block (comment) |
| 8635 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 435 | expected an indented block (comment) |
| 8634 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 384 | expected an indented block (comment) |
| 8633 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 282 | expected an indented block (comment) |
| 8632 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 266 | expected an indented block (comment) |
| 8631 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 252 | expected an indented block (comment) |
| 8630 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 221 | expected an indented block (comment) |
| 8629 | E115 | flake8 | `opt/web/panel/core/rpc_client.py` | 212 | expected an indented block (comment) |
| 8628 | E115 | flake8 | `opt/web/panel/config.py` | 180 | expected an indented block (comment) |
| 8627 | E122 | flake8 | `opt/web/panel/config.py` | 109 | continuation line missing indentation or outdented |
| 8626 | E115 | flake8 | `opt/web/panel/batch_operations.py` | 568 | expected an indented block (comment) |
| 8625 | E115 | flake8 | `opt/web/panel/batch_operations.py` | 558 | expected an indented block (comment) |
| 8624 | E115 | flake8 | `opt/web/panel/batch_operations.py` | 464 | expected an indented block (comment) |
| 8623 | E115 | flake8 | `opt/web/panel/batch_operations.py` | 430 | expected an indented block (comment) |
| 8622 | E115 | flake8 | `opt/web/panel/batch_operations.py` | 406 | expected an indented block (comment) |
| 8621 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 864 | expected an indented block (comment) |
| 8620 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 857 | expected an indented block (comment) |
| 8619 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 853 | expected an indented block (comment) |
| 8618 | E117 | flake8 | `opt/web/panel/auth_2fa.py` | 774 | over-indented (comment) |
| 8617 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 772 | expected an indented block (comment) |
| 8616 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 625 | expected an indented block (comment) |
| 8615 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 421 | expected an indented block (comment) |
| 8614 | E115 | flake8 | `opt/web/panel/auth_2fa.py` | 197 | expected an indented block (comment) |
| 8613 | E115 | flake8 | `opt/web/panel/app.py` | 544 | expected an indented block (comment) |
| 8612 | E115 | flake8 | `opt/web/panel/app.py` | 534 | expected an indented block (comment) |
| 8611 | E115 | flake8 | `opt/web/panel/app.py` | 445 | expected an indented block (comment) |
| 8610 | E115 | flake8 | `opt/web/panel/api_versioning.py` | 383 | expected an indented block (comment) |
| 8609 | E115 | flake8 | `opt/web/panel/api_versioning.py` | 360 | expected an indented block (comment) |
| 8608 | E115 | flake8 | `opt/web/panel/api_versioning.py` | 325 | expected an indented block (comment) |
| 8607 | E115 | flake8 | `opt/web/panel/analytics.py` | 442 | expected an indented block (comment) |
| 8606 | E115 | flake8 | `opt/web/panel/analytics.py` | 435 | expected an indented block (comment) |
| 8605 | E115 | flake8 | `opt/web/panel/analytics.py` | 399 | expected an indented block (comment) |
| 8604 | E115 | flake8 | `opt/web/panel/advanced_auth.py` | 491 | expected an indented block (comment) |
| 8603 | E115 | flake8 | `opt/web/panel/advanced_auth.py` | 286 | expected an indented block (comment) |
| 8602 | E115 | flake8 | `opt/web/panel/advanced_auth.py` | 254 | expected an indented block (comment) |
| 8601 | E115 | flake8 | `opt/tracing_integration.py` | 299 | expected an indented block (comment) |
| 8600 | E115 | flake8 | `opt/tracing_integration.py` | 249 | expected an indented block (comment) |
| 8599 | E115 | flake8 | `opt/tracing_integration.py` | 235 | expected an indented block (comment) |
| 8598 | E115 | flake8 | `opt/tools/debvisor_menu.py` | 170 | expected an indented block (comment) |
| 8597 | E115 | flake8 | `opt/tools/debvisor_menu.py` | 163 | expected an indented block (comment) |
| 8596 | E115 | flake8 | `opt/tools/debvisor_menu.py` | 153 | expected an indented block (comment) |
| 8595 | E115 | flake8 | `opt/testing/test_phase4_week4.py` | 632 | expected an indented block (comment) |
| 8594 | E115 | flake8 | `opt/testing/test_phase4_week4.py` | 177 | expected an indented block (comment) |
| 8593 | E122 | flake8 | `opt/testing/test_e2e_comprehensive.py` | 603 | continuation line missing indentation or outdented |
| 8592 | E115 | flake8 | `opt/testing/mock_mode.py` | 718 | expected an indented block (comment) |
| 8591 | E115 | flake8 | `opt/testing/mock_mode.py` | 248 | expected an indented block (comment) |
| 8590 | E115 | flake8 | `opt/testing/framework.py` | 553 | expected an indented block (comment) |
| 8589 | E115 | flake8 | `opt/system/hypervisor/xen_driver.py` | 882 | expected an indented block (comment) |
| 8588 | E115 | flake8 | `opt/system/hypervisor/xen_driver.py` | 615 | expected an indented block (comment) |
| 8587 | E115 | flake8 | `opt/system/hypervisor/xen_driver.py` | 601 | expected an indented block (comment) |
| 8586 | E115 | flake8 | `opt/system/hypervisor/xen_driver.py` | 364 | expected an indented block (comment) |
| 8585 | E115 | flake8 | `opt/system/hypervisor/xen_driver.py` | 361 | expected an indented block (comment) |
| 8584 | E115 | flake8 | `opt/system/hardware_detection.py` | 802 | expected an indented block (comment) |
| 8583 | E115 | flake8 | `opt/system/hardware_detection.py` | 748 | expected an indented block (comment) |
| 8582 | E115 | flake8 | `opt/system/hardware_detection.py` | 644 | expected an indented block (comment) |
| 8581 | E115 | flake8 | `opt/system/hardware_detection.py` | 512 | expected an indented block (comment) |
| 8580 | E115 | flake8 | `opt/system/hardware_detection.py` | 452 | expected an indented block (comment) |
| 8579 | F541 | flake8 | `opt/services/virtualization/xen_manager.py` | 832 | f-string is missing placeholders |
| 8578 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 704 | expected an indented block (comment) |
| 8577 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 671 | expected an indented block (comment) |
| 8576 | F541 | flake8 | `opt/services/virtualization/xen_manager.py` | 552 | f-string is missing placeholders |
| 8575 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 546 | expected an indented block (comment) |
| 8574 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 541 | expected an indented block (comment) |
| 8573 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 486 | expected an indented block (comment) |
| 8572 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 444 | expected an indented block (comment) |
| 8571 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 234 | expected an indented block (comment) |
| 8570 | E115 | flake8 | `opt/services/virtualization/xen_manager.py` | 209 | expected an indented block (comment) |
| 8569 | F401 | flake8 | `opt/services/virtualization/xen_manager.py` | 97 | 'typing.Tuple' imported but unused |
| 8568 | F401 | flake8 | `opt/services/virtualization/xen_manager.py` | 95 | 'datetime.timezone' imported but unused |
| 8567 | F401 | flake8 | `opt/services/virtualization/xen_manager.py` | 95 | 'datetime.datetime' imported but unused |
| 8566 | F401 | flake8 | `opt/services/virtualization/xen_manager.py` | 88 | 'json' imported but unused |
| 8565 | E115 | flake8 | `opt/services/tracing.py` | 697 | expected an indented block (comment) |
| 8564 | E115 | flake8 | `opt/services/tracing.py` | 661 | expected an indented block (comment) |
| 8563 | E115 | flake8 | `opt/services/tracing.py` | 438 | expected an indented block (comment) |
| 8562 | E115 | flake8 | `opt/services/storage/multiregion_storage.py` | 741 | expected an indented block (comment) |
| 8561 | E117 | flake8 | `opt/services/storage/multiregion_storage.py` | 641 | over-indented (comment) |
| 8560 | E115 | flake8 | `opt/services/storage/multiregion_storage.py` | 640 | expected an indented block (comment) |
| 8559 | E115 | flake8 | `opt/services/storage/multiregion_storage.py` | 503 | expected an indented block (comment) |
| 8558 | E115 | flake8 | `opt/services/storage/multiregion_storage.py` | 401 | expected an indented block (comment) |
| 8557 | E115 | flake8 | `opt/services/slo_tracking.py` | 714 | expected an indented block (comment) |
| 8556 | E115 | flake8 | `opt/services/slo_tracking.py` | 707 | expected an indented block (comment) |
| 8555 | E115 | flake8 | `opt/services/slo_tracking.py` | 681 | expected an indented block (comment) |
| 8554 | E115 | flake8 | `opt/services/slo_tracking.py` | 665 | expected an indented block (comment) |
| 8553 | E115 | flake8 | `opt/services/slo_tracking.py` | 628 | expected an indented block (comment) |
| 8552 | E115 | flake8 | `opt/services/slo_tracking.py` | 612 | expected an indented block (comment) |
| 8551 | E115 | flake8 | `opt/services/slo_tracking.py` | 546 | expected an indented block (comment) |
| 8550 | E122 | flake8 | `opt/services/slo_tracking.py` | 517 | continuation line missing indentation or outdented |
| 8549 | E115 | flake8 | `opt/services/slo_tracking.py` | 213 | expected an indented block (comment) |
| 8548 | E122 | flake8 | `opt/services/security_hardening.py` | 373 | continuation line missing indentation or outdented |
| 8547 | E115 | flake8 | `opt/services/security/ssh_hardening.py` | 819 | expected an indented block (comment) |
| 8546 | E115 | flake8 | `opt/services/security/ssh_hardening.py` | 693 | expected an indented block (comment) |
| 8545 | E115 | flake8 | `opt/services/security/ssh_hardening.py` | 579 | expected an indented block (comment) |
| 8544 | E115 | flake8 | `opt/services/security/ssh_hardening.py` | 539 | expected an indented block (comment) |
| 8543 | E115 | flake8 | `opt/services/security/firewall_manager.py` | 898 | expected an indented block (comment) |
| 8542 | E115 | flake8 | `opt/services/security/firewall_manager.py` | 861 | expected an indented block (comment) |
| 8541 | E115 | flake8 | `opt/services/security/firewall_manager.py` | 853 | expected an indented block (comment) |
| 8540 | E115 | flake8 | `opt/services/security/cert_pinning.py` | 410 | expected an indented block (comment) |
| 8539 | E115 | flake8 | `opt/services/security/cert_pinning.py` | 330 | expected an indented block (comment) |
| 8538 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 748 | expected an indented block (comment) |
| 8537 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 720 | expected an indented block (comment) |
| 8536 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 593 | expected an indented block (comment) |
| 8535 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 540 | expected an indented block (comment) |
| 8534 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 516 | expected an indented block (comment) |
| 8533 | E115 | flake8 | `opt/services/security/acme_certificates.py` | 343 | expected an indented block (comment) |
| 8532 | E115 | flake8 | `opt/services/secrets_management.py` | 655 | expected an indented block (comment) |
| 8531 | E115 | flake8 | `opt/services/secrets_management.py` | 470 | expected an indented block (comment) |
| 8530 | E115 | flake8 | `opt/services/secrets_management.py` | 464 | expected an indented block (comment) |
| 8529 | E115 | flake8 | `opt/services/secrets_management.py` | 397 | expected an indented block (comment) |
| 8528 | E115 | flake8 | `opt/services/secrets_management.py` | 340 | expected an indented block (comment) |
| 8527 | E115 | flake8 | `opt/services/secrets_management.py` | 276 | expected an indented block (comment) |
| 8526 | E115 | flake8 | `opt/services/secrets_management.py` | 217 | expected an indented block (comment) |
| 8525 | E115 | flake8 | `opt/services/secrets_management.py` | 206 | expected an indented block (comment) |
| 8524 | E115 | flake8 | `opt/services/secrets_management.py` | 192 | expected an indented block (comment) |
| 8523 | E115 | flake8 | `opt/services/secrets/vault_manager.py` | 564 | expected an indented block (comment) |
| 8522 | E115 | flake8 | `opt/services/secrets/vault_manager.py` | 494 | expected an indented block (comment) |
| 8521 | E115 | flake8 | `opt/services/secrets/vault_manager.py` | 275 | expected an indented block (comment) |
| 8520 | E115 | flake8 | `opt/services/secrets/vault_manager.py` | 180 | expected an indented block (comment) |
| 8519 | E115 | flake8 | `opt/services/sdn/sdn_controller.py` | 821 | expected an indented block (comment) |
| 8518 | E115 | flake8 | `opt/services/sdn/sdn_controller.py` | 667 | expected an indented block (comment) |
| 8517 | E115 | flake8 | `opt/services/sdn/sdn_controller.py` | 156 | expected an indented block (comment) |
| 8516 | E115 | flake8 | `opt/services/sdn/sdn_controller.py` | 152 | expected an indented block (comment) |
| 8515 | E115 | flake8 | `opt/services/scheduler/cli.py` | 675 | expected an indented block (comment) |
| 8514 | E115 | flake8 | `opt/services/scheduler/api.py` | 191 | expected an indented block (comment) |
| 8513 | E115 | flake8 | `opt/services/rpc/versioning.py` | 402 | expected an indented block (comment) |
| 8512 | E115 | flake8 | `opt/services/rpc/validators.py` | 464 | expected an indented block (comment) |
| 8511 | E115 | flake8 | `opt/services/rpc/validators.py` | 460 | expected an indented block (comment) |
| 8510 | E115 | flake8 | `opt/services/rpc/validators.py` | 431 | expected an indented block (comment) |
| 8509 | E115 | flake8 | `opt/services/rpc/validators.py` | 419 | expected an indented block (comment) |
| 8508 | E115 | flake8 | `opt/services/rpc/validators.py` | 405 | expected an indented block (comment) |
| 8507 | E115 | flake8 | `opt/services/rpc/validators.py` | 330 | expected an indented block (comment) |
| 8506 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 358 | undefined name 'Mock' |
| 8505 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 357 | undefined name 'Mock' |
| 8504 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 356 | undefined name 'Mock' |
| 8503 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 349 | undefined name 'Mock' |
| 8502 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 334 | undefined name 'Mock' |
| 8501 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 333 | undefined name 'Mock' |
| 8500 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 325 | undefined name 'Mock' |
| 8499 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 158 | undefined name 'patch' |
| 8498 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 155 | undefined name 'Mock' |
| 8497 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 150 | undefined name 'Mock' |
| 8496 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 149 | undefined name 'AsyncMock' |
| 8495 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 136 | undefined name 'Mock' |
| 8494 | F821 | flake8 | `opt/services/rpc/tests/test_rpc_features.py` | 135 | undefined name 'AsyncMock' |
| 8493 | E115 | flake8 | `opt/services/rpc/service.py` | 381 | expected an indented block (comment) |
| 8492 | E115 | flake8 | `opt/services/rpc/service.py` | 214 | expected an indented block (comment) |
| 8491 | E115 | flake8 | `opt/services/rpc/service.py` | 203 | expected an indented block (comment) |
| 8490 | E115 | flake8 | `opt/services/rpc/server.py` | 761 | expected an indented block (comment) |
| 8489 | E115 | flake8 | `opt/services/rpc/server.py` | 710 | expected an indented block (comment) |
| 8488 | E115 | flake8 | `opt/services/rpc/server.py` | 573 | expected an indented block (comment) |
| 8487 | E115 | flake8 | `opt/services/rpc/server.py` | 412 | expected an indented block (comment) |
| 8486 | E115 | flake8 | `opt/services/rpc/server.py` | 360 | expected an indented block (comment) |
| 8485 | E115 | flake8 | `opt/services/rpc/server.py` | 310 | expected an indented block (comment) |
| 8484 | E115 | flake8 | `opt/services/rpc/server.py` | 270 | expected an indented block (comment) |
| 8483 | E115 | flake8 | `opt/services/rpc/server.py` | 222 | expected an indented block (comment) |
| 8482 | E115 | flake8 | `opt/services/rpc/server.py` | 170 | expected an indented block (comment) |
| 8481 | E116 | flake8 | `opt/services/rpc/server.py` | 150 | unexpected indentation (comment) |
| 8480 | E116 | flake8 | `opt/services/rpc/server.py` | 145 | unexpected indentation (comment) |
| 8479 | E116 | flake8 | `opt/services/rpc/server.py` | 140 | unexpected indentation (comment) |
| 8478 | E115 | flake8 | `opt/services/rpc/security_enhanced.py` | 692 | expected an indented block (comment) |
| 8477 | E115 | flake8 | `opt/services/rpc/security_enhanced.py` | 599 | expected an indented block (comment) |
| 8476 | E115 | flake8 | `opt/services/rpc/rate_limiter.py` | 150 | expected an indented block (comment) |
| 8475 | E115 | flake8 | `opt/services/rpc/pool.py` | 376 | expected an indented block (comment) |
| 8474 | E115 | flake8 | `opt/services/rpc/pool.py` | 336 | expected an indented block (comment) |
| 8473 | E115 | flake8 | `opt/services/rpc/pool.py` | 311 | expected an indented block (comment) |
| 8472 | E115 | flake8 | `opt/services/rpc/pool.py` | 273 | expected an indented block (comment) |
| 8471 | E115 | flake8 | `opt/services/rpc/pool.py` | 210 | expected an indented block (comment) |
| 8470 | E115 | flake8 | `opt/services/rpc/pool.py` | 192 | expected an indented block (comment) |
| 8469 | E115 | flake8 | `opt/services/rpc/pool.py` | 130 | expected an indented block (comment) |
| 8468 | E115 | flake8 | `opt/services/rpc/health_check.py` | 208 | expected an indented block (comment) |
| 8467 | E115 | flake8 | `opt/services/rpc/error_handling.py` | 336 | expected an indented block (comment) |
| 8466 | E115 | flake8 | `opt/services/rpc/compression.py` | 293 | expected an indented block (comment) |
| 8465 | E115 | flake8 | `opt/services/rpc/cert_manager.py` | 196 | expected an indented block (comment) |
| 8464 | E122 | flake8 | `opt/services/rpc/authz.py` | 316 | continuation line missing indentation or outdented |
| 8463 | E115 | flake8 | `opt/services/rpc/authz.py` | 155 | expected an indented block (comment) |
| 8462 | E115 | flake8 | `opt/services/rpc/authz.py` | 152 | expected an indented block (comment) |
| 8461 | E116 | flake8 | `opt/services/rpc/authz.py` | 115 | unexpected indentation (comment) |
| 8460 | E116 | flake8 | `opt/services/rpc/auth.py` | 698 | unexpected indentation (comment) |
| 8459 | E115 | flake8 | `opt/services/rpc/auth.py` | 657 | expected an indented block (comment) |
| 8458 | E115 | flake8 | `opt/services/rpc/auth.py` | 514 | expected an indented block (comment) |
| 8457 | E115 | flake8 | `opt/services/rpc/auth.py` | 425 | expected an indented block (comment) |
| 8456 | E115 | flake8 | `opt/services/rpc/auth.py` | 257 | expected an indented block (comment) |
| 8455 | E115 | flake8 | `opt/services/rpc/audit.py` | 201 | expected an indented block (comment) |
| 8454 | E115 | flake8 | `opt/services/rpc/audit.py` | 175 | expected an indented block (comment) |
| 8453 | E115 | flake8 | `opt/services/resilience.py` | 528 | expected an indented block (comment) |
| 8452 | E115 | flake8 | `opt/services/resilience.py` | 276 | expected an indented block (comment) |
| 8451 | E115 | flake8 | `opt/services/resilience.py` | 244 | expected an indented block (comment) |
| 8450 | E115 | flake8 | `opt/services/request_signing.py` | 675 | expected an indented block (comment) |
| 8449 | E115 | flake8 | `opt/services/request_signing.py` | 412 | expected an indented block (comment) |
| 8448 | E115 | flake8 | `opt/services/reporting_scheduler.py` | 522 | expected an indented block (comment) |
| 8447 | E115 | flake8 | `opt/services/reporting_scheduler.py` | 474 | expected an indented block (comment) |
| 8446 | E115 | flake8 | `opt/services/reporting_scheduler.py` | 383 | expected an indented block (comment) |
| 8445 | E115 | flake8 | `opt/services/reporting_scheduler.py` | 219 | expected an indented block (comment) |
| 8444 | F821 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 592 | undefined name 'logging' |
| 8443 | F821 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 592 | undefined name 'logging' |
| 8442 | E115 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 541 | expected an indented block (comment) |
| 8441 | E115 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 222 | expected an indented block (comment) |
| 8440 | E115 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 182 | expected an indented block (comment) |
| 8439 | F821 | flake8 | `opt/services/rbac/fine_grained_rbac.py` | 88 | undefined name 'logging' |
| 8438 | E115 | flake8 | `opt/services/query_optimization_enhanced.py` | 505 | expected an indented block (comment) |
| 8437 | E115 | flake8 | `opt/services/query_optimization.py` | 711 | expected an indented block (comment) |
| 8436 | E115 | flake8 | `opt/services/profiling.py` | 588 | expected an indented block (comment) |
| 8435 | E115 | flake8 | `opt/services/profiling.py` | 457 | expected an indented block (comment) |
| 8434 | E115 | flake8 | `opt/services/profiling.py` | 399 | expected an indented block (comment) |
| 8433 | F541 | flake8 | `opt/services/ops/ai_runbooks.py` | 789 | f-string is missing placeholders |
| 8432 | F401 | flake8 | `opt/services/ops/ai_runbooks.py` | 96 | 'pathlib.Path' imported but unused |
| 8431 | F401 | flake8 | `opt/services/ops/ai_runbooks.py` | 95 | 'typing.Tuple' imported but unused |
| 8430 | F401 | flake8 | `opt/services/ops/ai_runbooks.py` | 93 | 'datetime.timedelta' imported but unused |
| 8429 | F401 | flake8 | `opt/services/ops/ai_runbooks.py` | 91 | 're' imported but unused |
| 8428 | F401 | flake8 | `opt/services/ops/ai_runbooks.py` | 89 | 'json' imported but unused |
| 8427 | E115 | flake8 | `opt/services/observability/energy.py` | 156 | expected an indented block (comment) |
| 8426 | E115 | flake8 | `opt/services/observability/energy.py` | 119 | expected an indented block (comment) |
| 8425 | E115 | flake8 | `opt/services/observability/energy.py` | 117 | expected an indented block (comment) |
| 8424 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 1248 | expected an indented block (comment) |
| 8423 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 901 | expected an indented block (comment) |
| 8422 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 849 | expected an indented block (comment) |
| 8421 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 561 | expected an indented block (comment) |
| 8420 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 516 | expected an indented block (comment) |
| 8419 | E115 | flake8 | `opt/services/observability/cardinality_controller.py` | 477 | expected an indented block (comment) |
| 8418 | F541 | flake8 | `opt/services/observability/carbon_telemetry.py` | 904 | f-string is missing placeholders |
| 8417 | E261 | flake8 | `opt/services/observability/carbon_telemetry.py` | 553 | at least two spaces before inline comment |
| 8416 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 451 | expected an indented block (comment) |
| 8415 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 416 | expected an indented block (comment) |
| 8414 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 399 | expected an indented block (comment) |
| 8413 | E116 | flake8 | `opt/services/observability/carbon_telemetry.py` | 391 | unexpected indentation (comment) |
| 8412 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 367 | expected an indented block (comment) |
| 8411 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 363 | expected an indented block (comment) |
| 8410 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 345 | expected an indented block (comment) |
| 8409 | E301 | flake8 | `opt/services/observability/carbon_telemetry.py` | 342 | expected 1 blank line, found 0 |
| 8408 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 330 | expected an indented block (comment) |
| 8407 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 300 | expected an indented block (comment) |
| 8406 | E115 | flake8 | `opt/services/observability/carbon_telemetry.py` | 295 | expected an indented block (comment) |
| 8405 | F401 | flake8 | `opt/services/observability/carbon_telemetry.py` | 90 | 'json' imported but unused |
| 8404 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 1146 | expected an indented block (comment) |
| 8403 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 1091 | expected an indented block (comment) |
| 8402 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 1086 | expected an indented block (comment) |
| 8401 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 835 | expected an indented block (comment) |
| 8400 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 540 | expected an indented block (comment) |
| 8399 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 535 | expected an indented block (comment) |
| 8398 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 355 | expected an indented block (comment) |
| 8397 | E115 | flake8 | `opt/services/network/multitenant_network.py` | 344 | expected an indented block (comment) |
| 8396 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 1039 | expected an indented block (comment) |
| 8395 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 1013 | expected an indented block (comment) |
| 8394 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 985 | expected an indented block (comment) |
| 8393 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 981 | expected an indented block (comment) |
| 8392 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 727 | expected an indented block (comment) |
| 8391 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 723 | expected an indented block (comment) |
| 8390 | E115 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 446 | expected an indented block (comment) |
| 8389 | E115 | flake8 | `opt/services/multiregion/k8s_integration.py` | 256 | expected an indented block (comment) |
| 8388 | E115 | flake8 | `opt/services/multiregion/k8s_integration.py` | 241 | expected an indented block (comment) |
| 8387 | E115 | flake8 | `opt/services/multiregion/k8s_integration.py` | 236 | expected an indented block (comment) |
| 8386 | E115 | flake8 | `opt/services/multiregion/k8s_integration.py` | 163 | expected an indented block (comment) |
| 8385 | E115 | flake8 | `opt/services/multiregion/k8s_integration.py` | 150 | expected an indented block (comment) |
| 8384 | E115 | flake8 | `opt/services/multiregion/failover.py` | 163 | expected an indented block (comment) |
| 8383 | F821 | flake8 | `opt/services/multiregion/core.py` | 922 | undefined name 'timezone' |
| 8382 | F821 | flake8 | `opt/services/multiregion/core.py` | 922 | undefined name 'datetime' |
| 8381 | F821 | flake8 | `opt/services/multiregion/core.py` | 899 | undefined name 'timezone' |
| 8380 | F821 | flake8 | `opt/services/multiregion/core.py` | 899 | undefined name 'datetime' |
| 8379 | F821 | flake8 | `opt/services/multiregion/core.py` | 815 | undefined name 'timezone' |
| 8378 | F821 | flake8 | `opt/services/multiregion/core.py` | 815 | undefined name 'datetime' |
| 8377 | E115 | flake8 | `opt/services/multiregion/core.py` | 807 | expected an indented block (comment) |
| 8376 | F821 | flake8 | `opt/services/multiregion/core.py` | 728 | undefined name 'timezone' |
| 8375 | F821 | flake8 | `opt/services/multiregion/core.py` | 728 | undefined name 'datetime' |
| 8374 | E115 | flake8 | `opt/services/multiregion/core.py` | 717 | expected an indented block (comment) |
| 8373 | F821 | flake8 | `opt/services/multiregion/core.py` | 453 | undefined name 'datetime' |
| 8372 | F821 | flake8 | `opt/services/multiregion/core.py` | 433 | undefined name 'timezone' |
| 8371 | F821 | flake8 | `opt/services/multiregion/core.py` | 433 | undefined name 'datetime' |
| 8370 | F821 | flake8 | `opt/services/multiregion/core.py` | 431 | undefined name 'datetime' |
| 8369 | F821 | flake8 | `opt/services/multiregion/core.py` | 409 | undefined name 'timezone' |
| 8368 | F821 | flake8 | `opt/services/multiregion/core.py` | 409 | undefined name 'datetime' |
| 8367 | F821 | flake8 | `opt/services/multiregion/core.py` | 407 | undefined name 'datetime' |
| 8366 | E115 | flake8 | `opt/services/multiregion/core.py` | 390 | expected an indented block (comment) |
| 8365 | F821 | flake8 | `opt/services/multiregion/core.py` | 217 | undefined name 'datetime' |
| 8364 | F821 | flake8 | `opt/services/multiregion/core.py` | 190 | undefined name 'timezone' |
| 8363 | F821 | flake8 | `opt/services/multiregion/core.py` | 190 | undefined name 'datetime' |
| 8362 | F821 | flake8 | `opt/services/multiregion/core.py` | 190 | undefined name 'datetime' |
| 8361 | F821 | flake8 | `opt/services/multiregion/core.py` | 156 | undefined name 'timezone' |
| 8360 | F821 | flake8 | `opt/services/multiregion/core.py` | 156 | undefined name 'datetime' |
| 8359 | F821 | flake8 | `opt/services/multiregion/core.py` | 156 | undefined name 'datetime' |
| 8358 | F821 | flake8 | `opt/services/multiregion/cli.py` | 557 | undefined name 'sys' |
| 8357 | F821 | flake8 | `opt/services/multiregion/cli.py` | 556 | undefined name 'sys' |
| 8356 | F821 | flake8 | `opt/services/multiregion/cli.py` | 547 | undefined name 'sys' |
| 8355 | F821 | flake8 | `opt/services/multiregion/cli.py` | 546 | undefined name 'sys' |
| 8354 | F821 | flake8 | `opt/services/multiregion/cli.py` | 528 | undefined name 'sys' |
| 8353 | F821 | flake8 | `opt/services/multiregion/cli.py` | 527 | undefined name 'sys' |
| 8352 | F821 | flake8 | `opt/services/multiregion/cli.py` | 486 | undefined name 'sys' |
| 8351 | F821 | flake8 | `opt/services/multiregion/cli.py` | 485 | undefined name 'sys' |
| 8350 | F821 | flake8 | `opt/services/multiregion/cli.py` | 482 | undefined name 'sys' |
| 8349 | F821 | flake8 | `opt/services/multiregion/cli.py` | 481 | undefined name 'sys' |
| 8348 | F821 | flake8 | `opt/services/multiregion/cli.py` | 452 | undefined name 'sys' |
| 8347 | F821 | flake8 | `opt/services/multiregion/cli.py` | 451 | undefined name 'sys' |
| 8346 | F821 | flake8 | `opt/services/multiregion/cli.py` | 448 | undefined name 'sys' |
| 8345 | F821 | flake8 | `opt/services/multiregion/cli.py` | 447 | undefined name 'sys' |
| 8344 | F821 | flake8 | `opt/services/multiregion/cli.py` | 432 | undefined name 'sys' |
| 8343 | F821 | flake8 | `opt/services/multiregion/cli.py` | 431 | undefined name 'sys' |
| 8342 | F821 | flake8 | `opt/services/multiregion/cli.py` | 426 | undefined name 'sys' |
| 8341 | F821 | flake8 | `opt/services/multiregion/cli.py` | 425 | undefined name 'sys' |
| 8340 | F821 | flake8 | `opt/services/multiregion/cli.py` | 418 | undefined name 'sys' |
| 8339 | F821 | flake8 | `opt/services/multiregion/cli.py` | 417 | undefined name 'sys' |
| 8338 | F841 | flake8 | `opt/services/multiregion/cli.py` | 416 | local variable 'e' is assigned to but never used |
| 8337 | F821 | flake8 | `opt/services/multiregion/cli.py` | 415 | undefined name 'sys' |
| 8336 | F821 | flake8 | `opt/services/multiregion/cli.py` | 414 | undefined name 'sys' |
| 8335 | F821 | flake8 | `opt/services/multiregion/cli.py` | 391 | undefined name 'sys' |
| 8334 | F821 | flake8 | `opt/services/multiregion/cli.py` | 390 | undefined name 'sys' |
| 8333 | F821 | flake8 | `opt/services/multiregion/cli.py` | 385 | undefined name 'sys' |
| 8332 | F821 | flake8 | `opt/services/multiregion/cli.py` | 384 | undefined name 'sys' |
| 8331 | F821 | flake8 | `opt/services/multiregion/cli.py` | 377 | undefined name 'sys' |
| 8330 | F821 | flake8 | `opt/services/multiregion/cli.py` | 376 | undefined name 'sys' |
| 8329 | F821 | flake8 | `opt/services/multiregion/cli.py` | 361 | undefined name 'sys' |
| 8328 | F821 | flake8 | `opt/services/multiregion/cli.py` | 360 | undefined name 'sys' |
| 8327 | F821 | flake8 | `opt/services/multiregion/cli.py` | 350 | undefined name 'sys' |
| 8326 | F821 | flake8 | `opt/services/multiregion/cli.py` | 349 | undefined name 'sys' |
| 8325 | E501 | flake8 | `opt/services/multiregion/cli.py` | 341 | line too long (121 > 120 characters) |
| 8324 | F821 | flake8 | `opt/services/multiregion/cli.py` | 327 | undefined name 'sys' |
| 8323 | F821 | flake8 | `opt/services/multiregion/cli.py` | 326 | undefined name 'sys' |
| 8322 | F821 | flake8 | `opt/services/multiregion/cli.py` | 319 | undefined name 'sys' |
| 8321 | F821 | flake8 | `opt/services/multiregion/cli.py` | 318 | undefined name 'sys' |
| 8320 | F821 | flake8 | `opt/services/multiregion/cli.py` | 277 | undefined name 'sys' |
| 8319 | F821 | flake8 | `opt/services/multiregion/cli.py` | 276 | undefined name 'sys' |
| 8318 | E115 | flake8 | `opt/services/multi_cluster.py` | 630 | expected an indented block (comment) |
| 8317 | E115 | flake8 | `opt/services/multi_cluster.py` | 622 | expected an indented block (comment) |
| 8316 | E115 | flake8 | `opt/services/multi_cluster.py` | 614 | expected an indented block (comment) |
| 8315 | E115 | flake8 | `opt/services/multi_cluster.py` | 580 | expected an indented block (comment) |
| 8314 | E115 | flake8 | `opt/services/multi_cluster.py` | 519 | expected an indented block (comment) |
| 8313 | E115 | flake8 | `opt/services/multi_cluster.py` | 396 | expected an indented block (comment) |
| 8312 | E115 | flake8 | `opt/services/migration/import_wizard.py` | 1295 | expected an indented block (comment) |
| 8311 | E115 | flake8 | `opt/services/migration/import_wizard.py` | 839 | expected an indented block (comment) |
| 8310 | E115 | flake8 | `opt/services/migration/import_wizard.py` | 481 | expected an indented block (comment) |
| 8309 | E115 | flake8 | `opt/services/migration/import_wizard.py` | 282 | expected an indented block (comment) |
| 8308 | E115 | flake8 | `opt/services/migration/advanced_migration.py` | 977 | expected an indented block (comment) |
| 8307 | E115 | flake8 | `opt/services/migration/advanced_migration.py` | 796 | expected an indented block (comment) |
| 8306 | E115 | flake8 | `opt/services/migration/advanced_migration.py` | 728 | expected an indented block (comment) |
| 8305 | E115 | flake8 | `opt/services/migration/advanced_migration.py` | 673 | expected an indented block (comment) |
| 8304 | E115 | flake8 | `opt/services/migration/advanced_migration.py` | 450 | expected an indented block (comment) |
| 8303 | E115 | flake8 | `opt/services/message_queue.py` | 161 | expected an indented block (comment) |
| 8302 | E115 | flake8 | `opt/services/marketplace/marketplace_service.py` | 1289 | expected an indented block (comment) |
| 8301 | E115 | flake8 | `opt/services/marketplace/marketplace_service.py` | 1017 | expected an indented block (comment) |
| 8300 | E115 | flake8 | `opt/services/marketplace/marketplace_service.py` | 990 | expected an indented block (comment) |
| 8299 | E115 | flake8 | `opt/services/marketplace/marketplace_service.py` | 680 | expected an indented block (comment) |
| 8298 | F541 | flake8 | `opt/services/marketplace/governance.py` | 784 | f-string is missing placeholders |
| 8297 | E115 | flake8 | `opt/services/marketplace/governance.py` | 614 | expected an indented block (comment) |
| 8296 | E128 | flake8 | `opt/services/marketplace/governance.py` | 608 | continuation line under-indented for visual indent |
| 8295 | E115 | flake8 | `opt/services/marketplace/governance.py` | 334 | expected an indented block (comment) |
| 8294 | E115 | flake8 | `opt/services/marketplace/governance.py` | 329 | expected an indented block (comment) |
| 8293 | E115 | flake8 | `opt/services/marketplace/governance.py` | 324 | expected an indented block (comment) |
| 8292 | E115 | flake8 | `opt/services/marketplace/governance.py` | 319 | expected an indented block (comment) |
| 8291 | E115 | flake8 | `opt/services/marketplace/governance.py` | 317 | expected an indented block (comment) |
| 8290 | F401 | flake8 | `opt/services/marketplace/governance.py` | 94 | 'subprocess' imported but unused |
| 8289 | F401 | flake8 | `opt/services/marketplace/governance.py` | 93 | 'pathlib.Path' imported but unused |
| 8288 | F401 | flake8 | `opt/services/marketplace/governance.py` | 92 | 'typing.Tuple' imported but unused |
| 8287 | F401 | flake8 | `opt/services/marketplace/governance.py` | 92 | 'typing.Set' imported but unused |
| 8286 | F401 | flake8 | `opt/services/marketplace/governance.py` | 90 | 'datetime.timedelta' imported but unused |
| 8285 | F401 | flake8 | `opt/services/marketplace/governance.py` | 88 | 're' imported but unused |
| 8284 | F401 | flake8 | `opt/services/marketplace/governance.py` | 86 | 'json' imported but unused |
| 8283 | F401 | flake8 | `opt/services/marketplace/governance.py` | 85 | 'hashlib' imported but unused |
| 8282 | E115 | flake8 | `opt/services/licensing/licensing_server.py` | 902 | expected an indented block (comment) |
| 8281 | E115 | flake8 | `opt/services/licensing/licensing_server.py` | 855 | expected an indented block (comment) |
| 8280 | E115 | flake8 | `opt/services/licensing/licensing_server.py` | 665 | expected an indented block (comment) |
| 8279 | E115 | flake8 | `opt/services/licensing/licensing_server.py` | 585 | expected an indented block (comment) |
| 8278 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 396 | undefined name 'hashlib' |
| 8277 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 392 | undefined name 'platform' |
| 8276 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 391 | undefined name 'platform' |
| 8275 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 381 | undefined name 'platform' |
| 8274 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 367 | undefined name 'platform' |
| 8273 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 356 | undefined name 'platform' |
| 8272 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 353 | undefined name 'platform' |
| 8271 | F821 | flake8 | `opt/services/licensing/licensing_server.py` | 339 | undefined name 'hashlib' |
| 8270 | E115 | flake8 | `opt/services/health_check.py` | 352 | expected an indented block (comment) |
| 8269 | E115 | flake8 | `opt/services/health_check.py` | 291 | expected an indented block (comment) |
| 8268 | E115 | flake8 | `opt/services/health_check.py` | 285 | expected an indented block (comment) |
| 8267 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 732 | expected an indented block (comment) |
| 8266 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 558 | expected an indented block (comment) |
| 8265 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 413 | expected an indented block (comment) |
| 8264 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 410 | expected an indented block (comment) |
| 8263 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 406 | expected an indented block (comment) |
| 8262 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 375 | expected an indented block (comment) |
| 8261 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 371 | expected an indented block (comment) |
| 8260 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 369 | expected an indented block (comment) |
| 8259 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 366 | expected an indented block (comment) |
| 8258 | E115 | flake8 | `opt/services/ha/fencing_agent.py` | 241 | expected an indented block (comment) |
| 8257 | E115 | flake8 | `opt/services/feature_flags.py` | 153 | expected an indented block (comment) |
| 8256 | E115 | flake8 | `opt/services/feature_flags.py` | 123 | expected an indented block (comment) |
| 8255 | E115 | flake8 | `opt/services/dns/hosting.py` | 274 | expected an indented block (comment) |
| 8254 | E115 | flake8 | `opt/services/diagnostics.py` | 379 | expected an indented block (comment) |
| 8253 | E115 | flake8 | `opt/services/diagnostics.py` | 373 | expected an indented block (comment) |
| 8252 | E115 | flake8 | `opt/services/diagnostics.py` | 307 | expected an indented block (comment) |
| 8251 | E115 | flake8 | `opt/services/diagnostics.py` | 241 | expected an indented block (comment) |
| 8250 | E115 | flake8 | `opt/services/diagnostics.py` | 188 | expected an indented block (comment) |
| 8249 | E115 | flake8 | `opt/services/database/query_optimizer.py` | 625 | expected an indented block (comment) |
| 8248 | E115 | flake8 | `opt/services/database/query_optimizer.py` | 534 | expected an indented block (comment) |
| 8247 | E115 | flake8 | `opt/services/database/query_optimizer.py` | 426 | expected an indented block (comment) |
| 8246 | E115 | flake8 | `opt/services/database/query_optimizer.py` | 275 | expected an indented block (comment) |
| 8245 | E115 | flake8 | `opt/services/cost_optimization/core.py` | 137 | expected an indented block (comment) |
| 8244 | E115 | flake8 | `opt/services/cost/cost_engine.py` | 894 | expected an indented block (comment) |
| 8243 | E115 | flake8 | `opt/services/cost/cost_engine.py` | 494 | expected an indented block (comment) |
| 8242 | E122 | flake8 | `opt/services/cost/cost_engine.py` | 312 | continuation line missing indentation or outdented |
| 8241 | E115 | flake8 | `opt/services/containers/container_integration.py` | 1036 | expected an indented block (comment) |
| 8240 | E115 | flake8 | `opt/services/containers/container_integration.py` | 878 | expected an indented block (comment) |
| 8239 | E115 | flake8 | `opt/services/containers/container_integration.py` | 851 | expected an indented block (comment) |
| 8238 | E115 | flake8 | `opt/services/containers/container_integration.py` | 377 | expected an indented block (comment) |
| 8237 | E115 | flake8 | `opt/services/containers/container_integration.py` | 372 | expected an indented block (comment) |
| 8236 | E115 | flake8 | `opt/services/containers/container_integration.py` | 295 | expected an indented block (comment) |
| 8235 | E115 | flake8 | `opt/services/containers/container_integration.py` | 293 | expected an indented block (comment) |
| 8234 | E115 | flake8 | `opt/services/connection_pool.py` | 843 | expected an indented block (comment) |
| 8233 | E115 | flake8 | `opt/services/connection_pool.py` | 698 | expected an indented block (comment) |
| 8232 | E115 | flake8 | `opt/services/connection_pool.py` | 662 | expected an indented block (comment) |
| 8231 | E115 | flake8 | `opt/services/connection_pool.py` | 499 | expected an indented block (comment) |
| 8230 | E115 | flake8 | `opt/services/connection_pool.py` | 496 | expected an indented block (comment) |
| 8229 | E115 | flake8 | `opt/services/compliance/reporting.py` | 132 | expected an indented block (comment) |
| 8228 | E115 | flake8 | `opt/services/compliance/remediation.py` | 109 | expected an indented block (comment) |
| 8227 | E115 | flake8 | `opt/services/compliance/cli.py` | 143 | expected an indented block (comment) |
| 8226 | F541 | flake8 | `opt/services/compliance/auto_remediation.py` | 795 | f-string is missing placeholders |
| 8225 | F541 | flake8 | `opt/services/compliance/auto_remediation.py` | 789 | f-string is missing placeholders |
| 8224 | F541 | flake8 | `opt/services/compliance/auto_remediation.py` | 784 | f-string is missing placeholders |
| 8223 | E115 | flake8 | `opt/services/compliance/auto_remediation.py` | 729 | expected an indented block (comment) |
| 8222 | E115 | flake8 | `opt/services/compliance/auto_remediation.py` | 560 | expected an indented block (comment) |
| 8221 | E115 | flake8 | `opt/services/compliance/auto_remediation.py` | 519 | expected an indented block (comment) |
| 8220 | E115 | flake8 | `opt/services/compliance/auto_remediation.py` | 471 | expected an indented block (comment) |
| 8219 | E115 | flake8 | `opt/services/compliance/auto_remediation.py` | 234 | expected an indented block (comment) |
| 8218 | F401 | flake8 | `opt/services/compliance/auto_remediation.py` | 93 | 'pathlib.Path' imported but unused |
| 8217 | F401 | flake8 | `opt/services/compliance/auto_remediation.py` | 92 | 'typing.Tuple' imported but unused |
| 8216 | F401 | flake8 | `opt/services/compliance/auto_remediation.py` | 92 | 'typing.Callable' imported but unused |
| 8215 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 956 | expected an indented block (comment) |
| 8214 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 945 | expected an indented block (comment) |
| 8213 | E116 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 882 | unexpected indentation (comment) |
| 8212 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 555 | expected an indented block (comment) |
| 8211 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 523 | expected an indented block (comment) |
| 8210 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 515 | expected an indented block (comment) |
| 8209 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 508 | expected an indented block (comment) |
| 8208 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 501 | expected an indented block (comment) |
| 8207 | E115 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 407 | expected an indented block (comment) |
| 8206 | E115 | flake8 | `opt/services/cache.py` | 584 | expected an indented block (comment) |
| 8205 | E115 | flake8 | `opt/services/cache.py` | 528 | expected an indented block (comment) |
| 8204 | E115 | flake8 | `opt/services/cache.py` | 523 | expected an indented block (comment) |
| 8203 | E115 | flake8 | `opt/services/cache.py` | 505 | expected an indented block (comment) |
| 8202 | E115 | flake8 | `opt/services/cache.py` | 274 | expected an indented block (comment) |
| 8201 | E122 | flake8 | `opt/services/business_metrics.py` | 299 | continuation line missing indentation or outdented |
| 8200 | E115 | flake8 | `opt/services/business_metrics.py` | 180 | expected an indented block (comment) |
| 8199 | F821 | flake8 | `opt/services/billing/billing_integration.py` | 587 | undefined name 'hashlib' |
| 8198 | E115 | flake8 | `opt/services/backup_manager.py` | 428 | expected an indented block (comment) |
| 8197 | E115 | flake8 | `opt/services/backup_manager.py` | 256 | expected an indented block (comment) |
| 8196 | E115 | flake8 | `opt/services/backup_manager.py` | 227 | expected an indented block (comment) |
| 8195 | E115 | flake8 | `opt/services/backup_manager.py` | 195 | expected an indented block (comment) |
| 8194 | E115 | flake8 | `opt/services/backup/dedup_backup_service.py` | 848 | expected an indented block (comment) |
| 8193 | E115 | flake8 | `opt/services/backup/backup_intelligence.py` | 1114 | expected an indented block (comment) |
| 8192 | E116 | flake8 | `opt/services/backup/backup_intelligence.py` | 721 | unexpected indentation (comment) |
| 8191 | E116 | flake8 | `opt/services/backup/backup_intelligence.py` | 711 | unexpected indentation (comment) |
| 8190 | E116 | flake8 | `opt/services/backup/backup_intelligence.py` | 701 | unexpected indentation (comment) |
| 8189 | E115 | flake8 | `opt/services/backup/backup_intelligence.py` | 605 | expected an indented block (comment) |
| 8188 | E115 | flake8 | `opt/services/backup/backup_intelligence.py` | 431 | expected an indented block (comment) |
| 8187 | E115 | flake8 | `opt/services/backup/backup_intelligence.py` | 325 | expected an indented block (comment) |
| 8186 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 547 | expected an indented block (comment) |
| 8185 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 466 | expected an indented block (comment) |
| 8184 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 380 | expected an indented block (comment) |
| 8183 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 364 | expected an indented block (comment) |
| 8182 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 334 | expected an indented block (comment) |
| 8181 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 322 | expected an indented block (comment) |
| 8180 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 294 | expected an indented block (comment) |
| 8179 | E115 | flake8 | `opt/services/auth/ldap_backend.py` | 193 | expected an indented block (comment) |
| 8178 | E115 | flake8 | `opt/services/audit_encryption.py` | 405 | expected an indented block (comment) |
| 8177 | E115 | flake8 | `opt/services/api_key_rotation.py` | 611 | expected an indented block (comment) |
| 8176 | E115 | flake8 | `opt/services/api_key_rotation.py` | 284 | expected an indented block (comment) |
| 8175 | E115 | flake8 | `opt/services/api_key_manager.py` | 294 | expected an indented block (comment) |
| 8174 | E115 | flake8 | `opt/services/anomaly/test_lstm.py` | 83 | expected an indented block (comment) |
| 8173 | E115 | flake8 | `opt/services/anomaly/core.py` | 1131 | expected an indented block (comment) |
| 8172 | E115 | flake8 | `opt/services/anomaly/core.py` | 685 | expected an indented block (comment) |
| 8171 | E115 | flake8 | `opt/services/anomaly/core.py` | 628 | expected an indented block (comment) |
| 8170 | E115 | flake8 | `opt/services/anomaly/core.py` | 570 | expected an indented block (comment) |
| 8169 | E115 | flake8 | `opt/services/anomaly/core.py` | 363 | expected an indented block (comment) |
| 8168 | E115 | flake8 | `opt/services/anomaly/core.py` | 356 | expected an indented block (comment) |
| 8167 | E115 | flake8 | `opt/plugin_architecture.py` | 465 | expected an indented block (comment) |
| 8166 | E115 | flake8 | `opt/plugin_architecture.py` | 389 | expected an indented block (comment) |
| 8165 | E115 | flake8 | `opt/plugin_architecture.py` | 289 | expected an indented block (comment) |
| 8164 | E115 | flake8 | `opt/plugin_architecture.py` | 269 | expected an indented block (comment) |
| 8163 | E115 | flake8 | `opt/netcfg_tui_full.py` | 611 | expected an indented block (comment) |
| 8162 | E115 | flake8 | `opt/netcfg_tui_full.py` | 609 | expected an indented block (comment) |
| 8161 | E115 | flake8 | `opt/netcfg_tui_app.py` | 330 | expected an indented block (comment) |
| 8160 | E115 | flake8 | `opt/netcfg_tui_app.py` | 242 | expected an indented block (comment) |
| 8159 | E115 | flake8 | `opt/netcfg_tui_app.py` | 120 | expected an indented block (comment) |
| 8158 | E115 | flake8 | `opt/netcfg_tui_app.py` | 89 | expected an indented block (comment) |
| 8157 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1385 | expected an indented block (comment) |
| 8156 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1381 | expected an indented block (comment) |
| 8155 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1377 | expected an indented block (comment) |
| 8154 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1350 | expected an indented block (comment) |
| 8153 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1340 | expected an indented block (comment) |
| 8152 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1332 | expected an indented block (comment) |
| 8151 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1161 | expected an indented block (comment) |
| 8150 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1153 | expected an indented block (comment) |
| 8149 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1147 | expected an indented block (comment) |
| 8148 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1116 | expected an indented block (comment) |
| 8147 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 1077 | expected an indented block (comment) |
| 8146 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 904 | expected an indented block (comment) |
| 8145 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 850 | expected an indented block (comment) |
| 8144 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 835 | expected an indented block (comment) |
| 8143 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 828 | expected an indented block (comment) |
| 8142 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 770 | expected an indented block (comment) |
| 8141 | E116 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 761 | unexpected indentation (comment) |
| 8140 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 758 | expected an indented block (comment) |
| 8139 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 711 | expected an indented block (comment) |
| 8138 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 641 | expected an indented block (comment) |
| 8137 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 440 | expected an indented block (comment) |
| 8136 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 289 | expected an indented block (comment) |
| 8135 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 231 | expected an indented block (comment) |
| 8134 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 223 | expected an indented block (comment) |
| 8133 | E115 | flake8 | `opt/netcfg-tui/netcfg_tui.py` | 206 | expected an indented block (comment) |
| 8132 | E115 | flake8 | `opt/netcfg-tui/main.py` | 666 | expected an indented block (comment) |
| 8131 | E115 | flake8 | `opt/netcfg-tui/main.py` | 198 | expected an indented block (comment) |
| 8130 | E115 | flake8 | `opt/netcfg-tui/backends.py` | 452 | expected an indented block (comment) |
| 8129 | E115 | flake8 | `opt/monitoring/fixtures/generator/app.py` | 118 | expected an indented block (comment) |
| 8128 | E115 | flake8 | `opt/monitoring/enhanced.py` | 404 | expected an indented block (comment) |
| 8127 | E116 | flake8 | `opt/models/migrations.py` | 364 | unexpected indentation (comment) |
| 8126 | E122 | flake8 | `opt/models/migrations.py` | 112 | continuation line missing indentation or outdented |
| 8125 | E116 | flake8 | `opt/migrations/env.py` | 110 | unexpected indentation (comment) |
| 8124 | E115 | flake8 | `opt/migrations/env.py` | 90 | expected an indented block (comment) |
| 8123 | E115 | flake8 | `opt/migrations/env.py` | 87 | expected an indented block (comment) |
| 8122 | E115 | flake8 | `opt/k8sctl_enhanced.py` | 532 | expected an indented block (comment) |
| 8121 | E115 | flake8 | `opt/k8sctl_enhanced.py` | 398 | expected an indented block (comment) |
| 8120 | E115 | flake8 | `opt/k8sctl_enhanced.py` | 314 | expected an indented block (comment) |
| 8119 | E115 | flake8 | `opt/hvctl_enhanced.py` | 742 | expected an indented block (comment) |
| 8118 | E115 | flake8 | `opt/hvctl_enhanced.py` | 429 | expected an indented block (comment) |
| 8117 | E115 | flake8 | `opt/hvctl_enhanced.py` | 400 | expected an indented block (comment) |
| 8116 | E115 | flake8 | `opt/hvctl_enhanced.py` | 284 | expected an indented block (comment) |
| 8115 | E115 | flake8 | `opt/graphql_integration.py` | 117 | expected an indented block (comment) |
| 8114 | E115 | flake8 | `opt/graphql_api.py` | 982 | expected an indented block (comment) |
| 8113 | E115 | flake8 | `opt/graphql_api.py` | 578 | expected an indented block (comment) |
| 8112 | E115 | flake8 | `opt/e2e_testing.py` | 590 | expected an indented block (comment) |
| 8111 | E115 | flake8 | `opt/dvctl.py` | 296 | expected an indented block (comment) |
| 8110 | E115 | flake8 | `opt/dvctl.py` | 293 | expected an indented block (comment) |
| 8109 | E115 | flake8 | `opt/distributed_tracing.py` | 444 | expected an indented block (comment) |
| 8108 | E115 | flake8 | `opt/distributed_tracing.py` | 322 | expected an indented block (comment) |
| 8107 | E115 | flake8 | `opt/distributed_tracing.py` | 320 | expected an indented block (comment) |
| 8106 | E115 | flake8 | `opt/distributed_tracing.py` | 251 | expected an indented block (comment) |
| 8105 | E115 | flake8 | `opt/discovery/zerotouch.py` | 178 | expected an indented block (comment) |
| 8104 | E115 | flake8 | `opt/deployment/migrations.py` | 289 | expected an indented block (comment) |
| 8103 | E115 | flake8 | `opt/deployment/migrations.py` | 243 | expected an indented block (comment) |
| 8102 | E115 | flake8 | `opt/deployment/configuration.py` | 492 | expected an indented block (comment) |
| 8101 | E115 | flake8 | `opt/core/unified_backend.py` | 1103 | expected an indented block (comment) |
| 8100 | E115 | flake8 | `opt/core/unified_backend.py` | 171 | expected an indented block (comment) |
| 8099 | E115 | flake8 | `opt/core/request_context.py` | 699 | expected an indented block (comment) |
| 8098 | E115 | flake8 | `opt/core/request_context.py` | 695 | expected an indented block (comment) |
| 8097 | E115 | flake8 | `opt/core/request_context.py` | 647 | expected an indented block (comment) |
| 8096 | E115 | flake8 | `opt/core/config.py` | 256 | expected an indented block (comment) |
| 8095 | E115 | flake8 | `opt/core/config.py` | 123 | expected an indented block (comment) |
| 8094 | E115 | flake8 | `opt/core/config.py` | 94 | expected an indented block (comment) |
| 8093 | E115 | flake8 | `opt/core/cli_utils.py` | 102 | expected an indented block (comment) |
| 8092 | E115 | flake8 | `opt/core/cli_utils.py` | 95 | expected an indented block (comment) |
| 8091 | E115 | flake8 | `opt/config_distributor.py` | 235 | expected an indented block (comment) |
| 8090 | E116 | flake8 | `opt/config_distributor.py` | 160 | unexpected indentation (comment) |
| 8089 | E115 | flake8 | `opt/config/validate-packages.py` | 222 | expected an indented block (comment) |
| 8088 | E115 | flake8 | `opt/config/validate-packages.py` | 208 | expected an indented block (comment) |
| 8087 | E115 | flake8 | `opt/cephctl_enhanced.py` | 452 | expected an indented block (comment) |
| 8086 | E115 | flake8 | `opt/cephctl_enhanced.py` | 314 | expected an indented block (comment) |
| 8085 | E115 | flake8 | `opt/cephctl_enhanced.py` | 249 | expected an indented block (comment) |
| 8084 | E115 | flake8 | `opt/ansible/validate-inventory.py` | 310 | expected an indented block (comment) |
| 8083 | E115 | flake8 | `opt/advanced_features.py` | 737 | expected an indented block (comment) |
| 8082 | E115 | flake8 | `etc/debvisor/test_validate_blocklists.py` | 540 | expected an indented block (comment) |
| 8081 | E115 | flake8 | `etc/debvisor/test_validate_blocklists.py` | 157 | expected an indented block (comment) |
| 8080 | E115 | flake8 | `etc/debvisor/test_validate_blocklists.py` | 60 | expected an indented block (comment) |
| 8079 | E116 | flake8 | `etc/debvisor/test_validate_blocklists.py` | 35 | unexpected indentation (comment) |
| 8078 | py/clear-text-logging-sensitive-data | CodeQL | `scripts/fix_all_errors.py` | 102 | This expression logs sensitive data (secret) as clear text. |
| 8077 | PinnedDependenciesID | Scorecard | `.github/workflows/test.yml` | 94 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8076 | PinnedDependenciesID | Scorecard | `.github/workflows/test.yml` | 80 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8074 | PinnedDependenciesID | Scorecard | `.github/workflows/test.yml` | 35 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8073 | PinnedDependenciesID | Scorecard | `.github/workflows/test.yml` | 32 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8072 | PinnedDependenciesID | Scorecard | `.github/workflows/lint.yml` | 114 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8071 | PinnedDependenciesID | Scorecard | `.github/workflows/architecture.yml` | 24 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8070 | PinnedDependenciesID | Scorecard | `.github/workflows/architecture.yml` | 24 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8069 | PinnedDependenciesID | Scorecard | `.github/workflows/validate-syntax.yml` | 141 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8068 | PinnedDependenciesID | Scorecard | `.github/workflows/validate-syntax.yml` | 139 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8067 | PinnedDependenciesID | Scorecard | `.github/workflows/validate-grafana.yml` | 36 | score is 4: npmCommand not pinned by hash Click Remediation section below to solve this issue |
| 8066 | PinnedDependenciesID | Scorecard | `.github/workflows/validate-configs.yml` | 46 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8065 | PinnedDependenciesID | Scorecard | `.github/workflows/type-check.yml` | 35 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8064 | PinnedDependenciesID | Scorecard | `.github/workflows/type-check.yml` | 34 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8063 | PinnedDependenciesID | Scorecard | `.github/workflows/type-check.yml` | 33 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8062 | PinnedDependenciesID | Scorecard | `.github/workflows/type-check.yml` | 32 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8056 | PinnedDependenciesID | Scorecard | `.github/workflows/security.yml` | 59 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8055 | PinnedDependenciesID | Scorecard | `.github/workflows/security.yml` | 36 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8054 | PinnedDependenciesID | Scorecard | `.github/workflows/security.yml` | 152 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8053 | PinnedDependenciesID | Scorecard | `.github/workflows/security.yml` | 152 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8052 | PinnedDependenciesID | Scorecard | `.github/workflows/security.yml` | 129 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8051 | PinnedDependenciesID | Scorecard | `.github/workflows/sbom.yml` | 26 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8050 | PinnedDependenciesID | Scorecard | `.github/workflows/sbom.yml` | 23 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8049 | PinnedDependenciesID | Scorecard | `.github/workflows/sbom.yml` | 23 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8048 | PinnedDependenciesID | Scorecard | `.github/workflows/release.yml` | 30 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8047 | PinnedDependenciesID | Scorecard | `.github/workflows/release.yml` | 29 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8046 | PinnedDependenciesID | Scorecard | `.github/workflows/release.yml` | 486 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8045 | PinnedDependenciesID | Scorecard | `.github/workflows/release.yml` | 485 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8044 | PinnedDependenciesID | Scorecard | `.github/workflows/performance.yml` | 29 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8043 | PinnedDependenciesID | Scorecard | `.github/workflows/mutation-testing.yml` | 19 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8042 | PinnedDependenciesID | Scorecard | `.github/workflows/mutation-testing.yml` | 18 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8041 | PinnedDependenciesID | Scorecard | `.github/workflows/mutation-testing.yml` | 17 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8040 | PinnedDependenciesID | Scorecard | `.github/workflows/markdown-lint.yml` | 32 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8039 | PinnedDependenciesID | Scorecard | `.github/workflows/markdown-lint.yml` | 31 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8038 | PinnedDependenciesID | Scorecard | `.github/workflows/manifest-validation.yml` | 192 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8037 | PinnedDependenciesID | Scorecard | `.github/workflows/manifest-validation.yml` | 44 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8035 | PinnedDependenciesID | Scorecard | `.github/workflows/lint.yml` | 100 | score is 4: npmCommand not pinned by hash Click Remediation section below to solve this issue |
| 8034 | PinnedDependenciesID | Scorecard | `.github/workflows/lint.yml` | 27 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8033 | PinnedDependenciesID | Scorecard | `.github/workflows/lint.yml` | 26 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8032 | PinnedDependenciesID | Scorecard | `.github/workflows/lint.yml` | 25 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8031 | PinnedDependenciesID | Scorecard | `.github/workflows/fuzzing.yml` | 27 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8030 | PinnedDependenciesID | Scorecard | `.github/workflows/fuzzing.yml` | 26 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8029 | PinnedDependenciesID | Scorecard | `.github/workflows/fuzzing.yml` | 25 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8028 | PinnedDependenciesID | Scorecard | `.github/workflows/fuzz-testing.yml` | 18 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8027 | PinnedDependenciesID | Scorecard | `.github/workflows/fuzz-testing.yml` | 17 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8026 | PinnedDependenciesID | Scorecard | `.github/workflows/deploy.yml` | 28 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8025 | PinnedDependenciesID | Scorecard | `.github/workflows/deploy.yml` | 27 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8024 | PinnedDependenciesID | Scorecard | `.github/workflows/compliance.yml` | 23 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8023 | PinnedDependenciesID | Scorecard | `.github/workflows/compliance.yml` | 22 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8022 | PinnedDependenciesID | Scorecard | `.github/workflows/codeql.yml` | 47 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8021 | PinnedDependenciesID | Scorecard | `.github/workflows/codeql.yml` | 46 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8020 | PinnedDependenciesID | Scorecard | `.github/workflows/chaos-testing.yml` | 18 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8019 | PinnedDependenciesID | Scorecard | `.github/workflows/chaos-testing.yml` | 17 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8018 | PinnedDependenciesID | Scorecard | `.github/workflows/blocklist-integration-tests.yml` | 210 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8017 | PinnedDependenciesID | Scorecard | `.github/workflows/blocklist-integration-tests.yml` | 209 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8016 | PinnedDependenciesID | Scorecard | `.github/workflows/blocklist-integration-tests.yml` | 57 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8015 | PinnedDependenciesID | Scorecard | `.github/workflows/blocklist-integration-tests.yml` | 56 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8012 | PinnedDependenciesID | Scorecard | `.github/workflows/architecture.yml` | 22 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8011 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-syntax-check.yml` | 34 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8010 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-syntax-check.yml` | 33 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8009 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-syntax-check.yml` | 32 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8008 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 241 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8007 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 240 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8006 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 203 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8005 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 202 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8004 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 34 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8003 | PinnedDependenciesID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 33 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8002 | PinnedDependenciesID | Scorecard | `.github/workflows/_common.yml` | 36 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 8001 | PinnedDependenciesID | Scorecard | `.github/workflows/secret-scan.yml` | 62 | score is 4: GitHub-owned GitHubAction not pinned by hash Remediation tip: update your workflow using [https://app.stepsecurity.io](https://app.stepsecurity.io/secureworkflow/UndiFineD/DebVisor/secret-scan.yml/main?enable=pin) Click Remediation section below for further remediation help |
| 8000 | TokenPermissionsID | Scorecard | `.github/workflows/vex-generate.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/vex-generate.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7999 | TokenPermissionsID | Scorecard | `.github/workflows/validate-syntax.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-syntax.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7998 | TokenPermissionsID | Scorecard | `.github/workflows/validate-kustomize.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-kustomize.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7997 | TokenPermissionsID | Scorecard | `.github/workflows/validate-grafana.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-grafana.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7996 | TokenPermissionsID | Scorecard | `.github/workflows/validate-fixtures.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-fixtures.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7995 | TokenPermissionsID | Scorecard | `.github/workflows/validate-dashboards.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-dashboards.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7994 | TokenPermissionsID | Scorecard | `.github/workflows/validate-configs.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-configs.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7993 | TokenPermissionsID | Scorecard | `.github/workflows/validate-blocklists.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/validate-blocklists.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7992 | TokenPermissionsID | Scorecard | `.github/workflows/type-check.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/type-check.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7991 | TokenPermissionsID | Scorecard | `.github/workflows/test.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7990 | TokenPermissionsID | Scorecard | `.github/workflows/test-profile-summary.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-profile-summary.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7989 | TokenPermissionsID | Scorecard | `.github/workflows/test-grafana.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/test-grafana.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7988 | TokenPermissionsID | Scorecard | `.github/workflows/slsa-verify.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/slsa-verify.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7987 | TokenPermissionsID | Scorecard | `.github/workflows/security.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/security.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7986 | TokenPermissionsID | Scorecard | `.github/workflows/secret-scan.yml` | 20 | score is 0: topLevel 'security-events' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/secret-scan.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7985 | TokenPermissionsID | Scorecard | `.github/workflows/sbom.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7984 | TokenPermissionsID | Scorecard | `.github/workflows/sbom-policy.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/sbom-policy.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7983 | TokenPermissionsID | Scorecard | `.github/workflows/runner-smoke.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/runner-smoke.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7982 | TokenPermissionsID | Scorecard | `.github/workflows/release.yml` | 11 | score is 0: topLevel 'packages' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7981 | TokenPermissionsID | Scorecard | `.github/workflows/release.yml` | 10 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7980 | TokenPermissionsID | Scorecard | `.github/workflows/release-please.yml` | 12 | score is 0: topLevel 'actions' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7979 | TokenPermissionsID | Scorecard | `.github/workflows/release-please.yml` | 10 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/release-please.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7978 | TokenPermissionsID | Scorecard | `.github/workflows/push-generator.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/push-generator.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7977 | TokenPermissionsID | Scorecard | `.github/workflows/notifications.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/notifications.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7976 | TokenPermissionsID | Scorecard | `.github/workflows/mutation-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/mutation-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7975 | TokenPermissionsID | Scorecard | `.github/workflows/merge-guard.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/merge-guard.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7974 | TokenPermissionsID | Scorecard | `.github/workflows/markdownlint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdownlint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7973 | TokenPermissionsID | Scorecard | `.github/workflows/markdown-lint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/markdown-lint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7972 | TokenPermissionsID | Scorecard | `.github/workflows/manifest-validation.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/manifest-validation.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7971 | TokenPermissionsID | Scorecard | `.github/workflows/lint.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/lint.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7970 | TokenPermissionsID | Scorecard | `.github/workflows/labeler.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/labeler.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7969 | TokenPermissionsID | Scorecard | `.github/workflows/fuzz-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/fuzz-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7968 | TokenPermissionsID | Scorecard | `.github/workflows/firstboot-smoke-test.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/firstboot-smoke-test.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7967 | TokenPermissionsID | Scorecard | `.github/workflows/doc-integrity.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/doc-integrity.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7966 | TokenPermissionsID | Scorecard | `.github/workflows/deploy.yml` | 13 | score is 0: topLevel 'contents' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/deploy.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7965 | TokenPermissionsID | Scorecard | `.github/workflows/conventional-commits.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/conventional-commits.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7964 | TokenPermissionsID | Scorecard | `.github/workflows/container-scan.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/container-scan.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7963 | TokenPermissionsID | Scorecard | `.github/workflows/compliance.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/compliance.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7962 | TokenPermissionsID | Scorecard | `.github/workflows/codeql.yml` | 20 | score is 0: topLevel 'security-events' permission set to 'write' Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/codeql.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7961 | TokenPermissionsID | Scorecard | `.github/workflows/chaos-testing.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/chaos-testing.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7960 | TokenPermissionsID | Scorecard | `.github/workflows/build-generator.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/build-generator.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7959 | TokenPermissionsID | Scorecard | `.github/workflows/blocklist-validate.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-validate.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7958 | TokenPermissionsID | Scorecard | `.github/workflows/blocklist-integration-tests.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/blocklist-integration-tests.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7957 | TokenPermissionsID | Scorecard | `.github/workflows/architecture.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/architecture.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7956 | TokenPermissionsID | Scorecard | `.github/workflows/ansible-syntax-check.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-syntax-check.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7955 | TokenPermissionsID | Scorecard | `.github/workflows/ansible-inventory-validation.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/ansible-inventory-validation.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7954 | TokenPermissionsID | Scorecard | `.github/workflows/_common.yml` | 1 | score is 0: no topLevel permission defined Remediation tip: Visit [https://app.stepsecurity.io/secureworkflow](https://app.stepsecurity.io/secureworkflow/github.com/UndiFineD/DebVisor/_common.yml/main?enable=permissions). Tick the 'Restrict permissions for GITHUB_TOKEN' Untick other options NOTE: If you want to resolve multiple issues at once, you can visit [https://app.stepsecurity.io/securerepo](https://app.stepsecurity.io/securerepo) instead. Click Remediation section below for further remediation help |
| 7953 | py/stack-trace-exposure | CodeQL | `opt/web/dashboard/app.py` | 234 | Stack trace information flows to this location and may be exposed to an external user. |
| 7951 | py/stack-trace-exposure | CodeQL | `opt/web/dashboard/app.py` | 192 | Stack trace information flows to this location and may be exposed to an external user. |
| 7950 | py/stack-trace-exposure | CodeQL | `opt/web/dashboard/app.py` | 169 | Stack trace information flows to this location and may be exposed to an external user. |
| 7949 | py/stack-trace-exposure | CodeQL | `opt/web/dashboard/app.py` | 142 | Stack trace information flows to this location and may be exposed to an external user. |
| 7948 | py/clear-text-logging-sensitive-data | CodeQL | `opt/services/compliance/core.py` | 308 | This expression logs sensitive data (password) as clear text. |
| 7947 | py/clear-text-logging-sensitive-data | CodeQL | `opt/services/compliance/core.py` | 259 | This expression logs sensitive data (password) as clear text. |
| 7946 | E305 | flake8 | `scripts/fix_all_errors.py` | 3639 | expected 2 blank lines after class or function definition, found 1 |
| 7941 | E302 | flake8 | `scripts/fix_all_errors.py` | 853 | expected 2 blank lines, found 1 |
| 7926 | E302 | flake8 | `scripts/fix_all_errors.py` | 174 | expected 2 blank lines, found 1 |
| 7925 | E261 | flake8 | `scripts/fix_all_errors.py` | 167 | at least two spaces before inline comment |
| 7923 | E261 | flake8 | `scripts/fix_all_errors.py` | 158 | at least two spaces before inline comment |
| 7918 | F841 | flake8 | `scripts/fix_all_errors.py` | 144 | local variable 'original_content' is assigned to but never used |
| 7917 | E261 | flake8 | `scripts/fix_all_errors.py` | 142 | at least two spaces before inline comment |
| 7915 | E302 | flake8 | `scripts/fix_all_errors.py` | 119 | expected 2 blank lines, found 1 |
| 7914 | E302 | flake8 | `scripts/fix_all_errors.py` | 108 | expected 2 blank lines, found 1 |
| 7913 | E302 | flake8 | `scripts/fix_all_errors.py` | 92 | expected 2 blank lines, found 1 |
| 7912 | E302 | flake8 | `scripts/fix_all_errors.py` | 84 | expected 2 blank lines, found 1 |
| 7907 | F401 | flake8 | `scripts/fix_all_errors.py` | 44 | 'dataclasses.asdict' imported but unused |
| 7905 | BinaryArtifactsID | Scorecard | `tools/shellcheck.exe` | 1 | score is 9: binary detected Click Remediation section below to solve this issue |
| 7904 | E302 | flake8 | `tests/test_ssh_hardening.py` | 4 | expected 2 blank lines, found 1 |
| 7900 | E116 | flake8 | `tests/test_migrations.py` | 6 | unexpected indentation (comment) |
| 7899 | E116 | flake8 | `tests/test_migrations.py` | 4 | unexpected indentation (comment) |
| 7898 | E302 | flake8 | `tests/test_marketplace_governance.py` | 9 | expected 2 blank lines, found 1 |
| 7875 | F821 | flake8 | `tests/test_backup_manager_encryption.py` | 40 | undefined name 'AESGCM' |
| 7872 | E302 | flake8 | `tests/test_audit_chain.py` | 12 | expected 2 blank lines, found 1 |
| 7871 | E116 | flake8 | `tests/test_audit_chain.py` | 10 | unexpected indentation (comment) |
| 7870 | E116 | flake8 | `tests/test_audit_chain.py` | 9 | unexpected indentation (comment) |
| 7869 | E116 | flake8 | `tests/test_audit_chain.py` | 8 | unexpected indentation (comment) |
| 7843 | E116 | flake8 | `opt/services/multiregion/replication_scheduler.py` | 85 | unexpected indentation (comment) |
| 7839 | E116 | flake8 | `opt/services/migration/advanced_migration.py` | 82 | unexpected indentation (comment) |
| 7838 | E116 | flake8 | `opt/services/marketplace/marketplace_service.py` | 90 | unexpected indentation (comment) |
| 7837 | E116 | flake8 | `opt/services/marketplace/marketplace_service.py` | 89 | unexpected indentation (comment) |
| 7829 | E116 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 80 | unexpected indentation (comment) |
| 7828 | E116 | flake8 | `opt/services/cluster/large_cluster_optimizer.py` | 79 | unexpected indentation (comment) |
| 7795 | F821 | flake8 | `opt/services/cache.py` | 109 | undefined name 'logging' |
| 7791 | E116 | flake8 | `opt/services/billing/billing_integration.py` | 88 | unexpected indentation (comment) |
| 7790 | E116 | flake8 | `opt/services/backup/dedup_backup_service.py` | 85 | unexpected indentation (comment) |
| 7789 | E116 | flake8 | `opt/services/backup/dedup_backup_service.py` | 81 | unexpected indentation (comment) |
| 7787 | E116 | flake8 | `opt/dvctl.py` | 22 | unexpected indentation (comment) |
| 7786 | E116 | flake8 | `opt/dvctl.py` | 21 | unexpected indentation (comment) |
| 7785 | E116 | flake8 | `opt/dvctl.py` | 20 | unexpected indentation (comment) |
| 7782 | E402 | flake8 | `tests/test_integration_suite.py` | 32 | module level import not at top of file |
| 7781 | E402 | flake8 | `tests/test_integration_suite.py` | 26 | module level import not at top of file |
| 7780 | E402 | flake8 | `tests/test_integration_suite.py` | 25 | module level import not at top of file |
| 7766 | E302 | flake8 | `tests/test_cost_optimization.py` | 10 | expected 2 blank lines, found 1 |
| 7746 | E301 | flake8 | `opt/webhook_system.py` | 390 | expected 1 blank line, found 0 |
| 7745 | E302 | flake8 | `opt/web/dashboard/app.py` | 79 | expected 2 blank lines, found 1 |
| 7744 | E301 | flake8 | `opt/testing/test_e2e_comprehensive.py` | 132 | expected 1 blank line, found 0 |
| 7742 | E302 | flake8 | `opt/services/sdn/sdn_controller.py` | 167 | expected 2 blank lines, found 1 |
| 7280 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 878 | Stack trace information flows to this location and may be exposed to an external user. |
| 7279 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 866 | Stack trace information flows to this location and may be exposed to an external user. |
| 7278 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 845 | Stack trace information flows to this location and may be exposed to an external user. |
| 7277 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 817 | Stack trace information flows to this location and may be exposed to an external user. |
| 7276 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 801 | Stack trace information flows to this location and may be exposed to an external user. |
| 7275 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 657 | Stack trace information flows to this location and may be exposed to an external user. |
| 7274 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 657 | Stack trace information flows to this location and may be exposed to an external user. |
| 7273 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 596 | Stack trace information flows to this location and may be exposed to an external user. |
| 7272 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 596 | Stack trace information flows to this location and may be exposed to an external user. |
| 7271 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 629 | Stack trace information flows to this location and may be exposed to an external user. |
| 7270 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 624 | Stack trace information flows to this location and may be exposed to an external user. |
| 7269 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 585 | Stack trace information flows to this location and may be exposed to an external user. Stack trace information flows to this location and may be exposed to an external user. |
| 7268 | py/stack-trace-exposure | CodeQL | `opt/services/compliance/api.py` | 119 | Stack trace information flows to this location and may be exposed to an external user. |
| 7267 | py/stack-trace-exposure | CodeQL | `opt/services/compliance/api.py` | 117 | Stack trace information flows to this location and may be exposed to an external user. |
| 7266 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 866 | Cross-site scripting vulnerability due to a user-provided value. |
| 7265 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 845 | Cross-site scripting vulnerability due to a user-provided value. |
| 7264 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 817 | Cross-site scripting vulnerability due to a user-provided value. |
| 7263 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 801 | Cross-site scripting vulnerability due to a user-provided value. |
| 7262 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 624 | Cross-site scripting vulnerability due to a user-provided value. |
| 7261 | py/incomplete-url-substring-sanitization | CodeQL | `tests/test_acme_certificates.py` | 59 | The string example.com may be at an arbitrary position in the sanitized URL. |
| 7141 | py/weak-sensitive-data-hashing | CodeQL | `opt/services/api_key_rotation.py` | 317 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 7128 | py/clear-text-logging-sensitive-data | CodeQL | `opt/services/secrets/vault_manager.py` | 712 | This expression logs sensitive data (secret) as clear text. This expression logs sensitive data (secret) as clear text. |
| 7127 | py/clear-text-logging-sensitive-data | CodeQL | `opt/services/secrets_management.py` | 691 | This expression logs sensitive data (password) as clear text. |
| 7077 | py/url-redirection | CodeQL | `opt/web/panel/app.py` | 552 | Untrusted URL redirection depends on a user-provided value. |
| 7076 | SecurityPolicyID | Scorecard | `no file associated with this alert` | 1 | score is 4: security policy file detected: Warn: no linked content found Click Remediation section below to solve this issue |
| 6925 | py/url-redirection | CodeQL | `opt/web/panel/routes/auth.py` | 193 | Untrusted URL redirection depends on a user-provided value. |
| 6801 | E302 | flake8 | `tests/test_backup_manager_encryption.py` | 22 | expected 2 blank lines, found 1 |
| 6350 | SASTID | Scorecard | `no file associated with this alert` | 1 | score is 7: SAST tool detected but not run on all commits: Warn: 0 commits out of 9 are checked with a SAST tool Click Remediation section below to solve this issue |
| 6199 | VulnerabilitiesID | Scorecard | `no file associated with this alert` | 1 | score is 0: 10 existing vulnerabilities detected: Warn: Project is vulnerable to: PYSEC-2024-48 / GHSA-fj7x-q9j7-g6q6 Warn: Project is vulnerable to: GHSA-mr82-8j83-vxmv Warn: Project is vulnerable to: GHSA-4grg-w6v8-c28g Warn: Project is vulnerable to: GHSA-43qf-4rqw-9q2g Warn: Project is vulnerable to: GHSA-7rxf-gvfg-47g4 Warn: Project is vulnerable to: GHSA-84pr-m4jr-85g5 Warn: Project is vulnerable to: GHSA-8vgw-p6qm-5gr7 Warn: Project is vulnerable to: PYSEC-2024-71 / GHSA-hxwh-jpp2-84pm Warn: Project is vulnerable to: GHSA-hc5x-x2vx-497g Warn: Project is vulnerable to: GHSA-w3h3-4rj7-4ph4 Click Remediation section below to solve this issue |
| 6198 | MaintainedID | Scorecard | `no file associated with this alert` | 1 | score is 0: project was created within the last 90 days. Please review its contents carefully: Warn: Repository was created within the last 90 days. Click Remediation section below to solve this issue |
| 6196 | CodeReviewID | Scorecard | `no file associated with this alert` | 1 | score is 0: Found 0/21 approved changesets -- score normalized to 0 Click Remediation section below to solve this issue |
| 6195 | CIIBestPracticesID | Scorecard | `no file associated with this alert` | 1 | score is 0: no effort to earn an OpenSSF best practices badge detected Click Remediation section below to solve this issue |
| 6082 | PinnedDependenciesID | Scorecard | `opt/monitoring/fixtures/generator/Dockerfile` | 12 | score is 4: pipCommand not pinned by hash Click Remediation section below to solve this issue |
| 6081 | PinnedDependenciesID | Scorecard | `opt/monitoring/fixtures/generator/Dockerfile` | 2 | score is 4: containerImage not pinned by hash Remediation tip: pin your Docker image by updating python:3.11-slim to python:3.11-slim@sha256:7cd0079a9bd8800c81632d65251048fc2848bf9afda542224b1b10e0cae45575 Click Remediation section below for further remediation help |
| 5770 | BranchProtectionID | Scorecard | `no file associated with this alert` | 1 | score is 3: branch protection is not maximal on development and all release branches: Warn: could not determine whether codeowners review is allowed Warn: no status checks found to merge onto branch 'main' Warn: PRs are not required to make changes on branch 'main'; or we don't have data to detect it.If you think it might be the latter, make sure to run Scorecard with a PAT or use Repo Rules (that are always public) instead of Branch Protection settings Click Remediation section below to solve this issue |
| 83 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 651 | Stack trace information flows to this location and may be exposed to an external user. |
| 82 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 651 | Stack trace information flows to this location and may be exposed to an external user. |
| 81 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 645 | Stack trace information flows to this location and may be exposed to an external user. |
| 80 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 645 | Stack trace information flows to this location and may be exposed to an external user. |
| 79 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 638 | Stack trace information flows to this location and may be exposed to an external user. |
| 78 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 638 | Stack trace information flows to this location and may be exposed to an external user. |
| 77 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 632 | Stack trace information flows to this location and may be exposed to an external user. |
| 76 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 632 | Stack trace information flows to this location and may be exposed to an external user. |
| 75 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 627 | Stack trace information flows to this location and may be exposed to an external user. |
| 74 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 627 | Stack trace information flows to this location and may be exposed to an external user. |
| 73 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 622 | Stack trace information flows to this location and may be exposed to an external user. |
| 72 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 622 | Stack trace information flows to this location and may be exposed to an external user. |
| 71 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 616 | Stack trace information flows to this location and may be exposed to an external user. |
| 70 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 616 | Stack trace information flows to this location and may be exposed to an external user. |
| 69 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 611 | Stack trace information flows to this location and may be exposed to an external user. |
| 68 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 611 | Stack trace information flows to this location and may be exposed to an external user. |
| 67 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 606 | Stack trace information flows to this location and may be exposed to an external user. |
| 66 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 606 | Stack trace information flows to this location and may be exposed to an external user. |
| 65 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 601 | Stack trace information flows to this location and may be exposed to an external user. |
| 64 | py/stack-trace-exposure | CodeQL | `opt/services/multiregion/api.py` | 601 | Stack trace information flows to this location and may be exposed to an external user. |
| 60 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 870 | Stack trace information flows to this location and may be exposed to an external user. |
| 58 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 858 | Stack trace information flows to this location and may be exposed to an external user. |
| 57 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 853 | Stack trace information flows to this location and may be exposed to an external user. |
| 56 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 849 | Stack trace information flows to this location and may be exposed to an external user. |
| 54 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 837 | Stack trace information flows to this location and may be exposed to an external user. |
| 53 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 833 | Stack trace information flows to this location and may be exposed to an external user. |
| 52 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 825 | Stack trace information flows to this location and may be exposed to an external user. |
| 51 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 821 | Stack trace information flows to this location and may be exposed to an external user. |
| 49 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 809 | Stack trace information flows to this location and may be exposed to an external user. |
| 48 | py/stack-trace-exposure | CodeQL | `opt/services/anomaly/api.py` | 805 | Stack trace information flows to this location and may be exposed to an external user. |
| 44 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 619 | Stack trace information flows to this location and may be exposed to an external user. |
| 43 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 612 | Stack trace information flows to this location and may be exposed to an external user. |
| 42 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 607 | Stack trace information flows to this location and may be exposed to an external user. |
| 41 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 602 | Stack trace information flows to this location and may be exposed to an external user. Stack trace information flows to this location and may be exposed to an external user. |
| 40 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 597 | Stack trace information flows to this location and may be exposed to an external user. |
| 39 | py/stack-trace-exposure | CodeQL | `opt/services/scheduler/api.py` | 592 | Stack trace information flows to this location and may be exposed to an external user. |
| 37 | py/weak-sensitive-data-hashing | CodeQL | `opt/services/rpc/auth.py` | 658 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 34 | py/weak-sensitive-data-hashing | CodeQL | `opt/services/api_key_manager.py` | 222 | Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. Sensitive data (password) is used in a hashing algorithm (SHA256) that is insecure for password hashing, since it is not a computationally expensive hash function. |
| 32 | py/reflective-xss | CodeQL | `opt/services/multiregion/api.py` | 632 | Cross-site scripting vulnerability due to a user-provided value. |
| 31 | py/reflective-xss | CodeQL | `opt/services/multiregion/api.py` | 616 | Cross-site scripting vulnerability due to a user-provided value. |
| 30 | py/reflective-xss | CodeQL | `opt/services/multiregion/api.py` | 611 | Cross-site scripting vulnerability due to a user-provided value. |
| 29 | py/reflective-xss | CodeQL | `opt/services/multiregion/api.py` | 606 | Cross-site scripting vulnerability due to a user-provided value. |
| 27 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 858 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 26 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 853 | Cross-site scripting vulnerability due to a user-provided value. |
| 24 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 833 | Cross-site scripting vulnerability due to a user-provided value. |
| 23 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 825 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 21 | py/reflective-xss | CodeQL | `opt/services/anomaly/api.py` | 809 | Cross-site scripting vulnerability due to a user-provided value. Cross-site scripting vulnerability due to a user-provided value. |
| 18 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 619 | Cross-site scripting vulnerability due to a user-provided value. |
| 17 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 612 | Cross-site scripting vulnerability due to a user-provided value. |
| 16 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 607 | Cross-site scripting vulnerability due to a user-provided value. |
| 15 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 602 | Cross-site scripting vulnerability due to a user-provided value. |
| 14 | py/reflective-xss | CodeQL | `opt/services/scheduler/api.py` | 597 | Cross-site scripting vulnerability due to a user-provided value. |
| 11 | py/clear-text-storage-sensitive-data | CodeQL | `opt/tools/first_boot_keygen.py` | 138 | This expression stores sensitive data (secret) as clear text. |
| 10 | py/clear-text-logging-sensitive-data | CodeQL | `opt/system/hypervisor/xen_driver.py` | 1048 | This expression logs sensitive data (password) as clear text. |
| 1 | py/clear-text-logging-sensitive-data | CodeQL | `opt/services/api_key_manager.py` | 519 | This expression logs sensitive data (password) as clear text. This expression logs sensitive data (password) as clear text. |

