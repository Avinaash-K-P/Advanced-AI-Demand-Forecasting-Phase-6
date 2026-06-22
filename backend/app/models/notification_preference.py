from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.session import Base

class NotificationPreferences(Base):

    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    email_enabled = Column(Boolean)

    in_app_enabled = Column(Boolean)

    forecast_alerts = Column(Boolean)

    workflow_alerts = Column(Boolean)

    report_alerts = Column(Boolean)