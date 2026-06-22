from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from app.db.session import Base
from datetime import datetime

class Workflowsteps(Base):

    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key = True, index = True)

    workflow_id = Column(Integer, ForeignKey("workflow.id"))

    step_order = Column(Integer)

    step_name = Column(String(50))

    step_type = Column(String(50))

    configuration = Column(String(50))

    is_required = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)