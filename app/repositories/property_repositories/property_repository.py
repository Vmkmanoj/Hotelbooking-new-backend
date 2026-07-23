from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums.property_enums.property_status import PropertyStatus

from app.models.property_models.address import Address
from app.models.property_models.property import Property

from app.schema.property_schema.property_schema import PropertyUpdate


class PropertyRepository:
    """
    Repository responsible for Property database operations.
    """

    @staticmethod
    async def create(
        db: AsyncSession,
        address: Address,
        property_obj: Property,
    ) -> Property:
        """
        Create a new property along with its address.
        """
        try:
            db.add(address)
            await db.flush()

            property_obj.address_id = address.id

            db.add(property_obj)

            await db.commit()

            await db.refresh(address)
            await db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Property]:
        """
        Retrieve all properties.
        """
        try:
            result = await db.execute(select(Property))
            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_by_owner_id(
        db: AsyncSession,
        owner_id: UUID,
    ) -> list[Property]:
        """
        Retrieve all properties owned by a user.
        """
        try:
            result = await db.execute(
                select(Property).where(
                    Property.owner_id == owner_id
                )
            )
            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        property_id: UUID,
    ) -> Property | None:
        """
        Retrieve a property by ID.
        """
        try:
            result = await db.execute(
                select(Property).where(
                    Property.id == property_id
                )
            )
            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def update(
        db: AsyncSession,
        property_obj: Property,
        property_data: PropertyUpdate,
    ) -> Property:
        """
        Update an existing property.
        """
        try:
            update_data = property_data.model_dump(
                exclude_unset=True
            )

            for key, value in update_data.items():
                setattr(property_obj, key, value)

            await db.commit()
            await db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def archive(
        db: AsyncSession,
        property_obj: Property,
    ) -> Property:
        """
        Archive a property.
        """
        try:
            property_obj.status = PropertyStatus.ARCHIVED

            await db.commit()
            await db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def submit_for_review(
        db: AsyncSession,
        property_obj: Property,
    ) -> Property:
        """
        Submit a property for admin review.
        """
        try:
            property_obj.status = PropertyStatus.PENDING

            await db.commit()
            await db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(
        db: AsyncSession,
        property_obj: Property,
    ) -> bool:
        """
        Delete a property.
        """
        try:
            await db.delete(property_obj)
            await db.commit()

            return True

        except SQLAlchemyError:
            await db.rollback()
            raise