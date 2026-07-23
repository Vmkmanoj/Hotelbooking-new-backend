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
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
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
    from app.models.property_models.property import Property
    from app.models.rooms_models.room import Room
    from app.models.rooms_models.room_amenity import RoomAmenity


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

    # ============================================================
    # Foreign Keys
    # ============================================================

    property_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
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

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    max_occupancy: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    base_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    size_sqm: Mapped[Decimal | None] = mapped_column(
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
        lazy="select",
    )

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="room_type",
        cascade="all, delete-orphan",
        lazy="select",
    )

    room_amenities: Mapped[list["RoomAmenity"]] = relationship(
        back_populates="room_type",
        cascade="all, delete-orphan",
        lazy="select",
    )