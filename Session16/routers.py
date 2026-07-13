from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import Student, Department, Enrollment, Course
from database import get_db

router = APIRouter()

@router.get("/students/{student_id}")
def get_students(student_id:int, db:Session = Depends(get_db)):
    student_found = db.query(Student).filter(Student.id == student_id).first()
    if not student_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found!")
    departments_found = db.query(Department).filter(Department.id == student_found.department_id).first()
    enrollment_ids = db.query(Enrollment).filter(Enrollment.student_id==student_found.id).all()
    course_ids = [enrollment.course_id for enrollment in enrollment_ids]
    course_data = db.query(Course).filter(Course.id.in_(course_ids)).all()
    return {
        "Student": student_found,
        "Department": departments_found,
        "Course": course_data
    }