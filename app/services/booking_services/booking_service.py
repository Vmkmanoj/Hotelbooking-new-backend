# ============================================================
# Standard Library
# ============================================================

import uuid
from datetime import date
from decimal import Decimal
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.repositories.booking_repositories.booking_repository import (
    BookingRepository,
)

from app.schema.booking_schema.booking_schemas import (
    BookingResponse,
    BookingRoomResponse,
    BookingSummaryResponse,
    CancelBookingRequest,
    CreateBookingRequest,
)

from app.exceptions.booking_exceptions.booking_exceptions import (
    BookingAlreadyCancelledException,
    BookingCannotBeCancelledException,
    BookingNotFoundException,
    InvalidBookingDatesException,
    PropertyNotFoundException,
    RoomNotAvailableException,
    RoomNotFoundException,
    GuestCapacityExceededException,
    PropertyNotAvailableException,
)

from app.common.enums.booking_enums.booking_enums import (
    BookingStatus,
    CancellationType,
    PaymentStatus,
    RefundStatus,
)

from app.models.booking_models.booking import Booking
from app.models.booking_models.booking_room import BookingRoom
from app.models.booking_models.booking_history import BookingHistory
from app.models.booking_models.booking_cancellation import (
    BookingCancellation,
)
from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)
from app.common.enums.room_enums.room_status import RoomStatus

from app.models.users_models.users import User

# ============================================================
# Booking Service
# ============================================================

class BookingService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.repo = BookingRepository(
            db,
        )

        self.db = db

    # ============================================================
    # Helper Methods
    # ============================================================

    async def generate_booking_reference(
        self,
    ) -> str:
        """
        Generates a unique booking reference.
        """

        

        return f"HB-{uuid.uuid4().hex[:8].upper()}"
    
    # ============================================================
    # Helper Methods
    # ============================================================

    def calculate_booking_amount(
        self,
        rooms: list,
        number_of_nights: int,
    ) -> tuple[
        Decimal,
        Decimal,
        Decimal,
        Decimal,
    ]:
        """
        Calculates the booking amount.

        Returns:
            subtotal,
            tax_amount,
            discount_amount,
            total_amount
        """

        subtotal = sum(
            room.room_type.base_price * number_of_nights
            for room in rooms
        )

        subtotal = Decimal(subtotal)

        tax_amount = (
            subtotal * Decimal("0.18")
        ).quantize(
            Decimal("0.01")
        )

        discount_amount = Decimal("0.00")

        total_amount = (
            subtotal
            + tax_amount
            - discount_amount
        )

        return (
            subtotal,
            tax_amount,
            discount_amount,
            total_amount,
        )
    
    # ============================================================
    # Create Booking
    # ============================================================

    async def create_booking(
        self,
        request: CreateBookingRequest,
        current_user: User,
    ) -> BookingResponse:
        """
        Creates a new booking.
        """
        try:
            if request.check_in_date >= request.check_out_date:
                raise InvalidBookingDatesException()
            
            property = await self.repo.get_property_by_id(
                request.property_id,
            )

            if property is None:
                raise PropertyNotFoundException()

            if property.status != PropertyStatus.APPROVED:
                raise PropertyNotAvailableException()
            
            room_ids = [
                room.room_id
                for room in request.rooms
            ]

            rooms = await self.repo.get_rooms_by_ids(
                room_ids,
            )

            if len(rooms) != len(room_ids):
                raise RoomNotFoundException()

            for room in rooms:

                if room.room_type.property_id != request.property_id:
                    raise RoomNotFoundException()

            total_capacity = sum(
                room.room_type.max_occupancy
                for room in rooms
            )

            if request.guest_count > total_capacity:
                raise GuestCapacityExceededException()

            # ============================================================
            # Validate Room Availability
            # ============================================================

            for room in rooms:

                is_available = await self.repo.check_room_availability(
                    room_id=room.id,
                    check_in_date=request.check_in_date,
                    check_out_date=request.check_out_date,
                )

                if not is_available:
                    raise RoomNotAvailableException()

                if room.status != RoomStatus.AVAILABLE:
                    raise RoomNotAvailableException()
                
            # ============================================================
            # Calculate Stay Duration
            # ============================================================

            number_of_nights = (
                request.check_out_date
                - request.check_in_date
            ).days


            # ============================================================
            # Calculate Booking Amount
            # ============================================================

            (
                subtotal,
                tax_amount,
                discount_amount,
                total_amount,
            ) = self.calculate_booking_amount(
                rooms=rooms,
                number_of_nights=number_of_nights,
            )

            # ============================================================
            # Generate Booking Reference
            # ============================================================

            booking_reference = await self.generate_booking_reference()


            # ============================================================
            # Create Booking Entity
            # ============================================================

            booking = Booking(
                customer_id=current_user.id,
                property_id=request.property_id,
                booking_reference=booking_reference,
                check_in_date=request.check_in_date,
                check_out_date=request.check_out_date,
                guest_count=request.guest_count,
                subtotal=subtotal,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                total_amount=total_amount,
                booking_status=BookingStatus.PENDING,
                payment_status=PaymentStatus.PENDING,
                special_requests=request.special_requests,
                created_by=current_user.id,
                updated_by=current_user.id,
            )

            # ============================================================
            # Save Booking
            # ============================================================

            booking = await self.repo.create_booking(
                booking,
            )

            # ============================================================
            # Create Booking Rooms
            # ============================================================

            booking_rooms = []

            for room in rooms:

                booking_rooms.append(
                    BookingRoom(
                        booking_id=booking.id,
                        room_id=room.id,
                        price_per_night=room.room_type.base_price,
                        number_of_nights=number_of_nights,
                        room_total=room.room_type.base_price * number_of_nights,
                        created_by=current_user.id,
                        updated_by=current_user.id,
                    )
                )

            await self.repo.create_booking_rooms(
                booking_rooms,
            )

            # ============================================================
            # Create Booking History
            # ============================================================

            booking_history = BookingHistory(
                booking_id=booking.id,
                booking_status=BookingStatus.PENDING,
                changed_by=current_user.id,
                remarks="Booking created.",
                created_by=current_user.id,
                updated_by=current_user.id,
            )

            await self.repo.create_booking_history(
                booking_history,
            )

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise


        return BookingResponse(
            id=booking.id,
            booking_reference=booking.booking_reference,
            customer_id=booking.customer_id,
            property_id=booking.property_id,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            guest_count=booking.guest_count,
            subtotal=booking.subtotal,
            tax_amount=booking.tax_amount,
            discount_amount=booking.discount_amount,
            total_amount=booking.total_amount,
            booking_status=booking.booking_status,
            payment_status=booking.payment_status,
            special_requests=booking.special_requests,
            rooms=[
                BookingRoomResponse(
                    room_id=room.room_id,
                    price_per_night=room.price_per_night,
                    number_of_nights=room.number_of_nights,
                    room_total=room.room_total,
                )
                for room in booking_rooms
            ],
        )
    
    # ============================================================
    # Get Booking By ID
    # ============================================================

    async def get_booking_by_id(
        self,
        booking_id: UUID,
        current_user: User,
    ) -> BookingResponse:
        """
        Retrieves a booking by its ID.
        """

        booking = await self.repo.get_booking_by_id(
            booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()
        
        # ============================================================
        # Authorization Check
        # ============================================================

        if booking.customer_id != current_user.id:
            raise BookingNotFoundException()
        
        return BookingResponse(
            id=booking.id,
            booking_reference=booking.booking_reference,
            customer_id=booking.customer_id,
            property_id=booking.property_id,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            guest_count=booking.guest_count,
            subtotal=booking.subtotal,
            tax_amount=booking.tax_amount,
            discount_amount=booking.discount_amount,
            total_amount=booking.total_amount,
            booking_status=booking.booking_status,
            payment_status=booking.payment_status,
            special_requests=booking.special_requests,
            rooms=[
                BookingRoomResponse(
                    room_id=room.room_id,
                    price_per_night=room.price_per_night,
                    number_of_nights=room.number_of_nights,
                    room_total=room.room_total,
                )
                for room in booking.booking_rooms
            ],
        )
    
    # ============================================================
    # Get My Bookings
    # ============================================================

    async def get_my_bookings(
        self,
        current_user: User,
    ) -> list[BookingSummaryResponse]:
        """
        Retrieves all bookings for the authenticated customer.
        """

        bookings = await self.repo.get_customer_bookings(
            current_user.id,
        )

        return [
            BookingSummaryResponse(
                id=booking.id,
                booking_reference=booking.booking_reference,
                property_id=booking.property_id,
                check_in_date=booking.check_in_date,
                check_out_date=booking.check_out_date,
                guest_count=booking.guest_count,
                total_amount=booking.total_amount,
                booking_status=booking.booking_status,
                payment_status=booking.payment_status,
            )
            for booking in bookings
        ]
    
    # ============================================================
    # Get Upcoming Bookings
    # ============================================================

    async def get_upcoming_bookings(
        self,
        current_user: User,
    ) -> list[BookingSummaryResponse]:
        """
        Retrieves all upcoming bookings for the authenticated customer.
        """

        bookings = await self.repo.get_upcoming_bookings(
            customer_id=current_user.id,
            today=date.today(),
        )

        return [
            BookingSummaryResponse(
                id=booking.id,
                booking_reference=booking.booking_reference,
                property_id=booking.property_id,
                check_in_date=booking.check_in_date,
                check_out_date=booking.check_out_date,
                guest_count=booking.guest_count,
                total_amount=booking.total_amount,
                booking_status=booking.booking_status,
                payment_status=booking.payment_status,
            )
            for booking in bookings
        ]
    

    # ============================================================
    # Get Completed Bookings
    # ============================================================

    async def get_completed_bookings(
        self,
        current_user: User,
    ) -> list[BookingSummaryResponse]:
        """
        Retrieves all completed bookings for the authenticated customer.
        """

        bookings = await self.repo.get_completed_bookings(
            customer_id=current_user.id,
        )

        return [
            BookingSummaryResponse(
                id=booking.id,
                booking_reference=booking.booking_reference,
                property_id=booking.property_id,
                check_in_date=booking.check_in_date,
                check_out_date=booking.check_out_date,
                guest_count=booking.guest_count,
                total_amount=booking.total_amount,
                booking_status=booking.booking_status,
                payment_status=booking.payment_status,
            )
            for booking in bookings
        ]
    
    # ============================================================
    # Cancel Booking
    # ============================================================

    async def cancel_booking(
        self,
        booking_id: UUID,
        request: CancelBookingRequest,
        current_user: User,
    ) -> None:
        """
        Cancels an existing booking.
        """

        booking = await self.repo.get_booking_by_id(
            booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()

        # ============================================================
        # Authorization
        # ============================================================

        if booking.customer_id != current_user.id:
            raise BookingNotFoundException()

        # ============================================================
        # Business Validations
        # ============================================================

        if booking.booking_status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelledException()

        if booking.booking_status == BookingStatus.COMPLETED:
            raise BookingCannotBeCancelledException()

        try:

            # ============================================================
            # Update Booking Status
            # ============================================================

            booking.booking_status = BookingStatus.CANCELLED
            booking.updated_by = current_user.id

            # ============================================================
            # Create Cancellation Record
            # ============================================================

            cancellation = BookingCancellation(
                booking_id=booking.id,
                cancellation_type=CancellationType.CUSTOMER,
                reason=request.reason,
                refund_status=RefundStatus.PENDING,
                refund_amount=Decimal("0.00"),
                cancelled_by=current_user.id,
                created_by=current_user.id,
                updated_by=current_user.id,
            )

            await self.repo.create_booking_cancellation(
                cancellation,
            )

            # ============================================================
            # Create Booking History
            # ============================================================

            history = BookingHistory(
                booking_id=booking.id,
                booking_status=BookingStatus.CANCELLED,
                changed_by=current_user.id,
                remarks=request.reason,
                created_by=current_user.id,
                updated_by=current_user.id,
            )

            await self.repo.create_booking_history(
                history,
            )

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise