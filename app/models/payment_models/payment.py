# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

# ============================================================
# Local Imports
# ============================================================

from app.database.base_table import BaseTable

from app.common.enums.payment_enums.payment_enums import (
    PaymentGateway,
    PaymentMethod,
    PaymentStatus,
    RefundStatus,
)

if TYPE_CHECKING:
    from app.models.booking_models.booking import Booking
    from app.models.users_models.users import User

# ============================================================
# Payment Model
# ============================================================

class Payment(BaseTable):
    """
    Represents a payment transaction for a booking.
    """

    __tablename__ = "payments"

    # ============================================================
    # Booking Reference
    # ============================================================

    booking_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "bookings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Payment Information
    # ============================================================

    payment_reference: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
    )

    # ============================================================
    # Payment Method
    # ============================================================

    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(
            PaymentMethod,
            name="payment_method_enum",
        ),
        nullable=False,
    )

    payment_gateway: Mapped[PaymentGateway] = mapped_column(
        Enum(
            PaymentGateway,
            name="payment_gateway_enum",
        ),
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            name="payment_status_enum",
        ),
        nullable=False,
        default=PaymentStatus.PENDING,
        index=True,
    )

    # ============================================================
    # Gateway Information
    # ============================================================

    gateway_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ============================================================
    # Refund Information
    # ============================================================

    refund_status: Mapped[RefundStatus] = mapped_column(
        Enum(
            RefundStatus,
            name="refund_status_enum",
        ),
        nullable=False,
        default=RefundStatus.NOT_APPLICABLE,
    )

    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    # ============================================================
    # Payment Time
    # ============================================================

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    booking: Mapped["Booking"] = relationship(
        back_populates="payments",
    )

    # paid_by_user : Mapped["User"] = relationship(
    #     back_populates="payments"
    # )