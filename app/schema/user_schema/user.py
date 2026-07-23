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
    EmailStr,
    Field,
)

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.user_enums.user_status import (
    UserStatus,
)


# ============================================================
# User Base
# ============================================================

class UserBase(BaseModel):
    """
    Base schema for users.
    """

    email: EmailStr

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    avatar_url: str | None = None

    role_id: UUID


# ============================================================
# Create
# ============================================================

class UserCreate(UserBase):

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# ============================================================
# Update
# ============================================================

class UserUpdate(BaseModel):

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    avatar_url: str | None = None

    role_id: UUID | None = None

    user_status: UserStatus | None = None


# ============================================================
# Response
# ============================================================

class UserResponse(UserBase):

    id: UUID

    user_status: UserStatus

    last_login_at: datetime | None = None

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )