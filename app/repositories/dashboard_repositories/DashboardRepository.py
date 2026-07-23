# ============================================================
# Standard Library
# ============================================================

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

# ============================================================
# Local Imports
# ============================================================

from app.models.users_models.users import User
from app.models.permissions_models.roles import Role
from app.models.property_models.property import Property

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)


# ============================================================
# Dashboard Repository
# ============================================================

class DashboardRepository:
    """
    Repository responsible for dashboard statistics.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ============================================================
    # User Statistics
    # ============================================================

    async def total_users(self) -> int:
        """
        Total registered users.
        """
        return await self._count(
            select(User)
        )

    async def total_customers(self) -> int:
        """
        Total customer accounts.
        """
        return await self._count(
            select(User)
            .join(Role)
            .where(
                Role.name == "CUSTOMER"
            )
        )

    async def total_property_owners(self) -> int:
        """
        Total property owners.
        """
        return await self._count(
            select(User)
            .join(Role)
            .where(
                Role.name == "PROPERTY_OWNER"
            )
        )

    async def total_admins(self) -> int:
        """
        Total super administrators.
        """
        return await self._count(
            select(User)
            .join(Role)
            .where(
                Role.name == "SUPER_ADMIN"
            )
        )

    # ============================================================
    # Property Statistics
    # ============================================================

    async def total_properties(self) -> int:
        """
        Total registered properties.
        """
        return await self._count(
            select(Property)
        )

    async def pending_properties(self) -> int:
        """
        Properties awaiting approval.
        """
        return await self._count(
            select(Property).where(
                Property.status == PropertyStatus.PENDING
            )
        )

    async def approved_properties(self) -> int:
        """
        Approved properties.
        """
        return await self._count(
            select(Property).where(
                Property.status == PropertyStatus.APPROVED
            )
        )

    async def rejected_properties(self) -> int:
        """
        Rejected properties.
        """
        return await self._count(
            select(Property).where(
                Property.status == PropertyStatus.REJECTED
            )
        )

    # ============================================================
    # Helper
    # ============================================================

    async def _count(
        self,
        statement: Select,
    ) -> int:
        """
        Execute a COUNT query.
        """
        try:
            result = await self.db.execute(
                select(
                    func.count()
                ).select_from(
                    statement.subquery()
                )
            )

            return result.scalar_one()

        except SQLAlchemyError:
            raise