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

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        amenity_data: AmenityCreate,
    ) -> Amenity:
        """
        Create a new amenity.
        """
        try:
            amenity = Amenity(
                **amenity_data.model_dump()
            )

            self.db.add(amenity)

            await self.db.commit()
            await self.db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_id(
        self,
        amenity_id: UUID,
    ) -> Amenity | None:
        """
        Retrieve an amenity by its ID.
        """
        try:
            result = await self.db.execute(
                select(Amenity).where(
                    Amenity.id == amenity_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def get_by_name(
        self,
        name: str,
    ) -> Amenity | None:
        """
        Retrieve an amenity by name.
        """
        try:
            result = await self.db.execute(
                select(Amenity).where(
                    Amenity.name == name
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def get_all(
        self,
    ) -> list[Amenity]:
        """
        Retrieve all amenities.
        """
        try:
            result = await self.db.execute(
                select(Amenity)
                .order_by(Amenity.name)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    async def update(
        self,
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

            await self.db.commit()
            await self.db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await self.db.rollback()
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