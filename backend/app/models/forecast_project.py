from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime


class ForecastProject(Base):

    __tablename__ = "forecast_projects"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    name = Column(String(255), nullable=False)

    description = Column(String(500), nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String(50), default="active")

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])

    members = relationship("ProjectMember", back_populates="project")

    datasets = relationship("ProjectDataset", back_populates="project")

    forecasts = relationship("ProjectForecast", back_populates="project")

    reports = relationship("ProjectReport", back_populates="project")

    activities = relationship("ProjectActivity", back_populates="project")