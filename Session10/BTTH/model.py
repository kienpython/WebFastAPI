from sqlalchemy import Column, Integer, String
from database import Base

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")
