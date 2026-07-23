from uuid import UUID

from app.models.rooms_models.room import Room
from app.repositories.rooms_repositories.room_repository import RoomRepository

from app.schema.rooms_schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
)


class RoomService:

    def __init__(
        self,
        repository: RoomRepository,
    ):
        self.repository = repository

    # =====================================================
    # Create Room
    # =====================================================

    async def create_room(
        self,
        request: RoomCreate,
    ) -> Room:

        room = Room(
            **request.model_dump(),
        )

        return await self.repository.create(
            room,
        )

    # =====================================================
    # Get Room
    # =====================================================

    async def get_room(
        self,
        room_id: UUID,
    ) -> Room | None:

        return await self.repository.get_by_id(
            room_id,
        )

    # =====================================================
    # Get All Rooms
    # =====================================================

    async def get_rooms(
        self,
    ) -> list[Room]:

        return await self.repository.get_all()

    # =====================================================
    # Update Room
    # =====================================================

    async def update_room(
        self,
        room_id: UUID,
        request: RoomUpdate,
    ) -> Room | None:

        room = await self.repository.get_by_id(
            room_id,
        )

        if room is None:
            return None

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(
                room,
                key,
                value,
            )

        return await self.repository.update(
            room,
        )

    # =====================================================
    # Delete Room
    # =====================================================

    async def delete_room(
        self,
        room_id: UUID,
    ) -> bool:

        room = await self.repository.get_by_id(
            room_id,
        )

        if room is None:
            return False

        await self.repository.delete(
            room,
        )

        return True