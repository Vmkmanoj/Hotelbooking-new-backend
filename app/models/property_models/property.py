# ============================================================
# Standard Library
# ============================================================


from datetime import (
    datetime,
    time,
)

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

# ============================================================
# Local Imports
# ============================================================

from app.database.base_table import BaseTable

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)
from app.common.enums.property_enums.property_type import PropertyType


if TYPE_CHECKING:
    from app.models.users_models.users import User
    from app.models.property_models.address import Address
    from app.models.favorites_models.favorites import Favorite
    from app.models.rooms_models.room import Room
    from app.models.rooms_models.room_type import RoomType
    from app.models.property_models.property_amenity import (
        PropertyAmenity,
    )
    from app.models.property_models.property_image import (
        PropertyImage,
    )
    from app.models.booking_models.booking import Booking
    from app.models.review_models.review_model import Review



class Property(BaseTable):
    __tablename__ = "properties"

    __table_args__ = (
        CheckConstraint(
            "(star_rating IS NULL) OR (star_rating BETWEEN 1 AND 5)",
            name="ck_property_star_rating",
        ),
        CheckConstraint(
            "avg_rating >= 0 AND avg_rating <= 5",
            name="ck_property_avg_rating",
        ),
    )
    
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    address_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "addresses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    approved_by: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    property_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    property_type: Mapped[PropertyType] = mapped_column(
        Enum(
            PropertyType,
            name="propertytype",
        ),
        nullable=False,
    )

    star_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    contact_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    contact_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    cancellation_policy: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    house_rules: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    child_policy: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pet_policy: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    smoking_policy: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    
    status: Mapped[PropertyStatus] = mapped_column(
        Enum(PropertyStatus),
        nullable=False,
        default=PropertyStatus.PENDING,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    avg_rating: Mapped[Decimal] = mapped_column(
        Numeric(2, 1),
        default=Decimal("0.0"),
        nullable=False,
    )

    total_reviews: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    check_in_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    check_out_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    approval_remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    

    # -----------------------
    # Relationships
    # -----------------------

    owner: Mapped["User"] = relationship(
        foreign_keys=[owner_id],
        back_populates="properties",
    )

    approved_admin: Mapped["User | None"] = relationship(
        foreign_keys=[approved_by],
        back_populates="approved_properties",
    )

    address: Mapped["Address"] = relationship(
        back_populates="property",
        uselist=False,
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
    )

    

    property_amenities: Mapped[list["PropertyAmenity"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
    )

    property_images: Mapped[list["PropertyImage"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="property",

    )

    room_types: Mapped[list["RoomType"]] = relationship(
        back_populates="property",
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        
    )


    
        
