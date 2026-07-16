from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), nullable=False)
    status = Column(String(60), nullable=False)
    # enrollment = relationship("Enrollment", back_populates="course")
    student = relationship("Student",secondary="enrollments", back_populates="course")