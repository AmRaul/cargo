from sqlalchemy import Column, String, Text, DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.core.database import Base
import uuid


class Client(Base):
    """Clients - клиенты"""
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    client_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_info = Column(Text, nullable=True)  # phone, email, etc
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def generate_next_client_number(session: Session) -> str:
    """Generate next client number in format CL-0001"""
    # Get the last client by client_number
    last_client = session.query(Client).order_by(Client.client_number.desc()).first()

    if not last_client or not last_client.client_number:
        return "CL-0001"

    # Extract number from CL-XXXX format
    try:
        last_number = int(last_client.client_number.split("-")[1])
        next_number = last_number + 1
        return f"CL-{next_number:04d}"
    except (IndexError, ValueError):
        # If parsing fails, start from 0001
        return "CL-0001"


@event.listens_for(Client, "before_insert")
def receive_before_insert(mapper, connection, target):
    """Auto-generate client_number before insert if not set"""
    if not target.client_number:
        # Create a session from the connection
        session = Session(bind=connection)
        target.client_number = generate_next_client_number(session)
        session.close()
