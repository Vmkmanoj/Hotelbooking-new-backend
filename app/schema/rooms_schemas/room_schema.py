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

from app.common.enums.room_enums.room_status import (
    RoomStatus,
)

# ============================================================
# Room Base
# ============================================================

class RoomBase(BaseModel):
    """
    Base schema for Rooms.
    """

    room_type_id: UUID

    room_number: str = Field(
        min_length=1,
        max_length=20,
    )

    floor: int | None = Field(
        default=None,
        ge=0,
    )

    status: RoomStatus = RoomStatus.AVAILABLE

    is_active: bool = True


# ============================================================
# Create
# ============================================================

class RoomCreate(RoomBase):

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Update
# ============================================================

class RoomUpdate(BaseModel):

    room_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    floor: int | None = Field(
        default=None,
        ge=0,
    )

    status: RoomStatus | None = None

    is_active: bool | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomResponse(RoomBase):

    id: UUID

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )