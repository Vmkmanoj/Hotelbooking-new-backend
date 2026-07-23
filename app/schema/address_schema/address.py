from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class AddressResponse(AddressBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str | None = None
    updated_by: str | None = None

    model_config = ConfigDict(from_attributes=True)