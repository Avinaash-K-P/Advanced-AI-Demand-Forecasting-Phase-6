from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Boolean
from app.db.session import Base
from datetime import datetime

class Workflow(Base):

    __tablename__ = "workflow"

    id = Column(Integer, primary_key = True, index = True)

    organization_id = Column(Integer, ForeignKey("organization.id"))

    name = Column(String(255))

    description = Column(String(500))

    workflow_type = Column(String(50))

    trigger_event = Column(String(50))

    is_active = Column(Boolean, default=True)

    created_by = Column(String(50))

    created_at = Column(DateTime, default = datetime.utcnow)

    updated_at = Column(DateTime)