# ============================================================
# Third Party
# ============================================================

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

# ============================================================
# Reject Property Request
# ============================================================

class RejectPropertyRequest(BaseModel):
    """
    Reject a property.
    """

    remarks: str = Field(
        min_length=5,
        max_length=500,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Suspend Property Request
# ============================================================

class SuspendPropertyRequest(BaseModel):
    """
    Suspend an approved property.
    """

    remarks: str = Field(
        min_length=5,
        max_length=500,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Activate Property Request
# ============================================================

class ActivatePropertyRequest(BaseModel):
    """
    Activate a suspended property.
    """

    remarks: str | None = Field(
        default=None,
        max_length=500,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )