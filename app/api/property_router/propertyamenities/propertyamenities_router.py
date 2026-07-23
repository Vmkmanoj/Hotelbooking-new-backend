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
# Create Property Amenity
# ============================================================

@router.post(
    "",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_property_amenity(
    request: PropertyAmenityCreate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyAmenityService(db)

    return await service.create_property_amenity(
        request,
    )


# ============================================================
# Get All Property Amenities
# ============================================================

@router.get(
    "",
    response_model=list[PropertyAmenityResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_property_amenities(
    db: AsyncSession = Depends(get_db),
):

    service = PropertyAmenityService(db)

    return await service.get_all_property_amenities()


# ============================================================
# Get Property Amenity By Id
# ============================================================

@router.get(
    "/{property_amenity_id}",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_200_OK,
)
async def get_property_amenity(
    property_amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyAmenityService(db)

    return await service.get_property_amenity(
        property_amenity_id,
    )


# ============================================================
# Update Property Amenity
# ============================================================

@router.patch(
    "/{property_amenity_id}",
    response_model=PropertyAmenityResponse,
    status_code=status.HTTP_200_OK,
)
async def update_property_amenity(
    property_amenity_id: UUID,
    request: PropertyAmenityUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyAmenityService(db)

    return await service.update_property_amenity(
        property_amenity_id=property_amenity_id,
        property_amenity_data=request,
    )


# ============================================================
# Delete Property Amenity
# ============================================================

# @router.delete(
#     "/{property_amenity_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_property_amenity(
#     property_amenity_id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#
#     service = PropertyAmenityService(db)
#
#     await service.delete_property_amenity(
#         property_amenity_id,
#     )