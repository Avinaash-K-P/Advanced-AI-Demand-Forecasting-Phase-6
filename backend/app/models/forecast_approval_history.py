from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base

class ForecastApprovalHistory(Base):

    __tablename__ = "forecast_approval_history"

    id = Column(Integer,primary_key=True, index= True)

    forecast_approval_id = Column(Integer, ForeignKey("forecast_approval.id"))

    forecast_id = Column(Integer, ForeignKey("forecast_results.id"))

    action_by = Column(String(100))

    old_status = Column(String(30))

    new_status = Column(String(30))

    remarks = Column(String(255))

    action_date = Column(DateTime)     