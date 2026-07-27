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
# Local Imports
# ============================================================

from app.common.enums.property_enums.amenity_category import (
    AmenityCategory,
)

# ============================================================
# Amenity Base
# ============================================================

class AmenityBase(BaseModel):
    """
    Base schema shared by Amenity Create, Update and Response.
    """

    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    category: AmenityCategory


# ============================================================
# Amenity Create
# ============================================================

class AmenityCreate(AmenityBase):
    """
    Request schema for creating a new amenity.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Amenity Update
# ============================================================

class AmenityUpdate(BaseModel):
    """
    Request schema for updating an amenity.

    All fields are optional to support PATCH updates.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    category: AmenityCategory | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Amenity Response
# ============================================================

class AmenityResponse(AmenityBase):
    """
    Amenity response returned to the client.
    """

    id: UUID

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )