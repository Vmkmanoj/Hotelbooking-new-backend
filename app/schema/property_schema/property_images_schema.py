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
# Property Image Create
# ============================================================

class PropertyImageCreate(BaseModel):
    """
    Schema for uploading a property image.
    """

    property_id: UUID

    image_url: str = Field(
        min_length=5,
        max_length=500,
    )

    caption: str | None = Field(
        default=None,
        max_length=255,
    )

    is_primary: bool = False

    is_cover: bool = False

    display_order: int = Field(
        default=1,
        ge=1,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Property Image Update
# ============================================================

class PropertyImageUpdate(BaseModel):
    """
    Schema for updating a property image.
    """

    image_url: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    caption: str | None = Field(
        default=None,
        max_length=255,
    )

    is_primary: bool | None = None

    is_cover: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=1,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# Property Image Response
# ============================================================

class PropertyImageResponse(BaseModel):
    """
    Property image response.
    """

    id: UUID

    property_id: UUID

    image_url: str

    caption: str | None = None

    is_primary: bool

    is_cover: bool

    display_order: int

    created_by: UUID | None = None

    updated_by: UUID | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )