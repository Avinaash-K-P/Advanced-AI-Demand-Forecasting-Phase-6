# models/dashboard_preferences.py

from sqlalchemy import Column,Integer,Boolean,ForeignKey
from app.db.session import Base

class DashboardPreference(Base):

    __tablename__ = "dashboard_preferences"

    id = Column(Integer,primary_key=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    user_id = Column(Integer,ForeignKey("users.id"),unique=True)

    show_kpi = Column(Boolean,default=True)

    show_revenue = Column(Boolean,default=True)

    show_profit = Column(Boolean,default=True)

    show_growth = Column(Boolean,default=True)

    show_cost = Column(Boolean,default=True)

    show_ai_insights = Column(Boolean,default=True)