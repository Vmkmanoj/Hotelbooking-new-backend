# ============================================================
# Standard Library
# ============================================================

from app.models.review_models.review_model import Review
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
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

from app.common.enums.user_enums.user_status import (
    UserStatus,
)

if TYPE_CHECKING:
    from app.models.permissions_models.roles import Role
    from app.models.property_models.property import Property
    from app.models.favorites_models.favorites import Favorite
    from app.models.booking_models.booking import Booking
    from app.models.payment_models.payment import Payment


# ============================================================
# User Model
# ============================================================

class User(BaseTable):
    """
    Stores all registered users of the application.
    """

    __tablename__ = "users"

    # ============================================================
    # Authentication
    # ============================================================

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ============================================================
    # Profile Information
    # ============================================================

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ============================================================
    # User Status
    # ============================================================

    user_status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        nullable=False,
        default=UserStatus.ACTIVE,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Role
    # ============================================================

    role_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    role: Mapped["Role | None"] = relationship(
        back_populates="users",
        lazy="select",
    )

    # Properties owned by the user
    properties: Mapped[list["Property"]] = relationship(
        foreign_keys="Property.owner_id",
        back_populates="owner",
        lazy="select",
    )

    # Properties approved by the admin
    approved_properties: Mapped[list["Property"]] = relationship(
        foreign_keys="Property.approved_by",
        back_populates="approved_admin",
        lazy="select",
    )

    # User favourites
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # Customer bookings
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="customer",
        lazy="select",
    )

    reviews: Mapped[list["Review"]] = relationship(
    back_populates="customer",
    cascade="all, delete-orphan",
    lazy="select",
)

    # # Customer payments
    # payments: Mapped[list["Payment"]] = relationship(
    #     back_populates="paid_by_user",
    #     lazy="select",
    # )