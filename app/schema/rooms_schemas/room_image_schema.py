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
    image_url: str = Field(
        min_length=5,
        max_length=500,
    )

    caption: str | None = Field(
        default=None,
        max_length=255,
    )

    display_order: int = Field(
        default=1,
        ge=1,
    )

    is_cover: bool = False


# ============================================================
# Create
# ============================================================

class RoomImageCreate(RoomImageBase):

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Update
# ============================================================

class RoomImageUpdate(BaseModel):

    image_url: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    caption: str | None = Field(
        default=None,
        max_length=255,
    )

    display_order: int | None = Field(
        default=None,
        ge=1,
    )

    is_cover: bool | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomImageResponse(RoomImageBase):

    id: UUID

    room_type_id: UUID

    created_by: str |None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )