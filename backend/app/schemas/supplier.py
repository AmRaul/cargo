from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_info: Optional[str] = None
    notes: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_info: Optional[str] = None
    notes: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
