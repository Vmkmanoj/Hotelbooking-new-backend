from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property_models.property_image import PropertyImage

from app.schema.property_schema.property_images_schema import (
    PropertyImageCreate,
    PropertyImageUpdate,
)


class PropertyImageRepository:
    """
    Repository responsible for Property Image database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        property_image_data: PropertyImageCreate,
    ) -> PropertyImage:
        """
        Create a property image.
        """
        try:
            property_image = PropertyImage(
                **property_image_data.model_dump()
            )

            self.db.add(property_image)

            await self.db.commit()
            await self.db.refresh(property_image)

            return property_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

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
                    PropertyImage.id == image_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def get_by_property_id(
        self,
        property_id: UUID,
    ) -> list[PropertyImage]:
        """
        Retrieve all images of a property ordered by display order.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage)
                .where(
                    PropertyImage.property_id == property_id
                )
                .order_by(PropertyImage.display_order)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    async def get_primary_image(
        self,
        property_id: UUID,
    ) -> PropertyImage | None:
        """
        Retrieve the primary image of a property.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage).where(
                    PropertyImage.property_id == property_id,
                    PropertyImage.is_primary.is_(True),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def get_cover_image(
        self,
        property_id: UUID,
    ) -> PropertyImage | None:
        """
        Retrieve the cover image of a property.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage).where(
                    PropertyImage.property_id == property_id,
                    PropertyImage.is_cover.is_(True),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def get_all(
        self,
    ) -> list[PropertyImage]:
        """
        Retrieve all property images.
        """
        try:
            result = await self.db.execute(
                select(PropertyImage)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

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
                exclude_unset=True
            )

            for key, value in update_data.items():
                setattr(property_image, key, value)

            await self.db.commit()
            await self.db.refresh(property_image)

            return property_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # Optional
    # @staticmethod
    # async def delete(
    #     db: AsyncSession,
    #     property_image: PropertyImage,
    # ) -> None:
    #     try:
    #         await db.delete(property_image)
    #         await db.commit()
    #
    #     except SQLAlchemyError:
    #         await db.rollback()
    #         raise