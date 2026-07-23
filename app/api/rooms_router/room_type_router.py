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

from app.schema.rooms_schemas.room_type_schema import (
    RoomTypeCreate,
    RoomTypeResponse,
    RoomTypeUpdate,
)

from app.services.rooms_services.room_type_service import (
    RoomTypeService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/room-types",
    tags=["Room Types"],
)

# ============================================================
# Create Room Type
# ============================================================

@router.post(
    "",
    response_model=RoomTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_room_type(
    request: RoomTypeCreate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomTypeService(db)

    return await service.create(
        request,
    )


# ============================================================
# Get All Room Types
# ============================================================

@router.get(
    "",
    response_model=list[RoomTypeResponse],
    status_code=status.HTTP_200_OK,
)
async def get_room_types(
    db: AsyncSession = Depends(get_db),
):

    service = RoomTypeService(db)

    return await service.get_all()


# ============================================================
# Get Room Type By Id
# ============================================================

@router.get(
    "/{room_type_id}",
    response_model=RoomTypeResponse,
    status_code=status.HTTP_200_OK,
)
async def get_room_type(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomTypeService(db)

    return await service.get_by_id(
        room_type_id,
    )


# ============================================================
# Update Room Type
# ============================================================

@router.patch(
    "/{room_type_id}",
    response_model=RoomTypeResponse,
    status_code=status.HTTP_200_OK,
)
async def update_room_type(
    room_type_id: UUID,
    request: RoomTypeUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomTypeService(db)

    return await service.update(
        room_type_id=room_type_id,
        request=request,
    )


# ============================================================
# Delete Room Type
# ============================================================

@router.delete(
    "/{room_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_type(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomTypeService(db)

    await service.delete(
        room_type_id,
    )