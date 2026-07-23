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
    Repository responsible for Room Image database operations.
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
        """
        Create a new room image.
        """
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
        """
        Retrieve a room image by its ID.
        """
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
    # Get Images By Room
    # ========================================================

    async def get_by_room(
        self,
        room_id: UUID,
    ) -> list[RoomImage]:
        """
        Retrieve all images belonging to a room.
        """
        try:
            result = await self.db.execute(
                select(RoomImage)
                .where(
                    RoomImage.room_id == room_id,
                )
                .order_by(
                    RoomImage.created_at.asc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Primary Image
    # ========================================================

    async def get_primary_image(
        self,
        room_id: UUID,
    ) -> RoomImage | None:
        """
        Retrieve the primary image for a room.
        """
        try:
            result = await self.db.execute(
                select(RoomImage).where(
                    RoomImage.room_id == room_id,
                    RoomImage.is_primary.is_(True),
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
        """
        Retrieve all room images.
        """
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
    # Remove Existing Primary Image
    # ========================================================

    async def clear_primary_image(
        self,
        room_id: UUID,
    ) -> None:
        """
        Remove the current primary image for a room.
        """
        try:
            image = await self.get_primary_image(room_id)

            if image:
                image.is_primary = False
                await self.db.flush()

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Save Room Image
    # ========================================================

    async def save(
        self,
        room_image: RoomImage,
    ) -> RoomImage:
        """
        Persist changes to a room image.
        """
        try:
            await self.db.commit()
            await self.db.refresh(room_image)

            return room_image

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def update(
        self,
        room_image: RoomImage,
        room_image_data: RoomImageUpdate,
    ) -> RoomImage:

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
    
    # ========================================================
    # Delete Room Image
    # ========================================================

    async def delete(
        self,
        room_image: RoomImage,
    ) -> None:
        """
        Delete a room image.
        """
        try:
            await self.db.delete(room_image)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise