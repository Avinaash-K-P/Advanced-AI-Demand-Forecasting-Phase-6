from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from app.db.session import Base

class KPIAlerts(Base):

    __tablename__ = "kpi_alerts"

    id = Column(Integer, primary_key=True, index=True)  

    kpi_id = Column(Integer, ForeignKey("kpis.id"))

    organization_id = Column(Integer, ForeignKey("organization.id"))

    alert_type = Column(String(20))

    threshold_value = Column(Float)

    current_value = Column(Float)

    status = Column(String(20))

    triggered_at = Column(DateTime)

    resolved_at = Column(DateTime)