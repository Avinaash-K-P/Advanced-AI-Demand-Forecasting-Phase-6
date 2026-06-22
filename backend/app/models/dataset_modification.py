from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class DatasetModification(Base):

    __tablename__ = "dataset_modifications"

    id = Column(Integer, primary_key=True, index=True)

    dataset_version_id = Column(Integer, ForeignKey("dataset_versions.id"), nullable=False)

    modified_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    modification_type = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    rows_affected = Column(Integer, default=0)

    previous_value = Column(Text, nullable=True)

    new_value = Column(Text, nullable=True)

    modified_at = Column(DateTime, default=datetime.utcnow, index=True)

    modifier = relationship("User", foreign_keys=[modified_by])

    version = relationship("DatasetVersion", back_populates="modifications")