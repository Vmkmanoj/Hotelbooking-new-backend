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

from app.schema.auth_schema.auth import (
    CustomerRegister,
    PropertyRegister,
    RegisterResponse,
)

from app.schema.auth_schema.login import (
    LoginRequest,
    LoginResponse,
)

from app.services.auth_services.auth_service import (
    AuthService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# ============================================================
# Login
# ============================================================

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    return await service.login(request)


# ============================================================
# Register Customer
# ============================================================

@router.post(
    "/register/customer",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_customer(
    request: CustomerRegister,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    return await service.customer_register(request)


# ============================================================
# Register Property Owner
# ============================================================

@router.post(
    "/register/property-owner",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_property_owner(
    request: PropertyRegister,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    return await service.property_owner_register(request)