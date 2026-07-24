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

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        address: Address,
        property_obj: Property,
    ) -> Property:
        """
        Create a new property along with its address.
        """
        try:
            self.db.add(address)
            await self.db.flush()

            property_obj.address_id = address.id

            self.db.add(property_obj)

            await self.db.commit()

            await self.db.refresh(address)
            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(
        self,
    ) -> list[Property]:
        """
        Retrieve all properties.
        """
        try:
            result = await self.db.execute(select(Property))
            return result.scalars().all()

        except SQLAlchemyError:
            raise

    async def get_by_owner_id(
        self,
        owner_id: UUID,
    ) -> list[Property]:
        """
        Retrieve all properties owned by a user.
        """
        try:
            result = await self.db.execute(
                select(Property).where(
                    Property.owner_id == owner_id
                )
            )
            return result.scalars().all()

        except SQLAlchemyError:
            raise

    async def get_by_id(
        self,
        property_id: UUID,
    ) -> Property | None:
        """
        Retrieve a property by ID.
        """
        try:
            result = await self.db.execute(
                select(Property).where(
                    Property.id == property_id
                )
            )
            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    async def update(
        self,
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

            await self.db.commit()
            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def archive(
        self,
        property_obj: Property,
    ) -> Property:
        """
        Archive a property.
        """
        try:
            property_obj.status = PropertyStatus.ARCHIVED

            await self.db.commit()
            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def submit_for_review(
        self,
        property_obj: Property,
    ) -> Property:
        """
        Submit a property for admin review.
        """
        try:
            property_obj.status = PropertyStatus.PENDING

            await self.db.commit()
            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete(
        self,
        property_obj: Property,
    ) -> bool:
        """
        Delete a property.
        """
        try:
            await self.db.delete(property_obj)
            await self.db.commit()

            return True

        except SQLAlchemyError:
            await self.db.rollback()
            raise