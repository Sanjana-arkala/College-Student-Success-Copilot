"""Load CSVs from ./data into PostgreSQL. Run: python -m app.db.seed"""
import pandas as pd

from app.db.models import Assignment, Attendance, Base, Course, Marks, Student
from app.db.session import SessionLocal, engine

DATA = "data"


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        for model, fname in [
            (Student, "students.csv"),
            (Attendance, "attendance.csv"),
            (Marks, "marks.csv"),
            (Assignment, "assignments.csv"),
            (Course, "courses.csv"),
        ]:
            rows = pd.read_csv(f"{DATA}/{fname}").to_dict("records")
            db.add_all([model(**r) for r in rows])
            print(f"Loaded {len(rows):>3} rows -> {fname}")
        db.commit()
    print("Seed complete.")


if __name__ == "__main__":
    main()
