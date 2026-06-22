from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String

from app.db.session import Base


class ForecastAccuracy(Base):

    __tablename__ = "forecast_accuracy"

    id = Column(Integer,primary_key=True,index=True)
    
    organization_id = Column(Integer, ForeignKey("organization.id"))    

    evaluation_date = Column(Date)

    actual_demand = Column(Float)

    predicted_demand = Column(Float)

    accuracy_percentage = Column(Float)

    model_type = Column(String(100)
)