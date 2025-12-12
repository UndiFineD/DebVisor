# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

"""
Enterprise Billing Integration for DebVisor.

Provides comprehensive billing system integration with support for:
- External billing provider webhooks (Stripe, Invoice Ninja, etc.)
- Usage-based metering and invoice generation
- Subscription management and billing cycles
- Payment processing and reconciliation
- Tax calculation and compliance
- Multi-currency support
- Credit/debit management
- Dunning and collections

Author: DebVisor Team
Date: November 28, 2025
"""

import json
import logging
# import hashlib
import hmac
    # import jsonimport logging
import threading
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

_logger=logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================
class BillingProvider(Enum):
    """Supported billing providers."""

    STRIPE = "stripe"
    INVOICE_NINJA = "invoice_ninja"
    CHARGEBEE = "chargebee"
    RECURLY = "recurly"
    PADDLE = "paddle"
    CUSTOM = "custom"
    INTERNAL = "internal"


class InvoiceStatus(Enum):
    """Invoice status states."""

    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class PaymentStatus(Enum):
    """Payment status states."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class SubscriptionStatus(Enum):
    """Subscription status states."""

    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class BillingCycle(Enum):
    """Billing cycle options."""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ONE_TIME = "one_time"


class CreditType(Enum):
    """Credit/adjustment types."""

    PROMOTIONAL = "promotional"
    GOODWILL = "goodwill"
    REFUND = "refund"
    PREPAID = "prepaid"
    OVERPAYMENT = "overpayment"
    REFERRAL = "referral"


class TaxType(Enum):
    """Tax types."""

    VAT = "vat"
    GST = "gst"
    SALES_TAX = "sales_tax"
    EXEMPT = "exempt"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass


class BillingConfig:
    """Billing system configuration."""

    provider: BillingProvider = BillingProvider.INTERNAL
    api_key: str = ""
    api_secret: str = ""
    webhook_secret: str = ""
    environment: str = "production"    # production, sandbox
    default_currency: str = "USD"
    tax_inclusive: bool = False
    auto_invoice: bool = True
    invoice_prefix: str = "INV"
    dunning_enabled: bool = True
    grace_period_days: int = 7
    retry_failed_payments: bool = True
    retry_attempts: int = 3
    retry_interval_hours: int = 24


@dataclass


class TaxRule:
    """Tax calculation rule."""

    id: str
    name: str
    tax_type: TaxType
    rate: Decimal    # As percentage
    country: str
    region: Optional[str] = None
    applies_to: List[str] = field(default_factory=list)    # Product categories
    active: bool = True

    def calculate_tax(self, amount: Decimal) -> Decimal:
        """Calculate tax for given amount."""
        return (amount * self.rate / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


@dataclass


class LineItem:
    """Invoice line item."""

    id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    currency: str = "USD"
    tax_rate: Decimal=Decimal("0")
    discount_pct: Decimal=Decimal("0")
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property

    def subtotal(self) -> Decimal:
        """Calculate subtotal before tax."""
        base = self.quantity * self.unit_price
        _discount=base * (self.discount_pct / Decimal("100"))
        return (base - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property

    def tax_amount(self) -> Decimal:
        """Calculate tax amount."""
        return (self.subtotal * self.tax_rate / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property

    def total(self) -> Decimal:
        """Calculate total including tax."""
        return self.subtotal + self.tax_amount


@dataclass


class Invoice:
    """Invoice record."""

    id: str
    number: str
    tenant_id: str
    status: InvoiceStatus = InvoiceStatus.DRAFT
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    subtotal: Decimal=Decimal("0")
    tax_total: Decimal=Decimal("0")
    discount_total: Decimal=Decimal("0")
    total: Decimal=Decimal("0")
    amount_paid: Decimal=Decimal("0")
    amount_due: Decimal=Decimal("0")
    issue_date: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    billing_period_start: Optional[datetime] = None
    billing_period_end: Optional[datetime] = None
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    external_id: Optional[str] = None    # ID in external billing system

    def calculate_totals(self) -> None:
        """Recalculate invoice totals."""
        self.subtotal=sum((item.subtotal for item in self.line_items), Decimal("0"))
        self.tax_total=sum((item.tax_amount for item in self.line_items), Decimal("0"))
        self.total = self.subtotal + self.tax_total
        self.amount_due = self.total - self.amount_paid

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "tenant_id": self.tenant_id,
            "status": self.status.value,
            "currency": self.currency,
            "line_items": [
                {
                    "id": item.id,
                    "description": item.description,
                    "quantity": str(item.quantity),
                    "unit_price": str(item.unit_price),
                    "subtotal": str(item.subtotal),
                    "tax_amount": str(item.tax_amount),
                    "total": str(item.total),
                }
                for item in self.line_items
            ],
            "subtotal": str(self.subtotal),
            "tax_total": str(self.tax_total),
            "total": str(self.total),
            "amount_paid": str(self.amount_paid),
            "amount_due": str(self.amount_due),
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }


@dataclass


class Payment:
    """Payment record."""

    id: str
    invoice_id: str
    tenant_id: str
    amount: Decimal
    currency: str = "USD"
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method: str = "card"    # card, bank_transfer, paypal, crypto
    reference: str = ""
    processed_at: Optional[datetime] = None
    external_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass


class Subscription:
    """Subscription record."""

    id: str
    tenant_id: str
    plan_id: str
    plan_name: str
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    price: Decimal=Decimal("0")
    currency: str = "USD"
    start_date: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancel_at_period_end: bool = False
    external_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass


class Credit:
    """Account credit record."""

    id: str
    tenant_id: str
    amount: Decimal
    remaining: Decimal
    currency: str = "USD"
    credit_type: CreditType = CreditType.PROMOTIONAL
    description: str = ""
    expires_at: Optional[datetime] = None
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))

    @property

    def is_valid(self) -> bool:
        """Check if credit is still valid."""
        if self.remaining <= 0:
            return False
        if self.expires_at and datetime.now(timezone.utc) > self.expires_at:
            return False
        return True


@dataclass


class WebhookEvent:
    """Webhook event from billing provider."""

    id: str
    provider: BillingProvider
    event_type: str
    payload: Dict[str, Any]
    signature: str
    received_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    processed: bool = False
    processed_at: Optional[datetime] = None
    error: Optional[str] = None


# =============================================================================
# Billing Provider Interface
# =============================================================================
class BillingProviderInterface(ABC):
    """Abstract interface for billing providers."""

    @abstractmethod
    async def create_customer(
        self, tenant_id: str, email: str, name: str, metadata: Dict[str, Any]
    ) -> str:
        """Create customer in billing system."""
        pass

    @abstractmethod
    async def create_subscription(
        self, customer_id: str, plan_id: str, trial_days: int = 0
    ) -> Subscription:
        """Create subscription for customer."""
        pass

    @abstractmethod
    async def cancel_subscription(
        self, subscription_id: str, at_period_end: bool = True
    ) -> bool:
        """Cancel subscription."""
        pass

    @abstractmethod
    async def create_invoice(
        self, customer_id: str, line_items: List[LineItem]
    ) -> Invoice:
        """Create invoice for customer."""
        pass

    @abstractmethod
    async def process_payment(self, invoice_id: str, payment_method_id: str) -> Payment:
        """Process payment for invoice."""
        pass

    @abstractmethod

    def verify_webhook(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature."""
        pass


# =============================================================================
# Internal Billing Provider
# =============================================================================
class InternalBillingProvider(BillingProviderInterface):
    """Internal billing provider for self-hosted billing."""

    def __init__(self, config: BillingConfig) -> None:
        self.config = config
        self._customers: Dict[str, Dict[str, Any]] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._invoices: Dict[str, Invoice] = {}
        self._payments: Dict[str, Payment] = {}
        self._invoice_counter = 0
        self._lock=threading.Lock()

    async def create_customer(
        self, tenant_id: str, email: str, name: str, metadata: Dict[str, Any]
    ) -> str:
        """Create internal customer record."""
        _customer_id=f"cust_{uuid.uuid4().hex[:12]}"
        self._customers[customer_id] = {
            "id": customer_id,
            "tenant_id": tenant_id,
            "email": email,
            "name": name,
            "metadata": metadata,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        logger.info(f"Created internal customer: {customer_id}")
        return customer_id

    async def create_subscription(
        self, customer_id: str, plan_id: str, trial_days: int = 0
    ) -> Subscription:
        """Create internal subscription."""
        _subscription_id=f"sub_{uuid.uuid4().hex[:12]}"
        _now=datetime.now(timezone.utc)

        subscription = Subscription(
            _id=subscription_id,
            _tenant_id=self._customers.get(customer_id, {}).get("tenant_id", ""),
            _plan_id=plan_id,
            _plan_name = f"Plan {plan_id}",
            _status = (
                SubscriptionStatus.TRIAL
                if trial_days > 0
                else SubscriptionStatus.ACTIVE
            ),
            _start_date = now,
            _current_period_start = now,
            _current_period_end=now + timedelta(days=30),
            _trial_end=now + timedelta(days=trial_days) if trial_days > 0 else None,
        )

        self._subscriptions[subscription_id] = subscription
        logger.info(f"Created internal subscription: {subscription_id}")
        return subscription

    async def cancel_subscription(
        self, subscription_id: str, at_period_end: bool = True
    ) -> bool:
        """Cancel internal subscription."""
        if subscription_id not in self._subscriptions:
            return False

        subscription = self._subscriptions[subscription_id]
        subscription.cancel_at_period_end = at_period_end

        if not at_period_end:
            subscription.status = SubscriptionStatus.CANCELLED
            subscription.cancelled_at=datetime.now(timezone.utc)

        logger.info(f"Cancelled subscription: {subscription_id}")
        return True

    async def create_invoice(
        self, customer_id: str, line_items: List[LineItem]
    ) -> Invoice:
        """Create internal invoice."""
        with self._lock:
            self._invoice_counter += 1
            invoice_number = f"{self.config.invoice_prefix}-{self._invoice_counter:06d}"

        _invoice_id=f"inv_{uuid.uuid4().hex[:12]}"
        _now=datetime.now(timezone.utc)

        invoice = Invoice(
            _id=invoice_id,
            _number=invoice_number,
            _tenant_id=self._customers.get(customer_id, {}).get("tenant_id", ""),
            _line_items = line_items,
            _issue_date = now,
            _due_date=now + timedelta(days=30),
        )
        invoice.calculate_totals()

        self._invoices[invoice_id] = invoice
        logger.info(f"Created internal invoice: {invoice_number}")
        return invoice

    async def process_payment(self, invoice_id: str, payment_method_id: str) -> Payment:
        """Process internal payment."""
        _invoice=self._invoices.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice not found: {invoice_id}")

        _payment_id=f"pay_{uuid.uuid4().hex[:12]}"
        payment = Payment(
            _id=payment_id,
            _invoice_id = invoice_id,
            _tenant_id = invoice.tenant_id,
            _amount=invoice.amount_due,
            _currency = invoice.currency,
            _status=PaymentStatus.COMPLETED,
            _payment_method = payment_method_id,
            _processed_at=datetime.now(timezone.utc),
        )

        # Update invoice
        invoice.amount_paid += payment.amount
        invoice.amount_due = invoice.total - invoice.amount_paid
        if invoice.amount_due <= 0:
            invoice.status = InvoiceStatus.PAID
            invoice.paid_date=datetime.now(timezone.utc)
        else:
            invoice.status = InvoiceStatus.PARTIAL

        self._payments[payment_id] = payment
        logger.info(f"Processed payment: {payment_id} for invoice {invoice_id}")
        return payment

    def verify_webhook(self, payload: bytes, signature: str) -> bool:
        """Verify internal webhook signature."""
        expected = hmac.new(
            self.config.webhook_secret.encode(), payload, hashlib.sha256  # type: ignore[name-defined]
        ).hexdigest()
        return hmac.compare_digest(signature, expected)


# =============================================================================
# Stripe Billing Provider
# =============================================================================
class StripeBillingProvider(BillingProviderInterface):
    """Stripe billing provider integration."""

    def __init__(self, config: BillingConfig) -> None:
        self.config = config
        self._stripe = None
        self._initialized = False

    def _ensure_initialized(self) -> Any:
        """Ensure Stripe is initialized."""
        if self._initialized:
            return self._stripe

        try:
            import stripe

            stripe.api_key = self.config.api_key
            self._stripe = stripe
            self._initialized = True
            logger.info("Stripe billing provider initialized")
        except ImportError:
            logger.warning("Stripe library not installed")
            raise RuntimeError("Stripe library required: pip install stripe")
        return self._stripe

    async def create_customer(
        self, tenant_id: str, email: str, name: str, metadata: Dict[str, Any]
    ) -> str:
        """Create Stripe customer."""
        _stripe_client=self._ensure_initialized()

        customer = stripe_client.Customer.create(
            _email = email,
            _name = name,
            _metadata={
                "tenant_id": tenant_id,
                **metadata,
            },
        )

        logger.info(f"Created Stripe customer: {customer.id}")
        return str(customer.id)

    async def create_subscription(
        self, customer_id: str, plan_id: str, trial_days: int = 0
    ) -> Subscription:
        """Create Stripe subscription."""
        _stripe_client=self._ensure_initialized()

        params: Dict[str, Any] = {
            "customer": customer_id,
            "items": [{"price": plan_id}],
        }

        if trial_days > 0:
            params["trial_period_days"] = trial_days

        _stripe_sub=stripe_client.Subscription.create(**params)

        return Subscription(
            _id=f"sub_{uuid.uuid4().hex[:12]}",
            _tenant_id = "",    # Will be resolved from customer
            _plan_id=plan_id,
            _plan_name = plan_id,
            _status=(
                SubscriptionStatus.TRIAL
                if stripe_sub.status == "trialing"
                else SubscriptionStatus.ACTIVE
            ),
            _external_id = stripe_sub.id,
            _start_date=datetime.fromtimestamp(stripe_sub.created, tz=timezone.utc),
            _current_period_start=datetime.fromtimestamp(
                stripe_sub.current_period_start, tz=timezone.utc
            ),
            _current_period_end=datetime.fromtimestamp(
                stripe_sub.current_period_end, tz=timezone.utc
            ),
        )

    async def cancel_subscription(
        self, subscription_id: str, at_period_end: bool = True
    ) -> bool:
        """Cancel Stripe subscription."""
        _stripe_client=self._ensure_initialized()

        try:
            if at_period_end:
                stripe_client.Subscription.modify(
                    subscription_id, cancel_at_period_end=True
                )
            else:
                stripe_client.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            logger.error(f"Failed to cancel subscription: {e}")
            return False

    async def create_invoice(
        self, customer_id: str, line_items: List[LineItem]
    ) -> Invoice:
        """Create Stripe invoice."""
        _stripe_client=self._ensure_initialized()

        # Create invoice items
        for item in line_items:
            stripe_client.InvoiceItem.create(
                _customer=customer_id,
                _description = item.description,
                _quantity=int(item.quantity),
                _unit_amount=int(item.unit_price * 100),    # Stripe uses cents
                _currency=item.currency.lower(),
            )

        # Create and finalize invoice
        stripe_invoice = stripe_client.Invoice.create(
            _customer = customer_id,
            _auto_advance = True,
        )
        stripe_invoice.finalize_invoice()

        invoice = Invoice(
            _id=f"inv_{uuid.uuid4().hex[:12]}",
            _number = stripe_invoice.number or f"INV-{stripe_invoice.id}",
            _tenant_id = "",
            _external_id = stripe_invoice.id,
            _line_items = line_items,
            _total=Decimal(str(stripe_invoice.total / 100)),
            _amount_due=Decimal(str(stripe_invoice.amount_due / 100)),
            _currency=stripe_invoice.currency.upper(),
        )
        invoice.calculate_totals()

        return invoice

    async def process_payment(self, invoice_id: str, payment_method_id: str) -> Payment:
        """Process Stripe payment."""
        _stripe_client=self._ensure_initialized()

        try:
            stripe_invoice = stripe_client.Invoice.pay(
                invoice_id,
                _payment_method = payment_method_id,
            )

            return Payment(
                _id=f"pay_{uuid.uuid4().hex[:12]}",
                _invoice_id = invoice_id,
                _tenant_id = "",
                _amount=Decimal(str(stripe_invoice.amount_paid / 100)),
                _currency=stripe_invoice.currency.upper(),
                _status = PaymentStatus.COMPLETED,
                _external_id = stripe_invoice.payment_intent,
                _processed_at=datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error(f"Payment failed: {e}")
            return Payment(
                _id=f"pay_{uuid.uuid4().hex[:12]}",
                _invoice_id = invoice_id,
                _tenant_id = "",
                _amount=Decimal("0"),
                _status = PaymentStatus.FAILED,
                _metadata={"error": str(e)},
            )

    def verify_webhook(self, payload: bytes, signature: str) -> bool:
        """Verify Stripe webhook signature."""
        _stripe_client=self._ensure_initialized()

        try:
            stripe_client.Webhook.construct_event(
                payload, signature, self.config.webhook_secret
            )
            return True
        except Exception as e:
            logger.error(f"Webhook verification failed: {e}")
            return False


# =============================================================================
# Billing Manager
# =============================================================================
class BillingManager:
    """
    Main billing manager coordinating all billing operations.

    Features:
    - Multi-provider support
    - Usage metering integration
    - Invoice generation
    - Payment processing
    - Webhook handling
    - Dunning management
    """

    def __init__(self, config: Optional[BillingConfig] = None) -> None:
        self.config=config or BillingConfig()
        self._provider: Optional[BillingProviderInterface] = None
        self._tax_rules: Dict[str, TaxRule] = {}
        self._credits: Dict[str, List[Credit]] = {}    # tenant_id -> credits
        self._subscriptions: Dict[str, Subscription] = {}    # tenant_id -> subscription
        self._invoices: Dict[str, List[Invoice]] = {}    # tenant_id -> invoices
        self._webhook_handlers: Dict[str, List[Callable[[WebhookEvent], None]]] = {}
        self._lock=threading.Lock()
        self._initialized = False

        # Metrics
        self._metrics: Dict[str, Any] = {
            "invoices_created": 0,
            "payments_processed": 0,
            "total_revenue": Decimal("0"),
            "webhooks_received": 0,
        }

    def initialize(self) -> None:
        """Initialize billing manager with configured provider."""
        if self._initialized:
            return

        if self.config.provider == BillingProvider.INTERNAL:
            self._provider=InternalBillingProvider(self.config)
        elif self.config.provider == BillingProvider.STRIPE:
            self._provider=StripeBillingProvider(self.config)
        else:
            logger.warning(
                f"Unsupported provider: {self.config.provider}, using internal"
            )
            self._provider=InternalBillingProvider(self.config)

        self._initialized = True
        logger.info(
            f"Billing manager initialized with provider: {self.config.provider.value}"
        )

    # -------------------------------------------------------------------------
    # Tax Management
    # -------------------------------------------------------------------------

    def add_tax_rule(self, rule: TaxRule) -> None:
        """Add tax calculation rule."""
        self._tax_rules[rule.id] = rule
        logger.info(f"Added tax rule: {rule.name} ({rule.rate}% for {rule.country})")

    def get_applicable_tax(
        self, country: str, region: Optional[str] = None, category: Optional[str] = None
    ) -> Optional[TaxRule]:
        """Get applicable tax rule for location and category."""
        for rule in self._tax_rules.values():
            if not rule.active:
                continue
            if rule.country != country:
                continue
            if rule.region and rule.region != region:
                continue
            if rule.applies_to and category and category not in rule.applies_to:
                continue
            return rule
        return None

    # -------------------------------------------------------------------------
    # Credit Management
    # -------------------------------------------------------------------------

    def add_credit(
        self,
        tenant_id: str,
        amount: Decimal,
        credit_type: CreditType = CreditType.PROMOTIONAL,
        description: str = "",
        expires_in_days: Optional[int] = None,
    ) -> Credit:
        """Add credit to tenant account."""
        _credit_id=f"cred_{uuid.uuid4().hex[:12]}"
        expires_at = None
        if expires_in_days:
            _expires_at=datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        credit = Credit(
            _id=credit_id,
            _tenant_id=tenant_id,
            _amount=amount,
            _remaining = amount,
            _credit_type = credit_type,
            _description = description,
            _expires_at = expires_at,
        )

        with self._lock:
            if tenant_id not in self._credits:
                self._credits[tenant_id] = []
            self._credits[tenant_id].append(credit)

        logger.info(f"Added {amount} credit to tenant {tenant_id}")
        return credit

    def get_credit_balance(self, tenant_id: str) -> Decimal:
        """Get available credit balance for tenant."""
        _credits=self._credits.get(tenant_id, [])
        return sum((c.remaining for c in credits if c.is_valid), Decimal("0"))

    def apply_credits(self, tenant_id: str, amount: Decimal) -> Decimal:
        """Apply credits to reduce amount. Returns remaining amount."""
        credits = sorted(
            [c for c in self._credits.get(tenant_id, []) if c.is_valid],
            _key=lambda c: c.expires_at or datetime.max.replace(tzinfo=timezone.utc),
        )

        remaining = amount
        for credit in credits:
            if remaining <= 0:
                break

            if credit.remaining >= remaining:
                credit.remaining -= remaining
                _remaining=Decimal("0")
            else:
                remaining -= credit.remaining
                credit.remaining=Decimal("0")

        return remaining

    # -------------------------------------------------------------------------
    # Customer Management
    # -------------------------------------------------------------------------

    async def create_customer(
        self,
        tenant_id: str,
        email: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create customer in billing system."""
        self.initialize()
        assert self._provider is not None
        return await self._provider.create_customer(
            tenant_id, email, name, metadata or {}
        )

    # -------------------------------------------------------------------------
    # Subscription Management
    # -------------------------------------------------------------------------

    async def create_subscription(
        self, tenant_id: str, customer_id: str, plan_id: str, trial_days: int = 0
    ) -> Subscription:
        """Create subscription for tenant."""
        self.initialize()
        assert self._provider is not None

        subscription = await self._provider.create_subscription(
            customer_id, plan_id, trial_days
        )
        subscription.tenant_id = tenant_id

        with self._lock:
            self._subscriptions[tenant_id] = subscription

        logger.info(f"Created subscription for tenant {tenant_id}: {subscription.id}")
        return subscription

    async def cancel_subscription(
        self, tenant_id: str, at_period_end: bool = True
    ) -> bool:
        """Cancel tenant subscription."""
        self.initialize()
        assert self._provider is not None

        _subscription=self._subscriptions.get(tenant_id)
        if not subscription:
            return False

        external_id = subscription.external_id or subscription.id
        _result=await self._provider.cancel_subscription(external_id, at_period_end)

        if result:
            subscription.cancel_at_period_end = at_period_end
            if not at_period_end:
                subscription.status = SubscriptionStatus.CANCELLED
                subscription.cancelled_at=datetime.now(timezone.utc)

        return result

    def get_subscription(self, tenant_id: str) -> Optional[Subscription]:
        """Get tenant's current subscription."""
        return self._subscriptions.get(tenant_id)

    # -------------------------------------------------------------------------
    # Invoice Management
    # -------------------------------------------------------------------------

    async def create_invoice(
        self,
        tenant_id: str,
        customer_id: str,
        line_items: List[LineItem],
        apply_credits: bool = True,
    ) -> Invoice:
        """Create invoice for tenant."""
        self.initialize()
        assert self._provider is not None

        _invoice=await self._provider.create_invoice(customer_id, line_items)
        invoice.tenant_id = tenant_id

        # Apply credits if enabled
        if apply_credits:
            _credit_balance=self.get_credit_balance(tenant_id)
            if credit_balance > 0:
                _applied=min(credit_balance, invoice.amount_due)
                invoice.amount_due=self.apply_credits(tenant_id, invoice.amount_due)
                invoice.amount_paid += applied
                invoice.metadata["credits_applied"] = str(applied)

        with self._lock:
            if tenant_id not in self._invoices:
                self._invoices[tenant_id] = []
            self._invoices[tenant_id].append(invoice)
            self._metrics["invoices_created"] += 1

        logger.info(f"Created invoice {invoice.number} for tenant {tenant_id}")
        return invoice

    def get_invoices(
        self, tenant_id: str, status: Optional[InvoiceStatus] = None
    ) -> List[Invoice]:
        """Get tenant invoices."""
        _invoices=self._invoices.get(tenant_id, [])
        if status:
            invoices = [inv for inv in invoices if inv.status == status]
        return invoices

    # -------------------------------------------------------------------------
    # Payment Processing
    # -------------------------------------------------------------------------

    async def process_payment(
        self, tenant_id: str, invoice_id: str, payment_method_id: str
    ) -> Payment:
        """Process payment for invoice."""
        self.initialize()
        assert self._provider is not None

        _payment=await self._provider.process_payment(invoice_id, payment_method_id)
        payment.tenant_id = tenant_id

        with self._lock:
            self._metrics["payments_processed"] += 1
            if payment.status == PaymentStatus.COMPLETED:
                self._metrics["total_revenue"] += payment.amount

        logger.info(f"Processed payment {payment.id}: {payment.status.value}")
        return payment

    # -------------------------------------------------------------------------
    # Webhook Handling
    # -------------------------------------------------------------------------

    def register_webhook_handler(
        self, event_type: str, handler: Callable[[WebhookEvent], None]
    ) -> None:
        """Register webhook event handler."""
        if event_type not in self._webhook_handlers:
            self._webhook_handlers[event_type] = []
        self._webhook_handlers[event_type].append(handler)

    async def handle_webhook(
        self,
        provider: BillingProvider,
        event_type: str,
        payload: Dict[str, Any],
        signature: str,
    ) -> bool:
        """Handle incoming webhook."""
        self.initialize()
        assert self._provider is not None

        # Verify signature
        _payload_bytes=json.dumps(payload, separators=(", ", ":")).encode()
        if not self._provider.verify_webhook(payload_bytes, signature):
            logger.warning(f"Invalid webhook signature for {event_type}")
            return False

        event = WebhookEvent(
            _id=f"evt_{uuid.uuid4().hex[:12]}",
            _provider = provider,
            _event_type=event_type,
            _payload = payload,
            _signature = signature,
        )

        # Process handlers
        _handlers=self._webhook_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Webhook handler error: {e}")

        event.processed = True
        event.processed_at=datetime.now(timezone.utc)

        with self._lock:
            self._metrics["webhooks_received"] += 1

        logger.info(f"Processed webhook: {event_type}")
        return True

    # -------------------------------------------------------------------------
    # Reporting
    # -------------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        """Get billing metrics."""
        with self._lock:
            return {
                "invoices_created": self._metrics["invoices_created"],
                "payments_processed": self._metrics["payments_processed"],
                "total_revenue": str(self._metrics["total_revenue"]),
                "webhooks_received": self._metrics["webhooks_received"],
                "active_subscriptions": len(
                    [
                        s
                        for s in self._subscriptions.values()
                        if s.status == SubscriptionStatus.ACTIVE
                    ]
                ),
                "total_credits_outstanding": str(
                    sum(self.get_credit_balance(tid) for tid in self._credits.keys())
                ),
            }

    def generate_revenue_report(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Generate revenue report for date range."""
        invoices = []
        for tenant_invoices in self._invoices.values():
            for inv in tenant_invoices:
                if start_date <= inv.issue_date <= end_date:
                    invoices.append(inv)

        _total_invoiced=sum(inv.total for inv in invoices)
        _total_collected=sum(inv.amount_paid for inv in invoices)
        _total_outstanding=sum(inv.amount_due for inv in invoices)

        return {
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "invoice_count": len(invoices),
            "total_invoiced": str(total_invoiced),
            "total_collected": str(total_collected),
            "total_outstanding": str(total_outstanding),
            "collection_rate": str(
                (total_collected / total_invoiced * 100)
                if total_invoiced > 0
                else Decimal("0")
            ),
        }


# =============================================================================
# Flask Integration
# =============================================================================
def create_billing_blueprint(billing_manager: BillingManager) -> Any:
    """Create Flask blueprint for billing endpoints."""
    try:
        from flask import Blueprint, request, jsonify, g

        _bp=Blueprint("billing", __name__, url_prefix="/api/billing")

        @bp.route("/webhook/<provider>", methods=["POST"])
        async def webhook_handler(provider: str) -> Any:
            """Handle billing webhooks."""
            try:
                _provider_enum=BillingProvider(provider)
            except ValueError:
                return jsonify({"error": "Unknown provider"}), 400

            _signature=request.headers.get("X-Signature", "")
            _payload=request.get_json() or {}
            _event_type=payload.get("type", "unknown")

            success = await billing_manager.handle_webhook(
                provider_enum, event_type, payload, signature
            )

            if success:
                return jsonify({"status": "processed"}), 200
            return jsonify({"error": "Verification failed"}), 400

        @bp.route("/invoices", methods=["GET"])

        def list_invoices() -> Any:
            """List invoices for current tenant."""
            _tenant_id=g.get("tenant_id", "default")
            _status_param=request.args.get("status")
            _status=InvoiceStatus(status_param) if status_param else None

            _invoices=billing_manager.get_invoices(tenant_id, status)
            return jsonify(
                {
                    "invoices": [inv.to_dict() for inv in invoices],
                    "count": len(invoices),
                }
            )

        @bp.route("/credits/balance", methods=["GET"])

        def credit_balance() -> Any:
            """Get credit balance for current tenant."""
            _tenant_id=g.get("tenant_id", "default")
            _balance=billing_manager.get_credit_balance(tenant_id)
            return jsonify(
                {
                    "tenant_id": tenant_id,
                    "balance": str(balance),
                    "currency": billing_manager.config.default_currency,
                }
            )

        @bp.route("/metrics", methods=["GET"])

        def billing_metrics() -> Any:
            """Get billing metrics."""
            return jsonify(billing_manager.get_metrics())

        return bp

    except ImportError:
        logger.warning("Flask not available for billing blueprint")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "BillingProvider",
    "InvoiceStatus",
    "PaymentStatus",
    "SubscriptionStatus",
    "BillingCycle",
    "CreditType",
    "TaxType",
    "BillingConfig",
    "TaxRule",
    "LineItem",
    "Invoice",
    "Payment",
    "Subscription",
    "Credit",
    "WebhookEvent",
    "BillingProviderInterface",
    "InternalBillingProvider",
    "StripeBillingProvider",
    "BillingManager",
    "create_billing_blueprint",
]
