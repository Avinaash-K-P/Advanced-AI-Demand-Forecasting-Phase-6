from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Float
from app.db.session import Base
from datetime import datetime

class ExecutiveDashboard(Base):

    __tablename__ = "executive_dashboard"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organization.id")
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    total_users = Column(Integer)

    total_forecasts = Column(Integer)

    total_reports = Column(Integer)

    total_kpis = Column(Integer)

    quality_score = Column(Float)

    active_workflows = Column(Integer)