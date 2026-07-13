from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    students = relationship("Student", back_populates="department")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(60))
    status = Column(String(60))
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    status = Column(String(60))
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, index=True, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")

