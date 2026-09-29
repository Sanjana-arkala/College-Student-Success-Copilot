from app.db.models import Student
from app.db.session import SessionLocal
from app.mcp_server.instance import mcp


def _to_dict(s: Student) -> dict:
    return {
        "student_id": s.student_id, "name": s.name, "course": s.course,
        "semester": s.semester, "previous_gpa": s.previous_gpa, "backlogs": s.backlogs,
    }


@mcp.tool()
def get_student(student_id: str) -> dict:
    """Get one student's profile by ID. Returns an error if the student does not exist."""
    with SessionLocal() as db:
        s = db.get(Student, student_id)
        if not s:
            return {"error": "Student not found", "student_id": student_id}
        return _to_dict(s)


@mcp.tool()
def get_students(course: str, semester: int) -> dict:
    """List students for a course (e.g. CSE) and semester."""
    with SessionLocal() as db:
        rows = db.query(Student).filter(Student.course == course, Student.semester == semester).all()
        return {"students": [_to_dict(s) for s in rows]}
