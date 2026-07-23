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
# Favorite Create
# ============================================================

class FavoriteCreate(BaseModel):
    """
    Add a property to the user's favorites.

    user_id will normally come from the authenticated JWT,
    but keeping it here makes the schema reusable if needed.
    """

    property_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Favorite Response
# ============================================================

class FavoriteResponse(BaseModel):
    """
    Favorite response.
    """

    id: UUID

    user_id: UUID

    property_id: UUID

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Favorite Action Response
# ============================================================

class FavoriteActionResponse(BaseModel):
    """
    Generic response for add/remove favorite actions.
    """

    success: bool

    message: str