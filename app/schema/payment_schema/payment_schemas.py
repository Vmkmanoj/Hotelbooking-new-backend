# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
from decimal import Decimal
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.payment_enums.payment_enums import (
    InvoiceStatus,
    PaymentGateway,
    PaymentMethod,
    PaymentStatus,
    RefundStatus,
)

# ============================================================
# Create Payment Request
# ============================================================

class CreatePaymentRequest(BaseModel):
    """
    Request schema for initiating a payment.
    """

    booking_id: UUID

    payment_method: PaymentMethod

    payment_gateway: PaymentGateway

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Verify Payment Request
# ============================================================

class VerifyPaymentRequest(BaseModel):
    """
    Request schema for verifying a payment.
    """

    gateway_transaction_id: str = Field(
        min_length=1,
        max_length=255,
    )

    gateway_response: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Refund Request
# ============================================================

class RefundRequest(BaseModel):
    """
    Request schema for processing a refund.
    """

    refund_amount: Decimal = Field(
        gt=0,
    )

    reason: str = Field(
        min_length=5,
        max_length=500,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Payment Gateway Response
# ============================================================

class PaymentGatewayResponse(BaseModel):
    """
    Response returned after payment initiation.
    """

    payment_reference: str

    payment_url: str

    expires_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Payment Summary Response
# ============================================================

class PaymentSummaryResponse(BaseModel):
    """
    Summary response for a payment.
    """

    id: UUID

    booking_id: UUID

    payment_reference: str

    amount: Decimal

    currency: str

    payment_method: PaymentMethod

    payment_gateway: PaymentGateway

    payment_status: PaymentStatus

    paid_at: datetime | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Payment Response
# ============================================================

class PaymentResponse(BaseModel):
    """
    Detailed payment response.
    """

    id: UUID

    booking_id: UUID

    payment_reference: str

    amount: Decimal

    currency: str

    payment_method: PaymentMethod

    payment_gateway: PaymentGateway

    payment_status: PaymentStatus

    gateway_transaction_id: str | None

    gateway_response: str | None

    refund_status: RefundStatus

    refund_amount: Decimal

    paid_at: datetime | None

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Invoice Response
# ============================================================

class InvoiceResponse(BaseModel):
    """
    Invoice response.
    """

    id: UUID

    booking_id: UUID

    invoice_number: str

    invoice_status: InvoiceStatus

    invoice_amount: Decimal

    currency: str

    generated_at: datetime

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Revenue Summary Response
# ============================================================

class RevenueSummaryResponse(BaseModel):
    """
    Revenue summary for a property owner.
    """

    total_payments: int

    total_revenue: Decimal

    total_refunds: Decimal

    net_revenue: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )