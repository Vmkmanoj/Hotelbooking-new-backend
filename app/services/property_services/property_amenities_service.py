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

from app.models.property_models.property_amenity import (
    PropertyAmenity,
)

from app.repositories.property_repositories.property_amenities_repository import (
    PropertyAmenityRepository,
)

from app.schema.property_schema.property_amenities_schema import (
    PropertyAmenityCreate,
    PropertyAmenityUpdate,
)


# ============================================================
# Property Amenity Service
# ============================================================

class PropertyAmenityService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = PropertyAmenityRepository(db)

    # ========================================================
    # Create Property Amenity
    # ========================================================

    async def create_property_amenity(
        self,
        property_amenity_data: PropertyAmenityCreate,
    ) -> PropertyAmenity:

        existing_mapping = await self.repo.get_by_property_and_amenity(
            property_id=property_amenity_data.property_id,
            amenity_id=property_amenity_data.amenity_id,
        )

        if existing_mapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity is already assigned to this property.",
            )

        return await self.repo.create(
            property_amenity_data,
        )

    # ========================================================
    # Get Property Amenity
    # ========================================================

    async def get_property_amenity(
        self,
        property_amenity_id: UUID,
    ) -> PropertyAmenity:

        return await self._get_property_amenity_or_404(
            property_amenity_id,
        )

    # ========================================================
    # Get All Property Amenities
    # ========================================================

    async def get_all_property_amenities(
        self,
    ) -> list[PropertyAmenity]:

        return await self.repo.get_all()

    # ========================================================
    # Update Property Amenity
    # ========================================================

    async def update_property_amenity(
        self,
        property_amenity_id: UUID,
        property_amenity_data: PropertyAmenityUpdate,
    ) -> PropertyAmenity:

        property_amenity = await self._get_property_amenity_or_404(
            property_amenity_id,
        )

        return await self.repo.update(
            property_amenity,
            property_amenity_data,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_property_amenity_or_404(
        self,
        property_amenity_id: UUID,
    ) -> PropertyAmenity:

        property_amenity = await self.repo.get_by_id(
            property_amenity_id,
        )

        if property_amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property amenity not found.",
            )

        return property_amenity