from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID


class RateBase(BaseModel):
    cargo_type: str = Field(..., max_length=255)
    supplier_id: UUID
    client_id: Optional[UUID] = None
    buy_rate: float = Field(..., gt=0)
    sell_rate: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=10)
    unit: str = Field(..., max_length=20)  # kg, cbm, item
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None


class RateCreate(RateBase):
    pass


class RateUpdate(BaseModel):
    cargo_type: Optional[str] = Field(None, max_length=255)
    supplier_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    buy_rate: Optional[float] = Field(None, gt=0)
    sell_rate: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=10)
    unit: Optional[str] = Field(None, max_length=20)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None


class RateResponse(RateBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
