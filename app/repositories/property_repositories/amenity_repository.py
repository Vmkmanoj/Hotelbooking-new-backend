from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property_models.amenities import Amenity

from app.schema.property_schema.amenity_schema import (
    AmenityCreate,
    AmenityUpdate,
)


class AmenityRepository:
    """
    Repository responsible for Amenity database operations.
    """

    @staticmethod
    async def create(
        db: AsyncSession,
        amenity_data: AmenityCreate,
    ) -> Amenity:
        """
        Create a new amenity.
        """
        try:
            amenity = Amenity(
                **amenity_data.model_dump()
            )

            db.add(amenity)

            await db.commit()
            await db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        amenity_id: UUID,
    ) -> Amenity | None:
        """
        Retrieve an amenity by its ID.
        """
        try:
            result = await db.execute(
                select(Amenity).where(
                    Amenity.id == amenity_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_by_name(
        db: AsyncSession,
        name: str,
    ) -> Amenity | None:
        """
        Retrieve an amenity by name.
        """
        try:
            result = await db.execute(
                select(Amenity).where(
                    Amenity.name == name
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Amenity]:
        """
        Retrieve all amenities.
        """
        try:
            result = await db.execute(
                select(Amenity)
                .order_by(Amenity.name)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def update(
        db: AsyncSession,
        amenity: Amenity,
        amenity_data: AmenityUpdate,
    ) -> Amenity:
        """
        Update an existing amenity.
        """
        try:
            update_data = amenity_data.model_dump(
                exclude_unset=True
            )

            for key, value in update_data.items():
                setattr(amenity, key, value)

            await db.commit()
            await db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await db.rollback()
            raise

    # Optional
    # @staticmethod
    # async def delete(
    #     db: AsyncSession,
    #     amenity: Amenity,
    # ) -> None:
    #     try:
    #         await db.delete(amenity)
    #         await db.commit()
    #
    #     except SQLAlchemyError:
    #         await db.rollback()
    #         raise