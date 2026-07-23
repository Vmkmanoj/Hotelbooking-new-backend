# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    String,
    Text,
)

from sqlalchemy import Enum

from app.common.enums.property_enums.amenity_category import (
    AmenityCategory,
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
    from app.models.property_models.property_amenity import (
        PropertyAmenity,
    )
    from app.models.rooms_models.room_amenity import RoomAmenity


# ============================================================
# Amenity Model
# ============================================================

class Amenity(BaseTable):
    """
    Master table storing available amenities.
    """

    __tablename__ = "amenities"

    # ============================================================
    # Amenity Information
    # ============================================================

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    
    category: Mapped[AmenityCategory] = mapped_column(
        Enum(AmenityCategory),
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    property_amenities: Mapped[list["PropertyAmenity"]] = relationship(
        back_populates="amenity",
        cascade="all, delete-orphan",
        lazy="select",
    )

    room_amenities: Mapped[list["RoomAmenity"]] = relationship(
    back_populates="amenity",
    cascade="all, delete-orphan",
    lazy="select",
)