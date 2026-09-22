from database import Base
from sqlalchemy import column,Integer,string,Boolean

class post(Base):
    __tablename__ = "products"
    id = column(Integer, primary_key = True,nullable = False)

