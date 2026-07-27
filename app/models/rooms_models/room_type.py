# ============================================================
# Standard Library
# ============================================================

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
    
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
    from app.models.property_models.property import Property
    from app.models.rooms_models.room import Room
    from app.models.rooms_models.room_amenity import RoomAmenity
    from app.models.rooms_models.room_image import RoomImage


# ============================================================
# Room Type Model
# ============================================================

class RoomType(BaseTable):
    """
    Represents a category of rooms inside a property.

    Examples:
    - Standard Room
    - Deluxe Room
    - Executive Room
    - Suite
    - Family Room
    """

    __tablename__ = "room_types"

    __table_args__ = (
        UniqueConstraint(
            "property_id",
            "room_name",
            name="uq_property_room_type",
        ),
        CheckConstraint(
            "max_adults > 0",
            name="ck_room_type_max_adults",
        ),
        CheckConstraint(
            "max_children >= 0",
            name="ck_room_type_max_children",
        ),
    )

    # ============================================================
    # Foreign Keys
    # ============================================================

    property_id: Mapped[UUID] = mapped_column(
       
        ForeignKey(
            "properties.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Room Type Information
    # ============================================================

    room_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    max_adults: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_children: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    base_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    room_size_sqm: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 2),
        nullable=True,
    )

    # Example:
    # {
    #     "KING": 1,
    #     "SOFA_BED": 1
    # }

    bed_configuration: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    property: Mapped["Property"] = relationship(
        back_populates="room_types",
        
    )

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="room_type",
        cascade="all, delete-orphan",
    )

    room_images: Mapped[list["RoomImage"]] = relationship(
        back_populates="room_type",
        cascade="all, delete-orphan",
    )

    room_amenities: Mapped[list["RoomAmenity"]] = relationship(
        back_populates="room_type",
        cascade="all, delete-orphan",
    )