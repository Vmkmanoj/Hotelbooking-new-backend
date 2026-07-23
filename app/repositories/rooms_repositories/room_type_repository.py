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

from app.models.rooms_models.room_type import RoomType 
from app.schema.rooms_schemas.room_type_schema import RoomTypeUpdate

# ============================================================
# Room Type Repository
# ============================================================

class RoomTypeRepository:
    """
    Repository responsible for Room Type database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Room Type
    # ========================================================

    async def create(
        self,
        room_type: RoomType,
    ) -> RoomType:
        """
        Create a new room type.
        """
        try:
            self.db.add(room_type)

            await self.db.commit()
            await self.db.refresh(room_type)

            return room_type

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Room Type By ID
    # ========================================================

    async def get_by_id(
        self,
        room_type_id: UUID,
    ) -> RoomType | None:
        """
        Retrieve a room type by its ID.
        """
        try:
            result = await self.db.execute(
                select(RoomType).where(
                    RoomType.id == room_type_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Room Type By Name
    # ========================================================

    async def get_by_name(
        self,
        property_id: UUID,
        name: str,
    ) -> RoomType | None:
        """
        Retrieve a room type by name within a property.
        """
        try:
            result = await self.db.execute(
                select(RoomType).where(
                    RoomType.property_id == property_id,
                    RoomType.name == name,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Room Types By Property
    # ========================================================

    async def get_by_property(
        self,
        property_id: UUID,
    ) -> list[RoomType]:
        """
        Retrieve all room types of a property.
        """
        try:
            result = await self.db.execute(
                select(RoomType)
                .where(
                    RoomType.property_id == property_id,
                )
                .order_by(
                    RoomType.name.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get All Room Types
    # ========================================================

    async def get_all(
        self,
    ) -> list[RoomType]:
        """
        Retrieve all room types.
        """
        try:
            result = await self.db.execute(
                select(RoomType)
                .order_by(
                    RoomType.created_at.desc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Save Room Type
    # ========================================================

    async def save(
        self,
        room_type: RoomType,
    ) -> RoomType:
        """
        Persist changes to a room type.
        """
        try:
            await self.db.commit()
            await self.db.refresh(room_type)

            return room_type

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Room Type
    # ========================================================

    async def delete(
        self,
        room_type: RoomType,
    ) -> None:
        """
        Delete a room type.
        """
        try:
            await self.db.delete(room_type)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Room Types With Available Rooms
    # ========================================================

    async def get_available_room_types(
        self,
        property_id: UUID,
    ) -> list[RoomType]:
        """
        Retrieve all room types of a property.

        Used by property details and booking pages.
        """
        try:
            result = await self.db.execute(
                select(RoomType)
                .where(
                    RoomType.property_id == property_id,
                )
                .order_by(
                    RoomType.base_price.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise


    async def update(
        self,
        room_type: RoomType,
        room_type_data: RoomTypeUpdate,
    ) -> RoomType:

        update_data = room_type_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                room_type,
                field,
                value,
            )

        await self.db.commit()
        await self.db.refresh(room_type)

        return room_type