from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base

class QuarterlyPlans(Base):
    
    __tablename__ = "quarterly_plans"

    id  = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))  

    annual_plan_id  = Column(Integer, ForeignKey("annual_plans.id"))  

    quarter = Column(String(10))

    year = Column(String(10))   

    name = Column(String(100))   

    description = Column(String(500))

    status  = Column(String(20))

    created_at = Column(DateTime, default= datetime.utcnow)

    updated_at = Column(DateTime)