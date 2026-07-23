# ============================================================
# Standard Library
# ============================================================

from typing import TYPE_CHECKING

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import (
    Boolean,
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
    from app.models.users_models.users import User
    from app.models.permissions_models.roles_permission import (
        RolePermission,
    )

# ============================================================
# Role Model
# ============================================================

class Role(BaseTable):
    """
    Stores system roles.
    Example:
    - Super Admin
    - Admin
    - Owner
    - Customer
    """

    __tablename__ = "roles"

    # ============================================================
    # Role Information
    # ============================================================

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )