from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Student, Department, Enrollment, Course
from schemas import EnrollmentCreate

def get_students(db: Session, student_id:int):
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

def create_enrollments(enrollment: EnrollmentCreate, db:Session):
    student_found = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not found!")
    if not (student_found.status == "ACTIVE"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not activate!")
    course_found = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course not found!")
    if not (course_found.status == "OPEN"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course not activate!")
    check_enrollment_exits = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id).first()
    if check_enrollment_exits:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student exits")
    
    new_enrollment = Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return {
        "Message": "Enrolly created successfully!",
        "Data": new_enrollment
    }