# ============================================================
# Standard Library
# ============================================================

from datetime import datetime, timezone
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

from app.models.property_models.property import Property
from app.models.users_models.users import User
from app.models.property_models.address import Address

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)


# ============================================================
# Super Admin Property Repository
# ============================================================

class SuperAdminPropertyRepository:
    """
    Repository responsible for Super Admin property management.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ============================================================
    # Property Queries
    # ============================================================

    async def get_pending_properties(self):
        """
        Retrieve all pending properties.
        """
        try:
            result = await self.db.execute(
                select(
                    Property.id,
                    Property.property_name,
                    User.first_name.label("owner_name"),
                    User.email.label("owner_email"),
                    Address.city,
                    Address.state,
                    Property.status,
                    Property.created_at,
                )
                .join(User, Property.owner_id == User.id)
                .join(Address, Property.address_id == Address.id)
                .where(
                    Property.status == PropertyStatus.PENDING
                )
                .order_by(
                    Property.created_at.desc()
                )
            )

            return result.all()

        except SQLAlchemyError:
            raise

    async def get_property_by_id(
        self,
        property_id: UUID,
    ):
        """
        Retrieve complete property details.
        """
        try:
            result = await self.db.execute(
                select(
                    Property.id,
                    Property.property_name,
                    Property.description,

                    User.first_name.label("owner_name"),
                    User.email.label("owner_email"),
                    User.phone.label("owner_phone"),

                    Address.address_line_1,
                    Address.address_line_2,
                    Address.city,
                    Address.state,
                    Address.country,
                    Address.postal_code,

                    Property.property_type,
                    Property.status,
                    Property.is_verified,
                    Property.created_at,
                )
                .join(User, Property.owner_id == User.id)
                .join(Address, Property.address_id == Address.id)
                .where(
                    Property.id == property_id
                )
            )

            return result.first()

        except SQLAlchemyError:
            raise

    async def get_approved_properties(self):
        """
        Retrieve all approved properties.
        """
        try:
            result = await self.db.execute(
                select(Property)
                .where(
                    Property.status == PropertyStatus.APPROVED
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    # ============================================================
    # Property Actions
    # ============================================================

    async def approve_property(
        self,
        property: Property,
        admin_id: UUID | None = None,
    ) -> Property:
        """
        Approve a property.
        """
        try:
            property.status = PropertyStatus.APPROVED
            property.is_verified = True
            property.approved_by = admin_id
            property.approved_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(property)

            return property

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def reject_property(
        self,
        property: Property,
        remarks: str,
        admin_id: UUID | None = None,
    ) -> Property:
        """
        Reject a property.
        """
        try:
            property.status = PropertyStatus.REJECTED
            property.is_verified = False
            property.approval_remarks = remarks
            property.approved_by = admin_id
            property.approved_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(property)

            return property

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def suspend_property(
        self,
        property: Property,
        remarks: str,
        admin_id: UUID | None = None,
    ) -> Property:
        """
        Suspend a property.
        """
        try:
            property.status = PropertyStatus.SUSPENDED
            property.approval_remarks = remarks
            property.approved_by = admin_id
            property.approved_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(property)

            return property

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def activate_property(
        self,
        property: Property,
        remarks: str,
        admin_id: UUID | None = None,
    ) -> Property:
        """
        Activate a suspended property.
        """
        try:
            property.status = PropertyStatus.APPROVED
            property.is_verified = True
            property.approval_remarks = remarks
            property.approved_by = admin_id
            property.approved_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(property)

            return property

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_property(
        self,
        property: Property,
    ) -> Property:
        """
        Soft delete a property.
        """
        try:
            property.is_deleted = True

            await self.db.commit()
            await self.db.refresh(property)

            return property

        except SQLAlchemyError:
            await self.db.rollback()
            raise


    async def get_active_property_by_id(
        self,
        property_id: UUID,
    ) -> Property | None:

        result = await self.db.execute(
            select(Property).where(
                Property.id == property_id,
                Property.is_deleted.is_(False),
            )
        )

        return result.scalar_one_or_none()