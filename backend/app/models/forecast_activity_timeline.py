from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class ForecastActivityTimeline(Base):

    __tablename__ = "forecast_activity_timeline"

    id = Column(Integer, primary_key=True, index=True)

    forecast_id = Column(Integer, ForeignKey("forecast_results.id"), nullable=True)
    # Nullable — some actions are model-level, not tied to a specific forecast row

    project_id = Column(Integer, ForeignKey("forecast_projects.id"), nullable=True)
    # Nullable — activity may exist outside a project context

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String(100), nullable=False)
    # FORECAST_GENERATED / MODEL_RETRAINED / ACCURACY_EVALUATED /
    # COMMENT_ADDED / REVISION_SAVED / FORECAST_EXPORTED / FORECAST_SHARED

    category = Column(String(50), nullable=False)
    # forecast / model / report / collaboration

    description = Column(Text, nullable=True)

    meta_value = Column(String(255), nullable=True)
    # e.g. accuracy %, model type, confidence score — quick reference value

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id]) 