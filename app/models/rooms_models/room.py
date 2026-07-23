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
    String,
    UniqueConstraint,
    Enum,
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

from app.common.enums.room_enums.room_status import (
    RoomStatus,
)

if TYPE_CHECKING:
    from app.models.rooms_models.room_type import RoomType
    from app.models.rooms_models.room_image import RoomImage
    from app.models.booking_models.booking_room import BookingRoom
    from app.models.property_models.property import Property


# ============================================================
# Room Model
# ============================================================

class Room(BaseTable):
    """
    Represents an individual physical room inside a property.

    Examples:
    - Room 101
    - Room 102
    - Room 201
    """

    __tablename__ = "rooms"

    __table_args__ = (
        UniqueConstraint(
            "room_type_id",
            "room_number",
            name="uq_room_type_room_number",
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

    # ============================================================
    # Room Information
    # ============================================================

    room_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    floor: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    status: Mapped[RoomStatus] = mapped_column(
        Enum(RoomStatus),
        default=RoomStatus.AVAILABLE,
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    room_type: Mapped["RoomType"] = relationship(
        back_populates="rooms",
        lazy="select",
    )

    images: Mapped[list["RoomImage"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="select",
    )

    booking_rooms: Mapped[list["BookingRoom"]] = relationship(
        back_populates="room",
        lazy="select",
    )

    property_id: Mapped[UUID] = mapped_column(
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    property: Mapped["Property"] = relationship(
        back_populates="rooms"
    )