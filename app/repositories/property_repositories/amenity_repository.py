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
from sqlalchemy import func

# ============================================================
# Local Imports
# ============================================================

from app.models.property_models.amenities import Amenity

from app.schema.property_schema.amenity_schema import (
    AmenityUpdate,
)


# ============================================================
# Amenity Repository
# ============================================================

class AmenityRepository:
    """
    Repository responsible for Amenity database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Amenity
    # ========================================================

    async def create(
        self,
        amenity: Amenity,
    ) -> Amenity:
        """
        Persist a new amenity.
        """
        try:
            self.db.add(amenity)

            await self.db.commit()

            await self.db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Amenity By ID
    # ========================================================

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
                    Amenity.id == amenity_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Amenity By Name
    # ========================================================

    async def get_by_name(
        self,
        room_name: str,
    ) -> Amenity | None:
        """
        Retrieve an amenity by name.
        """
        try:
            result = await self.db.execute(
                select(Amenity).where(
                    func.lower(Amenity.name) == room_name.lower(),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get All Amenities
    # ========================================================

    async def get_all(
        self,
    ) -> list[Amenity]:
        """
        Retrieve all amenities.
        """
        try:
            result = await self.db.execute(
                select(Amenity)
                .order_by(
                    Amenity.name,
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Update Amenity
    # ========================================================

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
                exclude_unset=True,
            )

            for key, value in update_data.items():
                setattr(
                    amenity,
                    key,
                    value,
                )

            await self.db.commit()

            await self.db.refresh(amenity)

            return amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Amenity
    # ========================================================

    async def delete(
        self,
        amenity: Amenity,
    ) -> None:
        """
        Permanently delete an amenity.
        """
        try:
            await self.db.delete(amenity)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise