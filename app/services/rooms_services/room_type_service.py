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

from app.models.rooms_models.room_type import RoomType

from app.repositories.rooms_repositories.room_type_repository import (
    RoomTypeRepository,
)

from app.schema.rooms_schemas.room_type_schema import (
    RoomTypeCreate,
    RoomTypeUpdate,
)


# ============================================================
# Room Type Service
# ============================================================

class RoomTypeService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = RoomTypeRepository(db)

    # ========================================================
    # Create Room Type
    # ========================================================

    async def create(
        self,
        request: RoomTypeCreate,
    ) -> RoomType:

        existing_room_type = await self.repo.get_by_name(
            property_id=request.property_id,
            name=request.name,
        )

        if existing_room_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room type already exists for this property.",
            )

        room_type = RoomType(
            **request.model_dump(),
        )

        return await self.repo.create(
            room_type,
        )

    # ========================================================
    # Get All Room Types
    # ========================================================

    async def get_all(
        self,
    ) -> list[RoomType]:

        return await self.repo.get_all()

    # ========================================================
    # Get Room Type
    # ========================================================

    async def get_by_id(
        self,
        room_type_id: UUID,
    ) -> RoomType:

        return await self._get_room_type_or_404(
            room_type_id,
        )

    # ========================================================
    # Get Room Types By Property
    # ========================================================

    async def get_by_property(
        self,
        property_id: UUID,
    ) -> list[RoomType]:

        return await self.repo.get_by_property(
            property_id,
        )

    # ========================================================
    # Update Room Type
    # ========================================================

    async def update(
        self,
        room_type_id: UUID,
        request: RoomTypeUpdate,
    ) -> RoomType:

        room_type = await self._get_room_type_or_404(
            room_type_id,
        )

        if (
            request.name
            and request.name != room_type.name
        ):
            existing = await self.repo.get_by_name(
                property_id=room_type.property_id,
                name=request.name,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Room type already exists for this property.",
                )

        return await self.repo.update(
            room_type,
            request,
        )

    # ========================================================
    # Delete Room Type
    # ========================================================

    async def delete(
        self,
        room_type_id: UUID,
    ) -> None:

        room_type = await self._get_room_type_or_404(
            room_type_id,
        )

        await self.repo.delete(
            room_type,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_room_type_or_404(
        self,
        room_type_id: UUID,
    ) -> RoomType:

        room_type = await self.repo.get_by_id(
            room_type_id,
        )

        if room_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room type not found.",
            )

        return room_type