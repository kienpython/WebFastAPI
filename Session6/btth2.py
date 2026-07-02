from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class StudentCreate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)


class StudentUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)


def find_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def is_duplicate_code(code: str, student_id: Optional[int] = None):
    for student in students:
        if student["code"].lower() == code.lower() and student["id"] != student_id:
            return True
    return False


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    if is_duplicate_code(student.code):
        raise HTTPException(status_code=400, detail="Student code already exists")

    new_id = max(item["id"] for item in students) + 1

    new_student = {
        "id": new_id,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Create student successfully",
        "data": new_student
    }


@app.get("/students")
def get_students(
    keyword: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None
):
    result = students

    if keyword:
        keyword_lower = keyword.lower()
        result = [
            student for student in result
            if keyword_lower in student["name"].lower()
            or keyword_lower in student["code"].lower()
            or keyword_lower in student["email"].lower()
        ]

    if min_age is not None:
        result = [
            student for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student for student in result
            if student["age"] <= max_age
        ]

    return {
        "message": "Get students successfully",
        "data": result
    }


@app.get("/students/{student_id}")
def get_student_detail(student_id: int):
    student = find_student_by_id(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "message": "Get student detail successfully",
        "data": student
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student_update: StudentUpdate):
    student = find_student_by_id(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if is_duplicate_code(student_update.code, student_id):
        raise HTTPException(status_code=400, detail="Student code already exists")

    student["code"] = student_update.code
    student["name"] = student_update.name
    student["email"] = student_update.email
    student["age"] = student_update.age

    return {
        "message": "Update student successfully",
        "data": student
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = find_student_by_id(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    students.remove(student)

    return {
        "message": "Delete student successfully"
    }