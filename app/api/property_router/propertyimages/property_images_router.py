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

from app.schema.property_schema.property_images_schema import (
    PropertyImageCreate,
    PropertyImageResponse,
    PropertyImageUpdate,
)

from app.services.property_services.property_images_service import (
    PropertyImageService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/property-images",
    tags=["Property Images"],
)

# ============================================================
# Create Property Image
# ============================================================

@router.post(
    "",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_property_image(
    request: PropertyImageCreate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyImageService(db)

    return await service.create_property_image(
        request,
    )


# ============================================================
# Get All Property Images
# ============================================================

@router.get(
    "",
    response_model=list[PropertyImageResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_property_images(
    db: AsyncSession = Depends(get_db),
):

    service = PropertyImageService(db)

    return await service.get_all_property_images()


# ============================================================
# Get Property Image By Id
# ============================================================

@router.get(
    "/{image_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_property_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyImageService(db)

    return await service.get_property_image(
        image_id,
    )


# ============================================================
# Update Property Image
# ============================================================

@router.patch(
    "/{image_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_200_OK,
)
async def update_property_image(
    image_id: UUID,
    request: PropertyImageUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyImageService(db)

    return await service.update_property_image(
        image_id=image_id,
        property_image_data=request,
    )


# ============================================================
# Delete Property Image
# ============================================================

# @router.delete(
#     "/{image_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_property_image(
#     image_id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#
#     service = PropertyImageService(db)
#
#     await service.delete_property_image(
#         image_id,
#     )