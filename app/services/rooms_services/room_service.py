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

from app.models.rooms_models.room import Room
from app.models.rooms_models.room_type import RoomType
from app.models.users_models.users import User

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

from app.repositories.rooms_repositories.room_repository import (
    RoomRepository,
)

from app.repositories.rooms_repositories.room_type_repository import (
    RoomTypeRepository,
)

from app.schema.rooms_schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
)


# ============================================================
# Room Service
# ============================================================

class RoomService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = RoomRepository(db)
        self.room_type_repo = RoomTypeRepository(db)
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Room
    # ========================================================

    async def create_room(
        self,
        request: RoomCreate,
        current_user: User,
    ) -> Room:

        room_type = await self._validate_room_type_owner(
            room_type_id=request.room_type_id,
            current_user=current_user,
        )

        existing = await self.repo.get_by_room_number(
            property_id=room_type.property_id,
            room_number=request.room_number,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room number already exists.",
            )

        room = Room(
            **request.model_dump(),
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(room)

    # ========================================================
    # Get All Rooms
    # ========================================================

    async def get_all_rooms(
        self,
        current_user: User,
    ) -> list[Room]:

        # Optional:
        # If SUPER_ADMIN -> return every room.
        # Otherwise you can later filter by owner.
        return await self.repo.get_all()

    # ========================================================
    # Get Room
    # ========================================================

    async def get_room(
        self,
        room_id: UUID,
        current_user: User,
    ) -> Room:

        room = await self._get_room_or_404(room_id)

        room_type = await self.room_type_repo.get_by_id(
            room.room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        return room

    # ========================================================
    # Get Rooms By Room Type
    # ========================================================

    async def get_rooms_by_room_type(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> list[Room]:

        room_type = await self._validate_room_type_owner(
            room_type_id=room_type_id,
            current_user=current_user,
        )

        return await self.repo.get_by_room_type_id(
            room_type.id,
        )

    # ========================================================
    # Update Room
    # ========================================================

    async def update_room(
        self,
        room_id: UUID,
        request: RoomUpdate,
        current_user: User,
    ) -> Room:

        room = await self._get_room_or_404(
            room_id,
        )

        room_type = await self.room_type_repo.get_by_id(
            room.room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        if (
            request.room_number
            and request.room_number != room.room_number
        ):

            existing = await self.repo.get_by_room_number(
                property_id=room_type.property_id,
                room_number=request.room_number,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Room number already exists.",
                )

        room.updated_by = current_user.email

        return await self.repo.update(
            room,
            request,
        )

    # ========================================================
    # Delete Room
    # ========================================================

    async def delete_room(
        self,
        room_id: UUID,
        current_user: User,
    ) -> None:

        room = await self._get_room_or_404(
            room_id,
        )

        room_type = await self.room_type_repo.get_by_id(
            room.room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        await self.repo.delete(room)

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_room_or_404(
        self,
        room_id: UUID,
    ) -> Room:

        room = await self.repo.get_by_id(
            room_id,
        )

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found.",
            )

        return room

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

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        return room_type

    async def _validate_property_owner(
        self,
        property_id: UUID,
        current_user: User,
    ):

        property_obj = await self.property_repo.get_by_id(
            property_id,
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
                detail="You are not allowed to manage rooms for this property.",
            )

        return property_obj