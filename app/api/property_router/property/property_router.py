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
    Response,
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

from app.schema.property_schema.property_schema import (
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
)

from app.schema.property_schema.property_review_schema import (
    PropertyApproveRequest,
    PropertyRejectRequest,
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
    current_user: User = Depends(
        require_permission("property.create"),
    ),
):
    service = PropertyService(db)

    return await service.create_property(
        property_data=request,
        current_user=current_user,
    )


# ============================================================
# Get My Properties
# ============================================================

@router.get(
    "/my",
    response_model=list[PropertyResponse],
)
async def get_my_properties(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.view"),
    ),
):
    service = PropertyService(db)

    return await service.get_my_properties(
        current_user=current_user,
    )


# ============================================================
# Get Property Details
# ============================================================

@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def get_property_details(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.view"),
    ),
):
    service = PropertyService(db)

    return await service.get_property_details(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Update Property
# ============================================================

@router.patch(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def update_property(
    property_id: UUID,
    request: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.update"),
    ),
):
    service = PropertyService(db)

    return await service.update_property(
        property_id=property_id,
        property_data=request,
        current_user=current_user,
    )


# ============================================================
# Archive Property
# ============================================================

@router.patch(
    "/{property_id}/archive",
    response_model=PropertyResponse,
)
async def archive_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.update"),
    ),
):
    service = PropertyService(db)

    return await service.archive_property(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Submit Property For Review
# ============================================================

@router.patch(
    "/{property_id}/submit-review",
    response_model=PropertyResponse,
)
async def submit_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.update"),
    ),
):
    service = PropertyService(db)

    return await service.submit_property_for_review(
        property_id=property_id,
        current_user=current_user,
    )


# ============================================================
# Approve Property
# ============================================================

@router.patch(
    "/{property_id}/approve",
    response_model=PropertyResponse,
)
async def approve_property(
    property_id: UUID,
    request: PropertyApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.approve"),
    ),
):
    service = PropertyService(db)

    return await service.approve_property(
        property_id=property_id,
        remarks=request.approval_remarks,
        current_user=current_user,
    )


# ============================================================
# Reject Property
# ============================================================

@router.patch(
    "/{property_id}/reject",
    response_model=PropertyResponse,
)
async def reject_property(
    property_id: UUID,
    request: PropertyRejectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.reject"),
    ),
):
    service = PropertyService(db)

    return await service.reject_property(
        property_id=property_id,
        remarks=request.approval_remarks,
        current_user=current_user,
    )


# ============================================================
# Delete Property (Soft Delete)
# ============================================================

@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_permission("property.delete"),
    ),
):
    service = PropertyService(db)

    await service.delete_property(
        property_id=property_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )