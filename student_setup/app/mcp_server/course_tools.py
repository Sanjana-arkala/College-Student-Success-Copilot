from app.db.models import Assignment, Course, Student
from app.db.session import SessionLocal
from app.mcp_server.instance import mcp


@mcp.tool()
def get_courses(student_id: str) -> dict:
    """Subjects a student is enrolled in this semester."""
    with SessionLocal() as db:
        s = db.get(Student, student_id)
        if not s:
            return {"error": "Student not found", "student_id": student_id}
        rows = db.query(Course).filter(Course.course == s.course, Course.semester == s.semester).all()
        return {"student_id": student_id, "subjects": [r.subject for r in rows]}


@mcp.tool()
def get_course_schedule(course: str) -> dict:
    """Class schedule for a course (e.g. CSE)."""
    with SessionLocal() as db:
        rows = db.query(Course).filter(Course.course == course).all()
        return {"schedule": [{"semester": r.semester, "subject": r.subject, "time": r.schedule} for r in rows]}


@mcp.tool()
def get_assignments(student_id: str) -> dict:
    """Assignment/lab status for a student."""
    with SessionLocal() as db:
        rows = db.query(Assignment).filter(Assignment.student_id == student_id).all()
        return {"student_id": student_id,
                "assignments": [{"subject": r.subject, "title": r.title, "status": r.status} for r in rows]}

