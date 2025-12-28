from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from app.models.expense import ExpenseTypeEnum


class ExpenseBase(BaseModel):
    shipment_id: UUID
    expense_type: ExpenseTypeEnum
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=10)
    comment: Optional[str] = None
    expense_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    expense_type: Optional[ExpenseTypeEnum] = None
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=10)
    comment: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseResponse(ExpenseBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
