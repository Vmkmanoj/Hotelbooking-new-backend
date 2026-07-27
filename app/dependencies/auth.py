# ============================================================
# Standard Library
# ============================================================

from collections.abc import Callable

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    Depends,
    HTTPException,
    status,
)

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

from app.models.users_models.users import User

from app.common.enums.user_enums.role_name import (
    RoleName,
)

from app.common.enums.user_enums.user_status import (
    UserStatus,
)

# ============================================================
# OAuth2
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)

# ============================================================
# Current User
# ============================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Authenticate and return the currently logged-in user.

    Performs:
    - JWT validation
    - User lookup
    - Active account validation
    - Role validation
    """

    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    repository = AuthRepository(db)

    user = await repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    if user.user_status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive.",
        )

    if user.role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not assigned.",
        )

    return user


# ============================================================
# Require Single Role
# ============================================================

def require_role(
    role: RoleName,
) -> Callable:

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role.name != role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return role_checker


# ============================================================
# Require Multiple Roles
# ============================================================

def require_roles(
    roles: list[RoleName],
) -> Callable:

    allowed_roles = {
        role.value
        for role in roles
    }

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return role_checker


# ============================================================
# Require Permission
# ============================================================

def require_permission(
    permission_name: str,
) -> Callable:

    async def permission_checker(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:

        # Super Admin bypass
        if current_user.role.name == RoleName.SUPER_ADMIN.value:
            return current_user

        repository = AuthRepository(db)

        permissions = await repository.get_permissions_by_role(
            current_user.role_id,
        )

        permission_names = {
            permission.name
            for permission in permissions
        }

        if permission_name not in permission_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return permission_checker


# ============================================================
# Require Property Owner
# ============================================================

def require_property_owner() -> Callable:
    """
    Shortcut dependency for Property Owner endpoints.
    """

    return require_role(
        RoleName.PROPERTY_OWNER,
    )


# ============================================================
# Require Customer
# ============================================================

def require_customer() -> Callable:
    """
    Shortcut dependency for Customer endpoints.
    """

    return require_role(
        RoleName.CUSTOMER,
    )


# ============================================================
# Require Super Admin
# ============================================================

def require_super_admin() -> Callable:
    """
    Shortcut dependency for Super Admin endpoints.
    """

    return require_role(
        RoleName.SUPER_ADMIN,
    )