"""Generate synthetic college data into ./data. Run: python scripts/generate_data.py"""
import csv
import random

random.seed(42)
SUBJECTS = ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Software Engineering"]
FIRST = ["Aarav", "Diya", "Rohan", "Sneha", "Kiran", "Meera", "Arjun", "Isha", "Vikram", "Anaya", "Rahul", "Priya"]
N = 12
# indices of students seeded as "at risk" so the demo has clear cases
AT_RISK = {3, 7, 10}

students, attendance, marks, assignments, courses = [], [], [], [], []
for i in range(1, N + 1):
    sid = f"2023CSE{100 + i}"
    risky = i in AT_RISK
    gpa = round(random.uniform(5.4, 6.2) if risky else random.uniform(6.8, 9.2), 1)
    backlogs = random.choice([1, 2, 3]) if risky else random.choice([0, 0, 0, 1])
    students.append([sid, f"{FIRST[i-1]} {chr(64+i)}.", "CSE", 6, gpa, backlogs])
    for sub in SUBJECTS:
        att = random.uniform(55, 72) if risky else random.uniform(76, 96)
        mk = random.uniform(32, 48) if risky else random.uniform(55, 92)
        attendance.append([sid, sub, round(att, 1)])
        marks.append([sid, sub, round(mk, 1)])
        for a in (1, 2):
            done = random.random() > (0.6 if risky else 0.08)
            assignments.append([sid, sub, f"Assignment {a}", "completed" if done else "incomplete"])

for j, sub in enumerate(SUBJECTS):
    courses.append(["CSE", 6, sub, f"Day {j+1}, 10:00-11:00"])


def write(name, header, rows):
    with open(f"data/{name}", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


write("students.csv", ["student_id", "name", "course", "semester", "previous_gpa", "backlogs"], students)
write("attendance.csv", ["student_id", "subject", "attendance_percent"], attendance)
write("marks.csv", ["student_id", "subject", "internal_percent"], marks)
write("assignments.csv", ["student_id", "subject", "title", "status"], assignments)
write("courses.csv", ["course", "semester", "subject", "schedule"], courses)
print("Synthetic data written to ./data")
