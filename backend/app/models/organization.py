from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship  
from app.db.session import Base
from datetime import datetime

class Organization(Base):

    __tablename__ = "organization"

    id = Column(Integer, primary_key= True, index = True)

    name = Column(String(255), unique=True ,index = True)

    code = Column(String(100), unique = True)

    industry = Column(String(100))

    description = Column(String(2550))

    contact_email = Column(String(100), unique=True)

    contact_phone = Column(String(10), unique=True)

    address = Column(String(255))

    country = Column(String(100))

    status = Column(String(20), default="active")

    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime)

    forecast_results = relationship("ForecastResult",back_populates="organization")

