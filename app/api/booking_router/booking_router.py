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

from app.services.booking_services.booking_service import (
    BookingService,
)

from app.schema.booking_schema.booking_schemas import (
    BookingMessageResponse,
    BookingResponse,
    BookingSummaryResponse,
    CancelBookingRequest,
    CreateBookingRequest,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

# ============================================================
# Service Dependency
# ============================================================

def get_booking_service(
    db: AsyncSession = Depends(get_db),
) -> BookingService:
    return BookingService(db)

# ============================================================
# Create Booking
# ============================================================

@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    request: CreateBookingRequest,
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """
    Create a new booking.
    """

    return await service.create_booking(
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get My Bookings
# ============================================================

@router.get(
    "/me",
    response_model=list[BookingSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> list[BookingSummaryResponse]:
    """
    Retrieve all bookings for the authenticated customer.
    """

    return await service.get_my_bookings(
        current_user=current_user,
    )


# ============================================================
# Get Upcoming Bookings
# ============================================================

@router.get(
    "/me/upcoming",
    response_model=list[BookingSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_bookings(
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> list[BookingSummaryResponse]:
    """
    Retrieve all upcoming bookings.
    """

    return await service.get_upcoming_bookings(
        current_user=current_user,
    )


# ============================================================
# Get Completed Bookings
# ============================================================

@router.get(
    "/me/completed",
    response_model=list[BookingSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_completed_bookings(
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> list[BookingSummaryResponse]:
    """
    Retrieve all completed bookings.
    """

    return await service.get_completed_bookings(
        current_user=current_user,
    )


# ============================================================
# Get Booking By ID
# ============================================================

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_booking_by_id(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """
    Retrieve booking details.
    """

    return await service.get_booking_by_id(
        booking_id=booking_id,
        current_user=current_user,
    )


# ============================================================
# Cancel Booking
# ============================================================

@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel_booking(
    booking_id: UUID,
    request: CancelBookingRequest,
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> BookingMessageResponse:
    """
    Cancel an existing booking.
    """

    await service.cancel_booking(
        booking_id=booking_id,
        request=request,
        current_user=current_user,
    )

    return BookingMessageResponse(
        success=True,
        message="Booking cancelled successfully.",
    )