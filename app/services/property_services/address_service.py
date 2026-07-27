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

from app.common.enums.user_enums.role_name import RoleName

from app.models.property_models.address import Address
from app.models.users_models.users import User

from app.repositories.property_repositories.address_repository import (
    AddressRepository,
)

from app.repositories.property_repositories.property_repository import (
    PropertyRepository,
)

from app.schema.property_schema.address import (
    AddressCreate,
    AddressUpdate,
)


# ============================================================
# Address Service
# ============================================================

class AddressService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.repo = AddressRepository(db)
        self.property_repo = PropertyRepository(db)

    # ========================================================
    # Create Address
    # ========================================================

    async def create_address(
        self,
        address_data: AddressCreate,
        current_user: User,
    ) -> Address:

        address = Address(
            address_line_1=address_data.address_line_1,
            address_line_2=address_data.address_line_2,
            city=address_data.city,
            state=address_data.state,
            country=address_data.country,
            postal_code=address_data.postal_code,
            created_by=current_user.email,
            updated_by=current_user.email,
        )

        return await self.repo.create(
            address,
        )

    # ========================================================
    # Get All Addresses
    # ========================================================

    async def get_all_addresses(
        self,
    ) -> list[Address]:

        return await self.repo.get_all()

    # ========================================================
    # Get Address
    # ========================================================

    async def get_address(
        self,
        address_id: UUID,
        current_user: User,
    ) -> Address:

        address = await self._get_address_or_404(
            address_id,
        )

        await self._validate_address_access(
            address,
            current_user,
        )

        return address

    # ========================================================
    # Update Address
    # ========================================================

    async def update_address(
        self,
        address_id: UUID,
        address_data: AddressUpdate,
        current_user: User,
    ) -> Address:

        address = await self._get_address_or_404(
            address_id,
        )

        await self._validate_address_access(
            address,
            current_user,
        )

        address.updated_by = current_user.email

        return await self.repo.update(
            address,
            address_data,
        )

    # ========================================================
    # Private Helpers
    # ========================================================

    async def _get_address_or_404(
        self,
        address_id: UUID,
    ) -> Address:

        address = await self.repo.get_by_id(
            address_id,
        )

        if address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found.",
            )

        return address

    # ========================================================
    # Address Ownership Validation
    # ========================================================

    async def _validate_address_access(
        self,
        address: Address,
        current_user: User,
    ) -> None:
        """
        Super Admin -> can access every address.

        Property Owner -> only addresses belonging
        to their own properties.
        """

        if current_user.role.name == RoleName.SUPER_ADMIN.value:
            return

        properties = await self.property_repo.get_by_owner_id(
            current_user.id,
        )

        address_ids = {
            property.address_id
            for property in properties
        }

        if address.id not in address_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this address.",
            )