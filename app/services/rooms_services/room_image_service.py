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

from app.models.rooms_models.room_image import RoomImage
from app.models.rooms_models.room_type import RoomType
from app.models.users_models.users import User

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

from app.repositories.rooms_repositories.room_image_repository import (
    RoomImageRepository,
)

from app.repositories.rooms_repositories.room_type_repository import (
    RoomTypeRepository,
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
        self.room_type_repo = RoomTypeRepository(db)
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Room Image
    # ========================================================

    async def create_room_image(
        self,
        room_type_id: UUID,
        request: RoomImageCreate,
        current_user: User,
    ) -> RoomImage:

        room_type = await self._validate_room_type_owner(
            room_type_id=room_type_id,
            current_user=current_user,
        )

        if request.is_cover:

            existing_cover = await self.repo.get_cover_image(
                room_type.id,
            )

            if existing_cover:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cover image already exists for this room type.",
                )

        room_image = RoomImage(
            room_type_id=room_type.id,
            **request.model_dump(),
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            room_image,
        )

    # ========================================================
    # Get Room Image
    # ========================================================

    async def get_room_image(
        self,
        image_id: UUID,
        current_user: User,
    ) -> RoomImage:

        room_image = await self._get_room_image_or_404(
            image_id,
        )

        await self._validate_room_type_owner(
            room_type_id=room_image.room_type_id,
            current_user=current_user,
        )

        return room_image

    # ========================================================
    # Get Images Of Room Type
    # ========================================================

    async def get_room_images(
        self,
        room_type_id: UUID,
        current_user: User,
    ) -> list[RoomImage]:

        await self._validate_room_type_owner(
            room_type_id=room_type_id,
            current_user=current_user,
        )

        return await self.repo.get_by_room_type_id(
            room_type_id,
        )

    # ========================================================
    # Update Room Image
    # ========================================================

    async def update_room_image(
        self,
        image_id: UUID,
        request: RoomImageUpdate,
        current_user: User,
    ) -> RoomImage:

        room_image = await self._get_room_image_or_404(
            image_id,
        )

        await self._validate_room_type_owner(
            room_type_id=room_image.room_type_id,
            current_user=current_user,
        )

        if request.is_cover:

            existing_cover = await self.repo.get_cover_image(
                room_image.room_type_id,
            )

            if (
                existing_cover
                and existing_cover.id != room_image.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cover image already exists for this room type.",
                )

        room_image.updated_by = current_user.email

        return await self.repo.update(
            room_image,
            request,
        )

    # ========================================================
    # Delete Room Image
    # ========================================================

    async def delete_room_image(
        self,
        image_id: UUID,
        current_user: User,
    ) -> None:

        room_image = await self._get_room_image_or_404(
            image_id,
        )

        await self._validate_room_type_owner(
            room_type_id=room_image.room_type_id,
            current_user=current_user,
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
                detail="You are not allowed to manage images for this room type.",
            )

        return room_type