from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)
from app.db.session import Base
from datetime import datetime

class ForecastHistory(Base):

    __tablename__ = "forecast_history"

    id = Column(Integer, primary_key=True, index=True)

    forecast_date = Column(String(100))

    predicted_demand = Column(Float)

    model_type = Column(String(100))

    generated_by = Column(String(100))

    generated_at = Column(DateTime, default=datetime.utcnow)