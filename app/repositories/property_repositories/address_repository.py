from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property_models.address import Address

from app.schema.address_schema.address import (
    AddressCreate,
    AddressUpdate,
)


class AddressRepository:
    """
    Repository responsible for Address database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

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
                updated_by=address_data.owner_id,
                created_by=address_data.owner_id,
            )

            self.db.add(address)

            await self.db.commit()
            await self.db.refresh(address)

            return address

        except SQLAlchemyError:
            await self.db.rollback()
            raise

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
                    Address.id == address_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

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
                exclude_unset=True
            )

            for key, value in update_data.items():
                setattr(address, key, value)

            await self.db.commit()
            await self.db.refresh(address)

            return address

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # Optional: keep delete if business requires it.
    #
    # @staticmethod
    # async def delete(
    #     db: AsyncSession,
    #     address: Address,
    # ) -> None:
    #     try:
    #         await db.delete(address)
    #         await db.commit()
    #
    #     except SQLAlchemyError:
    #         await db.rollback()
    #         raise