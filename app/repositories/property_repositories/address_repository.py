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

    @staticmethod
    async def create(
        db: AsyncSession,
        address_data: AddressCreate,
    ) -> Address:
        """
        Create a new address.
        """
        try:
            address = Address(**address_data.model_dump())

            db.add(address)

            await db.commit()
            await db.refresh(address)

            return address

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Address]:
        """
        Retrieve all addresses.
        """
        try:
            result = await db.execute(
                select(Address)
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        address_id: UUID,
    ) -> Address | None:
        """
        Retrieve an address by ID.
        """
        try:
            result = await db.execute(
                select(Address).where(
                    Address.id == address_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def update(
        db: AsyncSession,
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

            await db.commit()
            await db.refresh(address)

            return address

        except SQLAlchemyError:
            await db.rollback()
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