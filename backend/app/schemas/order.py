from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.order import RouteEnum, OrderStatusEnum


class OrderBase(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=255)
    client_phone: str = Field(..., min_length=10, max_length=50)
    client_email: Optional[EmailStr] = None
    company_name: Optional[str] = Field(None, max_length=255)

    route: RouteEnum
    cargo_type: str = Field(..., max_length=255)
    cargo_weight: Optional[float] = Field(None, gt=0)
    cargo_volume: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None

    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    estimated_price: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    status: OrderStatusEnum
    estimated_price: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
