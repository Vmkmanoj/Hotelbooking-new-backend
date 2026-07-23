# ============================================================
# Third Party
# ============================================================


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