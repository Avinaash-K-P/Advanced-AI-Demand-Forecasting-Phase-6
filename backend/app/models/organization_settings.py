from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from app.db.session import Base
from datetime import datetime

class OrganizationSettings(Base):

    __tablename__ = "organization_settings"

    id = Column(Integer, primary_key= True, index = True)
    
    organization_id = Column(Integer, ForeignKey("organization.id"))
 
    timezone = Column(String(100))

    currency = Column(String(20))

    forecast_retention_days = Column(Integer)

    default_forecast_model = Column(String(100))

    notifications_enabled = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)