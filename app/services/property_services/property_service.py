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

from app.models.property_models.address import Address
from app.models.property_models.property import Property

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

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = PropertyRepository(db)

    # ========================================================
    # Create Property
    # ========================================================

    async def create_property(
        self,
        property_data: PropertyCreate,
    ) -> Property:

        address = Address(
            address_line_1=property_data.address_line_1,
            address_line_2=property_data.address_line_2,
            city=property_data.city,
            state=property_data.state,
            country=property_data.country,
            postal_code=property_data.postal_code,
            created_by=property_data.owner_id,
            updated_by=property_data.owner_id,
        )

        property_obj = Property(
            owner_id=property_data.owner_id,
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
            created_by=property_data.owner_id,
            updated_by=property_data.owner_id,
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
        owner_id: UUID,
    ) -> list[Property]:

        return await self.repo.get_by_owner_id(
            owner_id,
        )

    # ========================================================
    # Get Property Details
    # ========================================================

    async def get_property_details(
        self,
        property_id: UUID,
    ) -> Property:

        return await self._get_property_or_404(
            property_id,
        )

    # ========================================================
    # Update Property
    # ========================================================

    async def update_property(
        self,
        property_id: UUID,
        owner_id: UUID,
        property_data: PropertyUpdate,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_owner(
            property_obj,
            owner_id,
        )

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
        owner_id: UUID,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_owner(
            property_obj,
            owner_id,
        )

        if property_obj.status == PropertyStatus.ARCHIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property is already archived.",
            )

        return await self.repo.archive(
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

    def _validate_property_owner(
        self,
        property_obj: Property,
        owner_id: UUID,
    ) -> None:

        if property_obj.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this property.",
            )


    # ========================================================
    # Submit Property For Review
    # ========================================================

    async def submit_property_for_review(
        self,
        property_id: UUID,
        owner_id: UUID,
    ) -> Property:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_owner(
            property_obj,
            owner_id,
        )

        if property_obj.status == PropertyStatus.ARCHIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Archived properties cannot be submitted for review.",
            )

        return await self.repo.submit_for_review(
            property_obj,
        )


    # ========================================================
    # Delete Draft Property
    # ========================================================

    async def delete_draft_property(
        self,
        property_id: UUID,
        owner_id: UUID,
    ) -> None:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_owner(
            property_obj,
            owner_id,
        )

        if property_obj.status != PropertyStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft properties can be deleted.",
            )

        await self.repo.delete(
            property_obj,
        )