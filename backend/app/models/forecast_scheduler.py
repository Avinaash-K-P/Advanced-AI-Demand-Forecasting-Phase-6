from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.db.session import Base

class ForecastSchedule(Base):

    __tablename__ = "forecast_schedules"

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    interval_type = Column(String(10))

    interval_value = Column(Integer)

    is_active = Column(Boolean, default=True)

    updated_at = Column(DateTime, default=datetime.utcnow)