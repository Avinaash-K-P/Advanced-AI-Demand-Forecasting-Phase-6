from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from app.db.session import Base

class GovernanceAuditLogs(Base):

    __tablename__ = "governance_audit_logs"

    id = Column(Integer, primary_key=True, index=True) 

    organization_id = Column(Integer, ForeignKey("organization.id")) 

    entity_type = Column(String(50)) 

    entity_id = Column(Integer)

    action = Column(String(20)) 

    performed_by = Column(String(50)) 

    old_value = Column(String(50)) 

    new_value = Column(String(50)) 

    created_at = Column(DateTime, default=datetime.utcnow)