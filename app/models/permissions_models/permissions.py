# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    String,
    Text,
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
    from app.models.permissions_models.roles_permission import (
        RolePermission,
    )


# ============================================================
# Permission Model
# ============================================================

class Permission(BaseTable):
    """
    Stores all system permissions.

    Example:
    - property:create
    - property:update
    - booking:view
    - payment:refund
    """

    __tablename__ = "permissions"

    # ============================================================
    # Permission Information
    # ============================================================

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
        lazy="select",
    )