from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from app.models.shipment import ShipmentStatusEnum


class ShipmentBase(BaseModel):
    shipment_code: str = Field(..., min_length=1, max_length=100)
    supplier_id: UUID
    client_id: UUID
    rate_id: UUID
    cargo_type: str = Field(..., max_length=255)
    quantity: float = Field(..., gt=0)
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
    status: ShipmentStatusEnum = ShipmentStatusEnum.PLANNED


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    shipment_code: Optional[str] = Field(None, min_length=1, max_length=100)
    supplier_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    rate_id: Optional[UUID] = None
    cargo_type: Optional[str] = Field(None, max_length=255)
    quantity: Optional[float] = Field(None, gt=0)
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
    status: Optional[ShipmentStatusEnum] = None


class ShipmentResponse(ShipmentBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ShipmentWithFinance(ShipmentResponse):
    """Shipment response with financial calculations"""
    revenue: float
    cost_of_goods: float
    total_expenses: float
    profit: float
    margin_percent: float
