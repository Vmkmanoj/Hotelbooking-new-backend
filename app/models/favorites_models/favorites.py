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
    from app.models.users_models.users import User
    from app.models.property_models.property import Property


# ============================================================
# Favorite Model
# ============================================================

class Favorite(BaseTable):
    """
    Stores properties bookmarked by users.

    One User -> Many Favorites
    One Property -> Many Favorites
    """

    __tablename__ = "favorites"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "property_id",
            name="uq_user_property_favorite",
        ),
    )
    # ============================================================
    # Foreign Keys
    # ============================================================

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

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
    # Relationships
    # ============================================================

    user: Mapped["User"] = relationship(
        back_populates="favorites",
        lazy="select",
    )

    property: Mapped["Property"] = relationship(
        back_populates="favorites",
        lazy="select",
    )