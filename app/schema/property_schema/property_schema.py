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

from app.common.enums.property_enums.property_type import (
    PropertyType,
)

# ============================================================
# Property Base
# ============================================================

class PropertyBase(BaseModel):
    """
    Base schema shared by Property Create, Update and Response.
    """

    property_name: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str | None = None

    property_type: PropertyType

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

    house_rules: dict[str, bool] | None = None

    child_policy: str | None = None

    pet_policy: str | None = None

    smoking_policy: str | None = None

    status: PropertyStatus = PropertyStatus.PENDING

    check_in_time: time

    check_out_time: time


# ============================================================
# Property Create
# ============================================================

class PropertyCreate(PropertyBase):
    """
    Property creation request.

    owner_id is intentionally omitted.
    The authenticated user (JWT) becomes the owner.
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
# Property Update
# ============================================================

class PropertyUpdate(BaseModel):
    """
    Property update request.

    Every field is optional to support PATCH updates.
    """

    property_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = None

    property_type: PropertyType | None = None

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

    house_rules: dict[str, bool] | None = None

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
# Property Response
# ============================================================

class PropertyResponse(PropertyBase):
    """
    Property response returned to the client.
    """

    id: UUID

    owner_id: UUID

    address_id: UUID

    approved_by: UUID | None = None

    approval_remarks: str | None = None

    approved_at: datetime | None = None

    is_verified: bool

    is_deleted: bool

    avg_rating: Decimal

    total_reviews: int

    created_by: str | None = None

    updated_by: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )