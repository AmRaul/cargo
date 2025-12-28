from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Supplier(Base):
    """Suppliers / Origin - откуда груз (Китай, завод, агент)"""
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_info = Column(Text, nullable=True)  # phone, email, etc
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
