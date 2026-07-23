# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
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
    from app.models.rooms_models.room_type import RoomType
    from app.models.property_models.amenities import Amenity


# ============================================================
# Room Amenity Model
# ============================================================

class RoomAmenity(BaseTable):
    """
    Junction table between Room Types and Amenities.

    One Room Type -> Many Amenities
    One Amenity -> Many Room Types
    """

    __tablename__ = "room_amenities"

    __table_args__ = (
        UniqueConstraint(
            "room_type_id",
            "amenity_id",
            name="uq_room_type_amenity",
        ),
    )

    # ============================================================
    # Foreign Keys
    # ============================================================

    room_type_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "room_types.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    amenity_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "amenities.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    room_type: Mapped["RoomType"] = relationship(
        back_populates="room_amenities",
        lazy="select",
    )

    amenity: Mapped["Amenity"] = relationship(
        back_populates="room_amenities",
        lazy="select",
    )