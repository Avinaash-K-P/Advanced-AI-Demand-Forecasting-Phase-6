from sqlalchemy import Column, ForeignKey, Integer, Index, Float, Date, DateTime, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class ForecastResult(Base):

    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    forecast_date = Column(Date, index=True)

    predicted_demand = Column(Float)

    prophet_prediction = Column(Float)

    lr_prediction = Column(Float)

    ma_prediction = Column(Float)

    sales_trend = Column(Float, default = 0)

    weekly_pattern = Column(Float, default = 0)

    yearly_pattern = Column(Float, default = 0)

    confidence_score = Column(Float,default=0)
    
    approval_status = Column(String(50), default="Draft")

    organization = relationship("Organization",back_populates="forecast_results")

    __table_args__ = (

    Index("idx_forecast_date", "forecast_date"),
    
    )
    