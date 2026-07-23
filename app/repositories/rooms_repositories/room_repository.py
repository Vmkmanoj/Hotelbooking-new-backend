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

from app.common.enums.room_enums.room_status import RoomStatus

from app.models.rooms_models.room import Room
from app.models.rooms_models.room_type import RoomType

from app.schema.rooms_schemas.room_schema import RoomUpdate


# ============================================================
# Room Repository
# ============================================================

class RoomRepository:
    """
    Repository responsible for Room database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Room
    # ========================================================

    async def create(
        self,
        room: Room,
    ) -> Room:

        try:
            self.db.add(room)

            await self.db.commit()
            await self.db.refresh(room)

            return room

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Room By ID
    # ========================================================

    async def get_by_id(
        self,
        room_id: UUID,
    ) -> Room | None:

        try:
            result = await self.db.execute(
                select(Room).where(
                    Room.id == room_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Room By Number (Within Property)
    # ========================================================

    async def get_by_room_number(
        self,
        property_id: UUID,
        room_number: str,
    ) -> Room | None:

        try:
            result = await self.db.execute(
                select(Room)
                .join(
                    RoomType,
                    Room.room_type_id == RoomType.id,
                )
                .where(
                    Room.room_number == room_number,
                    RoomType.property_id == property_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Rooms By Room Type
    # ========================================================

    async def get_by_room_type(
        self,
        room_type_id: UUID,
    ) -> list[Room]:

        try:
            result = await self.db.execute(
                select(Room)
                .where(
                    Room.room_type_id == room_type_id,
                )
                .order_by(
                    Room.room_number.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Available Rooms
    # ========================================================

    async def get_available_rooms(
        self,
        room_type_id: UUID,
    ) -> list[Room]:

        try:
            result = await self.db.execute(
                select(Room)
                .where(
                    Room.room_type_id == room_type_id,
                    Room.status == RoomStatus.AVAILABLE,
                )
                .order_by(
                    Room.room_number.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get All Rooms
    # ========================================================

    async def get_all(
        self,
    ) -> list[Room]:

        try:
            result = await self.db.execute(
                select(Room)
                .order_by(
                    Room.created_at.desc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Update Room
    # ========================================================

    async def update(
        self,
        room: Room,
        room_data: RoomUpdate,
    ) -> Room:

        try:
            update_data = room_data.model_dump(
                exclude_unset=True,
            )

            for field, value in update_data.items():
                setattr(
                    room,
                    field,
                    value,
                )

            await self.db.commit()
            await self.db.refresh(room)

            return room

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Room
    # ========================================================

    async def delete(
        self,
        room: Room,
    ) -> None:

        try:
            await self.db.delete(room)
            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise