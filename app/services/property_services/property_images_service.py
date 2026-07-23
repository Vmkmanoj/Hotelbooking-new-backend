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

from app.models.property_models.property_image import PropertyImage

from app.repositories.property_repositories.property_images_repository import (
    PropertyImageRepository,
)

from app.schema.property_schema.property_images_schema import (
    PropertyImageCreate,
    PropertyImageUpdate,
)


# ============================================================
# Property Image Service
# ============================================================

class PropertyImageService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = PropertyImageRepository(db)

    # ========================================================
    # Create Property Image
    # ========================================================

    async def create_property_image(
        self,
        property_image_data: PropertyImageCreate,
    ) -> PropertyImage:

        return await self.repo.create(
            property_image_data,
        )

    # ========================================================
    # Get Property Image
    # ========================================================

    async def get_property_image(
        self,
        image_id: UUID,
    ) -> PropertyImage:

        return await self._get_property_image_or_404(
            image_id,
        )

    # ========================================================
    # Get All Property Images
    # ========================================================

    async def get_all_property_images(
        self,
    ) -> list[PropertyImage]:

        return await self.repo.get_all()

    # ========================================================
    # Update Property Image
    # ========================================================

    async def update_property_image(
        self,
        image_id: UUID,
        property_image_data: PropertyImageUpdate,
    ) -> PropertyImage:

        property_image = await self._get_property_image_or_404(
            image_id,
        )

        return await self.repo.update(
            property_image,
            property_image_data,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_property_image_or_404(
        self,
        image_id: UUID,
    ) -> PropertyImage:

        property_image = await self.repo.get_by_id(
            image_id,
        )

        if property_image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property image not found.",
            )

        return property_image