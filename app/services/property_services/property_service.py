# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

from app.common.enums.user_enums.role_name import (
    RoleName,
)

from app.models.property_models.address import Address
from app.models.property_models.property import Property
from app.models.users_models.users import User

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

from app.schema.property_schema.property_schema import (
    PropertyCreate,
    PropertyUpdate,
)


# ============================================================
# Property Service
# ============================================================

class PropertyService:
    """
    Business logic for Property Management.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = PropertyRepository(db)

    # ========================================================
    # Create Property
    # ========================================================

    async def create_property(
        self,
        property_data: PropertyCreate,
        current_user: User,
    ) -> Property:

        if current_user.role.name != RoleName.PROPERTY_OWNER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only property owners can create properties.",
            )

        address = Address(
            address_line_1=property_data.address_line_1,
            address_line_2=property_data.address_line_2,
            city=property_data.city,
            state=property_data.state,
            country=property_data.country,
            postal_code=property_data.postal_code,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        property_obj = Property(
            owner_id=current_user.id,
            property_name=property_data.property_name,
            description=property_data.description,
            property_type=property_data.property_type,
            star_rating=property_data.star_rating,
            contact_email=property_data.contact_email,
            contact_number=property_data.contact_number,
            cancellation_policy=property_data.cancellation_policy,
            house_rules=property_data.house_rules,
            child_policy=property_data.child_policy,
            pet_policy=property_data.pet_policy,
            smoking_policy=property_data.smoking_policy,
            check_in_time=property_data.check_in_time,
            check_out_time=property_data.check_out_time,
            status=PropertyStatus.PENDING,
            is_verified=False,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            address=address,
            property_obj=property_obj,
        )

    # ========================================================
    # Get My Properties
    # ========================================================

    async def get_my_properties(
        self,
        current_user: User,
    ) -> list[Property]:

        return await self.repo.get_by_owner_id(
            current_user.id,
        )

    # ========================================================
    # Get Property Details
    # ========================================================

    async def get_property_details(
        self,
        property_id: UUID,
        current_user: User,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        return property_obj

    # ========================================================
    # Update Property
    # ========================================================

    async def update_property(
        self,
        property_id: UUID,
        property_data: PropertyUpdate,
        current_user: User,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        property_obj.updated_by = current_user.email

        #
        # Any modification requires re-approval
        #
        property_obj.status = PropertyStatus.PENDING
        property_obj.is_verified = False
        property_obj.approved_by = None
        property_obj.approved_at = None
        property_obj.approval_remarks = None

        return await self.repo.update(
            property_obj=property_obj,
            property_data=property_data,
        )

    # ========================================================
    # Archive Property
    # ========================================================

    async def archive_property(
        self,
        property_id: UUID,
        current_user: User,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        if property_obj.status == PropertyStatus.ARCHIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property is already archived.",
            )

        property_obj.updated_by = current_user.email

        return await self.repo.archive(
            property_obj,
        )

    # ========================================================
    # Submit Property For Review
    # ========================================================

    async def submit_property_for_review(
        self,
        property_id: UUID,
        current_user: User,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        if property_obj.status == PropertyStatus.ARCHIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Archived properties cannot be submitted.",
            )

        if property_obj.status == PropertyStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property is already awaiting approval.",
            )

        if property_obj.status == PropertyStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property is already approved.",
            )

        property_obj.updated_by = current_user.email

        return await self.repo.submit_for_review(
            property_obj,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_property_or_404(
        self,
        property_id: UUID,
    ) -> Property:

        property_obj = await self.repo.get_by_id(
            property_id,
        )

        if property_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        return property_obj

    # ========================================================
    # Ownership Validation
    # ========================================================

    def _validate_property_access(
        self,
        property_obj: Property,
        current_user: User,
    ) -> None:
        """
        Ensure the authenticated property owner owns
        the requested property.
        """

        if current_user.role.name != RoleName.PROPERTY_OWNER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only property owners can perform this action.",
            )

        if property_obj.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this property.",
            )


    # ========================================================
    # Approve Property
    # ========================================================

    async def approve_property(
        self,
        property_id: UUID,
        remarks: str | None,
        current_user: User,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        if property_obj.status != PropertyStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending properties can be approved.",
            )

        property_obj.updated_by = current_user.email

        return await self.repo.approve_property(
            property_obj=property_obj,
            approved_by=current_user.id,
            approval_remarks=remarks,
        )

    # ========================================================
    # Reject Property
    # ========================================================

    async def reject_property(
        self,
        property_id: UUID,
        remarks: str,
        current_user: User,
    ) -> Property:

        if not remarks.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rejection remarks are required.",
            )
        property_obj = await self._get_property_or_404(
            property_id,
        )

        if property_obj.status != PropertyStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending properties can be rejected.",
            )

        property_obj.updated_by = current_user.email

        await self.repo.reject_property(
            property_obj=property_obj,
            rejected_by=current_user.id,
            approval_remarks=remarks,
        )