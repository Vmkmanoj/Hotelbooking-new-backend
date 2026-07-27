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
    CheckConstraint,
    ForeignKey,
    Integer,
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

if TYPE_CHECKING:
    from app.models.rooms_models.room_type import RoomType


# ============================================================
# Room Image Model
# ============================================================

class RoomImage(BaseTable):
    """
    Stores images for a Room Type.

    Example:
    Deluxe Room
        ├── Image 1
        ├── Image 2
        └── Image 3
    """

    __tablename__ = "room_images"

    __table_args__ = (
        CheckConstraint(
            "display_order > 0",
            name="ck_room_image_display_order",
        ),
    )

    # ============================================================
    # Foreign Key
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
    # Image Information
    # ============================================================

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    caption: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        index=True,
    )

    is_cover: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    room_type: Mapped["RoomType"] = relationship(
        back_populates="room_images",
    )