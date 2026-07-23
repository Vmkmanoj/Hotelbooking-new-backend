# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.database.session import get_db

from app.schema.rooms_schemas.room_schema import (
    RoomCreate,
    RoomResponse,
    RoomUpdate,
)

from app.services.rooms_services.room_service import (
    RoomService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)

# ============================================================
# Create Room
# ============================================================

@router.post(
    "",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_room(
    request: RoomCreate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomService(db)

    return await service.create_room(
        request,
    )


# ============================================================
# Get All Rooms
# ============================================================

@router.get(
    "",
    response_model=list[RoomResponse],
    status_code=status.HTTP_200_OK,
)
async def get_rooms(
    db: AsyncSession = Depends(get_db),
):

    service = RoomService(db)

    return await service.get_rooms()


# ============================================================
# Get Room By Id
# ============================================================

@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
)
async def get_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomService(db)

    return await service.get_room(
        room_id,
    )


# ============================================================
# Update Room
# ============================================================

@router.patch(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
)
async def update_room(
    room_id: UUID,
    request: RoomUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomService(db)

    return await service.update_room(
        room_id=room_id,
        request=request,
    )


# ============================================================
# Delete Room
# ============================================================

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomService(db)

    await service.delete_room(
        room_id,
    )