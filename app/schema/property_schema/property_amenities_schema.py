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
# Property Amenity Create
# ============================================================

class PropertyAmenityCreate(BaseModel):
    """
    Assign an amenity to a property.
    """

    property_id: UUID

    amenity_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Property Amenity Update
# ============================================================

class PropertyAmenityUpdate(BaseModel):
    """
    Update a property-amenity mapping.
    """

    property_id: UUID | None = None

    amenity_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Property Amenity Response
# ============================================================

class PropertyAmenityResponse(BaseModel):
    """
    Property amenity mapping response.
    """

    id: UUID

    property_id: UUID

    amenity_id: UUID

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )