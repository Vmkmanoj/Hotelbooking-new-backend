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

    id: str

    email: EmailStr

    first_name: str

    last_name: str | None = None

    role: str

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

    role: str | None = None

    user: LoginUser | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )