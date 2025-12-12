import unittest
# from opt.services.marketplace.marketplace_service import (
#     SecurityScanner, Recipe, SecurityScanResult
# )
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime


class TestMarketplaceGovernance(unittest.TestCase):

    def setUp(self) -> None:
        self.scanner = SecurityScanner()
        self.recipe = Recipe(
            _name = "test-app",
            _version = "1.0.0",
            _publisher = "test-pub",
            _description = "Test App",
            _license = "MIT",
            _homepage = "https://example.com",
            _signatures = {"key1": "sig1"}
        )

    def test_trust_score_perfect(self) -> None:
    # Perfect score
        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 100)

    def test_trust_score_vulnerabilities(self) -> None:
    # Add vulnerabilities
        self.recipe.security_scan = SecurityScanResult(
            _passed = True,
            _scanned_at = None,  # type: ignore[arg-type]
            _scanner_version = "test",
            _vulnerabilities = [],
            _critical_count = 0,
            _high_count = 1,    # -20
            _medium_count = 2,    # -10
            _low_count = 0
        )
        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 70)    # 100 - 20 - 10

    def test_trust_score_missing_metadata(self) -> None:
        self.recipe.signatures = {}    # -30
        self.recipe.license = None    # -10

        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 60)    # 100 - 30 - 10

    def test_enforce_policy_pass(self) -> None:
        self.recipe.security_scan = SecurityScanResult(
            passed=True,
            _scanned_at = None,  # type: ignore[arg-type]
            _scanner_version = "test",
            _vulnerabilities = [],
            _critical_count = 0,
            _high_count = 0,
            _medium_count = 0,
            _low_count = 0
        )
        passed, msg = self.scanner.enforce_policy(self.recipe, min_score=80)
        self.assertTrue(passed)

    def test_enforce_policy_fail_critical(self) -> None:
        self.recipe.security_scan = SecurityScanResult(
            passed=False,    # Critical failure
            _scanned_at = None,  # type: ignore[arg-type]
            _scanner_version = "test",
            _vulnerabilities = [],
            _critical_count = 1,
            _high_count = 0,
            _medium_count = 0,
            _low_count = 0
        )
        passed, msg = self.scanner.enforce_policy(self.recipe)
        self.assertFalse(passed)
        self.assertIn("Security scan failed", msg)

    def test_enforce_policy_fail_score(self) -> None:
        self.recipe.signatures = {}    # -30
        self.recipe.license = None    # -10
        # Score 60

        passed, msg = self.scanner.enforce_policy(self.recipe, min_score=70)
        self.assertFalse(passed)
        self.assertIn("Trust score 60", msg)
