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

from app.models.property_models.amenities import Amenity

from app.repositories.property_repositories.amenity_repository import (
    AmenityRepository,
)

from app.schema.property_schema.amenity_schema import (
    AmenityCreate,
    AmenityUpdate,
)


# ============================================================
# Amenity Service
# ============================================================

class AmenityService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = AmenityRepository(db)

    # ========================================================
    # Create Amenity
    # ========================================================

    async def create_amenity(
        self,
        amenity_data: AmenityCreate,
    ) -> Amenity:

        existing = await self.repo.get_by_name(
            amenity_data.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity already exists.",
            )

        return await self.repo.create(
            amenity_data,
        )

    # ========================================================
    # Get Amenity
    # ========================================================

    async def get_amenity(
        self,
        amenity_id: UUID,
    ) -> Amenity:

        return await self._get_amenity_or_404(
            amenity_id,
        )

    # ========================================================
    # Get All Amenities
    # ========================================================

    async def get_all_amenities(
        self,
    ) -> list[Amenity]:

        return await self.repo.get_all()

    # ========================================================
    # Update Amenity
    # ========================================================

    async def update_amenity(
        self,
        amenity_id: UUID,
        amenity_data: AmenityUpdate,
    ) -> Amenity:

        amenity = await self._get_amenity_or_404(
            amenity_id,
        )

        if (
            amenity_data.name
            and amenity_data.name != amenity.name
        ):
            existing = await self.repo.get_by_name(
                amenity_data.name,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Amenity already exists.",
                )

        return await self.repo.update(
            amenity,
            amenity_data,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_amenity_or_404(
        self,
        amenity_id: UUID,
    ) -> Amenity:

        amenity = await self.repo.get_by_id(
            amenity_id,
        )

        if amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Amenity not found.",
            )

        return amenity