# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
from decimal import Decimal
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
# Room Type Base
# ============================================================

class RoomTypeBase(BaseModel):
    """
    Base schema for Room Types.
    """

    property_id: UUID

    room_name: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    max_adults: int = Field(
        ge=1,
    )

    max_children: int = Field(
        ge=0,
    )

    base_price: Decimal = Field(
        gt=0,
    )

    room_size_sqm: Decimal | None = Field(
        default=None,
        gt=0,
    )

    bed_configuration: dict[str, int] | None = None


# ============================================================
# Create
# ============================================================

class RoomTypeCreate(RoomTypeBase):

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Update
# ============================================================

class RoomTypeUpdate(BaseModel):

    room_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    max_adults: int | None = Field(
        default=None,
        ge=1,
    )

    max_children: int | None = Field(
        default=None,
        ge=0,
    )

    base_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    room_size_sqm: Decimal | None = Field(
        default=None,
        gt=0,
    )

    bed_configuration: dict[str, int] | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomTypeResponse(RoomTypeBase):

    id: UUID

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )