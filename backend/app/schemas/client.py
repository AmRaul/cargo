from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_info: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_info: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(ClientBase):
    id: UUID
    client_number: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
