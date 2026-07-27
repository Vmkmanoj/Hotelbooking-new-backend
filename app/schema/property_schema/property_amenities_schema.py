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
    Request schema for assigning an amenity to a property.
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
    Request schema for updating a property-amenity mapping.

    All fields are optional to support PATCH updates.
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
    Property amenity mapping returned to the client.
    """

    id: UUID

    property_id: UUID

    amenity_id: UUID

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )