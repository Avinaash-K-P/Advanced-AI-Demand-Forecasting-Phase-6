from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from app.db.session import Base
from datetime import datetime

class WorkflowLogs(Base):

    __tablename__ = "workflow_logs"

    id = Column(Integer, primary_key = True, index = True)

    workflow_execution_id = Column(Integer, ForeignKey("workflow_executions.id"))  

    workflow_step_id = Column(String(50))   

    log_level = Column(String(50))   

    message = Column(String(50))

    created_at = Column(DateTime, default = datetime.utcnow)