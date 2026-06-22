from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base

class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer,primary_key=True,index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    filename = Column(String(255))

    file_path = Column(String(255))

    file_type = Column(String(50))

    generated_by = Column(String(100))

    created_at = Column(DateTime,default=datetime.utcnow)