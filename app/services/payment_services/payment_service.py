# ============================================================
# Standard Library
# ============================================================

from datetime import datetime, timezone
from decimal import Decimal
import uuid
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.repositories.payment_repositories.payment_repository import (
    PaymentRepository,
)

from app.schema.payment_schema.payment_schemas import (
    CreatePaymentRequest,
    InvoiceResponse,
    PaymentResponse,
    PaymentSummaryResponse,
    RefundRequest,
    RevenueSummaryResponse,
    VerifyPaymentRequest,
)

from app.exceptions.payment_exceptions.payment_exceptions import (
    BookingPaymentAlreadyExistsException,
    InvoiceNotFoundException,
    InvalidPaymentStatusException,
    InvalidRefundAmountException,
    PaymentAccessDeniedException,
    PaymentAlreadyCompletedException,
    PaymentAlreadyFailedException,
    PaymentNotFoundException,
    PaymentVerificationFailedException,
    RefundAlreadyProcessedException,
    RefundNotAllowedException,
)

from app.exceptions.booking_exceptions.booking_exceptions import (
    BookingNotFoundException,
)

from app.common.enums.payment_enums.payment_enums import (
    InvoiceStatus,
    PaymentStatus,
    RefundStatus,
)

from app.common.enums.booking_enums.booking_enums import (
    BookingStatus,
)

from app.models.payment_models.invoice import Invoice
from app.models.payment_models.payment import Payment

from app.models.users_models.users import User
# ============================================================
# Payment Service
# ============================================================

class PaymentService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

        self.repository = PaymentRepository(
            db,
        )


    # ============================================================
    # Helper Methods
    # ============================================================

    async def generate_payment_reference(
        self,
    ) -> str:
        """
        Generates a unique payment reference.
        """

        return (
            f"PAY-{uuid.uuid4().hex[:8].upper()}"
        )


    # ============================================================
    # Helper Methods
    # ============================================================

    async def generate_invoice_number(
        self,
    ) -> str:
        """
        Generates a unique invoice number.
        """

        return (
            f"INV-{uuid.uuid4().hex[:8].upper()}"
        )


    # ============================================================
    # Create Payment
    # ============================================================

    async def create_payment(
        self,
        request: CreatePaymentRequest,
        current_user: User,
    ) -> PaymentResponse:
        """
        Creates a payment for a booking.
        """

        booking = await self.repository.get_booking_by_id(
            request.booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()
        
        if booking.customer_id != current_user.id:
            raise PaymentAccessDeniedException()
        
        if booking.booking_status != BookingStatus.PENDING:
            raise InvalidPaymentStatusException()
        
        existing_payment = await self.repository.get_payment_by_booking(
            booking.id,
        )

        if existing_payment is not None:
            raise BookingPaymentAlreadyExistsException()
        
        payment_reference = (
            await self.generate_payment_reference()
        )

        payment = Payment(
            booking_id=booking.id,
            payment_reference=payment_reference,
            amount=booking.total_amount,
            currency="INR",
            payment_method=request.payment_method,
            payment_gateway=request.payment_gateway,
            payment_status=PaymentStatus.PENDING,
            refund_status=RefundStatus.NOT_APPLICABLE,
            refund_amount=Decimal("0.00"),
            created_by=current_user.id,
            updated_by=current_user.id,
        )

        try:

            payment = await self.repository.create_payment(
                payment,
            )

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise

        return PaymentResponse(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_reference=payment.payment_reference,
            amount=payment.amount,
            currency=payment.currency,
            payment_method=payment.payment_method,
            payment_gateway=payment.payment_gateway,
            payment_status=payment.payment_status,
            gateway_transaction_id=payment.gateway_transaction_id,
            gateway_response=payment.gateway_response,
            refund_status=payment.refund_status,
            refund_amount=payment.refund_amount,
            paid_at=payment.paid_at,
        )

    # ============================================================
    # Verify Payment
    # ============================================================

    async def verify_payment(
        self,
        payment_id: UUID,
        request: VerifyPaymentRequest,
        current_user: User,
    ) -> PaymentResponse:
        """
        Verifies a payment transaction.
        """

        payment = await self.repository.get_payment_by_id(
            payment_id,
        )

        if payment is None:
            raise PaymentNotFoundException()

        booking = await self.repository.get_booking_by_id(
        payment.booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()

        if booking.customer_id != current_user.id:
            raise PaymentAccessDeniedException()

        if payment.payment_status == PaymentStatus.SUCCESS:
            raise PaymentAlreadyCompletedException()

        if payment.payment_status == PaymentStatus.FAILED:
            raise PaymentAlreadyFailedException()

        if not request.gateway_transaction_id:
            raise PaymentVerificationFailedException()

        payment.gateway_transaction_id = (
            request.gateway_transaction_id
        )

        payment.gateway_response = (
            request.gateway_response
        )

        payment.payment_status = PaymentStatus.SUCCESS

        payment.paid_at = datetime.now(
            timezone.utc,
        )

        payment.updated_by = current_user.id

        booking.booking_status = BookingStatus.CONFIRMED
        booking.payment_status = PaymentStatus.SUCCESS
        booking.updated_by = current_user.id

        existing_invoice = await self.repository.get_invoice_by_booking(
            booking.id,
        )

        if existing_invoice is not None:
            raise InvalidPaymentStatusException()
        
        invoice_number = (
            await self.generate_invoice_number()
        )

        invoice = Invoice(
            booking_id=booking.id,
            invoice_number=invoice_number,
            invoice_status=InvoiceStatus.GENERATED,
            invoice_amount=payment.amount,
            currency=payment.currency,
            generated_at=datetime.now(timezone.utc),
            created_by=current_user.id,
            updated_by=current_user.id,
        )

        try:

            await self.repository.update_payment(
                payment,
            )

            await self.repository.create_invoice(
                invoice,
            )

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise

        return PaymentResponse(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_reference=payment.payment_reference,
            amount=payment.amount,
            currency=payment.currency,
            payment_method=payment.payment_method,
            payment_gateway=payment.payment_gateway,
            payment_status=payment.payment_status,
            gateway_transaction_id=payment.gateway_transaction_id,
            gateway_response=payment.gateway_response,
            refund_status=payment.refund_status,
            refund_amount=payment.refund_amount,
            paid_at=payment.paid_at,
        )

    # ============================================================
    # Get Payment By ID
    # ============================================================

    async def get_payment_by_id(
        self,
        payment_id: UUID,
        current_user: User,
    ) -> PaymentResponse:
        """
        Retrieves a payment by its ID.
        """

        payment = await self.repository.get_payment_by_id(
            payment_id,
        )

        if payment is None:
            raise PaymentNotFoundException()

        booking = await self.repository.get_booking_by_id(
            payment.booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()

        if booking.customer_id != current_user.id:
            raise PaymentAccessDeniedException()

        return PaymentResponse(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_reference=payment.payment_reference,
            amount=payment.amount,
            currency=payment.currency,
            payment_method=payment.payment_method,
            payment_gateway=payment.payment_gateway,
            payment_status=payment.payment_status,
            gateway_transaction_id=payment.gateway_transaction_id,
            gateway_response=payment.gateway_response,
            refund_status=payment.refund_status,
            refund_amount=payment.refund_amount,
            paid_at=payment.paid_at,
        )

    # ============================================================
    # Get My Payments
    # ============================================================

    async def get_my_payments(
        self,
        current_user: User,
    ) -> list[PaymentSummaryResponse]:
        """
        Retrieves all payments for the authenticated customer.
        """

        payments = await self.repository.get_my_payments(
            current_user.id,
        )

        return [
            PaymentSummaryResponse(
                id=payment.id,
                booking_id=payment.booking_id,
                payment_reference=payment.payment_reference,
                amount=payment.amount,
                currency=payment.currency,
                payment_method=payment.payment_method,
                payment_gateway=payment.payment_gateway,
                payment_status=payment.payment_status,
                paid_at=payment.paid_at,
            )
            for payment in payments
        ]

    # ============================================================
    # Download Invoice
    # ============================================================

    async def download_invoice(
        self,
        booking_id: UUID,
        current_user: User,
    ) -> InvoiceResponse:
        """
        Retrieves the invoice for a booking.
        """

        booking = await self.repository.get_booking_by_id(
            booking_id,
        )

        if booking is None:
            raise BookingNotFoundException()

        if booking.customer_id != current_user.id:
            raise PaymentAccessDeniedException()

        invoice = await self.repository.get_invoice_by_booking(
            booking_id,
        )

        if invoice is None:
            raise InvoiceNotFoundException()

        return InvoiceResponse(
            id=invoice.id,
            booking_id=invoice.booking_id,
            invoice_number=invoice.invoice_number,
            invoice_status=invoice.invoice_status,
            currency=invoice.currency,
            invoice_amount=invoice.invoice_amount,
            generated_at=invoice.generated_at,
        )

    # ============================================================
    # Get Property Payments
    # ============================================================

    async def get_property_payments(
        self,
        current_user: User,
    ) -> list[PaymentSummaryResponse]:
        """
        Retrieves all payments for properties owned by the authenticated user.
        """

        payments = await self.repository.get_property_payments(
            current_user.id,
        )

        return [
            PaymentSummaryResponse(
                id=payment.id,
                booking_id=payment.booking_id,
                payment_reference=payment.payment_reference,
                amount=payment.amount,
                currency=payment.currency,
                payment_method=payment.payment_method,
                payment_gateway=payment.payment_gateway,
                payment_status=payment.payment_status,
                paid_at=payment.paid_at,
            )
            for payment in payments
        ]

    # ============================================================
    # Revenue Summary
    # ============================================================

    async def get_revenue_summary(
        self,
        current_user: User,
    ) -> RevenueSummaryResponse:
        """
        Retrieves the revenue summary for properties owned by the authenticated user.
        """

        (
            total_payments,
            total_revenue,
            total_refunds,
        ) = await self.repository.get_revenue_summary(
            current_user.id,
        )

        return RevenueSummaryResponse(
            total_payments=total_payments,
            total_revenue=Decimal(total_revenue),
            total_refunds=Decimal(total_refunds),
            net_revenue=Decimal(total_revenue)
            - Decimal(total_refunds),
        )

    # ============================================================
    # Process Refund
    # ============================================================

    async def process_refund(
        self,
        payment_id: UUID,
        request: RefundRequest,
        current_user: User,
    ) -> PaymentResponse:
        """
        Processes a refund for a payment.
        """

        payment = await self.repository.get_payment_by_id(
            payment_id,
        )

        if payment is None:
            raise PaymentNotFoundException()

        if payment.payment_status != PaymentStatus.SUCCESS:
            raise RefundNotAllowedException()

        if payment.refund_status == RefundStatus.COMPLETED:
            raise RefundAlreadyProcessedException()

        if request.refund_amount > payment.amount:
            raise InvalidRefundAmountException()

        payment.refund_amount = request.refund_amount

        payment.refund_status = RefundStatus.COMPLETED

        payment.payment_status = PaymentStatus.REFUNDED

        booking = await self.repository.get_booking_by_id(
            payment.booking_id,
        )

        booking.payment_status = PaymentStatus.REFUNDED
        booking.updated_by = current_user.id

        payment.updated_by = current_user.id

        try:

            await self.repository.update_payment(
                payment,
            )

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise

        return PaymentResponse(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_reference=payment.payment_reference,
            amount=payment.amount,
            currency=payment.currency,
            payment_method=payment.payment_method,
            payment_gateway=payment.payment_gateway,
            payment_status=payment.payment_status,
            gateway_transaction_id=payment.gateway_transaction_id,
            gateway_response=payment.gateway_response,
            refund_status=payment.refund_status,
            refund_amount=payment.refund_amount,
            paid_at=payment.paid_at,
        )