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

from app.services.payment_services.payment_service import (
    PaymentService,
)

from app.schema.payment_schema.payment_schemas import (
    CreatePaymentRequest,
    VerifyPaymentRequest,
    RefundRequest,
    PaymentResponse,
    PaymentSummaryResponse,
    InvoiceResponse,
    RevenueSummaryResponse,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

# ============================================================
# Service Dependency
# ============================================================

def get_payment_service(
    db: AsyncSession = Depends(get_db),
) -> PaymentService:
    return PaymentService(db)


# ============================================================
# Create Payment
# ============================================================

@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    request: CreatePaymentRequest,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:

    return await service.create_payment(
        request=request,
        current_user=current_user,
    )


# ============================================================
# Verify Payment
# ============================================================

@router.patch(
    "/{payment_id}/verify",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_payment(
    payment_id: UUID,
    request: VerifyPaymentRequest,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:

    return await service.verify_payment(
        payment_id=payment_id,
        request=request,
        current_user=current_user,
    )


# ============================================================
# Get Payment By ID
# ============================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_payment_by_id(
    payment_id: UUID,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:

    return await service.get_payment_by_id(
        payment_id=payment_id,
        current_user=current_user,
    )


# ============================================================
# Get My Payments
# ============================================================

@router.get(
    "/me",
    response_model=list[PaymentSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_my_payments(
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSummaryResponse]:

    return await service.get_my_payments(
        current_user=current_user,
    )


# ============================================================
# Download Invoice
# ============================================================

@router.get(
    "/{booking_id}/invoice",
    response_model=InvoiceResponse,
    status_code=status.HTTP_200_OK,
)
async def download_invoice(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> InvoiceResponse:

    return await service.download_invoice(
        booking_id=booking_id,
        current_user=current_user,
    )


# ============================================================
# Property Payments
# ============================================================

@router.get(
    "/property",
    response_model=list[PaymentSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_property_payments(
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSummaryResponse]:

    return await service.get_property_payments(
        current_user=current_user,
    )


# ============================================================
# Revenue Summary
# ============================================================

@router.get(
    "/property/revenue",
    response_model=RevenueSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_revenue_summary(
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> RevenueSummaryResponse:

    return await service.get_revenue_summary(
        current_user=current_user,
    )


# ============================================================
# Process Refund
# ============================================================

@router.patch(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def process_refund(
    payment_id: UUID,
    request: RefundRequest,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:

    return await service.process_refund(
        payment_id=payment_id,
        request=request,
        current_user=current_user,
    )