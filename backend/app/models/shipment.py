from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class ShipmentStatusEnum(str, enum.Enum):
    PLANNED = "planned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Shipment(Base):
    """Shipments - поставки / фуры"""
    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    shipment_code = Column(String(100), unique=True, nullable=False, index=True)  # CN-RU-001

    # Foreign Keys
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    rate_id = Column(UUID(as_uuid=True), ForeignKey("rates.id"), nullable=False)

    # Cargo details
    cargo_type = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)  # количество (кг, м3 и т.д.)

    # Dates
    departure_date = Column(Date, nullable=True)
    arrival_date = Column(Date, nullable=True)

    # Status
    status = Column(Enum(ShipmentStatusEnum), default=ShipmentStatusEnum.PLANNED)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    supplier = relationship("Supplier", backref="shipments")
    client = relationship("Client", backref="shipments")
    rate = relationship("Rate", backref="shipments")
    expenses = relationship("Expense", back_populates="shipment", cascade="all, delete-orphan")
