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
    UniqueConstraint
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
    from app.models.property_models.amenities import Amenity


# ============================================================
# Property Amenity Model
# ============================================================

class PropertyAmenity(BaseTable):
    """
    Junction table between Property and Amenity.
    """

    __tablename__ = "property_amenities"

    __table_args__ = (
        UniqueConstraint(
            "property_id",
            "amenity_id",
            name="uq_property_amenity",
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

    amenity_id: Mapped[UUID] = mapped_column(
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

    property: Mapped["Property"] = relationship(
        back_populates="property_amenities",
        lazy="select",
    )

    amenity: Mapped["Amenity"] = relationship(
        back_populates="property_amenities",
        lazy="select",
    )