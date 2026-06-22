from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from app.db.session import Base

class DataQualityReports(Base):

    __tablename__ = "data_quality_reports"

    id = Column(Integer, primary_key=True, index=True) 

    organization_id = Column(Integer, ForeignKey("organization.id"))

    dataset_id = Column(Integer,ForeignKey("project_datasets.id"))

    overall_score = Column(Float)

    total_records = Column(Integer)

    valid_records = Column(Integer)

    invalid_records = Column(Integer)

    duplicate_records = Column(Integer)

    missing_value_count = Column(Integer)

    outlier_count = Column(Integer)

    status = Column(String(20))

    generated_by = Column(String(50))

    generated_at = Column(DateTime, default=datetime.utcnow)