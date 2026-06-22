from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from app.db.session import Base

class BusinessTargets(Base):
    
    __tablename__ = "business_targets"

    id  = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))  

    annual_plan_id  = Column(Integer, ForeignKey("annual_plans.id"))  

    quarterly_plan_id  = Column(Integer, ForeignKey("quarterly_plans.id"))  

    target_name  = Column(String(20)) 

    target_type = Column(String(20))

    target_value    = Column(Float)

    current_value   = Column(Float)

    unit    = Column(String(20))

    status  = Column(String(30))

    created_at = Column(DateTime, default= datetime.utcnow)

    updated_at = Column(DateTime)