from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Float
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RouteEnum(str, enum.Enum):
    UAE_TO_RF = "uae_to_rf"
    TURKEY_TO_RF = "turkey_to_rf"


class OrderStatusEnum(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Клиентская информация
    client_name = Column(String(255), nullable=False)
    client_phone = Column(String(50), nullable=False)
    client_email = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)

    # Детали груза
    route = Column(Enum(RouteEnum), nullable=False)
    cargo_type = Column(String(255), nullable=False)
    cargo_weight = Column(Float, nullable=True)
    cargo_volume = Column(Float, nullable=True)
    description = Column(Text, nullable=True)

    # Адреса
    pickup_address = Column(Text, nullable=True)
    delivery_address = Column(Text, nullable=True)

    # Статус и дополнительно
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.NEW)
    estimated_price = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
