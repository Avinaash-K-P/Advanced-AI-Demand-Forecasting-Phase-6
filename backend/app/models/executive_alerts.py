from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from app.db.session import Base
from datetime import datetime

class ExecutiveAlerts(Base):

    __tablename__ = "executive_alerts"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organization.id")
    )

    alert_type = Column(String(50))

    severity = Column(String(20))

    message = Column(String(255))

    status = Column(String(20))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )