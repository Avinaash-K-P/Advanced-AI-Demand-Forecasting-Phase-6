from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from app.db.session import Base

class DatasetValidationLogs(Base):

    __tablename__ = "dataset_validation_logs"

    id = Column(Integer, primary_key=True, index=True) 

    quality_report_id = Column(Integer, ForeignKey("data_quality_reports.id"))

    dataset_id = Column(Integer, ForeignKey("project_datasets.id"))

    validation_type = Column(String(30))

    severity = Column(String(30))

    message = Column(String(255))

    affected_records = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)