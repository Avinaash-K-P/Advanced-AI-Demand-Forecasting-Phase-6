from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base

class AnnualPlans(Base):
    
    __tablename__ = "annual_plans"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))  

    year = Column(String(10))

    name = Column(String(100))

    description = Column(String(500))

    status = Column(String(50))

    created_by = Column(String(100))

    created_at = Column(DateTime, default= datetime.utcnow)

    updated_at = Column(DateTime)