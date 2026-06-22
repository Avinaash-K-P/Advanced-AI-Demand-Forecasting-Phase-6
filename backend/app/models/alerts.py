from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from app.db.session import Base
from datetime import datetime

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    alert_type = Column(String(100))

    message = Column(String(100))

    severity = Column(String(100))

    status = Column(String(100), default="unread")

    created_at = Column(DateTime, default=datetime.utcnow)