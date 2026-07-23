from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

from app.models.property_models.property import Property
from app.models.favorites_models.favorites import Favorite


class FavoriteRepository:
    """
    Repository responsible for Favorite database operations.
    """

    @staticmethod
    async def get_by_user_and_property(
        db: AsyncSession,
        user_id: UUID,
        property_id: UUID,
    ) -> Favorite | None:
        """
        Retrieve a favorite using user ID and property ID.
        Used to prevent duplicate favorites.
        """
        try:
            result = await db.execute(
                select(Favorite).where(
                    Favorite.user_id == user_id,
                    Favorite.property_id == property_id,
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def get_all_by_user(
        db: AsyncSession,
        user_id: UUID,
    ) -> list[Favorite]:
        """
        Retrieve all favorites of a user.
        """
        try:
            result = await db.execute(
                select(Favorite).where(
                    Favorite.user_id == user_id
                )
            )

            return result.scalars().all()

        except SQLAlchemyError:
            raise

    @staticmethod
    async def create(
        db: AsyncSession,
        favorite: Favorite,
    ) -> Favorite:
        """
        Create a favorite.
        """
        try:
            db.add(favorite)

            await db.commit()
            await db.refresh(favorite)

            return favorite

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(
        db: AsyncSession,
        favorite: Favorite,
    ) -> None:
        """
        Remove a favorite.
        """
        try:
            await db.delete(favorite)

            await db.commit()

        except SQLAlchemyError:
            await db.rollback()
            raise

    async def get_active_property_by_id(
        self,
        property_id: UUID,
    ) -> Property | None:

        result = await self.db.execute(
            select(Property).where(
                Property.id == property_id,
                Property.is_deleted.is_(False),
                Property.status == PropertyStatus.APPROVED,
            )
        )

        return result.scalar_one_or_none()