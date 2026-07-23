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
# Customer Registration
# ============================================================

class CustomerRegister(BaseModel):
    """
    Customer registration request.
    """

    user_name: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# ============================================================
# Property Owner Registration
# ============================================================

class PropertyRegister(BaseModel):
    """
    Property owner registration request.
    """

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    avatar_url: str | None = None


# ============================================================
# Registration Response
# ============================================================

class RegisterResponse(BaseModel):
    """
    Registration response.
    """

    success: bool

    message: str

    model_config = ConfigDict(
        from_attributes=True,
    )