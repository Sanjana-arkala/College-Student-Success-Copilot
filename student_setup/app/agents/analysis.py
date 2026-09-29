"""Academic Analysis Agent: rule-based and explainable (AC-05). Thresholds come from config."""
from statistics import mean

from app.config import settings


def analyze_student(profile: dict, attendance: list, marks: list, assignments: list) -> dict:
    avg_att = round(mean(a["percent"] for a in attendance), 1) if attendance else None
    avg_marks = round(mean(m["internal_percent"] for m in marks), 1) if marks else None
    incomplete = sum(1 for a in assignments if a["status"] != "completed")

    indicators = []
    if avg_att is not None and avg_att < settings.min_attendance_percent:
        indicators.append(f"Low attendance ({avg_att}% < {settings.min_attendance_percent}%)")
    if avg_marks is not None and avg_marks < settings.min_internal_marks_percent:
        indicators.append(f"Low internal performance ({avg_marks}% < {settings.min_internal_marks_percent}%)")
    if profile["previous_gpa"] < settings.min_previous_gpa:
        indicators.append(f"Previous academic difficulty (GPA {profile['previous_gpa']} < {settings.min_previous_gpa})")
    if profile["backlogs"] > settings.max_allowed_backlogs:
        indicators.append(f"Backlogs ({profile['backlogs']} > {settings.max_allowed_backlogs})")
    if incomplete > settings.max_incomplete_assignments:
        indicators.append(f"Incomplete assignments ({incomplete})")

    return {
        "student_id": profile["student_id"],
        "name": profile["name"],
        "evidence": {
            "attendance_avg": avg_att, "internal_avg": avg_marks,
            "previous_gpa": profile["previous_gpa"], "backlogs": profile["backlogs"],
            "incomplete_assignments": incomplete,
        },
        "indicators": indicators,
        "needs_attention": len(indicators) >= settings.min_indicators_for_alert,
    }
