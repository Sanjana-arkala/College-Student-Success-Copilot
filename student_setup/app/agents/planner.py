"""Planner Agent: classify intent and extract parameters."""
import json
import re

from app.agents.llm import ask_llm
from app.config import settings

SYSTEM = """You are a planner for a college Student Success Copilot.
Classify the request into exactly one intent:
- analyze_class: identify students who may need academic support (needs course, semester)
- student_report: details/evidence for one student (needs student_id)
- policy_question: question about college rules/policies (needs query)
- intervention_plan: recommended actions for one student (needs student_id)
- draft_message: draft a message to a student (needs student_id)
Reply with JSON only: {"intent": "...", "course": "CSE", "semester": 6, "student_id": null, "query": null}"""


def _fallback(message: str) -> dict:
    m = message.lower()
    sid = re.search(r"\b(20\d{2}[a-z]{2,4}\d{3})\b", message, re.I)
    sem = re.search(r"(\d)(?:st|nd|rd|th)?\s*(?:sem|year)", m)
    plan = {"intent": "policy_question", "course": "CSE", "semester": 6,
            "student_id": sid.group(1).upper() if sid else None, "query": message}
    if "draft" in m or "message" in m:
        plan["intent"] = "draft_message"
    elif "intervention" in m or "plan" in m:
        plan["intent"] = "intervention_plan"
    elif "analy" in m or "identify" in m or "class" in m:
        plan["intent"] = "analyze_class"
    elif sid:
        plan["intent"] = "student_report"
    if sem:
        plan["semester"] = int(sem.group(1)) * (2 if "year" in m else 1)
    return plan


def make_plan(message: str) -> dict:
    if not settings.anthropic_api_key:
        return _fallback(message)
    try:
        raw = ask_llm(SYSTEM, message).strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(raw)
    except Exception:
        return _fallback(message)
