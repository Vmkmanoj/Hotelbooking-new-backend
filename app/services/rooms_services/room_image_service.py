# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.rooms_models.room_image import RoomImage

from app.repositories.rooms_repositories.room_image_repository import (
    RoomImageRepository,
)
from app.repositories.rooms_repositories.room_repository import (
    RoomRepository,
)

from app.schema.rooms_schemas.room_image_schema import (
    RoomImageCreate,
    RoomImageUpdate,
)


# ============================================================
# Room Image Service
# ============================================================

class RoomImageService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = RoomImageRepository(db)
        self.room_repo = RoomRepository(db)

    # ========================================================
    # Create Room Image
    # ========================================================

    async def create(
        self,
        request: RoomImageCreate,
    ) -> RoomImage:

        room = await self.room_repo.get_by_id(
            request.room_id,
        )

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found.",
            )

        if request.is_primary:

            existing_primary = await self.repo.get_primary_image(
                request.room_id,
            )

            if existing_primary:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Primary image already exists for this room.",
                )

        room_image = RoomImage(
            **request.model_dump(),
        )

        return await self.repo.create(
            room_image,
        )

    # ========================================================
    # Get Room Image
    # ========================================================

    async def get_by_id(
        self,
        image_id: UUID,
    ) -> RoomImage:

        return await self._get_room_image_or_404(
            image_id,
        )

    # ========================================================
    # Get Images By Room
    # ========================================================

    async def get_by_room(
        self,
        room_id: UUID,
    ) -> list[RoomImage]:

        return await self.repo.get_by_room(
            room_id,
        )

    # ========================================================
    # Get All Images
    # ========================================================

    async def get_all(
        self,
    ) -> list[RoomImage]:

        return await self.repo.get_all()

    # ========================================================
    # Update Room Image
    # ========================================================

    async def update(
        self,
        image_id: UUID,
        request: RoomImageUpdate,
    ) -> RoomImage:

        room_image = await self._get_room_image_or_404(
            image_id,
        )

        if request.is_primary:

            existing_primary = await self.repo.get_primary_image(
                room_image.room_id,
            )

            if (
                existing_primary
                and existing_primary.id != room_image.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Primary image already exists for this room.",
                )

        return await self.repo.update(
            room_image,
            request,
        )

    # ========================================================
    # Delete Room Image
    # ========================================================

    async def delete(
        self,
        image_id: UUID,
    ) -> None:

        room_image = await self._get_room_image_or_404(
            image_id,
        )

        await self.repo.delete(
            room_image,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_room_image_or_404(
        self,
        image_id: UUID,
    ) -> RoomImage:

        room_image = await self.repo.get_by_id(
            image_id,
        )

        if room_image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room image not found.",
            )

        return room_image