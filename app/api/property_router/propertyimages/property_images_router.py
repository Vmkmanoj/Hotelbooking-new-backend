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
# Upload Property Image
# ============================================================

@router.post(
    "/property/{property_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def create_property_image(
    property_id: UUID,
    request: PropertyImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyImageService(db)

    return await service.create_property_image(
        property_id=property_id,
        image_data=request,
        current_user=current_user,
    )


# ============================================================
# Get Images Of Property
# ============================================================

@router.get(
    "/property/{property_id}",
    response_model=list[PropertyImageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.view",
            )
        )
    ],
)
async def get_property_images(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyImageService(db)

    return await service.get_property_images(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Get Image
# ============================================================

@router.get(
    "/{image_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.view",
            )
        )
    ],
)
async def get_property_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyImageService(db)

    return await service.get_property_image(
        image_id=image_id,
        current_user=current_user,
    )


# ============================================================
# Update Image
# ============================================================

@router.patch(
    "/{image_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def update_property_image(
    image_id: UUID,
    request: PropertyImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyImageService(db)

    return await service.update_property_image(
        image_id=image_id,
        image_data=request,
        current_user=current_user,
    )


# ============================================================
# Delete Image
# ============================================================

@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def delete_property_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyImageService(db)

    await service.delete_property_image(
        image_id=image_id,
        current_user=current_user,
    )