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

from app.schema.property_schema.property_schema import (
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
)

from app.services.property_services.property_service import (
    PropertyService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
)

# ============================================================
# Create Property
# ============================================================

@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_property(
    request: PropertyCreate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.create_property(
        request,
    )


# ============================================================
# Get My Properties
# ============================================================

@router.get(
    "/owner/{owner_id}",
    response_model=list[PropertyResponse],
    status_code=status.HTTP_200_OK,
)
async def get_my_properties(
    owner_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.get_my_properties(
        owner_id,
    )


# ============================================================
# Get Property Details
# ============================================================

@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
    status_code=status.HTTP_200_OK,
)
async def get_property_details(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.get_property_details(
        property_id,
    )


# ============================================================
# Update Property
# ============================================================

@router.patch(
    "/{property_id}",
    response_model=PropertyResponse,
    status_code=status.HTTP_200_OK,
)
async def update_property(
    property_id: UUID,
    owner_id: UUID,      # TODO: Replace with current_user.id after JWT integration
    request: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.update_property(
        property_id=property_id,
        owner_id=owner_id,
        property_data=request,
    )


# ============================================================
# Archive Property
# ============================================================

@router.patch(
    "/{property_id}/archive",
    response_model=PropertyResponse,
    status_code=status.HTTP_200_OK,
)
async def archive_property(
    property_id: UUID,
    owner_id: UUID,      # TODO: Replace with current_user.id after JWT integration
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.archive_property(
        property_id=property_id,
        owner_id=owner_id,
    )


# ============================================================
# Submit Property For Review
# ============================================================

@router.patch(
    "/{property_id}/submit-review",
    response_model=PropertyResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_property_for_review(
    property_id: UUID,
    owner_id: UUID,      # TODO: Replace with current_user.id after JWT integration
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    return await service.submit_property_for_review(
        property_id=property_id,
        owner_id=owner_id,
    )


# ============================================================
# Delete Draft Property
# ============================================================

@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_draft_property(
    property_id: UUID,
    owner_id: UUID,      # TODO: Replace with current_user.id after JWT integration
    db: AsyncSession = Depends(get_db),
):

    service = PropertyService(db)

    await service.delete_draft_property(
        property_id=property_id,
        owner_id=owner_id,
    )