# ============================================================
# Third Party
# ============================================================

from uuid import UUID
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from app.common.enums.user_enums.role_name import RoleName


# ============================================================
# Login Request
# ============================================================

class LoginRequest(BaseModel):
    """
    Login request.
    """

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# ============================================================
# Logged-in User
# ============================================================

class LoginUser(BaseModel):
    """
    Logged-in user details.
    """

    id: UUID

    email: EmailStr

    first_name: str

    last_name: str | None = None

    role: RoleName

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Login Response
# ============================================================

class LoginResponse(BaseModel):
    """
    Login response.
    """

    success: bool

    message: str

    access_token: str

    token_type: str = "bearer"

    role: RoleName | None = None

    user: LoginUser | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )