from sqlalchemy.orm import Session, joinedload
from models.student import Student
from fastapi import status, HTTPException, Depends
from database import get_db
def student_404_not_found(student_id:int, db:Session=Depends(get_db)):
    student_found = db.query(Student).options(joinedload(Student.department), joinedload(Student.course)).filter(Student.id == student_id).first()
    if not student_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found!")
    return student_found