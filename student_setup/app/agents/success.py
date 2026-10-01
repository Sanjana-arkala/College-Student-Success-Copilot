"""Student Success Agent: recommendations for faculty. Never autonomous decisions (AC-06)."""
from app.agents.llm import ask_llm

SYSTEM = ("You help faculty mentors support students. Given evidence and indicators, recommend "
          "interventions as a short numbered list. These are RECOMMENDATIONS for faculty review, "
          "not decisions about the student's academic status. Base everything on the evidence given.")


def rule_based(analysis: dict) -> list[str]:
    recs = []
    ind = " ".join(analysis["indicators"]).lower()
    if "attendance" in ind:
        recs.append("Faculty mentor discussion to review attendance circumstances")
    if "internal" in ind or "backlogs" in ind:
        recs.append("Subject-wise academic support / remedial classes")
    if "assignments" in ind:
        recs.append("Structured plan to complete pending assignments")
    recs.append("Follow-up assessment after 2-3 weeks")
    return recs


def recommend(analysis: dict, policy_text: str = "") -> dict:
    try:
        text = ask_llm(SYSTEM, f"Analysis: {analysis}\n\nRelevant policy:\n{policy_text}")
    except Exception:
        text = "\n".join(f"{i+1}. {r}" for i, r in enumerate(rule_based(analysis)))
    return {"student_id": analysis["student_id"], "recommendations": text}

