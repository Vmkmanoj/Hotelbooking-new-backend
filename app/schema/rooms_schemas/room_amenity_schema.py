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
# Room Amenity Base
# ============================================================

class RoomAmenityBase(BaseModel):
    """
    Maps amenities to a room type.
    """

    room_type_id: UUID

    amenity_id: UUID


# ============================================================
# Create
# ============================================================

class RoomAmenityCreate(RoomAmenityBase):

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Update
# ============================================================

class RoomAmenityUpdate(BaseModel):

    room_type_id: UUID | None = None

    amenity_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomAmenityResponse(RoomAmenityBase):

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )