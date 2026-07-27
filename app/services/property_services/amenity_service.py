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
from httpx import request
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.property_models.amenities import Amenity
from app.models.users_models.users import User

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
    """
    Business logic for Amenity Management.
    """

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
        current_user: User,
    ) -> Amenity:
        """
        Create a new amenity.
        """

        existing = await self.repo.get_by_name(
            amenity_data.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity already exists.",
            )

        amenity = Amenity(
            name=amenity_data.name,
            description=amenity_data.description,
            category=amenity_data.category,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            amenity,
        )

    # ========================================================
    # Get Amenity
    # ========================================================

    async def get_amenity(
        self,
        amenity_id: UUID,
    ) -> Amenity:
        """
        Retrieve an amenity by ID.
        """

        return await self._get_amenity_or_404(
            amenity_id,
        )

    # ========================================================
    # Get All Amenities
    # ========================================================

    async def get_all_amenities(
        self,
    ) -> list[Amenity]:
        """
        Retrieve all amenities.
        """

        return await self.repo.get_all()

    # ========================================================
    # Update Amenity
    # ========================================================

    async def update_amenity(
        self,
        amenity_id: UUID,
        amenity_data: AmenityUpdate,
        current_user: User,
    ) -> Amenity:
        """
        Update an existing amenity.
        """

        amenity = await self._get_amenity_or_404(
            amenity_id,
        )

        if (
            amenity_data.name is not None
            and amenity_data.name.lower() != amenity.name.lower()
        ):
            existing = await self.repo.get_by_name(
                amenity_data.name,
                room_name=request.room_name,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Amenity already exists.",
                )

        amenity.updated_by = current_user.email

        return await self.repo.update(
            amenity,
            amenity_data,
        )

    # ========================================================
    # Delete Amenity
    # ========================================================

    async def delete_amenity(
        self,
        amenity_id: UUID,
    ) -> None:
        """
        Delete an amenity.
        """

        amenity = await self._get_amenity_or_404(
            amenity_id,
        )

        await self.repo.delete(
            amenity,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_amenity_or_404(
        self,
        amenity_id: UUID,
    ) -> Amenity:
        """
        Retrieve an amenity or raise 404.
        """

        amenity = await self.repo.get_by_id(
            amenity_id,
        )

        if amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Amenity not found.",
            )

        return amenity