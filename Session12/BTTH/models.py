from sqlalchemy import Column, Integer, String
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False)
    subject = Column(String(60), nullable=False)
    document_type = Column(String(60), nullable=False)
    file_url = Column(String(60), nullable=False)