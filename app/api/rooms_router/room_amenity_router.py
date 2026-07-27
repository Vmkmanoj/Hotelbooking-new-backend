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
# Assign Amenity To Room Type
# ============================================================

@router.post(
    "",
    response_model=RoomAmenityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def create_room_amenity(
    request: RoomAmenityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomAmenityService(db)

    return await service.create_room_amenity(
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get Amenities Of Room Type
# ============================================================

@router.get(
    "/room-type/{room_type_id}",
    response_model=list[RoomAmenityResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room_type_amenities(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomAmenityService(db)

    return await service.get_room_amenities(
        room_type_id=room_type_id,
        current_user=current_user,
    )


# ============================================================
# Remove Amenity From Room Type
# ============================================================

@router.delete(
    "/{room_type_id}/{amenity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def delete_room_amenity(
    room_type_id: UUID,
    amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomAmenityService(db)

    await service.delete_room_amenity(
        room_type_id=room_type_id,
        amenity_id=amenity_id,
        current_user=current_user,
    )