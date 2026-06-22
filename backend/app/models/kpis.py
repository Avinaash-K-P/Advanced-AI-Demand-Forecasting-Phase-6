from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from app.db.session import Base

class Kpis(Base):

    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)  

    organization_id = Column(Integer, ForeignKey("organization.id"))

    name = Column(String(255))

    description = Column(String(500))

    category = Column(String(20))

    unit = Column(String(20))

    target_value = Column(Float)

    warning_threshold = Column(Float)

    critical_threshold = Column(Float)

    is_active = Column(String(20))

    created_by = Column(String(30))

    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime)