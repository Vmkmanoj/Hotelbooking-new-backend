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

from app.models.rooms_models.room_image import RoomImage
from app.schema.rooms_schemas.room_image_schema import RoomImageUpdate


# ============================================================
# Room Image Repository
# ============================================================

class RoomImageRepository:
    """
    Repository responsible for Room Type Image database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Room Image
    # ========================================================

    async def create(
        self,
        room_image: RoomImage,
    ) -> RoomImage:

        try:
            self.db.add(room_image)

            await self.db.commit()
            await self.db.refresh(room_image)

            return room_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Image By ID
    # ========================================================

    async def get_by_id(
        self,
        room_image_id: UUID,
    ) -> RoomImage | None:

        try:
            result = await self.db.execute(
                select(RoomImage).where(
                    RoomImage.id == room_image_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Images By Room Type
    # ========================================================

    async def get_by_room_type_id(
        self,
        room_type_id: UUID,
    ) -> list[RoomImage]:

        try:
            result = await self.db.execute(
                select(RoomImage)
                .where(
                    RoomImage.room_type_id == room_type_id,
                )
                .order_by(
                    RoomImage.display_order.asc(),
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
        room_type_id: UUID,
    ) -> RoomImage | None:

        try:
            result = await self.db.execute(
                select(RoomImage).where(
                    RoomImage.room_type_id == room_type_id,
                    RoomImage.is_cover.is_(True),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get All Images
    # ========================================================

    async def get_all(
        self,
    ) -> list[RoomImage]:

        try:
            result = await self.db.execute(
                select(RoomImage)
                .order_by(
                    RoomImage.created_at.desc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Clear Cover Image
    # ========================================================

    async def clear_cover_image(
        self,
        room_type_id: UUID,
    ) -> None:

        try:
            image = await self.get_cover_image(
                room_type_id,
            )

            if image:
                image.is_cover = False
                await self.db.flush()

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Update Room Image
    # ========================================================

    async def update(
        self,
        room_image: RoomImage,
        room_image_data: RoomImageUpdate,
    ) -> RoomImage:

        try:
            update_data = room_image_data.model_dump(
                exclude_unset=True,
            )

            for field, value in update_data.items():
                setattr(
                    room_image,
                    field,
                    value,
                )

            await self.db.commit()
            await self.db.refresh(room_image)

            return room_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Room Image
    # ========================================================

    async def delete(
        self,
        room_image: RoomImage,
    ) -> None:

        try:
            await self.db.delete(
                room_image,
            )

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise