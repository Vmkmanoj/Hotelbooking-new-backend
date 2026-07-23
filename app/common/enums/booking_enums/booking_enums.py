# ============================================================
# Standard Library
# ============================================================

from enum import Enum

# ============================================================
# Booking Status
# ============================================================

class BookingStatus(str, Enum):
    """
    Lifecycle status of a booking.
    """

    PENDING = "PENDING"

    CONFIRMED = "CONFIRMED"

    CHECKED_IN = "CHECKED_IN"

    CHECKED_OUT = "CHECKED_OUT"

    COMPLETED = "COMPLETED"

    CANCELLED = "CANCELLED"

# ============================================================
# Payment Status
# ============================================================

class PaymentStatus(str, Enum):
    """
    Payment status for a booking.
    """

    PENDING = "PENDING"

    PARTIALLY_PAID = "PARTIALLY_PAID"

    PAID = "PAID"

    REFUNDED = "REFUNDED"

    FAILED = "FAILED"

# ============================================================
# Cancellation Type
# ============================================================

class CancellationType(str, Enum):
    """
    Indicates who cancelled the booking.
    """

    CUSTOMER = "CUSTOMER"

    PROPERTY_OWNER = "PROPERTY_OWNER"

    SUPER_ADMIN = "SUPER_ADMIN"

    SYSTEM = "SYSTEM"


# ============================================================
# Refund Status
# ============================================================

class RefundStatus(str, Enum):
    """
    Refund processing status.
    """

    NOT_APPLICABLE = "NOT_APPLICABLE"

    PENDING = "PENDING"

    PROCESSED = "PROCESSED"

    FAILED = "FAILED"