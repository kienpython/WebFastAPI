from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import EnrollmentCreate
from services import get_students as gs, create_enrollments as ce
router = APIRouter()

@router.get("/students/{student_id}")
def get_students(student_id:int, db:Session = Depends(get_db)):
    return gs(db, student_id)

@router.post("/enrollments")
def create_enrollments(enrollment: EnrollmentCreate , db:Session = Depends(get_db)):
    return ce(enrollment, db)
    