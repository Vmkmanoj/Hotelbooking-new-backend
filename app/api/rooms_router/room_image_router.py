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

from app.schema.rooms_schemas.room_image_schema import (
    RoomImageCreate,
    RoomImageResponse,
    RoomImageUpdate,
)

from app.services.rooms_services.room_image_service import (
    RoomImageService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/room-images",
    tags=["Room Images"],
)

# ============================================================
# Upload Room Image
# ============================================================

@router.post(
    "/room-type/{room_type_id}",
    response_model=RoomImageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def create_room_image(
    room_type_id: UUID,
    request: RoomImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomImageService(db)

    return await service.create_room_image(
        room_type_id=room_type_id,
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get Images Of Room Type
# ============================================================

@router.get(
    "/room-type/{room_type_id}",
    response_model=list[RoomImageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room_images(
    room_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomImageService(db)

    return await service.get_room_images(
        room_type_id=room_type_id,
        current_user=current_user,
    )


# ============================================================
# Get Room Image
# ============================================================

@router.get(
    "/{image_id}",
    response_model=RoomImageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.view",
            )
        )
    ],
)
async def get_room_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomImageService(db)

    return await service.get_room_image(
        image_id=image_id,
        current_user=current_user,
    )


# ============================================================
# Update Room Image
# ============================================================

@router.patch(
    "/{image_id}",
    response_model=RoomImageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def update_room_image(
    image_id: UUID,
    request: RoomImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomImageService(db)

    return await service.update_room_image(
        image_id=image_id,
        request=request,
        current_user=current_user,
    )


# ============================================================
# Delete Room Image
# ============================================================

@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "room.update",
            )
        )
    ],
)
async def delete_room_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = RoomImageService(db)

    await service.delete_room_image(
        image_id=image_id,
        current_user=current_user,
    )