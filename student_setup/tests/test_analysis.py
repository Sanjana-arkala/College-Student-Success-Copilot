from app.agents.analysis import analyze_student


def test_flags_multiple_indicators():
    profile = {"student_id": "2023CSE104", "name": "Test", "previous_gpa": 5.9, "backlogs": 2}
    att = [{"subject": "A", "percent": 68}]
    marks = [{"subject": "A", "internal_percent": 43}]
    asg = [{"status": "incomplete"}] * 3
    r = analyze_student(profile, att, marks, asg)
    assert r["needs_attention"] is True
    assert len(r["indicators"]) >= 3


def test_healthy_student_not_flagged():
    profile = {"student_id": "X", "name": "Ok", "previous_gpa": 8.5, "backlogs": 0}
    r = analyze_student(profile, [{"subject": "A", "percent": 90}],
                        [{"subject": "A", "internal_percent": 80}], [{"status": "completed"}])
    assert r["needs_attention"] is False
