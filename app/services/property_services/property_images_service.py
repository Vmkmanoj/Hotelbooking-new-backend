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

from app.common.enums.user_enums.role_name import (
    RoleName,
)

from app.models.property_models.property import Property
from app.models.property_models.property_image import PropertyImage
from app.models.users_models.users import User

from app.repositories.property_repositories.property_images_repository import (
    PropertyImageRepository,
)

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
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
        self.image_repo = PropertyImageRepository(db)
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Property Image
    # ========================================================

    async def create_property_image(
        self,
        property_id: UUID,
        image_data: PropertyImageCreate,
        current_user: User,
    ) -> PropertyImage:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        if image_data.is_cover:
            await self.image_repo.clear_cover_image(
                property_id,
            )

        property_image = PropertyImage(
            property_id=property_id,
            image_url=image_data.image_url,
            caption=image_data.caption,
            is_cover=image_data.is_cover,
            display_order=image_data.display_order,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.image_repo.create(
            property_image,
        )

    # ========================================================
    # Get Property Image
    # ========================================================

    async def get_property_image(
        self,
        image_id: UUID,
        current_user: User,
    ) -> PropertyImage:

        image = await self._get_property_image_or_404(
            image_id,
        )

        property_obj = await self._get_property_or_404(
            image.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        return image

    # ========================================================
    # Get Property Images
    # ========================================================

    async def get_property_images(
        self,
        property_id: UUID,
        current_user: User,
    ) -> list[PropertyImage]:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        return await self.image_repo.get_by_property_id(
            property_id,
        )

    # ========================================================
    # Update Property Image
    # ========================================================

    async def update_property_image(
        self,
        image_id: UUID,
        image_data: PropertyImageUpdate,
        current_user: User,
    ) -> PropertyImage:

        image = await self._get_property_image_or_404(
            image_id,
        )

        property_obj = await self._get_property_or_404(
            image.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        if image_data.is_cover:
            await self.image_repo.clear_cover_image(
                image.property_id,
            )

        image.updated_by = current_user.email

        return await self.image_repo.update(
            image,
            image_data,
        )

    # ========================================================
    # Delete Property Image
    # ========================================================

    async def delete_property_image(
        self,
        image_id: UUID,
        current_user: User,
    ) -> None:

        image = await self._get_property_image_or_404(
            image_id,
        )

        property_obj = await self._get_property_or_404(
            image.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        await self.image_repo.delete(
            image,
        )

    # ========================================================
    # Property Helper
    # ========================================================

    async def _get_property_or_404(
        self,
        property_id: UUID,
    ) -> Property:

        property_obj = await self.property_repo.get_by_id(
            property_id,
        )

        if property_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        return property_obj

    # ========================================================
    # Image Helper
    # ========================================================

    async def _get_property_image_or_404(
        self,
        image_id: UUID,
    ) -> PropertyImage:

        image = await self.image_repo.get_by_id(
            image_id,
        )

        if image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property image not found.",
            )

        return image

    # ========================================================
    # Authorization
    # ========================================================

    def _validate_property_access(
        self,
        property_obj: Property,
        current_user: User,
    ) -> None:

        if current_user.role.name == RoleName.SUPER_ADMIN.value:
            return

        if property_obj.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to manage this property.",
            )