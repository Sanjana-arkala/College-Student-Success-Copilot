from app.db.models import Attendance, Student
from app.db.session import SessionLocal
from app.mcp_server.instance import mcp


@mcp.tool()
def get_attendance(student_id: str) -> dict:
    """Subject-wise attendance percentages for a student."""
    with SessionLocal() as db:
        rows = db.query(Attendance).filter(Attendance.student_id == student_id).all()
        return {"student_id": student_id,
                "attendance": [{"subject": r.subject, "percent": r.attendance_percent} for r in rows]}


@mcp.tool()
def get_class_attendance(course: str, semester: int) -> dict:
    """Attendance records for every student in a course and semester."""
    with SessionLocal() as db:
        rows = (db.query(Attendance).join(Student, Student.student_id == Attendance.student_id)
                .filter(Student.course == course, Student.semester == semester).all())
        return {"records": [{"student_id": r.student_id, "subject": r.subject,
                             "percent": r.attendance_percent} for r in rows]}

