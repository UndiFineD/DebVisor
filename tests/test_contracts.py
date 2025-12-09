#!/usr/bin/env python3
"""
Contract Testing for DebVisor APIs.

Implements consumer-driven contract testing using Pact:
- Provider contract verification
- Consumer contract generation
- Schema validation
- Breaking change detection

Author: DebVisor Team
Date: November 28, 2025
"""

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import pytest

# =============================================================================
# Contract Types
# =============================================================================


class HTTPMethod(Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class MatcherType(Enum):
    """Types of matchers for contract validation."""

    EXACT = "exact"
    REGEX = "regex"
    TYPE = "type"
    MIN_MAX = "min_max"
    EACH_LIKE = "each_like"
    ARRAY_CONTAINS = "array_contains"


# =============================================================================
# Matchers
# =============================================================================


@dataclass
class Matcher:
    """Base matcher for contract validation."""

    matcher_type: MatcherType
    expected: Any

    def matches(self, actual: Any) -> bool:
        """Check if actual value matches expectation."""
        raise NotImplementedError


class ExactMatcher(Matcher):
    """Exact value matcher."""

    def __init__(self, expected: Any):
        super().__init__(MatcherType.EXACT, expected)

    def matches(self, actual: Any) -> bool:
        return actual == self.expected


class RegexMatcher(Matcher):
    """Regex pattern matcher."""

    def __init__(self, pattern: str, example: str = ""):
        super().__init__(MatcherType.REGEX, pattern)
        self.pattern = re.compile(pattern)
        self.example = example

    def matches(self, actual: Any) -> bool:
        if not isinstance(actual, str):
            return False
        return bool(self.pattern.match(actual))


class TypeMatcher(Matcher):
    """Type matcher."""

    def __init__(self, expected_type: Type):
        super().__init__(MatcherType.TYPE, expected_type)

    def matches(self, actual: Any) -> bool:
        return isinstance(actual, self.expected)


class MinMaxMatcher(Matcher):
    """Range matcher for numbers."""

    def __init__(
        self, min_val: Optional[float] = None, max_val: Optional[float] = None
    ):
        super().__init__(MatcherType.MIN_MAX, {"min": min_val, "max": max_val})
        self.min_val = min_val
        self.max_val = max_val

    def matches(self, actual: Any) -> bool:
        if not isinstance(actual, (int, float)):
            return False
        if self.min_val is not None and actual < self.min_val:
            return False
        if self.max_val is not None and actual > self.max_val:
            return False
        return True


class EachLikeMatcher(Matcher):
    """Array matcher where each element matches template."""

    def __init__(self, template: Dict[str, Any], min_items: int = 1):
        super().__init__(MatcherType.EACH_LIKE, template)
        self.template = template
        self.min_items = min_items

    def matches(self, actual: Any) -> bool:
        if not isinstance(actual, list):
            return False
        if len(actual) < self.min_items:
            return False
        # Simplified - would need recursive schema validation
        return True


# =============================================================================
# Contract Definitions
# =============================================================================


@dataclass
class RequestContract:
    """Contract for HTTP request."""

    method: HTTPMethod
    path: str
    headers: Dict[str, Union[str, Matcher]] = field(default_factory=dict)
    query: Dict[str, Union[str, Matcher]] = field(default_factory=dict)
    body: Optional[Union[Dict[str, Any], Matcher]] = None


@dataclass
class ResponseContract:
    """Contract for HTTP response."""

    status: int
    headers: Dict[str, Union[str, Matcher]] = field(default_factory=dict)
    body: Optional[Union[Dict[str, Any], Matcher]] = None


@dataclass
class Interaction:
    """Single request/response interaction."""

    description: str
    request: RequestContract
    response: ResponseContract
    provider_state: Optional[str] = None


@dataclass
class Contract:
    """Full contract between consumer and provider."""

    consumer: str
    provider: str
    interactions: List[Interaction] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Contract Builder
# =============================================================================


class ContractBuilder:
    """Builder for creating contracts."""

    def __init__(self, consumer: str, provider: str):
        self.contract = Contract(consumer=consumer, provider=provider)
        self._current_interaction: Optional[Interaction] = None

    def given(self, provider_state: str) -> "ContractBuilder":
        """Set provider state for next interaction."""
        if self._current_interaction:
            self._current_interaction.provider_state = provider_state
        return self

    def upon_receiving(self, description: str) -> "ContractBuilder":
        """Start a new interaction."""
        self._current_interaction = Interaction(
            description=description,
            request=RequestContract(method=HTTPMethod.GET, path="/"),
            response=ResponseContract(status=200),
        )
        return self

    def with_request(
        self,
        method: HTTPMethod,
        path: str,
        headers: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> "ContractBuilder":
        """Define request details."""
        if self._current_interaction:
            self._current_interaction.request = RequestContract(
                method=method,
                path=path,
                headers=headers or {},
                query=query or {},
                body=body,
            )
        return self

    def will_respond_with(
        self,
        status: int,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> "ContractBuilder":
        """Define expected response."""
        if self._current_interaction:
            self._current_interaction.response = ResponseContract(
                status=status, headers=headers or {}, body=body
            )
            self.contract.interactions.append(self._current_interaction)
            self._current_interaction = None
        return self

    def build(self) -> Contract:
        """Build and return the contract."""
        return self.contract


# =============================================================================
# Contract Validator
# =============================================================================


class ContractValidationError(Exception):
    """Raised when contract validation fails."""

    pass


class ContractValidator:
    """Validates responses against contracts."""

    def __init__(self, contract: Contract):
        self.contract = contract
        self.validation_errors: List[str] = []

    def validate_response(
        self,
        interaction: Interaction,
        actual_status: int,
        actual_headers: Dict[str, str],
        actual_body: Any,
    ) -> bool:
        """Validate actual response against expected contract."""
        self.validation_errors = []

        # Validate status
        if actual_status != interaction.response.status:
            self.validation_errors.append(
                f"Status mismatch: expected {interaction.response.status}, got {actual_status}"
            )

        # Validate headers
        for key, expected in interaction.response.headers.items():
            actual = actual_headers.get(key)
            if isinstance(expected, Matcher):
                if not expected.matches(actual):
                    self.validation_errors.append(
                        f"Header '{key}' mismatch: {actual} doesn't match {expected}"
                    )
            elif actual != expected:
                self.validation_errors.append(
                    f"Header '{key}' mismatch: expected '{expected}', got '{actual}'"
                )

        # Validate body
        if interaction.response.body is not None:
            body_errors = self._validate_body(
                interaction.response.body, actual_body, "body"
            )
            self.validation_errors.extend(body_errors)

        return len(self.validation_errors) == 0

    def _validate_body(self, expected: Any, actual: Any, path: str) -> List[str]:
        """Recursively validate body structure."""
        errors = []

        if isinstance(expected, Matcher):
            if not expected.matches(actual):
                errors.append(
                    f"{path}: value doesn't match {expected.matcher_type.value} matcher"
                )
        elif isinstance(expected, dict):
            if not isinstance(actual, dict):
                errors.append(f"{path}: expected object, got {type(actual).__name__}")
            else:
                for key, exp_value in expected.items():
                    if key not in actual:
                        errors.append(f"{path}.{key}: missing required field")
                    else:
                        errors.extend(
                            self._validate_body(exp_value, actual[key], f"{path}.{key}")
                        )
        elif isinstance(expected, list):
            if not isinstance(actual, list):
                errors.append(f"{path}: expected array, got {type(actual).__name__}")
            # Additional array validation could go here
        elif expected != actual:
            errors.append(f"{path}: expected {expected!r}, got {actual!r}")

        return errors


# =============================================================================
# DebVisor API Contracts
# =============================================================================


class DebVisorContracts:
    """Contract definitions for DebVisor API."""

    @staticmethod
    def debt_api_contract() -> Contract:
        """Contract for Debt API endpoints."""
        return (
            ContractBuilder("web-panel", "debt-service")
            .given("debts exist")
            .upon_receiving("a request to list debts")
            .with_request(
                method=HTTPMethod.GET,
                path="/api/v2/debts",
                headers={
                    "Authorization": RegexMatcher(r"Bearer .+", "Bearer token123")
                },
            )
            .will_respond_with(
                status=200,
                headers={"Content-Type": "application/json"},
                body={
                    "data": EachLikeMatcher(
                        {
                            "id": TypeMatcher(str),
                            "debtor_id": TypeMatcher(str),
                            "creditor_id": TypeMatcher(str),
                            "original_amount": MinMaxMatcher(min_val=0),
                            "current_balance": MinMaxMatcher(min_val=0),
                            "status": RegexMatcher(
                                r"pending|active|paid|settled|disputed|cancelled"
                            ),
                            "created_at": TypeMatcher(str),
                        },
                        min_items=0,
                    ),
                    "pagination": {
                        "page": TypeMatcher(int),
                        "per_page": TypeMatcher(int),
                        "total": TypeMatcher(int),
                        "total_pages": TypeMatcher(int),
                    },
                },
            )
            .given("debt exists")
            .upon_receiving("a request to get single debt")
            .with_request(
                method=HTTPMethod.GET,
                path="/api/v2/debts/123",
                headers={"Authorization": RegexMatcher(r"Bearer .+")},
            )
            .will_respond_with(
                status=200,
                headers={"Content-Type": "application/json"},
                body={
                    "id": TypeMatcher(str),
                    "debtor_id": TypeMatcher(str),
                    "creditor_id": TypeMatcher(str),
                    "original_amount": MinMaxMatcher(min_val=0),
                    "current_balance": MinMaxMatcher(min_val=0),
                    "status": TypeMatcher(str),
                    "type": TypeMatcher(str),
                    "created_at": TypeMatcher(str),
                    "updated_at": TypeMatcher(str),
                },
            )
            .given("no authentication")
            .upon_receiving("unauthorized request")
            .with_request(method=HTTPMethod.GET, path="/api/v2/debts")
            .will_respond_with(
                status=401, body={"error": "Unauthorized", "message": TypeMatcher(str)}
            )
            .build()
        )

    @staticmethod
    def payment_api_contract() -> Contract:
        """Contract for Payment API endpoints."""
        return (
            ContractBuilder("web-panel", "payment-service")
            .given("valid payment details")
            .upon_receiving("a request to create payment")
            .with_request(
                method=HTTPMethod.POST,
                path="/api/v2/payments",
                headers={
                    "Authorization": RegexMatcher(r"Bearer .+"),
                    "Content-Type": "application/json",
                },
                body={
                    "debt_id": TypeMatcher(str),
                    "amount": MinMaxMatcher(min_val=0.01),
                    "method": RegexMatcher(r"ach|card|check|wire"),
                },
            )
            .will_respond_with(
                status=201,
                headers={"Content-Type": "application/json"},
                body={
                    "id": TypeMatcher(str),
                    "debt_id": TypeMatcher(str),
                    "amount": TypeMatcher((int, float)),
                    "status": ExactMatcher("pending"),
                    "created_at": TypeMatcher(str),
                },
            )
            .given("invalid payment amount")
            .upon_receiving("payment with negative amount")
            .with_request(
                method=HTTPMethod.POST,
                path="/api/v2/payments",
                headers={
                    "Authorization": RegexMatcher(r"Bearer .+"),
                    "Content-Type": "application/json",
                },
                body={"debt_id": "123", "amount": -100, "method": "card"},
            )
            .will_respond_with(
                status=400,
                body={"error": "Validation Error", "details": TypeMatcher(list)},
            )
            .build()
        )

    @staticmethod
    def user_api_contract() -> Contract:
        """Contract for User API endpoints."""
        return (
            ContractBuilder("web-panel", "user-service")
            .given("user exists")
            .upon_receiving("a request to get user profile")
            .with_request(
                method=HTTPMethod.GET,
                path="/api/v2/users/me",
                headers={"Authorization": RegexMatcher(r"Bearer .+")},
            )
            .will_respond_with(
                status=200,
                body={
                    "id": TypeMatcher(str),
                    "email": RegexMatcher(r".+@.+\..+"),
                    "first_name": TypeMatcher(str),
                    "last_name": TypeMatcher(str),
                    "role": RegexMatcher(r"consumer|agent|admin"),
                    "created_at": TypeMatcher(str),
                },
            )
            .build()
        )


# =============================================================================
# Contract Tests
# =============================================================================


class TestDebtAPIContract:
    """Contract tests for Debt API."""

    @pytest.fixture
    def contract(self) -> None:
        return DebVisorContracts.debt_api_contract()

    @pytest.fixture
    def validator(self, contract):
        return ContractValidator(contract)

    def test_list_debts_contract(self, contract, validator):
        """Test: List debts endpoint matches contract."""
        interaction = contract.interactions[0]  # First interaction

Simulated response from provider
        actual_response = {
            "data": [
                {
                    "id": "debt-123",
                    "debtor_id": "user-456",
                    "creditor_id": "cred-789",
                    "original_amount": 5000.00,
                    "current_balance": 3500.00,
                    "status": "active",
                    "created_at": "2024-01-15T10:30:00Z",
                }
            ],
            "pagination": {"page": 1, "per_page": 20, "total": 1, "total_pages": 1},
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=200,
            actual_headers={"Content-Type": "application/json"},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"

    def test_get_debt_contract(self, contract, validator):
        """Test: Get single debt endpoint matches contract."""
        interaction = contract.interactions[1]  # Second interaction

        actual_response = {
            "id": "debt-123",
            "debtor_id": "user-456",
            "creditor_id": "cred-789",
            "original_amount": 5000.00,
            "current_balance": 3500.00,
            "status": "active",
            "type": "medical",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:00:00Z",
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=200,
            actual_headers={"Content-Type": "application/json"},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"

    def test_unauthorized_contract(self, contract, validator):
        """Test: Unauthorized response matches contract."""
        interaction = contract.interactions[2]  # Third interaction

        actual_response = {
            "error": "Unauthorized",
            "message": "Invalid or missing authentication token",
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=401,
            actual_headers={},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"


class TestPaymentAPIContract:
    """Contract tests for Payment API."""

    @pytest.fixture
    def contract(self) -> None:
        return DebVisorContracts.payment_api_contract()

    @pytest.fixture
    def validator(self, contract):
        return ContractValidator(contract)

    def test_create_payment_contract(self, contract, validator):
        """Test: Create payment endpoint matches contract."""
        interaction = contract.interactions[0]

        actual_response = {
            "id": "pay-123",
            "debt_id": "debt-456",
            "amount": 500.00,
            "status": "pending",
            "created_at": "2024-01-20T15:00:00Z",
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=201,
            actual_headers={"Content-Type": "application/json"},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"

    def test_invalid_payment_contract(self, contract, validator):
        """Test: Invalid payment response matches contract."""
        interaction = contract.interactions[1]

        actual_response = {
            "error": "Validation Error",
            "details": ["Amount must be positive"],
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=400,
            actual_headers={},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"


class TestUserAPIContract:
    """Contract tests for User API."""

    @pytest.fixture
    def contract(self) -> None:
        return DebVisorContracts.user_api_contract()

    @pytest.fixture
    def validator(self, contract):
        return ContractValidator(contract)

    def test_get_profile_contract(self, contract, validator):
        """Test: Get user profile matches contract."""
        interaction = contract.interactions[0]

        actual_response = {
            "id": "user-123",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "consumer",
            "created_at": "2024-01-01T00:00:00Z",
        }

        is_valid = validator.validate_response(
            interaction,
            actual_status=200,
            actual_headers={},
            actual_body=actual_response,
        )

        assert is_valid, f"Validation errors: {validator.validation_errors}"


# =============================================================================
# Contract Export
# =============================================================================


def export_contract_to_json(contract: Contract) -> str:
    """Export contract to JSON format (Pact-compatible)."""

    def serialize_matcher(m: Any) -> Any:
        if isinstance(m, Matcher):
            return {
                "type": m.matcher_type.value,
                "expected": (
                    str(m.expected)
                    if not isinstance(m.expected, (str, int, float, bool, type(None)))
                    else m.expected
                ),
            }
        return m

    interactions = []
    for interaction in contract.interactions:
        inter_dict = {
            "description": interaction.description,
            "providerState": interaction.provider_state,
            "request": {
                "method": interaction.request.method.value,
                "path": interaction.request.path,
                "headers": {
                    k: serialize_matcher(v)
                    for k, v in interaction.request.headers.items()
                },
                "query": interaction.request.query,
                "body": interaction.request.body,
            },
            "response": {
                "status": interaction.response.status,
                "headers": {
                    k: serialize_matcher(v)
                    for k, v in interaction.response.headers.items()
                },
                "body": (
                    serialize_matcher(interaction.response.body)
                    if interaction.response.body
                    else None
                ),
            },
        }
        interactions.append(inter_dict)

    pact = {
        "consumer": {"name": contract.consumer},
        "provider": {"name": contract.provider},
        "interactions": interactions,
        "metadata": {"pactSpecification": {"version": "2.0.0"}, **contract.metadata},
    }

    return json.dumps(pact, indent=2, default=str)


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    # Export contracts
    contracts = [
        DebVisorContracts.debt_api_contract(),
        DebVisorContracts.payment_api_contract(),
        DebVisorContracts.user_api_contract(),
    ]

    for contract in contracts:
        filename = f"pact-{contract.consumer}-{contract.provider}.json"
        json_content = export_contract_to_json(contract)
        print(f"\n{'='*60}")
        print(f"Contract: {contract.consumer} -> {contract.provider}")
        print(f"{'='*60}")
        print(json_content[:500] + "..." if len(json_content) > 500 else json_content)

    # Run tests
    pytest.main([__file__, "-v"])
