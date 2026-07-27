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
    from app.models.review_models.review_model import Review


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
        unique=True,
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

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    role: Mapped["Role | None"] = relationship(
        back_populates="users",
        
    )

    # Properties owned by the user
    properties: Mapped[list["Property"]] = relationship(
        foreign_keys="Property.owner_id",
        back_populates="owner",
        
    )

    # Properties approved by the admin
    approved_properties: Mapped[list["Property"]] = relationship(
        foreign_keys="Property.approved_by",
        back_populates="approved_admin",
        
    )

    # User favourites
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        
    )

    # Customer bookings
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="customer",
        
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",       
    )

    # Customer payments
    payments: Mapped[list["Payment"]] = relationship(
        foreign_keys="Payment.user_id",
        back_populates="paid_by_user",
    )


    