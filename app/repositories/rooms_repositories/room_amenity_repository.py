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

from app.models.rooms_models.room_amenity import RoomAmenity


# ============================================================
# Room Amenity Repository
# ============================================================

class RoomAmenityRepository:
    """
    Repository responsible for Room Type ↔ Amenity mappings.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Mapping
    # ========================================================

    async def create(
        self,
        room_amenity: RoomAmenity,
    ) -> RoomAmenity:
        """
        Create a room type ↔ amenity mapping.
        """
        try:
            self.db.add(room_amenity)

            await self.db.commit()
            await self.db.refresh(room_amenity)

            return room_amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Mapping
    # ========================================================

    async def get_by_id(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
    ) -> RoomAmenity | None:
        """
        Retrieve a specific room amenity mapping.
        """
        try:
            result = await self.db.execute(
                select(RoomAmenity).where(
                    RoomAmenity.room_type_id == room_type_id,
                    RoomAmenity.amenity_id == amenity_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Amenities By Room Type
    # ========================================================

    async def get_by_room_type(
        self,
        room_type_id: UUID,
    ) -> list[RoomAmenity]:
        """
        Retrieve all amenities assigned to a room type.
        """
        try:
            result = await self.db.execute(
                select(RoomAmenity)
                .where(
                    RoomAmenity.room_type_id == room_type_id,
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Check Mapping Exists
    # ========================================================

    async def exists(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
    ) -> bool:
        """
        Check whether a room amenity mapping exists.
        """
        try:
            result = await self.db.execute(
                select(RoomAmenity).where(
                    RoomAmenity.room_type_id == room_type_id,
                    RoomAmenity.amenity_id == amenity_id,
                )
            )

            return result.scalar_one_or_none() is not None

        except SQLAlchemyError:
            raise

    # ========================================================
    # Delete Mapping
    # ========================================================

    async def delete(
        self,
        room_amenity: RoomAmenity,
    ) -> None:
        """
        Delete a room amenity mapping.
        """
        try:
            await self.db.delete(room_amenity)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Remove All Amenities
    # ========================================================

    async def delete_by_room_type(
        self,
        room_type_id: UUID,
    ) -> None:
        """
        Remove all amenity mappings for a room type.
        """
        try:
            result = await self.db.execute(
                select(RoomAmenity).where(
                    RoomAmenity.room_type_id == room_type_id,
                )
            )

            for mapping in result.scalars().all():
                await self.db.delete(mapping)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise