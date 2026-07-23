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
# Room Image Base
# ============================================================

class RoomImageBase(BaseModel):
    """
    Base schema for room images.
    """

    room_id: UUID

    image_url: str = Field(
        min_length=5,
        max_length=500,
    )

    image_name: str | None = Field(
        default=None,
        max_length=255,
    )

    is_primary: bool = False


# ============================================================
# Create
# ============================================================

class RoomImageCreate(RoomImageBase):
    """
    Upload a room image.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Update
# ============================================================

class RoomImageUpdate(BaseModel):
    """
    Update room image details.
    """

    image_url: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    image_name: str | None = Field(
        default=None,
        max_length=255,
    )

    is_primary: bool | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomImageResponse(RoomImageBase):
    """
    Room image response.
    """

    id: UUID

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )