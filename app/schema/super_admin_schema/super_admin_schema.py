# ============================================================
# Standard Library
# ============================================================

from datetime import datetime
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

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

# ============================================================
# Pending Property Response
# ============================================================

class PendingPropertyResponse(BaseModel):
    """
    Property waiting for admin approval.
    """

    id: UUID

    property_name: str

    owner_name: str

    owner_email: str

    city: str

    state: str

    status: PropertyStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Property Detail Response
# ============================================================

class PropertyDetailResponse(BaseModel):
    """
    Detailed property information for admin review.
    """

    id: UUID

    property_name: str

    description: str | None = None

    owner_name: str

    owner_email: str

    owner_phone: str

    address_line_1: str

    address_line_2: str | None = None

    city: str

    state: str

    country: str

    postal_code: str

    property_type: str

    status: PropertyStatus

    is_verified: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Approve Property Request
# ============================================================

class ApprovePropertyRequest(BaseModel):
    """
    Approve a property.
    """

    remarks: str | None = Field(
        default=None,
        max_length=500,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Generic Message Response
# ============================================================

class MessageResponse(BaseModel):
    """
    Generic success/failure response.
    """

    success: bool

    message: str