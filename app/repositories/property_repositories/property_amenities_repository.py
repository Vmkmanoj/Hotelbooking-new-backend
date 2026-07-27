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

from app.models.property_models.property_amenity import (
    PropertyAmenity,
)

from app.schema.property_schema.property_amenities_schema import (
    PropertyAmenityUpdate,
)


# ============================================================
# Property Amenity Repository
# ============================================================

class PropertyAmenityRepository:
    """
    Repository responsible for Property-Amenity database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Property Amenity
    # ========================================================

    async def create(
        self,
        property_amenity: PropertyAmenity,
    ) -> PropertyAmenity:
        """
        Persist a property-amenity mapping.
        """
        try:
            self.db.add(property_amenity)

            await self.db.commit()

            await self.db.refresh(property_amenity)

            return property_amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get Property Amenity By ID
    # ========================================================

    async def get_by_id(
        self,
        property_amenity_id: UUID,
    ) -> PropertyAmenity | None:
        """
        Retrieve a property-amenity mapping by ID.
        """
        try:
            result = await self.db.execute(
                select(PropertyAmenity).where(
                    PropertyAmenity.id == property_amenity_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Mapping By Property And Mapping ID
    # ========================================================

    async def get_by_property_id_and_id(
        self,
        property_id: UUID,
        property_amenity_id: UUID,
    ) -> PropertyAmenity | None:
        """
        Retrieve a property-amenity mapping that belongs
        to a specific property.
        """

        try:

            result = await self.db.execute(
                select(PropertyAmenity).where(
                    PropertyAmenity.id == property_amenity_id,
                    PropertyAmenity.property_id == property_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise
    # ========================================================
    # Get Mapping By Property & Amenity
    # ========================================================

    async def get_by_property_and_amenity(
        self,
        property_id: UUID,
        amenity_id: UUID,
    ) -> PropertyAmenity | None:
        """
        Retrieve a property-amenity mapping.
        """
        try:
            result = await self.db.execute(
                select(PropertyAmenity).where(
                    PropertyAmenity.property_id == property_id,
                    PropertyAmenity.amenity_id == amenity_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Amenities By Property
    # ========================================================

    async def get_by_property_id(
        self,
        property_id: UUID,
    ) -> list[PropertyAmenity]:
        """
        Retrieve all amenities assigned to a property.
        """
        try:
            result = await self.db.execute(
                select(PropertyAmenity)
                .where(
                    PropertyAmenity.property_id == property_id,
                )
                .order_by(
                    PropertyAmenity.amenity_id,
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get All Property Amenities
    # ========================================================

    async def get_all(
        self,
    ) -> list[PropertyAmenity]:
        """
        Retrieve all property-amenity mappings.
        """
        try:
            result = await self.db.execute(
                select(PropertyAmenity)
                .order_by(
                    PropertyAmenity.amenity_id,
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Update Property Amenity
    # ========================================================

    async def update(
        self,
        property_amenity: PropertyAmenity,
        property_amenity_data: PropertyAmenityUpdate,
    ) -> PropertyAmenity:
        """
        Update a property-amenity mapping.
        """
        try:
            update_data = property_amenity_data.model_dump(
                exclude_unset=True,
            )

            for key, value in update_data.items():
                setattr(
                    property_amenity,
                    key,
                    value,
                )

            await self.db.commit()

            await self.db.refresh(property_amenity)

            return property_amenity

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Delete Property Amenity
    # ========================================================

    async def delete(
        self,
        property_amenity: PropertyAmenity,
    ) -> None:
        """
        Remove an amenity assignment from a property.
        """
        try:
            await self.db.delete(property_amenity)

            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise