from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base

class ForecastApproval(Base):

    __tablename__ ="forecast_approval"

    id = Column(Integer, primary_key=True, index=True)

    forecast_id = Column(Integer, ForeignKey("forecast_results.id"))

    organization_id = Column(Integer, ForeignKey("organization.id"))

    submitted_by = Column(String(100))

    assigned_reviewer = Column(String(100))

    status = Column(String(20), default="active")

    submitted_at = Column(DateTime, default = datetime.utcnow)

    reviewed_at = Column(DateTime)

    comments = Column(String(500))

    created_at = Column(DateTime, default = datetime.utcnow)

    updated_at = Column(DateTime)
    