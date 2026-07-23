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

from app.schema.address_schema.address import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
)

from app.services.property_services.address_service import (
    AddressService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)

# ============================================================
# Create Address
# ============================================================

@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    request: AddressCreate,
    db: AsyncSession = Depends(get_db),
):

    service = AddressService(db)

    return await service.create_address(
        request,
    )


# ============================================================
# Get All Addresses
# ============================================================

@router.get(
    "",
    response_model=list[AddressResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_addresses(
    db: AsyncSession = Depends(get_db),
):

    service = AddressService(db)

    return await service.get_all_addresses()


# ============================================================
# Get Address By Id
# ============================================================

@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
async def get_address(
    address_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = AddressService(db)

    return await service.get_address(
        address_id,
    )


# ============================================================
# Update Address
# ============================================================

@router.patch(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
async def update_address(
    address_id: UUID,
    request: AddressUpdate,
    db: AsyncSession = Depends(get_db),
):

    service = AddressService(db)

    return await service.update_address(
        address_id=address_id,
        address_data=request,
    )

# ============================================================
# Delete Address
# ============================================================

# @router.delete(
#     "/{address_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_address(
#     address_id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#
#     service = AddressService(db)
#
#     await service.delete_address(
#         address_id,
#     )