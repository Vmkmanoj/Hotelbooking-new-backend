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

from app.models.rooms_models.room_type import RoomType
from app.models.users_models.users import User

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

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
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Room Type
    # ========================================================

    async def create_room_type(
        self,
        request: RoomTypeCreate,
        current_user: User,
    ) -> RoomType:

        property_obj = await self._validate_property_owner(
            property_id=request.property_id,
            current_user=current_user,
        )

        existing_room_type = await self.repo.get_by_name(
            property_id=property_obj.id,
            room_name=request.room_name,
        )

        if existing_room_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room type already exists for this property.",
            )

        room_type = RoomType(
            **request.model_dump(),
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            room_type,
        )

    # ========================================================
    # Get All Room Types
    # ========================================================

    async def get_all_room_types(
        self,
        current_user: User,
    ) -> list[RoomType]:

        return await self.repo.get_all()

    # ========================================================
    # Get Room Type
    # ========================================================

    async def get_room_type(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> RoomType:

        room_type = await self._get_room_type_or_404(
            room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        return room_type

    # ========================================================
    # Get Room Types By Property
    # ========================================================

    async def get_room_types_by_property(
        self,
        property_id: UUID,
        current_user: User,
    ) -> list[RoomType]:

        await self._validate_property_owner(
            property_id=property_id,
            current_user=current_user,
        )

        return await self.repo.get_by_property_id(
            property_id,
        )

    # ========================================================
    # Update Room Type
    # ========================================================

    async def update_room_type(
        self,
        room_type_id: UUID,
        request: RoomTypeUpdate,
        current_user: User,
    ) -> RoomType:

        room_type = await self._get_room_type_or_404(
            room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
        )

        if (
            request.room_name
            and request.room_name != room_type.room_name
        ):
            existing = await self.repo.get_by_name(
                property_id=room_type.property_id,
                room_name=request.room_name,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Room type already exists for this property.",
                )

        room_type.updated_by = current_user.email

        return await self.repo.update(
            room_type,
            request,
        )

    # ========================================================
    # Delete Room Type
    # ========================================================

    async def delete_room_type(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> None:

        room_type = await self._get_room_type_or_404(
            room_type_id,
        )

        await self._validate_property_owner(
            property_id=room_type.property_id,
            current_user=current_user,
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

    # ========================================================
    # Validate Property Owner
    # ========================================================

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
                detail="You are not allowed to manage this property's room types.",
            )

        return property_obj