from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from app.db.session import Base

class KPIValues(Base):

    __tablename__ = "kpi_values"

    id = Column(Integer, primary_key=True, index=True)  

    kpi_id = Column(Integer, ForeignKey("kpis.id"))

    organization_id = Column(Integer, ForeignKey("organization.id"))

    value = Column(Float)

    measurement_date = Column(DateTime)

    notes = Column(String(200))

    created_at = Column(DateTime, default=datetime.utcnow)