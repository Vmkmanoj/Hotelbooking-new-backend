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
)

# ============================================================
# Recent Property Response
# ============================================================

class RecentPropertyResponse(BaseModel):
    """
    Recently registered properties.
    """

    id: UUID

    property_name: str

    owner_name: str

    city: str

    status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Dashboard Response
# ============================================================

class DashboardResponse(BaseModel):
    """
    Super Admin Dashboard Summary.
    """

    # ==========================
    # User Statistics
    # ==========================

    total_users: int

    total_customers: int

    total_property_owners: int

    total_admins: int

    # ==========================
    # Property Statistics
    # ==========================

    total_properties: int

    pending_properties: int

    approved_properties: int

    rejected_properties: int

    suspended_properties: int = 0



    model_config = ConfigDict(
        from_attributes=True,
    )