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
    from app.models.permissions_models.roles import Role
    from app.models.permissions_models.permissions import Permission


# ============================================================
# Role Permission Model
# ============================================================

class RolePermission(BaseTable):
    """
    Maps Roles to Permissions.

    Each role can have multiple permissions.
    Each permission can belong to multiple roles.
    """

    __tablename__ = "role_permissions"

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission",
        ),
    )

    # ============================================================
    # Foreign Keys
    # ============================================================

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    role: Mapped["Role"] = relationship(
        back_populates="role_permissions",
        lazy="select",
    )

    permission: Mapped["Permission"] = relationship(
        back_populates="role_permissions",
        lazy="select",
    )