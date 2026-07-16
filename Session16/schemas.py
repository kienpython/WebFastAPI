from pydantic import BaseModel, Field
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int 