from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property_models.property_amenity import (
    PropertyAmenity,
)

from app.schema.property_schema.property_amenities_schema import (
    PropertyAmenityCreate,
    PropertyAmenityUpdate,
)


class PropertyAmenityRepository:
    """
    Repository responsible for Property-Amenity mapping operations.
    """

    @staticmethod
    async def create(
        db: AsyncSession,
        property_amenity_data: PropertyAmenityCreate,
    ) -> PropertyAmenity:
        """
        Create a property-amenity mapping.
        """
        try:
            property_amenity = PropertyAmenity(
                **property_amenity_data.model_dump()
            )

            db.add(property_amenity)

            await db.commit()
            await db.refresh(property_amenity)

            return property_amenity

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        property_amenity_id: UUID,
    ) -> PropertyAmenity | None:
        """
        Retrieve a property-amenity mapping by ID.
        """
        try:
            result = await db.execute(
                select(PropertyAmenity).where(
                    PropertyAmenity.id == property_amenity_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_by_property_and_amenity(
        db: AsyncSession,
        property_id: UUID,
        amenity_id: UUID,
    ) -> PropertyAmenity | None:
        """
        Retrieve a mapping using property and amenity IDs.
        """
        try:
            result = await db.execute(
                select(PropertyAmenity).where(
                    PropertyAmenity.property_id == property_id,
                    PropertyAmenity.amenity_id == amenity_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[PropertyAmenity]:
        """
        Retrieve all property-amenity mappings.
        """
        try:
            result = await db.execute(
                select(PropertyAmenity)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def update(
        db: AsyncSession,
        property_amenity: PropertyAmenity,
        property_amenity_data: PropertyAmenityUpdate,
    ) -> PropertyAmenity:
        """
        Update a property-amenity mapping.
        """
        try:
            update_data = property_amenity_data.model_dump(
                exclude_unset=True
            )

            for key, value in update_data.items():
                setattr(property_amenity, key, value)

            await db.commit()
            await db.refresh(property_amenity)

            return property_amenity

        except SQLAlchemyError:
            await db.rollback()
            raise

    async def get_by_property_and_amenity(
        self,
        property_id: UUID,
        amenity_id: UUID,
    ) -> PropertyAmenity | None:

        result = await self.db.execute(
            select(PropertyAmenity).where(
                PropertyAmenity.property_id == property_id,
                PropertyAmenity.amenity_id == amenity_id,
            )
        )

        return result.scalar_one_or_none()

    # Optional
    # @staticmethod
    # async def delete(
    #     db: AsyncSession,
    #     property_amenity: PropertyAmenity,
    # ) -> None:
    #     try:
    #         await db.delete(property_amenity)
    #         await db.commit()
    #
    #     except SQLAlchemyError:
    #         await db.rollback()
    #         raise