# ============================================================
# Standard Library
# ============================================================

from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

# ============================================================
# Third Party
# ============================================================

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

# ============================================================
# Local Imports
# ============================================================

from app.common.enums.property_enums.property_status import (
    PropertyStatus,
)

# ============================================================
# Property Base
# ============================================================

class PropertyBase(BaseModel):
    """
    Base schema shared by Create, Update and Response.
    """

    property_name: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str | None = None

    property_type: str = Field(
        min_length=3,
        max_length=100,
    )

    star_rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    contact_email: EmailStr

    contact_number: str = Field(
        min_length=8,
        max_length=20,
    )

    cancellation_policy: str | None = None

    house_rules: dict[str, str] | None = None

    child_policy: str | None = None

    pet_policy: str | None = None

    smoking_policy: str | None = None

    status: PropertyStatus = PropertyStatus.PENDING

    check_in_time: time

    check_out_time: time


# ============================================================
# Create
# ============================================================

class PropertyCreate(PropertyBase):
    """
    Property creation request.

    owner_id is intentionally omitted.
    It will be taken from the authenticated JWT user.
    """

    address_line_1: str = Field(
        min_length=3,
        max_length=255,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    country: str = Field(
        min_length=2,
        max_length=100,
    )

    postal_code: str = Field(
        min_length=3,
        max_length=20,
    )


# ============================================================
# Update
# ============================================================

class PropertyUpdate(BaseModel):

    property_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = None

    property_type: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    star_rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    contact_email: EmailStr | None = None

    contact_number: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
    )

    cancellation_policy: str | None = None

    house_rules: dict[str, str] | None = None

    child_policy: str | None = None

    pet_policy: str | None = None

    smoking_policy: str | None = None

    status: PropertyStatus | None = None

    check_in_time: time | None = None

    check_out_time: time | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Response
# ============================================================

class PropertyResponse(PropertyBase):

    id: UUID

    owner_id: UUID

    address_id: UUID

    approved_by: UUID | None = None

    approval_remarks: str | None = None

    approved_at: datetime | None = None

    is_verified: bool

    is_deleted: bool

    avg_rating: Decimal | None = None

    total_reviews: int

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )