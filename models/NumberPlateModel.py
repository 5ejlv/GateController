from sqlalchemy import Column, Integer, String, Date
from database import Base

class NumberPlates(Base):
    __tablename__ = 'NumberPlates'
    
    id = Column(Integer, primary_key=True)
    number_plate = Column(String, nullable=False)
    valid_until = Column(Date, nullable=True)