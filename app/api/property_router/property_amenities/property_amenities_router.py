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

from app.schema.property_schema.property_amenities_schema import (
    PropertyAmenityCreate,
    PropertyAmenityResponse,
    PropertyAmenityUpdate,
)

from app.services.property_services.property_amenities_service import (
    PropertyAmenityService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/property-amenities",
    tags=["Property Amenities"],
)

# ============================================================
# Assign Amenity To Property
# ============================================================

@router.post(
    "",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def create_property_amenity(
    request: PropertyAmenityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyAmenityService(db)

    return await service.create_property_amenity(
        property_amenity_data=request,
        current_user=current_user,
    )


# ============================================================
# Get Amenities Of Property
# ============================================================

@router.get(
    "/property/{property_id}",
    response_model=list[PropertyAmenityResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.view",
            )
        )
    ],
)
async def get_property_amenities(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyAmenityService(db)

    return await service.get_property_amenities(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Get Property Amenity
# ============================================================

@router.get(
    "/{property_amenity_id}",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.view",
            )
        )
    ],
)
async def get_property_amenity(
    property_amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyAmenityService(db)

    return await service.get_property_amenity(
        property_amenity_id=property_amenity_id,
        current_user=current_user,
    )


# ============================================================
# Update Property Amenity
# ============================================================

@router.patch(
    "/{property_amenity_id}",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def update_property_amenity(
    property_amenity_id: UUID,
    request: PropertyAmenityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyAmenityService(db)

    return await service.update_property_amenity(
        property_amenity_id=property_amenity_id,
        property_amenity_data=request,
        current_user=current_user,
    )


# ============================================================
# Remove Amenity From Property
# ============================================================

@router.delete(
    "/{property_amenity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "property.update",
            )
        )
    ],
)
async def delete_property_amenity(
    property_amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PropertyAmenityService(db)

    await service.delete_property_amenity(
        property_amenity_id=property_amenity_id,
        current_user=current_user,
    )