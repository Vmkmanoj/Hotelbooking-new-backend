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

from app.models.rooms_models.room_amenity import RoomAmenity

from app.repositories.rooms_repositories.room_amenity_repository import (
    RoomAmenityRepository,
)
from app.repositories.rooms_repositories.room_type_repository import (
    RoomTypeRepository,
)
from app.repositories.property_repositories.amenity_repository import (
    AmenityRepository,
)

from app.schema.rooms_schemas.room_amenity_schema import (
    RoomAmenityCreate,
)


# ============================================================
# Room Amenity Service
# ============================================================

class RoomAmenityService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = RoomAmenityRepository(db)
        self.room_type_repo = RoomTypeRepository(db)
        self.amenity_repo = AmenityRepository(db)

    # ========================================================
    # Create Room Amenity Mapping
    # ========================================================

    async def create(
        self,
        request: RoomAmenityCreate,
    ) -> RoomAmenity:

        room_type = await self.room_type_repo.get_by_id(
            request.room_type_id,
        )

        if room_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room type not found.",
            )

        amenity = await self.amenity_repo.get_by_id(
            request.amenity_id,
        )

        if amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Amenity not found.",
            )

        exists = await self.repo.exists(
            request.room_type_id,
            request.amenity_id,
        )

        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity is already mapped to this room type.",
            )

        room_amenity = RoomAmenity(
            **request.model_dump(),
        )

        return await self.repo.create(
            room_amenity,
        )

    # ========================================================
    # Get Mapping
    # ========================================================

    async def get_by_id(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
    ) -> RoomAmenity:

        return await self._get_room_amenity_or_404(
            room_type_id,
            amenity_id,
        )

    # ========================================================
    # Get Amenities By Room Type
    # ========================================================

    async def get_by_room_type(
        self,
        room_type_id: UUID,
    ) -> list[RoomAmenity]:

        return await self.repo.get_by_room_type(
            room_type_id,
        )

    # ========================================================
    # Delete Mapping
    # ========================================================

    async def delete(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
    ) -> None:

        room_amenity = await self._get_room_amenity_or_404(
            room_type_id,
            amenity_id,
        )

        await self.repo.delete(
            room_amenity,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_room_amenity_or_404(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
    ) -> RoomAmenity:

        room_amenity = await self.repo.get_by_id(
            room_type_id,
            amenity_id,
        )

        if room_amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room amenity mapping not found.",
            )

        return room_amenity