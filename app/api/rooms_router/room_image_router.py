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
# Create Room Image
# ============================================================

@router.post(
    "",
    response_model=RoomImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_room_image(
    request: RoomImageCreate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomImageService(db)

    return await service.create(
        request,
    )


# ============================================================
# Get All Room Images
# ============================================================

@router.get(
    "",
    response_model=list[RoomImageResponse],
    status_code=status.HTTP_200_OK,
)
async def get_room_images(
    db: AsyncSession = Depends(get_db),
):

    service = RoomImageService(db)

    return await service.get_all()


# ============================================================
# Get Room Image By Id
# ============================================================

@router.get(
    "/{image_id}",
    response_model=RoomImageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_room_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomImageService(db)

    return await service.get_by_id(
        image_id,
    )


# ============================================================
# Update Room Image
# ============================================================

@router.patch(
    "/{image_id}",
    response_model=RoomImageResponse,
    status_code=status.HTTP_200_OK,
)
async def update_room_image(
    image_id: UUID,
    request: RoomImageUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = RoomImageService(db)

    return await service.update(
        image_id=image_id,
        request=request,
    )


# ============================================================
# Delete Room Image
# ============================================================

@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = RoomImageService(db)

    await service.delete(
        image_id,
    )