# ============================================================
# Standard Library
# ============================================================

from uuid import UUID
from datetime import datetime, timezone

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

from app.models.property_models.address import Address
from app.models.property_models.property import Property

from app.schema.property_schema.property_schema import (
    PropertyUpdate,
)


# ============================================================
# Property Repository
# ============================================================

class PropertyRepository:
    """
    Repository responsible for Property database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # Create Property
    # ========================================================

    async def create(
        self,
        address: Address,
        property_obj: Property,
    ) -> Property:
        """
        Create a property along with its address.
        """
        try:
            self.db.add(address)

            await self.db.flush()

            property_obj.address_id = address.id

            self.db.add(property_obj)

            await self.db.commit()

            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Get All Properties
    # ========================================================

    async def get_all(
        self,
    ) -> list[Property]:
        """
        Retrieve all active properties.
        """
        try:
            result = await self.db.execute(
                select(Property)
                .where(
                    Property.is_deleted.is_(False),
                )
                .order_by(
                    Property.created_at.desc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Properties By Owner
    # ========================================================

    async def get_by_owner_id(
        self,
        owner_id: UUID,
    ) -> list[Property]:
        """
        Retrieve all active properties owned by a user.
        """
        try:
            result = await self.db.execute(
                select(Property)
                .where(
                    Property.owner_id == owner_id,
                    Property.is_deleted.is_(False),
                )
                .order_by(
                    Property.created_at.desc(),
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Get Property By ID
    # ========================================================

    async def get_by_id(
        self,
        property_id: UUID,
    ) -> Property | None:
        """
        Retrieve an active property by ID.
        """
        try:
            result = await self.db.execute(
                select(Property).where(
                    Property.id == property_id,
                    Property.is_deleted.is_(False),
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    # ========================================================
    # Update Property
    # ========================================================

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
                exclude_unset=True,
                exclude_none=True,
            )

            for key, value in update_data.items():
                setattr(
                    property_obj,
                    key,
                    value,
                )

            await self.db.commit()

            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # ========================================================
    # Archive Property
    # ========================================================

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

    # ========================================================
    # Submit Property For Review
    # ========================================================

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

    # ========================================================
    # Approve Property
    # ========================================================

    async def approve_property(
        self,
        property_obj: Property,
        approved_by: UUID,
        approval_remarks: str | None,
    ) -> Property:
        """
        Approve a property.
        """
        try:

            property_obj.status = PropertyStatus.APPROVED
            property_obj.is_verified = True
            property_obj.approved_by = approved_by
            property_obj.approval_remarks = approval_remarks
            property_obj.approved_at = datetime.now(timezone.utc)

            await self.db.commit()

            await self.db.refresh(
                property_obj,
            )

            return property_obj

        except SQLAlchemyError:

            await self.db.rollback()

            raise


    # ========================================================
    # Reject Property
    # ========================================================

    async def reject_property(
        self,
        property_obj: Property,
        rejected_by: UUID,
        approval_remarks: str,
    ) -> Property:
        """
        Reject a property.
        """

        try:

            property_obj.status = PropertyStatus.REJECTED
            property_obj.is_verified = False
            property_obj.approved_by = rejected_by
            property_obj.approval_remarks = approval_remarks
            property_obj.approved_at = datetime.now(
                timezone.utc,
            )

            await self.db.commit()

            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise
    # ========================================================
    # Soft Delete Property
    # ========================================================

    async def delete(
        self,
        property_obj: Property,
    ) -> Property:
        """
        Soft delete a property.

        The property remains in the database for
        historical records such as bookings,
        payments and reviews.
        """
        try:
            property_obj.is_deleted = True
            property_obj.status = PropertyStatus.ARCHIVED

            await self.db.commit()

            await self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise