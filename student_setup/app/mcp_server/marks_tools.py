from app.db.models import Marks, Student
from app.db.session import SessionLocal
from app.mcp_server.instance import mcp


@mcp.tool()
def get_marks(student_id: str) -> dict:
    """Subject-wise internal marks (percent) for a student."""
    with SessionLocal() as db:
        rows = db.query(Marks).filter(Marks.student_id == student_id).all()
        return {"student_id": student_id,
                "marks": [{"subject": r.subject, "internal_percent": r.internal_percent} for r in rows]}


@mcp.tool()
def get_course_marks(course: str, semester: int) -> dict:
    """Internal marks for every student in a course and semester."""
    with SessionLocal() as db:
        rows = (db.query(Marks).join(Student, Student.student_id == Marks.student_id)
                .filter(Student.course == course, Student.semester == semester).all())
        return {"records": [{"student_id": r.student_id, "subject": r.subject,
                             "internal_percent": r.internal_percent} for r in rows]}


@mcp.tool()
def get_previous_semester_results(student_id: str) -> dict:
    """Previous semester GPA and current backlog count for a student."""
    with SessionLocal() as db:
        s = db.get(Student, student_id)
        if not s:
            return {"error": "Student not found", "student_id": student_id}
        return {"student_id": student_id, "previous_gpa": s.previous_gpa, "backlogs": s.backlogs}
