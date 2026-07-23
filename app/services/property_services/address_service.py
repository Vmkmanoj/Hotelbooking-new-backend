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

from app.models.property_models.address import Address

from app.repositories.property_repositories.address_repository import (
    AddressRepository,
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

    # ========================================================
    # Create Address
    # ========================================================

    async def create_address(
        self,
        address_data: AddressCreate,
    ) -> Address:

        return await self.repo.create(
            address_data,
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
    ) -> Address:

        return await self._get_address_or_404(
            address_id,
        )

    # ========================================================
    # Update Address
    # ========================================================

    async def update_address(
        self,
        address_id: UUID,
        address_data: AddressUpdate,
    ) -> Address:

        address = await self._get_address_or_404(
            address_id,
        )

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