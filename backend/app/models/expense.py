from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Date, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class ExpenseTypeEnum(str, enum.Enum):
    CUSTOMS = "customs"
    DELIVERY = "delivery"
    AGENT_FEE = "agent_fee"
    WAREHOUSE = "warehouse"


class Expense(Base):
    """Expenses - расходы по поставке"""
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Foreign Key
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)

    # Expense details
    expense_type = Column(Enum(ExpenseTypeEnum), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    comment = Column(Text, nullable=True)
    expense_date = Column(Date, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    shipment = relationship("Shipment", back_populates="expenses")
