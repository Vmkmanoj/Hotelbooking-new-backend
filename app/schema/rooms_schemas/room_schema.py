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

    floor: str | None = Field(
        default=None,
        max_length=20,
    )

    status: RoomStatus = RoomStatus.AVAILABLE


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

    floor: str | None = Field(
        default=None,
        max_length=20,
    )

    status: RoomStatus | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class RoomResponse(RoomBase):

    id: UUID

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )