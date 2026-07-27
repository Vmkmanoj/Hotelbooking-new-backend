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

from app.models.property_models.property_amenity import (
    PropertyAmenity,
)

from app.models.users_models.users import User

from app.common.enums.user_enums.role_name import (
    RoleName,
)

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

from app.repositories.property_repositories.amenity_repository import (
    AmenityRepository,
)

from app.repositories.property_repositories.property_amenities_repository import (
    PropertyAmenityRepository,
)

from app.schema.property_schema.property_amenities_schema import (
    PropertyAmenityCreate,
    PropertyAmenityUpdate,
)


# ============================================================
# Property Amenity Service
# ============================================================

class PropertyAmenityService:
    """
    Business logic for assigning amenities to properties.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.property_repo = PropertyRepository(db)
        self.amenity_repo = AmenityRepository(db)
        self.mapping_repo = PropertyAmenityRepository(db)

    # ========================================================
    # Create Property Amenity
    # ========================================================

    async def create_property_amenity(
        self,
        property_amenity_data: PropertyAmenityCreate,
        current_user: User,
    ) -> PropertyAmenity:

        property_obj = await self._get_property_or_404(
            property_amenity_data.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        await self._get_amenity_or_404(
            property_amenity_data.amenity_id,
        )

        existing_mapping = (
            await self.mapping_repo.get_by_property_and_amenity(
                property_id=property_amenity_data.property_id,
                amenity_id=property_amenity_data.amenity_id,
            )
        )

        if existing_mapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Amenity is already assigned to this property.",
            )

        mapping = PropertyAmenity(
            property_id=property_amenity_data.property_id,
            amenity_id=property_amenity_data.amenity_id,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.mapping_repo.create(
            mapping,
        )

    # ========================================================
    # Get Property Amenity
    # ========================================================

    async def get_property_amenity(
        self,
        property_amenity_id: UUID,
        current_user: User,
    ) -> PropertyAmenity:

        mapping = await self._get_mapping_or_404(
            property_amenity_id,
        )

        property_obj = await self._get_property_or_404(
            mapping.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        return mapping

    # ========================================================
    # Get Amenities Of Property
    # ========================================================

    async def get_property_amenities(
        self,
        property_id: UUID,
        current_user: User,
    ) -> list[PropertyAmenity]:

        property_obj = await self._get_property_or_404(
            property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        return await self.mapping_repo.get_by_property_id(
            property_id,
        )

    # ========================================================
    # Update Property Amenity
    # ========================================================

    async def update_property_amenity(
        self,
        property_amenity_id: UUID,
        property_amenity_data: PropertyAmenityUpdate,
        current_user: User,
    ) -> PropertyAmenity:

        mapping = await self._get_mapping_or_404(
            property_amenity_id,
        )

        property_obj = await self._get_property_or_404(
            mapping.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        if property_amenity_data.amenity_id is not None:

            await self._get_amenity_or_404(
                property_amenity_data.amenity_id,
            )

            duplicate = (
                await self.mapping_repo.get_by_property_and_amenity(
                    property_id=mapping.property_id,
                    amenity_id=property_amenity_data.amenity_id,
                )
            )

            if (
                duplicate
                and duplicate.id != mapping.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Amenity is already assigned to this property.",
                )

        mapping.updated_by = current_user.email

        return await self.mapping_repo.update(
            mapping,
            property_amenity_data,
        )

    # ========================================================
    # Delete Property Amenity
    # ========================================================

    async def delete_property_amenity(
        self,
        property_amenity_id: UUID,
        current_user: User,
    ) -> None:

        mapping = await self._get_mapping_or_404(
            property_amenity_id,
        )

        property_obj = await self._get_property_or_404(
            mapping.property_id,
        )

        self._validate_property_access(
            property_obj,
            current_user,
        )

        await self.mapping_repo.delete(
            mapping,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_mapping_or_404(
        self,
        property_amenity_id: UUID,
    ) -> PropertyAmenity:

        mapping = await self.mapping_repo.get_by_id(
            property_amenity_id,
        )

        if mapping is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property amenity not found.",
            )

        return mapping

    async def _get_property_or_404(
        self,
        property_id: UUID,
    ):

        property_obj = await self.property_repo.get_by_id(
            property_id,
        )

        if property_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        return property_obj

    async def _get_amenity_or_404(
        self,
        amenity_id: UUID,
    ):

        amenity = await self.amenity_repo.get_by_id(
            amenity_id,
        )

        if amenity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Amenity not found.",
            )

        return amenity

    def _validate_property_access(
        self,
        property_obj,
        current_user: User,
    ) -> None:

        if current_user.role.name == RoleName.SUPER_ADMIN.value:
            return

        if property_obj.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to modify this property.",
            )