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
# Payment Exceptions
# ============================================================

class PaymentNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )


class PaymentAlreadyCompletedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="Payment has already been completed.",
        )


class PaymentAlreadyFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="Payment has already failed.",
        )


class PaymentVerificationFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Payment verification failed.",
        )


class InvalidPaymentStatusException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Payment is not in a valid state for this operation.",
        )


class PaymentAccessDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this payment.",
        )


class InvoiceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Invoice not found.",
        )


class RefundNotAllowedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Refund cannot be processed for this payment.",
        )


class RefundAlreadyProcessedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="Refund has already been processed.",
        )


class InvalidRefundAmountException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Refund amount is invalid.",
        )


class BookingPaymentAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail="A successful payment already exists for this booking.",
        )