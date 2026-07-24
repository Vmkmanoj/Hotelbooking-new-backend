# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    ForeignKey,
    Integer,
    Text,
    DateTime,
)

from sqlalchemy.dialects.postgresql import (
    UUID as PG_UUID,
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

if TYPE_CHECKING:
    from app.models.booking_models.booking import Booking
    from app.models.users_models.users import User
    from app.models.property_models.property import Property


# ============================================================
# Review Model
# ============================================================

class Review(BaseTable):
    """
    Stores customer reviews for completed bookings.

    One Booking  -> One Review
    One Property -> Many Reviews
    One Customer -> Many Reviews
    """

    __tablename__ = "reviews"

    # ============================================================
    # Foreign Keys
    # ============================================================

    booking_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "bookings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    property_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "properties.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Review Details
    # ============================================================

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    owner_reply: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    owner_replied_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    booking: Mapped["Booking"] = relationship(
        back_populates="review",
        lazy="select",
    )

    property: Mapped["Property"] = relationship(
        back_populates="reviews",
        lazy="select",
    )

    customer: Mapped["User"] = relationship(
        back_populates="reviews",
        lazy="select",
    )