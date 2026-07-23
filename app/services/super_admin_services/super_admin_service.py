# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

from app.models.property_models.property import Property

from app.repositories.super_admin_repositories.super_admin_repository import (
    SuperAdminPropertyRepository,
)

from app.schema.super_admin_schema.super_admin_schema import (
    MessageResponse,
    ApprovePropertyRequest,
)

from app.schema.super_admin_schema.super_admin_property_schema import (
    RejectPropertyRequest,
    SuspendPropertyRequest,
    ActivatePropertyRequest,
)


# ============================================================
# Super Admin Property Service
# ============================================================

class SuperAdminPropertyService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.repo = SuperAdminPropertyRepository(db)

    # ========================================================
    # Get Pending Properties
    # ========================================================

    async def get_pending_properties(
        self,
    ):

        return await self.repo.get_pending_properties()

    # ========================================================
    # Get Approved Properties
    # ========================================================

    async def get_all_approved_property(
        self,
    ):

        properties = await self.repo.get_approve_property()

        if not properties:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No approved properties found.",
            )

        return properties

    # ========================================================
    # Get Property
    # ========================================================

    async def get_property(
        self,
        property_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        return await self.repo.get_property_by_id(
            property_id,
        )

    # ========================================================
    # Approve Property
    # ========================================================

    async def approve_property(
        self,
        property_id: UUID,
        request: ApprovePropertyRequest,
        admin_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        if property.status != PropertyStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending properties can be approved.",
            )

        await self.repo.approve_property(
            property=property,
            admin_id=admin_id,
        )

        return MessageResponse(
            success=True,
            message="Property approved successfully.",
        )

    # ========================================================
    # Reject Property
    # ========================================================

    async def reject_property(
        self,
        property_id: UUID,
        request: RejectPropertyRequest,
        admin_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        if property.status != PropertyStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending properties can be rejected.",
            )

        await self.repo.reject_property(
            property=property,
            remarks=request.remarks,
            admin_id=admin_id,
        )

        return MessageResponse(
            success=True,
            message="Property rejected successfully.",
        )

    # ========================================================
    # Suspend Property
    # ========================================================

    async def suspend_property(
        self,
        property_id: UUID,
        request: SuspendPropertyRequest,
        admin_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        if property.status != PropertyStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only approved properties can be suspended.",
            )

        await self.repo.suspend_property(
            property=property,
            remarks=request.remarks,
            admin_id=admin_id,
        )

        return MessageResponse(
            success=True,
            message="Property suspended successfully.",
        )

    # ========================================================
    # Activate Property
    # ========================================================

    async def activate_property(
        self,
        property_id: UUID,
        request: ActivatePropertyRequest,
        admin_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        if property.status != PropertyStatus.SUSPENDED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only suspended properties can be activated.",
            )

        await self.repo.activate_property(
            property=property,
            remarks=request.remarks,
            admin_id=admin_id,
        )

        return MessageResponse(
            success=True,
            message="Property activated successfully.",
        )

    # ========================================================
    # Delete Property
    # ========================================================

    async def delete_property(
        self,
        property_id: UUID,
    ):

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        await self.repo.delete_property(
            property,
        )

        return MessageResponse(
            success=True,
            message="Property deleted successfully.",
        )