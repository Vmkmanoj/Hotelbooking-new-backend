# ============================================================
# Third Party
# ============================================================

from fastapi import HTTPException

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

# ============================================================
# Booking Exceptions
# ============================================================

class BookingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )


class RoomNotAvailableException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="One or more selected rooms are not available for the selected dates.",
        )


class InvalidBookingDatesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Check-out date must be later than check-in date.",
        )


class InvalidBookingStatusException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Booking is not in a valid state for this operation.",
        )


class BookingCancellationNotAllowedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="This booking cannot be cancelled.",
        )


class BookingAlreadyCancelledException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="Booking has already been cancelled.",
        )


class BookingCannotBeCancelledException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Completed bookings cannot be cancelled.",
        )


class InvalidCancellationReasonException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="A valid cancellation reason is required.",
        )


class PropertyNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Property not found.",
        )


class RoomNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )


class BookingAccessDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this booking.",
        )

class GuestCapacityExceededException(HTTPException):
    """
    Raised when the total guest count exceeds
    the maximum occupancy of the selected rooms.
    """

    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Guest count exceeds the maximum occupancy of the selected room(s).",
        )

class PropertyNotAvailableException(HTTPException):
    """
    Raised when the property exists but is not available for booking.
    """

    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="This property is not available for booking.",
        )