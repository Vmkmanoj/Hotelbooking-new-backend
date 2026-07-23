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

from app.schema.property_schema.amenity_schema import (
    AmenityCreate,
    AmenityResponse,
    AmenityUpdate,
)

from app.services.property_services.amenity_service import (
    AmenityService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/amenities",
    tags=["Amenities"],
)

# ============================================================
# Create Amenity
# ============================================================

@router.post(
    "",
    response_model=AmenityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_amenity(
    request: AmenityCreate,
    db: AsyncSession = Depends(get_db),
):

    service = AmenityService(db)

    return await service.create_amenity(
        request,
    )


# ============================================================
# Get All Amenities
# ============================================================

@router.get(
    "",
    response_model=list[AmenityResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_amenities(
    db: AsyncSession = Depends(get_db),
):

    service = AmenityService(db)

    return await service.get_all_amenities()


# ============================================================
# Get Amenity By Id
# ============================================================

@router.get(
    "/{amenity_id}",
    response_model=AmenityResponse,
    status_code=status.HTTP_200_OK,
)
async def get_amenity(
    amenity_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = AmenityService(db)

    return await service.get_amenity(
        amenity_id,
    )


# ============================================================
# Update Amenity
# ============================================================

@router.patch(
    "/{amenity_id}",
    response_model=AmenityResponse,
    status_code=status.HTTP_200_OK,
)
async def update_amenity(
    amenity_id: UUID,
    request: AmenityUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = AmenityService(db)

    return await service.update_amenity(
        amenity_id=amenity_id,
        amenity_data=request,
    )


# ============================================================
# Delete Amenity
# ============================================================

# @router.delete(
#     "/{amenity_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_amenity(
#     amenity_id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#
#     service = AmenityService(db)
#
#     await service.delete_amenity(
#         amenity_id,
#     )