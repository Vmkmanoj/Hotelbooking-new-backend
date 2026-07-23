# ============================================================
# Standard Library
# ============================================================

from datetime import datetime, timezone
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.permissions_models.permissions import Permission
from app.models.permissions_models.roles import Role
from app.models.permissions_models.roles_permission import RolePermission
from app.models.users_models.users import User
from app.common.enums.user_enums.role_name import RoleName


# ============================================================
# Auth Repository
# ============================================================

class AuthRepository:
    """
    Repository for authentication related database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ========================================================
    # User Queries
    # ========================================================

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        result = await self.db.execute(
            select(User).where(
                User.id == user_id,                
            )
        )

        return result.scalar_one_or_none()
    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """

        result = await self.db.execute(
            select(User).where(
                User.email == email,
            )
        )

        return result.scalar_one_or_none()

    async def create_user(
        self,
        user: User,
    ) -> User:
        """
        Persist a new user.
        """

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user

    async def update_last_login(
        self,
        user: User,
    ) -> None:
        """
        Update user's last login timestamp.
        """

        user.last_login_at = datetime.now(
            timezone.utc,
        )

        await self.db.commit()

    # ========================================================
    # Role Queries
    # ========================================================

    async def get_user_role(
        self,
        role_id: UUID,
    ) -> Role | None:
        """
        Retrieve role by ID.
        """

        result = await self.db.execute(
            select(Role).where(
                Role.id == role_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_role_by_name(
        self,
        role_name: RoleName,
    ) -> Role | None:
        """
        Retrieve role by name.
        """

        result = await self.db.execute(
            select(Role).where(
                Role.name == role_name,
            )
        )

        return result.scalar_one_or_none()

    # ========================================================
    # Permission Queries
    # ========================================================

    async def get_permissions_by_role(
        self,
        role_id: UUID,
    ) -> list[Permission]:
        """
        Retrieve all permissions assigned to a role.
        """

        result = await self.db.execute(
            select(Permission)
            .join(
                RolePermission,
                Permission.id == RolePermission.permission_id,
            )
            .where(
                RolePermission.role_id == role_id,
            )
        )

        return list(
            result.scalars().all(),
        )