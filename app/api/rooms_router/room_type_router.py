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
    dependencies=[
        Depends(
            require_permission(
                "room.create",
            )
        )
    ],
)
async def create_room_type(
    request: RoomTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    return await service.create_room_type(
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get All Room Types
# ============================================================

@router.get(
    "",
    response_model=list[RoomTypeResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_all_room_types(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    return await service.get_all_room_types(
        current_user=current_user,
    )


# ============================================================
# Get Room Types Of Property
# ============================================================

@router.get(
    "/property/{property_id}",
    response_model=list[RoomTypeResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room_types_by_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    return await service.get_room_types_by_property(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Get Room Type
# ============================================================

@router.get(
    "/{room_type_id}",
    response_model=RoomTypeResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room_type(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    return await service.get_room_type(
        room_type_id=room_type_id,
        current_user=current_user,
    )


# ============================================================
# Update Room Type
# ============================================================

@router.patch(
    "/{room_type_id}",
    response_model=RoomTypeResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def update_room_type(
    room_type_id: UUID,
    request: RoomTypeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    return await service.update_room_type(
        room_type_id=room_type_id,
        request=request,
        current_user=current_user,
    )


# ============================================================
# Delete Room Type
# ============================================================

@router.delete(
    "/{room_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "room.delete",
            )
        )
    ],
)
async def delete_room_type(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomTypeService(db)

    await service.delete_room_type(
        room_type_id=room_type_id,
        current_user=current_user,
    )