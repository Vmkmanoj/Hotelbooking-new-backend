# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.property_models.address import Address

from app.schema.address_schema.address import (
    AddressCreate,
    AddressUpdate,
)


# ============================================================
# Address Repository
# ============================================================

class AddressRepository:
    """
    Repository responsible for Address database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ============================================================
    # Create Address
    # ============================================================

    async def create(
        self,
        address_data: AddressCreate,
    ) -> Address:
        """
        Create a new address.
        """

        try:

            address = Address(
                address_line_1=address_data.address_line_1,
                address_line_2=address_data.address_line_2,
                city=address_data.city,
                state=address_data.state,
                country=address_data.country,
                pincode=address_data.pincode,

                # Temporary until JWT integration
                created_by=str(address_data.owner_id),
                updated_by=str(address_data.owner_id),
            )

            self.db.add(address)

            await self.db.commit()

            await self.db.refresh(address)

            return address

        except SQLAlchemyError:

            await self.db.rollback()

            raise

    # ============================================================
    # Get All Addresses
    # ============================================================

    async def get_all(
        self,
    ) -> list[Address]:
        """
        Retrieve all addresses.
        """

        try:

            result = await self.db.execute(
                select(Address)
            )

            return result.scalars().all()

        except SQLAlchemyError:

            raise

    # ============================================================
    # Get Address By Id
    # ============================================================

    async def get_by_id(
        self,
        address_id: UUID,
    ) -> Address | None:
        """
        Retrieve an address by ID.
        """

        try:

            result = await self.db.execute(
                select(Address).where(
                    Address.id == address_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:

            raise

    # ============================================================
    # Update Address
    # ============================================================

    async def update(
        self,
        address: Address,
        address_data: AddressUpdate,
    ) -> Address:
        """
        Update an existing address.
        """

        try:

            update_data = address_data.model_dump(
                exclude_unset=True,
            )

            for key, value in update_data.items():
                setattr(
                    address,
                    key,
                    value,
                )

            await self.db.commit()

            await self.db.refresh(address)

            return address

        except SQLAlchemyError:

            await self.db.rollback()

            raise

    # ============================================================
    # Delete Address (Optional)
    # ============================================================

    # async def delete(
    #     self,
    #     address: Address,
    # ) -> None:
    #
    #     try:
    #
    #         await self.db.delete(address)
    #
    #         await self.db.commit()
    #
    #     except SQLAlchemyError:
    #
    #         await self.db.rollback()
    #
    #         raise