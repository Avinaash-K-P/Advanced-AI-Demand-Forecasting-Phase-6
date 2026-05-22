from sqlalchemy import Column, Integer, DateTime
from app.db.session import Base
from datetime import datetime


class ModelMetadata(Base):

    __tablename__ = "model_metadata"


    id = Column(

        Integer,

        primary_key=True,

        index=True
    )


    last_trained_at = Column(

        DateTime,

        default=datetime.utcnow
    )


    last_sales_count = Column(

        Integer,

        default=0
    )