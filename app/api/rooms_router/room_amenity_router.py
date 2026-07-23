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

from app.schema.rooms_schemas.room_amenity_schema import (
    RoomAmenityCreate,
    RoomAmenityResponse,
)

from app.services.rooms_services.room_amenity_service import (
    RoomAmenityService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/room-amenities",
    tags=["Room Amenities"],
)

# ============================================================
# Create Room Amenity
# ============================================================

@router.post(
    "",
    response_model=RoomAmenityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_room_amenity(
    request: RoomAmenityCreate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomAmenityService(db)

    return await service.create(
        request,
    )


# ============================================================
# Get All Room Amenities
# ============================================================

@router.get(
    "",
    response_model=list[RoomAmenityResponse],
    status_code=status.HTTP_200_OK,
)
async def get_room_amenities(
    db: AsyncSession = Depends(get_db),
):

    service = RoomAmenityService(db)

    return await service.get_all()


# ============================================================
# Get Amenities By Room Type
# ============================================================

@router.get(
    "/room-type/{room_type_id}",
    response_model=list[RoomAmenityResponse],
    status_code=status.HTTP_200_OK,
)
async def get_room_type_amenities(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomAmenityService(db)

    return await service.get_by_room_type(
        room_type_id,
    )


# ============================================================
# Delete Room Amenity
# ============================================================

@router.delete(
    "/{room_type_id}/{amenity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_amenity(
    room_type_id: UUID,
    amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomAmenityService(db)

    await service.delete(
        room_type_id,
        amenity_id,
    )