from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Rate(Base):
    """Rates - ставки закупки и продажи"""
    __tablename__ = "rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    cargo_type = Column(String(255), nullable=False)  # например "perfumes"

    # Foreign Keys
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)  # может быть NULL

    # Ставки
    buy_rate = Column(Float, nullable=False)  # ставка закупки, например 1.78
    sell_rate = Column(Float, nullable=False)  # ставка клиенту, например 2.10
    currency = Column(String(10), nullable=False, default="USD")
    unit = Column(String(20), nullable=False)  # kg / cbm / item

    # Validity period
    valid_from = Column(Date, nullable=True)
    valid_to = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    supplier = relationship("Supplier", backref="rates", lazy="joined")
    client = relationship("Client", backref="rates", lazy="joined")

    def __repr__(self):
        supplier_name = self.supplier.name if self.supplier else "N/A"
        client_info = f" → {self.client.client_number}" if self.client else ""
        return f"{self.cargo_type} от {supplier_name}{client_info}"
