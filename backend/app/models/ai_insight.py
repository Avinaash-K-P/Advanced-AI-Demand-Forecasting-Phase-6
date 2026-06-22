# models/ai_insight.py

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.session import Base


class AIInsight(Base):

    __tablename__ = "ai_insights"

    id = Column(Integer,primary_key=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    insight_type = Column(String(100))

    title = Column( String(255))

    description = Column(Text)

    severity = Column(String(50))

    created_at = Column(DateTime,default=datetime.utcnow)