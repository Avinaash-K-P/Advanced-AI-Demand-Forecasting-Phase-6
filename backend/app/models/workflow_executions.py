from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base

class WorkflowExecution(Base):

    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key = True, index = True)

    workflow_id = Column(Integer, ForeignKey("workflow.id"))

    organization_id = Column(Integer, ForeignKey("organization.id"))

    status = Column(String(50))

    started_at  = Column(DateTime)

    completed_at = Column(DateTime)    

    triggered_by = Column(String(50))    

    execution_context = Column(String(50))   

    error_message = Column(String(50))