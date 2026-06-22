from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from app.db.session import Base

class ForecastLifecycle(Base):

    __tablename__ = "forecast_lifecycle"

    id  = Column(Integer, primary_key=True, index=True) 

    forecast_id = Column(Integer, ForeignKey("forecast_results.id"))

    organization_id = Column(Integer, ForeignKey("organization.id")) 

    current_stage  = Column(String(50)) 

    entered_at = Column(DateTime, default=datetime.utcnow)

    updated_by = Column(String(50)) 

    notes = Column(String(200)) 