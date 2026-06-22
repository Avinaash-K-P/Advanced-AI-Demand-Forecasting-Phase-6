from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class ForecastRevision(Base):

    __tablename__ = "forecast_revisions"

    id = Column(Integer, primary_key=True, index=True)

    revision_number = Column(Integer, nullable=False)
    # Auto-incremented per forecast_date — v1, v2, v3...

    forecast_date = Column(Date, nullable=False, index=True)

    # Full snapshot of all model predictions at time of revision
    predicted_demand = Column(Float, nullable=False)

    prophet_prediction = Column(Float, nullable=True)

    lr_prediction = Column(Float, nullable=True)

    ma_prediction = Column(Float, nullable=True)

    sales_trend = Column(Float, default=0)

    weekly_pattern = Column(Float, default=0)

    yearly_pattern = Column(Float, default=0)

    confidence_score = Column(Float, default=0)

    # Revision metadata
    model_type = Column(String(100), default="Ensemble")

    change_summary = Column(Text, nullable=True)
    # e.g. "Demand increased by 12.5% from previous revision"

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    project_id = Column(Integer, ForeignKey("forecast_projects.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])