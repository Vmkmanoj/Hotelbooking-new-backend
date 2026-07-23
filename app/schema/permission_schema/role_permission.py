# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from pydantic import (
    BaseModel,
    ConfigDict,
)


# ============================================================
# Base
# ============================================================

class RolePermissionBase(BaseModel):
    """
    Role ↔ Permission mapping.
    """

    role_id: UUID

    permission_id: UUID


# ============================================================
# Create
# ============================================================

class RolePermissionCreate(RolePermissionBase):
    pass


# ============================================================
# Response
# ============================================================

class RolePermissionResponse(RolePermissionBase):

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )