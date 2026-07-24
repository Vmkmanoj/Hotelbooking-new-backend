from app.services.review_services.review_services import ReviewService
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user
from app.schema.review_schema.review_schema import CreateReviewRequest
from uuid import UUID
from fastapi import APIRouter, Depends

# pyrefly: ignore [missing-import]






router = APIRouter()

@router.post("/reviews")
async def create_review(
    booking_id: UUID,
    property_id: UUID,
    request: CreateReviewRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ReviewService(db).create_review(
        booking_id=booking_id,
        property_id=property_id,
        customer_id=current_user.id,
        request=request,
    )