# ============================================================
# Standard Library
# ============================================================

from datetime import (
    date,
    datetime,
)
from decimal import Decimal
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.booking_enums.booking_enums import (
    BookingStatus,
    PaymentStatus,
    RefundStatus,
    CancellationType,
)

# ============================================================
# Booking Room Request
# ============================================================

class BookingRoomRequest(BaseModel):
    """
    Represents a room selected by the customer.
    """

    room_id: UUID

# ============================================================
# Create Booking Request
# ============================================================

class CreateBookingRequest(BaseModel):
    """
    Request schema for creating a booking.
    """

    property_id: UUID

    check_in_date: date

    check_out_date: date

    guest_count: int = Field(
        gt=0,
        description="Total number of guests.",
    )

    special_requests: str | None = None

    rooms: list[BookingRoomRequest] = Field(
        min_length=1,
    )



class BookingUpdate(BaseModel):

    check_in_date: date | None = None

    check_out_date: date | None = None

    guest_count: int | None = Field(
        default=None,
        gt=0,
    )

    special_requests: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )
# ============================================================
# Booking Room Response
# ============================================================

class BookingRoomResponse(BaseModel):

    room_id: UUID

    room_number: str

    room_type: str

    price_per_night: Decimal

    number_of_nights: int

    room_total: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )

# ============================================================
# Booking Summary Response
# ============================================================

class BookingSummaryResponse(BaseModel):
    """
    Summary information for a booking.
    """

    id: UUID

    booking_reference: str

    property_id: UUID

    check_in_date: date

    check_out_date: date

    guest_count: int

    total_amount: Decimal

    booking_status: BookingStatus

    payment_status: PaymentStatus

    model_config = ConfigDict(
        from_attributes=True,
    )

# ============================================================
# Booking Response
# ============================================================

class BookingResponse(BaseModel):
    """
    Detailed booking response.
    """

    id: UUID

    booking_reference: str

    customer_id: UUID

    property_id: UUID

    check_in_date: date

    check_out_date: date

    guest_count: int

    subtotal: Decimal

    tax_amount: Decimal

    discount_amount: Decimal

    total_amount: Decimal

    booking_status: BookingStatus

    payment_status: PaymentStatus

    special_requests: str | None

    rooms: list[BookingRoomResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )

# ============================================================
# Booking History Response
# ============================================================

class BookingHistoryResponse(BaseModel):
    """
    Response schema for a booking history entry.
    """

    booking_status: BookingStatus

    remarks: str | None

    changed_by: UUID | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Cancel Booking Request
# ============================================================

class CancelBookingRequest(BaseModel):
    """
    Request schema for cancelling a booking.
    """

    reason: str = Field(
        min_length=10,
        max_length=500,
    )

# ============================================================
# Booking Cancellation Response
# ============================================================

class BookingCancellationResponse(BaseModel):
    """
    Response schema for booking cancellation.
    """

    cancellation_type:  CancellationType

    reason: str

    refund_status: RefundStatus

    refund_amount: Decimal

    cancelled_by: UUID | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class BookingMessageResponse(BaseModel):
    success: bool
    message: str