from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    
    
    username = Column(String(50), unique=True, nullable=False)
    
    email = Column(String(100), unique=True, nullable=False)
    
    password = Column(String(255), nullable=False)   
    
    role = Column(String(20), default = "viewer")  

    status = Column(String(20),default="active")

    reset_token = Column(String(255),nullable=True)

    reset_token_expiry = Column(DateTime,nullable=True)

    logs = relationship("APILog",back_populates="user")
    


