from pydantic import BaseModel
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str
    code: str
    industry: Optional[str] = None
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None