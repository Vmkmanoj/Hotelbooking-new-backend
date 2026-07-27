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

from app.common.enums.user_enums.role_name import (
    RoleName,
)

from app.models.property_models.property import Property
from app.models.rooms_models.room_amenity import RoomAmenity
from app.models.rooms_models.room_type import RoomType
from app.models.users_models.users import User

from app.repositories.property_repositories.amenity_repository import (
    AmenityRepository,
)
from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)
from app.repositories.rooms_repositories.room_amenity_repository import (
    RoomAmenityRepository,
)
from app.repositories.rooms_repositories.room_type_repository import (
    RoomTypeRepository,
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
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Room Amenity
    # ========================================================

    async def create_room_amenity(
        self,
        request: RoomAmenityCreate,
        current_user: User,
    ) -> RoomAmenity:

        room_type = await self._validate_room_type_owner(
            room_type_id=request.room_type_id,
            current_user=current_user,
        )

        amenity = await self.amenity_repo.get_by_id(
            request.amenity_id,
        )

        if amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Amenity not found.",
            )

        existing_mapping = await self.repo.exists(
            request.room_type_id,
            request.amenity_id,
        )

        if existing_mapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity is already assigned to this room type.",
            )

        room_amenity = RoomAmenity(
            **request.model_dump(),
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            room_amenity,
        )

    # ========================================================
    # Get Room Amenity
    # ========================================================

    async def get_room_amenity(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
        current_user: User,
    ) -> RoomAmenity:

        await self._validate_room_type_owner(
            room_type_id,
            current_user,
        )

        return await self._get_room_amenity_or_404(
            room_type_id,
            amenity_id,
        )

    # ========================================================
    # Get Room Amenities
    # ========================================================

    async def get_room_amenities(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> list[RoomAmenity]:

        await self._validate_room_type_owner(
            room_type_id,
            current_user,
        )

        return await self.repo.get_by_room_type(
            room_type_id,
        )

    # ========================================================
    # Delete Room Amenity
    # ========================================================

    async def delete_room_amenity(
        self,
        room_type_id: UUID,
        amenity_id: UUID,
        current_user: User,
    ) -> None:

        await self._validate_room_type_owner(
            room_type_id,
            current_user,
        )

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

    async def _validate_room_type_owner(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> RoomType:

        room_type = await self.room_type_repo.get_by_id(
            room_type_id,
        )

        if room_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room type not found.",
            )

        property_obj = await self.property_repo.get_by_id(
            room_type.property_id,
        )

        if property_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        if (
            current_user.role.name != RoleName.SUPER_ADMIN.value
            and property_obj.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to manage this room type.",
            )

        return room_type