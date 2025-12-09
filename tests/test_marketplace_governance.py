import unittest
from unittest.mock import MagicMock
from opt.services.marketplace.marketplace_service import (
    SecurityScanner, Recipe, SecurityScanResult, SeverityLevel, CVERecord
)


class TestMarketplaceGovernance(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = SecurityScanner()
        self.recipe = Recipe(
            name="test-app",
            version="1.0.0",
            publisher="test-pub",
            description="Test App",
            license="MIT",
            homepage="https://example.com",
            signatures={"key1": "sig1"}
        )

    def test_trust_score_perfect(self) -> None:
        # Perfect score
        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 100)

    def test_trust_score_vulnerabilities(self) -> None:
        # Add vulnerabilities
        self.recipe.security_scan = SecurityScanResult(
            passed=True,
            scanned_at=None,
            scanner_version="test",
            vulnerabilities=[],
            critical_count=0,
            high_count=1,  # -20
            medium_count=2,  # -10
            low_count=0
        )
        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 70)  # 100 - 20 - 10

    def test_trust_score_missing_metadata(self) -> None:
        self.recipe.signatures = {}  # -30
        self.recipe.license = None  # -10

        score = self.scanner.calculate_trust_score(self.recipe)
        self.assertEqual(score, 60)  # 100 - 30 - 10

    def test_enforce_policy_pass(self) -> None:
        self.recipe.security_scan = SecurityScanResult(
            passed=True,
            scanned_at=None,
            scanner_version="test",
            vulnerabilities=[],
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0
        )
        passed, msg = self.scanner.enforce_policy(self.recipe, min_score=80)
        self.assertTrue(passed)

    def test_enforce_policy_fail_critical(self) -> None:
        self.recipe.security_scan = SecurityScanResult(
            passed=False,  # Critical failure
            scanned_at=None,
            scanner_version="test",
            vulnerabilities=[],
            critical_count=1,
            high_count=0,
            medium_count=0,
            low_count=0
        )
        passed, msg = self.scanner.enforce_policy(self.recipe)
        self.assertFalse(passed)
        self.assertIn("Security scan failed", msg)

    def test_enforce_policy_fail_score(self) -> None:
        self.recipe.signatures = {}  # -30
        self.recipe.license = None  # -10
        # Score 60

        passed, msg = self.scanner.enforce_policy(self.recipe, min_score=70)
        self.assertFalse(passed)
        self.assertIn("Trust score 60", msg)
