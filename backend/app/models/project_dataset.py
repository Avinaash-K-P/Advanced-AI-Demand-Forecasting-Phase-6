from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class ProjectDataset(Base):

    __tablename__ = "project_datasets"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("forecast_projects.id"), nullable=False)

    dataset_name = Column(String(255), nullable=False)

    sales_reference_id = Column(Integer, ForeignKey("sales.id"), nullable=True)

    uploaded_by = Column(String(100), nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("ForecastProject", back_populates="datasets")