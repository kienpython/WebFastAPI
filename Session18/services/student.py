from models.student import Student
from models.department import Department
from models.enrollment import Enrollment
from models.course import Course
def get_students(student_found:Student):
    return {
        "Student": student_found,
        "Department": student_found.department,
        "Course": student_found.course
    }
