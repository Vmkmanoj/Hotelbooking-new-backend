from uuid import UUID

from app.models.property_models.amenities import Amenity

from app.repositories.property_repositories.amenity_repository import (
    AmenityRepository,
)

from app.schema.property_schema.amenity_schema import (
    AmenityCreate,
    AmenityUpdate,
)


class AmenityService:

    def __init__(
        self,
        repository: AmenityRepository,
    ):
        self.repository = repository

    # ==========================================================
    # Create Amenity
    # ==========================================================

    async def create(
        self,
        request: AmenityCreate,
    ) -> Amenity:

        amenity = Amenity(
            **request.model_dump()
        )

        return await self.repository.create(
            amenity
        )

    # ==========================================================
    # Get All Amenities
    # ==========================================================

    async def get_all(
        self,
    ) -> list[Amenity]:

        return await self.repository.get_all()

    # ==========================================================
    # Get Amenity By ID
    # ==========================================================

    async def get_by_id(
        self,
        amenity_id: UUID,
    ) -> Amenity | None:

        return await self.repository.get_by_id(
            amenity_id
        )

    # ==========================================================
    # Update Amenity
    # ==========================================================

    async def update(
        self,
        amenity_id: UUID,
        request: AmenityUpdate,
    ) -> Amenity | None:

        amenity = await self.repository.get_by_id(
            amenity_id
        )

        if amenity is None:
            return None

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                amenity,
                field,
                value,
            )

        return await self.repository.update(
            amenity
        )

    # ==========================================================
    # Delete Amenity
    # ==========================================================

    async def delete(
        self,
        amenity_id: UUID,
    ) -> bool:

        amenity = await self.repository.get_by_id(
            amenity_id
        )

        if amenity is None:
            return False

        await self.repository.delete(
            amenity
        )

        return True