from sqlalchemy import Column, ForeignKey, Index, Integer, String, Float, Date
from app.db.session import Base

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organization.id"))    

    product_name = Column(String(255), index=True)
    
    category = Column(String(255), index=True)

    sales_date = Column(Date, index=True)

    quantity_sold = Column(Integer)

    revenue = Column(Float)

    region = Column(String(10), nullable=True, index=True)

    stock_available = Column(Integer,default=100)

    customer_id = Column(String(100))

    product_id = Column(String(100))
    
    transaction_id = Column(String(100))
    
    customer_age = Column(String(50))
    
    customer_gender = Column(String(50))
    
    customer_segment = Column(String(100))

    __table_args__ = (

    Index("idx_sales_date","sales_date"),

    Index("idx_product_name","product_name"),

    Index("idx_category","category"),

    Index("idx_region","region"),
    
)