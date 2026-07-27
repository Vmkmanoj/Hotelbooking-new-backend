# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.property_models.property import Property
from app.models.property_models.property_image import PropertyImage

from app.schema.property_schema.property_images_schema import (
    PropertyImageUpdate,
)


# ============================================================
# Property Image Repository
# ============================================================

class PropertyImageRepository:
    """
    Repository responsible for Property Image database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Property Image
    # ========================================================

    async def create(
        self,
        property_image: PropertyImage,
    ) -> PropertyImage:
        """
        Persist a property image.
        """
        try:
            self.db.add(property_image)

            await self.db.commit()

            await self.db.refresh(property_image)

            return property_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Image By ID
    # ========================================================

    async def get_by_id(
        self,
        image_id: UUID,
    ) -> PropertyImage | None:
        """
        Retrieve a property image by ID.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage).where(
                    PropertyImage.id == image_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Images By Property
    # ========================================================

    async def get_by_property_id(
        self,
        property_id: UUID,
    ) -> list[PropertyImage]:
        """
        Retrieve all images belonging to an active property.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage)
                .join(
                    Property,
                    Property.id == PropertyImage.property_id,
                )
                .where(
                    PropertyImage.property_id == property_id,
                    Property.is_deleted.is_(False),
                )
                .order_by(
                    PropertyImage.display_order.asc(),
                    PropertyImage.created_at.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Cover Image
    # ========================================================

    async def get_cover_image(
        self,
        property_id: UUID,
    ) -> PropertyImage | None:
        """
        Retrieve the cover image of an active property.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage)
                .join(
                    Property,
                    Property.id == PropertyImage.property_id,
                )
                .where(
                    PropertyImage.property_id == property_id,
                    PropertyImage.is_cover.is_(True),
                    Property.is_deleted.is_(False),
                )
                .order_by(
                    PropertyImage.display_order.asc(),
                    PropertyImage.created_at.asc(),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Clear Existing Cover Image
    # ========================================================

    async def clear_cover_image(
        self,
        property_id: UUID,
    ) -> None:
        """
        Ensure only one cover image exists per property.
        """

        result = await self.db.execute(
            select(PropertyImage).where(
                PropertyImage.property_id == property_id,
                PropertyImage.is_cover.is_(True),
            )
        )

        cover_image = result.scalar_one_or_none()

        if cover_image:
            cover_image.is_cover = False

            await self.db.flush()

    # ========================================================
    # Get All Images
    # ========================================================

    async def get_all(
        self,
    ) -> list[PropertyImage]:
        """
        Retrieve all images.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage)
                .order_by(
                    PropertyImage.display_order.asc(),
                    PropertyImage.created_at.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Update Property Image
    # ========================================================

    async def update(
        self,
        property_image: PropertyImage,
        property_image_data: PropertyImageUpdate,
    ) -> PropertyImage:
        """
        Update a property image.
        """
        try:
            update_data = property_image_data.model_dump(
                exclude_unset=True,
            )

            for key, value in update_data.items():
                setattr(
                    property_image,
                    key,
                    value,
                )

            await self.db.commit()

            await self.db.refresh(property_image)

            return property_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Property Image
    # ========================================================

    async def delete(
        self,
        property_image: PropertyImage,
    ) -> None:
        """
        Delete a property image.
        """
        try:
            await self.db.delete(property_image)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise