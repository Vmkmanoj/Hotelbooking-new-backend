# ============================================================
# Standard Library
# ============================================================

from decimal import Decimal
from uuid import UUID
from datetime import datetime

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

    name: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    max_occupancy: int = Field(
        ge=1,
        le=20,
    )

    base_price: Decimal = Field(
        gt=0,
    )

    size_sqm: Decimal | None = Field(
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

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    max_occupancy: int | None = Field(
        default=None,
        ge=1,
        le=20,
    )

    base_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    size_sqm: Decimal | None = Field(
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

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )