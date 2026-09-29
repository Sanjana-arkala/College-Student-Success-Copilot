from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    course: Mapped[str] = mapped_column(String(20))
    semester: Mapped[int] = mapped_column(Integer)
    previous_gpa: Mapped[float] = mapped_column(Float)
    backlogs: Mapped[int] = mapped_column(Integer, default=0)


class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), index=True)
    subject: Mapped[str] = mapped_column(String(100))
    attendance_percent: Mapped[float] = mapped_column(Float)


class Marks(Base):
    __tablename__ = "marks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), index=True)
    subject: Mapped[str] = mapped_column(String(100))
    internal_percent: Mapped[float] = mapped_column(Float)


class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), index=True)
    subject: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20))  # completed / incomplete


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course: Mapped[str] = mapped_column(String(20))
    semester: Mapped[int] = mapped_column(Integer)
    subject: Mapped[str] = mapped_column(String(100))
    schedule: Mapped[str] = mapped_column(String(100))
