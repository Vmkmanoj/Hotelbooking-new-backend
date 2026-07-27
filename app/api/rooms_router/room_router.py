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

from app.dependencies.auth import (
    get_current_user,
    require_permission,
)

from app.models.users_models.users import User

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
    dependencies=[
        Depends(
            require_permission(
                "room.create",
            )
        )
    ],
)
async def create_room(
    request: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    return await service.create_room(
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get All Rooms
# ============================================================

@router.get(
    "",
    response_model=list[RoomResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_all_rooms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    return await service.get_all_rooms(
        current_user=current_user,
    )


# ============================================================
# Get Rooms By Room Type
# ============================================================

@router.get(
    "/room-type/{room_type_id}",
    response_model=list[RoomResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_rooms_by_room_type(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    return await service.get_rooms_by_room_type(
        room_type_id=room_type_id,
        current_user=current_user,
    )


# ============================================================
# Get Room
# ============================================================

@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    return await service.get_room(
        room_id=room_id,
        current_user=current_user,
    )


# ============================================================
# Update Room
# ============================================================

@router.patch(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def update_room(
    room_id: UUID,
    request: RoomUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    return await service.update_room(
        room_id=room_id,
        request=request,
        current_user=current_user,
    )


# ============================================================
# Delete Room
# ============================================================

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "room.delete",
            )
        )
    ],
)
async def delete_room(
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomService(db)

    await service.delete_room(
        room_id=room_id,
        current_user=current_user,
    )