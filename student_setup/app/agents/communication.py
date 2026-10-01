"""Communication Agent: drafts only. Sending requires human approval."""
from app.agents.llm import ask_llm
from app.approvals import create_draft

SYSTEM = ("Draft a short, supportive, non-judgmental message from a faculty mentor to a student "
          "inviting them to meet about their academic progress. Do not mention other students. "
          "Do not state consequences or decisions about academic status.")


def draft_message(analysis: dict) -> dict:
    try:
        body = ask_llm(SYSTEM, f"Student: {analysis['name']}\nIndicators: {analysis['indicators']}")
    except Exception:
        body = (f"Hi {analysis['name']}, I'd like to meet to talk about how the semester is going and "
                "how I can support you. Please let me know a time that works for you.")
    return create_draft("student_message", analysis["student_id"], body)

