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
    from app.models.property_models.property import Property


# ============================================================
# Property Image Model
# ============================================================

class PropertyImage(BaseTable):
    """
    Stores all images belonging to a property.
    """

    __tablename__ = "property_images"

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
    # Image Information
    # ============================================================

    image_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    caption: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_cover: Mapped[bool] = mapped_column(
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

    property: Mapped["Property"] = relationship(
        back_populates="property_images",
        lazy="select",
    )