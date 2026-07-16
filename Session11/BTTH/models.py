# Chỉ chứa models bên trong
from database import Base
from sqlalchemy import Column, Integer, String

class Document(Base):
    __table_name__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    link = Column(String(60))
    category = Column(String(60))
    

