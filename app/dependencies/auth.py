# ============================================================
# Third Party
# ============================================================


from app.models.permissions_models.roles_permission import RolePermission
from app.models.permissions_models.permissions import Permission
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.database.session import get_db
from app.core.jwt import verify_access_token

from app.repositories.auth_repositories.auth_repositories import (
    AuthRepository,
)

# ============================================================
# OAuth2
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)

# ============================================================
# Current User Dependency
# ============================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    payload = verify_access_token(token)

    user_id = payload.get("sub")

    repository = AuthRepository(db)

    user = await repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials.",
                )

    return user


# ============================================================
# Require Permission Dependency
# ============================================================

def require_permission(permission_name: str):
    async def permission_checker(
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        result = await db.execute(
            select(Permission.name)
            .join(
                RolePermission,
                Permission.id == RolePermission.permission_id,
            )
            .where(RolePermission.role_id == current_user.role_id)
        )

        permissions = result.scalars().all()

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return permission_checker