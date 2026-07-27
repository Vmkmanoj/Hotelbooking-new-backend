# ============================================================
# Standard Library
# ============================================================

from app.schema.user_schema.user import getUser
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

from app.models.property_models.property import Property
from app.models.users_models.users import User
from app.models.permissions_models.roles import Role

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
        self.db = db
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

        properties = await self.repo.get_approved_properties()

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


    async def getAllCustomers(self):
        result = await self.db.execute(
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(Role.name == "CUSTOMER")
        )

        customers = result.scalars().all()

        if not customers:
            raise HTTPException(status_code=404, detail="Customers not found")

        return [
            getUser(
                email=cus.email,
                first_name=cus.first_name,
                last_name=cus.last_name,
                phone=cus.phone,
                last_login_at=cus.last_login_at,
            )
            for cus in customers
        ]

    async def getAllPropertyOwners(self):
        result = await self.db.execute(
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(Role.name == "PROPERTY_OWNER")
        )

        property_owners = result.scalars().all()

        if not property_owners:
            raise HTTPException(status_code=404, detail="Property owners not found")

        return property_owners

    async def getAllProperty(self):
        
        result = await self.repo.get_all_property()

        return result
