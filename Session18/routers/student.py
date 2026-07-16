from fastapi import APIRouter, Depends
from services.student import get_students as gs
from dependances.student_404_not_found import student_404_not_found
from models.student import Student

router = APIRouter()

@router.get("/students/{student_id}")
def get_students(student_id:int, student_found:Student = Depends(student_404_not_found)):
    return gs(student_found=student_found)

 