# ============================================================
# Standard Library
# ============================================================

from typing import List
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

from app.schema.super_admin_schema.super_admin_property_schema import (
    ActivatePropertyRequest,
    RejectPropertyRequest,
    SuspendPropertyRequest,
)

from app.schema.super_admin_schema.super_admin_schema import (
    ApprovePropertyRequest,
    MessageResponse,
    PendingPropertyResponse,
    PropertyDetailResponse,
)

from app.services.super_admin_services.super_admin_service import (
    SuperAdminPropertyService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/super-admin",
    tags=["Super Admin"],
)

# ============================================================
# Service Dependency
# ============================================================

def get_super_admin_service(
    db: AsyncSession = Depends(get_db),
) -> SuperAdminPropertyService:

    return SuperAdminPropertyService(db)

# ============================================================
# Get Pending Properties
# ============================================================

@router.get(
    "/property/pending",
    response_model=List[PendingPropertyResponse],
    status_code=status.HTTP_200_OK,
)
async def get_pending_properties(
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.get_pending_properties()


# ============================================================
# Get Property Details
# ============================================================

@router.get(
    "/property/{property_id}",
    response_model=PropertyDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_property(
    property_id: UUID,
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.get_property(
        property_id,
    )


# ============================================================
# Approve Property
# ============================================================

@router.patch(
    "/property/{property_id}/approve",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def approve_property(
    property_id: UUID,
    request: ApprovePropertyRequest,
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.approve_property(
        property_id,
        request,
    )


# ============================================================
# Reject Property
# ============================================================

@router.patch(
    "/property/{property_id}/reject",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def reject_property(
    property_id: UUID,
    request: RejectPropertyRequest,
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.reject_property(
        property_id,
        request,
    )


# ============================================================
# Suspend Property
# ============================================================

@router.patch(
    "/property/{property_id}/suspend",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def suspend_property(
    property_id: UUID,
    request: SuspendPropertyRequest,
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.suspend_property(
        property_id,
        request,
    )


# ============================================================
# Activate Property
# ============================================================

@router.patch(
    "/property/{property_id}/activate",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def activate_property(
    property_id: UUID,
    request: ActivatePropertyRequest,
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.activate_property(
        property_id,
        request,
    )


# ============================================================
# Get Approved Properties
# ============================================================

@router.get(
    "/property/status/approved",
    status_code=status.HTTP_200_OK,
)
async def get_approved_properties(
    service: SuperAdminPropertyService = Depends(
        get_super_admin_service,
    ),
):

    return await service.get_all_approved_property()


# ============================================================
# Delete Property
# ============================================================

# @router.delete(
#     "/property/{property_id}",
#     response_model=MessageResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_property(
#     property_id: UUID,
#     service: SuperAdminPropertyService = Depends(
#         get_super_admin_service,
#     ),
# ):
#
#     return await service.delete_property(
#         property_id,
#     )