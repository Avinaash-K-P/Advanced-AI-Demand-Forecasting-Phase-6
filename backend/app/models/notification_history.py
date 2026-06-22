from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base

class NotificationHistory(Base):

    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True)

    notification_id = Column(Integer,ForeignKey("notifications.id"))

    user_id = Column(Integer,ForeignKey("users.id"))

    delivery_status = Column(String(20))

    delivered_at = Column(DateTime)

    read_at = Column(DateTime)