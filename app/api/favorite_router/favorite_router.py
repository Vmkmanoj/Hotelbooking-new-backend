# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.database.session import get_db

from app.dependencies.auth import get_current_user

from app.models.users_models.users import User

from app.schema.favorite_schema.favorite_schema import (
    FavoriteResponse,
)

from app.services.favorite_services.favorite_service import (
    FavoriteService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)

# ============================================================
# Service Dependency
# ============================================================

def get_favorite_service(
    db: AsyncSession = Depends(get_db),
) -> FavoriteService:
    return FavoriteService(db)

# ============================================================
# Add Favorite
# ============================================================

@router.post(
    "/{property_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_favorites(
    property_id: UUID,
    current_user: User = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:

    return await service.add_favorite(
        user_id=current_user.id,
        property_id=property_id,
    )


# ============================================================
# Remove Favorite
# ============================================================

@router.delete(
    "/{property_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_200_OK,
)
async def remove_from_favorites(
    property_id: UUID,
    current_user: User = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:

    return await service.remove_favorite(
        user_id=current_user.id,
        property_id=property_id,
    )