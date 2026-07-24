from app.repositories.booking_repositories.booking_repository import BookingRepository
from app.models.booking_models.booking import Booking
from app.repositories.review_repositories.review_repositories import ReviewRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review_models.review_model import Review
from fastapi import HTTPException
from app.schema.review_schema.review_schema import CreateReviewRequest
from click import UUID




class ReviewService:
    def __init__(self, db: AsyncSession):
        self.repo = ReviewRepository(db)
        self.booking = BookingRepository(db)


    async def create_review(
        self,
        booking_id: UUID,
        property_id: UUID,
        customer_id: UUID,
        request: CreateReviewRequest,
    ):
        booking = await self.booking.get_booking_by_id(booking_id)

        if not booking:
            raise HTTPException(404, "Booking not found")

        if booking.customer_id != customer_id:
            raise HTTPException(403, "You cannot review this booking")

        if booking.property_id != property_id:
            raise HTTPException(400, "Invalid property")

        existing = await self.repo.get_review_by_booking(booking_id)

        if existing:
            raise HTTPException(400, "Review already submitted")

        review = Review(
            booking_id=booking_id,
            property_id=property_id,
            customer_id=customer_id,
            rating=request.rating,
            comment=request.comment,
        )

        await self.repo.create(review)
        return review

