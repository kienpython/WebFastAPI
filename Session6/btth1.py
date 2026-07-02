from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class CourseCreate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    fee: float = Field(..., ge=0)


class CourseUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    fee: float = Field(..., ge=0)


def find_course_by_id(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def is_duplicate_code(code: str, course_id: Optional[int] = None):
    for course in courses:
        if course["code"].lower() == code.lower() and course["id"] != course_id:
            return True
    return False


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    if is_duplicate_code(course.code):
        raise HTTPException(status_code=400, detail="Course code already exists")

    new_id = max(item["id"] for item in courses) + 1

    new_course = {
        "id": new_id,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "message": "Create course successfully",
        "data": new_course
    }


@app.get("/courses")
def get_courses(
    keyword: Optional[str] = None,
    min_fee: Optional[float] = None,
    max_fee: Optional[float] = None
):
    result = courses

    if keyword:
        keyword_lower = keyword.lower()
        result = [
            course for course in result
            if keyword_lower in course["name"].lower()
            or keyword_lower in course["code"].lower()
        ]

    if min_fee is not None:
        result = [
            course for course in result
            if course["fee"] >= min_fee
        ]

    if max_fee is not None:
        result = [
            course for course in result
            if course["fee"] <= max_fee
        ]

    return {
        "message": "Get courses successfully",
        "data": result
    }


@app.get("/courses/{course_id}")
def get_course_detail(course_id: int):
    course = find_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return {
        "message": "Get course detail successfully",
        "data": course
    }


@app.put("/courses/{course_id}")
def update_course(course_id: int, course_update: CourseUpdate):
    course = find_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    if is_duplicate_code(course_update.code, course_id):
        raise HTTPException(status_code=400, detail="Course code already exists")

    course["code"] = course_update.code
    course["name"] = course_update.name
    course["duration"] = course_update.duration
    course["fee"] = course_update.fee

    return {
        "message": "Update course successfully",
        "data": course
    }


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    course = find_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    courses.remove(course)

    return {
        "message": "Delete course successfully"
    }