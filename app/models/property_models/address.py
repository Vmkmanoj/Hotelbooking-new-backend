# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
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
# Address Model
# ============================================================

class Address(BaseTable):
    """
    Stores the physical location of a property.
    """

    __tablename__ = "addresses"

    # ============================================================
    # Address Information
    # ============================================================

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    property: Mapped["Property"] = relationship(
        back_populates="address",
        uselist=False,
        lazy="select",
    )