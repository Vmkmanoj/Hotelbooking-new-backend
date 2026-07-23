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
    Field,
)


# ============================================================
# Permission Base
# ============================================================

class PermissionBase(BaseModel):
    """
    Base schema for permissions.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    modules: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )


# ============================================================
# Create
# ============================================================

class PermissionCreate(PermissionBase):
    pass


# ============================================================
# Update
# ============================================================

class PermissionUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    modules: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )


# ============================================================
# Response
# ============================================================

class PermissionResponse(PermissionBase):

    id: UUID

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )