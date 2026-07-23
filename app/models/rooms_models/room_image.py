# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
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

from app.common.enums.room_enums.room_image_type import (
    RoomImageType,
)

if TYPE_CHECKING:
    from app.models.rooms_models.room import Room


# ============================================================
# Room Image Model
# ============================================================

class RoomImage(BaseTable):
    """
    Stores images for an individual room.

    A room can have multiple images.
    One image can be marked as the primary image.
    """

    __tablename__ = "room_images"

    # ============================================================
    # Foreign Keys
    # ============================================================

    room_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "rooms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Image Information
    # ============================================================

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    image_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    image_type: Mapped[RoomImageType] = mapped_column(
        Enum(RoomImageType),
        default=RoomImageType.ROOM,
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    room: Mapped["Room"] = relationship(
        back_populates="images",
        lazy="select",
    )