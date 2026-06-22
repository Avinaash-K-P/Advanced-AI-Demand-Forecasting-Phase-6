from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
from datetime import datetime

class Notifications(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))

    title = Column(String(255))

    message = Column(String(1000))

    notification_type = Column(String(50))

    target_role = Column(String(50))

    status = Column(String(20))

    created_by = Column(String(50))

    created_at = Column(DateTime, default= datetime.utcnow())