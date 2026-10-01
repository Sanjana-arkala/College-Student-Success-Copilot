
""" Load CSVs from ./data into PostgreSQL. Run: python -m app.db.seed """

import pandas as pd

from app.db.models import Assignment, Attendance, Base, Course, Marks, Student
from app.db.session import SessionLocal, engine

DATA = "data"


def load_table(db, model, filename):
    rows = pd.read_csv(f"{DATA}/{filename}").to_dict("records")
    db.add_all([model(**row) for row in rows])
    db.commit()
    print(f"Loaded {len(rows):>3} rows -> {filename}")


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        load_table(db, Student, "students.csv")
        load_table(db, Course, "courses.csv")
        load_table(db, Attendance, "attendance.csv")
        load_table(db, Marks, "marks.csv")
        load_table(db, Assignment, "assignments.csv")

    print("Seed complete.")


if __name__ == "__main__":
    main()

