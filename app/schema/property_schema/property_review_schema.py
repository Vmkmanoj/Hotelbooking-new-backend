# ============================================================
# Standard Library
# ============================================================

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
# Approve Property
# ============================================================

class PropertyApproveRequest(BaseModel):
    """
    Property approval request.

    Remarks are optional.
    """

    approval_remarks: str | None = Field(
        default=None,
        max_length=500,
    )


# ============================================================
# Reject Property
# ============================================================

class PropertyRejectRequest(BaseModel):
    """
    Property rejection request.

    Remarks are mandatory.
    """

    approval_remarks: str = Field(
        min_length=5,
        max_length=500,
    )


# ============================================================
# Review Response
# ============================================================

class PropertyReviewResponse(BaseModel):
    """
    Response after approving/rejecting a property.
    """

    success: bool

    message: str

    property_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )