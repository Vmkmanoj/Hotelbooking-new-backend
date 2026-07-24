



from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review_models.review_model import Review
from sqlalchemy import select
from click import UUID


# ============================================================
# Review Repository
# ============================================================

class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_review_by_booking(self, booking_id: UUID):
        result = await self.db.execute(
            select(Review).where(Review.booking_id == booking_id)
        )
        return result.scalar_one_or_none()