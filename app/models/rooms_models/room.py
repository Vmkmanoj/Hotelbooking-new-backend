# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Enum,
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
    from app.models.booking_models.booking_room import BookingRoom
    


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
            name="uq_property_room_number",
        ),
        CheckConstraint(
            "length(trim(room_number)) > 0",
            name="ck_room_number_not_empty",
        ),
    )
    # ============================================================
    # Foreign Keys
    # ============================================================

    
    room_type_id: Mapped[UUID] = mapped_column(
        
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

    room_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=False,
    )

    floor: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[RoomStatus] = mapped_column(
        Enum(RoomStatus),
        default=RoomStatus.AVAILABLE,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    # ============================================================
    # Relationships
    # ============================================================

    room_type: Mapped["RoomType"] = relationship(
        back_populates="rooms",
        
    )

    

    booking_rooms: Mapped[list["BookingRoom"]] = relationship(
        back_populates="room",
        
    )

    
    