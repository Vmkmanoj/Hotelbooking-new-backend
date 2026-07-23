# ============================================================
# Standard Library
# ============================================================

from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.models.favorites_models.favorites import Favorite

from app.repositories.favorite_repositories.favorite_repository import (
    FavoriteRepository,
)

from app.schema.favorite_schema.favorite_schema import (
    FavoriteResponse,
)


# ============================================================
# Favorite Service
# ============================================================

class FavoriteService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.repo = FavoriteRepository(db)

    # ========================================================
    # Add Favorite
    # ========================================================

    async def add_favorite(
        self,
        user_id: UUID,
        property_id: UUID,
    ) -> FavoriteResponse:

        property = await self.repo.get_active_property_by_id(
            property_id,
        )

        if property is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        favorite = await self.repo.get_by_user_and_property(
            user_id=user_id,
            property_id=property_id,
        )

        if favorite is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property already added to favorites.",
            )

        favorite = Favorite(
            user_id=user_id,
            property_id=property_id,
            created_by=user_id,
            updated_by=user_id,
        )

        await self.repo.create(
            favorite,
        )

        return FavoriteResponse(
            success=True,
            message="Property added to favorites.",
        )

    # ========================================================
    # Remove Favorite
    # ========================================================

    async def remove_favorite(
        self,
        user_id: UUID,
        property_id: UUID,
    ) -> FavoriteResponse:

        favorite = await self.repo.get_by_user_and_property(
            user_id=user_id,
            property_id=property_id,
        )

        if favorite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found.",
            )

        await self.repo.delete(
            favorite,
        )

        return FavoriteResponse(
            success=True,
            message="Property removed from favorites.",
        )