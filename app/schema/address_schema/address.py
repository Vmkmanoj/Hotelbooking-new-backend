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
# Address Base
# ============================================================

class AddressBase(BaseModel):
    """
    Base schema shared by Address Create, Update and Response.
    """

    address_line_1: str = Field(
        min_length=3,
        max_length=255,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    country: str = Field(
        min_length=2,
        max_length=100,
    )

    postal_code: str = Field(
        min_length=3,
        max_length=20,
    )


# ============================================================
# Address Create
# ============================================================

class AddressCreate(AddressBase):
    """
    Request schema for creating an address.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Address Update
# ============================================================

class AddressUpdate(BaseModel):
    """
    Request schema for updating an address.

    Supports partial updates.
    """

    address_line_1: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Address Response
# ============================================================

class AddressResponse(AddressBase):
    """
    Address response returned to the client.
    """

    id: UUID

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )