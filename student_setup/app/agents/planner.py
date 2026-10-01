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

    plan = {
        "intent": "policy_question",
        "course": "CSE",
        "semester": 6,
        "student_id": sid.group(1).upper() if sid else None,
        "query": message,
    }

    # Class analysis must be checked before intervention_plan,
    # because a class-analysis request may contain the word "intervention".
    if (
        "analy" in m
        or "analyse" in m
        or "identify students" in m
        or "students who may need" in m
        or "class" in m
    ):
        plan["intent"] = "analyze_class"

    elif "draft" in m or "message" in m:
        plan["intent"] = "draft_message"

    elif "intervention" in m or "plan" in m:
        plan["intent"] = "intervention_plan"

    elif sid:
        plan["intent"] = "student_report"

    if sem:
        plan["semester"] = int(sem.group(1)) * (2 if "year" in m else 1)

    return plan


def make_plan(message: str) -> dict:
    # Use deterministic rules for clear intents.
    # This keeps important workflows reliable during the MVP/demo.
    fallback = _fallback(message)
    m = message.lower()

    if (
        "analyze" in m
        or "analyse" in m
        or "identify students" in m
        or "students who may need" in m
    ):
        return fallback

    if not settings.anthropic_api_key:
        return fallback

    try:
        raw = (
            ask_llm(SYSTEM, message)
            .strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )
        plan = json.loads(raw)

        # Safety check: only accept known intents.
        valid_intents = {
            "analyze_class",
            "student_report",
            "policy_question",
            "intervention_plan",
            "draft_message",
        }

        if plan.get("intent") not in valid_intents:
            return fallback

        return plan

    except Exception:
        return fallback

